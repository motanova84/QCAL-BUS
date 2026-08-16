"""Build a deterministic NOESIS evidence graph from repository artifacts.

The builder is deliberately conservative: resonance/proximity can create a
`resonates_with` edge, but never a `supports` or `proves` edge by itself.
Formal and experimental relations require explicit verified artifacts.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

F0_REFERENCE = 141.7001
EPSILON = 0.001
SCHEMA = "NOESIS-EVIDENCE-GRAPH/1.0"


@dataclass(frozen=True)
class Node:
    node_id: str
    kind: str
    label: str
    repository: str
    path: str
    line: int | None = None
    status: str = "UNRESOLVED"


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    kind: str
    repository: str
    path: str
    line: int | None = None
    verified: bool = False
    note: str = ""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_revision(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
        ).strip()
    except Exception:
        return "UNKNOWN"


def node_id(repository: str, path: str, label: str) -> str:
    raw = f"{repository}:{path}:{label}".encode()
    return "node:" + sha256_bytes(raw)[:20]


def scan_python(path: Path, repository: str) -> list[Node]:
    nodes: list[Node] = []
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, UnicodeDecodeError):
        return nodes
    for item in ast.walk(tree):
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            nodes.append(Node(
                node_id(repository, str(path), item.name),
                "python_declaration", item.name, repository, str(path), item.lineno,
                "IMPLEMENTED",
            ))
    return nodes


def scan_lean(path: Path, repository: str) -> tuple[list[Node], list[Edge]]:
    nodes: list[Node] = []
    edges: list[Edge] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return nodes, edges

    declaration = re.compile(r"^\\s*(theorem|lemma|def|axiom|example)\\s+([A-Za-z0-9_'.]+)")
    for number, line in enumerate(text.splitlines(), 1):
        match = declaration.match(line)
        if match:
            kind, label = match.groups()
            status = "FORMALIZED" if kind in {"theorem", "lemma", "example"} else "DEFINED"
            if kind == "axiom":
                status = "AXIOM"
            nid = node_id(repository, str(path), label)
            nodes.append(Node(nid, kind, label, repository, str(path), number, status))
            if "sorry" in line:
                edges.append(Edge(nid, nid, "blocks", repository, str(path), number, False,
                                  "Declaration contains a sorry marker."))

    for number, line in enumerate(text.splitlines(), 1):
        if re.search(r"\\bsorry\\b|\\badmit\\b", line):
            label = f"proof-obligation@{number}"
            nid = node_id(repository, str(path), label)
            nodes.append(Node(nid, "proof_obligation", label, repository, str(path), number, "UNRESOLVED"))
    return nodes, edges


def scan_repository(root: Path, repository: str) -> tuple[list[Node], list[Edge]]:
    nodes: list[Node] = []
    edges: list[Edge] = []
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix == ".lean":
            n, e = scan_lean(path, repository)
            nodes.extend(n); edges.extend(e)
        elif path.suffix == ".py":
            nodes.extend(scan_python(path, repository))
    return nodes, edges


def build_graph(root: Path, repository: str) -> dict[str, Any]:
    nodes, edges = scan_repository(root, repository)

    # Deterministic semantic anchor. Proximity to f0 is deliberately represented
    # only as a candidate relation; it is never upgraded to scientific support.
    f0_nodes = [n for n in nodes if n.label in {"f0", "f0_base", "F0_REFERENCE"}]
    anchor = Node("concept:qcal.f0", "concept", "qcal.f0", repository, "semantic-registry", None, "DEFINED")
    nodes.append(anchor)
    for n in f0_nodes:
        edges.append(Edge(n.node_id, anchor.node_id, "depends_on", n.repository, n.path, n.line, False,
                          "Symbolic name matches QCAL frequency anchor; verify exact semantics."))

    nodes = sorted({n.node_id: n for n in nodes}.values(), key=lambda x: x.node_id)
    edges = sorted(edges, key=lambda x: (x.source, x.target, x.kind, x.path, x.line or 0))
    payload = {
        "schema": SCHEMA,
        "repository": repository,
        "commit": git_revision(root),
        "reference": {"f0_hz": F0_REFERENCE, "epsilon_hz": EPSILON},
        "nodes": [asdict(n) for n in nodes],
        "edges": [asdict(e) for e in edges],
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    payload["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--repository", default="motanova84/QCAL-BUS")
    parser.add_argument("--output", default="checkpoints/checkpoint_v1.json")
    args = parser.parse_args()
    graph = build_graph(Path(args.root).resolve(), args.repository)
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(target), "nodes": len(graph["nodes"]), "edges": len(graph["edges"]), "sha256": graph["sha256"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
