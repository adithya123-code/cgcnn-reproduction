import argparse
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--csv", required=True)
parser.add_argument("--prop", required=True)
args = parser.parse_args()

df = pd.read_csv(args.csv, header=None, names=["ID", "true", "pred"])
mae = np.mean(np.abs(df["true"] - df["pred"]))
mad = np.mean(np.abs(df["true"] - df["true"].mean()))
print(f"{args.prop} test set size: {len(df)}")
print(f"Paper's own MAE/MAD ratio: {mae/mad:.4f}")

test_ids = sorted(set(df["ID"]))
pd.Series(test_ids).to_csv(f"data/processed/{args.prop}/paper_test_ids.csv", index=False, header=False)
print(f"Saved {len(test_ids)} test ids")