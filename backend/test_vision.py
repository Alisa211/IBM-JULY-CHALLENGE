import asyncio
import base64
from dotenv import load_dotenv
load_dotenv("../.env")
from app.integrations.vision.client import VisionClient
from app.core.config import settings

async def test_vision():
    client = VisionClient()
    print("Testing VisionClient...")
    try:
        from app.services.sculpture_service import SculptureService
        from app.core.database import AsyncSessionLocal
        import io
        from fastapi import UploadFile
        
        # Create a dummy UploadFile
        dummy_png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")
        file = UploadFile(filename="nataraja_sculpture.png", file=io.BytesIO(dummy_png), headers={"content-type": "image/png"})
        
        async with AsyncSessionLocal() as db:
            service = SculptureService(db)
            analysis = await service.process_sculpture_upload(file)
            print("[SUCCESS] Vision analysis completed!")
            print(analysis)
    except Exception as e:
        print("[ERROR]:", str(e))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_vision())
