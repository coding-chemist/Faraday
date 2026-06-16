"""ExperimentService — business logic. Wraps the repository; same class.verb vocabulary."""
from datetime import datetime

from sqlalchemy.orm import Session

from faraday_engine.domain.experiment import Experiment
from faraday_engine.domain.experiment import ExperimentFilters
from faraday_engine.domain.experiment import ExperimentStatus
from faraday_engine.repositories.experiment_repository import ExperimentRepository
from faraday_shared.logging import get_logger

log = get_logger(__name__)


class ExperimentService:
    """Verbs: create, fetch, list, update, delete."""

    def __init__(self, session: Session) -> None:
        self._session = session
        self._repository = ExperimentRepository(session)

    def create(self, experiment: Experiment) -> Experiment:
        log.info("experiment.service.create", title=experiment.title, type=experiment.type)
        return self._repository.create(experiment)

    def fetch(self, id: str) -> Experiment | None:
        return self._repository.fetch(id)

    def list(self, filters: ExperimentFilters | None = None) -> list[Experiment]:
        return self._repository.list(filters)

    def update(self, id: str, data: dict) -> Experiment:
        return self._repository.update(id, data)

    def delete(self, id: str) -> None:
        self._repository.delete(id)

    def count_total(self) -> int:
        return self._repository.count_total()

    def complete(self, id: str, completed_at: datetime | None = None) -> Experiment:
        """Mark an experiment complete. Convenience wrapper over update."""
        return self.update(
            id,
            {
                "status": ExperimentStatus.COMPLETED.value,
                "completed_at": completed_at or datetime.utcnow(),
            },
        )
