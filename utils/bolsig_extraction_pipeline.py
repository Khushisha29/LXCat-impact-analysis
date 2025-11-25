import os
import re
from collections import defaultdict
import pandas as pd

def protect(text: str) -> str:
    ABBREV_PAT = re.compile(
    r'\b(?:Mr|Mrs|Ms|Dr|Prof|Inc|Ltd|Jr|Sr|Co|St|Fig|fig|vs|etc|al|wt|approx|i\.e|e\.g|E\.g|\.com|\.net|\.org)\b\.?'
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

def restore(text: str) -> str:
    return text.replace('<DOT>', '.')

def robust_sentence_split(text: str):

    SPLIT_RGX = re.compile(
    r'(?:(?<=[.!?])\s+(?=(?:"|“|”|\'|’)?[A-Z])|(?<=[.!?]["”’])\s+(?=[A-Z]))'
    )

    safe = protect(text)
    parts = SPLIT_RGX.split(safe)
    return [restore(p).strip() for p in parts if p.strip()]

def join_multiline_sentences(lines):
    buffer = ""
    full_text = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        buffer += " " + line

        if re.search(r'[.!?]"?$', line):  # sentence end
            full_text.append(buffer.strip())
            buffer = ""

    if buffer.strip():  # leftover
        full_text.append(buffer.strip())

    return full_text


# -------------------------
# TOKENIZER
# -------------------------

def smart_tokenize(sentence):
    token_pattern = re.compile(
        r"""
        \([^\(\)]*\)                
        |                           
        [a-zA-Z0-9_\-\.+'\+]+       
        """, re.VERBOSE
    )

    tokens = token_pattern.findall(sentence)

    final_tokens = []
    for tok in tokens:
        if tok.startswith("(") and tok.endswith(")"):
            final_tokens.append(tok)
        else:
            final_tokens.append(tok.lower())

    return final_tokens


# -------------------------
# MAIN PROCESSOR FUNCTION
# -------------------------

def bolsig_processor(txt_input_dir, output_csv):
    
    keywords = {"bolsig+"}
    solver_name = {"bolsig+"}

    # Create output directory if missing
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    # Remove existing CSV (start fresh)
    if os.path.exists(output_csv):
        os.remove(output_csv)

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
                    words = smart_tokenize(lowered)

                    for tok in words:

                        # inside parentheses: (something)
                        if tok.startswith("(") and tok.endswith(")"):
                            inner = tok[1:-1]
                            inner_tokens = smart_tokenize(inner)

                            for db in solver_name:
                                if db.lower() in inner_tokens:
                                    db_doc_frequency[db] += 1

                        # normal token
                        for db in solver_name:
                            if db.lower() == tok:
                                db_doc_frequency[db] += 1

            # merge db-vX versions
            merged_db_frequency = defaultdict(int)
            for db, freq in db_doc_frequency.items():
                match = re.match(r'^([a-z0-9\-]+?)(?:-v[\d\.]+)$', db)
                base = match.group(1) if match else db
                merged_db_frequency[base] += freq

            bolsig_count = merged_db_frequency.get("bolsig+", 0)

            df_row = pd.DataFrame([{
                "file_name": filename.replace(".txt", ""),
                "bolsig+_counts": bolsig_count
            }])

            # Append to CSV
            if not os.path.exists(output_csv):
                df_row.to_csv(output_csv, index=False)
            else:
                df_row.to_csv(output_csv, mode='a', header=False, index=False)

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

    print("\nBOLSIG+ Extraction Pipeline Completed Successfully!")

