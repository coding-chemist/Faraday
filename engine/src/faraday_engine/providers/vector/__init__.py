"""Vector providers — base + concrete impls. Imports trigger registration."""
from faraday_engine.providers.vector.base import VectorProvider, VectorRegistry
from faraday_engine.providers.vector.faiss_provider import FAISSConfig, FAISSProvider

__all__ = ["VectorProvider", "VectorRegistry", "FAISSConfig", "FAISSProvider"]
