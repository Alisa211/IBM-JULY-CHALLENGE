from sqlalchemy import Column, String, Integer, Float, DateTime
from datetime import datetime
from app.core.database import Base
import uuid

class AIUsage(Base):
    __tablename__ = "ai_usage"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    workflow_run_id = Column(String, index=True, nullable=True)
    model = Column(String, nullable=False)
    tokens = Column(Integer, default=0)
    latency = Column(Float, default=0.0) # seconds
    cost = Column(Float, default=0.0) # calculated cost
    created_at = Column(DateTime, default=datetime.utcnow)

