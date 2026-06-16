"""Shared pytest fixtures."""
import pytest

from tests.fakes.fake_llm import FakeLLMProvider


@pytest.fixture
def fake_llm() -> FakeLLMProvider:
    """A canned-response LLM provider for unit tests — no network, no model."""
    return FakeLLMProvider()
