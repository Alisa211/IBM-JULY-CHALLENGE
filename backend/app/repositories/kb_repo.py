from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.models.knowledge_chunk import SculptureKBEntry, AncientArtChunk

class KnowledgeBaseRepository:
    """Repository for querying the pgvector Knowledge Base."""
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_similar_sculptures(self, query_embedding: List[float], limit: int = 3) -> List[SculptureKBEntry]:
        """
        Finds the most semantically similar sculptures using pgvector l2_distance.
        """
        # Order by L2 distance (nearest neighbors)
        stmt = (
            select(SculptureKBEntry)
            .order_by(SculptureKBEntry.embedding.l2_distance(query_embedding))
            .limit(limit)
        )
        
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def find_ancient_texts(self, query_embedding: List[float], limit: int = 3) -> List[AncientArtChunk]:
        """
        Finds the most relevant textual rules/shastras using pgvector l2_distance.
        """
        stmt = (
            select(AncientArtChunk)
            .order_by(AncientArtChunk.embedding.l2_distance(query_embedding))
            .limit(limit)
        )
        
        result = await self.db.execute(stmt)
        return result.scalars().all()

