#!/usr/bin/env python3
"""Audit archived 20%-support reference rows; never generate model predictions."""
import argparse
import csv
from collections import defaultdict
from pathlib import Path
from statistics import fmean, pstdev

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    (ROOT / "reference_results/patchshot_core_20pct_per_seed.csv", "Method"),
    (ROOT / "reference_results/matched_ce_20pct_per_seed.csv", "Method"),
)
EXPECTED = {
    ("Raw-MAE", "heavy_5"): (0.1602, 0.0051),
    ("Raw-MAE", "heavy_10"): (0.1191, 0.0029),
    ("SupConShot", "heavy_5"): (0.2329, 0.0057),
    ("SupConShot", "heavy_10"): (0.1665, 0.0158),
    ("Matched CE re-access", "heavy_5"): (0.2255, 0.0137),
    ("Matched CE re-access", "heavy_10"): (0.1684, 0.0083),
}
# Comparison numbers are the manuscript's 4-decimal (0..1 CSI) values.
def audit():
    groups = defaultdict(dict)
    for filename, method_column in FILES:
        with filename.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                name = row[method_column]
                label = row["Label"]
                seed = int(row["Seed"])
                case_count = int(row["SupportCases"])
                query_count = int(row["QueryCases"])
                if case_count != 384 or query_count != 961:
                    raise AssertionError(f"{filename}: wrong support/query counts")
                key = (name,label)
                if seed in groups[key]:
                    raise AssertionError(f"{filename}: duplicate seed for {key}")
                score = float(row["CSI"])
                if not 0 <= score <= 1:
                    raise AssertionError(f"{filename}: invalid CSI {score}")
                groups[key][seed] = score
    if set(groups) != set(EXPECTED):
        raise AssertionError(f"methods mismatch: expected {set(EXPECTED)}, got {set(groups)}")
    results = []
    for key in sorted(EXPECTED):
        per_seed = groups[key]
        if set(per_seed) != set(range(5)):
            raise AssertionError(f"missing or unexpected seeds for {key}: {sorted(per_seed)}")
        scores = list(per_seed.values())
        avg, sd = fmean(scores), pstdev(scores)
        mean_ref, sd_ref = EXPECTED[key]
        if abs(avg-mean_ref)>0.00005 or abs(sd-sd_ref)>0.00005:
            raise AssertionError(f"{key}: mean/std ({avg:.6f}, {sd:.6f}) inconsistent with paper rounding")
        results.append((key[0],key[1],avg,sd))
    return results

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    for name,label,avg,sd in audit():
        print(f"{name:23s} {label:9s} CSI={avg*100:.4f}% +/- {sd*100:.4f}% (five archived seeds)")
    print("PASS: archived source-derived rows agree with Table I rounding.")
    print("NOTE: archived-row consistency is not independent model reproduction.")

if __name__=="__main__":
    main()
