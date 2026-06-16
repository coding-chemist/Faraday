"""FastAPI app factory + middleware + lifespan."""
import time
import uuid
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from faraday_api.routes import ask
from faraday_api.routes import health
from faraday_engine.repositories import init_db
from faraday_shared.config import settings
from faraday_shared.logging import get_logger
from faraday_shared.logging import http_request_id
from faraday_shared.logging import setup_logging


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    setup_logging(level=settings.log_level, json=settings.log_json)
    init_db()
    log = get_logger("faraday.api")
    log.info("api.startup", env=settings.env)
    _warn_on_missing_secrets(log)
    yield
    log.info("api.shutdown")


def _warn_on_missing_secrets(log) -> None:
    """Flag config that will almost certainly fail at first request."""
    if settings.env != "prod":
        return
    if settings.llm.provider == "ollama":
        host = str(settings.llm.config.get("host", ""))
        api_key = settings.llm.config.get("api_key")
        if "ollama.com" in host and not api_key:
            log.warning(
                "startup.secret.missing",
                detail=(
                    "FARADAY_LLM_CONFIG__API_KEY is empty but FARADAY_LLM_CONFIG__HOST "
                    "targets Ollama Cloud. Embeddings + completions will 401 — set the "
                    "secret in HF Space → Settings → Variables and secrets."
                ),
            )
    if not settings.cors_origin_list:
        log.warning(
            "startup.secret.missing",
            detail=(
                "FARADAY_CORS_ORIGINS is empty — the Vercel frontend will be blocked by "
                "CORS on every request. Set it to your Vercel URL(s)."
            ),
        )


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Bind http_request_id into ContextVar so all logs in this request carry it."""

    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get("x-request-id") or str(uuid.uuid4())
        token = http_request_id.set(rid)
        log = get_logger("faraday.api.request")
        start = time.perf_counter()
        try:
            log.info("request.start", method=request.method, path=request.url.path)
            response = await call_next(request)
            elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
            log.info(
                "request.done",
                method=request.method,
                path=request.url.path,
                status=response.status_code,
                elapsed_ms=elapsed_ms,
            )
            response.headers["x-request-id"] = rid
            return response
        except Exception as exc:
            log.exception("request.error", error=str(exc))
            raise
        finally:
            http_request_id.reset(token)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Faraday API",
        version="0.1.0",
        description="AI-assisted lab notebook for industry chemists",
        lifespan=lifespan,
    )

    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_origin_regex=r"https://.*\.vercel\.app",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["x-request-id"],
    )

    app.include_router(health.router)
    app.include_router(ask.router)
    return app


app = create_app()
