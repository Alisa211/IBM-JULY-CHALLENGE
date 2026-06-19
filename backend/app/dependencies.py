from typing import AsyncGenerator, Any
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.database import AsyncSessionLocal
from app.core.redis import get_redis
from app.services.cache_service import CacheService

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Database session dependency.
    
    Yields:
        AsyncSession: Database session
    """
    async with AsyncSessionLocal() as session:
        yield session

def get_cache_service(redis_client: Any = Depends(get_redis)) -> CacheService:
    """
    Cache service dependency.
    
    Args:
        redis_client: Redis client instance
        
    Returns:
        CacheService instance
    """
    from app.services.cache_service import CacheService
    return CacheService(redis_client)

def get_project_service(db: AsyncSession = Depends(get_db)):
    from app.services.project_service import ProjectService
    return ProjectService(db)

def get_asset_service(db: AsyncSession = Depends(get_db)):
    from app.services.asset_service import AssetService
    return AssetService(db)

def get_analysis_service(db: AsyncSession = Depends(get_db), cache = Depends(get_cache_service)):
    from app.services.analysis_service import AnalysisService
    return AnalysisService(db, cache)

def get_idea_service(cache: CacheService = Depends(get_cache_service)):
    from app.services.idea_service import IdeaService
    from app.services.watsonx_service import get_watsonx_service
    from app.core.config import settings
    
    # Initialize Watsonx service
    watsonx_service = get_watsonx_service(
        api_key=settings.WATSONX_API_KEY,
        project_id=settings.WATSONX_PROJECT_ID,
        url=settings.WATSONX_URL,
        model_id=settings.WATSONX_MODEL_ID
    )
    
    return IdeaService(watsonx_service, cache)
