from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_ok():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_ok_without_ollama_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["recipes_loaded"] > 0
    assert data["ollama_checked"] is False
