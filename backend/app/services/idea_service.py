"""
Idea Service

Business logic layer for idea generation and management.
Orchestrates Watsonx service, repository, and caching.
"""

import logging
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.idea import Idea
from app.schemas.idea import (
    IdeaCardCreate,
    IdeaCardResponse,
    IdeaGenerateRequest,
    IdeaGenerateResponse,
    IdeaUpdateRequest
)
from app.repositories.idea_repo import idea_repository
from app.services.watsonx_service import WatsonxService
from app.services.cache_service import CacheService

logger = logging.getLogger(__name__)


class IdeaServiceError(Exception):
    """Raised when idea service operations fail"""
    pass


class IdeaService:
    """
    Service layer for idea operations.
    
    Handles:
    - Idea generation via Watsonx
    - Idea persistence
    - Idea retrieval
    - Caching
    """
    
    def __init__(self, watsonx_service: WatsonxService, cache_service: Optional[CacheService] = None):
        """
        Initialize idea service.
        
        Args:
            watsonx_service: Watsonx service instance
            cache_service: Optional cache service instance
        """
        self.watsonx_service = watsonx_service
        self.cache_service = cache_service
        self.repository = idea_repository
        logger.info("IdeaService initialized")
    
    async def generate_ideas(
        self,
        db: AsyncSession,
        request: IdeaGenerateRequest,
        project_id: Optional[str] = None
    ) -> IdeaGenerateResponse:
        """
        Generate new sculpture concept ideas.
        
        Args:
            db: Database session
            request: Idea generation request
            project_id: Optional project ID to associate ideas with
            
        Returns:
            IdeaGenerateResponse with generated ideas
            
        Raises:
            IdeaServiceError: If generation fails
        """
        try:
            logger.info(f"Generating {request.num_ideas} ideas for brief: {request.brief[:100]}...")
            
            # Check cache first (if cache service is available)
            cached_ideas = None
            if self.cache_service:
                cache_key = f"ideas:{hash(request.brief)}:{request.num_ideas}"
                cached_ideas = await self.cache_service.get(cache_key)
            
            if cached_ideas:
                logger.info("Returning cached ideas")
                return IdeaGenerateResponse(**cached_ideas)
            
            # Generate ideas via Watsonx
            raw_ideas = await self.watsonx_service.generate_ideas(
                brief=request.brief,
                num_ideas=request.num_ideas or 3
            )
            
            # Save ideas to database
            saved_ideas = []
            for raw_idea in raw_ideas:
                idea_create = IdeaCardCreate(
                    title=raw_idea['title'],
                    description=raw_idea['description'],
                    artistic_rationale=raw_idea['artistic_rationale'],
                    materials=raw_idea.get('materials'),
                    scale=raw_idea.get('scale'),
                    cultural_references=raw_idea.get('cultural_references'),
                    brief=request.brief,
                    project_id=project_id
                )
                
                saved_idea = await self.repository.create(db, idea_create)
                saved_ideas.append(saved_idea)
            
            # Convert to response schema
            idea_responses = [
                IdeaCardResponse.model_validate(idea)
                for idea in saved_ideas
            ]
            
            # Create response
            response = IdeaGenerateResponse(
                ideas=idea_responses,
                brief=request.brief,
                generated_at=datetime.utcnow(),
                model_used=self.watsonx_service.model_id
            )
            
            # Cache response (if cache service is available)
            if self.cache_service:
                cache_key = f"ideas:{hash(request.brief)}:{request.num_ideas}"
                await self.cache_service.set(
                    cache_key,
                    response.model_dump(),
                    expire=3600  # 1 hour
                )
            
            logger.info(f"Successfully generated and saved {len(saved_ideas)} ideas")
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to generate ideas: {e}")
            raise IdeaServiceError(f"Failed to generate ideas: {str(e)}")
    
    async def get_idea(
        self,
        db: AsyncSession,
        idea_id: str
    ) -> Optional[IdeaCardResponse]:
        """
        Get a specific idea by ID.
        
        Args:
            db: Database session
            idea_id: Idea ID
            
        Returns:
            IdeaCardResponse or None if not found
        """
        try:
            idea = await self.repository.get(db, idea_id)
            if idea:
                return IdeaCardResponse.model_validate(idea)
            return None
        except Exception as e:
            logger.error(f"Failed to get idea {idea_id}: {e}")
            raise IdeaServiceError(f"Failed to get idea: {str(e)}")
    
    async def get_ideas(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[IdeaCardResponse]:
        """
        Get multiple ideas with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of IdeaCardResponse
        """
        try:
            ideas = await self.repository.get_multi(db, skip=skip, limit=limit)
            return [IdeaCardResponse.model_validate(idea) for idea in ideas]
        except Exception as e:
            logger.error(f"Failed to get ideas: {e}")
            raise IdeaServiceError(f"Failed to get ideas: {str(e)}")
    
    async def get_ideas_by_project(
        self,
        db: AsyncSession,
        project_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[IdeaCardResponse]:
        """
        Get ideas for a specific project.
        
        Args:
            db: Database session
            project_id: Project ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of IdeaCardResponse
        """
        try:
            ideas = await self.repository.get_by_project(
                db,
                project_id=project_id,
                skip=skip,
                limit=limit
            )
            return [IdeaCardResponse.model_validate(idea) for idea in ideas]
        except Exception as e:
            logger.error(f"Failed to get ideas for project {project_id}: {e}")
            raise IdeaServiceError(f"Failed to get ideas: {str(e)}")
    
    async def get_recent_ideas(
        self,
        db: AsyncSession,
        limit: int = 10
    ) -> List[IdeaCardResponse]:
        """
        Get most recent ideas.
        
        Args:
            db: Database session
            limit: Maximum number of records to return
            
        Returns:
            List of IdeaCardResponse
        """
        try:
            ideas = await self.repository.get_recent(db, limit=limit)
            return [IdeaCardResponse.model_validate(idea) for idea in ideas]
        except Exception as e:
            logger.error(f"Failed to get recent ideas: {e}")
            raise IdeaServiceError(f"Failed to get recent ideas: {str(e)}")
    
    async def update_idea(
        self,
        db: AsyncSession,
        idea_id: str,
        update_data: IdeaUpdateRequest
    ) -> Optional[IdeaCardResponse]:
        """
        Update an existing idea.
        
        Args:
            db: Database session
            idea_id: Idea ID
            update_data: Update data
            
        Returns:
            Updated IdeaCardResponse or None if not found
        """
        try:
            idea = await self.repository.get(db, idea_id)
            if not idea:
                return None
            
            updated_idea = await self.repository.update(db, idea, update_data)
            return IdeaCardResponse.model_validate(updated_idea)
        except Exception as e:
            logger.error(f"Failed to update idea {idea_id}: {e}")
            raise IdeaServiceError(f"Failed to update idea: {str(e)}")
    
    async def delete_idea(
        self,
        db: AsyncSession,
        idea_id: str
    ) -> bool:
        """
        Delete an idea.
        
        Args:
            db: Database session
            idea_id: Idea ID
            
        Returns:
            True if deleted, False if not found
        """
        try:
            deleted = await self.repository.delete(db, idea_id)
            return deleted is not None
        except Exception as e:
            logger.error(f"Failed to delete idea {idea_id}: {e}")
            raise IdeaServiceError(f"Failed to delete idea: {str(e)}")

# Made with Bob
