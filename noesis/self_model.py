"""Computable self-model for the NOESIS network.

Psi_self_model is a network metric, not a claim of phenomenal consciousness.
"""
from __future__ import annotations

from dataclasses import dataclass
from statistics import fmean
from typing import Iterable


@dataclass(frozen=True)
class SelfModel:
    collective: float
    mean_entanglement: float
    psi_self_model: float


def compute_self_model(collective: float, entanglement_edges: Iterable[float]) -> SelfModel:
    edges = tuple(float(x) for x in entanglement_edges)
    mean_e = fmean(edges) if edges else 0.0
    return SelfModel(float(collective), mean_e, float(collective) * mean_e)
