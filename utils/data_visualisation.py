import os
import pandas as pd
import matplotlib.pyplot as plt
import ast
import re

PLOTS_DIR = "results/plots/"

# Create output plot directory
def ensure_plot_dir():
    os.makedirs(PLOTS_DIR, exist_ok=True)

# Load a sheet safely from results.xlsx
def load_sheet(sheet_name):
    excel_path = "results/data/results.xlsx"
    return pd.read_excel(excel_path, sheet_name=sheet_name)

# Load species formula mapping (Gas_name -> Gas_Symbol)
species_map_df = pd.read_csv("documents/data/LXCat_species_mapping.csv")

name_to_formula = {}

for _, row in species_map_df.iterrows():
    name = str(row["Gas_name"]).strip().lower()
    formula = str(row["Gas_Symbol"]).strip()
    if name and formula:
        name_to_formula[name] = formula


def get_formula(name):
    """Convert species name to chemical formula using mapping."""
    if pd.isna(name):
        return name
    key = str(name).strip().lower()
    return name_to_formula.get(key, name)

# Manual override for species → neutral formula
# -----------------------------------------------------------
manual_species_map = {
    "oxygen": "O2",
    "molecular oxygen": "O2",
    "nitrogen": "N2",
    "molecular nitrogen": "N2",
    "hydrogen": "H2",
    "argon": "Ar",
    "xenon": "Xe",
    "carbon": "C",
}

def normalize_formula(formula):
    """
    Normalize charged, isotope & malformed formulas into neutral species.
    Applies manual overrides, removes isotopes, charges, and trailing digits.
    """
    if pd.isna(formula):
        return formula

    f = str(formula).strip()

    # manual override first
    key = f.lower()
    if key in manual_species_map:
        return manual_species_map[key]

    # remove isotope masses (40Ar → Ar)
    f = re.sub(r"^\d+", "", f)

    # remove charges (O2+, O2-, O22+, etc.)
    f = re.sub(r"[+\-]\d*$", "", f)
    f = re.sub(r"\d+[+\-]$", "", f)
    f = f.replace("+", "").replace("-", "")

    # remove trailing digits that are not part of valid formula (O22 → O2, Ar2 → Ar)
    f = re.sub(r"(\D)\d+$", r"\1", f)

    # after cleaning, check manual mapping again
    key2 = f.lower()
    if key2 in manual_species_map:
        return manual_species_map[key2]

    return f


# -----------------------------------------------------------
# Database Name Formatter
# -----------------------------------------------------------
def format_db_name(name):
    if pd.isna(name):
        return name

    mapping = {
        "ist-lisbon": "IST-Lisbon",
        "bsr": "BSR",
        "anu": "ANU",
        "emol-lehavre": "eMol-LeHavre",
        "ccc": "CCC",
        "flinders": "FLINDERS",
        "laplace": "LAPLACE",
        "quantemol": "QUANTEMOL",
        "siglo": "SIGLO",
        "triniti": "TRINITI",
        "unam": "UNAM",
        "ut": "UT",
        "cdap": "CDAP",
        "ethz": "ETHZ",
        "ngfsrdw": "NGFSRDW"
    }

    name_lower = str(name).lower()
    return mapping.get(name_lower, str(name).capitalize())

# -----------------------------------------------------------
# UNIVERSAL column exploding function
# -----------------------------------------------------------
def explode_column(df, column):
    df = df.copy()

    def to_list(val):

        # Case 1: dict (gas, db)
        if isinstance(val, dict):
            return list(val.keys())

        # Case 2: string representation of dict
        if isinstance(val, str) and val.strip().startswith("{") and val.strip().endswith("}"):
            try:
                parsed = ast.literal_eval(val)
                if isinstance(parsed, dict):
                    return list(parsed.keys())
            except:
                pass

        # Case 3: comma or semicolon separated
        if isinstance(val, str) and ("," in val or ";" in val):
            tokens = re.split(r"[;,]", val)
            return [t.strip() for t in tokens if t.strip()]

        # Case 4: single value
        return [str(val).strip()]

    df[column] = df[column].apply(to_list)
    df = df.explode(column)

    df[column] = df[column].astype(str).str.strip()
    df = df[df[column] != ""]
    df = df[df[column].str.lower() != "nan"]
    df = df.dropna(subset=[column])

    return df


