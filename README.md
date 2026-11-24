# Beyond Average Accuracy: The Reliability Landscape of 3D Radar Precipitation Retrieval

Research code and reproducibility notes for the TGRS manuscript. This repository originally hosted the 3DMAEPP / randomized-smoothing project. Its earlier overview is preserved in [docs/LEGACY_README.md](docs/LEGACY_README.md).

**Release scope (24 November 2026): partial code and audit utilities, NOT a complete reproduction of every manuscript table or figure.** No manuscript result should be considered independently reproduced by this repository without the corresponding checkpoint, restricted data, exact split, and a verified run log.

## Three distinct experimental protocols

| Manuscript evidence | Experiment | Present public coverage |
| --- | --- | --- |
| Tables I–II; Figure 4 | Frozen 3DMAE rare-event readouts, support/query evaluation, empirical probe envelope | Not yet a verified runnable PatchShot/CE/PaCo reproduction |
| Table III; Figure 2 original columns | Original frozen 3DMAEPP, low-threshold event decisions, structured perturbations | Existing perturbation scripts; checkpoint and restricted data required, numerical match not yet verified |
| Table IV; Figure 2 H5/H10 | Separate frozen M3_natural predictor, 2023 event split | Full event-specific implementation, split and exports not yet published here |
| Figures 3, 5, 6 | Unperturbed PatchShot decisions, radar / precipitation / DEM conditional mismatch | Full terrain analysis and input provenance not yet published here |

The experiments differ in predictor, event definition, data split, and evaluation unit. Do not merge their numbers into one leaderboard or infer that layer rankings transfer between protocols. H5/H10 are rainfall thresholds (5/10 mm/h); L0–L5 are radar height levels.

## Existing implementation

- models/, training/, configs/, data/: baseline 3DMAEPP architecture, training and data-loading components.
- evaluation/compare_physical_rs_uncertainty.py: six structured perturbation families underlying the original low-threshold diagnosis.
- evaluation/compare_height_layer_rs_uncertainty.py: targeted group and single-level perturbation evaluation.
- evaluation/evaluate.py and run_evaluation.py: earlier generic QPE evaluation facilities. The latter contains explicit NotImplementedError placeholders: **it is not an entrypoint for Tables I–II of this manuscript**.

With *authorized* local data and a compatible trained checkpoint, the original structural scripts can be invoked as follows (example paths, not turnkey reproductions):

    python evaluation/compare_physical_rs_uncertainty.py --checkpoint /local/3dmaepp.pt --num-samples 16 --max-batches 50 --seed 2026 --out-csv /local/table_iii_families.csv
    python evaluation/compare_height_layer_rs_uncertainty.py --checkpoint /local/3dmaepp.pt --num-samples 16 --max-batches 50 --drop-prob 0.5 --seed 2026 --out-csv /local/table_iii_layers.csv

Important: the targeted-height script previously defaulted to **8** perturbation draws and **20** batches, so the manuscript's 16/50 settings must be specified explicitly. In that script, the selected layer *group is gated jointly* by a single random dropout decision per realization (not independently per layer). A validated checkpoint/loader, exact split, and output comparison are still required before claiming Table III reproduction.

## Independent metrics audit (no model inference)

The new helper computes observed event-vote F1 and instability from actual per-draw event-score exports:

    python tools/audit_instability.py --input /local/per_draw_scores.csv --prediction-threshold 0.0005 --expected-draws 16 --output /local/instability_summary.csv
    python -m unittest discover -s tests -v

The example threshold 0.0005 applies to the *original Table III QPE-score* protocol only. The separate Table IV H5/H10 experiment must use its own frozen thresholds and event-score definition. This helper never invents experimental predictions or regenerates manuscript tables.

See [docs/PROTOCOLS.md](docs/PROTOCOLS.md), [docs/PER_DRAW_SCHEMA.md](docs/PER_DRAW_SCHEMA.md), and [docs/RELEASE_CHECKLIST.md](docs/RELEASE_CHECKLIST.md).

## Data and code availability

Radar and station-derived precipitation observations, some checkpoints, and restricted derived artifacts are not redistributed. Access to inputs requires authorization from their data owners. The absence of these materials prevents turnkey numerical reproduction. The repository does not yet contain complete end-to-end reproduction paths for all three manuscript branches.
