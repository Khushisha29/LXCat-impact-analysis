from utils.text_cleaning import preprocess_txt_folder
from utils.species_extraction import process_all_txts
from utils.species_filtering import filter_all_raw_counts
from utils.species_mapping import map_and_aggregate_counts_in_folder
from utils.species_summarize import create_summary
from utils.lxcat_species_filtering import filter_lxcat_gases

def run_gas_TM_pipeline(
        raw_txt_folder,
        cleaned_txt_folder,
        intermediate_folder,
        manually_resolved_csv,
        summary_csv,
        lxcat_csv,
        lxcat_out_csv):
    
    # 1. Clean text
    preprocess_txt_folder(raw_txt_folder, cleaned_txt_folder)

    # 2. Extract species
    process_all_txts(cleaned_txt_folder, intermediate_folder)

    # 3. Filter species
    filter_all_raw_counts(intermediate_folder, cleaned_txt_folder)

    # 4. Map to standardized names
    map_and_aggregate_counts_in_folder(intermediate_folder, manually_resolved_csv)

    # 5. Create summary CSV
    create_summary(intermediate_folder, summary_csv)

    # 6. Filter LXCat gases
    filter_lxcat_gases(summary_csv, lxcat_csv, lxcat_out_csv)
