from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ContextBundle(BaseModel):
    query: str
    ancient_texts: List[str]
    visual_precedents: List[Dict[str, Any]]
    style_dna: List[str]
    modern_trends: List[str] = []
    proven_successes: List[Dict[str, Any]] = []
    known_anti_patterns: List[Dict[str, Any]] = []
    combined_summary: str
    
    class Config:
        from_attributes = True

