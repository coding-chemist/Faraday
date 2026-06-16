"""Claude LLM provider — fallback when Ollama Cloud rate-limits or for higher-quality runs."""
from typing import Any

import instructor
from anthropic import Anthropic
from pydantic import BaseModel

from faraday_engine.providers.llm.base import LLMProvider, LLMRegistry, ProviderConfig
from faraday_shared.logging import get_logger

log = get_logger(__name__)


class ClaudeConfig(ProviderConfig):
    api_key: str
    model: str = "claude-opus-4-7"
    embed_model: str = "voyage-3"  # Claude doesn't ship embeddings; route elsewhere if used
    max_retries: int = 3
    max_tokens: int = 4096


@LLMRegistry.register("claude", config=ClaudeConfig)
class ClaudeProvider(LLMProvider):
    def __init__(self, config: ClaudeConfig) -> None:
        super().__init__(config)
        self._config: ClaudeConfig = config
        self._client = instructor.from_anthropic(Anthropic(api_key=config.api_key))
        log.info("claude.init", model=config.model)

    def parse(self, prompt: str, response_model: type[BaseModel], **kwargs: Any) -> BaseModel:
        return self._client.chat.completions.create(
            model=self._config.model,
            response_model=response_model,
            max_retries=self._config.max_retries,
            max_tokens=self._config.max_tokens,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )

    def embed(self, text: str) -> list[float]:
        raise NotImplementedError(
            "Claude does not provide embeddings. Use Ollama (nomic-embed-text) or "
            "sentence-transformers for embeddings, even when using Claude for completions."
        )
