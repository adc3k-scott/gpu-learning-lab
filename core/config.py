"""
Central configuration — reads from environment / .env files.
All other modules should import settings from here instead of calling os.getenv directly.
"""

from __future__ import annotations

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[".env", ".venv/.env"],
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Anthropic
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-opus-4-5"

    # Redis (optional — in-memory fallback used when not set)
    redis_url: str | None = None

    # API server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    # Paths
    project_root: Path = Path(__file__).resolve().parent.parent

    @property
    def has_redis(self) -> bool:
        return self.redis_url is not None


# Singleton — import and use directly:  from core.config import settings
settings = Settings()
