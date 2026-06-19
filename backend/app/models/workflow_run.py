from sqlalchemy import Column, String, DateTime, JSON
from datetime import datetime
from app.core.database import Base
import uuid

class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    project_id = Column(String, index=True, nullable=True) # made nullable to allow independent runs
    workflow_name = Column(String, nullable=False, default="creative_generation")
    current_step = Column(String, nullable=True)
    status = Column(String, default="CREATED") # CREATED, RUNNING, WAITING_FOR_REVIEW, PAUSED, COMPLETED, FAILED
    state = Column(JSON, default=dict)
    reasoning_trace = Column(JSON, default=list)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
