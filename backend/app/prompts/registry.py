from sqlalchemy import select, desc
from app.core.database import AsyncSessionLocal
from app.models.versioning import PromptVersion
import logging

logger = logging.getLogger(__name__)

class PromptRegistry:
    
    DEFAULT_PROMPTS = {
        "planner_agent": "Analyze the following brief and determine the workflow to use.\nAvailable workflows: {workflows}\nBrief: {brief}\n\nReturn just the workflow name (e.g. creative_generation, style_analysis, concept_only).",
        "researcher_agent": "Extract 3 main keywords from this brief to search for modern trends and cultural context:\nBrief: {brief}\nKeywords (comma separated):",
        "style_agent": "Generate a JSON string defining the style parameters for the following brief.\nBrief: {brief}\nJSON:",
        "ideation_agent": "Generate 3 creative concepts based on the following context.\nBrief: {brief}\nResearch: {research}\nStyle: {style}\nConcepts (JSON array):",
        "critique_agent": "Critique the following concepts from multiple personas (Historian, Curator, Critic, Audience).\nConcepts: {concepts}\nCritique (JSON array):",
        "revision_agent": "Revise the concepts based on the critique.\nOriginal Concepts: {concepts}\nCritique: {critique}\nReviewer Notes: {feedback}\nRevised Concepts (JSON array):"
    }

    @classmethod
    async def get_prompt(cls, prompt_name: str) -> str:
        try:
            async with AsyncSessionLocal() as db:
                stmt = select(PromptVersion).where(PromptVersion.prompt_name == prompt_name).order_by(desc(PromptVersion.version)).limit(1)
                result = await db.execute(stmt)
                version = result.scalars().first()
                if version:
                    return version.content
        except Exception as e:
            logger.error(f"Failed to fetch prompt '{prompt_name}' from DB: {e}. Falling back to default.")
            
        return cls.DEFAULT_PROMPTS.get(prompt_name, "")

    @classmethod
    async def save_prompt(cls, prompt_name: str, content: str) -> PromptVersion:
        async with AsyncSessionLocal() as db:
            stmt = select(PromptVersion).where(PromptVersion.prompt_name == prompt_name).order_by(desc(PromptVersion.version)).limit(1)
            result = await db.execute(stmt)
            latest = result.scalars().first()
            
            new_version = 1 if not latest else latest.version + 1
            prompt_v = PromptVersion(
                prompt_name=prompt_name,
                version=new_version,
                content=content
            )
            db.add(prompt_v)
            await db.commit()
            await db.refresh(prompt_v)
            return prompt_v

