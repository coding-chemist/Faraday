"""Faraday settings — loaded from env. Nested via double underscore (e.g. FARADAY_LLM_CONFIG__HOST)."""
from typing import Any, Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProviderSettings(BaseSettings):
    """Generic provider block: which one + free-form config dict."""
    model_config = SettingsConfigDict(env_nested_delimiter="__", extra="allow")

    provider: str
    config: dict[str, Any] = Field(default_factory=dict)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="FARADAY_",
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    env: Literal["dev", "prod"] = "dev"
    log_level: str = "INFO"
    log_json: bool = False

    database_url: str = "sqlite:///./data/faraday.db"

    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"

    llm: ProviderSettings = Field(
        default_factory=lambda: ProviderSettings(
            provider="ollama",
            config={
                "host": "http://localhost:11434",
                "model": "qwen2.5:7b",
                "embed_model": "nomic-embed-text",
            },
        )
    )

    vector: ProviderSettings = Field(
        default_factory=lambda: ProviderSettings(
            provider="faiss",
            config={"index_path": "./data/faiss_index"},
        )
    )

    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
