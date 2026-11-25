#!/usr/bin/env python3
"""Verify paired 20% PatchShot minus frozen-prototype CSI from archived observations.

This is an ARITHMETIC consistency check of pre-existing per-seed scores, not
model inference. The archived seed IDs are 0..4. A figure with s1..s5
must document whether those display names map to these seed IDs.
"""
import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def check(source=None, target=None, tolerance=1e-7):
    source = Path(source) if source else ROOT / "reference_results/patchshot_core_20pct_per_seed.csv"
    target = Path(target) if target else ROOT / "reference_results/patchshot_20pct_paired_deltas.csv"
    values = {}
    with source.open(newline="",encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if abs(float(row["SupportRatio"]) - 0.20) > 1e-9:
                continue
            key = (row["Label"],int(row["Seed"]))
            method = row["Method"]
            values.setdefault(key, {})
            if method in values[key]:
                raise ValueError(f"Duplicate {key} {method}")
            values[key][method] = float(row["CSI"])
    if len(values)!=10:
        raise ValueError("Expected 10 paired event/seed combinations")
    with target.open(newline="",encoding="utf-8") as handle:
        rows=list(csv.DictReader(handle))
    if len(rows)!=10:
        raise ValueError("Expected 10 archived paired-delta rows")
    seen=set()
    for row in rows:
        key=(row["Label"],int(row["Seed"]))
        if key in seen or key not in values:
            raise ValueError(f"Missing/duplicate key {key}")
        seen.add(key)
        expected=values[key]["SupConShot"]-values[key]["Raw-MAE"]
        provided=float(row["DeltaCSI"])
        if abs(expected-provided)>tolerance:
            raise AssertionError(f"Wrong paired delta {key}: {provided} vs {expected}")
    return {key: vals["SupConShot"]-vals["Raw-MAE"] for key,vals in values.items()}

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",type=Path)
    parser.add_argument("--target",type=Path)
    args=parser.parse_args()
    results=check(args.source,args.target)
    for (event,seed),value in sorted(results.items()):
        print(f"{event:9s} seed={seed}: PatchShot - frozen = {value:.8f}")
    print("PASS: archival arithmetic only; not a model rerun.")
