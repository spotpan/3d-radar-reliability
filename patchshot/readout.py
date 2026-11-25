from __future__ import annotations
from typing import Tuple
import numpy as np
from .metrics import metric_dict

def l2_normalize(x: np.ndarray) -> np.ndarray:
    x = x.astype(np.float32, copy=False)
    return x / (np.linalg.norm(x, axis=-1, keepdims=True) + 1e-8)

def prototype_scores(support_embedding: np.ndarray, support_target: np.ndarray,
                     query_embedding: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    support_embedding = l2_normalize(support_embedding)
    query_embedding = l2_normalize(query_embedding)
    support_target = support_target.astype(bool)
    if support_target.sum() == 0:
        raise RuntimeError("Support set has no positive patch.")
    if (~support_target).sum() == 0:
        raise RuntimeError("Support set has no negative patch.")
    positive_prototype = l2_normalize(
        support_embedding[support_target].mean(axis=0, keepdims=True))[0]
    negative_prototype = l2_normalize(
        support_embedding[~support_target].mean(axis=0, keepdims=True))[0]
    support_score = support_embedding @ positive_prototype - support_embedding @ negative_prototype
    query_score = query_embedding @ positive_prototype - query_embedding @ negative_prototype
    return support_score, query_score

def choose_threshold(score: np.ndarray, target: np.ndarray,
                     num_thresholds: int = 500) -> float:
    """Original support-only CSI calibration, with F1 tie-breaking."""
    lo = float(np.quantile(score, 0.001))
    hi = float(np.quantile(score, 0.999))
    if abs(hi - lo) < 1e-12:
        return lo
    best_threshold, best_csi, best_f1 = lo, -1.0, -1.0
    for threshold in np.linspace(lo, hi, num_thresholds):
        metrics = metric_dict(score >= threshold, target, score)
        better = metrics["CSI"] > best_csi + 1e-12
        tied = abs(metrics["CSI"] - best_csi) <= 1e-12
        if better or (tied and metrics["F1"] > best_f1):
            best_csi = metrics["CSI"]
            best_f1 = metrics["F1"]
            best_threshold = float(threshold)
    return best_threshold
