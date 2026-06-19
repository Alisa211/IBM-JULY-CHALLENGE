import asyncio
import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.analysis_repo import analysis_repo
from app.schemas.analysis import AnalysisCreate
from app.models.analysis import AnalysisResult
from app.services.cache_service import CacheService

class AnalysisService:
    def __init__(self, db: AsyncSession, cache: CacheService):
        self.db = db
        self.cache = cache

    async def start_analysis_job(self, asset_id: str, analysis_type: str) -> str:
        job_id = str(uuid.uuid4())
        
        # Track initial job status in Redis
        await self.cache.set_job_status(job_id, {
            "status": "processing",
            "asset_id": asset_id,
            "progress": 0,
            "message": "Analysis started"
        })
        
        # Run background mock simulation (in real life, push to Celery/Kafka)
        asyncio.create_task(self._simulate_analysis(job_id, asset_id))
        
        return job_id

    async def _simulate_analysis(self, job_id: str, asset_id: str):
        # Simulate processing time
        await asyncio.sleep(2)
        await self.cache.set_job_status(job_id, {"status": "processing", "progress": 50, "message": "Extracting features"})
        await asyncio.sleep(3)
        
        # Simulate result
        summary = "Mock analysis summary for the sculpture."
        tags = ["mock-motif", "simulated-tag"]
        confidence = 0.89
        
        # Save to DB
        analysis_in = AnalysisCreate(
            asset_id=asset_id,
            summary=summary,
            tags=tags,
            confidence=confidence
        )
        try:
            db_obj = await analysis_repo.create(self.db, obj_in=analysis_in)
            
            # Cache the result to avoid re-computation
            await self.cache.set(f"analysis:{asset_id}", {
                "id": db_obj.id,
                "summary": summary,
                "tags": tags,
                "confidence": confidence
            })
            
            # Mark job complete
            await self.cache.set_job_status(job_id, {
                "status": "complete",
                "progress": 100,
                "message": "Analysis complete",
                "result_id": db_obj.id
            })
        except Exception as e:
            await self.cache.set_job_status(job_id, {
                "status": "failed",
                "progress": 0,
                "message": str(e)
            })

    async def get_analysis_by_asset(self, asset_id: str) -> List[AnalysisResult]:
        # Check cache first
        cached = await self.cache.get(f"analysis:{asset_id}")
        if cached:
            # Wrap as a list for consistent API if we just return cached dict
            pass # In a real app we'd construct the schema. For now, fetch from DB.

        return await analysis_repo.get_by_asset(self.db, asset_id=asset_id)
