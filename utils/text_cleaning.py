import re
from pathlib import Path

def clean_text(text: str) -> str:
    """Clean text (remove citations, URLs, LaTeX, math, braces)."""

    # Remove citations like [1], [12,13]
    text = re.sub(r'\[[^\]]*\d+[^\]]*\]', '', text)

    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)

    # Remove LaTeX commands (\rm, \alpha, \textit)
    text = re.sub(r'\\[a-zA-Z]+(\{.*?\})?', '', text)

    # Remove math expressions
    text = re.sub(r'\${1,2}.*?\${1,2}', '', text)

    # Remove leftover braces
    text = re.sub(r'[\{\}]', '', text)

    return text


def preprocess_txt_folder(input_folder: str, output_folder: str):
    in_dir = Path(input_folder)
    out_dir = Path(output_folder)
    out_dir.mkdir(exist_ok=True, parents=True)

    for file in in_dir.glob("*.txt"):
        raw = file.read_text(encoding="utf-8", errors="ignore")
        cleaned = clean_text(raw)
        (out_dir / file.name).write_text(cleaned, encoding="utf-8")
        print(f"[cleaner] Done: {file.name}")

    print(f"All cleaned TXT saved → {out_dir.resolve()}")
