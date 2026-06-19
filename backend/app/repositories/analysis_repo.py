from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.analysis import AnalysisResult
from app.schemas.analysis import AnalysisCreate
from app.repositories.base import BaseRepository

class AnalysisRepository(BaseRepository[AnalysisResult, AnalysisCreate, AnalysisCreate]):
    async def get_by_asset(self, db: AsyncSession, asset_id: str) -> List[AnalysisResult]:
        result = await db.execute(select(self.model).filter(self.model.asset_id == asset_id))
        return result.scalars().all()

analysis_repo = AnalysisRepository(AnalysisResult)
