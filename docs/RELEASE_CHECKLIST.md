# Methods-only release checks

- [x] Retain the base 3DMAE / 3DMAEPP model and training components.
- [x] Retain frozen-feature PatchShot and objective-matched CE readouts.
- [x] Retain support-only calibration and case-grouped OOF probe algorithms.
- [x] Retain structured radar perturbation and post-inference instability code.
- [x] Test core algorithms using small **synthetic** fixtures.
- [x] Exclude original experimental score CSVs, paired-seed summaries and Figure-specific numerical audit files from the current source tree.
- [x] Document input formats, model boundaries and data-access limitations.
- [ ] Full original experiment numerical reproduction requires independently obtained authorized radar/reference data, checkpoints and run manifests; it is not claimed by this release.

**Policy:** Public code illustrates scientific ideas and methods.
Do not commit real radar/precipitation data, model outputs, per-seed
scores, raw frozen features, private paths, access tokens or weights.
Paper tables and figures are the public reference for reported results.
