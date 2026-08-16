"""Adapter for importing the Ramsey repository's resonance graph semantics.

The adapter deliberately treats Ramsey resonance as a graph-analysis layer,
not as an independent certificate of the scientific claims described by the
source repository. Provenance is retained so NOESIS can audit every edge.

Source: motanova84/Ramsey/resonance_analysis.py
Reference commit: b31a863fe1249db9b24cec97c098fd9bf34abbb9
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
import json
from typing import Iterable

F0 = 141.7001
EPSILON = 0.001
SOURCE_REPOSITORY = "motanova84/Ramsey"
SOURCE_PATH = "resonance_analysis.py"
SOURCE_COMMIT = "b31a863fe1249db9b24cec97c098fd9bf34abbb9"


@dataclass(frozen=True)
class ResonanceNode:
    node_id: str
    frequency_hz: float


@dataclass(frozen=True)
class ResonanceEdge:
    source: str
    target: str
    delta_hz: float
    resonant: bool
    modulus_hz: float
    threshold_hz: float
    source_repository: str = SOURCE_REPOSITORY
    source_path: str = SOURCE_PATH
    source_commit: str = SOURCE_COMMIT


def pairwise_resonance_graph(
    frequencies: Iterable[float],
    *,
    f0: float = F0,
    epsilon: float = EPSILON,
) -> dict:
    """Build a deterministic resonance graph using Ramsey's edge rule.

    For each pair, the circular frequency distance is
    min(|wi-wj|, f0-|wi-wj|). An edge is resonant iff that distance is below
    epsilon. This mirrors the current Ramsey implementation exactly.
    """
    values = [float(value) for value in frequencies]
    nodes = [ResonanceNode(str(i), value) for i, value in enumerate(values)]
    edges: list[ResonanceEdge] = []

    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            raw = abs(values[i] - values[j])
            delta = min(raw, f0 - raw)
            edges.append(
                ResonanceEdge(
                    source=str(i),
                    target=str(j),
                    delta_hz=delta,
                    resonant=delta < epsilon,
                    modulus_hz=f0,
                    threshold_hz=epsilon,
                )
            )

    payload = {
        "schema": "NOESIS-RAMSEY-RESONANCE-GRAPH/1.0",
        "nodes": [asdict(node) for node in nodes],
        "edges": [asdict(edge) for edge in edges],
        "parameters": {"f0_hz": f0, "epsilon_hz": epsilon},
        "provenance": {
            "repository": SOURCE_REPOSITORY,
            "path": SOURCE_PATH,
            "commit": SOURCE_COMMIT,
        },
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["sha256"] = sha256(canonical.encode()).hexdigest()
    return payload


def resonance_summary(graph: dict) -> dict:
    """Return auditable graph statistics without assigning scientific truth."""
    edges = graph["edges"]
    resonant = sum(1 for edge in edges if edge["resonant"])
    total = len(edges)
    return {
        "nodes": len(graph["nodes"]),
        "edges": total,
        "resonant_edges": resonant,
        "non_resonant_edges": total - resonant,
        "resonance_fraction": resonant / total if total else 0.0,
        "graph_sha256": graph["sha256"],
        "provenance": graph["provenance"],
    }
