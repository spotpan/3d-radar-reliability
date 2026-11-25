# Reviewer-facing verification status: TGRS manuscript, 2026-11-25

This audit tracks claims and evidence, without changing the manuscript's
metrics or manufacturing additional experimental results.

## Verified source correspondence
- Original Stage-27 per-seed SupConShot CSI at 20% support: H5 0.232928,
  H10 0.166453, as reported in Table I.
- Original Stage-121e attribution source includes **A3 Matched CE re-access**
  with CSI H5 0.225542, H10 0.168372, over five paired seeds.
- The archived **A1 Balanced CE head** gives H5 0.206058,
  H10 0.152014 and must never be renamed Matched CE.
- Existing structural sensitivity scripts map to the original Table III
  experiment; a distinct M3_natural runner is required for Table IV.

## Open numerical and provenance questions

1. **Figure 4(b) vs Table I:** at the 20% support budget, the heatmap
   (two-decimal scale) shows about 0.21 H5 for Balanced Linear whereas
   Table I's five-seed mean is 0.2235 (which rounds to 0.22).
   PaCo H5 and other readouts are similarly not straightforward rounded
   versions of Table I. Regenerate from the correct *per-seed* source files,
   matched query cases and calibration. Do not relabel the heatmap by hand.
2. **Original QPE head:** Figure 4(b) about 0.01 at H5 versus Table I
   0.00% needs original per-seed scores, unit and threshold verification.
3. **Figure 4(a):** label frozen feature extractor explicitly as frozen
   3DMAE encoder; do not imply complete 3DMAEPP forward model was used
   as a PatchShot readout.
4. **Table II:** original OOF probe code is identified, but a runnable,
   self-contained complete release of the actual five-seed OOF artifacts
   is not yet verified. Table I support-only thresholding does not
   reproduce Table II OOF calibration.
5. **Case-disjoint vs event-disjoint:** six history frames sampled at 12
   minute intervals could overlap; case disjoint split alone cannot
   establish independent storms, calendar days or cross-year testing.
6. **Table IV:** document the exact source and evaluation mapping from
   48 scenes to 7,920 event patches and use frozen H5/H10 thresholds,
   not the low-threshold Table III score cutoff.
7. **Terrain:** preserve the fixed 6x8 PatchShot prediction grid; finer
   12x16, 24x32, 48x64 subdivisions are *observation diagnostics*.
8. **Figure 1:** ERA5 / AGRI / DEM visual sources must not be interpreted
   as a quantitatively evaluated single fused input when separate
   experiment protocols are used.
9. **Appendix D:** reference the new repository slug
   `spotpan/3d-radar-reliability`; distinguish public partial code
   coverage from full numerical reproduction.

## Publication discipline

- Publish code/traceable results only with rights to redistribute.
- Maintain exact event CSI definitions and separate patch/case/pixel units.
- Distinguish code-source discovery, smoke testing, archived numerical
  correspondence and independent fresh-run reproduction.
- Use archived result CSVs only as references, not as source model outputs.
