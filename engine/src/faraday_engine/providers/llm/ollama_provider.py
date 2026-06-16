"""Ollama LLM provider — supports both local (localhost:11434) and Ollama Cloud (ollama.com).

Single class, two modes — toggled by `host` and optional `api_key` in config.
"""
from typing import Any

import instructor
from openai import OpenAI
from pydantic import BaseModel

from faraday_engine.providers.llm.base import LLMProvider, LLMRegistry, ProviderConfig
from faraday_shared.logging import get_logger

log = get_logger(__name__)


class OllamaConfig(ProviderConfig):
    host: str = "http://localhost:11434"
    model: str = "qwen2.5:7b"
    embed_model: str = "nomic-embed-text"
    api_key: str | None = None  # set for Ollama Cloud, leave unset for local
    timeout_s: int = 60
    max_retries: int = 3


@LLMRegistry.register("ollama", config=OllamaConfig)
class OllamaProvider(LLMProvider):
    """Ollama via OpenAI-compatible endpoint. Works for both local Ollama and Ollama Cloud."""

    def __init__(self, config: OllamaConfig) -> None:
        super().__init__(config)
        self._config: OllamaConfig = config
        base_url = config.host.rstrip("/") + "/v1"
        self._raw = OpenAI(
            base_url=base_url,
            api_key=config.api_key or "ollama",  # dummy for local, real for cloud
            timeout=config.timeout_s,
        )
        self._client = instructor.from_openai(self._raw, mode=instructor.Mode.JSON)
        log.info("ollama.init", host=config.host, model=config.model, cloud=bool(config.api_key))

    def parse(self, prompt: str, response_model: type[BaseModel], **kwargs: Any) -> BaseModel:
        return self._client.chat.completions.create(
            model=self._config.model,
            response_model=response_model,
            max_retries=self._config.max_retries,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )

    def embed(self, text: str) -> list[float]:
        resp = self._raw.embeddings.create(model=self._config.embed_model, input=text)
        return resp.data[0].embedding
