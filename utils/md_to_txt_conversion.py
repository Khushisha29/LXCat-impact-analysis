import re
from pathlib import Path
import pypandoc

def remove_references_section(text):
    # Match any markdown heading (blue-colored lines in editors)
    # that contain "references" in any form.
    pattern = r"""
        ^\s*                         # Start of line
        \#{1,6}                      # Markdown heading (#, ##, ### ...)
        [^\n]*                       # Anything on that heading line
        references?                  # The word reference/references
        [^\n]*$                      # End of that heading line
    """

    # Search for the 'References' heading
    match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE)

    # If found → remove everything from that point to end
    if match:
        return text[:match.start()].rstrip()

    return text

def convert_md_to_txt(md_path: Path, out_path: Path):
    """Convert a single markdown file to text while removing references."""
    md_text = md_path.read_text(encoding="utf-8", errors="ignore")
    md_text = remove_references_section(md_text)

    # Ensure pandoc exists
    pypandoc.download_pandoc()

    pypandoc.convert_text(
        md_text,
        "plain",
        format="md",
        outputfile=str(out_path),
        extra_args=["--standalone"]
    )

    print(f"✅ Converted: {md_path} → {out_path}")


def batch_convert_md_folder(input_root: str, output_root: str):
    """
    Converts all md files inside nested folders
    """
    input_root = Path(input_root)
    output_root = Path(output_root)
    output_root.mkdir(exist_ok=True, parents=True)

    for folder in input_root.iterdir():
        if folder.is_dir():
            md_file = folder / f"{folder.name}.md"
            if md_file.exists():
                out_file = output_root / f"{folder.name}.txt"
                convert_md_to_txt(md_file, out_file)

    print("\nAll files converted successfully!")
