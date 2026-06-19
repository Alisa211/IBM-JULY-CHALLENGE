from typing import Dict, Any, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.project import Project
from app.models.idea import Idea

class LearningService:
    """Service responsible for adapting user preferences based on outcomes."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.learning_rate = 0.05  # How much a preference changes per feedback

    async def apply_outcome(self, project_id: str, idea_id: str, accepted: bool) -> Dict[str, Any]:
        """
        Updates the learned preferences for a project based on the idea outcome.
        """
        # Fetch the project
        project_result = await self.db.execute(select(Project).where(Project.id == project_id))
        project = project_result.scalars().first()
        if not project:
            return {"error": "Project not found"}
            
        # Fetch the idea
        idea_result = await self.db.execute(select(Idea).where(Idea.id == idea_id))
        idea = idea_result.scalars().first()
        if not idea:
            return {"error": "Idea not found"}
            
        preferences = project.learned_preferences or {}
        
        # Extract features from idea to learn from (e.g., style keywords, motifs)
        # Assuming the idea has "cultural_references" or "materials" we can weight
        features_to_update = []
        if idea.materials:
            features_to_update.extend([m.strip().lower() for m in idea.materials.split(",")])
        
        # In a real system, we would also extract keywords from the idea content/description
        # For this foundation, we just use a placeholder feature
        features_to_update.append("sacred_geometry") if "sacred" in idea.description.lower() else None
        
        # Apply learning rate
        multiplier = 1.0 if accepted else -1.0
        
        for feature in features_to_update:
            if not feature:
                continue
            current_weight = preferences.get(feature, 0.5) # Default neutral
            # Adjust weight bounded between 0.0 and 1.0
            new_weight = max(0.0, min(1.0, current_weight + (self.learning_rate * multiplier)))
            preferences[feature] = new_weight
            
        project.learned_preferences = preferences
        await self.db.commit()
        
        return preferences

