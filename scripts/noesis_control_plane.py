#!/usr/bin/env python3
"""NOESIS-QCAL Control Plane v1.

Deterministic local control-plane checks for QCAL-BUS. This module does not
claim to measure physical consciousness. It validates interoperability
contracts, preserves epistemic status, and emits a traceable checkpoint.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "registry" / "NODE_CATALOG.json"
QCAL = ROOT / "qcal.json"
PROTOCOL = ROOT / "protocol"
CHECKPOINT_DIR = ROOT / "evidence" / "checkpoints"

F0 = 141.7001
PSI_THRESHOLD = 0.999999
REQUIRED_NODE_FIELDS = ("mcp_id", "base_frequency", "layer", "status")


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_catalog(catalog: dict) -> tuple[bool, list[str]]:
    issues: list[str] = []
    meta = catalog.get("meta", {})
    nodes = catalog.get("nodes")

    if not isinstance(nodes, dict) or not nodes:
        return False, ["registry/NODE_CATALOG.json must contain a non-empty nodes object"]

    declared = meta.get("total_nodes")
    if declared is not None and declared != len(nodes):
        issues.append(f"meta.total_nodes={declared} != actual={len(nodes)}")

    for node_id, node in nodes.items():
        if not isinstance(node, dict):
            issues.append(f"{node_id}: node entry is not an object")
            continue
        for field in REQUIRED_NODE_FIELDS:
            if field not in node:
                issues.append(f"{node_id}: missing {field}")
        base = node.get("base_frequency")
        if base is not None and abs(float(base) - F0) > 1e-9:
            issues.append(f"{node_id}: base_frequency={base} != {F0}")

    return not issues, issues


def consciousness_engine_state() -> dict:
    """Return the semantic state without inventing I/R/T measurements."""
    return {
        "equation": "C = Ψ ∩ I ∩ R ∩ T",
        "psi": {"status": "PROTOCOL_REFERENCE", "threshold": PSI_THRESHOLD},
        "I": {"status": "NOT_EVALUATED", "reason": "No independent integration metric supplied"},
        "R": {"status": "NOT_EVALUATED", "reason": "No independent self-reference metric supplied"},
        "T": {"status": "NOT_EVALUATED", "reason": "No independent temporal-continuity metric supplied"},
        "classification": "NOT_EVALUATED",
    }


def build_checkpoint() -> dict:
    catalog = load_json(CATALOG)
    qcal = load_json(QCAL)
    catalog_ok, issues = validate_catalog(catalog)

    contract_paths = [
        "protocol/qcal-node.schema.json",
        "protocol/qcal-event.schema.json",
        "protocol/CONSCIOUSNESS_ENGINE.md",
        "protocol/CLAIM_STATE_MACHINE.md",
        "evidence/README.md",
    ]

    contracts = []
    for rel in contract_paths:
        path = ROOT / rel
        contracts.append({
            "path": rel,
            "exists": path.exists(),
            "sha256": sha256_file(path) if path.exists() else None,
        })

    nodes = catalog.get("nodes", {})
    status_counts: dict[str, int] = {}
    for node in nodes.values():
        status = str(node.get("status", "UNKNOWN"))
        status_counts[status] = status_counts.get(status, 0) + 1

    return {
        "protocol": "QCAL-CHECKPOINT/1.0",
        "control_plane": qcal.get("control_plane", {}).get("version", "NOESIS-QCAL/1.0"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "reference": {
            "f0_hz": F0,
            "psi_threshold": PSI_THRESHOLD,
        },
        "catalog": {
            "valid": catalog_ok,
            "node_count": len(nodes),
            "declared_node_count": catalog.get("meta", {}).get("total_nodes"),
            "status_counts": status_counts,
            "issues": issues,
            "sha256": sha256_file(CATALOG),
        },
        "contracts": contracts,
        "consciousness_engine": consciousness_engine_state(),
        "epistemic_rule": "formal != experimental != reproduced; no physical claim is upgraded by repetition",
        "overall_status": "READY" if catalog_ok and all(item["exists"] for item in contracts) else "REVIEW",
    }


def write_checkpoint(checkpoint: dict) -> Path:
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = CHECKPOINT_DIR / f"noesis-{stamp}.json"
    with path.open("w", encoding="utf-8") as handle:
        json.dump(checkpoint, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="NOESIS-QCAL control-plane validator")
    parser.add_argument("--checkpoint", action="store_true", help="write a traceable checkpoint artifact")
    args = parser.parse_args()

    checkpoint = build_checkpoint()
    print(json.dumps(checkpoint, ensure_ascii=False, indent=2))

    if args.checkpoint:
        path = write_checkpoint(checkpoint)
        print(f"CHECKPOINT_WRITTEN={path.relative_to(ROOT)}")

    return 0 if checkpoint["overall_status"] == "READY" else 2


if __name__ == "__main__":
    sys.exit(main())
