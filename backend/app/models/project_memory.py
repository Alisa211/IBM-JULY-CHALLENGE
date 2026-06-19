from sqlalchemy import Column, String, DateTime, JSON
from datetime import datetime
from app.core.database import Base
import uuid

class ProjectMemory(Base):
    __tablename__ = "project_memory"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    project_id = Column(String, index=True, nullable=False, unique=True)
    historical_decisions = Column(JSON, default=list) # e.g. [{"decision": "Minimalist", "timestamp": "..."}]
    accepted_ideas = Column(JSON, default=list)
    rejected_ideas = Column(JSON, default=list)
    preferences = Column(JSON, default=dict) # e.g. {"style": "Chola", "material": "Bronze"}
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

