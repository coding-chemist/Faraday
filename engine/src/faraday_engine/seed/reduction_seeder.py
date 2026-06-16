"""Carbonyl reduction seeder. 25 experiments.

Fit considers selectivity: NaBH4 reduces aldehydes faster than ketones (chemoselective);
LiAlH4 reduces everything (over-reduction risk); DIBAL is for selective aldehyde-from-ester
or partial reductions at low temperature.
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
from faraday_engine.seed.building_blocks import CARBONYLS
from faraday_engine.seed.distributions import (
    correlated_yield,
    date_in_last_n_months,
    gaussian_clamped,
    lognormal_time,
    weighted_choice,
)
from faraday_engine.seed.reagent_library import (
    APROTIC_SOLVENTS,
    HYDRIDE_REDUCTANTS,
    PROTIC_SOLVENTS,
)


@SeederRegistry.register(ExperimentType.CARBONYL_REDUCTION, count=25)
class CarbonylReductionSeeder(ExperimentSeeder):
    def generate(self) -> Experiment:
        rng = self._rng

        carbonyl = weighted_choice(rng, [(c, 1.0) for c in CARBONYLS])
        reductant = weighted_choice(rng, HYDRIDE_REDUCTANTS)

        # Reductant-driven solvent + temperature choice
        if reductant.name == "sodium borohydride":
            solvent = weighted_choice(rng, [(s, w) for s, w in PROTIC_SOLVENTS
                                            if s.name in {"methanol", "ethanol"}])
            temp = gaussian_clamped(rng, mu=5.0, sigma=4.0, low=-5.0, high=25.0)
        elif reductant.name == "lithium aluminum hydride":
            solvent = weighted_choice(rng, [(s, w) for s, w in APROTIC_SOLVENTS
                                            if s.name in {"tetrahydrofuran", "diethyl ether",
                                                          "1,4-dioxane"} or s.name == "tetrahydrofuran"])
            temp = gaussian_clamped(rng, mu=10.0, sigma=8.0, low=-10.0, high=40.0)
        elif reductant.name == "diisobutylaluminum hydride":
            solvent = weighted_choice(rng, [(s, w) for s, w in APROTIC_SOLVENTS
                                            if s.name in {"toluene", "dichloromethane",
                                                          "tetrahydrofuran"}])
            temp = gaussian_clamped(rng, mu=-65.0, sigma=10.0, low=-78.0, high=-40.0)
        else:
            solvent = weighted_choice(rng, [(s, w) for s, w in APROTIC_SOLVENTS
                                            if s.name == "tetrahydrofuran"])
            temp = gaussian_clamped(rng, mu=22.0, sigma=4.0, low=0.0, high=40.0)

        fit = 0.0
        if reductant.name == "sodium borohydride" and "aldehyde" in carbonyl.class_tags:
            fit += 0.4  # NaBH4 + aldehyde is textbook
        if reductant.name == "sodium borohydride" and "ketone" in carbonyl.class_tags:
            fit += 0.1  # works but slower
        if reductant.name == "lithium aluminum hydride":
            fit += 0.2  # broadly works
            if "protected" in carbonyl.class_tags:
                fit -= 0.3  # may remove Boc/other protecting groups
        if reductant.name == "diisobutylaluminum hydride" and "aldehyde" in carbonyl.class_tags:
            fit -= 0.2  # over-reduction to alcohol is risky here
        if reductant.name == "sodium cyanoborohydride":
            fit -= 0.3  # NaBH3CN is too weak for plain carbonyl reduction
        if reductant.name == "sodium triacetoxyborohydride":
            fit -= 0.4  # STAB doesn't reduce carbonyls efficiently on its own
        fit = max(-1.0, min(1.0, fit))

        substrate_mmol = round(rng.uniform(0.5, 5.0), 2)
        reductant_eq = round(rng.uniform(1.0, 2.5), 2)
        time_min = lognormal_time(rng, median_h=3.0, sigma=0.6)

        roll = rng.random()
        if roll < 0.05:
            status, yield_pct, result_notes = ExperimentStatus.IN_PROGRESS, None, None
        elif roll < 0.10:
            status, yield_pct, result_notes = ExperimentStatus.FAILED, None, rng.choice([
                "Over-reduction observed by LCMS.",
                "Quench too aggressive — exotherm, product decomposition.",
                "Protecting group cleaved during reduction.",
            ])
        else:
            status = ExperimentStatus.COMPLETED
            yield_pct = correlated_yield(rng, fit, base_mu=78.0, base_sigma=12.0)
            result_notes = rng.choice([
                "Quenched with sat. NH4Cl, extracted with EtOAc, dried over MgSO4.",
                "Cold quench (1M HCl), then standard aqueous workup.",
                "Filtered through celite, concentrated, used directly.",
                "Distilled at reduced pressure.",
            ])

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
            product_mw_approx = carbonyl.mw + 2  # carbonyl + H2
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
