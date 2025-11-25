import os
from collections import Counter, defaultdict
from pathlib import Path
from chemdataextractor.doc import Document
import re
import pandas as pd
import json
import ast
from pathlib import Path


### Step 1: Species extraction ###
def read_text_as_bytes(path: Path) -> bytes:
    """
    Read a text file and return bytes (utf-8). ChemDataExtractor.from_string expects bytes.
    """
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    return text.encode("utf-8")

def extract_and_count_from_bytes(text_bytes: bytes) -> Counter:
    """
    Create a ChemDataExtractor Document from bytes and count chemical entity mentions.
    Uses Document.from_string (preferred in CDE v2).
    """
    # Use from_string to construct a Document from bytes (v2 API)
    # doc = Document.from_string(text_bytes)
    doc = Document(text_bytes.decode("utf-8", errors="ignore"))

    # doc.cems returns Span-like objects; .text is the chemical string
    names = (c.text.strip() for c in doc.cems if getattr(c, "text", "").strip())
    return Counter(names)

def process_all_txts(in_folder: str, out_root: str):
    in_root = Path(in_folder)
    out_root = Path(out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    txt_files = sorted([p for p in in_root.iterdir() if p.suffix.lower() == ".txt"])

    if not txt_files:
        print("No .txt files found in:", in_root)
        return

    for txt_path in txt_files:
        file_id = txt_path.stem
        folder = out_root / file_id
        folder.mkdir(parents=True, exist_ok=True)

        print(f"[extract] Processing: {txt_path.name}")

        text_bytes = read_text_as_bytes(txt_path)
        counter = extract_and_count_from_bytes(text_bytes)
        # print("[DEBUG] CDE raw species:", counter["CO2"])

        outpath = folder / f"{file_id}_raw_chem_counts.txt"
        with open(outpath, "w", encoding="utf-8") as f:
            # write results sorted by descending count
            for chem, count in counter.most_common():
                f.write(f"{chem}\t{count}\n")

        print(f"[extract] Saved: {outpath}")


### Step 2: Species filtering ###

# 2.1. REACTION-LIKE / IRRELEVANT TERM FILTERS
def is_reaction_like(term):
    return bool(re.search(r'\+|→|--+|=|•|⇒|←', term)) or len(term) > 15

def is_irrelevant(term):
    t = term.lower()
    if re.search(r'\b(sin|cos|theta|phi|omega|alpha|beta|gamma|mu|nu|pi|rho|tau|lambda|manuscript)\b', t):
        return True
    if re.search(r'[=•→←∑∫∞±′″°ϵϑϕ∂∇ΔΓΛΩΨ]', t):
        return True
    if re.match(r'^\d+[a-zA-Z]', t):
        return True
    if '/' in t and len(t.split('/')) > 2:
        return True
    return False


# 2.2. FORMULA NORMALIZATION
SUBSCRIPT_MAP = str.maketrans({
    "₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4",
    "₅": "5", "₆": "6", "₇": "7", "₈": "8", "₉": "9"
})

def normalize_formula(s: str) -> str:
    if not s:
        return s
    s = s.replace(" ", "").replace("_", "")
    s = s.translate(SUBSCRIPT_MAP)
    s = re.sub(r'[+\-⁺⁻]', '', s)
    return s.upper()


# 2.3. NON-CHEMICAL / JUNK WORD REMOVAL
JUNK_WORDS = {
    "BOLSIG", "HYDROCARBON", "STAINLESSSTEEL", "QUARTZ",
    "FIGURE", "TABLE", "DATA", "BY"
}

def is_junk(term: str) -> bool:
    return term.upper() in JUNK_WORDS


# def looks_like_formula(term: str) -> bool:
#     return bool(re.fullmatch(r'[A-Z][A-Za-z0-9]*', term))

def looks_like_formula(term):
    # Accept multi-word chemical names
    if " " in term:
        return True
    # Accept formulas
    return bool(re.fullmatch(r'[A-Z][A-Za-z0-9]*', term))


# 2.4. FILTER PIPELINE
def filter_all_raw_counts(intermediate_root, cleaned_txt_root):

    folders = [
        f for f in os.listdir(intermediate_root)
        if os.path.isdir(os.path.join(intermediate_root, f))
    ]

    for folder in folders:
        base = os.path.join(intermediate_root, folder)

        raw_file = os.path.join(base, f"{folder}_raw_chem_counts.txt")
        out_file = os.path.join(base, f"{folder}_filtered_chem_counts.txt")

        if not os.path.exists(raw_file):
            print(f"[filter] Missing raw file for {folder}")
            continue

        filtered = []
        bad_terms = set()

        with open(raw_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    chem, count = line.strip().split("\t")
                    count = int(count)
                except:
                    continue

                raw = chem.strip()

                # Skip obvious junk
                if is_junk(raw) or is_reaction_like(raw) or is_irrelevant(raw):
                    continue

                # CASE 1 — MULTI WORD NAMES (carbon dioxide, atomic oxygen, carbon dioxide CO2)
                if " " in raw:
                    filtered.append((raw.lower().strip(), count))
                    continue

                # CASE 2 — SINGLE WORD NAMES (oxygen, quartz, tungsten)
                if raw.isalpha():
                    filtered.append((raw.lower().strip(), count))
                    continue

                # CASE 3 — CHEMICAL FORMULAS (CO2, O2, CO2+, H2O)
                norm = normalize_formula(raw)
                filtered.append((norm, count))


        # ---- Write ONLY the filtered chemicals ----
        with open(out_file, "w", encoding="utf-8") as f:
            for chem, count in sorted(filtered, key=lambda x: -x[1]):
                f.write(f"{chem}\t{count}\n")

        print(f"[filter] {folder}: {len(filtered)} kept, {len(bad_terms)} removed")


### Step 3: Species Mapping ###

# 3.1. NORMALIZATION HELPERS (NO NAME MAPPING)
CHARGE_PATTERN = re.compile(r'[+\-⁺⁻]')

def normalize_formula(s: str) -> str:
    """
    Normalize only formulas, not names.
    O₂, O_2, O2+, O2− → O2
    """
    if not s:
        return s
    s = s.replace(" ", "").replace("_", "")
    s = s.translate(SUBSCRIPT_MAP)
    s = CHARGE_PATTERN.sub("", s)
    return s.upper()

# 3.2. LOAD CSV MAPPING FILE (ONLY SOURCE OF MAPPING)
def load_filtered_chemicals(csv_path):
    df = pd.read_csv(csv_path)
    df = df[df["resolved_chemical_name"].notna()]

    # CASE A: "chemical_name" as NAME → resolved NAME
    name_to_resolved = {
        row["chemical_name"].strip().lower(): row["resolved_chemical_name"].strip().lower()
        for _, row in df.iterrows()
    }

    # CASE B: "chemical_name" as FORMULA (CO2, O2, etc.)
    formula_to_resolved = {
        normalize_formula(row["chemical_name"].strip()): row["resolved_chemical_name"].strip().lower()
        for _, row in df.iterrows()
        if re.fullmatch(r"[A-Z][A-Za-z0-9]*", row["chemical_name"])
    }

    resolved_set = set(name_to_resolved.values()) | set(formula_to_resolved.values())
    return name_to_resolved, formula_to_resolved, resolved_set

# 3.3. CLEAN RESOLVED LABEL
def clean_label(name: str) -> str:
    name = name.lower().strip()
    name = re.sub(r"[+\-−]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name

# 3.4. MAPPING + AGGREGATION
def map_and_aggregate_counts_in_folder(intermediate_root, csv_path):
    # Load mapping dictionaries
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

        with open(input_file, "r", encoding="utf-8") as f:
            for line in f:
                parts = re.split(r"\s+", line.strip())
                if len(parts) != 2:
                    continue

                raw_chem, count = parts
                count = int(count)

                raw = raw_chem.strip()
                lower = raw.lower()

                # ---- CASE 1: MULTI-WORD NAME -----------------------------------
                if " " in raw:
                    resolved = name2res.get(lower)
                    if resolved:
                        final_name = clean_label(resolved)
                        final_counts[final_name] += count
                        mapping_lines.append(f"{raw} => {final_name}")
                    else:
                        # keep as multi-word name
                        final_counts[lower] += count
                        mapping_lines.append(f"{raw} => [UNRESOLVED] ({lower})")
                    continue

                # ---- CASE 2: SINGLE WORD NAME (oxygen, helium) -----------------
                if lower.isalpha():
                    resolved = name2res.get(lower)
                    if resolved:
                        final_name = clean_label(resolved)
                        final_counts[final_name] += count
                        mapping_lines.append(f"{raw} => {final_name}")
                    else:
                        final_counts[lower] += count
                        mapping_lines.append(f"{raw} => [UNRESOLVED] ({lower})")
                    continue

                # ---- CASE 3: FORMULA (CO2, O2, CO2+, O(1D)) --------------------
                norm = normalize_formula(raw)

                resolved = form2res.get(norm) or name2res.get(lower)

                if resolved:
                    final_name = clean_label(resolved)
                    final_counts[final_name] += count
                    mapping_lines.append(f"{raw} => {final_name}")
                else:
                    final_counts[norm.lower()] += count
                    mapping_lines.append(f"{raw} => [UNRESOLVED] ({norm})")

        # ---- SAVE OUTPUTS ------------------------------------------------------
        with open(output_dict, "w", encoding="utf-8") as out:
            for chem, c in sorted(final_counts.items(), key=lambda x: -x[1]):
                out.write(f"{chem} => {c}\n")

        with open(output_mapping, "w", encoding="utf-8") as m:
            for line in mapping_lines:
                m.write(line + "\n")

        print(f"✅ Folder: {folder} | Final species: {len(final_counts)} | Saved → {output_dict}")

### Step 4: Species summary ###

# dict to csv
def create_summary(intermediate_root, output_csv):
    rows = []

    for folder in sorted(os.listdir(intermediate_root)):
        base = os.path.join(intermediate_root, folder)
        dict_file = os.path.join(base, f"{folder}_final_chem_counts_dict.txt")

        if not os.path.exists(dict_file):
            continue

        chem_dict = {}
        for line in open(dict_file, "r", encoding="utf-8"):
            if "=>" not in line:
                continue
            chem, count = line.split("=>")
            chem_dict[chem.strip()] = int(count.strip())

        rows.append({
            "filename": f"{folder}.txt",
            "chemical_counts": json.dumps(chem_dict)
        })

    pd.DataFrame(rows).to_csv(output_csv, index=False)
    print(f"[summary] Saved: {output_csv}")


### Step 5: LxCat Species Filtering ###
def filter_lxcat_gases(df_path, lxcat_path, out_dir):
    df = pd.read_csv(df_path)
    df["chemical_counts"] = df["chemical_counts"].apply(ast.literal_eval)

    lxcat = pd.read_csv(lxcat_path)
    lxcat_set = set(lxcat['Gas_name'].str.lower().str.strip())

    # Filter dict by LXCat set
    df["lxcat_gases_count"] = df["chemical_counts"].apply(
        lambda d: {k: v for k, v in d.items() if k.lower() in lxcat_set}
    )

    df = df.drop(['chemical_counts'], axis=1)

    # --- Create output directory ---
    output_dir = Path(out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Output file inside output directory
    out_path = output_dir / "final_lxcat_species.csv"

    df.to_csv(out_path, index=False)
    print("\nSpecies Extraction Pipeline Completed Successfully!")


### Main execution ###
def run_species_extraction_pipeline(
        raw_txt_folder,
        intermediate_folder,
        manually_resolved_csv,
        summary_csv,
        lxcat_csv,
        lxcat_out_csv):
    
    # 1. Extract species
    process_all_txts(raw_txt_folder, intermediate_folder)

    # 2. Filter species
    filter_all_raw_counts(intermediate_folder, raw_txt_folder)

    # 3. Map to standardized names
    map_and_aggregate_counts_in_folder(intermediate_folder, manually_resolved_csv)

    # 4. Create summary CSV
    create_summary(intermediate_folder, summary_csv)

    # 5. Filter LXCat gases
    filter_lxcat_gases(summary_csv, lxcat_csv, lxcat_out_csv)
