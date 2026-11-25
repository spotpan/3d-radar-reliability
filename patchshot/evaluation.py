from __future__ import annotations
from dataclasses import dataclass
from typing import Dict
import numpy as np
from sklearn.decomposition import PCA
from .data import flatten_cases
from .metrics import metric_dict, separation_ratio
from .model import project_numpy, train_supcon_projection
from .readout import choose_threshold, prototype_scores
from .matched_ce import train_matched_ce_projection

@dataclass
class EvaluationConfig:
    mode: str = "supcon"
    pca_dim: int = 128
    pca_whiten: bool = False
    epochs: int = 20
    steps_per_epoch: int = 60
    batch_size: int = 512
    learning_rate: float = 1e-3
    temperature: float = 0.1
    threshold_steps: int = 500
    device: str = "cuda"

def evaluate_one_split(z_case: np.ndarray, y_case: np.ndarray,
                       query_cases: np.ndarray, support_cases: np.ndarray,
                       seed: int, config: EvaluationConfig) -> Dict[str, float]:
    """Canonical patch-level evaluation with disjoint query/support cases."""
    support_features, support_target = flatten_cases(z_case, y_case, support_cases)
    query_features, query_target = flatten_cases(z_case, y_case, query_cases)
    if support_target.sum() == 0:
        raise RuntimeError(f"No support positives for seed={seed}.")
    if support_target.sum() == len(support_target):
        raise RuntimeError("No support negatives.")
    if config.mode == "frozen":
        support_embedding, query_embedding = support_features, query_features
    elif config.mode == "pca":
        n_components = min(config.pca_dim, support_features.shape[0], support_features.shape[1])
        pca = PCA(n_components=n_components, whiten=config.pca_whiten, random_state=seed)
        support_embedding = pca.fit_transform(support_features.astype(np.float32))
        query_embedding = pca.transform(query_features.astype(np.float32))
    elif config.mode == "supcon":
        model = train_supcon_projection(
            support_features=support_features, support_target=support_target,
            seed=seed, epochs=config.epochs, steps_per_epoch=config.steps_per_epoch,
            batch_size=config.batch_size, learning_rate=config.learning_rate,
            temperature=config.temperature, device=config.device,
        )
        support_embedding = project_numpy(model, support_features, config.device)
        query_embedding = project_numpy(model, query_features, config.device)
    elif config.mode == "matched_ce":
        model = train_matched_ce_projection(
            support_features=support_features,
            support_target=support_target,
            seed=seed,
            epochs=config.epochs,
            steps_per_epoch=config.steps_per_epoch,
            batch_size=config.batch_size,
            learning_rate=config.learning_rate,
            weight_decay=1e-4,
            device=config.device,
        )
        support_embedding = project_numpy(model, support_features, config.device)
        query_embedding = project_numpy(model, query_features, config.device)
    else:
        raise ValueError(f"Unsupported mode: {config.mode}")
    support_score, query_score = prototype_scores(support_embedding, support_target, query_embedding)
    threshold = choose_threshold(support_score, support_target, config.threshold_steps)
    result = metric_dict(query_score >= threshold, query_target, query_score)
    result["SepRatio"] = separation_ratio(query_score, query_target)
    result["Threshold"] = float(threshold)
    result["SupportCases"] = int(len(support_cases))
    result["QueryCases"] = int(len(query_cases))
    result["SupportPatches"] = int(len(support_target))
    result["QueryPatches"] = int(len(query_target))
    return result
