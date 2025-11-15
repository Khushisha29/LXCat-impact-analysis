# dict to csv
import os
import json
import pandas as pd

def create_summary(intermediate_root, output_csv):
    rows = []

    for folder in sorted(os.listdir(intermediate_root)):
        base = os.path.join(intermediate_root, folder)
        dict_file = os.path.join(base, f"{folder}_final_chem_counts_dict.txt")

        if not os.path.exists(dict_file):
            continue

        chem_dict = {}
        for line in open(dict_file, "r", encoding="utf-8"):
            if "=>" not in line:
                continue
            chem, count = line.split("=>")
            chem_dict[chem.strip()] = int(count.strip())

        rows.append({
            "filename": f"{folder}.grobid.tei.xml",
            "chemical_counts": json.dumps(chem_dict)
        })

    pd.DataFrame(rows).to_csv(output_csv, index=False)
    print(f"[summary] Saved: {output_csv}")
