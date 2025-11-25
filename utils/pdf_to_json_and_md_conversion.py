from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
import os
import json
import subprocess
import torch
from pathlib import Path

base_config = {
    "output_format": "json",
    "disable_image_extraction": True,
}

# ================================
# PARALLEL WORKER: JSON
# ================================
def json_worker(args):
    pdf_path, json_path, config_dict = args

    # Reconstruct everything inside the process
    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict
    from marker.config.parser import ConfigParser

    config_parser = ConfigParser(config_dict)
    converter = PdfConverter(
        config=config_parser.generate_config_dict(),
        artifact_dict=create_model_dict(),
        processor_list=config_parser.get_processors(),
        renderer=config_parser.get_renderer(),
    )

    rendered = converter(pdf_path)
    rendered_dict = rendered.model_dump()

    with open(json_path, "w") as f:
        json.dump(rendered_dict, f, indent=4)

    return json_path


# ================================
# PARALLEL WORKER: MD
# ================================
def md_worker(pdf_path_output_dir):
    pdf_path, output_dir = pdf_path_output_dir

    cmd = [
        "marker_single",
        pdf_path,
        "--output_format", "markdown",
        "--disable_image_extraction",
        "--output_dir", output_dir,
    ]
    subprocess.run(cmd, check=False)
    return pdf_path


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
# PARALLEL PDF → JSON
# ================================
def convert_pdfs_to_json_parallel(pdf_folder, json_folder, workers=None):
    os.makedirs(json_folder, exist_ok=True)
    workers = workers or max(1, multiprocessing.cpu_count() - 1)

    pdf_files = sorted([
        f for f in os.listdir(pdf_folder)
        if f.lower().endswith(".pdf")
    ])

    print(f"\n===== Parallel JSON Conversion ({workers} workers) =====")

    # IMPORTANT: capture the config explicitly so it's passed to workers
    config_dict = dict(base_config)

    tasks = []
    for pdf_name in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_name)
        json_path = os.path.join(json_folder, Path(pdf_name).stem + ".json")

        # Pass config_dict instead of base_config
        tasks.append((pdf_path, json_path, config_dict))

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(json_worker, t) for t in tasks]

        for fut in as_completed(futures):
            try:
                result = fut.result()
                print(f"✔ Saved JSON: {result}")
            except Exception as e:
                print(f"❌ JSON conversion failed: {e}")

    print("===== Parallel JSON conversion completed =====\n")


# ================================
# PARALLEL FALLBACK PDF → MD
# ================================
def convert_pdfs_to_md_parallel(pdf_folder, md_folder, workers=None):
    input_dir = Path(pdf_folder)
    output_dir = Path(md_folder)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("===== Running marker batch mode (MD) =====")
    run_marker_batch(str(input_dir), str(output_dir))

    # Fallback
    print("===== Checking for missing/empty MD files =====")

    missing = []
    for pdf_file in input_dir.glob("*.pdf"):
        stem = pdf_file.stem
        md_file = output_dir / f"{stem}.md"

        if not md_file.exists() or md_file.stat().st_size == 0:
            print(f"⚠ Missing/empty MD detected: {md_file.name}")
            missing.append((str(pdf_file), str(output_dir)))

    if not missing:
        print("✓ All Markdown files generated successfully.")
        return

    workers = workers or max(1, multiprocessing.cpu_count() - 1)
    print(f"Running {len(missing)} fallback conversions with {workers} workers")

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(md_worker, t) for t in missing]

        for fut in as_completed(futures):
            try:
                result = fut.result()
                print(f"Completed fallback MD: {result}")
            except Exception as e:
                print(f"MD fallback failed: {e}")

    print("===== Parallel MD fallback completed =====\n")


# ================================
# MAIN PIPELINE (parallel)
# ================================
def run_full_pipeline(pdf_folder, json_folder, md_folder, workers=None):
    print("\nStarting Parallel PDF → JSON + MD pipeline...\n")

    convert_pdfs_to_json_parallel(pdf_folder, json_folder, workers)
    convert_pdfs_to_md_parallel(pdf_folder, md_folder, workers)

    print("\nPDF Conversion Pipeline completed successfully!\n")