import asyncio
from dotenv import load_dotenv
load_dotenv("../.env")
from app.services.watsonx_service import WatsonxService

async def main():
    service = WatsonxService()
    print("Testing Idea Generation...")
    ideas = await service.generate_ideas("Create an interactive outdoor installation", 3, "Chola Bronze Nataraja, South India")
    print("Ideas Generated:", len(ideas))
    for i in ideas:
        print("-", i.get("title"))
        
if __name__ == "__main__":
    asyncio.run(main())
