"""Structured logging with Celery task ID + HTTP request ID propagation.

Every log line carries the trace ID that's active in the current context — Celery task IDs
flow in via signal hooks, HTTP request IDs flow in via FastAPI middleware. One get_logger()
import everywhere; context propagates automatically through ContextVar.
"""
import logging
import sys
from contextvars import ContextVar
from typing import Any

import structlog
from celery.signals import task_failure, task_postrun, task_prerun

# Context vars — read inside the _bind_context processor on every log call
celery_task_id: ContextVar[str | None] = ContextVar("celery_task_id", default=None)
celery_task_name: ContextVar[str | None] = ContextVar("celery_task_name", default=None)
http_request_id: ContextVar[str | None] = ContextVar("http_request_id", default=None)


def _bind_context(_logger: Any, _method: str, event_dict: dict[str, Any]) -> dict[str, Any]:
    if tid := celery_task_id.get():
        event_dict["celery_task_id"] = tid
        event_dict["celery_task_name"] = celery_task_name.get()
    if rid := http_request_id.get():
        event_dict["http_request_id"] = rid
    return event_dict


def setup_logging(level: str = "INFO", json: bool = True) -> None:
    """Configure structlog + route stdlib logging through it.

    Call once at app startup (FastAPI lifespan, Celery worker_init). Idempotent.
    """
    timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)

    shared_processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        timestamper,
        _bind_context,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    renderer = (
        structlog.processors.JSONRenderer()
        if json
        else structlog.dev.ConsoleRenderer(colors=True)
    )

    structlog.configure(
        processors=[*shared_processors, renderer],
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, level.upper())),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )

    # Route stdlib logging (uvicorn, sqlalchemy, celery internals) through structlog formatting
    root = logging.getLogger()
    root.handlers = []
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    root.addHandler(handler)
    root.setLevel(getattr(logging, level.upper()))


def get_logger(name: str | None = None) -> Any:
    """Get a structlog logger bound to the calling module."""
    return structlog.get_logger(name)


# --- Celery signal wiring — task IDs flow into ContextVar automatically ---

@task_prerun.connect
def _on_task_prerun(task_id: str, task: Any, *_args: Any, **_kwargs: Any) -> None:
    celery_task_id.set(task_id)
    celery_task_name.set(task.name)


@task_postrun.connect
def _on_task_postrun(task_id: str, task: Any, *_args: Any, **_kwargs: Any) -> None:
    celery_task_id.set(None)
    celery_task_name.set(None)


@task_failure.connect
def _on_task_failure(
    task_id: str,
    exception: Exception,
    traceback: Any,
    einfo: Any,
    *_args: Any,
    **_kwargs: Any,
) -> None:
    get_logger("celery").error(
        "task.failed",
        task_id=task_id,
        error=str(exception),
        error_type=type(exception).__name__,
    )
