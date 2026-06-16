"""LLM providers — base + concrete impls. Imports trigger registration."""
from faraday_engine.providers.llm.base import LLMProvider, LLMRegistry, ProviderConfig
from faraday_engine.providers.llm.ollama_provider import OllamaConfig, OllamaProvider
from faraday_engine.providers.llm.claude_provider import ClaudeConfig, ClaudeProvider

__all__ = [
    "LLMProvider",
    "LLMRegistry",
    "ProviderConfig",
    "OllamaConfig",
    "OllamaProvider",
    "ClaudeConfig",
    "ClaudeProvider",
]
