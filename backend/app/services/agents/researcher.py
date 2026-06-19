import logging
import json
from typing import Dict, Any
from app.services.agents.base import BaseAgent
from app.services.context_builder import ContextBuilder
from app.core.database import AsyncSessionLocal

logger = logging.getLogger(__name__)

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Researcher", role="Compiles historical context and modern trends")

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("ResearchAgent is running...")
        brief = state.get("brief", "")
        style_traits = state.get("style_traits", [])
        
        # 1. Use an LLM to quickly extract keywords from the brief for trend searching
        prompt_template = await self.get_prompt()
        prompt = prompt_template.format(brief=brief)
        keywords_str = self.watsonx.generate_text(prompt, model_id="meta-llama/llama-3-70b-instruct", workflow_run_id=state.get("workflow_run_id"))
        keywords = [k.strip() for k in keywords_str.split(",")] if keywords_str else []
        
        # 2. Get full context from ContextBuilder
        async with AsyncSessionLocal() as db:
            context_builder = ContextBuilder(db)
            context_bundle = await context_builder.build_context_for_prompt(brief, style_traits=style_traits, keywords=keywords)
        
        research_summary = {
            "historical_context": [text for text in context_bundle.ancient_texts] + [v["summary"] for v in context_bundle.visual_precedents],
            "modern_trends": context_bundle.modern_trends,
            "keywords": keywords,
            "combined_summary": context_bundle.combined_summary
        }
        
        state["research_summary"] = research_summary
        
        self.append_trace(state, "Completed Research via ContextBuilder", {
            "keywords_extracted": keywords, 
            "rag_sources_used": len(context_bundle.ancient_texts) + len(context_bundle.visual_precedents)
        })
        
        return state

