# 3D Radar Reliability

**Beyond Average Accuracy: The Reliability Landscape of 3D Radar Precipitation Retrieval**  
Research artifacts and code for a manuscript prepared for *IEEE Transactions on Geoscience and Remote Sensing (TGRS)*.

This repository studies reliability **beyond aggregate quantitative precipitation estimation (QPE) accuracy** from complementary perspectives:

1. **Representation accessibility:** can heavy- and extreme-rain evidence be recovered from frozen 3D radar representations using limited labels?
2. **Structural sensitivity:** how stable are event decisions when radar intensity, vertical levels, temporal frames, or local echoes are perturbed?
3. **Terrain-associated radar–rainfall mismatch:** how does observational disagreement accompanying prediction errors vary across topography?

These are **separate experiments**, not three measurements from one common trained model. Their backbones, splits, event definitions, and analysis units must not be conflated.

> **Release status (November 2026): partial research code.** The publicly available repository currently includes the 3DMAEPP base-model code, original structural-perturbation scripts, and lightweight diagnostic audit utilities. It does **not yet** provide fully validated, end-to-end reproduction of every reported table and figure. The **radar-only PatchShot core** (frozen-feature loading, case-disjoint support/query splits, support-supervised projection, prototype calibration and a runnable CLI) has been integrated from the archived clean release. The original objective-matched CE readout and a post-embedding OOF probe utility have also been added. PaCo-Proto, complete Table II numerical reproduction, M3_natural, and terrain analysis remain incomplete. No missing implementation or data is represented as publicly available.

## Paper-to-code map

| Evidence in manuscript | Evaluation setting | Public repository status |
| --- | --- | --- |
| **Tables I–II, Figure 4** | Frozen 3DMAE readouts (PatchShot, prototypes, matched supervised controls, empirical envelope) | **Available:** PatchShot and Matched CE readout CLIs, 20%-support archived Table I reference rows, Figure 4 radar-only budget summaries, and case-grouped OOF probe code. **Not verified:** PaCo, complete Table II outputs, exact restricted feature inputs, full-budget methods other than Frozen/PatchShot, fresh full-scale reproduction |
| **Table III; original analyses in Figure 2** | Frozen 3DMAEPP with lower-threshold QPE-derived patch-event decisions | **Code available:** existing perturbation evaluation scripts; full numeric reproduction still needs authorized data, checkpoint and audit |
| **Table IV; H5/H10 analyses in Figure 2** | Separate frozen M3_natural experiment and 2023 event split | **Pending integration:** dedicated high-intensity evaluation protocol, model outputs and test-split manifests |
| **Figures 3, 5–6** | Unperturbed PatchShot decisions with aligned radar, precipitation reference and DEM | **Pending integration:** full spatial/terrain mismatch and calendar-day bootstrap pipeline |

**Notation:** H5 and H10 mean rainfall-event thresholds of 5 and 10 mm/h; L0–L5 are radar vertical-level indices. Original Table III and separate Table IV sensitivity rankings are *not* directly comparable across their different protocols.

## Repository layout

```text
3d-radar-reliability/
├── configs/                       # Original model and dataset configurations
├── data/                          # Data loaders (restricted data are not included)
├── models/                        # 3DMAE encoder and QPE components
├── training/                      # Base-model training components
├── evaluation/                    # Existing QPE and structural diagnostics
├── patchshot/                     # Frozen-feature PatchShot and matched CE readouts
├── scripts/                       # PatchShot, OOF and plot CLIs; training utilities
├── reference_results/             # Source-traced archived CSI summaries and seed deltas
├── tools/audit_instability.py     # Post-inference vote/instability consistency audit
├── tests/                         # Unit tests for audit utilities
├── docs/                          # Protocol boundaries and release checklist
├── requirements.txt
└── README.md
```

See [docs/PATCHSHOT_PROTOCOL.md](docs/PATCHSHOT_PROTOCOL.md) for Stage-27, [docs/MATCHED_CE_PROTOCOL.md](docs/MATCHED_CE_PROTOCOL.md) for matched CE, and [docs/OOF_PROBES.md](docs/OOF_PROBES.md) for the separately calibrated probe workflow.

The earlier project description is preserved in [docs/LEGACY_README.md](docs/LEGACY_README.md). Older generic QPE evaluation examples are documented separately in [evaluation/README.md](evaluation/README.md); they must not be treated as the current TGRS Tables I–II.

## Getting started

```bash
git clone https://github.com/spotpan/3d-radar-reliability.git
cd 3d-radar-reliability
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

### Radar-only PatchShot core (Table I pathway)

```bash
python scripts/run_patchshot.py \
  --npz /authorized/path/to/val_event_patch_features_raw_mae.npz \
  --out_dir /local/patchshot_output \
  --labels heavy_5,heavy_10 --ratios 0.20 --seeds 5 --device cuda
```

When you supply authorized frozen-feature arrays, the CLI computes new query CSI/AP results. The arrays and original radar model checkpoints are restricted and are not included. This CLI implements the original case-disjoint, support-only calibration protocol, **not** the separate OOF probe-envelope experiment of Table II. The original Table I numerical values must be verified by comparing real exported rows from the correct frozen features; the synthetic unit tests do not establish those results. Matched CE uses the same CLI with `--mode matched_ce --method 'Matched CE re-access'`; the separate PaCo method is not implemented.

### Objective-matched cross-entropy control (Table I)

```bash
python scripts/run_patchshot.py \
  --npz /authorized/path/to/val_event_patch_features_raw_mae.npz \
  --mode matched_ce --method "Matched CE re-access" \
  --ratios 0.20 --seeds 5 --device cuda \
  --out_dir /local/matched_ce_output
```

Matched CE uses the same support cases, architecture and optimizer steps as the SupCon projector, but optimizes a temporary CE classifier and **discards that classifier** before the prototype readout. Refer to [docs/MATCHED_CE_PROTOCOL.md](docs/MATCHED_CE_PROTOCOL.md). Reference results are archived from the real original experiments; full data-free numerical reproduction is not claimed.

### Evidence-covered Figure 4 panels (archived data; no new model inference)

Use the committed aggregate and five-seed paired-difference CSVs to produce three radar-only panels:

```bash
python scripts/plot_verified_figure4.py --out_dir figure_output
python tools/audit_table_i_reference.py
python tools/audit_figure4_paired_deltas.py
```

The plots intentionally contain only source-verified evidence: Frozen prototype/PatchShot across 1%, 5%, 10%, 20%, and 50% support; additional ProtoNet, SimpleShot, Balanced Linear and Matched CE at **20% only**. Other original QPE, PaCo and ERA5 budget cells are not reconstructed or imputed. The underlying Stage-27 dataset has **1,922 cases, 961 query cases, and 961 support cases at 50%**. The 959-case support figure belongs to a separate 1,918-case aligned pool. See [docs/FIGURE4_FULL_BUDGET_AUDIT.md](docs/FIGURE4_FULL_BUDGET_AUDIT.md).

### OOF probing (algorithm only; Table II numbers not independently reproduced)

```bash
python scripts/run_oof_probes.py --npz /authorized/embeddings/seed0.npz \
  --label heavy_5 --seed 0 --method "Frozen 3DMAE" \
  --out /local/oof/frozen_h5_seed0.csv
```

This probes an already computed embedding array using case-grouped out-of-fold calibration; it does **not** recover unpublished adapted embeddings or independently reproduce Table II.

### Original structural-sensitivity scripts (Table III pathway)

The following commands are **illustrative invocations** that require a compatible trained 3DMAEPP checkpoint, the original validation data, and valid local loader configuration. Running them on an arbitrary checkpoint or split does not reproduce Table III.

```bash
python evaluation/compare_physical_rs_uncertainty.py \
  --checkpoint /authorized/path/to/3dmaepp.pt \
  --num-samples 16 --max-batches 50 --batch-size 1 --seed 2026 \
  --out-csv /local/results/table_iii_families.csv

python evaluation/compare_height_layer_rs_uncertainty.py \
  --checkpoint /authorized/path/to/3dmaepp.pt \
  --num-samples 16 --max-batches 50 --batch-size 1 --drop-prob 0.5 --seed 2026 \
  --out-csv /local/results/table_iii_height_levels.csv
```

The height-layer utility's original **defaults** are eight draws and twenty batches, so the 16/50 flags are intentional. The present targeted-group implementation applies a **shared Bernoulli dropout gate** to the entire selected layer group in each draw; it does not sample each level independently. The original family-dropout probability is 0.15, distinct from targeted-group dropout at 0.5. Check all details against [docs/PROTOCOLS.md](docs/PROTOCOLS.md) before attempting manuscript-level comparisons.

### Auditing real per-draw exports

```bash
python tools/audit_instability.py \
  --input /local/results/per_draw_scores.csv \
  --output /local/results/audited_vote_statistics.csv \
  --prediction-threshold 0.0005 --expected-draws 16
```

This utility computes patch-level F1 and mean decision instability `U = 4p(1-p)` from **actual model-produced draw scores**. The example 0.0005 threshold refers only to the original low-threshold Table III pathway. It does not apply to Table IV's independently calibrated H5/H10 protocol. The helper does not generate radar predictions or independently reproduce manuscript data; see [input schema](docs/PER_DRAW_SCHEMA.md).

## Reproducibility and access

- [Protocol-by-protocol evidence and limitations](docs/PROTOCOLS.md)
- [Source-backed Figure 4 reconstruction and scope](docs/FIGURE4_FULL_BUDGET_AUDIT.md)
- [Table I and Matched CE source provenance](docs/MATCHED_CE_PROTOCOL.md)
- [Post-embedding OOF probe methods (not Table II replication)](docs/OOF_PROBES.md)
- [Per-draw CSV requirements](docs/PER_DRAW_SCHEMA.md)
- [Checklist before claiming complete reproduction](docs/RELEASE_CHECKLIST.md)
- [Historical baseline repository description](docs/LEGACY_README.md)

Radar and station-derived precipitation measurements, certain trained checkpoints and other restricted artifacts are not redistributed. Access requires authorization from their data owners. Manuscript results need verified experiment manifests, model versions, splits, calibration, input provenance and output comparisons; the presence of source code alone does not establish numerical reproduction.

## Citation

If referencing this work, cite the manuscript **“Beyond Average Accuracy: The Reliability Landscape of 3D Radar Precipitation Retrieval”** by Yu Bu, Xinchuang Hu, and Baoquan Zhang. Do not use a fabricated publication year, DOI or finalized journal citation before publication.
