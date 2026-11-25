# Before claiming complete TGRS reproduction

- [ ] Verify available 3DMAEPP model-loading path, restricted data preprocessing, checkpoint source SHA, and all Table III perturbation results against the actual frozen validation split.
- [ ] Verify targeted group-drop implementation (single shared Bernoulli gate), sample count (16), 50 validation cases, and original Table III score-standard-deviation convention.
- [x] Publish Stage-27 PatchShot core and the archived paired-seed frozen/PatchShot reference measurements.
- [x] Publish source-derived objective-matched CE projection and its archived five-seed Table I reference measurements.
- [ ] Independently reproduce all Table I methods on original authorized frozen features; publish exact split manifests and query predictions if rights permit.
- [ ] Publish audited Table II case-grouped OOF probe implementation and per-seed source outputs; a historical script has been identified but not verified as a standalone runner.
- [ ] Reconcile original-head CSI between Figure 4(b) and Table I from real exports, not by modifying visual labels by hand.
- [ ] Publish validated frozen M3_natural H5/H10 perturbation code and the definition that produces 7,920 patches from 48 radar scenes.
- [ ] Publish the terrain conditional mismatch pipeline with proper 6x8 parent decisions, DEM alignment, controls and day-cluster bootstrap.
- [ ] Audit temporal input-window overlap across support and query; do not claim storm or cross-year independence unless established.
- [ ] Supply per-table configuration, seed, environment, run command, exact source data description, expected artifact shape and evaluation output.
- [ ] Verify upstream dependencies and redistribution rights; publish no restricted radar/station data, checkpoints, access tokens or private paths.
- [ ] Run a fresh-clone test with authorized materials and compare actual results to the paper, including all reported std/CI conventions.
- [ ] Update manuscript Appendix D to state exactly which parts are public and reproducible at publication time.

Until complete, describe this repository as a **partial code release** for the existing 3DMAEPP/structural diagnostic work plus auditable documentation, not as a complete reproduction of Tables I–IV or Figures 1–6.
