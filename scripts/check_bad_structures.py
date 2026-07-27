"""
Test each structure individually through CGCNN's data loader,
find any that produce NaN/Inf or extreme feature values.
"""
import sys
sys.path.insert(0, "external/cgcnn")
from cgcnn.data import CIFData
import numpy as np

dataset = CIFData("data/structures/poly_electronic")
print(f"Total structures: {len(dataset)}")

for i in range(len(dataset)):
    try:
        (atom_fea, nbr_fea, nbr_fea_idx), target, cif_id = dataset[i]
        if np.isnan(atom_fea.numpy()).any() or np.isinf(atom_fea.numpy()).any():
            print(f"BAD (atom_fea NaN/Inf): {cif_id}")
        if np.isnan(nbr_fea.numpy()).any() or np.isinf(nbr_fea.numpy()).any():
            print(f"BAD (nbr_fea NaN/Inf): {cif_id}")
        if abs(target.item()) > 100:  # extreme target value check
            print(f"EXTREME TARGET: {cif_id} = {target.item()}")
    except Exception as e:
        print(f"ERROR loading structure {i}: {e}")