from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from app.schemas.asset import AssetResponse
from app.services.asset_service import AssetService
from app.dependencies import get_asset_service

router = APIRouter()

@router.post("/upload", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def upload_asset(
    project_id: str = Form(...),
    file: UploadFile = File(...),
    service: AssetService = Depends(get_asset_service)
):
    ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp"]
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail=f"File type {file.content_type} not supported. Use JPEG, PNG, or WEBP.")
    return await service.upload_asset(project_id, file)

@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(
    asset_id: str,
    service: AssetService = Depends(get_asset_service)
):
    asset = await service.get_asset(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset
