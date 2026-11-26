# 3D Radar Reliability

**Beyond Average Accuracy: The Reliability Landscape of 3D Radar Precipitation Retrieval**

This repository presents **research methods and implementation examples** for diagnosing reliability in three-dimensional weather-radar precipitation retrieval. It supports a manuscript prepared for *IEEE Transactions on Geoscience and Remote Sensing (TGRS)*.

## Research idea

High aggregate retrieval accuracy does not, by itself, explain whether rare precipitation events are accessible in a learned representation, how predictions respond to changes in radar observations, or why radar and surface rainfall references disagree under different environments.

We study three complementary questions:

1. **Representation accessibility:** can heavy-rain evidence be recovered from frozen radar embeddings by a small, support-supervised readout?
2. **Structural sensitivity:** which temporal, vertical and spatial radar components influence the stability of retrieval decisions?
3. **Terrain-associated mismatch:** how should retrieval decisions be investigated together with radar, surface observations and terrain?

These are complementary *diagnostic perspectives*, not a single joint model or a universally shared evaluation protocol.

## Code organization

| Location | Purpose |
| --- | --- |
| `models/`, `training/`, `data/`, `configs/` | Base 3DMAE/3DMAEPP architectures, data interface and training utilities |
| `patchshot/data.py` | Case-disjoint support/query partitioning and patch-feature input |
| `patchshot/model.py` | Support-supervised contrastive projection adapter |
| `patchshot/matched_ce.py` | Objective-matched cross-entropy control |
| `patchshot/readout.py`, `patchshot/evaluation.py` | Support-derived prototypes, calibration, event metrics |
| `patchshot/oof_probes.py` | Prototype, linear and k-NN probes with case-grouped out-of-fold calibration |
| `evaluation/compare_physical_rs_uncertainty.py` | Radar-oriented perturbation families |
| `evaluation/compare_height_layer_rs_uncertainty.py` | Targeted radar-height perturbation diagnostics |
| `tools/audit_instability.py` | Post-inference event-vote stability calculation |
| `scripts/run_patchshot.py`, `scripts/run_oof_probes.py` | Example entrypoints for running readouts on **user-provided** representations |
| `tests/` | Small **synthetic code checks**, not published experiment observations |

The original randomized-smoothing project overview is retained at [docs/LEGACY_README.md](docs/LEGACY_README.md).

## Installation

```bash
git clone https://github.com/spotpan/3d-radar-reliability.git
cd 3d-radar-reliability
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

## Example: support-supervised representation readout

Prepare your own case-organized frozen embeddings in a local NPZ:

- `z_patch`: floating-point array shaped `[cases, patches, embedding_dim]`
- `heavy_5` and `heavy_10`: binary labels shaped `[cases, patches]`, or a `target_max` array from which they can be derived

```bash
python scripts/run_patchshot.py \
    --npz /path/to/your_patch_features.npz \
    --mode supcon --device cuda \
    --out_dir /path/to/local_results
```

To compare the matched cross-entropy objective:

```bash
python scripts/run_patchshot.py \
    --npz /path/to/your_patch_features.npz \
    --mode matched_ce --method "Matched CE" \
    --device cuda --out_dir /path/to/local_results_ce
```

Input features, targets and model checkpoints are **not distributed here**. The scripts write results only to the location specified by the user. They are method-level examples and have not been independently validated as a full numerical reproduction of every manuscript experiment.

See [PatchShot protocol](docs/PATCHSHOT_PROTOCOL.md) and [Matched CE protocol](docs/MATCHED_CE_PROTOCOL.md).

## Example: empirical accessibility probes

`patchshot/oof_probes.py` implements support-fold threshold calibration for three lightweight probe families. It measures an **empirical**, evaluated readout envelope, not a theoretical information bound.

```bash
python scripts/run_oof_probes.py \
    --npz /path/to/your_embeddings.npz \
    --label heavy_5 --seed 0 --method "Frozen embedding" \
    --out /path/to/local_oof_scores.csv
```

Read [OOF probe methods](docs/OOF_PROBES.md) for the calibration contract and limitations.

## Structural perturbations and stability

The original 3DMAEPP scripts in `evaluation/` implement structured changes to radar observations, including temporal-frame dropout, vertical-level dropout, intensity scaling, noise and local echo masking. Trained checkpoints and source observations must be supplied locally.

The post-inference utility `tools/audit_instability.py` consumes **actual per-draw predictions** created by a user-run model and calculates vote instability; see [per-draw input schema](docs/PER_DRAW_SCHEMA.md).

## Data and result policy

**This is a methods-only public code release.** The repository deliberately does **not** publish experimental result tables, per-seed scores, Figure-specific numerical exports, raw radar or precipitation observations, frozen feature arrays, or trained model weights.

Synthetic values used inside unit tests are solely for checking algorithms. The paper remains the source for reported experimental findings. Neither the code release nor its unit tests should be described as independent end-to-end reproduction of all manuscript results.

See [protocol boundaries](docs/PROTOCOLS.md) and [release checks](docs/RELEASE_CHECKLIST.md).
