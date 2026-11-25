from __future__ import annotations

from typing import List

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class ProjectionHead(nn.Module):
    """Support-supervised PatchShot re-access projection.

    Canonical Stage-27 architecture:
        Linear(d, 256) -> GELU -> Linear(256, 128) -> L2 norm
    """

    def __init__(
        self,
        in_dim: int,
        hidden_dim: int = 256,
        out_dim: int = 128,
    ):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, out_dim),
        )

    def forward(
        self,
        x: torch.Tensor,
    ) -> torch.Tensor:
        return F.normalize(
            self.net(x),
            dim=-1,
        )


def supcon_loss(
    embedding: torch.Tensor,
    labels: torch.Tensor,
    temperature: float,
) -> torch.Tensor:
    """Supervised contrastive loss used by canonical PatchShot."""
    similarity = (
        embedding @ embedding.T
        / temperature
    )

    eye = torch.eye(
        similarity.shape[0],
        dtype=torch.bool,
        device=similarity.device,
    )

    positive_mask = (
        labels[:, None].eq(labels[None, :])
        & ~eye
    )

    logits_mask = ~eye

    similarity = (
        similarity
        - similarity.max(
            dim=1,
            keepdim=True,
        ).values.detach()
    )

    exp_similarity = (
        torch.exp(similarity)
        * logits_mask
    )

    log_probability = (
        similarity
        - torch.log(
            exp_similarity.sum(
                dim=1,
                keepdim=True,
            )
            + 1e-8
        )
    )

    positive_count = positive_mask.sum(dim=1)
    valid = positive_count > 0

    positive_log_probability = (
        (positive_mask * log_probability).sum(dim=1)
        / positive_count.clamp_min(1)
    )

    return -positive_log_probability[valid].mean()


def balanced_batch_indices(
    labels: torch.Tensor,
    batch_size: int,
) -> torch.Tensor:
    """Sample an approximately 50/50 positive/negative patch batch."""
    positive_indices = torch.where(
        labels == 1
    )[0]

    negative_indices = torch.where(
        labels == 0
    )[0]

    if (
        len(positive_indices) == 0
        or len(negative_indices) == 0
    ):
        raise RuntimeError(
            "Balanced sampling requires both classes."
        )

    positive_count = batch_size // 2
    negative_count = batch_size - positive_count

    positive_sample = positive_indices[
        torch.randint(
            len(positive_indices),
            (positive_count,),
            device=labels.device,
        )
    ]

    negative_sample = negative_indices[
        torch.randint(
            len(negative_indices),
            (negative_count,),
            device=labels.device,
        )
    ]

    indices = torch.cat(
        [positive_sample, negative_sample],
        dim=0,
    )

    permutation = torch.randperm(
        len(indices),
        device=labels.device,
    )

    return indices[permutation]


def train_supcon_projection(
    support_features: np.ndarray,
    support_target: np.ndarray,
    seed: int,
    epochs: int = 20,
    steps_per_epoch: int = 60,
    batch_size: int = 512,
    learning_rate: float = 1e-3,
    temperature: float = 0.1,
    device: str = "cuda",
) -> ProjectionHead:
    """Fit PatchShot projection using support patches only."""
    torch.manual_seed(seed)
    np.random.seed(seed)

    x = torch.from_numpy(
        support_features.astype(np.float32)
    ).to(device)

    y = torch.from_numpy(
        support_target.astype(np.int64)
    ).long().to(device)

    model = ProjectionHead(
        in_dim=support_features.shape[-1],
    ).to(device)

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=learning_rate,
        weight_decay=1e-4,
    )

    for _ in range(epochs):
        model.train()

        for _ in range(steps_per_epoch):
            indices = balanced_batch_indices(
                labels=y,
                batch_size=batch_size,
            )

            embedding = model(x[indices])

            loss = supcon_loss(
                embedding=embedding,
                labels=y[indices],
                temperature=temperature,
            )

            optimizer.zero_grad(
                set_to_none=True
            )
            loss.backward()
            optimizer.step()

    return model


def project_numpy(
    model: nn.Module,
    array: np.ndarray,
    device: str,
    batch_size: int = 4096,
) -> np.ndarray:
    outputs: List[np.ndarray] = []

    model.eval()

    with torch.no_grad():
        for start in range(
            0,
            len(array),
            batch_size,
        ):
            batch = torch.from_numpy(
                array[
                    start:start + batch_size
                ].astype(np.float32)
            ).to(device)

            outputs.append(
                model(batch).cpu().numpy()
            )

    return np.concatenate(
        outputs,
        axis=0,
    )
