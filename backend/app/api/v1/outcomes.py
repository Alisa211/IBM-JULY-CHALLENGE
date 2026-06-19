import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.analytics import ProjectOutcome
from app.models.idea import Idea

router = APIRouter()

class OutcomeCreate(BaseModel):
    idea_id: str
    project_id: str
    accepted: bool
    feedback: Optional[str] = None

@router.post("/")
async def log_outcome(outcome: OutcomeCreate, db: AsyncSession = Depends(get_db)):
    """
    Logs whether a final Granite-refined Idea was accepted or rejected by the user.
    This feeds the Evolution Engine for future RAG injection.
    """
    # 1. Verify Idea exists
    stmt = select(Idea).where(Idea.id == outcome.idea_id)
    result = await db.execute(stmt)
    idea = result.scalar_one_or_none()
    
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
        
    # 2. Update Idea status
    idea.status = "accepted" if outcome.accepted else "rejected"
    
    # 3. Create Outcome Record
    db_outcome = ProjectOutcome(
        id=str(uuid.uuid4()),
        idea_id=outcome.idea_id,
        project_id=outcome.project_id,
        accepted=outcome.accepted,
        feedback=outcome.feedback
    )
    
    db.add(db_outcome)
    await db.commit()
    
    return {"status": "success", "outcome_id": db_outcome.id}

