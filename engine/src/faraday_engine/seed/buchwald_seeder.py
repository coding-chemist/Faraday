"""Buchwald-Hartwig amination seeder. 30 experiments.

Sensitive to base (strong alkoxide preferred), ligand (BINAP/XPhos for hindered amines),
and solvent (toluene/dioxane standard). Condition fit declared in _FIT_RULES.
"""
from dataclasses import dataclass
from datetime import timedelta

from faraday_engine.domain.experiment import Experiment
from faraday_engine.domain.experiment import ExperimentStatus
from faraday_engine.domain.experiment import ExperimentType
from faraday_engine.domain.experiment import Reagent
from faraday_engine.domain.experiment import ReagentRole
from faraday_engine.domain.experiment import Result
from faraday_engine.seed.base import ExperimentSeeder
from faraday_engine.seed.base import SeederRegistry
from faraday_engine.seed.building_blocks import AMINES
from faraday_engine.seed.building_blocks import ARYL_HALIDES
from faraday_engine.seed.building_blocks import BuildingBlock
from faraday_engine.seed.distributions import correlated_yield
from faraday_engine.seed.distributions import date_in_last_n_months
from faraday_engine.seed.distributions import gaussian_clamped
from faraday_engine.seed.distributions import lognormal_time
from faraday_engine.seed.distributions import weighted_choice
from faraday_engine.seed.fit_rules import FitRule
from faraday_engine.seed.fit_rules import compute_fit
from faraday_engine.seed.reagent_library import APROTIC_SOLVENTS
from faraday_engine.seed.reagent_library import ChemReagent
from faraday_engine.seed.reagent_library import INERT_ATMOSPHERES
from faraday_engine.seed.reagent_library import LIGANDS_FOR_PD
from faraday_engine.seed.reagent_library import PD_CATALYSTS
from faraday_engine.seed.reagent_library import STRONG_BASES


@dataclass(frozen=True)
class _BuchwaldContext:
    aryl: BuildingBlock
    amine: BuildingBlock
    pd: ChemReagent
    ligand: ChemReagent
    base: ChemReagent
    solvent: ChemReagent


_FIT_RULES: list[FitRule] = [
    FitRule(lambda c: "primary_amine" in c.amine.class_tags and "aromatic" not in c.amine.class_tags, 0.25, "primary alkyl amines couple easily"),
    FitRule(lambda c: "secondary_amine" in c.amine.class_tags and c.ligand.name in {"XPhos", "SPhos", "BINAP"}, 0.30, "secondary amines need bulky ligand"),
    FitRule(lambda c: "aromatic" in c.amine.class_tags and c.ligand.name == "BINAP", 0.35, "BINAP is classical for anilines"),
    FitRule(lambda c: "hindered" in c.aryl.class_tags and c.ligand.name not in {"XPhos", "SPhos"}, -0.40, "hindered ArX without bulky ligand fails"),
    FitRule(lambda c: "aryl_chloride" in c.aryl.class_tags and c.ligand.name not in {"XPhos", "SPhos"}, -0.60, "ArCl without bulky electron-rich ligand"),
    FitRule(lambda c: "heterocycle" in c.aryl.class_tags, -0.10, "heterocyclic ArX trickier in Buchwald"),
]


