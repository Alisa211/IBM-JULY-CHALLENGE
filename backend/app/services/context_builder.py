from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional

from app.services.rag_service import RAGService
from app.schemas.context import ContextBundle
from app.integrations.discovery.client import DiscoveryClient
from app.services.cache_service import CacheService
from app.services.analytics_service import AnalyticsService

class ContextBuilder:
    """Centralizes context gathering by merging Ancient Art rules, Physical Sculpture precedents, Modern Trends, and Past Outcomes."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.rag_service = RAGService(db)
        self.discovery_client = DiscoveryClient()
        self.cache = CacheService()
        self.analytics = AnalyticsService(db)

    async def build_context_for_prompt(
        self, 
        query: str, 
        style_traits: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None
    ) -> ContextBundle:
        """
        Retrieves from multiple sources, merges, deduplicates, and formats into a ContextBundle.
        """
        # 1. Search Ancient Texts (Shilpa Shastra rules)
        ancient_texts = await self.rag_service.search_ancient_texts(query, limit=3)
        
        # 2. Search Sculpture Precedents
        # We enrich the query with style traits if available to find visually aligned sculptures
        sculpture_query = query
        if style_traits:
            sculpture_query += " " + " ".join(style_traits)
            
        visual_precedents = await self.rag_service.search_sculptures(sculpture_query, limit=3)
        
        # 3. Discovery Trends
        modern_trends = []
        if keywords:
            trend_query = " ".join(keywords)
            cached_trends = await self.cache.get("discovery_trends", trend_query)
            
            if cached_trends:
                modern_trends = cached_trends
            else:
                try:
                    modern_trends = await self.discovery_client.search_trends(trend_query)
                    await self.cache.set("discovery_trends", trend_query, modern_trends, ttl_seconds=86400)
                except Exception as e:
                    # Fallback on error
                    modern_trends = [f"Unable to retrieve live trends for: {trend_query}"]
                    
        # 4. Evolution Engine (Past Outcomes)
        past_outcomes = await self.analytics.find_similar_outcomes(query, limit=2)
        proven_successes = past_outcomes.get("successes", [])
        known_anti_patterns = past_outcomes.get("anti_patterns", [])
        
        # 5. Format Combined Summary for prompt injection
        summary_parts = []
        
        if ancient_texts:
            summary_parts.append("--- ANCIENT TEXTUAL RULES ---")
            for i, text in enumerate(ancient_texts, 1):
                summary_parts.append(f"{i}. {text}")
                
        if visual_precedents:
            summary_parts.append("\n--- HISTORICAL SCULPTURE PRECEDENTS ---")
            for i, prec in enumerate(visual_precedents, 1):
                summary_parts.append(f"{i}. {prec['title']}: {prec['summary']}")
                
        if modern_trends:
            summary_parts.append("\n--- MODERN DESIGN TRENDS ---")
            for i, trend in enumerate(modern_trends, 1):
                summary_parts.append(f"{i}. {trend}")
                
        if proven_successes:
            summary_parts.append("\n--- PROVEN SUCCESSES (Ideas users previously accepted) ---")
            for i, succ in enumerate(proven_successes, 1):
                summary_parts.append(f"{i}. {succ['title']}: {succ['description']}")
                
        if known_anti_patterns:
            summary_parts.append("\n--- KNOWN ANTI-PATTERNS (Ideas users previously rejected) ---")
            for i, anti in enumerate(known_anti_patterns, 1):
                summary_parts.append(f"{i}. {anti['title']}: Avoid this because -> {anti['feedback']}")
                
        if style_traits:
            summary_parts.append("\n--- TARGET STYLE DNA ---")
            summary_parts.append(", ".join(style_traits))

        combined_summary = "\n".join(summary_parts)
        
        return ContextBundle(
            query=query,
            ancient_texts=ancient_texts,
            visual_precedents=visual_precedents,
            style_dna=style_traits or [],
            modern_trends=modern_trends,
            proven_successes=proven_successes,
            known_anti_patterns=known_anti_patterns,
            combined_summary=combined_summary
        )

