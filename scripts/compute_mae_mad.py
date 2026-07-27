"""
Compute MAE/MAD ratio from CGCNN's test_results.csv, matching paper's
reported metric format (mean ± SD once you have multiple seed runs).
Usage: python compute_mae_mad.py --results results/K_VRH/test_results.csv
"""
import argparse
import pandas as pd
import numpy as np

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True)
    args = parser.parse_args()

    # CGCNN's test_results.csv has no header: id, target, prediction
    df = pd.read_csv(args.results, header=None, names=["id", "target", "prediction"])

    mae = np.mean(np.abs(df["target"] - df["prediction"]))
    mad = np.mean(np.abs(df["target"] - df["target"].mean()))
    ratio = mae / mad

    print(f"Test set size: {len(df)}")
    print(f"Target mean: {df['target'].mean():.3f}")
    print(f"MAE (raw units): {mae:.3f}")
    print(f"MAD (raw units): {mad:.3f}")
    print(f"MAE/MAD ratio: {ratio:.4f}")

if __name__ == "__main__":
    main()