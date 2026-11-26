# Experimental protocol boundaries

This document describes implementation contracts and distinguishes
different research questions. It intentionally contains **no published
performance numbers or experimental result exports**.

## Frozen radar representation readout

The PatchShot pathway freezes a 3D radar encoder and evaluates lightweight
support-supervised readouts on patch-level embeddings. Support and query cases
are disjoint. Support labels may train a projection head, define prototypes,
and calibrate the decision threshold; query labels are used only in evaluation.

The matched CE control changes the projection training objective while
retaining the support-derived prototype readout. Do not confuse this control
with a direct balanced-CE classification head.

These case-level splits do not by themselves establish time-block- or
storm-level independence. The exact source split and input provenance are
the responsibility of each experimental reproduction.

## Empirical accessibility probes

The standalone probe code evaluates prototype, linear and k-NN readouts
using case-grouped, out-of-fold support threshold selection. This differs
from PatchShot's regular support-only calibration. The evaluated maximum
across a specified probe family is an empirical envelope, not a theoretical
bound. The repository does not ship adapted embeddings or the records
underlying manuscript tables.

## Structural sensitivity

The `evaluation/` utilities operate on a separate 3DMAEPP retrieval
pathway with user-provided checkpoints and radar observations. Their
perturbation modes, score transforms, sample selection and thresholds must
be recorded by the experimenter; results cannot be directly combined with
the frozen-representation readout experiment.

The targeted height-group dropout utility applies a *joint gate* to its
selected group, not independent gates for each height level.

## Heavy/extreme event sensitivity

An additional high-intensity predictor, if evaluated, must retain its own
model checkpoint, event construction, validation-frozen thresholds and
data split. It must not silently inherit the original structural
diagnostic's score threshold.

## Terrain-associated mismatch

Terrain analysis should preserve the fixed prediction decision grid
while allowing finer observational subdivisions for radar, rainfall
reference and DEM diagnostics. That process requires registered
observations and appropriately grouped uncertainty estimates.
No full terrain analysis runner or underlying observations are shipped.

## Publication boundary

The public repository contains implementation and synthetic unit tests,
not original research data, model weights or manuscript result files.
Users can run the methods on data they are authorized to use.
