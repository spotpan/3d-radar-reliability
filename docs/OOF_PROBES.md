# Case-grouped out-of-fold readout probes

This module describes **how to compute** a support-calibrated empirical
readout envelope from already available representations. It does not
contain manuscript numerical results.

The implemented probe families are:
- positive/negative prototype score
- balanced linear classification score
- k-nearest-neighbor score

Each probe fits on training support *cases*, predicts held-out support
cases, and uses those out-of-fold scores to select an event threshold.
The probe then fits on all support cases and predicts the fixed query
set with that support-derived threshold.

An empirical envelope is the maximum evaluated query CSI across these
specific probes for an experiment. It is **not an information-theoretic
bound** and should not be compared to an experiment using a different
split, representation, label, or calibration family without qualification.

## Method-only entrypoint

```bash
python scripts/run_oof_probes.py \
  --npz /path/to/your_embeddings.npz \
  --label heavy_5 --seed 0 --method "Frozen embedding" \
  --out /path/to/local_oof_scores.csv
```

Any output is written only to a local user-specified path. The public
repository does not provide the underlying adapted embeddings,
real experiments' splits or individual query predictions. The
unit tests use synthetic examples to check algorithm behavior.
