import pandas as pd
import ast

def filter_lxcat_gases(df_path, lxcat_path, out_path):
    df = pd.read_csv(df_path)
    df["chemical_counts"] = df["chemical_counts"].apply(ast.literal_eval)

    lxcat = pd.read_csv(lxcat_path)
    lxcat_set = set(lxcat['Gas_name'].str.lower().str.strip())

    # Filter dict by LXCat set
    df["lxcat_gases_count"] = df["chemical_counts"].apply(
        lambda d: {k: v for k, v in d.items() if k.lower() in lxcat_set}
    )

    df.to_csv(out_path, index=False)
    print(f"[lxcat] Saved: {out_path}")
