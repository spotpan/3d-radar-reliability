"""Matched cross-entropy objective control for the Stage-27 PatchShot protocol.

Derived from legacy/controls/121e_final_table1_component_attribution.py
function train_matched_ce_projection. The projector and training schedule
match Stage-27 SupCon; only the training objective differs. The temporary
binary classifier is NOT the query readout: after training, support-derived
positive/negative prototypes and support-only calibration are used.
"""
from __future__ import annotations
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from .model import ProjectionHead, balanced_batch_indices

def train_matched_ce_projection(
    support_features: np.ndarray,
    support_target: np.ndarray,
    seed: int,
    epochs: int = 20,
    steps_per_epoch: int = 60,
    batch_size: int = 512,
    learning_rate: float = 1e-3,
    weight_decay: float = 1e-4,
    device: str = "cuda",
) -> ProjectionHead:
    """Fit matched CE projection using support labels only."""
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    if device.startswith("cuda") and not torch.cuda.is_available():
        device = "cpu"
    device_obj = torch.device(device)
    x = torch.from_numpy(
        support_features.astype(np.float32, copy=False)
    ).to(device_obj)
    y = torch.from_numpy(
        support_target.astype(np.int64, copy=False)
    ).long().to(device_obj)
    if (y == 0).sum().item() == 0 or (y == 1).sum().item() == 0:
        raise ValueError("Both support classes are required.")
    projector = ProjectionHead(in_dim=support_features.shape[-1]).to(device_obj)
    classifier = nn.Linear(128, 1).to(device_obj)
    optimizer = torch.optim.AdamW(
        list(projector.parameters()) + list(classifier.parameters()),
        lr=learning_rate, weight_decay=weight_decay
    )
    total_steps = epochs * steps_per_epoch
    projector.train()
    classifier.train()
    for _ in range(total_steps):
        indices = balanced_batch_indices(labels=y, batch_size=batch_size)
        embedding = projector(x[indices])
        logits = classifier(embedding).squeeze(-1)
        loss = F.binary_cross_entropy_with_logits(logits, y[indices].float())
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
    projector.eval()
    return projector
