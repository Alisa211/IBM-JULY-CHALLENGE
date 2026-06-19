from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class AnalysisRequest(BaseModel):
    asset_id: str
    analysis_type: str = "visual"

class AnalysisResultBase(BaseModel):
    asset_id: str
    summary: str
    tags: Optional[List[str]] = None
    confidence: Optional[float] = None

class AnalysisCreate(AnalysisResultBase):
    pass

class AnalysisResponse(AnalysisResultBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class JobResponse(BaseModel):
    job_id: str
    status: str
    message: str
