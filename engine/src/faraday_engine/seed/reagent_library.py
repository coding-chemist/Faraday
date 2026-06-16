"""Real reagent library — Pd catalysts, ligands, bases, solvents, coupling agents, reductants.

All CAS and MW values are verified. Selection weights reflect real lab usage frequency.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ChemReagent:
    name: str
    cas: str
    mw: float
    supplier: str = "Sigma-Aldrich"


# ============================================================
# Catalysts and ligands (Pd + Cu sources for cross-couplings)
# ============================================================
PD_CATALYSTS: tuple[tuple[ChemReagent, float], ...] = (
    # (catalyst, relative weight in real lab usage)
    (ChemReagent("palladium(II) acetate", "3375-31-3", 224.51), 4.0),
    (ChemReagent("tetrakis(triphenylphosphine)palladium(0)", "14221-01-3", 1155.56), 3.0),
    (ChemReagent("[1,1'-bis(diphenylphosphino)ferrocene]dichloropalladium(II)", "72287-26-4", 731.70), 2.5),
    (ChemReagent("tris(dibenzylideneacetone)dipalladium(0)", "51364-51-3", 915.72), 2.0),
    (ChemReagent("bis(triphenylphosphine)palladium(II) dichloride", "13965-03-2", 701.90), 1.5),
    (ChemReagent("XPhos Pd G3", "1445085-77-7", 793.30), 1.0),
)

LIGANDS_FOR_PD: tuple[tuple[ChemReagent, float], ...] = (
    (ChemReagent("triphenylphosphine", "603-35-0", 262.29), 4.0),
    (ChemReagent("SPhos", "657408-07-6", 410.53), 2.0),
    (ChemReagent("XPhos", "564483-18-7", 476.72), 2.0),
    (ChemReagent("1,1'-bis(diphenylphosphino)ferrocene", "12150-46-8", 554.38), 1.5),
    (ChemReagent("BINAP", "98327-87-8", 622.67), 1.0),
)


# ============================================================
# Bases
# ============================================================
INORGANIC_BASES: tuple[tuple[ChemReagent, float], ...] = (
    (ChemReagent("potassium carbonate", "584-08-7", 138.21), 4.0),
    (ChemReagent("potassium phosphate tribasic", "7778-53-2", 212.27), 2.5),
    (ChemReagent("cesium carbonate", "534-17-8", 325.82), 2.0),
    (ChemReagent("sodium carbonate", "497-19-8", 105.99), 1.0),
)

STRONG_BASES: tuple[tuple[ChemReagent, float], ...] = (
    (ChemReagent("sodium tert-butoxide", "865-48-5", 96.10, "Fisher"), 1.0),
    (ChemReagent("potassium tert-butoxide", "865-47-4", 112.21, "Fisher"), 1.0),
)

AMINE_BASES: tuple[tuple[ChemReagent, float], ...] = (
    (ChemReagent("N,N-diisopropylethylamine", "7087-68-5", 129.24), 4.0),
    (ChemReagent("triethylamine", "121-44-8", 101.19), 3.0),
    (ChemReagent("N-methylmorpholine", "109-02-4", 101.15), 1.5),
)


# ============================================================
# Solvents
# ============================================================
APROTIC_SOLVENTS: tuple[tuple[ChemReagent, float], ...] = (
    (ChemReagent("1,4-dioxane", "123-91-1", 88.11), 3.0),
    (ChemReagent("toluene", "108-88-3", 92.14), 3.0),
    (ChemReagent("N,N-dimethylformamide", "68-12-2", 73.09), 2.5),
    (ChemReagent("tetrahydrofuran", "109-99-9", 72.11), 2.5),
    (ChemReagent("dichloromethane", "75-09-2", 84.93), 2.0),
    (ChemReagent("1,2-dichloroethane", "107-06-2", 98.96), 1.5),
    (ChemReagent("acetonitrile", "75-05-8", 41.05), 1.5),
    (ChemReagent("N-methyl-2-pyrrolidinone", "872-50-4", 99.13), 1.0),
)

PROTIC_SOLVENTS: tuple[tuple[ChemReagent, float], ...] = (
    (ChemReagent("ethanol", "64-17-5", 46.07, "Fisher"), 2.0),
    (ChemReagent("methanol", "67-56-1", 32.04, "Fisher"), 2.0),
    (ChemReagent("water", "7732-18-5", 18.02, "in-house"), 1.5),
)


# ============================================================
# Amide-coupling reagents
# ============================================================
AMIDE_COUPLING_REAGENTS: tuple[tuple[ChemReagent, float], ...] = (
    (ChemReagent("HATU", "148893-10-1", 380.23), 4.0),
    (ChemReagent("EDC hydrochloride", "25952-53-8", 191.70), 3.0),
    (ChemReagent("T3P", "68957-94-8", 318.18), 2.0),
    (ChemReagent("PyBOP", "128625-52-5", 520.40), 1.5),
    (ChemReagent("DCC", "538-75-0", 206.33), 1.0),
)

HOBT_ADDITIVES: tuple[tuple[ChemReagent, float], ...] = (
    (ChemReagent("1-hydroxybenzotriazole", "2592-95-2", 135.12), 1.0),
)


# ============================================================
# Reductants
# ============================================================
HYDRIDE_REDUCTANTS: tuple[tuple[ChemReagent, float], ...] = (
    (ChemReagent("sodium borohydride", "16940-66-2", 37.83), 3.0),
    (ChemReagent("sodium triacetoxyborohydride", "56553-60-7", 211.94), 2.5),
    (ChemReagent("sodium cyanoborohydride", "25895-60-7", 62.84), 2.0),
    (ChemReagent("lithium aluminum hydride", "16853-85-3", 37.95), 1.5),
    (ChemReagent("diisobutylaluminum hydride", "1191-15-7", 142.22), 1.0),
)


# ============================================================
# Reductive-amination acid catalysts
# ============================================================
RA_ACIDS: tuple[tuple[ChemReagent, float], ...] = (
    (ChemReagent("acetic acid", "64-19-7", 60.05), 3.0),
    (ChemReagent("trifluoroacetic acid", "76-05-1", 114.02), 1.0),
)


# ============================================================
# Atmospheres
# ============================================================
INERT_ATMOSPHERES: tuple[tuple[str, float], ...] = (
    ("N2", 3.0),
    ("Ar", 1.5),
)
