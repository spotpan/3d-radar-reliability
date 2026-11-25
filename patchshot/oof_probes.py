"""Case-grouped out-of-fold (OOF) readout probes from the Stage-116a protocol.

Requires already-computed case/patch representations. Does NOT reconstruct
unpublished Table II adapted embeddings or independent numerical results.
"""
from __future__ import annotations
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import StratifiedKFold

PROBES = ("Prototype", "Linear", "k-NN")

def l2(x):
    x = np.asarray(x, dtype=np.float32)
    return x / np.maximum(np.linalg.norm(x, axis=-1, keepdims=True), 1e-12)

def scores(probe, train_x, train_y, test_x, seed=0, k=5, alpha=1e-4, chunk=768):
    train_x, test_x = l2(train_x), l2(test_x)
    train_y = np.asarray(train_y, dtype=np.int8)
    if len(np.unique(train_y)) != 2:
        raise ValueError("Both positive and negative patches must occur in training.")
    if probe == "Prototype":
        pos = l2(train_x[train_y == 1].mean(axis=0, keepdims=True))[0]
        neg = l2(train_x[train_y == 0].mean(axis=0, keepdims=True))[0]
        return (test_x @ pos - test_x @ neg).astype(np.float32)
    if probe == "Linear":
        clf = SGDClassifier(
            loss="log_loss", penalty="l2", alpha=alpha,
            class_weight="balanced", max_iter=2500, tol=1e-4,
            random_state=seed, average=True,
        )
        clf.fit(train_x, train_y)
        return np.asarray(clf.decision_function(test_x), dtype=np.float32)
    if probe == "k-NN":
        import torch
        train_tensor = torch.from_numpy(train_x)
        labels_tensor = torch.from_numpy(train_y.astype(np.float32))
        out = np.empty(len(test_x), dtype=np.float32)
        with torch.no_grad():
            for start in range(0, len(test_x), chunk):
                end = min(start + chunk, len(test_x))
                qt = torch.from_numpy(test_x[start:end])
                similarity = qt @ train_tensor.T
                values, idx = torch.topk(similarity, k=min(k, len(train_x)),
                                         dim=1, largest=True, sorted=False)
                weights = torch.softmax(values / .1, dim=1)
                out[start:end] = (weights * labels_tensor[idx]).sum(dim=1).numpy()
        return out
    raise ValueError(f"Unknown probe: {probe}")

def best_csi_threshold(labels, value):
    labels = np.asarray(labels, dtype=np.int8)
    value = np.asarray(value, dtype=np.float64)
    finite = np.isfinite(value)
    labels, value = labels[finite], value[finite]
    if len(value) == 0 or labels.sum() == 0:
        return float("inf"), 0.0
    order = np.argsort(-value, kind="mergesort")
    ordered_value, ordered_label = value[order], labels[order]
    tp = np.cumsum(ordered_label)
    fp = np.cumsum(1 - ordered_label)
    fn = int(ordered_label.sum()) - tp
    csi = tp / np.maximum(tp + fp + fn, 1)
    boundary = np.ones(len(ordered_value), dtype=bool)
    if len(ordered_value) > 1:
        boundary[:-1] = ordered_value[:-1] != ordered_value[1:]
    choices = np.flatnonzero(boundary)
    best = choices[np.argmax(csi[choices])]
    return float(ordered_value[best]), float(csi[best])

def query_csi(labels, value, threshold):
    target = np.asarray(labels, dtype=bool).reshape(-1)
    pred = np.asarray(value).reshape(-1) >= threshold
    tp = int(np.sum(target & pred))
    fp = int(np.sum(~target & pred))
    fn = int(np.sum(target & ~pred))
    return tp / max(tp + fp + fn, 1)

def evaluate_oof_probe(probe, support_x_case, support_y_case,
                       query_x_case, query_y_case, seed=0, folds=5,
                       k=5, alpha=1e-4):
    sx = np.asarray(support_x_case, dtype=np.float32)
    sy = np.asarray(support_y_case, dtype=np.int8)
    qx = np.asarray(query_x_case, dtype=np.float32)
    qy = np.asarray(query_y_case, dtype=np.int8)
    n, patches, dim = sx.shape
    if sy.shape != (n, patches):
        raise ValueError("Support label shape mismatch.")
    if qx.ndim != 3 or qx.shape[1:] != (patches, dim) or qy.shape != qx.shape[:2]:
        raise ValueError("Query representation/label shape mismatch.")
    case_event = sy.astype(bool).any(axis=1).astype(int)
    n_folds = min(folds, int(case_event.sum()), int((1 - case_event).sum()))
    if n_folds < 2:
        raise ValueError("Cannot stratify case-grouped OOF folds.")
    splitter = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=seed)
    oof = np.full((n, patches), np.nan, dtype=np.float32)
    for fold, (train, valid) in enumerate(splitter.split(np.arange(n), case_event)):
        fold_scores = scores(probe, sx[train].reshape(-1, dim),
                             sy[train].reshape(-1),
                             sx[valid].reshape(-1, dim),
                             seed=seed * 100 + fold, k=k, alpha=alpha)
        oof[valid] = fold_scores.reshape(len(valid), patches)
    if not np.isfinite(oof).all():
        raise RuntimeError("Incomplete held-out case OOF scores.")
    threshold, calib_csi = best_csi_threshold(sy.ravel(), oof.ravel())
    query_scores = scores(probe, sx.reshape(-1, dim), sy.reshape(-1),
                          qx.reshape(-1, dim), seed=seed, k=k, alpha=alpha)
    return {"Probe": probe, "CSI": query_csi(qy, query_scores, threshold),
            "Threshold": threshold, "SupportOOFCSI": calib_csi,
            "OOFFolds": n_folds}

def evaluate_accessibility(support_x_case, support_y_case,
                           query_x_case, query_y_case, seed=0, folds=5):
    rows = [evaluate_oof_probe(probe, support_x_case, support_y_case,
                              query_x_case, query_y_case, seed=seed, folds=folds)
            for probe in PROBES]
    values = {row["Probe"]: row["CSI"] for row in rows}
    envelope = max(values.values())
    prototype = values["Prototype"]
    return rows, {"PrototypeCSI": prototype, "EnvelopeCSI": envelope,
                  "Accessibility": prototype / max(envelope, 1e-12),
                  "Gap": envelope - prototype}
