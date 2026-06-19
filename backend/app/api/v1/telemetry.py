from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from sqlalchemy import select, func
from app.core.database import AsyncSessionLocal
from app.models.event import Event
from app.models.ai_usage import AIUsage
from app.models.workflow_run import WorkflowRun

router = APIRouter()

@router.get("/runs/{run_id}/events", response_model=List[Dict[str, Any]])
async def get_run_events(run_id: str):
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Event)
            .where(Event.workflow_run_id == run_id)
            .order_by(Event.timestamp.asc())
        )
        events = result.scalars().all()
        return [
            {
                "id": e.id,
                "event_type": e.event_type,
                "timestamp": e.timestamp.isoformat(),
                "payload": e.payload
            } for e in events
        ]

@router.get("/costs/project/{project_id}")
async def get_project_costs(project_id: str):
    async with AsyncSessionLocal() as db:
        # Get all runs for project
        runs_result = await db.execute(select(WorkflowRun.id).where(WorkflowRun.project_id == project_id))
        run_ids = [row for row in runs_result.scalars().all()]
        
        if not run_ids:
            return {"project_id": project_id, "total_cost": 0.0, "total_tokens": 0}
            
        # Sum AI usage costs
        usage_result = await db.execute(
            select(func.sum(AIUsage.cost).label("total_cost"), func.sum(AIUsage.tokens).label("total_tokens"))
            .where(AIUsage.workflow_run_id.in_(run_ids))
        )
        
        row = usage_result.first()
        return {
            "project_id": project_id,
            "total_cost": float(row.total_cost or 0.0),
            "total_tokens": int(row.total_tokens or 0)
        }

@router.get("/costs/runs/{run_id}")
async def get_run_costs(run_id: str):
    async with AsyncSessionLocal() as db:
        usage_result = await db.execute(
            select(func.sum(AIUsage.cost).label("total_cost"), func.sum(AIUsage.tokens).label("total_tokens"))
            .where(AIUsage.workflow_run_id == run_id)
        )
        row = usage_result.first()
        return {
            "run_id": run_id,
            "total_cost": float(row.total_cost or 0.0),
            "total_tokens": int(row.total_tokens or 0)
        }

from app.models.analytics import ProjectOutcome, PromptRun
from pydantic import BaseModel

class OutcomeRequest(BaseModel):
    project_id: str
    idea_id: str
    accepted: bool
    feedback: str = None

from app.services.learning_service import LearningService

@router.post("/outcomes", response_model=Dict[str, Any])
async def log_outcome(req: OutcomeRequest):
    async with AsyncSessionLocal() as db:
        outcome = ProjectOutcome(
            project_id=req.project_id,
            idea_id=req.idea_id,
            accepted=req.accepted,
            feedback=req.feedback
        )
        db.add(outcome)
        
        # Apply preference learning
        learning_svc = LearningService(db)
        await learning_svc.apply_outcome(req.project_id, req.idea_id, req.accepted)
        
        await db.commit()
        return {"status": "success", "outcome_id": outcome.id}

@router.get("/prompts/analytics", response_model=List[Dict[str, Any]])
async def get_prompt_analytics():
    async with AsyncSessionLocal() as db:
        stmt = select(
            PromptRun.prompt_name,
            PromptRun.prompt_version,
            func.avg(PromptRun.latency).label("avg_latency"),
            func.count(PromptRun.id).label("total_runs")
        ).group_by(PromptRun.prompt_name, PromptRun.prompt_version)
        
        result = await db.execute(stmt)
        rows = result.all()
        
        return [
            {
                "prompt_name": r.prompt_name,
                "prompt_version": r.prompt_version,
                "avg_latency": float(r.avg_latency) if r.avg_latency else 0.0,
                "total_runs": r.total_runs
            } for r in rows
        ]
