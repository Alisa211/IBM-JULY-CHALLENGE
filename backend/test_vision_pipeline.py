import asyncio
from dotenv import load_dotenv
load_dotenv("../.env")
from app.integrations.vision.client import VisionClient
from app.services.vision_extraction_service import VisionExtractionService
from app.services.style_dna_generator import StyleDNAGenerator

async def main():
    print("--- Stage 1: Image Captioning ---")
    vision_client = VisionClient()
    # using a mock image bytes
    caption = await vision_client.analyze_image(b"mock_image", filename="nataraja_bronze.jpg")
    print("Image Caption:")
    print(caption)
    
    print("\n--- Stage 2: Granite JSON Extraction ---")
    extractor = VisionExtractionService()
    extracted_json = await extractor.extract_structured_data(caption)
    print("Extracted JSON:")
    import json
    print(json.dumps(extracted_json, indent=2))
    
    print("\n--- Stage 3: Style DNA Generation ---")
    dna = StyleDNAGenerator.generate_style_dna(extracted_json)
    print("Style DNA:")
    print(json.dumps(dna, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
