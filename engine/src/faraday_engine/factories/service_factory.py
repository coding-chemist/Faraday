"""ServiceFactory — apps call this, never `new` services directly."""
from sqlalchemy.orm import Session

from faraday_engine.factories.provider_factory import ProviderFactory
from faraday_engine.repositories.experiment_repository import ExperimentRepository
from faraday_engine.services.embedding_service import EmbeddingService
from faraday_engine.services.experiment_service import ExperimentService


class ServiceFactory:
    """Construct fully-wired services. Sessions are passed in by the transport layer."""

    @staticmethod
    def create_experiment_service(session: Session) -> ExperimentService:
        return ExperimentService(session)

    @staticmethod
    def create_embedding_service(session: Session) -> EmbeddingService:
        return EmbeddingService(
            llm=ProviderFactory.create_llm(),
            vector=ProviderFactory.create_vector(),
            repository=ExperimentRepository(session),
        )
