from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.integrations.embeddings.client import EmbeddingsClient
from app.integrations.embeddings.utils import build_embedding_text_from_vision
from app.repositories.kb_repo import KnowledgeBaseRepository

class RAGService:
    """Service to handle Retrieval-Augmented Generation context building."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.embeddings_client = EmbeddingsClient()
        self.kb_repo = KnowledgeBaseRepository(db)

    async def find_similar_sculptures_from_vision(self, vision_result: Any) -> List[Dict[str, Any]]:
        """
        Takes a vision analysis result, generates an embedding, and finds similar historical sculptures.
        """
        # 1. Build a text representation of the vision analysis
        search_text = build_embedding_text_from_vision(
            iconography=vision_result.iconography,
            motifs=vision_result.motifs,
            style_traits=getattr(vision_result, "style_traits", []),
            deity=vision_result.deity,
            tradition=vision_result.tradition,
            region=vision_result.region
        )
        
        # 2. Generate embedding vector
        query_embedding = await self.embeddings_client.generate_embedding(search_text)
        
        # 3. Retrieve from KB
        matches = await self.kb_repo.find_similar_sculptures(query_embedding, limit=3)
        
        # 4. Format output
        results = []
        for match in matches:
            results.append({
                "id": match.id,
                "title": match.title,
                "period": match.period,
                "region": match.region,
                "material": match.material,
                "similarity": 0.89, # Placeholder: pgvector l2_distance can be converted to similarity score
                "summary": match.summary
            })
            
        return results

    async def search_ancient_texts(self, query: str, limit: int = 3) -> List[str]:
        """
        Searches the Ancient Art KB (Shilpa Shastra rules).
        """
        query_embedding = await self.embeddings_client.generate_embedding(query)
        matches = await self.kb_repo.find_ancient_texts(query_embedding, limit=limit)
        return [match.text for match in matches]
        
    async def search_sculptures(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Searches the Sculpture KB using a raw string query.
        """
        query_embedding = await self.embeddings_client.generate_embedding(query)
        matches = await self.kb_repo.find_similar_sculptures(query_embedding, limit=limit)
        
        results = []
        for match in matches:
            results.append({
                "id": match.id,
                "title": match.title,
                "period": match.period,
                "region": match.region,
                "material": match.material,
                "summary": match.summary
            })
        return results
