# Protocol and script audit (TGRS draft, 2026-11-24)

This file maps manuscript evidence to the *present repository*; no publication-grade reproduction has been verified from a fresh clone with the actual restricted data.

## Representation accessibility: Tables I and II, Figure 4

- Frozen 3DMAE representation pathway; does NOT use the original full 3DMAEPP Temporal Transformer and QPE decoder as the PatchShot readout.
- Radar-only Table I at 20% support: 384 support and 961 query cases per seed; five paired seeds; H5/H10 threshold-specific labels and support-only calibration.
- Figure 4 uses nested support budgets; ERA5-conditioned comparisons have an additional alignment/development-data protocol. Do not treat them as radar-only budget-matched results.
- Needed to release full code: exact case manifests, readout training, per-seed query predictions, Matched CE and PaCo controls, calibration, OOF envelope, plotting inputs.
- Legacy run_evaluation.py and evaluation/README.md are *generic QPE examples*, not evidence of reproduced manuscript Tables I/II.

## Original structural sensitivity: Table III

- Frozen 3DMAEPP QPE predictor, thresholded low-rainfall patch events (reference threshold 0.1 mm/h), 50 validation cases, 16 draws per perturbation mode.
- Existing family script evaluation/compare_physical_rs_uncertainty.py defaults to 16 draws / 50 batches, with Gaussian std .03, scaling std .10, vertical and frame dropout probability .15, four 64x64 blocks; its default checkpoint must be checked locally.
- Existing targeted-level script evaluation/compare_height_layer_rs_uncertainty.py defaults to only 8 draws / 20 batches: override both to 16 / 50 and set drop probability .5.
- Targeted group code sets all selected levels to zero *together* when a Bernoulli(.5) gate fires. This is not independent per-level dropout. The published mean U group values are 0.0938 / 0.0151 / 0.0176; their mean is 0.0421667 and the defined max/mean ratio is about 2.22.
- Existing code computes score std using distinct conventions across scripts (Torch std vs NumPy std). Verify actual experiment provenance before matching the manuscript's Mean Std. column.
- The data loader, source checkpoint SHA, split, and output CSV must be audited to establish a numerical match.

## Separate heavy/extreme structural sensitivity: Table IV

- Frozen M3_natural, independent 2023 test split, 48 radar scenes and 7,920 evaluated patches, 16 draws, fixed validation-calibrated H5/H10 decisions.
- This is NOT the Table III model or sample population. The source construction of 7,920 patches from 48 scenes is not yet provided in this repository.
- Preserve a separate event-score transform and calibration; do not reuse Table III's 0.0005 QPE-score threshold.
- The current repository does not provide a verified standalone M3_natural Table IV runner.

## Terrain-associated mismatch: Figures 3, 5 and 6

- PatchShot event decisions remain fixed on 6x8 parent grid.
- 12x16, 24x32, 48x64 subdivisions describe finer observational analysis only, not new model predictions.
- Requires registered radar/ref-rain/DEM observations, parent outcomes, landform labels, FP/TN and FN/TP controls, day-cluster bootstrap, and source predictions.
- The current repository does not yet provide the complete terrain-statistics runner.

## Scope of available reproducibility

Public source availability is not equivalent to independently validated numerical reproduction. Keep all restricted data and checkpoints out of version control, document actual provenance, and retain the original evaluation scripts for historical continuity.
