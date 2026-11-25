# OOF probe implementation, not Table II numerical reproduction

This repository includes an independent post-embedding implementation
of Stage-116a's **case-grouped out-of-fold** support calibration.

Three readouts are evaluated: Prototype, balanced linear, and k-NN.
Each is trained on support folds; its predictions on held-out support
cases are used to calibrate a CSI-maximizing threshold. The full
support set then trains each query readout; query labels are **not**
used to select thresholds. The envelope is the per-seed maximum of
the three evaluated CSI values and is not an information-theoretic
bound. Ratios and gaps are computed from these evaluated values.

```bash
python scripts/run_oof_probes.py \
  --npz /authorized/embeddings/seed0_matched_ce.npz \
  --label heavy_5 --seed 0 --method "Matched CE" \
  --out /local/oof/matched_ce_h5_seed0.csv
```

**Scientific limitation:** the original Stage-116a code's default
representations are frozen radar plus several environment-conditioned
variants from the aligned 1,918-case benchmark. The current TGRS
Table II instead reports Frozen 3DMAE, radar-only Matched CE and
radar-only PatchShot, but this archive has **no confirmed complete
per-seed OOF probe CSVs and adapted embedding stores** for all six
Table II method/event rows.

The CLI above uses the current 1,922-case Stage-27 split
(seeds 0–4), *not* the historical Stage-116a aligned seed/split
protocol. It cannot be claimed equivalent to the published Table II
without tracing the exact original adapted embeddings and seed maps
and rerunning those probes on verified inputs. A check of basic
algorithm behavior using synthetic test fixtures is not a
scientific replication of Table II.
