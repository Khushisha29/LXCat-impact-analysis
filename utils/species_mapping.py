import os
import re
import pandas as pd
from collections import defaultdict

# ===========================================================
# 1. NORMALIZATION HELPERS
# ===========================================================

SUBSCRIPT_MAP = str.maketrans({
    "₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4",
    "₅": "5", "₆": "6", "₇": "7", "₈": "8", "₉": "9"
})

CHARGE_PATTERN = re.compile(r'[+\-⁺⁻]')

def normalize_formula(s: str) -> str:
    """
    Convert all formula variants into a consistent uppercase form:
    O₂, O_2, O2+, O2−, O 2 → O2
    CO₂ → CO2
    N₂ → N2
    Does NOT convert O2 → oxygen (mapping happens later).
    """
    if not s:
        return s

    s = s.replace(" ", "").replace("_", "")
    s = s.translate(SUBSCRIPT_MAP)
    s = CHARGE_PATTERN.sub("", s)        # remove ANY charge
    return s.upper()


# ===========================================================
# 2. CANONICAL NAME MAPPING (formula → species name)
# ===========================================================

CANONICAL_NAME_MAP = {
    "O2": "oxygen",
    "O":  "oxygen",

    "N2": "nitrogen",
    "N":  "nitrogen",

    "CO2": "carbon dioxide",
    "CO":  "carbon monoxide",
}

def formula_to_name(chem: str) -> str:
    """
    Convert normalized formulas like O2 → oxygen, N2 → nitrogen
    If not in dict, return the formula unchanged.
    """
    return CANONICAL_NAME_MAP.get(chem, chem.lower())


# ===========================================================
# 3. PUBCHEM / RESOLVED NAME CLEANING
# ===========================================================

def clean_label(name: str) -> str:
    name = name.lower().strip()
    name = re.sub(r'^(atomic|molecular|insoluble)\s+', '', name)
    name = re.sub(r'\s+(atom|ion|cation|molecule|gas|radical|metallic|element|gas|dimer)$', '', name)
    name = re.sub(r'[+\-−]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name


# ===========================================================
# 4. LOAD CSV MAPPING FILE
# ===========================================================

def load_filtered_chemicals(csv_path):
    df = pd.read_csv(csv_path)
    df = df[df['resolved_chemical_name'].notna()]

    # mapping name → resolved name
    name_to_resolved = {
        row['chemical_name'].strip().lower(): row['resolved_chemical_name'].strip().lower()
        for _, row in df.iterrows()
    }

    # mapping formula → resolved name
    formula_to_resolved = {
        row['chemical_name'].strip(): row['resolved_chemical_name'].strip().lower()
        for _, row in df.iterrows()
        if re.fullmatch(r'[A-Z][A-Za-z0-9]*', row['chemical_name'])  # crude formula check
    }

    resolved_set = set(name_to_resolved.values()) | set(formula_to_resolved.values())

    return name_to_resolved, formula_to_resolved, resolved_set


# ===========================================================
# 5. MAIN MAPPING + AGGREGATION
# ===========================================================

def map_and_aggregate_counts_in_folder(intermediate_root, csv_path):
    name2res, form2res, resolved_set = load_filtered_chemicals(csv_path)

    subfolders = [
        f for f in os.listdir(intermediate_root)
        if os.path.isdir(os.path.join(intermediate_root, f))
    ]

    for folder in subfolders:
        folder_path = os.path.join(intermediate_root, folder)
        input_file = os.path.join(folder_path, f"{folder}_filtered_chem_counts.txt")
        output_dict = os.path.join(folder_path, f"{folder}_final_chem_counts_dict.txt")
        output_mapping = os.path.join(folder_path, f"{folder}_cde_to_pubchem_mapping.txt")

        if not os.path.exists(input_file):
            print(f"Skipping {folder}: filtered count file not found")
            continue

        final_counts = defaultdict(int)
        mapping_lines = []

        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                # SUPPORT BOTH TABS AND SPACES
                parts = re.split(r'\s+', line.strip())
                if len(parts) != 2:
                    continue

                chem_raw, count = parts[0], int(parts[1])

                # STEP 1 — normalize formulas
                norm = normalize_formula(chem_raw)  # O₂ → O2
                key = norm.lower()

                # STEP 2 — convert formulas to species names
                species = formula_to_name(norm)     # O2 → oxygen

                # STEP 3 — try CSV mappings
                resolved = (
                    form2res.get(norm) or
                    name2res.get(species) or
                    name2res.get(key) or
                    None
                )

                if resolved:
                    final_name = clean_label(resolved)
                    final_counts[final_name] += count
                    mapping_lines.append(f"{chem_raw} => {final_name}")

                else:
                    # unresolved species kept separate but normalized
                    final_counts[species] += count
                    mapping_lines.append(f"{chem_raw} => [UNRESOLVED] ({species})")

        # --------------------------------------------------
        # Save outputs
        # --------------------------------------------------

        with open(output_dict, 'w', encoding='utf-8') as out:
            for chem, c in sorted(final_counts.items(), key=lambda x: x[1], reverse=True):
                out.write(f"{chem} => {c}\n")

        with open(output_mapping, 'w', encoding='utf-8') as m:
            for line in mapping_lines:
                m.write(line + "\n")

        print(f"✅ Folder: {folder} | Final species: {len(final_counts)} | Saved → {output_dict}")
