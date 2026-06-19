from sqlalchemy import Column, String, JSON
from pgvector.sqlalchemy import Vector
from app.core.database import Base

class StyleProfile(Base):
    __tablename__ = "style_profiles"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    embedding = Column(Vector(384)) # 384 dimensions depending on model (e.g. all-MiniLM-L6-v2)
    traits = Column(JSON, default=list)
