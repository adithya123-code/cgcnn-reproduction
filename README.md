# cgcnn-reproduction
# CGCNN Benchmark Reproduction

## Overview

This repository contains the reproduction of the benchmark experiments reported in the paper:

**"Examining graph neural networks for crystal structures:
Limitations and opportunities for capturing periodicity"**

The objective is to reproduce the reported CGCNN benchmark results on various material properties from the Materials Project database by following the original methodology as closely as possible.

---

## Project Objectives

- Reproduce the CGCNN benchmark results reported in the paper.
- Match the original paper's train/validation/test split.
- Download the required crystal structures from the Materials Project.
- Train the original CGCNN implementation.
- Evaluate using the MAE/MAD metric reported in the paper.
- Investigate discrepancies between reproduced and published results.

---

# Repository Structure

```
cgcnn-reproduction/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── structures/
│
├── external/
│   └── cgcnn/
│
├── results/
│
├── scripts/
│
├── README.md
├── requirements.txt
└── .gitignore

# Materials Project API

Set the API key before downloading structures.

Windows

```cmd
set MP_API_KEY=YOUR_API_KEY
```

Linux

```bash
export MP_API_KEY=YOUR_API_KEY
```

---

# Workflow

The complete workflow followed during reproduction is:

```
Paper Dataset
        │
        ▼
Extract paper test IDs
        │
        ▼
Fetch crystal structures
        │
        ▼
Verify downloaded CIFs
        │
        ▼
Generate matched id_prop.csv
        │
        ▼
Train original CGCNN
        │
        ▼
Evaluate test set
        │
        ▼
Compute MAE/MAD
```

---

# Scripts

## fetch_structures.py

Downloads crystal structures from the Materials Project.

Example

```bash
python scripts/fetch_structures.py --prop K_VRH
```

---

## build_matched_split.py

Creates an `id_prop.csv` such that after CGCNN's internal random shuffle (`random.seed(123)`), the paper's published test set becomes the final test set used during training.

Example

```bash
python scripts/build_matched_split.py --prop K_VRH
```

---

## paper_reference.py

Extracts

- paper test material IDs
- paper MAE/MAD ratio

Example

```bash
python scripts/paper_reference.py --csv data/raw/test_cgcnn_n_index.csv --prop n_index
```

---

## compute_mae_mad.py

Computes

- Test MAE
- Test MAD
- MAE/MAD ratio

Example

```bash
python scripts/compute_mae_mad.py --results results/n_index/test_results.csv
```

---

## filtered_copy.py

Copies already downloaded CIF files from another property if both datasets contain identical material IDs.

Example

```bash
python scripts/filtered_copy.py --prop poly_total --src poly_electronic
```

---

## verify_split.py

Verifies

- dataset size
- duplicate IDs
- overlap with paper test IDs

---

## verify_structures.py

Checks

- missing CIF files
- corrupted structures
- incomplete downloads

---

# Training

Example

```bash
cd results/K_VRH

python ../../external/cgcnn/main.py \
    --train-size 4567 \
    --val-size 650 \
    --test-size 1305 \
    --epochs 300 \
    --batch-size 256 \
    --workers 0 \
    ../../data/structures/K_VRH
```

For some properties Adam optimizer with a smaller learning rate was evaluated:

```bash
--optim Adam --lr 0.001
```

---

# Properties Reproduced

| Property | Dataset |
|----------|----------|
| Bulk modulus (K_VRH) | Materials Project |
| Shear modulus (G_VRH) | Materials Project |
| Refractive Index (n_index) | Materials Project |
| Electronic dielectric constant (poly_electronic) | Materials Project |
| Total dielectric constant (poly_total) | Materials Project |
| Internal Energy (U) | Materials Project |
| Heat Capacity (Cv) | Materials Project |
| Piezoelectric modulus (eij_max) | Materials Project |

---

# Current Results

| Property | Paper MAE/MAD | Reproduced MAE/MAD | Status |
|-----------|---------------|-------------------|--------|
| K_VRH | 0.22 ± 0.02 | 0.2463 | Close reproduction |
| G_VRH | 0.40 ± 0.02 | 0.66 | Under investigation |
| U | 0.71 ± 0.03 | 0.6729 | Successfully reproduced |
| Cv | 0.76 ± 0.04 | 0.7772 | Successfully reproduced |
| eij_max | 0.81 | 0.8881 | Reasonably close |
| n_index | 0.24 | 0.4762 | Under investigation |
| poly_electronic | 0.256 | 0.2932 | Improved after filtering |
| poly_total |0.56  | 0.5239 |

---

# Important Findings

During reproduction several issues were identified:

- Exact paper test IDs were reconstructed by pre-arranging `id_prop.csv`.
- Missing Materials Project structures reduced the available benchmark size for some datasets.
- Several dielectric constant values in the downloaded Materials Project dataset were physically implausible.
- Filtering unrealistic dielectric values significantly improved training stability.
- Adam optimizer (`lr = 0.001`) provided more stable optimization for dielectric property prediction.
- Original CGCNN internally performs target normalization, while the benchmark dataset released with the paper uses median and percentile-based normalization. This difference is under investigation.

---

# Reproduction Notes

The original paper publishes the exact test IDs.

Instead of modifying CGCNN source code, this project reconstructs the identical split by generating a specially ordered `id_prop.csv`.

After CGCNN performs its internal

```python
random.seed(123)
random.shuffle(dataset)
```

the resulting test partition matches the paper's published benchmark.



# Future Work

- Investigate normalization differences between the released benchmark dataset and the original CGCNN implementation.
- Compare CGCNN with ALIGNN and other graph neural network models.
- Extend the benchmark to additional Materials Project properties.
- Evaluate descriptor-hybridized graph neural networks.



# References

1. Xie, T., & Grossman, J. C. Crystal Graph Convolutional Neural Networks for an Accurate and Interpretable Prediction of Material Properties.

2. Improving Deep Representation Learning for Crystal Structures by Learning and Hybridizing Human-Designed Descriptors.

3. Materials Project

https://materialsproject.org



