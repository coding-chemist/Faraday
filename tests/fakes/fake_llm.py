"""FakeLLMProvider — canned responses for unit tests, no network.

Tests set `canned_response`, call the service, then assert what was sent in the prompt
(via `prompts_received`) and that the canned object came back.
"""
from typing import Any

from pydantic import BaseModel

from faraday_engine.providers.llm.base import LLMProvider
from faraday_engine.providers.llm.base import ProviderConfig


class _FakeConfig(ProviderConfig):
    """No real config — the fake doesn't talk to anything."""


class FakeLLMProvider(LLMProvider):
    """Implements LLMProvider with hand-set responses. Records every prompt for assertions."""

    name = "fake"

    def __init__(self) -> None:
        super().__init__(_FakeConfig())
        self.prompts_received: list[str] = []
        self.canned_response: BaseModel | None = None

    def parse(self, prompt: str, response_model: type[BaseModel], **_: Any) -> BaseModel:
        self.prompts_received.append(prompt)
        if self.canned_response is None:
            raise RuntimeError(
                "FakeLLMProvider has no canned_response set. "
                "Tests must assign fake.canned_response before calling parse()."
            )
        return self.canned_response

    def embed(self, text: str) -> list[float]:
        # Deterministic zero vector — tests that need real similarity should mock differently
        return [0.0] * 768
