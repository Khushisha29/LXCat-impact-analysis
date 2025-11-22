import subprocess
import shutil
import pandas as pd
import os
import zipfile
from utils.pdf_to_json_and_md_conversion import run_full_pipeline
from utils.md_cleaning import process_md_folders
from utils.md_to_txt_conversion import batch_convert_md_folder
from utils.database_extraction_pipeline import db_processor
from utils.bolsig_extraction_pipeline import bolsig_processor
from utils.country_fetching_pipeline import country_fetch_main
from utils.data_visualisation import generate_all_plots

def write_to_results_excel(sheet_name, dataframe, output_dir="results/data",
                           keep_csv=True, csv_path=None):
    """
    Writes a dataframe into results.xlsx (append sheet).
    Optionally deletes the original CSV (no zip).
    """

    # Ensure results folder exists
    os.makedirs(output_dir, exist_ok=True)

    # Excel file path
    excel_path = os.path.join(output_dir, "results.xlsx")

    # Append or create Excel
    if os.path.exists(excel_path):
        with pd.ExcelWriter(excel_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            dataframe.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            dataframe.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"✔ Added sheet '{sheet_name}' to results.xlsx")

    # DELETE CSV if keep_csv=False
    if csv_path and not keep_csv:
        if os.path.exists(csv_path):
            os.remove(csv_path)
            print(f"🗑 Deleted raw CSV: {csv_path}")
        else:
            print(f"⚠ CSV not found for deletion: {csv_path}")

    # DELETE zip if exists
    zip_path = os.path.join(output_dir, "raw_results.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)
        print(f"🗑 Deleted existing zip file: {zip_path}")


def run_pipeline():

    # Step 1: Convert PDF to MD and JSON
    run_full_pipeline(
        pdf_folder="documents/pdfs/",
        json_folder="documents/jsons/",
        md_folder="documents/mds/"
    )

    # Step 2: Md cleaning
    process_md_folders("documents/mds/", "documents/cleaned_mds/")
    
    # Step 3: Convert MDs to TXTs
    batch_convert_md_folder(
        input_root="documents/cleaned_mds/",
        output_root="documents/txts/"
    )

    # Step 4: Database Extraction Pipeline
    db_processor(
        txt_input_dir="documents/txts/",
        output_csv="results/data/Database_counts.csv"
    )

    # Step 5: Bolsig+ Extraction Pipeline
    bolsig_processor(
        txt_input_dir="documents/txts/",
        output_csv="results/data/bolsig+_counts.csv"
    )

    # Step 6: Country Fetching Pipeline
    country_fetch_main(
        input_folder="documents/jsons/",
        output_csv="results/data/country_fetch_outputs.csv"
    )

    # Step 7: Gas TM Pipeline (Python 3.9 env)
    print("\n\n=== Switching to python 3.9 Gas TM environment ===\n")

    subprocess.run([
        "mamba", "run", "-n", "lxcat_cde", "python",
        "-c",
        (
            "from utils.species_extraction_pipeline import run_species_extraction_pipeline; "
            "run_species_extraction_pipeline("
            "raw_txt_folder='documents/txts/',"
            "intermediate_folder='documents/intermediate/',"
            "manually_resolved_csv='documents/data/Pubchem_species_mapping.csv',"
            "summary_csv='documents/species_summary.csv',"
            "lxcat_csv='documents/data/LXCat_species_mapping.csv',"
            "lxcat_out_csv='results/data'"
            ");"
        )
    ], check=True)

    # Remove intermediate folder and summary file
    intermediate_folder = "documents/intermediate/"
    summary_file = "documents/species_summary.csv"

    if os.path.exists(intermediate_folder) and os.path.isdir(summary_file):
        shutil.rmtree(intermediate_folder)
        shutil.rmtree(summary_file)
        print(f"Deleted intermediate folder: {intermediate_folder}")
        print(f"Deleted summary file: {summary_file}")
    else:
        print("intermediate folder or summary file not found — skipping delete")


    # Step 8: Store results

    # Store species result
    gas_csv = "results/data/final_lxcat_species.csv"
    gas_df = pd.read_csv(gas_csv)
    write_to_results_excel(
        sheet_name="Species",
        dataframe=gas_df,
        keep_csv=False,
        csv_path=gas_csv
    )

    # Store database result
    db_csv = "results/data/Database_counts.csv"
    db_df = pd.read_csv(db_csv)
    write_to_results_excel(
        sheet_name="Database",
        dataframe=db_df,
        keep_csv=False,
        csv_path=db_csv
    )

    # Store bolsig+ result
    bs_csv = "results/data/bolsig+_counts.csv"
    bs_df = pd.read_csv(bs_csv)
    write_to_results_excel(
        sheet_name="Bolsig",
        dataframe=bs_df,
        keep_csv=False,
        csv_path=bs_csv
    )

    # Store country fetch result
    ct_csv = "results/data/country_fetch_outputs.csv"
    ct_df = pd.read_csv(ct_csv)
    write_to_results_excel(
        sheet_name="Country",
        dataframe=ct_df,
        keep_csv=False,
        csv_path=ct_csv
    )

    # Step 9: Create Visualisations
    print("\n=== Generating Visualisation Plots ===\n")
    generate_all_plots()

    print("=== Entire Pipeline Completed Successfully!! ===")

if __name__ == "__main__": 
    run_pipeline()