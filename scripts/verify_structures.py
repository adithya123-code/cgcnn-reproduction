"""
Verify a property's structure folder has EXACTLY the needed cifs —
no missing, no extra unrelated ones.
Usage: python verify_structures.py --prop eij_max
"""
import argparse
import os
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prop", required=True)
    parser.add_argument("--csv", default="data/raw/mp_selected_prop.csv")
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    df[args.prop] = pd.to_numeric(df[args.prop], errors="coerce")
    needed_ids = set(df[df[args.prop].notna()]["ID"])

    struct_dir = f"data/structures/{args.prop}"
    have_files = [f[:-4] for f in os.listdir(struct_dir) if f.endswith(".cif")]
    have_ids = set(have_files)

    missing = needed_ids - have_ids
    extra = have_ids - needed_ids

    print(f"=== {args.prop} ===")
    print(f"Needed: {len(needed_ids)}")
    print(f"Have (cif files): {len(have_ids)}")
    print(f"Missing (needed but not fetched): {len(missing)}")
    print(f"Extra (fetched but not needed): {len(extra)}")

    if missing:
        pd.Series(sorted(missing)).to_csv(f"data/processed/{args.prop}/missing_ids.csv", index=False, header=False)
        print(f"  -> saved list to data/processed/{args.prop}/missing_ids.csv")
    if extra:
        pd.Series(sorted(extra)).to_csv(f"data/processed/{args.prop}/extra_ids.csv", index=False, header=False)
        print(f"  -> saved list to data/processed/{args.prop}/extra_ids.csv")

if __name__ == "__main__":
    main()