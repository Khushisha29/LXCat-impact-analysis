import os
import subprocess
from pathlib import Path


def run_marker_batch(input_dir: str, output_dir: str):
    """
    Run marker on a folder of PDFs.
    """
    print("===== Running marker batch mode =====")
    cmd = [
        "marker",
        input_dir,
        "--output_format", "markdown",
        "--disable_image_extraction",
        "--output_dir", output_dir
    ]

    subprocess.run(cmd, check=False)


def run_marker_single(pdf_path: str, output_dir: str):
    """
    Run marker_single for a single PDF.
    """
    print(f"↻ Retrying single file: {pdf_path}")

    cmd = [
        "marker_single",
        pdf_path,
        "--output_format", "markdown",
        "--disable_image_extraction",
        "--output_dir", output_dir
    ]

    subprocess.run(cmd, check=False)


def convert_pdfs_with_fallback(input_dir: str, output_dir: str):
    """
    Convert all PDFs in a folder to MD, retrying failures using marker_single.
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Batch processing
    run_marker_batch(str(input_dir), str(output_dir))

    # Step 2: Fallback for missing/empty MD files
    print("===== Checking for missing MD files =====")

    for pdf_file in input_dir.glob("*.pdf"):
        stem = pdf_file.stem
        md_file = output_dir / f"{stem}.md"

        # Check: file missing or empty
        if not md_file.exists() or md_file.stat().st_size == 0:
            print(f"⚠️  Missing/empty output for: {stem}.md")
            run_marker_single(str(pdf_file), str(output_dir))

    print("===== PDF → MD Conversion Completed Successfully =====")
