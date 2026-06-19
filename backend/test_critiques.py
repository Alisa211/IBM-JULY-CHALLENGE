import asyncio
from dotenv import load_dotenv
load_dotenv("../.env")
from app.services.critique_service import CritiqueService
import json

async def main():
    service = CritiqueService()
    print("Testing Critique Generation...")
    
    idea = """Title: Nataraja Nexus
Description: A massive bronze interactive installation featuring the Nataraja ring of fire.
Rationale: Blends classic Chola bronze traditions with modern public interactive spaces.
"""
    
    critiques = await service.run_critiques(idea)
    print("Critiques Received:")
    for persona, critique in critiques.items():
        print(f"\n--- {persona} ---")
        print(json.dumps(critique, indent=2))
        
if __name__ == "__main__":
    asyncio.run(main())
