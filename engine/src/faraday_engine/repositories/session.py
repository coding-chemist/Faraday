"""SQLAlchemy engine + session factory. One engine per process, sessions per unit-of-work."""
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from faraday_engine.repositories.base import Base
from faraday_shared.config import settings
from faraday_shared.logging import get_logger

log = get_logger(__name__)

_engine: Engine | None = None
_SessionLocal: sessionmaker[Session] | None = None


def _ensure_data_dir(url: str) -> None:
    """SQLite file path may be in a directory that doesn't exist yet."""
    if url.startswith("sqlite:///"):
        path = url.replace("sqlite:///", "", 1)
        Path(path).parent.mkdir(parents=True, exist_ok=True)


def get_engine() -> Engine:
    global _engine, _SessionLocal
    if _engine is None:
        _ensure_data_dir(settings.database_url)
        connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
        _engine = create_engine(
            settings.database_url,
            echo=False,
            future=True,
            connect_args=connect_args,
        )
        _SessionLocal = sessionmaker(bind=_engine, autoflush=False, expire_on_commit=False)
        log.info("db.engine.init", url=_redact(settings.database_url))
    return _engine


def get_session_factory() -> sessionmaker[Session]:
    if _SessionLocal is None:
        get_engine()
    assert _SessionLocal is not None
    return _SessionLocal


@contextmanager
def session_scope() -> Iterator[Session]:
    """Commit on clean exit, rollback on exception, always close."""
    session = get_session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db() -> None:
    """Create all tables. Dev convenience for SQLite; production should use Alembic."""
    # Import models so they register with Base.metadata
    from faraday_engine.repositories import models  # noqa: F401

    engine = get_engine()
    Base.metadata.create_all(engine)
    log.info("db.init", tables=sorted(Base.metadata.tables.keys()))


def _redact(url: str) -> str:
    """Strip credentials from URL for logging."""
    if "@" not in url:
        return url
    scheme, rest = url.split("://", 1)
    creds, host = rest.rsplit("@", 1)
    return f"{scheme}://***@{host}"
