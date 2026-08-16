"""Deterministic bridge from Ramsey resonance edges to NOESIS evidence edges.

The bridge preserves provenance and keeps resonance from being interpreted as
scientific support by itself. A resonance edge is a graph relation; evidence
status must be supplied by an independently verified artifact.
"""

from dataclasses import dataclass, asdict
from hashlib import sha256
import json
from typing import Literal

EvidenceKind = Literal[
    "defines", "depends_on", "resonates_with", "supports", "proves",
    "implements", "tests", "reproduces", "blocks", "contradicts",
]


@dataclass(frozen=True)
class Provenance:
    repository: str
    commit: str
    path: str


@dataclass(frozen=True)
class EvidenceEdge:
    source: str
    target: str
    kind: EvidenceKind
    provenance: Provenance
    verified: bool = False
    note: str = ""

    def canonical(self) -> dict:
        value = asdict(self)
        value["provenance"] = asdict(self.provenance)
        return value


def resonance_edge(source: str, target: str, provenance: Provenance,
                   verified: bool = False) -> EvidenceEdge:
    return EvidenceEdge(
        source=source,
        target=target,
        kind="resonates_with",
        provenance=provenance,
        verified=verified,
        note="Resonance is a graph relation, not scientific validation by itself.",
    )


def graph_digest(edges: list[EvidenceEdge]) -> str:
    payload = [edge.canonical() for edge in edges]
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return sha256(canonical.encode("utf-8")).hexdigest()
