import os
import json
import subprocess
import torch
from pathlib import Path
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.config.parser import ConfigParser


# ================================
# GPU CONFIG
# ================================
def configure_gpu():
    if torch.cuda.is_available():
        print("⚡ Using GPU for Marker!")
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
    else:
        print("⚠ No GPU detected. Using CPU only.")


configure_gpu()


# ================================
# MARKER JSON CONVERTER (STATIC SETUP)
# ================================
base_config = {
    "output_format": "json",
    "disable_image_extraction": True,
}

config_parser = ConfigParser(base_config)

json_converter = PdfConverter(
    config=config_parser.generate_config_dict(),
    artifact_dict=create_model_dict(),
    processor_list=config_parser.get_processors(),
    renderer=config_parser.get_renderer(),
)


# ================================
# FUNCTION: Convert PDFs → JSON
# ================================
def convert_pdfs_to_json(pdf_folder, json_folder):
    os.makedirs(json_folder, exist_ok=True)

    pdf_files = sorted([
        f for f in os.listdir(pdf_folder)
        if f.lower().endswith(".pdf")
    ])

    print("\n===== Starting PDF → JSON conversion =====")

    for pdf_name in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_name)
        stem = Path(pdf_name).stem
        json_path = os.path.join(json_folder, f"{stem}.json")

        print(f"Processing JSON: {pdf_name}")

        # Convert
        rendered = json_converter(pdf_path)
        rendered_dict = rendered.model_dump()

        # Save JSON
        with open(json_path, "w") as f:
            json.dump(rendered_dict, f, indent=4)

        print(f"✔ Saved JSON: {json_path}")

    print("===== JSON conversion completed =====\n")


# ================================
# FUNCTIONS FOR PDF → MD
# ================================
def run_marker_batch(input_dir, output_dir):
    print("===== Running marker batch mode (MD) =====")
    cmd = [
        "marker",
        input_dir,
        "--output_format", "markdown",
        "--disable_image_extraction",
        "--output_dir", output_dir,
    ]
    subprocess.run(cmd, check=False)


def run_marker_single(pdf_path, output_dir):
    print(f"↻ Retrying single MD: {pdf_path}")
    cmd = [
        "marker_single",
        pdf_path,
        "--output_format", "markdown",
        "--disable_image_extraction",
        "--output_dir", output_dir,
    ]
    subprocess.run(cmd, check=False)


# ================================
# FUNCTION: Convert PDFs → MD (with fallback)
# ================================
def convert_pdfs_to_md(pdf_folder, md_folder):
    input_dir = Path(pdf_folder)
    output_dir = Path(md_folder)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Batch mode
    run_marker_batch(str(input_dir), str(output_dir))

    # Fallback check
    print("===== Checking for missing/empty MD files =====")

    for pdf_file in input_dir.glob("*.pdf"):
        stem = pdf_file.stem
        md_file = output_dir / f"{stem}.md"

        if not md_file.exists() or md_file.stat().st_size == 0:
            print(f"⚠ Missing/empty MD detected: {md_file.name}")
            run_marker_single(str(pdf_file), str(output_dir))

    print("===== MD conversion completed =====\n")


# ================================
# MAIN PIPELINE FUNCTION
# ================================
def run_full_pipeline(pdf_folder, json_folder, md_folder):
    """
    Run the full pipeline:
    1. Convert PDFs → JSON
    2. Convert PDFs → Markdown (.md)
    """
    print("\nStarting PDF → JSON + MD pipeline...\n")
    convert_pdfs_to_json(pdf_folder, json_folder)
    convert_pdfs_to_md(pdf_folder, md_folder)
    print("\nPDF Conversion Pipeline completed successfully!\n")