# -----------------------------------------------------------
# 1. TOP 10 GASES
# -----------------------------------------------------------
def plot_top_gases():
    print("📊 Generating Top 10 Species plot (names only)...")

    df = load_sheet("Species")

    gas_col = df.columns[1]

    # Expand species column
    df_exp = explode_column(df, gas_col)

    # Clean & keep names ONLY
    df_exp[gas_col] = (
        df_exp[gas_col]
        .astype(str)
        .str.strip()
    )

    # Title-case the words → "molecular oxygen" → "Molecular Oxygen"
    df_exp[gas_col] = df_exp[gas_col].str.title()

    # Compute counts
    gas_counts = df_exp[gas_col].value_counts().head(10)

    plt.figure(figsize=(12, 6))

    bar_color = "#61a3dd"
    plt.bar(
        gas_counts.index,
        gas_counts.values,
        color=bar_color,
        edgecolor="black",
        linewidth=1.5
    )

    plt.title("Top 10 Species", fontsize=18)
    plt.xlabel("Species", fontsize=16)
    plt.ylabel("Number of Publications", fontsize=16)
    plt.xticks(rotation=20, fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()

    out_path = os.path.join(PLOTS_DIR, "top10_species.png")
    plt.savefig(out_path, dpi=300)
    plt.close()

    print(f"✔ Saved: {out_path}")


# -----------------------------------------------------------
# 2. TOP 10 DATABASES
# -----------------------------------------------------------
def plot_top_databases():
    print("📊 Generating Top 10 Databases plot...")

    df = load_sheet("Database")
    db_col = df.columns[1]

    df_exp = explode_column(df, db_col)

    df_exp[db_col] = df_exp[db_col].apply(format_db_name)

    db_counts = df_exp[db_col].value_counts().head(10)

    plt.figure(figsize=(12, 6))

    bar_color = "#61a3dd"
    bars = plt.bar(
        db_counts.index,
        db_counts.values,
        color=bar_color,
        edgecolor="black",
        linewidth=1.5
    )

    plt.title("Top 10 Databases", fontsize=18)
    plt.xlabel("Database", fontsize=16)
    plt.ylabel("Number of Publications", fontsize=16)
    plt.xticks(rotation=45, fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()

    out_path = os.path.join(PLOTS_DIR, "top10_databases.png")
    plt.savefig(out_path, dpi=300)
    plt.close()

    print(f"✔ Saved: {out_path}")


# -----------------------------------------------------------
# 3. TOP 10 COUNTRIES
# -----------------------------------------------------------
def plot_top_countries():
    print("📊 Generating Top 10 Countries plot...")

    df = load_sheet("Country")

    filename_col = df.columns[0]
    country_col = df.columns[1]

    df_exp = explode_column(df, country_col)

    # Capitalize each word in country names
    df_exp[country_col] = df_exp[country_col].str.title()

    # Replace "United States Of America" with "USA"
    df_exp[country_col] = df_exp[country_col].replace({
        "United States Of America": "USA"
    })

    country_counts = df_exp[country_col].value_counts().head(10)

    plt.figure(figsize=(12, 6))

    bar_color = "#61a3dd"
    bars = plt.bar(
        country_counts.index,
        country_counts.values,
        color=bar_color,
        edgecolor="black",
        linewidth=1.5
    )

    plt.title("Top 10 Countries", fontsize=18)
    plt.xlabel("Country", fontsize=16)
    plt.ylabel("Number of Publications", fontsize=16)
    plt.xticks(rotation=45, fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()

    out_path = os.path.join(PLOTS_DIR, "top10_countries.png")
    plt.savefig(out_path, dpi=300)
    plt.close()

    print(f"✔ Saved: {out_path}")



# -----------------------------------------------------------
# MAIN ENTRY
# -----------------------------------------------------------
def generate_all_plots():
    ensure_plot_dir()
    plot_top_gases()
    plot_top_databases()
    plot_top_countries()

    print("\n🎉 All visualisation plots generated successfully!\n")
