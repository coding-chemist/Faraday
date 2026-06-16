"""Real building blocks — substrates, boronic acids, amines, carbonyls.

CAS numbers and molecular weights are real and verified against PubChem / Sigma-Aldrich.
Each entry includes a `class_tags` set used to bias condition selection (e.g. an
electron-poor aryl bromide pairs well with Pd(PPh3)4; hindered substrates need XPhos).
"""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class BuildingBlock:
    name: str
    cas: str
    mw: float
    supplier: str = "Sigma-Aldrich"
    class_tags: frozenset[str] = field(default_factory=frozenset)


# --- Aryl halides for Suzuki / Buchwald ---
ARYL_HALIDES: tuple[BuildingBlock, ...] = (
    BuildingBlock("4-bromoanisole", "104-92-7", 187.04, class_tags=frozenset({"aryl_bromide", "electron_rich"})),
    BuildingBlock("methyl 4-bromobenzoate", "619-42-1", 215.04, class_tags=frozenset({"aryl_bromide", "electron_poor"})),
    BuildingBlock("4-bromobenzonitrile", "623-00-7", 182.02, class_tags=frozenset({"aryl_bromide", "electron_poor"})),
    BuildingBlock("3-bromopyridine", "626-55-1", 158.00, class_tags=frozenset({"aryl_bromide", "heterocycle", "electron_poor"})),
    BuildingBlock("2-bromopyridine", "109-04-6", 158.00, class_tags=frozenset({"aryl_bromide", "heterocycle", "hindered"})),
    BuildingBlock("4-bromobiphenyl", "92-66-0", 233.10, class_tags=frozenset({"aryl_bromide", "neutral"})),
    BuildingBlock("6-bromoquinoline", "5332-25-2", 208.06, class_tags=frozenset({"aryl_bromide", "heterocycle"})),
    BuildingBlock("4-bromobenzaldehyde", "1122-91-4", 185.02, class_tags=frozenset({"aryl_bromide", "electron_poor"})),
    BuildingBlock("2-bromothiophene", "1003-09-4", 163.04, class_tags=frozenset({"aryl_bromide", "heterocycle"})),
    BuildingBlock("5-bromo-2-methylpyridine", "3510-66-5", 172.02, class_tags=frozenset({"aryl_bromide", "heterocycle", "hindered"})),
    BuildingBlock("4-chloroanisole", "623-12-1", 142.58, class_tags=frozenset({"aryl_chloride", "electron_rich"})),
    BuildingBlock("methyl 4-chlorobenzoate", "1126-46-1", 170.59, class_tags=frozenset({"aryl_chloride", "electron_poor"})),
    BuildingBlock("4-iodotoluene", "624-31-7", 218.04, class_tags=frozenset({"aryl_iodide", "neutral"})),
    BuildingBlock("3-bromothiophene", "872-31-1", 163.04, class_tags=frozenset({"aryl_bromide", "heterocycle"})),
    BuildingBlock("2-bromonaphthalene", "580-13-2", 207.07, class_tags=frozenset({"aryl_bromide", "neutral"})),
)


# --- Boronic acids / esters for Suzuki ---
BORONIC_PARTNERS: tuple[BuildingBlock, ...] = (
    BuildingBlock("phenylboronic acid", "98-80-6", 121.93, class_tags=frozenset({"boronic_acid", "neutral"})),
    BuildingBlock("4-methoxyphenylboronic acid", "5720-07-0", 151.96, class_tags=frozenset({"boronic_acid", "electron_rich"})),
    BuildingBlock("4-fluorophenylboronic acid", "1765-93-1", 139.91, class_tags=frozenset({"boronic_acid", "electron_poor"})),
    BuildingBlock("4-(trifluoromethyl)phenylboronic acid", "128796-39-4", 189.92, class_tags=frozenset({"boronic_acid", "electron_poor"})),
    BuildingBlock("pyridin-3-ylboronic acid", "1692-25-7", 122.92, class_tags=frozenset({"boronic_acid", "heterocycle"})),
    BuildingBlock("naphthalen-2-ylboronic acid", "32316-92-0", 171.99, class_tags=frozenset({"boronic_acid", "hindered"})),
    BuildingBlock("cyclopropylboronic acid", "411235-57-9", 85.89, class_tags=frozenset({"boronic_acid", "sp3"})),
    BuildingBlock("vinylboronic acid pinacol ester", "75927-49-0", 154.02, class_tags=frozenset({"boronate", "alkene"})),
    BuildingBlock("4-(methoxycarbonyl)phenylboronic acid", "99768-12-4", 179.97, class_tags=frozenset({"boronic_acid", "electron_poor"})),
)


