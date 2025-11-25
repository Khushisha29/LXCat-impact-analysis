import os
import re
# import matplotlib.pyplot as plt
from collections import defaultdict
import pandas as pd
from collections import OrderedDict


def protect(text):

    ABBREV_PAT = re.compile(
    r'\b(?:Mr|Mrs|Ms|Dr|Prof|Inc|Ltd|Jr|Sr|Co|St|Fig|fig|vs|etc|al|wt|approx|i\.e|e\.g|\.com|\.net|\.org)\b\.?'
    )
    IE_EG_PAT = re.compile(r'\b(?:i\.e|e\.g)\.', flags=re.IGNORECASE)
    DECIMAL_DOT_PAT = re.compile(r'(?<=\d)\.(?=\d)')
    WT_PERCENT_PAT = re.compile(r'(?<=\bwt)\.(?=%)')
    ACRONYM_DOTS_PAT = re.compile(r'\b(?:[A-Za-z]\.){2,}')

    
    text = ABBREV_PAT.sub(lambda m: m.group(0).replace('.', '<DOT>'), text)
    text = IE_EG_PAT.sub(lambda m: m.group(0).replace('.', '<DOT>'), text)
    text = ACRONYM_DOTS_PAT.sub(lambda m: m.group(0).replace('.', '<DOT>'), text)
    text = DECIMAL_DOT_PAT.sub('<DOT>', text)
    text = WT_PERCENT_PAT.sub('<DOT>', text)
    return text


def restore(text):
    return text.replace('<DOT>', '.')


def robust_sentence_split(text):
    SPLIT_RGX = re.compile(
        r'(?:(?<=[.!?])\s+(?=(?:"|“|”|\'|’)?[A-Z])|(?<=[.!?]["”’])\s+(?=[A-Z]))'
    )

    safe = protect(text)
    parts = SPLIT_RGX.split(safe)
    return [restore(p).strip() for p in parts if p.strip()]


# ------------------ JOIN MULTI-LINE SENTENCES ------------------
def join_multiline_sentences(lines):
    buffer = ""
    full_text = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        buffer += " " + line

        if re.search(r'[.!?]"?$', line):
            full_text.append(buffer.strip())
            buffer = ""

    if buffer.strip():
        full_text.append(buffer.strip())

    return full_text


# ------------------ AUTHOR PATTERNS ------------------
def create_flexible_patterns(author_list):
    author_patterns = {}

    for full_name in author_list:
        parts = full_name.replace("-", " ").split()
        initials = "".join([p[0] for p in parts[:-1]])
        surname = parts[-1]

        if initials:
            flexible_initials = (
                r"(?:\b" +
                r"[\s\.\-]*".join(initials) +
                r"[\s\.\-]*\b)?"
            )
        else:
            flexible_initials = ""

        if len(parts) > 2:
            first_name_pattern = re.escape(parts[0]) + r"[\s\-]?" + re.escape(parts[1])
        else:
            first_name_pattern = re.escape(parts[0])

        patterns = [
            fr"\b{first_name_pattern}[\s\-]*{surname}\b",
            fr"\b{flexible_initials}\s*{surname}\b",
            fr"\b{surname},?\s*{flexible_initials}\b",
            fr"\b{surname}\s+et\s+al\.?\b"
        ]

        author_patterns[full_name] = [re.compile(p, re.IGNORECASE) for p in patterns]

    return author_patterns


# ------------------ TOKENIZER ------------------
def smart_tokenize(sentence, author_list):
    patterns = create_flexible_patterns(author_list)

    protected_text = sentence
    found_authors = set()

    for full_name, regex_list in patterns.items():
        for pattern in regex_list:
            matches = pattern.findall(protected_text)
            for match in matches:
                cleaned = match.strip()
                if cleaned not in found_authors:
                    found_authors.add(cleaned)
                    protected = cleaned.replace(" ", "_").replace("-", "_")
                    protected_text = re.sub(
                        re.escape(cleaned), protected, protected_text
                    )

    token_pattern = re.compile(
        r"""
        \([^\(\)]*\)
        |
        [a-zA-Z0-9_\-\.+'\+]+
        """,
        re.VERBOSE
    )

    tokens = token_pattern.findall(protected_text)

    final_tokens = []
    for tok in tokens:
        tok = tok.replace("_", " ")
        if tok.startswith("(") and tok.endswith(")"):
            final_tokens.append(tok)
        else:
            final_tokens.append(tok.lower())

    return final_tokens


# ===================================================================
#                          MAIN PROCESSOR
# ===================================================================
def db_processor(txt_input_dir, output_csv):

    if os.path.exists(output_csv):
        os.remove(output_csv)


    keywords = {'database', 'dataset', 'datasets', 'databases', 'data'}

    known_databases = {
        "anu", "biagi", "biagi-v7.1", "biagi-v8.9", "bordage", "bsr", "budapest", "cdap",
        "ccc", "christophorou", "cop", "dutton", "emol-lehavre", "ethz", "flinders",
        "hayashi", "heidelberg", "iaa", "ist-lisbon", "itikawa", "laporta", "laplace",
        "morgan", "muroranit", "ngfsrdw", "phelps", "puech", "quantemol", "siglo",
        "triniti", "unam", "ut", "viehland", "xjtuaetlab"
    }

    author_list = [
        "S. F. Biagi", "Marie-Claude Bordage", "Loucas G. Christophorou", "Y. Itikawa",
        "Vincenzo Laporta", "W. L. Morgan", "A. V. Phelps", "L. A. Viehland",
        "J. Dutton", "M. Hayashi"
    ]

    
    txt_files = sorted([f for f in os.listdir(txt_input_dir) if f.endswith('.txt')])

    for filename in txt_files:
        file_path = os.path.join(txt_input_dir, filename)

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                raw_lines = file.readlines()

            joined_blocks = join_multiline_sentences(raw_lines)

            matched_sentences = []
            db_doc_frequency = defaultdict(int)

            for block in joined_blocks:
                sentences = robust_sentence_split(block)

                for sentence in sentences:
                    lowered = sentence.lower()

                    if not any(kw in lowered for kw in keywords):
                        continue

                    matched_sentences.append(sentence.strip())

                    words = smart_tokenize(lowered, author_list)

                    for tok in words:
                        for db in known_databases:
                            if db.lower() == tok:
                                db_doc_frequency[db] += 1

                    if tok.startswith("(") and tok.endswith(")"):
                        inner = tok[1:-1]
                        inner_tokens = smart_tokenize(inner, author_list)
                        for db in known_databases:
                            if db.lower() in inner_tokens:
                                db_doc_frequency[db] += 1

            merged_db_frequency = defaultdict(int)
            for db, freq in db_doc_frequency.items():
                match = re.match(r'^([a-z0-9\-]+?)(?:-v[\d\.]+)$', db)
                base = match.group(1) if match else db
                merged_db_frequency[base] += freq
            
            ####-------To Store output in csv------------------------------
            sorted_items = sorted(merged_db_frequency.items(), key=lambda x: x[1], reverse=True)

            sorted_dict = OrderedDict(sorted_items)


            # Convert to JSON-like string
            db_json_str = "{" + ", ".join([f'"{db}": {freq}' for db, freq in sorted_dict.items()]) + "}"

            df_row = pd.DataFrame([{
                "file_name": filename.replace(".txt", ""),
                "Database_Counts": db_json_str
            }])

            # Append to CSV
            if not os.path.exists(output_csv):
                df_row.to_csv(output_csv, index=False)
            else:
                df_row.to_csv(output_csv, mode='a', header=False, index=False)

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
    print("Database Extraction Pipeline Completed Successfully!")