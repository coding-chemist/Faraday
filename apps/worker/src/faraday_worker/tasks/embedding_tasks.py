"""Embedding tasks — Celery wrappers over EmbeddingService.

Tasks stay thin. All logic in engine/services/embedding_service.py. Retries handle
transient Ollama Cloud rate-limits or network blips.
"""
from celery.exceptions import MaxRetriesExceededError

from faraday_engine.factories.service_factory import ServiceFactory
from faraday_engine.repositories.session import session_scope
from faraday_shared.logging import get_logger
from faraday_worker.celery_app import celery_app

log = get_logger(__name__)


@celery_app.task(
    name="embedding.create",
    bind=True,
    max_retries=3,
    default_retry_delay=30,
    acks_late=True,
)
def create_embedding(self, experiment_id: str) -> dict:
    """Embed one experiment and persist to the vector store.

    Called from the API after experiment creation. Retries on transient failures
    (LLM provider rate limits, network blips) with exponential backoff.
    """
    try:
        with session_scope() as session:
            service = ServiceFactory.create_embedding_service(session)
            service.create(experiment_id)
        return {"experiment_id": experiment_id, "status": "indexed"}
    except KeyError:
        # Experiment doesn't exist — don't retry, the work is unrecoverable
        log.error("embedding.create.not_found", experiment_id=experiment_id)
        return {"experiment_id": experiment_id, "status": "not_found"}
    except Exception as exc:
        log.exception("embedding.create.error", experiment_id=experiment_id, error=str(exc))
        try:
            raise self.retry(exc=exc, countdown=2 ** self.request.retries * 30)
        except MaxRetriesExceededError:
            return {"experiment_id": experiment_id, "status": "failed", "error": str(exc)}


@celery_app.task(name="embedding.backfill", bind=True, acks_late=True)
def backfill_embeddings(self) -> dict:
    """Re-embed every experiment. Run after seed or after a searchable-text shape change."""
    with session_scope() as session:
        service = ServiceFactory.create_embedding_service(session)
        count = service.backfill()
    return {"count": count, "status": "complete"}
