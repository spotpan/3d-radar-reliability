# PatchShot radar-only reproduction pathway

Source: `PatchShot_OpenReview_Code(1).zip`, extracted clean implementation.
The `patchshot/data.py` and `patchshot/model.py` code and the
metric/readout/evaluation routines here preserve the published Stage-27
methodology. The CLI was compacted for this repository; results must be
checked against actual Stage-27 per-seed CSVs and the original feature arrays.

## What is runnable

```bash
python scripts/run_patchshot.py \
    --npz /authorized/path/to/val_event_patch_features_raw_mae.npz \
    --out_dir /local/patchshot_20pct \
    --labels heavy_5,heavy_10 \
    --ratios 0.20 --seeds 5 --device cuda
```

Inputs must contain `z_patch` of shape `[1922,48,768]` and patch
labels `heavy_5`, `heavy_10` of shape `[1922,48]`; alternatively
`target_max` can be used to construct patch labels. Actual arrays,
checkpoint and station/radar inputs are not redistributed.

For each seed: one 50% query set (961 cases), 20% support (384 cases),
nested support subsets from a fixed support pool. Support and query
**cases** do not overlap; this does not establish time-block or
storm-disjoint independence. Patch-level CSI and AP are computed
from the query patches (not case-level or pixel-level metrics).

Canonical SupCon settings: frozen 768-D inputs; 768->256->128
projection with GELU, L2 normalization, balanced patch batches,
20 epochs, 60 steps/epoch, batch 512, AdamW at 1e-3,
weight decay 1e-4, temperature 0.1. Two support-derived
prototypes; support-only threshold search over 500 candidates,
with a CSI objective and F1 tie-break. Query labels are never
used for training, prototype creation or threshold calibration.
This is *in-sample support calibration*, not an OOF-calibrated
protocol. Table II's separate empirical probe-envelope analysis
must not be conflated with these Table I outputs.

## Coverage and limitations

The present import covers PatchShot and frozen/PCA prototype
comparisons. It **does not** yet include complete audited
implementations of Matched CE, PaCo-Proto, Table II probe
envelopes, ERA5 routing or terrain statistics. The legacy
OpenReview scripts contain local absolute paths and were
not copied wholesale. The 1922-case radar-only and 1918-case
ERA5-aligned experiments are not strictly matched populations.

Published Table I 20% support cross-check values (CSI, percentages):
Frozen prototype H5=16.02/H10=11.91; PatchShot
H5=23.29/H10=16.65. These are reference findings, not outputs
generated during the repository import. Five-seed standard
deviations should follow the manuscript's population or sample
convention consistently.

Use `python -m unittest discover -s tests -v` for elementary
code checks; those checks use synthetic *unit-test fixtures*,
not actual experimental cases.
