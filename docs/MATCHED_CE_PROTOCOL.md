# Matched CE re-access — original source and limits

The source archive `PatchShot_OpenReview_Code(1).zip` **does contain** the
Table I `Matched CE re-access` implementation in
`legacy/controls/121e_final_table1_component_attribution.py`
(function `train_matched_ce_projection`, method ID `A3`).

This repository's `patchshot/matched_ce.py` extracts that training
function, with the same Stage-27 adapter (768→256→128), balanced
support-patch batches, AdamW optimizer, step count and learning rate.
A temporary linear CE classifier trains the projection and is
**discarded before prediction**. Evaluation uses support-class prototypes
and support-only CSI threshold calibration exactly as in the PatchShot
readout. This is an **objective-matched CE** comparison, not the
separate `Balanced CE head` (A1), whose head and metrics differ.

```bash
python scripts/run_patchshot.py \
  --npz /authorized/path/to/val_event_patch_features_raw_mae.npz \
  --mode matched_ce --method "Matched CE re-access" \
  --ratios 0.20 --seeds 5 --out_dir /local/matched_ce_output \
  --device cuda
```

Archived real Stage-121e A3 per-seed measurements are under
`reference_results/matched_ce_20pct_per_seed.csv`. These are
**source results**, not a new end-to-end run from this repository.
Mean ± population std for CSI (percent): H5 22.55 ± 1.37;
H10 16.84 ± 0.83. Original restricted 1922-case features and
model checkpoints are not distributed. Full numerical equivalence
needs a new run with authorized features and seed-by-seed checks.

**Separate Table II:** the archive also contains
`legacy/diagnostics/116a_patchshot_probe_accessibility.py`,
which computes prototype/linear/kNN probe CSI using case-grouped
out-of-fold support calibration. That calibration is **not**
used by the Table I/Stage-27 support-only code. The original
script depends on historical Stage-113 features and experiment
paths; it has not yet been refactored into a verified
standalone repository runner. Table II values are not inferred
from Table I files.
