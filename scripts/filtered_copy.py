"""
Copy only the cifs actually needed for a given property from an existing
source folder (e.g. K_VRH), keeping destination folder clean/relevant.
Usage: python filtered_copy.py --prop eij_max --src K_VRH
"""
import argparse
import os
import shutil
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prop", required=True, help="column name in mp_selected_prop.csv")
    parser.add_argument("--src", required=True, help="existing folder name under data/structures to copy from")
    parser.add_argument("--csv", default="data/raw/mp_selected_prop.csv")
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    df[args.prop] = pd.to_numeric(df[args.prop], errors="coerce")
    needed_ids = set(df[df[args.prop].notna()]["ID"])

    src_dir = f"data/structures/{args.src}"
    dst_dir = f"data/structures/{args.prop}"
    os.makedirs(dst_dir, exist_ok=True)

    copied = 0
    for mid in needed_ids:
        src = os.path.join(src_dir, f"{mid}.cif")
        dst = os.path.join(dst_dir, f"{mid}.cif")
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy(src, dst)
            copied += 1

    print(f"Needed ids for {args.prop}: {len(needed_ids)}")
    print(f"Copied {copied} matching cifs from {args.src} into {args.prop}")

if __name__ == "__main__":
    main()