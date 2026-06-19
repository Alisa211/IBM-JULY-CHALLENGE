import logging
import json
from typing import Dict, Any
from app.services.agents.base import BaseAgent
from app.services.style_dna_service import StyleDNAService

logger = logging.getLogger(__name__)

class StyleSpecialistAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Style Specialist", role="Formulates visual language and design rules")
        self.style_dna = StyleDNAService()

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("StyleSpecialistAgent is running...")
        brief = state.get("brief", "")
        research = state.get("research_summary", {})
        project_memory = state.get("project_memory", {})
        
        prompt_template = await self.get_prompt()
        prompt = prompt_template.format(brief=brief)
        
        response_text = self.watsonx.generate_text(prompt, model_id="meta-llama/llama-3-70b-instruct", workflow_run_id=state.get("workflow_run_id"))
        
        try:
            # Simple json extraction
            json_str = response_text[response_text.find("{"):response_text.rfind("}")+1]
            style_profile = json.loads(json_str)
        except Exception as e:
            logger.error(f"Failed to parse Style Specialist output: {e}")
            style_profile = {
                "design_rules": ["Integrate traditional forms with modern materials."],
                "visual_language": "Balanced, contemporary, respectful of history."
            }
            
        state["style_profile"] = style_profile
        
        self.append_trace(state, "Generated Style Profile", {"rules_count": len(style_profile.get("design_rules", []))})
        
        return state

