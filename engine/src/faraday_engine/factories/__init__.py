"""Factories — construct wired services. Apps call factories; never `new` services directly."""
from faraday_engine.factories.provider_factory import ProviderFactory

__all__ = ["ProviderFactory"]
