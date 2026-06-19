from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "MuseEngine API"}

def test_ideas_generation_rate_limit(monkeypatch):
    class MockWatsonxClient:
        def __init__(self):
            pass
        def generate_text(self, prompt, params):
            return "Mock text"
    
    from app.services import watsonx_service
    monkeypatch.setattr(watsonx_service, "WatsonxClient", MockWatsonxClient)

    # Make multiple requests to trigger rate limit (configured 10/minute)
    for _ in range(11):
        response = client.post("/api/v1/ideas/generate", json={"brief": "A modern bronze sculpture"})
    
    assert response.status_code == 429 # Too Many Requests

