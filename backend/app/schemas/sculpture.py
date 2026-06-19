from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SculptureAnalysisResponse(BaseModel):
    id: str
    asset_id: str
    iconography: List[str]
    motifs: List[str]
    materials: Optional[List[str]] = []
    period: Optional[str] = None
    summary: Optional[str] = None
    composition_notes: Optional[str]
    style_traits: List[str]
    confidence: float
    similar_sculptures: Optional[List[dict]] = []
    created_at: datetime
    
    class Config:
        from_attributes = True

