"""LLM provider base + decorator-based registry.

Adding a new provider = one new file with @LLMRegistry.register("name", config=ConfigClass).
No edits to factories or callers.
"""
from abc import ABC, abstractmethod
from typing import Any, ClassVar

from pydantic import BaseModel


class ProviderConfig(BaseModel):
    """Each LLM provider declares its own config shape by subclassing this."""


class LLMProvider(ABC):
    """Base interface for any LLM provider (Ollama, Claude, OpenAI, ...)."""

    name: ClassVar[str] = ""

    def __init__(self, config: ProviderConfig) -> None:
        self._config = config

    @abstractmethod
    def parse(self, prompt: str, response_model: type[BaseModel], **kwargs: Any) -> BaseModel:
        """Return a validated Pydantic instance — handles structured-output retries internally."""

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Return embedding vector for a single text."""

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Default impl: one-at-a-time. Override for batched APIs."""
        return [self.embed(t) for t in texts]


class LLMRegistry:
    """Name → (provider_cls, config_cls). Populated at import time by decorators."""

    _providers: ClassVar[dict[str, tuple[type[LLMProvider], type[ProviderConfig]]]] = {}

    @classmethod
    def register(cls, name: str, config: type[ProviderConfig]):
        """Decorator — each LLM provider self-registers."""
        def wrap(provider_cls: type[LLMProvider]) -> type[LLMProvider]:
            if name in cls._providers:
                raise ValueError(f"LLM provider '{name}' already registered")
            provider_cls.name = name
            cls._providers[name] = (provider_cls, config)
            return provider_cls
        return wrap

    @classmethod
    def resolve(cls, name: str) -> tuple[type[LLMProvider], type[ProviderConfig]]:
        if name not in cls._providers:
            raise ValueError(
                f"Unknown LLM provider: '{name}'. "
                f"Available: {sorted(cls._providers.keys())}"
            )
        return cls._providers[name]

    @classmethod
    def list(cls) -> list[str]:
        return sorted(cls._providers.keys())
