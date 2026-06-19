import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.idea import Idea
from app.models.analytics import ProjectOutcome
from app.integrations.embeddings.client import EmbeddingsClient

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Handles logic for the Stage 9 Evolution Engine (Learning from past outcomes)."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.embeddings = EmbeddingsClient()

    async def find_similar_outcomes(self, query: str, limit: int = 2) -> Dict[str, List[Dict[str, Any]]]:
        """
        Semantic search for past ideas similar to the current prompt.
        Returns a dict separating them by accepted vs rejected.
        """
        logger.info(f"Searching for past outcomes matching: {query}")
        query_embedding = await self.embeddings.get_embedding(query)
        
        # We want to find Ideas that have an associated ProjectOutcome
        stmt = (
            select(Idea, ProjectOutcome)
            .join(ProjectOutcome, Idea.id == ProjectOutcome.idea_id)
            .where(Idea.embedding.is_not(None))
            .order_by(Idea.embedding.cosine_distance(query_embedding))
            .limit(limit * 2) # Fetch extra so we can split them
        )
        
        result = await self.db.execute(stmt)
        rows = result.all()
        
        outcomes = {
            "successes": [],
            "anti_patterns": []
        }
        
        for idea, outcome in rows:
            data = {
                "title": idea.title,
                "description": idea.description,
                "feedback": outcome.feedback
            }
            if outcome.accepted:
                outcomes["successes"].append(data)
            else:
                outcomes["anti_patterns"].append(data)
                
        # Trim to limit
        outcomes["successes"] = outcomes["successes"][:limit]
        outcomes["anti_patterns"] = outcomes["anti_patterns"][:limit]
        
        return outcomes

