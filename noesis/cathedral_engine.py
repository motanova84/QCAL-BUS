#!/usr/bin/env python3
"""NOESIS Cathedral Engine v1.

Discovers Lean proof obligations across a local ecosystem checkout without
claiming that discovery is proof. The engine emits deterministic metadata for
later proof synthesis and verification.

Design principle:
    C = Psi ∩ I ∩ R ∩ T

Operationally this means coherence, integration, self-inspection and
continuity are recorded as auditable metadata. A candidate proof is accepted
only by the downstream Lean compiler; this module never edits theorem bodies.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

SORRY_RE = re.compile(r"\b(?:sorry|by\s+sorry|admit)\b")
DECL_RE = re.compile(r"^\s*(?:theorem|lemma|example)\s+([A-Za-z0-9_'.]+)")
AXIOM_RE = re.compile(r"^\s*axiom\s+([A-Za-z0-9_'.]+)")


@dataclass(frozen=True)
class ProofObligation:
    proof_id: str
    repository: str
    file: str
    line: int
    declaration: str | None
    kind: str
    text: str
    sha256: str


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def iter_lean_files(root: Path) -> Iterable[Path]:
    yield from sorted(p for p in root.rglob("*.lean") if ".git" not in p.parts)


def discover(root: Path, repository: str) -> list[ProofObligation]:
    found: list[ProofObligation] = []
    for path in iter_lean_files(root):
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        declaration: str | None = None
        for idx, line in enumerate(lines, 1):
            match = DECL_RE.match(line)
            if match:
                declaration = match.group(1)
            kind = None
            if SORRY_RE.search(line):
                kind = "SORRY"
            elif AXIOM_RE.match(line):
                kind = "AXIOM"
            if kind:
                relative = path.relative_to(root).as_posix()
                material = f"{repository}:{relative}:{idx}:{line}"
                found.append(
                    ProofObligation(
                        proof_id="proof-" + sha256_text(material)[:16],
                        repository=repository,
                        file=relative,
                        line=idx,
                        declaration=declaration,
                        kind=kind,
                        text=line.strip(),
                        sha256=sha256_text(path.read_text(encoding="utf-8", errors="replace")),
                    )
                )
    return found


def lean_version(root: Path) -> str | None:
    try:
        proc = subprocess.run(["lake", "env", "lean", "--version"], cwd=root, text=True,
                              capture_output=True, timeout=30, check=False)
        return (proc.stdout or proc.stderr).strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="NOESIS mathematical cathedral discovery")
    parser.add_argument("root", type=Path, help="Local checkout containing Lean projects")
    parser.add_argument("--repository", default="local-ecosystem")
    parser.add_argument("--output", type=Path, default=Path("noesis-cathedral.json"))
    args = parser.parse_args()

    root = args.root.resolve()
    obligations = discover(root, args.repository)
    payload = {
        "protocol": "NOESIS-CATHEDRAL/1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": args.repository,
        "root": str(root),
        "invariants": {"Psi": "coherence", "I": "integration", "R": "self-reference", "T": "continuity"},
        "lean_version": lean_version(root),
        "counts": {
            "proof_obligations": sum(x.kind == "SORRY" for x in obligations),
            "axioms": sum(x.kind == "AXIOM" for x in obligations),
        },
        "obligations": [asdict(x) for x in obligations],
        "policy": {
            "auto_accept": False,
            "axiom_inflation": False,
            "compiler_is_authority": True,
        },
    }
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"NOESIS-CATHEDRAL/1.0: {len(obligations)} obligations recorded")
    print(f"output: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