# --- Amines for Buchwald, amide coupling, reductive amination ---
AMINES: tuple[BuildingBlock, ...] = (
    BuildingBlock("benzylamine", "100-46-9", 107.15, class_tags=frozenset({"primary_amine", "alkyl"})),
    BuildingBlock("aniline", "62-53-3", 93.13, class_tags=frozenset({"primary_amine", "aromatic"})),
    BuildingBlock("piperidine", "110-89-4", 85.15, class_tags=frozenset({"secondary_amine", "cyclic"})),
    BuildingBlock("morpholine", "110-91-8", 87.12, class_tags=frozenset({"secondary_amine", "cyclic"})),
    BuildingBlock("pyrrolidine", "123-75-1", 71.12, class_tags=frozenset({"secondary_amine", "cyclic"})),
    BuildingBlock("4-methoxybenzylamine", "2393-23-9", 137.18, class_tags=frozenset({"primary_amine", "alkyl"})),
    BuildingBlock("4-aminopyridine", "504-24-5", 94.11, class_tags=frozenset({"primary_amine", "aromatic", "heterocycle"})),
    BuildingBlock("N-methylpiperazine", "109-01-3", 100.16, class_tags=frozenset({"secondary_amine", "cyclic"})),
    BuildingBlock("cyclohexylamine", "108-91-8", 99.17, class_tags=frozenset({"primary_amine", "alkyl", "hindered"})),
    BuildingBlock("3-aminopyridine", "462-08-8", 94.11, class_tags=frozenset({"primary_amine", "aromatic", "heterocycle"})),
)


# --- Carboxylic acids for amide coupling ---
CARBOXYLIC_ACIDS: tuple[BuildingBlock, ...] = (
    BuildingBlock("benzoic acid", "65-85-0", 122.12, class_tags=frozenset({"acid", "aromatic"})),
    BuildingBlock("4-methoxybenzoic acid", "100-09-4", 152.15, class_tags=frozenset({"acid", "aromatic", "electron_rich"})),
    BuildingBlock("4-fluorobenzoic acid", "456-22-4", 140.11, class_tags=frozenset({"acid", "aromatic", "electron_poor"})),
    BuildingBlock("nicotinic acid", "59-67-6", 123.11, class_tags=frozenset({"acid", "aromatic", "heterocycle"})),
    BuildingBlock("N-Boc-L-proline", "15761-39-4", 215.25, class_tags=frozenset({"acid", "amino_acid", "protected"})),
    BuildingBlock("N-Boc-glycine", "4530-20-5", 175.18, class_tags=frozenset({"acid", "amino_acid", "protected"})),
    BuildingBlock("furan-2-carboxylic acid", "88-14-2", 112.08, class_tags=frozenset({"acid", "heterocycle"})),
    BuildingBlock("4-bromobenzoic acid", "586-76-5", 201.02, class_tags=frozenset({"acid", "aromatic"})),
    BuildingBlock("3,4-dimethoxybenzoic acid", "93-07-2", 182.17, class_tags=frozenset({"acid", "aromatic", "electron_rich"})),
)


# --- Carbonyls (aldehydes + ketones) for reductive amination + carbonyl reduction ---
CARBONYLS: tuple[BuildingBlock, ...] = (
    BuildingBlock("benzaldehyde", "100-52-7", 106.12, class_tags=frozenset({"aldehyde", "aromatic"})),
    BuildingBlock("4-methoxybenzaldehyde", "123-11-5", 136.15, class_tags=frozenset({"aldehyde", "aromatic", "electron_rich"})),
    BuildingBlock("cyclohexanone", "108-94-1", 98.15, class_tags=frozenset({"ketone", "cyclic"})),
    BuildingBlock("acetone", "67-64-1", 58.08, class_tags=frozenset({"ketone", "small"})),
    BuildingBlock("4-nitrobenzaldehyde", "555-16-8", 151.12, class_tags=frozenset({"aldehyde", "aromatic", "electron_poor"})),
    BuildingBlock("pyridine-2-carboxaldehyde", "1121-60-4", 107.11, class_tags=frozenset({"aldehyde", "heterocycle"})),
    BuildingBlock("N-Boc-piperidin-4-one", "76855-69-1", 199.25, class_tags=frozenset({"ketone", "cyclic", "protected"})),
    BuildingBlock("isovaleraldehyde", "590-86-3", 86.13, class_tags=frozenset({"aldehyde", "alkyl"})),
    BuildingBlock("cyclopentanone", "120-92-3", 84.12, class_tags=frozenset({"ketone", "cyclic"})),
    BuildingBlock("4-bromobenzaldehyde", "1122-91-4", 185.02, class_tags=frozenset({"aldehyde", "aromatic"})),
)
