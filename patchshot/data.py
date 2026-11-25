from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, Tuple

import numpy as np


def load_patch_data(
    path: str | Path,
    feature_key: str = "z_patch",
    labels: Iterable[str] = ("heavy_5", "heavy_10"),
) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
    """Load case-organized frozen patch representations.

    Expected representation shape:
        [num_cases, num_patches, feature_dim]

    Labels remain patch-level:
        [num_cases, num_patches]
    """
    path = Path(path)

    with np.load(path, allow_pickle=True) as data:
        if feature_key not in data.files:
            raise KeyError(
                f"Feature key '{feature_key}' not found. "
                f"Available keys: {data.files}"
            )

        z_case = np.asarray(
            data[feature_key],
            dtype=np.float32,
        )

        if z_case.ndim != 3:
            raise ValueError(
                "Expected [cases, patches, dim], "
                f"got {z_case.shape}"
            )

        y = {}

        for label in labels:
            if label in data.files:
                y[label] = np.asarray(
                    data[label],
                    dtype=np.int64,
                )

            elif label == "heavy_5" and "target_max" in data.files:
                y[label] = (
                    np.asarray(data["target_max"]) >= 5.0
                ).astype(np.int64)

            elif label == "heavy_10" and "target_max" in data.files:
                y[label] = (
                    np.asarray(data["target_max"]) >= 10.0
                ).astype(np.int64)

            else:
                raise KeyError(
                    f"Cannot construct label '{label}'."
                )

            if y[label].shape != z_case.shape[:2]:
                raise ValueError(
                    f"{label}: expected label shape "
                    f"{z_case.shape[:2]}, got {y[label].shape}"
                )

    return z_case, y


def flatten_cases(
    z_case: np.ndarray,
    y_case: np.ndarray,
    case_indices: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """Flatten selected cases into patch-level samples."""
    z = z_case[case_indices].reshape(
        -1,
        z_case.shape[-1],
    )
    y = y_case[case_indices].reshape(-1).astype(
        np.int64
    )
    return z, y


def build_fixed_query_and_support_pool(
    num_cases: int,
    seed: int,
    query_ratio: float = 0.50,
) -> Tuple[np.ndarray, np.ndarray]:
    """Construct one case-disjoint query/support partition."""
    rng = np.random.default_rng(seed)
    order = rng.permutation(num_cases)

    query_count = int(round(num_cases * query_ratio))

    query_cases = order[:query_count]
    support_pool = order[query_count:]

    return query_cases, support_pool


def nested_support_cases(
    support_pool: np.ndarray,
    total_num_cases: int,
    support_ratio: float,
) -> np.ndarray:
    """Return nested support cases.

    Important:
    support_ratio is defined relative to the full benchmark,
    not relative to the residual support pool.
    """
    desired_count = max(
        1,
        int(round(total_num_cases * support_ratio)),
    )

    desired_count = min(
        desired_count,
        len(support_pool),
    )

    return support_pool[:desired_count]
