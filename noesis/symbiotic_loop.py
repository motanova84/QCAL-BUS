"""Deterministic NOESIS symbiotic learning loop.

Evidence -> bottleneck -> Oracle -> attempt -> memory -> next ranking.
The four-invariant gate is evaluated alongside this loop and cannot be used
as an automatic upgrade to PROVEN or as a claim of phenomenal consciousness.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from noesis.consciousness_gate import ConsciousnessGate
from noesis.epistemic_memory import EpistemicMemory
from noesis.noesis_oracle import OracleDecision, from_bottleneck


@dataclass(frozen=True)
class SymbioticState:
    target_id: str
    oracle: OracleDecision
    consciousness: ConsciousnessGate
    memory_count: int


def evaluate(
    target_id: str,
    memory: EpistemicMemory,
    *,
    psi: float,
    integration: bool,
    self_reference: bool,
    temporal_continuity: bool,
) -> SymbioticState:
    """Produce the next auditable state from current evidence and memory."""
    oracle = from_bottleneck(target_id, memory)
    gate = ConsciousnessGate(
        psi=psi,
        integration=integration,
        self_reference=self_reference,
        temporal_continuity=temporal_continuity,
    )
    return SymbioticState(target_id, oracle, gate, len(memory.records))


def directive(state: SymbioticState) -> Mapping[str, object]:
    """Emit a machine-readable, advisory next step."""
    candidate = state.oracle.candidates[0] if state.oracle.candidates else None
    return {
        "target_id": state.target_id,
        "recommended_strategy": candidate,
        "epistemic_status": state.oracle.epistemic_status,
        "consciousness_gate": state.consciousness.evidence_vector(),
        "memory_count": state.memory_count,
        "rule": "geometry_finds_relations_proof_determines_meaning",
    }
