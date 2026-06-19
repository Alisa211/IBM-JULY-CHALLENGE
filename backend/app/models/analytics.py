from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base

class ProjectOutcome(Base):
    __tablename__ = "project_outcomes"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
    idea_id = Column(String, ForeignKey("ideas.id"), nullable=True)
    accepted = Column(Boolean, nullable=False)
    feedback = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class PromptRun(Base):
    __tablename__ = "prompt_runs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    prompt_name = Column(String, nullable=False)
    prompt_version = Column(Integer, nullable=False)
    model = Column(String, nullable=False)
    latency = Column(Float, nullable=False)
    score = Column(Float, nullable=True)  # Critique score or acceptance score
    accepted = Column(Boolean, nullable=True)
    workflow_run_id = Column(String, ForeignKey("workflow_runs.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

