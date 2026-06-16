"""Health + introspection routes."""
import time

from fastapi import APIRouter
from pydantic import BaseModel

from faraday_engine.providers.llm import LLMRegistry
from faraday_engine.providers.vector import VectorRegistry
from faraday_shared.config import settings

router = APIRouter(tags=["health"])

_STARTED_AT = time.time()


class HealthResponse(BaseModel):
    status: str
    env: str
    uptime_s: float


class ProvidersResponse(BaseModel):
    llm: list[str]
    vector: list[str]
    active_llm: str
    active_vector: str


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Liveness check. Frontend warms HF Spaces by calling this on mount."""
    return HealthResponse(
        status="ok",
        env=settings.env,
        uptime_s=round(time.time() - _STARTED_AT, 2),
    )


@router.get("/providers", response_model=ProvidersResponse)
def providers() -> ProvidersResponse:
    """Introspect what providers are registered. Useful for debugging Ollama Cloud swaps."""
    return ProvidersResponse(
        llm=LLMRegistry.list(),
        vector=VectorRegistry.list(),
        active_llm=settings.llm.provider,
        active_vector=settings.vector.provider,
    )
