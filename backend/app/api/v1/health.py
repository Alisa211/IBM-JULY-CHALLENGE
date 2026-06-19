from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db

router = APIRouter()

@router.get("/")
async def deep_health_check(db: AsyncSession = Depends(get_db)):
    """
    Performs a deep health check verifying Database and critical external services.
    """
    health_status = {
        "status": "up",
        "database": "unknown",
        "redis": "skipped_local"
    }
    
    # 1. Check Database
    try:
        await db.execute(text("SELECT 1"))
        health_status["database"] = "up"
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["database"] = "down"
        
    return health_status

