import logging
import json
from typing import Dict, Any, Callable, Awaitable
from datetime import datetime

from app.core.database import AsyncSessionLocal
from sqlalchemy import select
from app.models.workflow_run import WorkflowRun
from app.runtime.registry import AgentRegistry
from app.workflows.definitions import get_workflow
from app.events.event_manager import EventManager

logger = logging.getLogger(__name__)

class WorkflowEngine:
    def __init__(self):
        pass

    async def execute_run(self, run_id: str, on_state_change: Callable[[str, Dict[str, Any]], Awaitable[None]] = None):
        """
        Executes a workflow run, resuming from its current state.
        """
        try:
            async with AsyncSessionLocal() as db:
                run = await db.get(WorkflowRun, run_id)
                if not run:
                    raise ValueError(f"Run {run_id} not found")
                
                if run.status in ["PAUSED", "COMPLETED", "FAILED", "WAITING_FOR_REVIEW"]:
                    logger.info(f"Run {run_id} is in status {run.status}, not executing.")
                    return run.state
                
                workflow_def = get_workflow(run.workflow_name)
                steps = workflow_def.get("steps", [])
                pauses_after = workflow_def.get("pauses_after", [])
                
                state = dict(run.state or {})
                
                # Determine starting index
                start_idx = 0
                if run.current_step and run.current_step in steps:
                    start_idx = steps.index(run.current_step) + 1
                    
                for i in range(start_idx, len(steps)):
                    step_name = steps[i]
                    
                    run.current_step = step_name
                    run.status = "RUNNING"
                    await db.commit()
                    
                    if on_state_change:
                        await on_state_change(step_name.upper(), state)
                        
                    await EventManager.emit(run_id, f"STEP_STARTED_{step_name.upper()}", {"step": step_name})
                    
                    state["workflow_run_id"] = run_id
                    
                    from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

                    # Execute agent with retries
                    agent = AgentRegistry.get_agent(step_name)
                    
                    @retry(
                        stop=stop_after_attempt(3),
                        wait=wait_exponential(multiplier=1, min=2, max=10),
                        reraise=True
                    )
                    async def execute_with_retry(st: Dict[str, Any]) -> Dict[str, Any]:
                        return await agent.execute(st)
                    
                    try:
                        state = await execute_with_retry(state)
                    except Exception as step_exc:
                        logger.error(f"Agent {step_name} failed after retries: {step_exc}")
                        raise step_exc
                    
                    # Save state
                    run.state = state
                    await db.commit()
                    
                    await EventManager.emit(run_id, f"STEP_COMPLETED_{step_name.upper()}", {"step": step_name})
                    
                    if step_name in pauses_after:
                        run.status = "WAITING_FOR_REVIEW"
                        await db.commit()
                        if on_state_change:
                            await on_state_change("WAITING_FOR_REVIEW", state)
                        await EventManager.emit(run_id, "WORKFLOW_PAUSED", {"step": step_name})
                        logger.info(f"Workflow {run_id} paused for review after {step_name}.")
                        return state
                
                run.status = "COMPLETED"
                run.completed_at = datetime.utcnow()
                await db.commit()
                if on_state_change:
                    await on_state_change("COMPLETED", state)
                await EventManager.emit(run_id, "WORKFLOW_COMPLETED", {"status": "success"})
                
                return state
                
        except Exception as e:
            logger.error(f"Workflow Engine failed on run {run_id}: {e}")
            async with AsyncSessionLocal() as db:
                run = await db.get(WorkflowRun, run_id)
                if run:
                    run.status = "FAILED"
                    await db.commit()
            await EventManager.emit(run_id, "WORKFLOW_FAILED", {"error": str(e)})
            if on_state_change:
                await on_state_change("FAILED", {"error": str(e)})
            raise

