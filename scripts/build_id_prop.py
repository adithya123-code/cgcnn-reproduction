"""
Build CGCNN-compatible id_prop.csv (no header, id + target) and copy
atom_init.json into the structures folder so it becomes a full root_dir.
Usage: python build_id_prop.py --prop K_VRH
"""
import argparse
import os
import shutil
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prop", required=True)
    args = parser.parse_args()

    struct_dir = f"data/structures/{args.prop}"
    fetched_csv = f"data/processed/{args.prop}/fetched_ids.csv"

    df = pd.read_csv(fetched_csv)  # columns: ID, <prop>

    df = df[df["ID"].apply(lambda x: os.path.exists(os.path.join(struct_dir, f"{x}.cif")))]

    out_path = os.path.join(struct_dir, "id_prop.csv")
    df.to_csv(out_path, index=False, header=False)
    print(f"Wrote {out_path} with {len(df)} rows")

    src_atom_init = "external/cgcnn/data/sample-regression/atom_init.json"
    dst_atom_init = os.path.join(struct_dir, "atom_init.json")
    shutil.copy(src_atom_init, dst_atom_init)
    print(f"Copied atom_init.json to {dst_atom_init}")

    print(f"\n{struct_dir} is now a complete CGCNN root_dir:")
    print(f"  - {len(df)} .cif files")
    print(f"  - id_prop.csv")
    print(f"  - atom_init.json")

if __name__ == "__main__":
    main()