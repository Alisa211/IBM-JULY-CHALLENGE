import logging
import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.idea import Idea, RefinedOutput
from app.integrations.granite.client import GraniteClient
from app.integrations.granite.prompts import GRANITE_REFINEMENT_PROMPT

logger = logging.getLogger(__name__)

class GraniteService:
    """Service to handle final style refinement via IBM Granite."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.client = GraniteClient()

    def _calculate_mock_alignment_score(self, style_dna: List[str], refined_text: str) -> float:
        """
        Calculates a mock stylistic alignment score.
        In a real scenario, we would run an Eval prompt or cosine similarity check.
        """
        score = 0.5
        text_lower = refined_text.lower()
        for trait in style_dna:
            # Check if any words from the trait made it into the text
            trait_words = trait.lower().split()
            if any(word in text_lower for word in trait_words if len(word) > 3):
                score += 0.1
                
        return min(0.99, score) # Max out at 0.99

    async def refine_idea(self, idea_id: str, style_dna: List[str]) -> Idea:
        """
        Takes an existing Idea, runs its description through Granite to align with style_dna,
        saves the RefinedOutput record, and updates the Idea.
        """
        # 1. Fetch Idea
        stmt = select(Idea).where(Idea.id == idea_id)
        result = await self.db.execute(stmt)
        idea = result.scalar_one_or_none()
        
        if not idea:
            raise ValueError(f"Idea {idea_id} not found")
            
        original_text = idea.description
        
        # 2. Run through Granite
        refined_text = await self.client.refine_text(
            text=original_text,
            style_dna=style_dna,
            prompt_template=GRANITE_REFINEMENT_PROMPT
        )
        
        # 3. Calculate alignment score
        score = self._calculate_mock_alignment_score(style_dna, refined_text)
        
        # 4. Save RefinedOutput
        refined_output = RefinedOutput(
            id=str(uuid.uuid4()),
            idea_id=idea.id,
            original_text=original_text,
            refined_text=refined_text,
            style_alignment_score=score
        )
        self.db.add(refined_output)
        
        # 5. Update the Idea
        idea.description = refined_text
        idea.status = "refined"
        
        await self.db.commit()
        await self.db.refresh(idea)
        
        logger.info(f"Successfully refined Idea {idea.id} with Granite. Score: {score}")
        
        return idea

