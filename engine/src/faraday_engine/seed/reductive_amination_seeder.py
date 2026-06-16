"""Reductive amination seeder. 40 experiments.

STAB/DCE gold standard for ketones. NaBH3CN tolerates acid. NaBH4 fine for aldehydes,
poor for hindered ketones. Fit declared in _FIT_RULES.
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
from faraday_engine.seed.reagent_library import RA_ACIDS


@dataclass(frozen=True)
class _ReductiveAminationContext:
    carbonyl: BuildingBlock
    amine: BuildingBlock
    reductant: ChemReagent
    solvent: ChemReagent
    use_acid: bool


_FIT_RULES: list[FitRule] = [
    FitRule(lambda c: c.reductant.name == "sodium triacetoxyborohydride" and "ketone" in c.carbonyl.class_tags, 0.35, "STAB on ketones is gold standard"),
    FitRule(lambda c: c.reductant.name == "sodium triacetoxyborohydride" and c.solvent.name in {"dichloromethane", "1,2-dichloroethane"}, 0.20, "STAB in DCM/DCE textbook combo"),
    FitRule(lambda c: c.reductant.name == "sodium cyanoborohydride" and c.use_acid, 0.15, "NaBH3CN works best at low pH"),
    FitRule(lambda c: c.reductant.name == "sodium borohydride" and "ketone" in c.carbonyl.class_tags, -0.30, "NaBH4 over-reduces or fails on hindered ketones"),
    FitRule(lambda c: "aldehyde" in c.carbonyl.class_tags, 0.15, "aldehydes are more reactive than ketones"),
    FitRule(lambda c: "small" in c.carbonyl.class_tags and "primary_amine" in c.amine.class_tags, 0.10, "small carbonyl + primary amine kinetically favorable"),
]


@SeederRegistry.register(ExperimentType.REDUCTIVE_AMINATION, count=40)
class ReductiveAminationSeeder(ExperimentSeeder):
    def generate(self) -> Experiment:
        rng = self._rng

        carbonyl = weighted_choice(rng, [(c, 1.0) for c in CARBONYLS])
        amine = weighted_choice(rng, [(a, 1.0) for a in AMINES])
        ra_reductants = [(r, w) for r, w in HYDRIDE_REDUCTANTS if r.name in {
            "sodium triacetoxyborohydride", "sodium cyanoborohydride", "sodium borohydride",
        }]
        reductant = weighted_choice(rng, ra_reductants)

        if reductant.name == "sodium triacetoxyborohydride":
            solvent = weighted_choice(rng, [(s, w) for s, w in APROTIC_SOLVENTS
                                            if s.name in {"dichloromethane", "1,2-dichloroethane"}])
        else:
            solvent = weighted_choice(rng, [(s, w) for s, w in PROTIC_SOLVENTS
                                            if s.name in {"methanol", "ethanol"}])

        use_acid = rng.random() < 0.65
        acid = weighted_choice(rng, RA_ACIDS) if use_acid else None

        ctx = _ReductiveAminationContext(carbonyl, amine, reductant, solvent, use_acid)
        fit = compute_fit(ctx, _FIT_RULES)

        substrate_mmol = round(rng.uniform(0.5, 3.0), 2)
        amine_eq = round(rng.uniform(1.0, 1.5), 2)
        reductant_eq = round(rng.uniform(1.2, 1.8), 2)
        acid_eq = round(rng.uniform(0.5, 1.5), 2) if use_acid else None
        temp = gaussian_clamped(rng, mu=22.0, sigma=3.0, low=0.0, high=40.0)
        time_min = lognormal_time(rng, median_h=12.0, sigma=0.5)

        status, yield_pct, result_notes = _resolve_outcome(rng, fit)
        started = date_in_last_n_months(rng, 12)
        completed = started + timedelta(minutes=time_min) if status == ExperimentStatus.COMPLETED else None

        reagents = [
            Reagent(name=carbonyl.name, role=ReagentRole.SUBSTRATE, cas=carbonyl.cas, mw=carbonyl.mw,
                    equivalents=1.0, mass_g=round(substrate_mmol * carbonyl.mw / 1000, 3),
                    moles_mmol=substrate_mmol, supplier=carbonyl.supplier),
            Reagent(name=amine.name, role=ReagentRole.REAGENT, cas=amine.cas, mw=amine.mw,
                    equivalents=amine_eq, mass_g=round(substrate_mmol * amine_eq * amine.mw / 1000, 3),
                    moles_mmol=round(substrate_mmol * amine_eq, 2), supplier=amine.supplier),
            Reagent(name=reductant.name, role=ReagentRole.REAGENT, cas=reductant.cas, mw=reductant.mw,
                    equivalents=reductant_eq, mass_g=round(substrate_mmol * reductant_eq * reductant.mw / 1000, 3),
                    moles_mmol=round(substrate_mmol * reductant_eq, 2), supplier=reductant.supplier),
            Reagent(name=solvent.name, role=ReagentRole.SOLVENT, cas=solvent.cas, mw=solvent.mw,
                    supplier=solvent.supplier),
        ]
        if use_acid and acid is not None:
            reagents.append(Reagent(
                name=acid.name, role=ReagentRole.ACID, cas=acid.cas, mw=acid.mw,
                equivalents=acid_eq, supplier=acid.supplier,
            ))

        result = None
        if status == ExperimentStatus.COMPLETED:
            product_mw_approx = carbonyl.mw + amine.mw - 16
            product_mass = round(substrate_mmol * (yield_pct / 100) * product_mw_approx / 1000, 3)
            result = Result(
                yield_pct=yield_pct,
                purity_pct=round(min(99.0, 87 + rng.uniform(0, 12)), 1),
                mass_g=product_mass,
                moles_mmol=round(substrate_mmol * (yield_pct / 100), 3),
                notes=result_notes,
            )

        return Experiment(
            title=f"Reductive amination of {carbonyl.name} with {amine.name}",
            type=ExperimentType.REDUCTIVE_AMINATION,
            status=status,
            solvent_name=solvent.name,
            temperature_c=round(temp, 1),
            time_min=time_min,
            atmosphere="N2" if rng.random() < 0.5 else "air",
            notes=rng.choice([
                "Amine + carbonyl pre-stirred to form imine, then reductant added.",
                "All reagents combined; monitored by TLC every 2-3h.",
                "Acid added catalytically to accelerate imine formation.",
                "Run at rt overnight.",
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
    if roll < 0.11:
        return ExperimentStatus.FAILED, None, rng.choice([
            "Carbonyl reduction product (alcohol) dominant — wrong reductant choice.",
            "Imine never formed cleanly. Carbonyl recovered.",
            "Dialkylation observed (2:1 amine:aldehyde adduct).",
        ])
    y = correlated_yield(rng, fit, base_mu=75.0, base_sigma=12.0)
    notes = rng.choice([
        "Quenched with sat. NaHCO3, extracted with DCM, dried, concentrated.",
        "Filtered through silica plug, then column chromatography (MeOH/DCM).",
        "Acid/base extraction to isolate amine product.",
    ])
    return ExperimentStatus.COMPLETED, y, notes
