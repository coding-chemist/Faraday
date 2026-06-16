"""Provider factory — 6-line lookup, no if/elif. Stays this short whether you have 2 providers or 200."""
from faraday_engine.providers.llm import LLMProvider, LLMRegistry  # noqa: F401 — registration side-effect
from faraday_engine.providers.vector import VectorProvider, VectorRegistry  # noqa: F401
from faraday_shared.config import settings


class ProviderFactory:
    """Resolve provider name → instantiate with config from env-driven settings."""

    @staticmethod
    def create_llm(name: str | None = None) -> LLMProvider:
        name = name or settings.llm.provider
        provider_cls, config_cls = LLMRegistry.resolve(name)
        return provider_cls(config_cls(**settings.llm.config))

    @staticmethod
    def create_vector(name: str | None = None) -> VectorProvider:
        name = name or settings.vector.provider
        provider_cls, config_cls = VectorRegistry.resolve(name)
        return provider_cls(config_cls(**settings.vector.config))
