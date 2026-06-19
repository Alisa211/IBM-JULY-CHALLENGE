from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import AsyncSessionLocal
from app.services.sculpture_service import SculptureService
from app.schemas.sculpture import SculptureAnalysisResponse

router = APIRouter()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/analyze", response_model=SculptureAnalysisResponse)
async def analyze_sculpture(
    file: UploadFile = File(...),
    project_id: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Vertical Slice #1: Sculpture Intelligence Pipeline.
    Uploads an image, runs IBM Vision AI extraction, derives style traits, and persists the analysis.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")
        
    try:
        service = SculptureService(db)
        analysis = await service.process_sculpture_upload(file, project_id)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

