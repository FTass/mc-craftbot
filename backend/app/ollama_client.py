import requests

from app.config import get_settings


class OllamaClientError(RuntimeError):
    pass


def ollama_tags() -> dict:
    settings = get_settings()
    url = f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/tags"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise OllamaClientError(f"No se pudo consultar Ollama en {url}: {exc}") from exc


def is_ollama_available() -> bool:
    try:
        ollama_tags()
        return True
    except OllamaClientError:
        return False


def ask_ollama(system_prompt: str, user_prompt: str) -> str:
    settings = get_settings()
    url = f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/chat"
    payload = {
        "model": settings.OLLAMA_MODEL,
        "stream": False,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "options": {
            "temperature": settings.OLLAMA_TEMPERATURE,
        },
    }

    try:
        response = requests.post(url, json=payload, timeout=settings.OLLAMA_TIMEOUT_SECONDS)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"].strip()
    except requests.exceptions.ConnectionError as exc:
        raise OllamaClientError(
            "No se pudo conectar con Ollama. Verifica que Ollama esté abierto y responda en localhost:11434."
        ) from exc
    except requests.exceptions.Timeout as exc:
        raise OllamaClientError(
            "Ollama tardó demasiado en responder. Prueba una pregunta más simple o verifica el rendimiento del equipo."
        ) from exc
    except KeyError as exc:
        raise OllamaClientError("La respuesta de Ollama no tiene el formato esperado.") from exc
    except requests.RequestException as exc:
        raise OllamaClientError(f"Error HTTP al consultar Ollama: {exc}") from exc
