"""Deterministic Critical Bottleneck analysis for the NOESIS evidence graph.

This module produces a *work-priority* signal, not a truth oracle. It never
promotes an epistemic state and never interprets resonance as proof.

The objective is deliberately narrower and more useful: identify unresolved
artifacts whose resolution would unlock the largest amount of explicitly
represented evidence in the graph.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

SCHEMA = "NOESIS-CRITICAL-BOTTLENECK/1.0"
UNRESOLVED_STATUSES = frozenset({"UNRESOLVED", "AXIOM"})


@dataclass(frozen=True)
class BottleneckCandidate:
    node_id: str
    label: str
    kind: str
    repository: str
    path: str
    line: int | None
    status: str
    direct_dependents: int
    reachable_dependents: int
    blocking_edges: int
    score: int
    rationale: str


def _nodes(graph: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return list(graph.get("nodes", []))


def _edges(graph: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return list(graph.get("edges", []))


def _reverse_dependencies(edges: Iterable[Mapping[str, Any]]) -> dict[str, set[str]]:
    """target -> sources for explicit ``source depends_on target`` edges."""
    reverse: dict[str, set[str]] = defaultdict(set)
    for edge in edges:
        if edge.get("kind") != "depends_on":
            continue
        source, target = str(edge.get("source", "")), str(edge.get("target", ""))
        if source and target and source != target:
            reverse[target].add(source)
    return reverse


def _forward_blocks(edges: Iterable[Mapping[str, Any]]) -> dict[str, set[str]]:
    """source -> targets for explicit ``source blocks target`` edges."""
    forward: dict[str, set[str]] = defaultdict(set)
    for edge in edges:
        if edge.get("kind") != "blocks":
            continue
        source, target = str(edge.get("source", "")), str(edge.get("target", ""))
        if source and target and source != target:
            forward[source].add(target)
    return forward


def _closure(start: str, adjacency: Mapping[str, set[str]]) -> set[str]:
    seen: set[str] = set()
    queue: deque[str] = deque(sorted(adjacency.get(start, set())))
    while queue:
        node = queue.popleft()
        if node in seen or node == start:
            continue
        seen.add(node)
        queue.extend(sorted(adjacency.get(node, set())))
    return seen


def _candidate_nodes(graph: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return [
        node for node in _nodes(graph)
        if str(node.get("status", "")) in UNRESOLVED_STATUSES
        or str(node.get("kind", "")) == "proof_obligation"
    ]


def rank_bottlenecks(graph: Mapping[str, Any]) -> list[BottleneckCandidate]:
    """Rank unresolved artifacts by deterministic graph-unlock potential.

    Only explicit dependency/blocking edges participate.  Frequency values,
    resonance proximity, coherence values and labels are intentionally absent
    from the scoring function.
    """
    reverse = _reverse_dependencies(_edges(graph))
    forward = _forward_blocks(_edges(graph))
    ranked: list[BottleneckCandidate] = []

    for node in _candidate_nodes(graph):
        node_id = str(node.get("node_id", node.get("id", "")))
        dependents = _closure(node_id, reverse)
        blocked = _closure(node_id, forward)
        direct = len(reverse.get(node_id, set()))
        edge_count = direct + len(forward.get(node_id, set()))
        reachable = len(dependents | blocked)

        # Integer, explainable score. Topology only.
        score = 100 * reachable + 10 * direct + edge_count
        rationale: list[str] = []
        if dependents:
            rationale.append(f"unlocks {len(dependents)} dependent node(s)")
        if blocked:
            rationale.append(f"blocks {len(blocked)} downstream node(s)")
        if not rationale:
            rationale.append("no explicit downstream dependency is recorded")

        ranked.append(BottleneckCandidate(
            node_id=node_id,
            label=str(node.get("label", "")),
            kind=str(node.get("kind", "")),
            repository=str(node.get("repository", "")),
            path=str(node.get("path", "")),
            line=node.get("line"),
            status=str(node.get("status", "")),
            direct_dependents=direct,
            reachable_dependents=reachable,
            blocking_edges=edge_count,
            score=score,
            rationale="; ".join(rationale),
        ))

    return sorted(ranked, key=lambda c: (-c.score, c.node_id))


def build_directive(graph: Mapping[str, Any]) -> dict[str, Any]:
    ranked = rank_bottlenecks(graph)
    top = asdict(ranked[0]) if ranked else None
    return {
        "schema": SCHEMA,
        "graph_schema": graph.get("schema"),
        "graph_commit": graph.get("commit"),
        "selection_policy": {
            "objective": "maximize explicit graph-unlock potential",
            "epistemic_effect": "none",
            "tie_break": "node_id ascending",
            "frequency_or_coherence_used": False,
        },
        "candidate_count": len(ranked),
        "critical_bottleneck": top,
        "candidates": [asdict(candidate) for candidate in ranked],
        "next_action": (
            {
                "action": "INVESTIGATE",
                "target": top["node_id"],
                "verification_required": True,
                "promotion_allowed": False,
            }
            if top else {"action": "NO_UNRESOLVED_BOTTLENECK"}
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Rank NOESIS evidence-graph bottlenecks")
    parser.add_argument("--graph", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    graph = json.loads(Path(args.graph).read_text(encoding="utf-8"))
    directive = build_directive(graph)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(directive, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    top = directive["critical_bottleneck"]
    print(json.dumps({
        "output": str(output),
        "candidate_count": directive["candidate_count"],
        "critical_bottleneck": top["node_id"] if top else None,
        "score": top["score"] if top else None,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
