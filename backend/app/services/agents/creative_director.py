import logging
import json
from typing import Dict, Any, Callable, Awaitable
from app.services.agents.base import BaseAgent
from app.services.agents.researcher import ResearchAgent
from app.services.agents.style_specialist import StyleSpecialistAgent
from app.services.agents.ideation import IdeationAgent
from app.services.agents.critic import CritiqueBoardAgent
from app.services.agents.revision import RevisionAgent

logger = logging.getLogger(__name__)

class CreativeDirectorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Creative Director", role="Orchestrator")
        self.researcher = ResearchAgent()
        self.style_specialist = StyleSpecialistAgent()
        self.ideation = IdeationAgent()
        self.critic = CritiqueBoardAgent()
        self.revision = RevisionAgent()

    async def execute(self, state: Dict[str, Any], on_state_change: Callable[[str, Dict[str, Any]], Awaitable[None]] = None) -> Dict[str, Any]:
        logger.info("CreativeDirectorAgent started run...")
        
        # Phase 1: Research
        if on_state_change: await on_state_change("RESEARCHING", state)
        state = await self.researcher.execute(state)
        
        # Phase 2: Style
        if on_state_change: await on_state_change("STYLE_ANALYSIS", state)
        state = await self.style_specialist.execute(state)
        
        # Phase 3: Ideation
        if on_state_change: await on_state_change("IDEATING", state)
        state = await self.ideation.execute(state)
        
        # Phase 4: Critique
        if on_state_change: await on_state_change("CRITIQUING", state)
        state = await self.critic.execute(state)
        
        # Phase 5: Revision
        if on_state_change: await on_state_change("REVISING", state)
        state = await self.revision.execute(state)
        
        # Done
        if on_state_change: await on_state_change("COMPLETED", state)
        
        return state

