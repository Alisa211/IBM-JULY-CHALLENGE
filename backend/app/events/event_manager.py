import logging
import json
from typing import Dict, Any
from app.models.event import Event
from app.core.database import AsyncSessionLocal

logger = logging.getLogger(__name__)

class EventManager:
    @staticmethod
    async def emit(workflow_run_id: str, event_type: str, payload: Dict[str, Any]):
        """
        Emit a structured event, persisting it to the database.
        """
        logger.info(f"Event: {event_type} | Run: {workflow_run_id}")
        try:
            async with AsyncSessionLocal() as db:
                event = Event(
                    workflow_run_id=workflow_run_id,
                    event_type=event_type,
                    payload=payload
                )
                db.add(event)
                await db.commit()
        except Exception as e:
            logger.error(f"Failed to record event {event_type}: {e}")

