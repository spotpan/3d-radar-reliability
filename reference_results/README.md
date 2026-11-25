# Archived source-derived reference results (not independently rerun)

The CSV `patchshot_core_20pct_per_seed.csv` contains **20 real numerical
rows extracted and rounded to eight decimals** from the supplied
`PatchShot_OpenReview_Code(1).zip`:

- `reference_results/unified_raw_mae_per_seed.csv`, filtered to support ratio 0.20
- `reference_results/unified_supconshot_per_seed.csv`, filtered to support ratio 0.20

They contain five paired seed IDs for each H5/H10 threshold and are
**recorded experimental outputs**, not generated synthetic values or claims
that this repository independently reran a checkpoint. Raw-case
features, time identifiers and trained weights are not included.

`Raw-MAE` means frozen 3DMAE identity prototype; `SupConShot` is
the canonical PatchShot readout from the archived Stage-27 protocol.
CSI and AP are on the [0,1] scale, in contrast with percentage-valued
numbers in manuscript Table I. Compute mean and population standard
deviation (ddof=0) across five seeds for Table I consistency.

The archived `BalancedCE` is **not** automatically equivalent to the
manuscript's `Matched CE re-access`: the former is a different baseline
whose published archived H5 CSI mean is about 0.206, not 0.2255.
Do not relabel these rows. PaCo-Proto and full Table II results are
not present in this reference CSV. Additional original source and
per-seed outputs must be traced before declaring full Table I/II
artifact completeness.


## Additional auditable records

- `matched_ce_20pct_per_seed.csv`: ten original A3 objective-matched CE rows for H5/H10, five seeds each.
- `patchshot_20pct_paired_deltas.csv`: matched frozen-vs-PatchShot seed deltas at 20% support.
- `figure4_verified_budget_summary.csv`: 28 source-covered method/event/budget aggregate rows (population SD).
- `figure4_verified_paired_deltas_matrix.csv`: paired seed differences for Frozen/PatchShot across five support budgets.

Run `python scripts/plot_verified_figure4.py --out_dir figure_output` to regenerate the **available-evidence subset** of Figure 4(b–d) as PDF/PNG. It cannot reconstruct absent original QPE head, PaCo-Proto, ERA5, or multi-budget control records. No synthetic experimental results have been added.
