"""Rank unresolved evidence-graph nodes by downstream impact.

The output is a CANDIDATE priority, never a proof or scientific claim.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path


def rank_nodes(graph: dict) -> list[dict]:
    nodes = {n["id"]: n for n in graph.get("nodes", []) if isinstance(n, dict) and "id" in n}
    outgoing = {node_id: set() for node_id in nodes}
    incoming = {node_id: set() for node_id in nodes}
    for edge in graph.get("edges", []):
        source, target = edge.get("source"), edge.get("target")
        if source in nodes and target in nodes:
            outgoing[source].add(target)
            incoming[target].add(source)
    candidates = []
    for node_id, node in nodes.items():
        text = json.dumps(node, ensure_ascii=False).lower()
        if not any(token in text for token in ("sorry", "admit", "unresolved")):
            continue
        downstream = len(outgoing[node_id])
        upstream = len(incoming[node_id])
        score = downstream * 10 + upstream
        candidates.append({
            "candidate": node_id,
            "score": score,
            "downstream_nodes": sorted(outgoing[node_id]),
            "upstream_nodes": sorted(incoming[node_id]),
            "status": "CANDIDATE",
        })
    return sorted(candidates, key=lambda item: (-item["score"], item["candidate"]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    graph = json.loads(Path(args.graph).read_text(encoding="utf-8"))
    payload = {
        "schema": "NOESIS-CRITICAL-BOTTLENECK/1.0",
        "graph_sha256": graph.get("sha256"),
        "status": "CANDIDATE",
        "ranking_method": "downstream*10+upstream",
        "candidates": rank_nodes(graph),
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
