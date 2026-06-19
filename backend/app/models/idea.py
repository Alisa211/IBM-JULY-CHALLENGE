"""
Idea Model

SQLAlchemy model for storing generated idea cards.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class Idea(Base):
    """
    Idea Card Model
    
    Stores AI-generated sculpture concept ideas with all relevant details.
    """
    __tablename__ = "ideas"

    id = Column(String, primary_key=True, default=generate_uuid)
    
    # Core content
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    artistic_rationale = Column(Text, nullable=False)
    
    # Optional details
    materials = Column(String(500), nullable=True)
    scale = Column(String(200), nullable=True)
    cultural_references = Column(Text, nullable=True)
    
    # Generation metadata
    brief = Column(Text, nullable=False)
    project_id = Column(String, ForeignKey("projects.id"), nullable=True, index=True)
    workflow_run_id = Column(String, ForeignKey("workflow_runs.id"), nullable=True)
    
    # Revisions and Variants
    parent_idea_id = Column(String, ForeignKey("ideas.id"), nullable=True)
    version = Column(String, default="v1.0") # e.g. v1.0, v2.0 (after revision)
    status = Column(String, default="generated") # generated, accepted, rejected, revised
    
    # Vector Embedding for Semantic Search (Evolution Engine)
    embedding = Column(Vector(1536), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    # project = relationship("Project", back_populates="ideas")
    
    def __repr__(self):
        return f"<Idea(id={self.id}, title={self.title})>"

class RefinedOutput(Base):
    """
    Refined Output Model
    
    Stores the stylistic refinement deltas applied by the Granite model.
    """
    __tablename__ = "refined_outputs"

    id = Column(String, primary_key=True, default=generate_uuid)
    idea_id = Column(String, ForeignKey("ideas.id", ondelete="CASCADE"), nullable=False, index=True)
    original_text = Column(Text, nullable=False)
    refined_text = Column(Text, nullable=False)
    style_alignment_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
