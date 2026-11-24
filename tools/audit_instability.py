#!/usr/bin/env python3
"""Audit patch-event vote statistics from actual per-draw score exports.

Post-inference only. Does not run a model, create synthetic results, calibrate
thresholds, or establish reproduction of any manuscript table.
"""
import argparse
import csv
from collections import defaultdict
from math import isfinite
from pathlib import Path


REQUIRED = {"case_id", "patch_id", "perturbation", "draw_id",
            "event_score", "reference_event"}


def summarize(rows, threshold, expected_draws=16, vote_threshold=0.5):
    if not isfinite(threshold) or not (0 <= vote_threshold <= 1):
        raise ValueError("threshold must be finite and vote threshold in [0,1]")
    if expected_draws < 1:
        raise ValueError("expected_draws must be positive")
    scores = defaultdict(dict)
    labels = {}
    boundaries = {}
    by_patch_label = {}
    for i, row in enumerate(rows, 2):
        missing = REQUIRED - set(row)
        if missing:
            raise ValueError(f"row {i}: missing {sorted(missing)}")
        key = (row["case_id"], row["patch_id"], row["perturbation"])
        draw_id = row["draw_id"]
        if not all(key) or not draw_id:
            raise ValueError(f"row {i}: blank identifiers")
        if row["reference_event"] not in ("0", "1"):
            raise ValueError(f"row {i}: reference_event must be 0/1")
        label = int(row["reference_event"])
        pk = key[:2]
        if pk in by_patch_label and by_patch_label[pk] != label:
            raise ValueError(f"row {i}: inconsistent reference label for {pk}")
        by_patch_label[pk] = label
        labels[key] = label
        if draw_id in scores[key]:
            raise ValueError(f"row {i}: duplicate draw ID in {key}")
        try:
            value = float(row["event_score"])
        except (ValueError, TypeError) as exc:
            raise ValueError(f"row {i}: invalid score") from exc
        if not isfinite(value):
            raise ValueError(f"row {i}: nonfinite score")
        scores[key][draw_id] = value
        boundary = row.get("is_boundary", "")
        if boundary not in ("", None):
            if boundary not in ("0", "1"):
                raise ValueError(f"row {i}: is_boundary must be 0/1")
            if key in boundaries and boundaries[key] != int(boundary):
                raise ValueError(f"row {i}: inconsistent boundary flag")
            boundaries[key] = int(boundary)
    if not scores:
        raise ValueError("no input rows")
    by_mode = defaultdict(list)
    for key, draws in sorted(scores.items()):
        if len(draws) != expected_draws:
            raise ValueError(f"{key}: got {len(draws)} draws, expected {expected_draws}")
        p = sum(v >= threshold for v in draws.values()) / len(draws)
        by_mode[key[2]].append((labels[key], int(p >= vote_threshold),
                                4.0*p*(1.0-p), boundaries.get(key)))
    result = []
    for mode, patches in sorted(by_mode.items()):
        tp = sum(t == 1 and p == 1 for t, p, _, _ in patches)
        fp = sum(t == 0 and p == 1 for t, p, _, _ in patches)
        fn = sum(t == 1 and p == 0 for t, p, _, _ in patches)
        boundary_vals = [u for _, _, u, flag in patches if flag == 1]
        result.append({
            "perturbation": mode, "n_patches": len(patches),
            "tp": tp, "fp": fp, "fn": fn,
            "precision": tp / (tp+fp) if tp+fp else 0.0,
            "recall": tp / (tp+fn) if tp+fn else 0.0,
            "f1": 2*tp / (2*tp+fp+fn) if 2*tp+fp+fn else 0.0,
            "mean_u": sum(x[2] for x in patches) / len(patches),
            "boundary_u": sum(boundary_vals)/len(boundary_vals)
                          if boundary_vals else "",
        })
    return result


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--prediction-threshold", type=float, required=True)
    p.add_argument("--vote-threshold", type=float, default=0.5)
    p.add_argument("--expected-draws", type=int, default=16)
    args = p.parse_args(argv)
    with args.input.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    summary = summarize(rows, args.prediction_threshold,
                        args.expected_draws, args.vote_threshold)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    print(f"Wrote observed patch-event diagnostics for {len(summary)} modes.")
    print("This is an input-dependent audit, not independent table reproduction.")


if __name__ == "__main__":
    main()
