import logging
import json
from typing import Dict, Any
from app.integrations.watsonx.client import WatsonxClient

logger = logging.getLogger(__name__)

class BaseAgent:
    """Base class for all creative agents."""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.watsonx = WatsonxClient()

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's core logic. Must be implemented by subclasses.
        """
        raise NotImplementedError
        
    async def get_prompt(self) -> str:
        """
        Fetch the prompt template for this agent from the PromptRegistry.
        """
        from app.prompts.registry import PromptRegistry
        # Derive prompt name from class name, e.g., ResearchAgent -> researcher_agent
        class_name = self.__class__.__name__
        if class_name == "ResearchAgent":
            return await PromptRegistry.get_prompt("researcher_agent")
        elif class_name == "StyleAgent":
            return await PromptRegistry.get_prompt("style_agent")
        elif class_name == "IdeationAgent":
            return await PromptRegistry.get_prompt("ideation_agent")
        elif class_name == "CritiqueBoardAgent":
            return await PromptRegistry.get_prompt("critique_agent")
        elif class_name == "RevisionAgent":
            return await PromptRegistry.get_prompt("revision_agent")
        return await PromptRegistry.get_prompt(class_name.lower())

    def append_trace(self, state: Dict[str, Any], action: str, details: Any) -> None:
        """
        Appends a reasoning trace entry to the state.
        """
        import datetime
        trace_entry = {
            "agent": self.name,
            "action": action,
            "details": details,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        if "reasoning_trace" not in state:
            state["reasoning_trace"] = []
        state["reasoning_trace"].append(trace_entry)

