# PatchShot: support-supervised re-access to frozen radar features

The goal is to test whether a frozen radar representation contains
heavy-rain event evidence that a direct prototype or original retrieval
head does not reliably expose.

## Inputs and split

- Frozen, case-organized patch embeddings `z_patch` shaped
  `[cases, patches, feature_dim]`.
- Patch-level binary event labels shaped `[cases, patches]`.
- A **case-disjoint** query set and a support pool. Nested support budgets
  are drawn only from the support pool.
- All training, prototype construction and threshold calibration use
  support examples only.

Case-disjoint does not imply temporally or storm-disjoint. Users should
apply appropriate temporal controls when drawing new conclusions.

## Algorithm

1. Keep the radar encoder frozen.
2. Train a small `Linear → GELU → Linear` projection on support patches
   with a supervised contrastive objective and balanced batches.
3. Normalize the projected embeddings and compute positive/negative
   support prototypes.
4. Calibrate a score threshold by optimizing support CSI, with F1
   tie-breaking.
5. Evaluate on held-out query patches using the unchanged calibration.

The `frozen` and `pca` modes in
`scripts/run_patchshot.py` provide lightweight readout comparisons.
See `patchshot/model.py`, `readout.py` and `evaluation.py` for
configuration defaults and formulas.

## Run on your own authorized features

```bash
python scripts/run_patchshot.py \
  --npz /path/to/local_frozen_patch_features.npz \
  --mode supcon --device cuda \
  --out_dir /path/to/local_output
```

Output CSVs are created **locally** by the user and are not stored in
this repository. The supplied package does not include upstream
radar observations, reference precipitation, extracted features or
model checkpoints. This method implementation alone is not a
complete reproduction of the manuscript.
