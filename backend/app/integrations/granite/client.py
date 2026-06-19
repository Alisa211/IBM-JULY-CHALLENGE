import logging
import asyncio
from typing import List
from app.core.config import settings

logger = logging.getLogger(__name__)

class GraniteClient:
    """Client for connecting to IBM Granite models."""
    
    def __init__(self):
        self.api_key = settings.WATSONX_API_KEY
        self.project_id = settings.WATSONX_PROJECT_ID
        self.url = settings.WATSONX_URL
        self.model_id = "ibm/granite-4-h-small"
        
    async def refine_text(self, text: str, style_dna: List[str], prompt_template: str) -> str:
        """
        Sends raw draft text to Granite and forces it to rewrite according to Style DNA.
        """
        from app.integrations.watsonx.client import WatsonxClient
        
        logger.info(f"Sending text to IBM Granite for style refinement...")
        
        # Format the actual prompt
        formatted_prompt = prompt_template.format(
            style_dna=", ".join(style_dna),
            draft_text=text
        )
        
        try:
            watsonx_client = WatsonxClient()
            # Run blocking call in thread
            response = await asyncio.to_thread(
                watsonx_client.generate_text, 
                formatted_prompt, 
                self.model_id
            )
            return response.strip()
        except Exception as e:
            logger.error(f"Failed to refine text: {e}")
            return text + f"\n\n[Refined by Granite (Fallback Mock): {', '.join(style_dna[:2])}]"
