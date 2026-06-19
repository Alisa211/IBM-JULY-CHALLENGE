from fastapi import APIRouter, HTTPException, BackgroundTasks, Request, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import os
import asyncio
import redis.asyncio as redis # type: ignore
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.database import AsyncSessionLocal
from sqlalchemy import select
from app.models.workflow_run import WorkflowRun
from app.workflows.planner import WorkflowPlanner
from app.runtime.engine import WorkflowEngine
from app.services.cache_service import get_cache_service_instance
from app.events.event_manager import EventManager

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, db=0, decode_responses=True)
cache_service = get_cache_service_instance()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, run_id: str):
        await websocket.accept()
        if run_id not in self.active_connections:
            self.active_connections[run_id] = []
        self.active_connections[run_id].append(websocket)

    def disconnect(self, websocket: WebSocket, run_id: str):
        if run_id in self.active_connections:
            self.active_connections[run_id].remove(websocket)

    async def broadcast_to_run(self, run_id: str, message: dict):
        if run_id in self.active_connections:
            for connection in self.active_connections[run_id]:
                try:
                    await connection.send_json(message)
                except:
                    pass

manager = ConnectionManager()

class PipelineRequest(BaseModel):
    brief: str
    project_id: Optional[str] = None

async def _run_engine_in_bg(run_id: str):
    engine = WorkflowEngine()
    
    async def on_state_change(state_name: str, state_data: dict):
        await cache_service.set("job", run_id, {"status": state_name, "data": state_data}, ttl_seconds=86400)
        await manager.broadcast_to_run(run_id, {"status": state_name, "data": state_data})
        
    await engine.execute_run(run_id, on_state_change=on_state_change)

@router.post("/run", response_model=Dict[str, Any])
@limiter.limit("10/minute")
async def run_pipeline(request: Request, pipeline_req: PipelineRequest, background_tasks: BackgroundTasks):
    planner = WorkflowPlanner()
    workflow_name = await planner.plan(pipeline_req.brief)
    
    async with AsyncSessionLocal() as db:
        run = WorkflowRun(
            project_id=pipeline_req.project_id,
            workflow_name=workflow_name,
            state={"brief": pipeline_req.brief}
        )
        db.add(run)
        await db.commit()
        await db.refresh(run)
        run_id = run.id
        
    await EventManager.emit(run_id, "WORKFLOW_STARTED", {"workflow_name": workflow_name})
    await cache_service.set("job", run_id, {"status": "CREATED", "progress": 0}, ttl_seconds=86400)
    
    background_tasks.add_task(_run_engine_in_bg, run_id=run_id)
    
    return {"run_id": run_id, "status": "CREATED", "workflow": workflow_name}

class ReviewRequest(BaseModel):
    feedback: Optional[str] = None

@router.post("/{run_id}/resume", response_model=Dict[str, Any])
async def resume_pipeline(run_id: str, background_tasks: BackgroundTasks, review: Optional[ReviewRequest] = None):
    async with AsyncSessionLocal() as db:
        run = await db.get(WorkflowRun, run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
        if run.status != "WAITING_FOR_REVIEW":
            raise HTTPException(status_code=400, detail="Run is not waiting for review")
            
        # Inject feedback into state
        state = dict(run.state or {})
        if review and review.feedback:
            state["reviewer_feedback"] = review.feedback
        run.state = state
            
        # Update status to allow engine to proceed
        run.status = "RUNNING"
        await db.commit()

    await EventManager.emit(run_id, "WORKFLOW_RESUMED", {"feedback_provided": bool(review and review.feedback)})
    background_tasks.add_task(_run_engine_in_bg, run_id=run_id)
    return {"status": "RESUMED"}

@router.post("/{run_id}/pause", response_model=Dict[str, Any])
async def pause_pipeline(run_id: str):
    async with AsyncSessionLocal() as db:
        run = await db.get(WorkflowRun, run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
        run.status = "PAUSED"
        await db.commit()
        
    await EventManager.emit(run_id, "WORKFLOW_PAUSED", {})
    return {"status": "PAUSED"}

@router.get("/jobs/{run_id}", response_model=Dict[str, Any])
async def get_job_status(run_id: str):
    status = await cache_service.get("job", run_id)
    if not status:
        # Fallback to DB
        async with AsyncSessionLocal() as db:
            run = await db.get(WorkflowRun, run_id)
            if run:
                return {"status": run.status, "data": run.state}
        raise HTTPException(status_code=404, detail="Job not found")
    return status

@router.websocket("/ws/{run_id}")
async def websocket_endpoint(websocket: WebSocket, run_id: str):
    await manager.connect(websocket, run_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, run_id)

