"""Smoke-test task — proves Celery + Flower + task-ID logging are wired correctly."""
import time

from faraday_shared.logging import get_logger
from faraday_worker.celery_app import celery_app

log = get_logger(__name__)


@celery_app.task(name="hello.ping", bind=True)
def ping(self, message: str = "hello") -> dict[str, str]:
    log.info("hello.ping.start", message=message)
    time.sleep(0.5)
    log.info("hello.ping.done")
    return {"task_id": self.request.id, "message": message, "status": "ok"}
