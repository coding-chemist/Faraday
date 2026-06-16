"""Amide coupling seeder. 60 experiments — #1 reaction in medchem volume.

HATU/T3P > EDC for hindered partners. DIPEA preferred. HOBt added with carbodiimides.
Fit declared in _FIT_RULES — adding chemistry rule = one line.
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
from faraday_engine.seed.building_blocks import CARBOXYLIC_ACIDS
from faraday_engine.seed.building_blocks import BuildingBlock
from faraday_engine.seed.distributions import correlated_yield
from faraday_engine.seed.distributions import date_in_last_n_months
from faraday_engine.seed.distributions import gaussian_clamped
from faraday_engine.seed.distributions import lognormal_time
from faraday_engine.seed.distributions import weighted_choice
from faraday_engine.seed.fit_rules import FitRule
from faraday_engine.seed.fit_rules import compute_fit
from faraday_engine.seed.reagent_library import AMIDE_COUPLING_REAGENTS
from faraday_engine.seed.reagent_library import AMINE_BASES
from faraday_engine.seed.reagent_library import APROTIC_SOLVENTS
from faraday_engine.seed.reagent_library import ChemReagent
from faraday_engine.seed.reagent_library import HOBT_ADDITIVES


@dataclass(frozen=True)
class _AmideContext:
    acid: BuildingBlock
    amine: BuildingBlock
    coupler: ChemReagent
    base: ChemReagent
    solvent: ChemReagent
    use_hobt: bool


_FIT_RULES: list[FitRule] = [
    FitRule(lambda c: c.coupler.name in {"HATU", "T3P"}, 0.35, "HATU/T3P high-yielding workhorses"),
    FitRule(lambda c: c.coupler.name == "EDC hydrochloride" and c.use_hobt, 0.15, "EDC + HOBt reliable, suppresses racemization"),
    FitRule(lambda c: "amino_acid" in c.acid.class_tags and c.coupler.name == "HATU", 0.20, "HATU is the gold standard for peptide couplings"),
    FitRule(lambda c: "hindered" in c.amine.class_tags and c.coupler.name in {"T3P", "PyBOP"}, 0.25, "bulky-tolerant couplers handle hindered amines"),
    FitRule(lambda c: "aromatic" in c.amine.class_tags and "primary_amine" in c.amine.class_tags, -0.20, "anilines are sluggish nucleophiles"),
    FitRule(lambda c: c.base.name == "N,N-diisopropylethylamine", 0.10, "DIPEA (Hünig's base) preferred"),
]


@SeederRegistry.register(ExperimentType.AMIDE_COUPLING, count=60)
class AmideCouplingSeeder(ExperimentSeeder):
    def generate(self) -> Experiment:
        rng = self._rng

        acid = weighted_choice(rng, [(a, 1.0) for a in CARBOXYLIC_ACIDS])
        amine = weighted_choice(rng, [(a, 1.0) for a in AMINES])
        coupler = weighted_choice(rng, AMIDE_COUPLING_REAGENTS)
        base = weighted_choice(rng, AMINE_BASES)
        solvent = weighted_choice(rng, [(s, w) for s, w in APROTIC_SOLVENTS if s.name in {
            "N,N-dimethylformamide", "dichloromethane", "N-methyl-2-pyrrolidinone",
            "tetrahydrofuran", "acetonitrile"
        }])
        use_hobt = coupler.name in {"EDC hydrochloride", "DCC"}

        ctx = _AmideContext(acid, amine, coupler, base, solvent, use_hobt)
        fit = compute_fit(ctx, _FIT_RULES)

        substrate_mmol = round(rng.uniform(0.2, 5.0), 2)
        amine_eq = round(rng.uniform(1.0, 1.3), 2)
        coupler_eq = round(rng.uniform(1.1, 1.5), 2)
        base_eq = round(rng.uniform(2.0, 4.0), 1)
        temp = gaussian_clamped(rng, mu=22.0, sigma=4.0, low=0.0, high=40.0)
        time_min = lognormal_time(rng, median_h=6.0, sigma=0.6)

        status, yield_pct, result_notes = _resolve_outcome(rng, fit)
        started = date_in_last_n_months(rng, 12)
        completed = started + timedelta(minutes=time_min) if status == ExperimentStatus.COMPLETED else None

        reagents = [
            Reagent(name=acid.name, role=ReagentRole.SUBSTRATE, cas=acid.cas, mw=acid.mw,
                    equivalents=1.0, mass_g=round(substrate_mmol * acid.mw / 1000, 3),
                    moles_mmol=substrate_mmol, supplier=acid.supplier),
            Reagent(name=amine.name, role=ReagentRole.REAGENT, cas=amine.cas, mw=amine.mw,
                    equivalents=amine_eq, mass_g=round(substrate_mmol * amine_eq * amine.mw / 1000, 3),
                    moles_mmol=round(substrate_mmol * amine_eq, 2), supplier=amine.supplier),
            Reagent(name=coupler.name, role=ReagentRole.REAGENT, cas=coupler.cas, mw=coupler.mw,
                    equivalents=coupler_eq, mass_g=round(substrate_mmol * coupler_eq * coupler.mw / 1000, 3),
                    moles_mmol=round(substrate_mmol * coupler_eq, 2), supplier=coupler.supplier),
            Reagent(name=base.name, role=ReagentRole.BASE, cas=base.cas, mw=base.mw,
                    equivalents=base_eq, mass_g=round(substrate_mmol * base_eq * base.mw / 1000, 3),
                    moles_mmol=round(substrate_mmol * base_eq, 2), supplier=base.supplier),
            Reagent(name=solvent.name, role=ReagentRole.SOLVENT, cas=solvent.cas, mw=solvent.mw,
                    supplier=solvent.supplier),
        ]
        if use_hobt:
            hobt = HOBT_ADDITIVES[0][0]
            reagents.append(Reagent(
                name=hobt.name, role=ReagentRole.ADDITIVE, cas=hobt.cas, mw=hobt.mw,
                equivalents=1.2, mass_g=round(substrate_mmol * 1.2 * hobt.mw / 1000, 3),
                moles_mmol=round(substrate_mmol * 1.2, 2), supplier=hobt.supplier,
            ))

        result = None
        if status == ExperimentStatus.COMPLETED:
            product_mw_approx = acid.mw + amine.mw - 18
            product_mass = round(substrate_mmol * (yield_pct / 100) * product_mw_approx / 1000, 3)
            result = Result(
                yield_pct=yield_pct,
                purity_pct=round(min(99.5, 90 + rng.uniform(0, 9)), 1),
                mass_g=product_mass,
                moles_mmol=round(substrate_mmol * (yield_pct / 100), 3),
                notes=result_notes,
            )

        return Experiment(
            title=f"Amide coupling of {acid.name} with {amine.name}",
            type=ExperimentType.AMIDE_COUPLING,
            status=status,
            solvent_name=solvent.name,
            temperature_c=round(temp, 1),
            time_min=time_min,
            atmosphere="N2" if rng.random() < 0.7 else "air",
            notes=rng.choice([
                "Amine added dropwise to pre-activated acid.",
                "Pre-stirred acid + coupler + base for 10 min before amine addition.",
                "Reaction monitored by TLC and LCMS for completion.",
                "All reagents combined at 0°C, then warmed to rt overnight.",
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
    if roll < 0.04:
        return ExperimentStatus.IN_PROGRESS, None, None
    if roll < 0.09:
        return ExperimentStatus.FAILED, None, rng.choice([
            "Significant epimerization detected by chiral HPLC. Aborted.",
            "Activated ester decomposed before amine addition.",
            "No conversion. Carboxylic acid recovered quantitatively.",
        ])
    y = correlated_yield(rng, fit, base_mu=82.0, base_sigma=10.0)
    notes = rng.choice([
        "Quenched with water, extracted with EtOAc, washed with sat. NaHCO3 and brine.",
        "Acidic and basic aqueous washes to remove HOBt and unreacted amine.",
        "Direct purification by reverse-phase HPLC (0.1% formic acid).",
        "Crystallized from EtOAc/hexanes.",
    ])
    return ExperimentStatus.COMPLETED, y, notes
