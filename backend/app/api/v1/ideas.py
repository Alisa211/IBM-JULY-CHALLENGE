from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Any
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.services.watsonx_service import WatsonxService

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

class IdeaRequest(BaseModel):
    brief: str
    style_dna: str = "Classic traditional sculpture"

@router.post("/generate", response_model=List[Dict[str, Any]])
@limiter.limit("10/minute")
async def generate_ideas(request: Request, idea_req: IdeaRequest):
    service = WatsonxService()
    try:
        ideas = await service.generate_ideas(brief=idea_req.brief, style_dna=idea_req.style_dna)
        return ideas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
