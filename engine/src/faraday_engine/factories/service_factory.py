"""ServiceFactory — apps call this, never `new` services directly."""
from sqlalchemy.orm import Session

from faraday_engine.services.experiment_service import ExperimentService


class ServiceFactory:
    """Construct fully-wired services. Sessions are passed in by the transport layer."""

    @staticmethod
    def create_experiment_service(session: Session) -> ExperimentService:
        return ExperimentService(session)
