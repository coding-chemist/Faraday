"""SQLAlchemy declarative base. All ORM models inherit from Base."""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Faraday ORM base. Migrations are driven from Base.metadata."""
