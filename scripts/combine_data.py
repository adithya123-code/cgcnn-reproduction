import pandas as pd
import os

for prop, col_name in [("internal_energy", "U"), ("cv", "Cv")]:
    train = pd.read_csv(f"data/raw/{prop}_training.csv", header=0)
    test = pd.read_csv(f"data/raw/{prop}_test.csv", header=0)

    train = train.iloc[:, -2:]
    test = test.iloc[:, -2:]

    train.columns = ["ID", col_name]
    test.columns = ["ID", col_name]

    combined = pd.concat([train, test], ignore_index=True)
    combined.to_csv(f"data/raw/{col_name}_combined.csv", index=False)
    print(f"{col_name}: {len(combined)} rows written to data/raw/{col_name}_combined.csv")

    os.makedirs(f"data/processed/{col_name}", exist_ok=True)
    test["ID"].to_csv(f"data/processed/{col_name}/paper_test_ids.csv", index=False, header=False)
    print(f"{col_name}: {len(test)} test ids written to data/processed/{col_name}/paper_test_ids.csv")