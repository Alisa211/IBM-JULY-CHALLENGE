import logging
import json
from typing import Dict, Any
from app.services.agents.base import BaseAgent

logger = logging.getLogger(__name__)

class RevisionAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Revision", role="Improves concepts based on critique")

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("RevisionAgent is running...")
        concepts = state.get("concepts", [])
        critiques = state.get("critiques", [])
        
        if not concepts or not critiques:
            state["recommended_direction"] = concepts[0] if concepts else {}
            return state

        # We will revise the first concept based on its critiques
        top_concept = concepts[0]
        top_critique = critiques[0].get("critique", {})
        
        reviewer_feedback = state.get("reviewer_feedback", "No specific human feedback.")
        
        prompt_template = await self.get_prompt()
        prompt = prompt_template.format(
            concepts=json.dumps([top_concept]),
            critique=json.dumps(top_critique),
            feedback=reviewer_feedback
        )
        
        response_text = self.watsonx.generate_text(prompt, model_id="meta-llama/llama-3-70b-instruct", workflow_run_id=state.get("workflow_run_id"))
        
        from app.integrations.granite.client import GraniteClient
        from app.integrations.granite.prompts import GRANITE_REFINEMENT_PROMPT
        
        try:
            json_str = response_text[response_text.find("{"):response_text.rfind("}")+1]
            revised_concept = json.loads(json_str)
        except Exception as e:
            logger.error(f"Failed to parse Revision output: {e}")
            revised_concept = top_concept
            revised_concept["title"] += " (Revised)"
            
        # --- GRANITE REFINEMENT ---
        style_traits = state.get("style_traits", [])
        if style_traits and "description" in revised_concept:
            logger.info("Passing revised concept to IBM Granite for style alignment...")
            granite_client = GraniteClient()
            refined_desc = await granite_client.refine_text(
                text=revised_concept["description"],
                style_dna=style_traits,
                prompt_template=GRANITE_REFINEMENT_PROMPT
            )
            revised_concept["description"] = refined_desc
            logger.info("Granite Refinement complete.")
            
        state["recommended_direction"] = revised_concept
        
        # Determine next steps
        state["next_steps"] = [
            "Review the final dossier.",
            "Select materials and scale.",
            "Generate 3D mockup based on the revised concept."
        ]
        
        self.append_trace(state, "Generated Revision", {"feedback_used": reviewer_feedback, "final_title": revised_concept.get("title")})
        
        return state

