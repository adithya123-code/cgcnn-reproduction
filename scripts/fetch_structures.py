"""
Fetch structures from Materials Project. Saves each cif under the
REQUESTED mp-id (matches mp_selected_prop.csv), not MP's renamed canonical id.
Handles "no" placeholder values in the property column (converts to real NaN).
Usage: python fetch_structures.py --prop K_VRH
"""
import argparse
import os
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from pymatgen.core import Structure
from pymatgen.io.cif import CifWriter

BASE_URL = "https://api.materialsproject.org/materials/summary/"
MAX_WORKERS = 8

def fetch_one(mid, headers, out_dir):
    cif_path = os.path.join(out_dir, f"{mid}.cif")
    if os.path.exists(cif_path):
        return mid, True
    params = {"material_ids": mid, "_fields": "structure", "_limit": 1}
    try:
        resp = requests.get(BASE_URL, headers=headers, params=params, timeout=30)
        if resp.status_code != 200:
            return mid, False
        data = resp.json().get("data", [])
        if not data:
            return mid, False
        struct = Structure.from_dict(data[0]["structure"])
        CifWriter(struct).write_file(cif_path)  # saved under REQUESTED mid, not response id
        return mid, True
    except Exception:
        return mid, False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prop", required=True)
    parser.add_argument("--csv", default="data/raw/mp_selected_prop.csv")
    args = parser.parse_args()

    api_key = os.environ.get("MP_API_KEY")
    if not api_key:
        raise RuntimeError("Set MP_API_KEY env var first: set MP_API_KEY=your_key")

    df = pd.read_csv(args.csv)

    # fix: missing values stored as string "no", not blank -> convert to real NaN
    df[args.prop] = pd.to_numeric(df[args.prop], errors="coerce")

    df = df[["ID", args.prop]].dropna()
    print(f"Total non-null rows for {args.prop}: {len(df)}")

    out_dir = f"data/structures/{args.prop}"
    os.makedirs(out_dir, exist_ok=True)

    id_to_val = dict(zip(df["ID"], df[args.prop]))
    remaining = [mid for mid in id_to_val if not os.path.exists(os.path.join(out_dir, f"{mid}.cif"))]
    print(f"Already have: {len(id_to_val) - len(remaining)}, remaining: {len(remaining)}")

    headers = {"X-API-KEY": api_key}
    failed = []
    done_count = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(fetch_one, mid, headers, out_dir): mid for mid in remaining}
        for fut in as_completed(futures):
            mid, ok = fut.result()
            if not ok:
                failed.append(mid)
            done_count += 1
            if done_count % 200 == 0:
                print(f"Progress: {done_count}/{len(remaining)} (failed so far: {len(failed)})")

    all_fetched = [mid for mid in id_to_val if os.path.exists(os.path.join(out_dir, f"{mid}.cif"))]
    print(f"\nTotal fetched: {len(all_fetched)}, Failed: {len(failed)}")

    result_df = pd.DataFrame(
        [(mid, id_to_val[mid]) for mid in all_fetched],
        columns=["ID", args.prop]
    )
    result_df.to_csv(f"data/processed/{args.prop}/fetched_ids.csv", index=False)
    if failed:
        pd.Series(failed).to_csv(f"data/processed/{args.prop}/failed_ids.csv", index=False)

if __name__ == "__main__":
    main()