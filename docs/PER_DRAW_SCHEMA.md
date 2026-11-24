# Real per-draw score export for tools/audit_instability.py

This is a **post-inference** data format, not a raw radar input format. Export it from the appropriate trained predictor under the correct dataset/split/protocol.

Required CSV columns:

- case_id: opaque scene/case identifier
- patch_id: identifier unique within each case
- perturbation: mode name (e.g., gaussian, drop_low)
- draw_id: unique perturbation realization identifier within a case/patch/mode
- event_score: a **real finite scalar** score before binary decision, using the protocol's score definition
- reference_event: 0 or 1 using the *same* patch label definition as the original experiment

Optional column: is_boundary (0 or 1), computed from the experiment's actual reference-label grid.

Each (case_id, patch_id, perturbation) must have the stated number of draws; do not mix predictors, thresholds, label definitions, or splits in one file. Set --prediction-threshold to the protocol's previously calibrated value, not a test-fitted value. The helper reports mean instability U = 4p(1-p), where p is the observed frequency of predicted event across draws, and majority-vote F1. It does not calibrate anything.

No synthetic study results or prefilled data are supplied. F1 computed from this format is patch-event F1, not pixel CSI or case-level CSI. It does not directly reproduce manuscript Table III/IV without checking input generation, per-mode sampled cases, patch layout, and exact aggregation code.
