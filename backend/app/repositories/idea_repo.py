"""
Idea Repository

Data access layer for Idea model operations.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.idea import Idea
from app.schemas.idea import IdeaCardCreate, IdeaUpdateRequest
from app.repositories.base import BaseRepository


class IdeaRepository(BaseRepository[Idea, IdeaCardCreate, IdeaUpdateRequest]):
    """Repository for Idea CRUD operations"""
    
    def __init__(self):
        super().__init__(Idea)
    
    async def get_by_project(
        self,
        db: AsyncSession,
        project_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Idea]:
        """
        Get all ideas for a specific project.
        
        Args:
            db: Database session
            project_id: Project ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of Idea objects
        """
        result = await db.execute(
            select(Idea)
            .filter(Idea.project_id == project_id)
            .order_by(desc(Idea.created_at))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_brief(
        self,
        db: AsyncSession,
        brief: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Idea]:
        """
        Get ideas generated from a specific brief.
        
        Args:
            db: Database session
            brief: Brief text to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of Idea objects
        """
        result = await db.execute(
            select(Idea)
            .filter(Idea.brief == brief)
            .order_by(desc(Idea.created_at))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_recent(
        self,
        db: AsyncSession,
        limit: int = 10
    ) -> List[Idea]:
        """
        Get most recent ideas.
        
        Args:
            db: Database session
            limit: Maximum number of records to return
            
        Returns:
            List of Idea objects
        """
        result = await db.execute(
            select(Idea)
            .order_by(desc(Idea.created_at))
            .limit(limit)
        )
        return result.scalars().all()
    
    async def search_by_title(
        self,
        db: AsyncSession,
        search_term: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Idea]:
        """
        Search ideas by title.
        
        Args:
            db: Database session
            search_term: Term to search for in titles
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of Idea objects
        """
        result = await db.execute(
            select(Idea)
            .filter(Idea.title.ilike(f"%{search_term}%"))
            .order_by(desc(Idea.created_at))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def count_by_project(
        self,
        db: AsyncSession,
        project_id: str
    ) -> int:
        """
        Count ideas for a specific project.
        
        Args:
            db: Database session
            project_id: Project ID to count for
            
        Returns:
            Number of ideas
        """
        result = await db.execute(
            select(Idea)
            .filter(Idea.project_id == project_id)
        )
        return len(result.scalars().all())


# Singleton instance
idea_repository = IdeaRepository()

# Made with Bob
