import asyncio
from app.workflows.planner import WorkflowPlanner
from app.runtime.engine import WorkflowEngine
from app.models.workflow_run import WorkflowRun
from app.models.event import Event
from app.models.ai_usage import AIUsage
from app.core.database import AsyncSessionLocal
from sqlalchemy import select

async def test():
    # 1. Plan
    planner = WorkflowPlanner()
    workflow_name = await planner.plan("Create a test concept")
    print("Planned Workflow:", workflow_name)
    
    # 2. Setup run
    async with AsyncSessionLocal() as db:
        run = WorkflowRun(workflow_name=workflow_name, state={"brief": "Create a test concept"})
        db.add(run)
        await db.commit()
        await db.refresh(run)
        run_id = run.id
        
    print("Run ID:", run_id)
    
    # 3. Execute
    engine = WorkflowEngine()
    async def on_state_change(state_name, state_data):
        print(f"STATE -> {state_name}")
        
    await engine.execute_run(run_id, on_state_change=on_state_change)
    
    # 4. Resume if waiting
    async with AsyncSessionLocal() as db:
        run = await db.get(WorkflowRun, run_id)
        if run.status == "WAITING_FOR_REVIEW":
            print("Run is paused. Resuming...")
            run.status = "RUNNING"
            await db.commit()
            await engine.execute_run(run_id, on_state_change=on_state_change)
            
    # 5. Verify events and usage
    async with AsyncSessionLocal() as db:
        events = (await db.execute(select(Event).where(Event.workflow_run_id == run_id))).scalars().all()
        print(f"Recorded {len(events)} events.")
        usages = (await db.execute(select(AIUsage).where(AIUsage.workflow_run_id == run_id))).scalars().all()
        print(f"Recorded {len(usages)} AI calls.")

if __name__ == "__main__":
    asyncio.run(test())

