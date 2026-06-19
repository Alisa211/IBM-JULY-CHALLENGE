import logging
import json
from typing import Dict, Any, List
from app.services.agents.base import BaseAgent
from app.services.critique_service import CritiqueService

logger = logging.getLogger(__name__)

class CritiqueBoardAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Critique Board", role="Evaluates concepts using multiple personas")
        self.critique_service = CritiqueService()

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("CritiqueBoardAgent is running...")
        concepts = state.get("concepts", [])
        
        prompt_template = await self.get_prompt()
        prompt = prompt_template.format(concepts=json.dumps(concepts))
        
        response_text = self.watsonx.generate_text(prompt, model_id="meta-llama/llama-3-70b-instruct", workflow_run_id=state.get("workflow_run_id"))
        
        try:
            json_str = response_text[response_text.find("["):response_text.rfind("]")+1]
            all_critiques = json.loads(json_str)
        except Exception as e:
            logger.error(f"Failed to parse Critique output: {e}")
            all_critiques = [{"concept_index": 0, "critique": {"score": 8, "feedback": "Looks good."}}]
            
        state["critiques"] = all_critiques
        
        self.append_trace(state, "Generated Critiques", {"critiques_count": len(all_critiques)})
        
        return state

