from __future__ import annotations
from typing import Dict
import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score

def metric_dict(pred: np.ndarray, target: np.ndarray, score: np.ndarray) -> Dict[str, float]:
    pred = pred.astype(bool)
    target = target.astype(bool)
    tp = int(np.sum(pred & target))
    fp = int(np.sum(pred & ~target))
    fn = int(np.sum(~pred & target))
    tn = int(np.sum(~pred & ~target))
    total = tp + fp + fn + tn
    precision = tp / (tp + fp + 1e-8)
    recall = tp / (tp + fn + 1e-8)
    f1 = 2 * tp / (2 * tp + fp + fn + 1e-8)
    csi = tp / (tp + fp + fn + 1e-8)
    far = fp / (tp + fp + 1e-8)
    acc = (tp + tn) / (total + 1e-8)
    pred_ratio = (tp + fp) / (total + 1e-8)
    true_ratio = (tp + fn) / (total + 1e-8)
    bias_ratio = pred_ratio / (true_ratio + 1e-8)
    if np.unique(target).size == 2:
        ap = float(average_precision_score(target, score))
        auroc = float(roc_auc_score(target, score))
    else:
        ap = float("nan")
        auroc = float("nan")
    return {
        "TP": tp, "FP": fp, "FN": fn, "TN": tn,
        "CSI": float(csi), "F1": float(f1),
        "Precision": float(precision), "Recall": float(recall),
        "FAR": float(far), "ACC": float(acc),
        "AP": ap, "AUROC": auroc,
        "PredRatio": float(pred_ratio), "TrueRatio": float(true_ratio),
        "BiasRatio": float(bias_ratio),
    }

def separation_ratio(score: np.ndarray, target: np.ndarray) -> float:
    target = target.astype(bool)
    positive, negative = score[target], score[~target]
    if len(positive) == 0 or len(negative) == 0:
        return float("nan")
    numerator = abs(float(positive.mean() - negative.mean()))
    pooled_std = np.sqrt(0.5 * (float(positive.var()) + float(negative.var())))
    return numerator / (pooled_std + 1e-8)
