#!/usr/bin/env python3
"""Run Stage-116a style case-grouped OOF probes on authorized embeddings.

Not a full reproduction of manuscript Table II: input embeddings for
radar-only matched CE/PatchShot must be independently supplied per seed.
"""
from pathlib import Path
import argparse, csv, sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from patchshot.data import load_patch_data, build_fixed_query_and_support_pool, nested_support_cases
from patchshot.oof_probes import evaluate_accessibility

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--npz", type=Path, required=True)
    p.add_argument("--feature-key", default="z_patch")
    p.add_argument("--label", choices=["heavy_5","heavy_10"], required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--support-ratio", type=float, default=.20)
    p.add_argument("--method", required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    x, label_map = load_patch_data(args.npz, feature_key=args.feature_key,
                                    labels=[args.label])
    query, pool = build_fixed_query_and_support_pool(len(x), args.seed)
    support = nested_support_cases(pool, len(x), args.support_ratio)
    rows, summary = evaluate_accessibility(
        x[support], label_map[args.label][support],
        x[query], label_map[args.label][query], seed=args.seed, folds=5)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as handle:
        fields = ["Representation","Label","Seed","SupportCases","QueryCases",
                  "Probe","CSI","Threshold","SupportOOFCSI","OOFFolds"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({"Representation":args.method,"Label":args.label,
                             "Seed":args.seed,"SupportCases":len(support),
                             "QueryCases":len(query),**row})
    print(summary)
    print("Input-dependent OOF probe results only; not independent Table II reproduction.")

if __name__=="__main__":
    main()
