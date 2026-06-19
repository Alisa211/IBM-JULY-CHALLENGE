"""
Idea Schemas

Pydantic models for idea generation requests and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class IdeaGenerateRequest(BaseModel):
    """Request schema for generating ideas"""
    brief: str = Field(
        ...,
        description="Creative brief describing the desired sculpture concept",
        min_length=10,
        max_length=2000
    )
    num_ideas: Optional[int] = Field(
        default=3,
        description="Number of ideas to generate (1-5)",
        ge=1,
        le=5
    )


class IdeaCardBase(BaseModel):
    """Base schema for idea card"""
    title: str = Field(..., description="Concept title")
    description: str = Field(..., description="Detailed concept description")
    artistic_rationale: str = Field(..., description="Artistic reasoning")
    materials: Optional[str] = Field(None, description="Suggested materials")
    scale: Optional[str] = Field(None, description="Suggested scale/dimensions")
    cultural_references: Optional[str] = Field(None, description="Cultural references")


class IdeaCardCreate(IdeaCardBase):
    """Schema for creating an idea card"""
    project_id: Optional[str] = Field(None, description="Associated project ID")
    brief: str = Field(..., description="Original brief used for generation")


class IdeaCardResponse(IdeaCardBase):
    """Schema for idea card response"""
    id: str
    project_id: Optional[str]
    brief: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IdeaGenerateResponse(BaseModel):
    """Response schema for idea generation"""
    ideas: List[IdeaCardResponse]
    brief: str
    generated_at: datetime
    model_used: str = "ibm/granite-13b-instruct-v2"


class IdeaBatchResponse(BaseModel):
    """Response schema for batch idea retrieval"""
    ideas: List[IdeaCardResponse]
    total: int
    page: int
    page_size: int


class IdeaUpdateRequest(BaseModel):
    """Request schema for updating an idea"""
    title: Optional[str] = None
    description: Optional[str] = None
    artistic_rationale: Optional[str] = None
    materials: Optional[str] = None
    scale: Optional[str] = None
    cultural_references: Optional[str] = None

# Made with Bob
