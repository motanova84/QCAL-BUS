"""NOESIS semantic registry seed.

Creates deterministic cross-repository identities for concepts that the
Cathedral Engine must trace. It does not certify scientific truth.
"""
from dataclasses import dataclass, asdict
from hashlib import sha256
import json
from pathlib import Path
from typing import Literal

Status = Literal["SYMBOLIC", "DEFINED", "FORMALIZED", "IMPLEMENTED", "EXPERIMENTAL", "REPRODUCED", "UNRESOLVED"]

@dataclass(frozen=True)
class SemanticEntry:
    concept_id: str
    symbol: str
    description: str
    status: Status
    repositories: tuple[str, ...]
    paths: tuple[str, ...]
    notes: str = ""

    def canonical(self) -> dict:
        value = asdict(self)
        value["repositories"] = list(self.repositories)
        value["paths"] = list(self.paths)
        return value

REGISTRY = (
    SemanticEntry(
        "qcal.f0", "f0", "QCAL reference frequency", "DEFINED",
        ("motanova84/141hz", "motanova84/Riemann-adelic", "motanova84/QCAL-BUS"),
        ("formalizacion/via_a_f0_tau_QCAL.lean", "qcal/FORMALIZACION_LEAN4_FINAL.lean", "QCAL/FORMALIZACION_LEAN4_FINAL.lean"),
        "Trace units, definition, derivation and independent empirical support separately.",
    ),
    SemanticEntry(
        "qcal.tau", "tau_QCAL", "QCAL characteristic time associated with f0", "FORMALIZED",
        ("motanova84/141hz", "motanova84/Riemann-adelic"),
        ("formalizacion/via_a_f0_tau_QCAL.lean", "formal/cierre_formal_qcal.lean"),
    ),
    SemanticEntry(
        "noesis.consciousness", "C", "NOESIS operational consciousness protocol", "DEFINED",
        ("motanova84/QCAL-BUS",), ("noesis/",),
        "Operational invariant; not a claim of phenomenological consciousness.",
    ),
    SemanticEntry(
        "qcal.psi", "Psi", "QCAL coherence variable and related expressions", "UNRESOLVED",
        ("motanova84/141hz", "motanova84/Riemann-adelic"), (),
        "Registry seed only; Cathedral must resolve each expression's exact context, units and domain.",
    ),
    SemanticEntry(
        "bal003.hardware_observer", "BAL003", "Experimental hardware and network observation node", "EXPERIMENTAL",
        ("motanova84/141hz", "motanova84/QCAL-BUS", "motanova84/RelojCuantico-141Hz-QCAL"),
        ("templo_core/noesis_live.py", "qcal/ARQUITECTURA_ECOSISTEMA.md", "noesis/service_registry.json"),
        "Connectivity and telemetry are observed separately from scientific claims; discovery is read-only and registry-bound.",
    ),
)

def build_registry() -> dict:
    entries = [entry.canonical() for entry in REGISTRY]
    payload = {"schema": "NOESIS-SEMANTIC-REGISTRY/1.0", "entries": entries}
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    payload["sha256"] = sha256(canonical.encode("utf-8")).hexdigest()
    return payload

def write_registry(path: str = "artifacts/noesis_semantic_registry.json") -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(build_registry(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target

if __name__ == "__main__":
    print(json.dumps(build_registry(), ensure_ascii=False, indent=2))
