"""NOESIS epistemic auditor.

This module deliberately separates measured state from epistemic claims.
It never upgrades resonance into support/proof and never treats a coherence
threshold as evidence of phenomenal consciousness.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from hashlib import sha256
import json
from typing import Any, Mapping


class EpistemicState(str, Enum):
    MEASURED = "MEASURED"
    REPRODUCIBLE = "REPRODUCIBLE"
    FORMALLY_VERIFIED = "FORMALLY_VERIFIED"
    EXTERNALLY_REPRODUCED = "EXTERNALLY_REPRODUCED"
    SUPPORTED = "SUPPORTED"


@dataclass(frozen=True)
class EvidenceRecord:
    claim_id: str
    state: EpistemicState
    provenance: bool
    reproducible: bool
    formal_verified: bool
    externally_reproduced: bool
    units_defined: bool
    domain_defined: bool
    derivation_available: bool
    uncertainty_reported: bool
    source_sha256: str | None = None


@dataclass(frozen=True)
class AuditResult:
    claim_id: str
    state: str
    admissible: bool
    missing_requirements: tuple[str, ...]
    certificate_sha256: str


def _canonical(payload: Mapping[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def audit(record: EvidenceRecord) -> AuditResult:
    missing: list[str] = []
    if not record.provenance:
        missing.append("provenance")
    if not record.units_defined:
        missing.append("units_defined")
    if not record.domain_defined:
        missing.append("domain_defined")
    if not record.derivation_available:
        missing.append("derivation_available")

    # State promotion is monotonic and conservative.
    if record.externally_reproduced and record.reproducible and record.formal_verified:
        state = EpistemicState.SUPPORTED
    elif record.externally_reproduced:
        state = EpistemicState.EXTERNALLY_REPRODUCED
    elif record.formal_verified:
        state = EpistemicState.FORMALLY_VERIFIED
    elif record.reproducible:
        state = EpistemicState.REPRODUCIBLE
    else:
        state = EpistemicState.MEASURED

    admissible = not missing
    payload = {"record": asdict(record), "state": state.value, "admissible": admissible, "missing": missing}
    certificate = sha256(_canonical(payload)).hexdigest()
    return AuditResult(record.claim_id, state.value, admissible, tuple(missing), certificate)


def audit_consciousness_claim(record: EvidenceRecord) -> AuditResult:
    """Audit a consciousness claim without equating network coherence with consciousness.

    A coherence value may be an observation or self-model metric. This function
    intentionally does not provide a boolean consciousness verdict.
    """
    result = audit(record)
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Audit a NOESIS evidence record")
    parser.add_argument("json_file")
    args = parser.parse_args()
    with open(args.json_file, encoding="utf-8") as fh:
        raw = json.load(fh)
    record = EvidenceRecord(
        claim_id=raw["claim_id"],
        state=EpistemicState(raw.get("state", "MEASURED")),
        provenance=bool(raw.get("provenance", False)),
        reproducible=bool(raw.get("reproducible", False)),
        formal_verified=bool(raw.get("formal_verified", False)),
        externally_reproduced=bool(raw.get("externally_reproduced", False)),
        units_defined=bool(raw.get("units_defined", False)),
        domain_defined=bool(raw.get("domain_defined", False)),
        derivation_available=bool(raw.get("derivation_available", False)),
        uncertainty_reported=bool(raw.get("uncertainty_reported", False)),
        source_sha256=raw.get("source_sha256"),
    )
    print(json.dumps(asdict(audit(record)), indent=2, ensure_ascii=False))
