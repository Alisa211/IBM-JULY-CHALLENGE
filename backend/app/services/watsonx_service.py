import asyncio
from typing import List, Dict, Any
from app.integrations.watsonx.client import WatsonxClient
from app.integrations.watsonx.prompts import IDEA_GENERATION_PROMPT
from app.integrations.watsonx.parser import WatsonxParser

class WatsonxService:
    def __init__(self):
        self.client = WatsonxClient()
        self.parser = WatsonxParser()

    async def generate_ideas(self, brief: str, num_ideas: int = 3, style_dna: str = "Classic traditional sculpture") -> List[Dict[str, Any]]:
        """
        Takes a user brief, wraps it in the prompt template, sends it to Watsonx,
        and parses the response into Idea dictionaries.
        """
        prompt = IDEA_GENERATION_PROMPT.format(brief=brief, style_dna=style_dna)
        raw_response = await asyncio.to_thread(self.client.generate_text, prompt)
        ideas = self.parser.parse_ideas(raw_response)
        return ideas
