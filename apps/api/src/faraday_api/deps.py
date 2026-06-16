"""FastAPI dependency providers — wrap ServiceFactory for Depends() injection.

Tests override via app.dependency_overrides[get_X] = fake_factory.
"""
from collections.abc import Iterator

from fastapi import Depends
from sqlalchemy.orm import Session

from faraday_engine.factories.service_factory import ServiceFactory
from faraday_engine.repositories.session import session_scope
from faraday_engine.services.analyze_service import AnalyzeService
from faraday_engine.services.experiment_service import ExperimentService
from faraday_engine.services.query_parser_service import QueryParserService


def get_db() -> Iterator[Session]:
    """Per-request session. Commits on clean exit, rolls back on exception."""
    with session_scope() as session:
        yield session


def get_query_parser_service() -> QueryParserService:
    return ServiceFactory.create_query_parser_service()


def get_experiment_service(session: Session = Depends(get_db)) -> ExperimentService:
    return ServiceFactory.create_experiment_service(session)


def get_analyze_service() -> AnalyzeService:
    return ServiceFactory.create_analyze_service()
