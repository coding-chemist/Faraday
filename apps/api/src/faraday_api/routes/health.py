"""Health + introspection routes."""
import time

from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel

from faraday_engine.factories.provider_factory import ProviderFactory
from faraday_engine.providers.llm import LLMRegistry
from faraday_engine.providers.vector import VectorRegistry
from faraday_shared.config import settings
from faraday_shared.logging import get_logger

log = get_logger(__name__)

router = APIRouter(tags=["health"])

_STARTED_AT = time.time()


class RootResponse(BaseModel):
    service: str
    version: str
    docs: str
    endpoints: list[str]


class HealthResponse(BaseModel):
    status: str
    env: str
    uptime_s: float


@router.get("/", response_model=RootResponse, include_in_schema=False)
def root() -> RootResponse:
    """Friendly landing for the HF Space 'App' tab — no UI here, just the API map."""
    return RootResponse(
        service="Faraday API",
        version="0.1.0",
        docs="/docs",
        endpoints=["/health", "/health/llm", "/providers", "/memory/ask"],
    )


class ProvidersResponse(BaseModel):
    llm: list[str]
    vector: list[str]
    active_llm: str
    active_vector: str
    llm_host: str | None
    llm_model: str | None
    llm_embed_model: str | None
    llm_api_key_set: bool


class _Pong(BaseModel):
    """Minimal schema for the chat smoke-test: forces the model through the
    same JSON-validated path /memory/ask uses, without touching the DB."""
    pong: bool


class LLMHealthResponse(BaseModel):
    status: str
    provider: str
    host: str | None
    cloud: bool
    model: str | None
    chat_ok: bool


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Liveness check. Frontend warms HF Spaces by calling this on mount.

    Stays fast — does NOT touch the LLM. Use /health/llm for the end-to-end
    secret + connectivity smoke test.
    """
    return HealthResponse(
        status="ok",
        env=settings.env,
        uptime_s=round(time.time() - _STARTED_AT, 2),
    )


@router.get("/health/llm", response_model=LLMHealthResponse)
def llm_health() -> LLMHealthResponse:
    """End-to-end LLM smoke check — proves the API key + host + chat model wire up.

    Uses the chat path (the one /memory/ask actually depends on), NOT embed.
    Ollama Cloud doesn't serve /api/embeddings, and the chat round-trip is
    what we actually care about for the demo. 503 with the underlying error
    if the provider doesn't respond. Latency ~500-2000ms — fine for manual
    deploy checks, do not include in liveness probes.
    """
    try:
        llm = ProviderFactory.create_llm()
        result = llm.parse('Respond with JSON {"pong": true}. Nothing else.', _Pong)
        host = settings.llm.config.get("host")
        api_key = settings.llm.config.get("api_key")
        return LLMHealthResponse(
            status="ok",
            provider=llm.name,
            host=str(host) if host else None,
            cloud=bool(api_key),
            model=settings.llm.config.get("model"),
            chat_ok=bool(getattr(result, "pong", False)),
        )
    except Exception as exc:
        log.exception("health.llm.failed", error=str(exc))
        raise HTTPException(
            status_code=503,
            detail=f"LLM unreachable: {type(exc).__name__}: {exc}",
        ) from exc


@router.get("/providers", response_model=ProvidersResponse)
def providers() -> ProvidersResponse:
    """Introspect what providers are registered + the active LLM config.
    api_key value is masked — only its presence is reported."""
    cfg = settings.llm.config or {}
    return ProvidersResponse(
        llm=LLMRegistry.list(),
        vector=VectorRegistry.list(),
        active_llm=settings.llm.provider,
        active_vector=settings.vector.provider,
        llm_host=cfg.get("host"),
        llm_model=cfg.get("model"),
        llm_embed_model=cfg.get("embed_model"),
        llm_api_key_set=bool(cfg.get("api_key")),
    )