@SeederRegistry.register(ExperimentType.BUCHWALD_HARTWIG, count=30)
class BuchwaldSeeder(ExperimentSeeder):
    def generate(self) -> Experiment:
        rng = self._rng

        aryl = weighted_choice(rng, [(b, 1.0) for b in ARYL_HALIDES if "aryl_iodide" not in b.class_tags])
        amine = weighted_choice(rng, [(a, 1.0) for a in AMINES])
        pd = weighted_choice(rng, [(p, w) for p, w in PD_CATALYSTS
                                   if "Pd2(dba)3" in p.name or "XPhos" in p.name or "acetate" in p.name])
        ligand = weighted_choice(rng, [(lig, w) for lig, w in LIGANDS_FOR_PD if lig.name != "triphenylphosphine"])
        base = weighted_choice(rng, STRONG_BASES)
        solvent = weighted_choice(rng, [(s, w) for s, w in APROTIC_SOLVENTS
                                        if s.name in {"toluene", "1,4-dioxane", "tetrahydrofuran"}])

        ctx = _BuchwaldContext(aryl, amine, pd, ligand, base, solvent)
        fit = compute_fit(ctx, _FIT_RULES)

        substrate_mmol = round(rng.uniform(0.5, 3.0), 2)
        amine_eq = round(rng.uniform(1.1, 1.5), 2)
        pd_eq = round(rng.choice([0.02, 0.025, 0.03, 0.05]), 3)
        ligand_eq = pd_eq * round(rng.choice([2, 2.5, 3]), 1)
        base_eq = round(rng.choice([1.2, 1.4, 2.0]), 1)
        temp = gaussian_clamped(rng, mu=95.0, sigma=10.0, low=70.0, high=120.0)
        time_min = lognormal_time(rng, median_h=18.0, sigma=0.5)

        status, yield_pct, result_notes = _resolve_outcome(rng, fit)
        started = date_in_last_n_months(rng, 12)
        completed = started + timedelta(minutes=time_min) if status == ExperimentStatus.COMPLETED else None

        reagents = [
            Reagent(name=aryl.name, role=ReagentRole.SUBSTRATE, cas=aryl.cas, mw=aryl.mw,
                    equivalents=1.0, mass_g=round(substrate_mmol * aryl.mw / 1000, 3),
                    moles_mmol=substrate_mmol, supplier=aryl.supplier),
            Reagent(name=amine.name, role=ReagentRole.REAGENT, cas=amine.cas, mw=amine.mw,
                    equivalents=amine_eq, mass_g=round(substrate_mmol * amine_eq * amine.mw / 1000, 3),
                    moles_mmol=round(substrate_mmol * amine_eq, 2), supplier=amine.supplier),
            Reagent(name=pd.name, role=ReagentRole.CATALYST, cas=pd.cas, mw=pd.mw,
                    equivalents=pd_eq, moles_mmol=round(substrate_mmol * pd_eq, 4), supplier=pd.supplier),
            Reagent(name=ligand.name, role=ReagentRole.LIGAND, cas=ligand.cas, mw=ligand.mw,
                    equivalents=ligand_eq, moles_mmol=round(substrate_mmol * ligand_eq, 4), supplier=ligand.supplier),
            Reagent(name=base.name, role=ReagentRole.BASE, cas=base.cas, mw=base.mw,
                    equivalents=base_eq, mass_g=round(substrate_mmol * base_eq * base.mw / 1000, 3),
                    moles_mmol=round(substrate_mmol * base_eq, 2), supplier=base.supplier),
            Reagent(name=solvent.name, role=ReagentRole.SOLVENT, cas=solvent.cas, mw=solvent.mw,
                    supplier=solvent.supplier),
        ]

        result = None
        if status == ExperimentStatus.COMPLETED:
            product_mw_approx = aryl.mw + amine.mw - 80
            product_mass = round(substrate_mmol * (yield_pct / 100) * product_mw_approx / 1000, 3)
            result = Result(
                yield_pct=yield_pct,
                purity_pct=round(min(99.0, 85 + rng.uniform(0, 12)), 1),
                mass_g=product_mass,
                moles_mmol=round(substrate_mmol * (yield_pct / 100), 3),
                notes=result_notes,
            )

        return Experiment(
            title=f"Buchwald-Hartwig amination of {aryl.name} with {amine.name}",
            type=ExperimentType.BUCHWALD_HARTWIG,
            status=status,
            solvent_name=solvent.name,
            temperature_c=round(temp, 1),
            time_min=time_min,
            atmosphere=weighted_choice(rng, INERT_ATMOSPHERES),
            notes=rng.choice([
                "Sealed tube, oil bath at indicated temperature.",
                "Schlenk technique. Solvent degassed by freeze-pump-thaw.",
                "Microwave: 120°C, 60 min — full conversion confirmed.",
                "Glovebox preparation. Catalyst pre-formed with ligand before addition.",
            ]),
            started_at=started,
            completed_at=completed,
            created_at=started,
            updated_at=completed or started,
            reagents=reagents,
            result=result,
        )


def _resolve_outcome(rng, fit: float):
    roll = rng.random()
    if roll < 0.05:
        return ExperimentStatus.IN_PROGRESS, None, None
    if roll < 0.13:
        return ExperimentStatus.FAILED, None, rng.choice([
            "Significant homocoupling and dehalogenation observed.",
            "No conversion after 24h. Tried higher catalyst loading — still no product.",
            "Amine reacted with base. Restarted with milder conditions in separate experiment.",
        ])
    y = correlated_yield(rng, fit, base_mu=68.0, base_sigma=14.0)
    notes = rng.choice([
        "Worked up with brine, extracted with EtOAc. Column purified.",
        "Crude purified by silica chromatography (5% MeOH/DCM).",
        "Acid/base extraction to remove unreacted amine, then column.",
    ])
    return ExperimentStatus.COMPLETED, y, notes
