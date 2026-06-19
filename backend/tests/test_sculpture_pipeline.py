import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/health/")
    assert response.status_code == 200
    assert "status" in response.json()

@pytest.mark.asyncio
async def test_error_handler():
    # Attempting to hit a non-existent route should return JSON, not HTML
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/this-does-not-exist")
    assert response.status_code == 404
    assert response.headers.get("content-type") == "application/json"

