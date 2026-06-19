from typing import Dict, Any, Type
from app.services.agents.base import BaseAgent
from app.services.agents.researcher import ResearchAgent
from app.services.agents.style_specialist import StyleSpecialistAgent
from app.services.agents.ideation import IdeationAgent
from app.services.agents.critic import CritiqueBoardAgent
from app.services.agents.revision import RevisionAgent

class AgentRegistry:
    """Registry to map string step names to Agent instances."""
    
    _agents: Dict[str, Type[BaseAgent]] = {
        "research": ResearchAgent,
        "style": StyleSpecialistAgent,
        "generate": IdeationAgent,
        "critique": CritiqueBoardAgent,
        "revise": RevisionAgent
    }

    @classmethod
    def get_agent(cls, step_name: str) -> BaseAgent:
        agent_cls = cls._agents.get(step_name)
        if not agent_cls:
            raise ValueError(f"Agent for step '{step_name}' not found in registry.")
        return agent_cls()

    @classmethod
    def register_agent(cls, step_name: str, agent_cls: Type[BaseAgent]):
        cls._agents[step_name] = agent_cls

