from fastapi.testclient import TestClient

import app.main as main_module
from app.main import app


client = TestClient(app)


def test_chat_rejects_empty_message():
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 400


def test_chat_returns_not_found_for_unknown_recipe():
    response = client.post("/chat", json={"message": "¿Cómo hago una mesa de encantamientos?"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "not_found"
    assert data["matched_item"] is None
    assert "No tengo información suficiente" in data["answer"]


def test_chat_accepts_message_field_and_calls_ollama(monkeypatch):
    def fake_ask_ollama(system_prompt: str, user_prompt: str) -> str:
        assert "Pico de madera" in user_prompt
        assert "Reglas obligatorias" in system_prompt
        return "Para fabricar un pico de madera necesitas 3 tablones de madera y 2 palos."

    monkeypatch.setattr(main_module, "ask_ollama", fake_ask_ollama)

    response = client.post("/chat", json={"message": "¿Cómo hago un pico de madera?"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "answered"
    assert data["matched_item"] == "Pico de madera"
    assert data["matched_recipe_id"] == "wooden_pickaxe"
    assert "3 tablones" in data["answer"]


def test_chat_accepts_question_field_for_frontend_compatibility(monkeypatch):
    def fake_ask_ollama(system_prompt: str, user_prompt: str) -> str:
        return "Para fabricar un horno necesitas 8 bloques de roca."

    monkeypatch.setattr(main_module, "ask_ollama", fake_ask_ollama)

    response = client.post("/chat", json={"question": "¿Cómo hago un horno?"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "answered"
    assert data["matched_item"] == "Horno"
