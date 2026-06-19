import asyncio
from dotenv import load_dotenv
load_dotenv("../.env")
from app.integrations.watsonx.client import WatsonxClient

async def main():
    client = WatsonxClient()
    prompt = """You are acting as the Art Historian.
Evaluate the following sculpture concept from your unique perspective.

Concept:
Title: Nataraja Nexus
Description: A massive bronze interactive installation featuring the Nataraja ring of fire.
Rationale: Blends classic Chola bronze traditions with modern public interactive spaces.

Return your evaluation STRICTLY as a JSON object without any markdown formatting or code blocks. Use this exact structure:
{
  "persona": "Art Historian",
  "score": 8.5,
  "feedback": "2 sentences of specific feedback.",
  "strengths": ["Strength 1", "Strength 2"],
  "weaknesses": ["Weakness 1", "Weakness 2"]
}

JSON Response:
"""
    print("Raw Response:")
    res = await asyncio.to_thread(client.generate_text, prompt)
    print(repr(res))
    
if __name__ == "__main__":
    asyncio.run(main())
