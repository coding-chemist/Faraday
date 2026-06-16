"""Carbonyl reduction seeder. 25 experiments.

NaBH4 chemoselective for aldehydes, LiAlH4 broad reducer (can over-reduce or remove
protecting groups), DIBAL for low-temp partial reductions. Fit declared in _FIT_RULES.
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
from faraday_engine.seed.building_blocks import CARBONYLS
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
from faraday_engine.seed.reagent_library import HYDRIDE_REDUCTANTS
from faraday_engine.seed.reagent_library import PROTIC_SOLVENTS


@dataclass(frozen=True)
class _ReductionContext:
    carbonyl: BuildingBlock
    reductant: ChemReagent
    solvent: ChemReagent


_FIT_RULES: list[FitRule] = [
    FitRule(lambda c: c.reductant.name == "sodium borohydride" and "aldehyde" in c.carbonyl.class_tags, 0.40, "NaBH4 + aldehyde textbook"),
    FitRule(lambda c: c.reductant.name == "sodium borohydride" and "ketone" in c.carbonyl.class_tags, 0.10, "NaBH4 on ketones works but slower"),
    FitRule(lambda c: c.reductant.name == "lithium aluminum hydride", 0.20, "LiAlH4 broadly reduces carbonyls"),
    FitRule(lambda c: c.reductant.name == "lithium aluminum hydride" and "protected" in c.carbonyl.class_tags, -0.30, "LiAlH4 may strip Boc/protecting groups"),
    FitRule(lambda c: c.reductant.name == "diisobutylaluminum hydride" and "aldehyde" in c.carbonyl.class_tags, -0.20, "DIBAL on aldehydes risks over-reduction"),
    FitRule(lambda c: c.reductant.name == "sodium cyanoborohydride", -0.30, "NaBH3CN too weak for plain carbonyl reduction"),
    FitRule(lambda c: c.reductant.name == "sodium triacetoxyborohydride", -0.40, "STAB doesn't reduce carbonyls efficiently alone"),
]


@SeederRegistry.register(ExperimentType.CARBONYL_REDUCTION, count=25)
class CarbonylReductionSeeder(ExperimentSeeder):
    def generate(self) -> Experiment:
        rng = self._rng

        carbonyl = weighted_choice(rng, [(c, 1.0) for c in CARBONYLS])
        reductant = weighted_choice(rng, HYDRIDE_REDUCTANTS)
        solvent, temp = _solvent_and_temp_for_reductant(rng, reductant.name)

        ctx = _ReductionContext(carbonyl, reductant, solvent)
        fit = compute_fit(ctx, _FIT_RULES)

        substrate_mmol = round(rng.uniform(0.5, 5.0), 2)
        reductant_eq = round(rng.uniform(1.0, 2.5), 2)
        time_min = lognormal_time(rng, median_h=3.0, sigma=0.6)

        status, yield_pct, result_notes = _resolve_outcome(rng, fit)
        started = date_in_last_n_months(rng, 12)
        completed = started + timedelta(minutes=time_min) if status == ExperimentStatus.COMPLETED else None

        reagents = [
            Reagent(name=carbonyl.name, role=ReagentRole.SUBSTRATE, cas=carbonyl.cas, mw=carbonyl.mw,
                    equivalents=1.0, mass_g=round(substrate_mmol * carbonyl.mw / 1000, 3),
                    moles_mmol=substrate_mmol, supplier=carbonyl.supplier),
            Reagent(name=reductant.name, role=ReagentRole.REAGENT, cas=reductant.cas, mw=reductant.mw,
                    equivalents=reductant_eq, mass_g=round(substrate_mmol * reductant_eq * reductant.mw / 1000, 4),
                    moles_mmol=round(substrate_mmol * reductant_eq, 2), supplier=reductant.supplier),
            Reagent(name=solvent.name, role=ReagentRole.SOLVENT, cas=solvent.cas, mw=solvent.mw,
                    supplier=solvent.supplier),
        ]

        result = None
        if status == ExperimentStatus.COMPLETED:
            product_mw_approx = carbonyl.mw + 2
            product_mass = round(substrate_mmol * (yield_pct / 100) * product_mw_approx / 1000, 3)
            result = Result(
                yield_pct=yield_pct,
                purity_pct=round(min(99.5, 90 + rng.uniform(0, 9)), 1),
                mass_g=product_mass,
                moles_mmol=round(substrate_mmol * (yield_pct / 100), 3),
                notes=result_notes,
            )

        return Experiment(
            title=f"Reduction of {carbonyl.name} with {reductant.name}",
            type=ExperimentType.CARBONYL_REDUCTION,
            status=status,
            solvent_name=solvent.name,
            temperature_c=round(temp, 1),
            time_min=time_min,
            atmosphere="N2" if reductant.name in {"lithium aluminum hydride", "diisobutylaluminum hydride"} else "air",
            notes=rng.choice([
                "Reductant added slowly at low temperature.",
                "Reaction monitored by TLC; quenched immediately on consumption of starting material.",
                "Cold bath: dry ice/acetone.",
                "Standard reduction protocol per SOP-RED-001.",
            ]),
            started_at=started,
            completed_at=completed,
            created_at=started,
            updated_at=completed or started,
            reagents=reagents,
            result=result,
        )


def _solvent_and_temp_for_reductant(rng, reductant_name: str) -> tuple[ChemReagent, float]:
    """Solvent + temperature regime keyed by reductant. Each reductant has a textbook
    solvent class and temperature window."""
    if reductant_name == "sodium borohydride":
        solvent = weighted_choice(rng, [(s, w) for s, w in PROTIC_SOLVENTS
                                        if s.name in {"methanol", "ethanol"}])
        return solvent, gaussian_clamped(rng, mu=5.0, sigma=4.0, low=-5.0, high=25.0)
    if reductant_name == "lithium aluminum hydride":
        solvent = weighted_choice(rng, [(s, w) for s, w in APROTIC_SOLVENTS
                                        if s.name == "tetrahydrofuran"])
        return solvent, gaussian_clamped(rng, mu=10.0, sigma=8.0, low=-10.0, high=40.0)
    if reductant_name == "diisobutylaluminum hydride":
        solvent = weighted_choice(rng, [(s, w) for s, w in APROTIC_SOLVENTS
                                        if s.name in {"toluene", "dichloromethane", "tetrahydrofuran"}])
        return solvent, gaussian_clamped(rng, mu=-65.0, sigma=10.0, low=-78.0, high=-40.0)
    solvent = weighted_choice(rng, [(s, w) for s, w in APROTIC_SOLVENTS if s.name == "tetrahydrofuran"])
    return solvent, gaussian_clamped(rng, mu=22.0, sigma=4.0, low=0.0, high=40.0)


def _resolve_outcome(rng, fit: float):
    roll = rng.random()
    if roll < 0.05:
        return ExperimentStatus.IN_PROGRESS, None, None
    if roll < 0.10:
        return ExperimentStatus.FAILED, None, rng.choice([
            "Over-reduction observed by LCMS.",
            "Quench too aggressive — exotherm, product decomposition.",
            "Protecting group cleaved during reduction.",
        ])
    y = correlated_yield(rng, fit, base_mu=78.0, base_sigma=12.0)
    notes = rng.choice([
        "Quenched with sat. NH4Cl, extracted with EtOAc, dried over MgSO4.",
        "Cold quench (1M HCl), then standard aqueous workup.",
        "Filtered through celite, concentrated, used directly.",
        "Distilled at reduced pressure.",
    ])
    return ExperimentStatus.COMPLETED, y, notes
