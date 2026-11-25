#!/usr/bin/env python3
"""Case-disjoint PatchShot benchmark from frozen patch-feature arrays.

Faithful entrypoint for the radar-only support/query readout protocol. The
restricted feature arrays are not distributed. This script is NOT an end-to-end
3DMAE checkpoint inference pipeline and does not run Matched CE or PaCo.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from patchshot.data import load_patch_data, build_fixed_query_and_support_pool, nested_support_cases
from patchshot.evaluation import EvaluationConfig, evaluate_one_split

METRICS = ("CSI", "F1", "Precision", "Recall", "FAR", "ACC", "AP",
           "AUROC", "SepRatio", "Threshold")

def summarize(frame):
    records = []
    for (label, ratio), block in frame.groupby(["Label", "SupportRatio"], sort=False):
        row = {
            "Method": block["Method"].iloc[0], "Label": label,
            "SupportRatio": ratio, "Seeds": len(block),
            "SupportCases": int(round(block["SupportCases"].mean())),
            "QueryCases": int(round(block["QueryCases"].mean())),
        }
        for metric in METRICS:
            values = block[metric].astype(float).to_numpy()
            row[metric + "_mean"] = float(np.nanmean(values))
            row[metric + "_std"] = float(np.nanstd(values, ddof=0))
        records.append(row)
    return pd.DataFrame(records)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--npz", required=True, type=Path)
    p.add_argument("--out_dir", required=True, type=Path)
    p.add_argument("--feature_key", default="z_patch")
    p.add_argument("--mode", choices=["frozen","pca","supcon"], default="supcon")
    p.add_argument("--labels", default="heavy_5,heavy_10")
    p.add_argument("--ratios", default="0.01,0.05,0.10,0.20,0.50")
    p.add_argument("--seeds", type=int, default=5)
    p.add_argument("--query_ratio", type=float, default=0.50)
    p.add_argument("--epochs", type=int, default=20)
    p.add_argument("--steps_per_epoch", type=int, default=60)
    p.add_argument("--batch_size", type=int, default=512)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--temperature", type=float, default=0.1)
    p.add_argument("--threshold_steps", type=int, default=500)
    p.add_argument("--pca_dim", type=int, default=128)
    p.add_argument("--pca_whiten", action="store_true")
    p.add_argument("--device", default="cuda")
    p.add_argument("--method", default="PatchShot")
    args = p.parse_args()
    labels = [x.strip() for x in args.labels.split(",") if x.strip()]
    ratios = [float(x.strip()) for x in args.ratios.split(",") if x.strip()]
    z_case, label_map = load_patch_data(args.npz, feature_key=args.feature_key, labels=labels)
    config = EvaluationConfig(
        mode=args.mode, pca_dim=args.pca_dim, pca_whiten=args.pca_whiten,
        epochs=args.epochs, steps_per_epoch=args.steps_per_epoch,
        batch_size=args.batch_size, learning_rate=args.lr,
        temperature=args.temperature, threshold_steps=args.threshold_steps,
        device=args.device,
    )
    rows = []
    for label in labels:
        for seed in range(args.seeds):
            query, pool = build_fixed_query_and_support_pool(
                num_cases=len(z_case), seed=seed, query_ratio=args.query_ratio)
            for ratio in ratios:
                support = nested_support_cases(pool, len(z_case), ratio)
                result = evaluate_one_split(z_case, label_map[label], query, support, seed, config)
                result.update(Method=args.method, Mode=args.mode, Label=label,
                              SupportRatio=ratio, Seed=seed, FeatureKey=args.feature_key)
                rows.append(result)
                print(f"{label} seed={seed} support={ratio:.2f} CSI={result['CSI']:.4f}")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(args.out_dir / "patchshot_per_seed.csv", index=False)
    summarize(df).to_csv(args.out_dir / "patchshot_summary.csv", index=False)
    print(f"Saved actual experiment results to {args.out_dir}")

if __name__ == "__main__":
    main()
