from utils.pdf_to_md_conversion import convert_pdfs_with_fallback
from utils.md_to_txt_conversion import batch_convert_md_folder
from utils.gas_TM_pipeline import run_gas_TM_pipeline

def run_pipeline():
    # Step 1: Convert PDFs to MDs 
    convert_pdfs_with_fallback("documents/pdfs/", "documents/mds/")
    
    # Step 2: Convert MDs to TXTs
    batch_convert_md_folder(
        input_root="documents/mds/",
        output_root="documents/txts/")
    
    # Step 3: Run Gas TM Pipeline
    run_gas_TM_pipeline(
        raw_txt_folder="documents/txts/",
        cleaned_txt_folder="documents/cleaned_txts/",
        intermediate_folder="documents/intermediate/",
        manually_resolved_csv="documents/manually_resolved_species.csv",
        summary_csv="documents/summary/species_summary.csv",
        lxcat_csv="data/lxcat_gases.csv",
        lxcat_out_csv="documents/summary/lxcat_filtered_species.csv")

if __name__ == "__main__":
    run_pipeline()
