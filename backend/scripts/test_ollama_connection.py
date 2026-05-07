"""Manual script to verify the local Ollama service before running the chatbot."""

from pathlib import Path
import sys

# Permite ejecutar este archivo directamente desde PowerShell:
# python scripts\test_ollama_connection.py
BACKEND_ROOT = Path(__file__).resolve().parents[1]

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.config import get_settings
from app.ollama_client import ollama_tags, OllamaClientError


if __name__ == "__main__":
    settings = get_settings()

    print(f"Consultando Ollama en: {settings.OLLAMA_BASE_URL}")
    print(f"Modelo configurado: {settings.OLLAMA_MODEL}")

    try:
        data = ollama_tags()

    except OllamaClientError as exc:
        print("OLLAMA NO DISPONIBLE")
        print(exc)
        raise SystemExit(1)

    models = [
        item.get("name") or item.get("model")
        for item in data.get("models", [])
    ]

    print("OLLAMA DISPONIBLE")
    print("Modelos detectados:")

    for model in models:
        print(f"- {model}")

    if settings.OLLAMA_MODEL not in models:
        print(
            f"ADVERTENCIA: no se detectó exactamente el modelo "
            f"{settings.OLLAMA_MODEL}."
        )
        print("Ejecuta: ollama pull llama3.2")