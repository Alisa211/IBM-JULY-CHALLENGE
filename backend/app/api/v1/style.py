from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from app.services.style_dna_service import StyleDNAService

router = APIRouter()

class StyleCreateRequest(BaseModel):
    name: str
    description: str

class StyleSearchRequest(BaseModel):
    description: str

@router.post("/create", response_model=Dict[str, Any])
async def create_style(request: StyleCreateRequest):
    service = StyleDNAService()
    try:
        profile = await service.create_style_profile(name=request.name, description=request.description)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=List[Dict[str, Any]])
async def search_styles(request: StyleSearchRequest):
    service = StyleDNAService()
    try:
        results = await service.search_similar_styles(description=request.description)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
