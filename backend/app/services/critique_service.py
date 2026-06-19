import asyncio
import hashlib
import json
import logging
from typing import Dict, Any
from app.services.cache_service import get_cache_service_instance
from app.integrations.watsonx.client import WatsonxClient

logger = logging.getLogger(__name__)
cache_service = get_cache_service_instance()

CRITIQUE_PROMPT_TEMPLATE = """You are acting as the {persona}.
Evaluate the following sculpture concept from your unique perspective.
Concept:
{idea}

Return your evaluation STRICTLY as a JSON object without any markdown formatting or code blocks. Use this exact structure:
{{
  "persona": "{persona}",
  "score": 8.5,
  "feedback": "2 sentences of specific feedback.",
  "strengths": ["Strength 1", "Strength 2"],
  "weaknesses": ["Weakness 1", "Weakness 2"]
}}

JSON Response:
"""

class CritiqueService:
    def __init__(self):
        self.client = WatsonxClient()

    async def _evaluate(self, idea: str, persona: str) -> Dict[str, Any]:
        prompt = CRITIQUE_PROMPT_TEMPLATE.format(persona=persona, idea=idea)
        
        try:
            # Call Watsonx in a thread
            raw_response = await asyncio.to_thread(self.client.generate_text, prompt)
            
            # Basic cleanup in case LLM wraps it in ```json
            content = raw_response.strip()
            if content.startswith("```json"):
                content = content.replace("```json", "", 1)
                if content.endswith("```"):
                    content = content[:-3]
            content = content.strip()
            
            result = json.loads(content)
            
            # Validate required fields
            return {
                "persona": result.get("persona", persona),
                "score": float(result.get("score", 7.0)),
                "feedback": result.get("feedback", "No feedback provided."),
                "strengths": result.get("strengths", []),
                "weaknesses": result.get("weaknesses", [])
            }
        except Exception as e:
            logger.error(f"Failed to generate critique for {persona}: {e}")
            return {
                "persona": persona,
                "score": 7.0,
                "feedback": "Evaluation failed due to LLM parsing error.",
                "strengths": ["Concept remains intact"],
                "weaknesses": ["Feedback unavailable"]
            }

    async def run_critiques(self, idea_description: str) -> Dict[str, Any]:
        """
        Runs the 4 critique personas in parallel using asyncio.gather.
        """
        query_hash = hashlib.md5(idea_description.encode()).hexdigest()
        
        cached = await cache_service.get("critique", query_hash)
        if cached:
            return cached
            
        results = await asyncio.gather(
            self._evaluate(idea_description, "Art Historian"),
            self._evaluate(idea_description, "Structural Engineer (focusing on materials like Bronze/Polymers)"),
            self._evaluate(idea_description, "Contemporary Curator"),
            self._evaluate(idea_description, "Public Arts Board")
        )
        
        result = {
            "historian": results[0],
            "structural_analyst": results[1],
            "creative_director": results[2],
            "cultural_reviewer": results[3]
        }
        await cache_service.set("critique", query_hash, result, ttl_seconds=86400)
        return result
