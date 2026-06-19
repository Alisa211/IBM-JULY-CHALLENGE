import json
import logging
import asyncio
from typing import Dict, Any
from app.integrations.watsonx.client import WatsonxClient

logger = logging.getLogger(__name__)

VISION_EXTRACTION_PROMPT = """You are an expert art historian and appraiser.
Analyze the following sculpture description and extract key structured information.

Description:
{image_description}

Return your analysis STRICTLY as a JSON object without any markdown formatting or code blocks. Use this exact structure:
{{
  "deity": "Name of deity or subject (if recognizable)",
  "form": "Specific form or pose (e.g., Nataraja)",
  "iconography": [
    "Key iconographic element 1",
    "Key iconographic element 2"
  ],
  "tradition": "Artistic tradition or period (e.g., Chola Bronze)",
  "symbolism": [
    "Symbolic meaning 1",
    "Symbolic meaning 2"
  ],
  "motifs": [
    "Decorative motif 1"
  ],
  "materials": [
    "Material 1"
  ],
  "composition": [
    "Compositional element 1"
  ],
  "confidence": 0.95
}}

JSON Response:
"""

class VisionExtractionService:
    def __init__(self):
        self.client = WatsonxClient()
        self.model_id = "ibm/granite-4-h-small"

    async def extract_structured_data(self, image_description: str) -> Dict[str, Any]:
        """
        Uses Granite to parse the unstructured image description into structured JSON.
        """
        prompt = VISION_EXTRACTION_PROMPT.format(image_description=image_description)
        
        try:
            raw_response = await asyncio.to_thread(
                self.client.generate_text, 
                prompt,
                self.model_id
            )
            
            # Basic cleanup in case LLM wraps it in ```json
            content = raw_response.strip()
            if content.startswith("```json"):
                content = content.replace("```json", "", 1)
                if content.endswith("```"):
                    content = content[:-3]
            content = content.strip()
            
            result = json.loads(content)
            
            # If the LLM returned a list instead of a dictionary, take the first element
            if isinstance(result, list) and len(result) > 0:
                result = result[0]
            if not isinstance(result, dict):
                raise ValueError("JSON response is not a dictionary.")
                
            logger.info(f"Successfully extracted vision JSON: {result}")
            
            # Ensure confidence is a float
            if "confidence" in result:
                try:
                    result["confidence"] = float(result["confidence"])
                except ValueError:
                    result["confidence"] = 0.85
            else:
                result["confidence"] = 0.85
                
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Granite extraction response as JSON: {raw_response[:200]}... Error: {e}")
            # Fallback to structured response if LLM fails
            fallback_data = {
                "deity": "Unknown",
                "form": "Generic Sculpture",
                "iconography": ["sculptural form", "artistic representation"],
                "tradition": "Unknown Tradition",
                "symbolism": ["general artistic expression"],
                "motifs": ["traditional craftsmanship", "cultural heritage"],
                "materials": ["unknown material"],
                "composition": ["balanced structure", "focal point"],
                "confidence": 0.6
            }
            return fallback_data
        except Exception as e:
            logger.error(f"Vision Extraction API call failed: {e}")
            fallback_data = {
                "deity": "Unknown",
                "form": "Generic Sculpture",
                "iconography": ["sculptural form", "artistic representation"],
                "tradition": "Unknown Tradition",
                "symbolism": ["general artistic expression"],
                "motifs": ["traditional craftsmanship", "cultural heritage"],
                "materials": ["unknown material"],
                "composition": ["balanced structure", "focal point"],
                "confidence": 0.6
            }
            return fallback_data
