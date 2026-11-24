# Evaluation utilities — existing QPE baseline and structural diagnostics

This directory belongs to **[3D Radar Reliability](../README.md)**, the code repository for the manuscript *Beyond Average Accuracy: The Reliability Landscape of 3D Radar Precipitation Retrieval*.

## What is actually present

- `compare_physical_rs_uncertainty.py`: original 3DMAEPP perturbation families, e.g. noise, level dropout, temporal-frame dropout, scaling and block masks.
- `compare_height_layer_rs_uncertainty.py`: targeted vertical-group/single-layer perturbations.
- `evaluate.py`, `evaluate_reg_event_patch.py` and related scripts: earlier general QPE evaluation utilities. Their loss/metric conventions may differ from manuscript-specific readout and event experiments.
- The top-level `run_evaluation.py` is a **template**, with user-provided model loading, data loading and comparison-model placeholders. It is not a validated Table I or Table II reproduction.

The full historical evaluation tutorial, including example-only numbers and placeholder citation, is preserved at **[docs/LEGACY_EVALUATION_README.md](../docs/LEGACY_EVALUATION_README.md)**. Those example numbers are *not* results from the current TGRS manuscript.

## Appropriate use and boundaries

The original structure-focused scripts can be applied to the baseline frozen model with authorized observations/checkpoints. They do not implement PatchShot few-shot readout training, the complete empirical envelope of Table II, M3_natural H5/H10 Table IV, or the DEM terrain analysis. Use the protocol and CLI instructions in the [main README](../README.md) and [protocol document](../docs/PROTOCOLS.md) before running experiments. Results from different evaluation units (patch versus case versus pixel) or distinct models must not be directly compared without their explicit shared protocol.

**No original evaluation source files have been modified by this README update.**
