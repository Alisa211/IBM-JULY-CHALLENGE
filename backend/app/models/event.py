from sqlalchemy import Column, String, DateTime, JSON
from datetime import datetime
from app.core.database import Base
import uuid

class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    workflow_run_id = Column(String, index=True, nullable=True)
    event_type = Column(String, nullable=False, index=True) # e.g. IDEA_GENERATED, CRITIQUE_COMPLETED
    payload = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

