"""
Pre-arranges id_prop.csv rows so that after CGCNN's internal
random.seed(123) shuffle, the exact test set matches paper's ids.
Usage: python build_matched_split.py --prop K_VRH
"""
import argparse
import os
import random
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prop", required=True)
    parser.add_argument("--val-frac", type=float, default=0.1)
    args = parser.parse_args()

    struct_dir = f"data/structures/{args.prop}"
    fetched_csv = f"data/processed/{args.prop}/fetched_ids.csv"
    test_ids_csv = f"data/processed/{args.prop}/paper_test_ids.csv"

    df = pd.read_csv(fetched_csv)
    prop_col = df.columns[1]
    df = df[df["ID"].apply(lambda x: os.path.exists(os.path.join(struct_dir, f"{x}.cif")))]
    id_to_val = dict(zip(df["ID"], df[prop_col]))

    paper_test_ids = list(pd.read_csv(test_ids_csv, header=None)[0])
    test_ids = [i for i in paper_test_ids if i in id_to_val]
    test_size = len(test_ids)
    print(f"Paper test ids available in our fetched set: {test_size} / {len(paper_test_ids)}")

    remaining_ids = [i for i in id_to_val if i not in set(test_ids)]
    N = len(id_to_val)
    val_size = int(N * args.val_frac)
    train_size = N - val_size - test_size

    random.Random(0).shuffle(remaining_ids)  # arbitrary order for train/val pick, not the CGCNN seed
    val_ids = remaining_ids[:val_size]
    train_ids = remaining_ids[val_size:]

    # desired FINAL order after CGCNN's internal shuffle
    desired_order = train_ids + val_ids + test_ids  # train first, val next, test last
    assert len(desired_order) == N

    # simulate CGCNN's exact shuffle to find the permutation
    dummy = list(range(N))
    random.seed(123)
    random.shuffle(dummy)
    # dummy[i] = original position that lands at final position i after shuffle

    # build the PRE-shuffle order we must write, so post-shuffle == desired_order
    pre_shuffle = [None] * N
    for i in range(N):
        pre_shuffle[dummy[i]] = desired_order[i]

    out_path = os.path.join(struct_dir, "id_prop.csv")
    with open(out_path, "w", newline="") as f:
        for _id in pre_shuffle:
            f.write(f"{_id},{id_to_val[_id]}\n")

    print(f"Wrote {out_path}: train={train_size}, val={val_size}, test={test_size}")
    print(f"Train with: --train-size {train_size} --val-size {val_size} --test-size {test_size}")

if __name__ == "__main__":
    main()