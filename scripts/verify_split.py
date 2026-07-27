"""
Directly replicates CGCNN's exact shuffle on the CURRENT id_prop.csv,
tells us the REAL resulting test set, to check against paper's ids.
Usage: python verify_split.py --prop n_index --test-size 1414 --val-size 705
"""
import argparse
import csv
import random
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--prop", required=True)
parser.add_argument("--test-size", type=int, required=True)
parser.add_argument("--val-size", type=int, required=True)
args = parser.parse_args()

path = f"data/structures/{args.prop}/id_prop.csv"
with open(path) as f:
    reader = csv.reader(f)
    rows = [row for row in reader]

N = len(rows)
print(f"Actual N (as CGCNN would see it): {N}")

# check for duplicate ids
ids = [r[0] for r in rows]
dupes = len(ids) - len(set(ids))
print(f"Duplicate ids in file: {dupes}")

random.seed(123)
random.shuffle(rows)

test_rows = rows[-args.test_size:]
test_ids_actual = set(r[0] for r in test_rows)

paper_ids = set(pd.read_csv(f"data/processed/{args.prop}/paper_test_ids.csv", header=None)[0])

overlap = test_ids_actual & paper_ids
print(f"Overlap with paper test ids: {len(overlap)} / {len(paper_ids)}")