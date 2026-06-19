import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Float
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(String, primary_key=True, default=generate_uuid)
    asset_id = Column(String, ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    iconography = Column(JSON, nullable=True) # list of strings
    motifs = Column(JSON, nullable=True) # list of strings
    composition_notes = Column(String, nullable=True)
    style_traits = Column(JSON, nullable=True) # list of strings
    confidence = Column(Float, nullable=True)
    raw_payload = Column(JSON, nullable=True) # store raw vision output
    created_at = Column(DateTime, default=datetime.utcnow)
