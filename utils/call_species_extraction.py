from species_extraction_pipeline import run_species_extraction_pipeline

run_species_extraction_pipeline(
    raw_txt_folder='documents/txts/',
    intermediate_folder='documents/intermediate/',
    manually_resolved_csv='documents/data/Pubchem_species_mapping.csv',
    summary_csv='documents/species_summary.csv',
    lxcat_csv='documents/data/LXCat_species_mapping.csv',
    lxcat_out_csv='results/data'
)
