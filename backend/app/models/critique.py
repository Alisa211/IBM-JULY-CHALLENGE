from sqlalchemy import Column, String, Float, DateTime, Text, JSON
from datetime import datetime
from app.core.database import Base
import uuid

class Critique(Base):
    __tablename__ = "critiques"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    idea_id = Column(String, index=True, nullable=False)
    persona = Column(String, nullable=False) # Historian, Creative Director, etc.
    score = Column(Float, nullable=False)
    feedback = Column(Text, nullable=False)
    strengths = Column(JSON, default=list)
    weaknesses = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
