import pandas as pd
df = pd.read_csv("data/raw/mp_selected_prop.csv")
for col in ["K_VRH", "eij_max", "n_index", "poly_electronic", "poly_total"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

k_ids = set(df[df["K_VRH"].notna()]["ID"])
for col in ["eij_max", "n_index", "poly_electronic", "poly_total"]:
    prop_ids = set(df[df[col].notna()]["ID"])
    overlap = len(k_ids & prop_ids)
    print(f"{col}: {len(prop_ids)} total, {overlap} overlap with K_VRH ({100*overlap/len(prop_ids):.1f}%)")