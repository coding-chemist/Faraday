"""Experiment domain model — pure Pydantic, no SQLAlchemy.

Repositories convert between this and ORM models. Services and routes only
ever see these types.
"""
from datetime import datetime
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class ExperimentType(StrEnum):
    """Categories chosen to match the v0.1 template library + Lab Memory Ask queries.

    The five seed types (Suzuki, Buchwald, amide coupling, reductive amination,
    carbonyl reduction) reflect Roughley & Jordan J. Med. Chem. 2011 reaction-frequency
    analysis of medchem literature.
    """
    SUZUKI_COUPLING = "suzuki_coupling"
    BUCHWALD_HARTWIG = "buchwald_hartwig"
    AMIDE_COUPLING = "amide_coupling"
    REDUCTIVE_AMINATION = "reductive_amination"
    CARBONYL_REDUCTION = "carbonyl_reduction"
    RECRYSTALLIZATION = "recrystallization"
    COLUMN_CHROMATOGRAPHY = "column_chromatography"
    NMR_CHARACTERIZATION = "nmr_characterization"
    HPLC_PURITY = "hplc_purity"
    OXIDATION = "oxidation"
    ESTERIFICATION = "esterification"
    OTHER = "other"


class ExperimentStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ReagentRole(StrEnum):
    """Reagent role within the experiment — drives the 'group by catalyst' style queries."""
    SUBSTRATE = "substrate"
    REAGENT = "reagent"
    CATALYST = "catalyst"
    LIGAND = "ligand"
    SOLVENT = "solvent"
    BASE = "base"
    ACID = "acid"
    ADDITIVE = "additive"
    INTERNAL_STANDARD = "internal_standard"
    PRODUCT = "product"


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


class Reagent(BaseModel):
    """A chemical used in an experiment."""
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: str = Field(default_factory=lambda: _new_id("rgt"))
    name: str                                    # "palladium(II) acetate"
    role: ReagentRole
    cas: str | None = None                       # "3375-31-3"
    mw: float | None = None                      # g/mol
    equivalents: float | None = None
    mass_g: float | None = None
    moles_mmol: float | None = None
    supplier: str | None = None                  # "Sigma-Aldrich"
    lot_number: str | None = None
    coa_url: str | None = None                   # Certificate of Analysis link


class Result(BaseModel):
    """Outcome of an experiment — yield, purity, recovered mass."""
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(default_factory=lambda: _new_id("res"))
    yield_pct: float | None = None               # 0-100
    purity_pct: float | None = None              # 0-100
    mass_g: float | None = None
    moles_mmol: float | None = None
    notes: str | None = None


class Experiment(BaseModel):
    """The aggregate root — owns its reagents and result."""
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: str = Field(default_factory=lambda: _new_id("exp"))
    title: str
    type: ExperimentType
    status: ExperimentStatus = ExperimentStatus.IN_PROGRESS

    # Conditions — promoted to top-level columns because Ask mode filters on them often
    solvent_name: str | None = None              # denormalized for fast grouping
    temperature_c: float | None = None
    time_min: float | None = None
    atmosphere: str | None = None                # "N2", "Ar", "air"

    notes: str | None = None

    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    reagents: list[Reagent] = Field(default_factory=list)
    result: Result | None = None

    # Convenience accessors used heavily by Ask-mode aggregations
    def catalysts(self) -> list[Reagent]:
        return [r for r in self.reagents if r.role == ReagentRole.CATALYST.value]

    def primary_catalyst_name(self) -> str | None:
        cats = self.catalysts()
        return cats[0].name if cats else None

    def yield_pct(self) -> float | None:
        return self.result.yield_pct if self.result else None

    def to_searchable_text(self) -> str:
        """Flatten experiment to a single text for embedding."""
        parts = [
            f"{self.type.replace('_', ' ')}: {self.title}",
            f"solvent: {self.solvent_name or 'n/a'}",
            f"temperature: {self.temperature_c}°C" if self.temperature_c else "",
            f"time: {self.time_min} min" if self.time_min else "",
        ]
        for r in self.reagents:
            parts.append(f"{r.role}: {r.name}")
        if self.result and self.result.yield_pct is not None:
            parts.append(f"yield: {self.result.yield_pct}%")
        if self.notes:
            parts.append(f"notes: {self.notes}")
        return " | ".join(p for p in parts if p)


class ExperimentFilters(BaseModel):
    """Filters for ExperimentRepository.list — keep flat, deserialize from QuerySpec later."""
    type: ExperimentType | None = None
    status: ExperimentStatus | None = None
    catalyst_name: str | None = None
    solvent_name: str | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None
    yield_min: float | None = None
    yield_max: float | None = None
    limit: int = 100
    offset: int = 0
