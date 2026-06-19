import pytest
from app.services.style_dna_service import StyleDNAService
from app.services.rag_service import RAGService
from app.services.critique_service import CritiqueService

@pytest.mark.asyncio
async def test_style_dna_caching():
    service = StyleDNAService()
    # Execute
    result = await service.create_style_profile("Test Style", "A modern style")
    assert "id" in result
    assert result["name"] == "Test Style"
    
    similar = await service.search_similar_styles("A modern style")
    assert len(similar) > 0

@pytest.mark.asyncio
async def test_rag_caching():
    service = RAGService()
    result = await service.ingest_document("Source 1", "This is some test text")
    assert "id" in result
    
    context = await service.retrieve_context("Test query")
    assert len(context) > 0

@pytest.mark.asyncio
async def test_critique_caching():
    service = CritiqueService()
    result = await service.run_critiques("Idea description")
    assert "historian" in result
    assert "creative_director" in result
    assert "structural_analyst" in result
    assert "cultural_reviewer" in result
