from pydantic import BaseModel
from typing import List, Optional

class VisionAnalysisResult(BaseModel):
    iconography: List[str]
    motifs: List[str]
    composition: List[str]
    confidence: float
    deity: Optional[str] = None
    form: Optional[str] = None
    tradition: Optional[str] = None
    region: Optional[str] = None
    symbolism: List[str] = []
    materials: List[str] = []

