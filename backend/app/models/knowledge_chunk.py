from sqlalchemy import Column, String, Text, JSON
from pgvector.sqlalchemy import Vector
from app.core.database import Base

class AncientArtChunk(Base):
    __tablename__ = "ancient_art_chunks"

    id = Column(String, primary_key=True, index=True)
    source = Column(String, nullable=False) # e.g., "Shilpa Shastra Vol 1"
    text = Column(Text, nullable=False)
    embedding = Column(Vector(384)) # 384 dimensions

class SculptureKBEntry(Base):
    __tablename__ = "sculpture_kb_entries"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    period = Column(String, nullable=True)
    region = Column(String, nullable=True)
    material = Column(String, nullable=True)
    iconography = Column(JSON, nullable=True)
    summary = Column(Text, nullable=True)
    embedding = Column(Vector(384))
    source = Column(String, nullable=True)
