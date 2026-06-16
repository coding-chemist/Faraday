"""Unit tests for OllamaProvider — focused on the cloud-only quirks
(fence stripping) that can't be reached via the local-Ollama OpenAI path."""
import pytest

from faraday_engine.providers.llm.ollama_provider import _strip_json_fence


class TestStripJsonFence:
    """gpt-oss:* on Ollama Cloud wraps JSON in markdown fences even when
    format='json' is set. The provider strips them before model_validate_json
    so the retry loop doesn't burn three attempts on the same fenced reply."""

    def test_strips_json_language_fence(self) -> None:
        wrapped = '```json\n{"pong": true}\n```'
        assert _strip_json_fence(wrapped) == '{"pong": true}'

    def test_strips_bare_fence_without_language_tag(self) -> None:
        wrapped = '```\n{"a": 1}\n```'
        assert _strip_json_fence(wrapped) == '{"a": 1}'

    def test_handles_uppercase_language_tag(self) -> None:
        wrapped = '```JSON\n{"a": 1}\n```'
        assert _strip_json_fence(wrapped) == '{"a": 1}'

    def test_passes_through_unfenced_json(self) -> None:
        plain = '{"pong": true}'
        assert _strip_json_fence(plain) == plain

    def test_trims_outer_whitespace_around_fence(self) -> None:
        wrapped = '  \n```json\n{"x": 2}\n```\n  '
        assert _strip_json_fence(wrapped) == '{"x": 2}'

    def test_preserves_inner_json_whitespace(self) -> None:
        wrapped = '```json\n{\n  "nested": {\n    "k": 1\n  }\n}\n```'
        assert _strip_json_fence(wrapped) == '{\n  "nested": {\n    "k": 1\n  }\n}'

    def test_trims_unfenced_outer_whitespace(self) -> None:
        assert _strip_json_fence('  {"a": 1}  ') == '{"a": 1}'
