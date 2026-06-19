import logging
import json
from typing import Dict, Any
from app.services.agents.base import BaseAgent

logger = logging.getLogger(__name__)

class IdeationAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Ideation", role="Generates multiple concept variants")

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("IdeationAgent is running...")
        brief = state.get("brief", "")
        research = state.get("research_summary", {})
        style = state.get("style_profile", {})
        
        prompt_template = await self.get_prompt()
        prompt = prompt_template.format(brief=brief, research=json.dumps(research), style=json.dumps(style))
        
        response_text = self.watsonx.generate_text(prompt, model_id="meta-llama/llama-3-70b-instruct", workflow_run_id=state.get("workflow_run_id"))
        
        try:
            json_str = response_text[response_text.find("["):response_text.rfind("]")+1]
            concepts = json.loads(json_str)
        except Exception as e:
            logger.error(f"Failed to parse Ideation output: {e}")
            concepts = [{
                "title": "Default Concept",
                "description": "A balanced fusion of traditional forms.",
                "artistic_rationale": "Fallback concept due to generation error."
            }]
            
        state["concepts"] = concepts
        
        self.append_trace(state, "Generated Concepts", {"concepts_count": len(concepts)})
        
        return state

