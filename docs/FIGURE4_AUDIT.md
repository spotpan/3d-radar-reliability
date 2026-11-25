# Figure 4(d) data audit: original 20% support protocol

Archived source files from `PatchShot_OpenReview_Code(1).zip`:
- `reference_results/unified_raw_mae_per_seed.csv`
- `reference_results/unified_supconshot_per_seed.csv`

Both are five-seed, radar-only results under the original Stage-27
case-disjoint support/query protocol. For **each matching `(Label,Seed)`**
at support ratio 0.20, this audit computes:

    delta_CSI = CSI(SupConShot) - CSI(Raw-MAE)

The resulting actual archived values are in
`reference_results/patchshot_20pct_paired_deltas.csv`.
No model was rerun to create this subtraction.

H5, seeds 0..4: +0.07035, +0.07928, +0.06357, +0.06769, +0.08273.
H10, seeds 0..4: +0.05348, +0.05961, +0.05286, +0.05907, +0.01175.

**Manuscript risk:** Figure 4(d)'s visual per-seed 20% annotations are
not demonstrably the above paired deltas. The figure uses seed labels
s1..s5 while original archive uses seeds 0..4; a mapping is required
before asserting they should match. Figure 4(b)'s 20% heatmap also
does not simply round several Table I numbers, including the H5
Balanced Linear mean (Table I 0.2235 -> 0.22 versus figure about
0.21). The original QPE head appears as about 0.01 in the figure
against 0.00% CSI in Table I.

Do NOT manually overwrite Figure 4 annotations to make them
look consistent. Locate the actual per-seed plotting inputs and
query/split/calibration protocol for every method and budget.
If data sources are different, caption and methods must clearly
state the differences. Otherwise redraw with the audited files
and use the exact source seed IDs.

The public repository does **not** yet contain complete
five-seed × five-budget records for every Figure 4(b) method.
The current audit verifies only the 20% radar-only frozen
prototype / PatchShot paired deltas. It cannot generate the
entire Figure 4(b--d) without further evidence.
