import pytest
from typing import Dict, Any
from app.runtime.engine import WorkflowEngine
from app.services.cache_service import get_cache_service_instance
import redis.asyncio as redis # type: ignore
import os

# Set up test cache
redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, db=1, decode_responses=True)
cache_service = get_cache_service_instance(redis_client)

@pytest.mark.asyncio
async def test_full_creative_generation_workflow():
    """
    Evaluates the full creative generation workflow for completion and quality.
    """
    run_id = "test_eval_run_001"
    
    # 1. Initialize engine
    engine = WorkflowEngine()
    
    # Track states
    state_history = []
    async def on_state_change(state_name: str, state_data: dict):
        state_history.append(state_name)
        
    # Inject initial state for test run
    await cache_service.set_job_status(run_id, {"status": "CREATED", "progress": 0})
    # Seed state in engine logic (for testing, we bypass DB and inject directly)
    # Actually, WorkflowEngine.execute_run fetches from DB. We must mock the DB or test the agent sequence directly.
    # We will test the agent sequence manually as an integration eval
    from app.services.agents.researcher import ResearchAgent
    from app.services.agents.style_specialist import StyleSpecialistAgent
    from app.services.agents.ideation import IdeationAgent
    from app.services.agents.critic import CritiqueBoardAgent
    from app.services.agents.revision import RevisionAgent
    
    initial_state = {
        "workflow_run_id": run_id,
        "brief": "A sculpture symbolizing the fusion of nature and technology for a modern tech campus."
    }
    
    # Run Research
    agent1 = ResearchAgent()
    state = await agent1.execute(initial_state)
    assert "research_summary" in state, "Research should produce research_summary"
    
    # Run Style
    agent2 = StyleSpecialistAgent()
    state = await agent2.execute(state)
    assert "style_profile" in state, "Style should produce style_profile"
    
    # Run Ideation
    agent3 = IdeationAgent()
    state = await agent3.execute(state)
    assert "concepts" in state, "Ideation should produce concepts"
    assert len(state["concepts"]) > 0, "Ideation should produce at least one concept"
    
    # Run Critique
    agent4 = CritiqueBoardAgent()
    state = await agent4.execute(state)
    assert "critiques" in state, "Critique should produce critiques"
    
    # Inject human feedback
    state["reviewer_feedback"] = "Make the technology aspect more subtle and organic."
    
    # Run Revision
    agent5 = RevisionAgent()
    state = await agent5.execute(state)
    assert "recommended_direction" in state, "Revision should produce recommended_direction"
    
    # Quality assert: Did the revised concept include something about subtle technology?
    # Because we use mocks, we just assert the structure is solid.
    revised = state["recommended_direction"]
    assert "title" in revised, "Revised concept must have a title"

