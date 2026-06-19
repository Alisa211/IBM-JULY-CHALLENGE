import logging
import uuid
from typing import Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile

from app.models.asset import Asset
from app.models.analysis import AnalysisResult
from app.integrations.vision.client import VisionClient
from app.services.asset_service import AssetService

logger = logging.getLogger(__name__)

class SculptureService:
    """Service to handle the Sculpture Intelligence Pipeline (Vertical Slice 1)."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.vision_client = VisionClient()
        self.asset_service = AssetService(db)

    async def process_sculpture_upload(self, file: UploadFile, project_id: str = None) -> AnalysisResult:
        """
        Full vertical slice:
        1. Save uploaded image to cloud/local storage
        2. Pass image to Vision AI (Mocked Captioning)
        3. Extract JSON with Granite
        4. Extract stylistic DNA
        5. RAG Retrieval
        """
        # 1. Save Asset
        project_id = project_id or "1"
        asset = await self.asset_service.upload_asset(project_id, file)
        
        # 2. Call Vision AI for Caption
        file.file.seek(0)
        file_bytes = file.file.read()
        
        logger.info(f"Sending asset {asset.id} to Vision Image Captioning...")
        image_description = await self.vision_client.analyze_image(file_bytes, file.content_type, file.filename)
        
        # 3. Extract JSON with Granite
        from app.services.vision_extraction_service import VisionExtractionService
        extractor = VisionExtractionService()
        logger.info(f"Extracting JSON from image description...")
        extracted_json = await extractor.extract_structured_data(image_description)
        
        from app.integrations.vision.types import VisionAnalysisResult
        vision_result = VisionAnalysisResult(
            iconography=extracted_json.get("iconography", []),
            motifs=extracted_json.get("motifs", []),
            composition=extracted_json.get("composition", []),
            confidence=extracted_json.get("confidence", 0.85),
            deity=extracted_json.get("deity"),
            form=extracted_json.get("form"),
            tradition=extracted_json.get("tradition"),
            symbolism=extracted_json.get("symbolism", []),
            materials=extracted_json.get("materials", [])
        )
        
        # 4. Extract Style DNA
        from app.services.style_dna_generator import StyleDNAGenerator
        dna_result = StyleDNAGenerator.generate_style_dna(extracted_json)
        style_traits = dna_result["style_traits"]
        vector_scores = dna_result["vector_scores"]
        
        from app.services.rag_service import RAGService
        
        # 5. Save Analysis Result
        analysis = AnalysisResult(
            id=str(uuid.uuid4()),
            asset_id=asset.id,
            iconography=vision_result.iconography,
            motifs=vision_result.motifs,
            composition_notes=" ".join(vision_result.composition),
            style_traits=style_traits,
            confidence=vision_result.confidence,
            raw_payload={
                "extracted_json": extracted_json,
                "vector_scores": vector_scores
            }
        )
        
        self.db.add(analysis)
        await self.db.commit()
        await self.db.refresh(analysis)
        
        # 6. Connect to Sculpture KB Retrieval (Sprint 2)
        try:
            rag_service = RAGService(self.db)
            similar = await rag_service.find_similar_sculptures_from_vision(vision_result)
        except Exception as e:
            logger.warning(f"RAG search failed: {e}")
            similar = []
            
        # We need to return an object that matches SculptureAnalysisResponse schema
        raw_json = analysis.raw_payload.get("extracted_json", {})
        deity = raw_json.get("deity", "Unknown Deity")
        form = raw_json.get("form", "Unknown Form")
        
        analysis_dict = {
            "id": analysis.id,
            "asset_id": analysis.asset_id,
            "iconography": analysis.iconography,
            "motifs": analysis.motifs,
            "materials": raw_json.get("materials", []),
            "period": raw_json.get("tradition", "Unknown Period"),
            "summary": f"This sculpture depicts {deity} in the {form} form. It belongs to the {raw_json.get('tradition', 'unknown')} tradition.",
            "composition_notes": analysis.composition_notes,
            "style_traits": analysis.style_traits,
            "confidence": analysis.confidence,
            "created_at": analysis.created_at,
            "similar_sculptures": similar
        }
        
        return analysis_dict

