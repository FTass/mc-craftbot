from functools import lru_cache
from pathlib import Path
import os


class Settings:
    """Centralized backend configuration.

    Values can be overridden using environment variables without changing source code.
    """

    APP_NAME: str = "MC Craftbot Backend"
    APP_VERSION: str = "1.0.0"

    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
    OLLAMA_TIMEOUT_SECONDS: int = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "120"))
    OLLAMA_TEMPERATURE: float = float(os.getenv("OLLAMA_TEMPERATURE", "0.1"))

    # Comma-separated list. Keep explicit localhost origins for Vite during development.
    CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000",
        ).split(",")
        if origin.strip()
    ]

    BASE_DIR: Path = Path(__file__).resolve().parent
    DATA_DIR: Path = BASE_DIR / "data"
    RECIPES_PATH: Path = DATA_DIR / "recipes.json"


@lru_cache
def get_settings() -> Settings:
    return Settings()
