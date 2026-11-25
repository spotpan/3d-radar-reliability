# Verified Figure 4 radar-only budget data

Sources inside user-supplied `PatchShot_OpenReview_Code(1).zip`:

- `reference_results/unified_raw_mae_per_seed.csv` (50 rows, Frozen prototype, five budgets)
- `reference_results/unified_supconshot_per_seed.csv` (50 rows, PatchShot, five budgets)
- `reference_results/table1plus_inductive_per_seed.csv` (30 selected rows, ProtoNet, SimpleShot, Balanced Linear, **20% only**)
- `reference_results/component_attribution/final_component_per_seed.csv` (10 A3 Matched CE rows, **20% only**)

These two CSVs contain **source-calculated** means, five-seed population standard deviations (ddof=0), and 50 source-derived paired differences in seed0…seed4 columns. No inferred budgets or surrogate experiment outputs have been added. The original per-seed raw data and regeneration code are provided separately in the downloadable Figure4 source-audit bundle. This public repository contains exact reported statistics, not original restricted patch-feature arrays.

## Strong scientific protocol boundary

The Stage-27 radar-only protocol has **1,922 cases**, **961 query cases per seed**, and support budgets **19, 96, 192, 384, 961**. The legacy Stage-112a support replay is a different **1,918-case ERA5-aligned pool**, **959 query cases**, seeds **1–5**, and 50% support **959**. The original PDF currently states 50% = 959 alongside the radar-only 1,922-case protocol; it should be 961 if the Stage-27 protocol is claimed. Do not combine Stage-112a aligned results and Stage-27 radar-only results in one matched-baseline heatmap.

## Main Figure 4 risks

The existing heatmap (b) is not a direct display of archived radar-only five-budget means. Example: 1% H5 PatchShot from Stage-27 is **0.12475**, not ~0.10; 10% H5 is **0.20574**, not ~0.22. Figure (d) should use the source-derived paired deltas, not the other protocol's s1–s5 marks.

From the source data the seed-level paired improvements have H5 wins of **1/5, 4/5, 5/5, 5/5, 5/5**, and H10 wins of **0/5, 4/5, 5/5, 5/5, 5/5** across budgets 1%, 5%, 10%, 20%, 50%. This agrees with the direction and counts of the manuscript's Finding 4.

Coverage: Frozen and PatchShot all five budgets; ProtoNet, SimpleShot, Balanced Linear and Matched CE at 20% only. There are no validated PaCo-Proto, original QPE head, ERA5-aligned cross-budget records in these files. Do not fill missing cells from intuition or manuscript numbers.

Note the paper's Table II is a separate OOF-probe analysis and cannot be deduced from these Table I support-calibration records.
