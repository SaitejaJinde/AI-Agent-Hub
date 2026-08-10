import os
from fastapi.testclient import TestClient

from backend.main import app


def test_chat_endpoint_with_mock_llm(monkeypatch):
    # Ensure the app uses the mock LLM for predictable responses
    os.environ["USE_MOCK_LLM"] = "true"

    client = TestClient(app)

    # Root health
    r = client.get("/")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

    # Chat endpoint
    r = client.post("/chat", json={"message": "Hello world"})
    assert r.status_code == 200
    data = r.json()
    assert "response" in data
    assert isinstance(data["response"], str)
    assert "Mock response" in data["response"]
