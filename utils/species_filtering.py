import os
import re

# ===========================================================
# 1. REACTION-LIKE / IRRELEVANT TERM FILTERS
# ===========================================================

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


# ===========================================================
# 2. FORMULA NORMALIZATION
# ===========================================================

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


# ===========================================================
# 3. NON-CHEMICAL / JUNK WORD REMOVAL
# ===========================================================

JUNK_WORDS = {
    "BOLSIG", "HYDROCARBON", "STAINLESSSTEEL", "QUARTZ",
    "FIGURE", "TABLE", "DATA", "BY"
}

def is_junk(term: str) -> bool:
    return term.upper() in JUNK_WORDS


def looks_like_formula(term: str) -> bool:
    return bool(re.fullmatch(r'[A-Z][A-Za-z0-9]*', term))


# ===========================================================
# 4. FILTER PIPELINE (NO TXT MODIFICATIONS)
# ===========================================================

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
                except:
                    continue

                norm = normalize_formula(chem)

                # Skip unwanted terms
                if (is_junk(norm)
                    or is_reaction_like(norm)
                    or is_irrelevant(norm)
                    or not looks_like_formula(norm)):
                    bad_terms.add(norm)
                    continue

                filtered.append((norm, int(count)))

        # ---- Write ONLY the filtered chemicals ----
        with open(out_file, "w", encoding="utf-8") as f:
            for chem, count in sorted(filtered, key=lambda x: -x[1]):
                f.write(f"{chem}\t{count}\n")

        print(f"[filter] {folder}: {len(filtered)} kept, {len(bad_terms)} removed")