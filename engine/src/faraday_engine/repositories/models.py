"""SQLAlchemy ORM models — mirror domain types, never leak out of repositories."""
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from faraday_engine.repositories.base import Base


class ExperimentORM(Base):
    __tablename__ = "experiments"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    title: Mapped[str] = mapped_column(String(500))
    type: Mapped[str] = mapped_column(String(64), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)

    solvent_name: Mapped[str | None] = mapped_column(String(200), index=True)
    temperature_c: Mapped[float | None] = mapped_column(Float)
    time_min: Mapped[float | None] = mapped_column(Float)
    atmosphere: Mapped[str | None] = mapped_column(String(32))

    notes: Mapped[str | None] = mapped_column(Text)

    started_at: Mapped[datetime | None] = mapped_column(DateTime, index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    reagents: Mapped[list["ReagentORM"]] = relationship(
        back_populates="experiment", cascade="all, delete-orphan", lazy="selectin"
    )
    result: Mapped["ResultORM | None"] = relationship(
        back_populates="experiment", cascade="all, delete-orphan", uselist=False, lazy="joined"
    )


class ReagentORM(Base):
    __tablename__ = "reagents"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    experiment_id: Mapped[str] = mapped_column(
        ForeignKey("experiments.id", ondelete="CASCADE"), index=True
    )

    name: Mapped[str] = mapped_column(String(300), index=True)
    role: Mapped[str] = mapped_column(String(32), index=True)
    cas: Mapped[str | None] = mapped_column(String(32), index=True)
    mw: Mapped[float | None] = mapped_column(Float)
    equivalents: Mapped[float | None] = mapped_column(Float)
    mass_g: Mapped[float | None] = mapped_column(Float)
    moles_mmol: Mapped[float | None] = mapped_column(Float)
    supplier: Mapped[str | None] = mapped_column(String(100))
    lot_number: Mapped[str | None] = mapped_column(String(64))
    coa_url: Mapped[str | None] = mapped_column(String(500))

    experiment: Mapped[ExperimentORM] = relationship(back_populates="reagents")


class ResultORM(Base):
    __tablename__ = "results"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    experiment_id: Mapped[str] = mapped_column(
        ForeignKey("experiments.id", ondelete="CASCADE"), unique=True, index=True
    )

    yield_pct: Mapped[float | None] = mapped_column(Float, index=True)
    purity_pct: Mapped[float | None] = mapped_column(Float)
    mass_g: Mapped[float | None] = mapped_column(Float)
    moles_mmol: Mapped[float | None] = mapped_column(Float)
    notes: Mapped[str | None] = mapped_column(Text)

    experiment: Mapped[ExperimentORM] = relationship(back_populates="result")
