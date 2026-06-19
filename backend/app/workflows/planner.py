import logging
import json
from typing import Dict, Any, List
from app.workflows.definitions import WORKFLOW_DEFINITIONS
from app.integrations.watsonx.client import WatsonxClient

logger = logging.getLogger(__name__)

class WorkflowPlanner:
    def __init__(self):
        self.watsonx = WatsonxClient()

    async def plan(self, user_request: str) -> str:
        """
        Dynamically select the best workflow for the user request.
        """
        from app.prompts.registry import PromptRegistry
        prompt_template = await PromptRegistry.get_prompt("planner_agent")
        # Planner prompt needs to receive brief and available workflows
        prompt = prompt_template.format(brief=user_request, workflows=list(WORKFLOW_DEFINITIONS.keys()))
        
        try:
            response_text = self.watsonx.generate_text(prompt, model_id="ibm/granite-13b-chat-v2")
            json_str = response_text[response_text.find("{"):response_text.rfind("}")+1]
            data = json.loads(json_str)
            workflow = data.get("selected_workflow", "creative_generation")
            if workflow not in WORKFLOW_DEFINITIONS:
                workflow = "creative_generation"
            return workflow
        except Exception as e:
            logger.error(f"Planner failed: {e}")
            return "creative_generation"

