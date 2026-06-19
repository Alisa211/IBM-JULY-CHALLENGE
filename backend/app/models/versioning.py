from sqlalchemy import Column, String, Integer, DateTime, JSON
from datetime import datetime
from app.core.database import Base
import uuid

class PromptVersion(Base):
    __tablename__ = "prompt_versions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    prompt_name = Column(String, index=True, nullable=False)
    version = Column(Integer, nullable=False, default=1)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class WorkflowVersion(Base):
    __tablename__ = "workflow_versions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    workflow_name = Column(String, index=True, nullable=False)
    version = Column(Integer, nullable=False, default=1)
    definition = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

