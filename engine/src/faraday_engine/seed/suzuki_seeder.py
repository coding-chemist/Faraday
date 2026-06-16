"""Suzuki-Miyaura coupling seeder.

55 experiments. Condition fit considers electronic match (electron-poor aryl halide +
Pd(PPh3)4 is great), steric match (hindered substrate + XPhos preferred), heterocycle
handling (Pd(dppf)Cl2 likes pyridines), and base/solvent combos (K3PO4 + toluene is
classical; aqueous K2CO3 + dioxane is the textbook).
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
from faraday_engine.seed.building_blocks import ARYL_HALIDES, BORONIC_PARTNERS
from faraday_engine.seed.distributions import (
    correlated_yield,
    date_in_last_n_months,
    gaussian_clamped,
    lognormal_time,
    weighted_choice,
)
from faraday_engine.seed.reagent_library import (
    APROTIC_SOLVENTS,
    INERT_ATMOSPHERES,
    INORGANIC_BASES,
    LIGANDS_FOR_PD,
    PD_CATALYSTS,
    PROTIC_SOLVENTS,
)


@SeederRegistry.register(ExperimentType.SUZUKI_COUPLING, count=55)
class SuzukiSeeder(ExperimentSeeder):
    def generate(self) -> Experiment:
        rng = self._rng

        aryl = weighted_choice(rng, [(b, 1.0) for b in ARYL_HALIDES])
        boronic = weighted_choice(rng, [(b, 1.0) for b in BORONIC_PARTNERS])
        pd = weighted_choice(rng, PD_CATALYSTS)
        ligand = weighted_choice(rng, LIGANDS_FOR_PD)
        base = weighted_choice(rng, INORGANIC_BASES)
        # Aqueous co-solvent is common in Suzuki
        use_water = rng.random() < 0.35
        solvent = weighted_choice(rng, APROTIC_SOLVENTS)
        water = next(s for s, _ in PROTIC_SOLVENTS if s.name == "water")

        # --- Condition fit scoring (chemistry credibility lives here) ---
        fit = 0.0
        if "electron_poor" in aryl.class_tags and pd.name.startswith("tetrakis"):
            fit += 0.4
        if "hindered" in aryl.class_tags and ligand.name in {"XPhos", "SPhos"}:
            fit += 0.4
        if "heterocycle" in aryl.class_tags and "dppf" in pd.name:
            fit += 0.3
        if "aryl_chloride" in aryl.class_tags and ligand.name in {"XPhos", "SPhos"}:
            fit += 0.5
        elif "aryl_chloride" in aryl.class_tags:
            fit -= 0.5  # ArCl without bulky ligand → struggles
        if "aryl_iodide" in aryl.class_tags:
            fit += 0.2  # ArI is reactive
        if solvent.name == "1,4-dioxane" and base.name.startswith("potassium phosphate"):
            fit += 0.15  # classical combo
        if solvent.name == "toluene" and use_water:
            fit -= 0.1  # toluene/water is harder to mix
        fit = max(-1.0, min(1.0, fit))

        # --- Stoichiometry (real medchem doses) ---
        substrate_mmol = round(rng.uniform(0.5, 5.0), 2)
        boronic_eq = round(rng.uniform(1.1, 1.5), 2)
        pd_eq = round(rng.choice([0.02, 0.025, 0.03, 0.05, 0.075, 0.1]), 3)
        ligand_eq = pd_eq * round(rng.choice([2, 2.5, 3]), 1) if "Pd2(dba)3" not in pd.name else pd_eq * 4
        base_eq = round(rng.choice([2.0, 2.5, 3.0]), 1)
        temp = gaussian_clamped(rng, mu=95.0, sigma=8.0, low=70.0, high=110.0)
        time_min = lognormal_time(rng, median_h=12.0, sigma=0.4)

        # --- Status (89% completed, 6% failed, 5% in_progress) ---
        roll = rng.random()
        status, yield_pct, result_notes = _resolve_outcome(rng, fit, roll)

        started = date_in_last_n_months(rng, 12)
        completed = started + timedelta(minutes=time_min) if status == ExperimentStatus.COMPLETED else None

        reagents = [
            Reagent(name=aryl.name, role=ReagentRole.SUBSTRATE, cas=aryl.cas, mw=aryl.mw,
                    equivalents=1.0, mass_g=round(substrate_mmol * aryl.mw / 1000, 3),
                    moles_mmol=substrate_mmol, supplier=aryl.supplier),
            Reagent(name=boronic.name, role=ReagentRole.REAGENT, cas=boronic.cas, mw=boronic.mw,
                    equivalents=boronic_eq, mass_g=round(substrate_mmol * boronic_eq * boronic.mw / 1000, 3),
                    moles_mmol=round(substrate_mmol * boronic_eq, 2), supplier=boronic.supplier),
            Reagent(name=pd.name, role=ReagentRole.CATALYST, cas=pd.cas, mw=pd.mw,
                    equivalents=pd_eq, mass_g=round(substrate_mmol * pd_eq * pd.mw / 1000, 4),
                    moles_mmol=round(substrate_mmol * pd_eq, 4), supplier=pd.supplier),
            Reagent(name=ligand.name, role=ReagentRole.LIGAND, cas=ligand.cas, mw=ligand.mw,
                    equivalents=ligand_eq, mass_g=round(substrate_mmol * ligand_eq * ligand.mw / 1000, 4),
                    moles_mmol=round(substrate_mmol * ligand_eq, 4), supplier=ligand.supplier),
            Reagent(name=base.name, role=ReagentRole.BASE, cas=base.cas, mw=base.mw,
                    equivalents=base_eq, mass_g=round(substrate_mmol * base_eq * base.mw / 1000, 3),
                    moles_mmol=round(substrate_mmol * base_eq, 2), supplier=base.supplier),
            Reagent(name=solvent.name, role=ReagentRole.SOLVENT, cas=solvent.cas, mw=solvent.mw,
                    supplier=solvent.supplier),
        ]
        if use_water:
            reagents.append(Reagent(name=water.name, role=ReagentRole.SOLVENT, cas=water.cas,
                                    mw=water.mw, supplier=water.supplier))

        result = None
        if status == ExperimentStatus.COMPLETED and yield_pct is not None:
            product_mass = round(substrate_mmol * (yield_pct / 100) * (aryl.mw + boronic.mw - 80) / 1000, 3)
            result = Result(
                yield_pct=yield_pct,
                purity_pct=round(min(99.5, 88 + rng.uniform(0, 11)), 1),
                mass_g=product_mass,
                moles_mmol=round(substrate_mmol * (yield_pct / 100), 3),
                notes=result_notes,
            )

        return Experiment(
            title=f"Suzuki coupling of {aryl.name} with {boronic.name}",
            type=ExperimentType.SUZUKI_COUPLING,
            status=status,
            solvent_name=f"{solvent.name}/water" if use_water else solvent.name,
            temperature_c=round(temp, 1),
            time_min=time_min,
            atmosphere=weighted_choice(rng, INERT_ATMOSPHERES),
            notes=_pick_procedure_note(rng, fit),
            started_at=started,
            completed_at=completed,
            created_at=started,
            updated_at=completed or started,
            reagents=reagents,
            result=result,
        )


def _resolve_outcome(rng, fit: float, roll: float):
    """Returns (status, yield_pct, result_notes)."""
    if roll < 0.05:
        return ExperimentStatus.IN_PROGRESS, None, None
    if roll < 0.11:
        return ExperimentStatus.FAILED, None, rng.choice([
            "Starting material consumed, no product detected by LCMS.",
            "Pd black formed, complex mixture by TLC. Aborted.",
            "No conversion after 24h. Possible boronic acid decomposition.",
        ])
    y = correlated_yield(rng, fit, base_mu=72.0, base_sigma=12.0)
    notes = rng.choice([
        "Clean product after silica column (10-30% EtOAc/hexanes).",
        "Workup: aqueous Na2CO3 wash, dried over MgSO4, concentrated. Column purified.",
        "Filtered through celite, concentrated, recrystallized from EtOH.",
        "Purified by reverse-phase HPLC (5-95% MeCN/H2O + 0.1% formic acid).",
    ])
    return ExperimentStatus.COMPLETED, y, notes


def _pick_procedure_note(rng, fit: float) -> str:
    if fit > 0.5:
        return rng.choice([
            "Standard conditions. Reaction monitored by TLC every 2h.",
            "Degassed solvent before adding Pd. Clean conversion observed.",
        ])
    if fit < -0.3:
        return rng.choice([
            "Tried this combination — see SOP-SUZUKI-002 for preferred conditions.",
            "Catalyst loading increased to 7.5 mol% after sluggish conversion.",
        ])
    return rng.choice([
        "Reaction prepared under nitrogen via Schlenk technique.",
        "Microwave: 130°C, 30 min — confirmed by LCMS.",
        "Glovebox preparation. Solvent dried over MS 4Å.",
    ])
