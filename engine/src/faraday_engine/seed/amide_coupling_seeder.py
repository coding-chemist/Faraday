"""Amide coupling seeder. 60 experiments — most common reaction in real medchem labs.

Fit considers coupling-reagent quality (HATU/T3P > EDC for hindered partners), base
appropriateness (DIPEA beats Et3N for sluggish couplings), and substrate match (Boc-amino
acids couple cleanly; sterically hindered acids need T3P/PyBOP). HOBt is added with EDC
to suppress racemization.
"""
from datetime import timedelta

from faraday_engine.domain.experiment import (
    Experiment,
    ExperimentStatus,
    ExperimentType,
    Reagent,
    ReagentRole,
    Result,
)
from faraday_engine.seed.base import ExperimentSeeder, SeederRegistry
from faraday_engine.seed.building_blocks import AMINES, CARBOXYLIC_ACIDS
from faraday_engine.seed.distributions import (
    correlated_yield,
    date_in_last_n_months,
    gaussian_clamped,
    lognormal_time,
    weighted_choice,
)
from faraday_engine.seed.reagent_library import (
    AMIDE_COUPLING_REAGENTS,
    AMINE_BASES,
    APROTIC_SOLVENTS,
    HOBT_ADDITIVES,
)


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

        # HOBt usually added with EDC/DCC carbodiimides
        use_hobt = coupler.name in {"EDC hydrochloride", "DCC"}

        fit = 0.0
        if coupler.name in {"HATU", "T3P"}:
            fit += 0.35  # high-yielding workhorses
        if coupler.name in {"EDC hydrochloride"} and use_hobt:
            fit += 0.15  # EDC+HOBt is reliable
        if "amino_acid" in acid.class_tags and coupler.name == "HATU":
            fit += 0.2  # HATU is the gold standard for peptide couplings
        if "hindered" in amine.class_tags and coupler.name in {"T3P", "PyBOP"}:
            fit += 0.25
        if "aromatic" in amine.class_tags and "primary_amine" in amine.class_tags:
            fit -= 0.2  # anilines are sluggish nucleophiles
        if base.name == "N,N-diisopropylethylamine":
            fit += 0.1
        fit = max(-1.0, min(1.0, fit))

        substrate_mmol = round(rng.uniform(0.2, 5.0), 2)
        amine_eq = round(rng.uniform(1.0, 1.3), 2)
        coupler_eq = round(rng.uniform(1.1, 1.5), 2)
        base_eq = round(rng.uniform(2.0, 4.0), 1)
        temp = gaussian_clamped(rng, mu=22.0, sigma=4.0, low=0.0, high=40.0)
        time_min = lognormal_time(rng, median_h=6.0, sigma=0.6)

        roll = rng.random()
        if roll < 0.04:
            status, yield_pct, result_notes = ExperimentStatus.IN_PROGRESS, None, None
        elif roll < 0.09:
            status, yield_pct, result_notes = ExperimentStatus.FAILED, None, rng.choice([
                "Significant epimerization detected by chiral HPLC. Aborted.",
                "Activated ester decomposed before amine addition.",
                "No conversion. Carboxylic acid recovered quantitatively.",
            ])
        else:
            status = ExperimentStatus.COMPLETED
            yield_pct = correlated_yield(rng, fit, base_mu=82.0, base_sigma=10.0)
            result_notes = rng.choice([
                "Quenched with water, extracted with EtOAc, washed with sat. NaHCO3 and brine.",
                "Acidic and basic aqueous washes to remove HOBt and unreacted amine.",
                "Direct purification by reverse-phase HPLC (0.1% formic acid).",
                "Crystallized from EtOAc/hexanes.",
            ])

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
            product_mw_approx = acid.mw + amine.mw - 18  # condensation: -H2O
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
