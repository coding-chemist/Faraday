"""Vector store provider base + registry. Same pattern as LLMRegistry."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar

from faraday_engine.providers.llm.base import ProviderConfig


@dataclass(frozen=True)
class ScoredId:
    """A vector search result — id of the matched item + similarity score."""
    id: str
    score: float


class VectorProvider(ABC):
    name: ClassVar[str] = ""

    def __init__(self, config: ProviderConfig) -> None:
        self._config = config

    @abstractmethod
    def upsert(self, id: str, vector: list[float]) -> None: ...

    @abstractmethod
    def upsert_batch(self, items: list[tuple[str, list[float]]]) -> None: ...

    @abstractmethod
    def search(self, vector: list[float], k: int = 20) -> list[ScoredId]: ...

    @abstractmethod
    def delete(self, id: str) -> None: ...

    @abstractmethod
    def persist(self) -> None:
        """Write index to disk."""

    @abstractmethod
    def load(self) -> None:
        """Reload index from disk (if exists)."""


class VectorRegistry:
    _providers: ClassVar[dict[str, tuple[type[VectorProvider], type[ProviderConfig]]]] = {}

    @classmethod
    def register(cls, name: str, config: type[ProviderConfig]):
        def wrap(provider_cls: type[VectorProvider]) -> type[VectorProvider]:
            if name in cls._providers:
                raise ValueError(f"Vector provider '{name}' already registered")
            provider_cls.name = name
            cls._providers[name] = (provider_cls, config)
            return provider_cls
        return wrap

    @classmethod
    def resolve(cls, name: str) -> tuple[type[VectorProvider], type[ProviderConfig]]:
        if name not in cls._providers:
            raise ValueError(
                f"Unknown vector provider: '{name}'. "
                f"Available: {sorted(cls._providers.keys())}"
            )
        return cls._providers[name]

    @classmethod
    def list(cls) -> list[str]:
        return sorted(cls._providers.keys())
