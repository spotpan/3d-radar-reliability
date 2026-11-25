#!/usr/bin/env python3
"""Plot the *verified source-covered* radar-only Figure 4 alternatives.

Inputs: archived five-seed aggregate CSI and paired-delta matrices from
reference_results/. This script cannot reproduce missing PaCo, original QPE
head, or ERA5 rows. It does not recompute model predictions.
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
import numpy as np

BUDGETS = (0.01, 0.05, 0.10, 0.20, 0.50)
LABELS = ("heavy_5", "heavy_10")
FULL = ("Frozen prototype", "PatchShot")
AT20 = ("Frozen prototype", "ProtoNet", "SimpleShot",
        "Balanced Linear", "Matched CE", "PatchShot")
ROOT = Path(__file__).resolve().parents[1]


def load_verified(summary_file: Path, deltas_file: Path):
    with summary_file.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 28:
        raise ValueError(f"Expected 28 source-covered aggregate rows, got {len(rows)}")
    stats = {}
    for row in rows:
        key = (row["Label"], row["Method"], float(row["SupportRatio"]))
        if key in stats:
            raise ValueError(f"Duplicate aggregate {key}")
        mu, sd = float(row["mean_CSI"]), float(row["SD_pop"])
        if not (0 <= mu <= 1 and 0 <= sd <= 1):
            raise ValueError(f"Invalid CSI/SD for {key}")
        stats[key] = (mu, sd)
    expected = {(label, method, budget)
                for label in LABELS for method in FULL for budget in BUDGETS}
    expected |= {(label, method, .20)
                 for label in LABELS for method in AT20}
    if set(stats) != expected:
        raise ValueError(f"Unexpected aggregate keys; missing {expected - set(stats)}")
    with deltas_file.open(newline="", encoding="utf-8") as f:
        delta_rows = list(csv.DictReader(f))
    if len(delta_rows) != 10:
        raise ValueError("Expected 10 H5/H10 by budget paired-delta rows.")
    deltas = {}
    for row in delta_rows:
        key = (row["Label"], float(row["SupportRatio"]))
        if key in deltas:
            raise ValueError(f"Duplicate delta key {key}")
        ds = [float(row[f"seed{i}"]) for i in range(5)]
        if any(not np.isfinite(v) or abs(v) > 1 for v in ds):
            raise ValueError(f"Invalid delta for {key}")
        deltas[key] = ds
    if set(deltas) != {(label,budget) for label in LABELS for budget in BUDGETS}:
        raise ValueError("Incomplete paired-delta matrix.")
    # Each paired mean must equal the difference of two group means,
    # subject to published CSV rounding.
    for (label,budget), values in deltas.items():
        expected_mean = stats[(label,"PatchShot",budget)][0] - stats[(label,"Frozen prototype",budget)][0]
        if abs(float(np.mean(values)) - expected_mean) > 5e-6:
            raise ValueError(f"Unpaired or inconsistent delta: {(label,budget)}")
    return stats, deltas


def make_plots(stats, deltas, out_dir: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    out_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,
                         "pdf.fonttype":42,"savefig.dpi":220})
    def save(fig, name):
        fig.savefig(out_dir / (name + ".pdf"), bbox_inches="tight")
        fig.savefig(out_dir / (name + ".png"), bbox_inches="tight")
        plt.close(fig)
    fig, ax = plt.subplots(figsize=(9.2, 3.5))
    for label, marker in ((LABELS[0],"o"),(LABELS[1],"s")):
        for method in FULL:
            vals = [stats[(label,method,b)] for b in BUDGETS]
            means = np.array([v[0] for v in vals]) * 100
            sds = np.array([v[1] for v in vals]) * 100
            ax.errorbar([b*100 for b in BUDGETS], means, yerr=sds,
                        marker=marker, capsize=3,
                        linestyle="-" if method=="PatchShot" else "--",
                        label=f"{'H5' if label=='heavy_5' else 'H10'}: {method}")
    ax.set_xticks([b*100 for b in BUDGETS],["1%","5%","10%","20%","50%"])
    ax.set_ylim(bottom=0)
    ax.set_xlabel("Support budget (% of 1,922 radar-only cases)")
    ax.set_ylabel("Query CSI (%, mean ± population SD)")
    ax.set_title("(b) Support-efficiency: fully traced five-budget readouts",loc="left")
    ax.grid(axis="y",alpha=.25);ax.legend(fontsize=8,ncol=2)
    fig.tight_layout();save(fig,"figure4_b_verified_radar_budget")

    fig, ax = plt.subplots(figsize=(9.3, 3.6))
    xs=np.arange(len(AT20)); width=.38
    for i,label in enumerate(LABELS):
        vals=[stats[(label,m,.20)] for m in AT20]
        means=np.array([v[0] for v in vals])*100
        sds=np.array([v[1] for v in vals])*100
        ax.bar(xs+(i-.5)*width, means, width, yerr=sds,
               capsize=2.5, label="H5" if label=="heavy_5" else "H10")
    ax.set_xticks(xs, AT20, rotation=12, ha="right")
    ax.set_ylim(bottom=0)
    ax.set_ylabel("Query CSI (%, mean ± population SD)")
    ax.set_title("(c) Readouts with source-backed five-seed records at 20% support",loc="left")
    ax.grid(axis="y",alpha=.2); ax.legend()
    fig.tight_layout();save(fig,"figure4_c_verified_radar_readouts")

    mat=np.array([deltas[(label,b)] for label in LABELS for b in []]) if False else np.array(
        [[deltas[(label,b)][seed]*100 for b in BUDGETS]
         for label in LABELS for seed in range(5)])
    fig, ax = plt.subplots(figsize=(9.0,4.1))
    im=ax.imshow(mat, aspect="auto", interpolation="nearest")
    ax.set_xticks(range(5),[f"{int(b*100)}%" for b in BUDGETS])
    ax.set_yticks(range(10),[f"H5 seed {i}" for i in range(5)]+
                   [f"H10 seed {i}" for i in range(5)])
    ax.axhline(4.5,linewidth=1)
    for i in range(10):
        for j in range(5):
            ax.text(j,i,f"{mat[i,j]:+.1f}",ha="center",va="center",
                    color="white" if mat[i,j]>(mat.max()+mat.min())/2 else "black",fontsize=8.5)
    ax.set_xlabel("Support budget")
    ax.set_title("(d) Paired CSI gains: PatchShot − frozen prototype",loc="left")
    fig.colorbar(im,ax=ax,pad=.02,label="CSI gain (percentage points)")
    fig.tight_layout();save(fig,"figure4_d_verified_paired_gains")


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--summary",type=Path,default=ROOT/"reference_results/figure4_verified_budget_summary.csv")
    p.add_argument("--deltas",type=Path,default=ROOT/"reference_results/figure4_verified_paired_deltas_matrix.csv")
    p.add_argument("--out_dir",type=Path,default=ROOT/"figure_output")
    args=p.parse_args()
    stats, deltas = load_verified(args.summary,args.deltas)
    make_plots(stats,deltas,args.out_dir)
    print("Wrote three source-covered radar-only PDF/PNG panels.")
    print("This is a plotting audit, not full Figure 4 or independent model reproduction.")


if __name__=="__main__":
    main()
