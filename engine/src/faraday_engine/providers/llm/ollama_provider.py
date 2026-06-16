"""Ollama LLM provider — handles BOTH local Ollama AND Ollama Cloud.
//
// The two endpoint families are different:
//   Local Ollama  (http://localhost:11434)  exposes OpenAI-compat at /v1/*
//                                            (Ollama's own translation layer)
//   Ollama Cloud  (https://ollama.com)      ONLY exposes the native /api/*
//                                            endpoints, no /v1/* compat layer
//
// So we branch: cloud mode (api_key set) uses the native `ollama` library;
// local mode uses OpenAI SDK + instructor for structured-output retries.
"""
import json
from typing import Any

import instructor
from ollama import Client as OllamaClient
from openai import OpenAI
from pydantic import BaseModel
from pydantic import ValidationError

from faraday_engine.providers.llm.base import LLMProvider
from faraday_engine.providers.llm.base import LLMRegistry
from faraday_engine.providers.llm.base import ProviderConfig
from faraday_shared.logging import get_logger

log = get_logger(__name__)


class OllamaConfig(ProviderConfig):
    host: str = "http://localhost:11434"
    model: str = "qwen2.5:7b"
    embed_model: str = "nomic-embed-text"
    api_key: str | None = None  # set for Ollama Cloud, leave unset for local
    timeout_s: int = 60
    max_retries: int = 3


@LLMRegistry.register("ollama", config=OllamaConfig)
class OllamaProvider(LLMProvider):
    """Branches on `api_key` presence to talk to either local or cloud Ollama."""

    def __init__(self, config: OllamaConfig) -> None:
        super().__init__(config)
        self._config: OllamaConfig = config
        self._is_cloud = bool(config.api_key)

        if self._is_cloud:
            headers = {"Authorization": f"Bearer {config.api_key}"}
            self._cloud = OllamaClient(host=config.host, headers=headers, timeout=config.timeout_s)
            self._local = None
            self._instructor = None
        else:
            base_url = config.host.rstrip("/") + "/v1"
            self._local = OpenAI(
                base_url=base_url,
                api_key=config.api_key or "ollama",
                timeout=config.timeout_s,
            )
            self._instructor = instructor.from_openai(self._local, mode=instructor.Mode.JSON)
            self._cloud = None

        log.info(
            "ollama.init",
            host=config.host,
            model=config.model,
            embed_model=config.embed_model,
            cloud=self._is_cloud,
        )

    def parse(self, prompt: str, response_model: type[BaseModel], **kwargs: Any) -> BaseModel:
        if self._is_cloud:
            return self._parse_cloud(prompt, response_model)
        assert self._instructor is not None
        return self._instructor.chat.completions.create(
            model=self._config.model,
            response_model=response_model,
            max_retries=self._config.max_retries,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )

    def _parse_cloud(self, prompt: str, response_model: type[BaseModel]) -> BaseModel:
        """Ollama Cloud has no instructor integration — manual retry loop with
        validation-error feedback, same shape instructor uses under the hood."""
        assert self._cloud is not None
        current_prompt = prompt
        last_error: Exception | None = None
        for attempt in range(self._config.max_retries):
            response = self._cloud.chat(
                model=self._config.model,
                messages=[{"role": "user", "content": current_prompt}],
                format="json",
            )
            content = response["message"]["content"]
            try:
                return response_model.model_validate_json(content)
            except ValidationError as exc:
                last_error = exc
                current_prompt = (
                    f"{prompt}\n\n"
                    f"Previous attempt failed validation: {exc}\n"
                    f"Return valid JSON matching the requested schema."
                )
                log.info("ollama.cloud.parse.retry", attempt=attempt + 1, error=str(exc)[:200])
            except (KeyError, json.JSONDecodeError) as exc:
                last_error = exc
                current_prompt = f"{prompt}\n\nPrevious output was not valid JSON. Return valid JSON only."
                log.info("ollama.cloud.parse.invalid_json", attempt=attempt + 1)
        raise RuntimeError(
            f"Ollama Cloud failed to produce valid {response_model.__name__} JSON after "
            f"{self._config.max_retries} attempts. Last error: {last_error}"
        )

    def embed(self, text: str) -> list[float]:
        if self._is_cloud:
            assert self._cloud is not None
            response = self._cloud.embeddings(model=self._config.embed_model, prompt=text)
            return list(response["embedding"])
        assert self._local is not None
        response = self._local.embeddings.create(model=self._config.embed_model, input=text)
        return response.data[0].embedding
