from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.asset import Asset
from app.schemas.asset import AssetCreate
from app.repositories.base import BaseRepository

class AssetRepository(BaseRepository[Asset, AssetCreate, AssetCreate]):
    async def get_by_project(self, db: AsyncSession, project_id: str) -> List[Asset]:
        result = await db.execute(select(self.model).filter(self.model.project_id == project_id))
        return result.scalars().all()

asset_repo = AssetRepository(Asset)
