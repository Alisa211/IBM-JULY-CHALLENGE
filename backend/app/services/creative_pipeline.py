import time
import os
import redis.asyncio as redis # type: ignore
from typing import Dict, Any, Callable, Awaitable

from app.services.agents.creative_director import CreativeDirectorAgent
from app.services.cache_service import get_cache_service_instance

import logging
logger = logging.getLogger(__name__)

redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, db=0, decode_responses=True)
cache_service = get_cache_service_instance(redis_client)

class CreativePipeline:
    def __init__(self):
        self.director = CreativeDirectorAgent()

    async def run_pipeline(self, brief: str, job_id: str, on_state_change: Callable[[str, Dict[str, Any]], Awaitable[None]] = None) -> Dict[str, Any]:
        """
        Orchestrates the entire creative reasoning process via the Creative Director Agent.
        """
        try:
            initial_state = {
                "brief": brief,
                "project_memory": {} # To be populated by a future memory service
            }
            
            final_state = await self.director.execute(initial_state, on_state_change=on_state_change)
            
            # The director will have called on_state_change("COMPLETED", state)
            return final_state
            
        except Exception as e:
            logger.error(f"Pipeline failed for {job_id}: {e}")
            if on_state_change:
                await on_state_change("FAILED", {"reason": str(e)})
            raise
