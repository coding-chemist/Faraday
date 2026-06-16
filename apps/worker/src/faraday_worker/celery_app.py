"""Celery app — task IDs flow into logs automatically via signal handlers in faraday_shared.logging."""
from celery import Celery
from celery.signals import worker_process_init

from faraday_engine.repositories import init_db
from faraday_shared.config import settings
from faraday_shared.logging import setup_logging

celery_app = Celery(
    "faraday",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        "faraday_worker.tasks.hello_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
    broker_connection_retry_on_startup=True,
)


@worker_process_init.connect
def _on_worker_init(**_kwargs):
    setup_logging(level=settings.log_level, json=settings.log_json)
    init_db()
