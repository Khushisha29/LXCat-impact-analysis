import os
from collections import Counter
from pathlib import Path
# CDE v2 import 
from chemdataextractor.doc import Document

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
    doc = Document.from_string(text_bytes)

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

        outpath = folder / f"{file_id}_raw_chem_counts.txt"
        with open(outpath, "w", encoding="utf-8") as f:
            # write results sorted by descending count
            for chem, count in counter.most_common():
                f.write(f"{chem}\t{count}\n")

        print(f"[extract] Saved: {outpath}")
