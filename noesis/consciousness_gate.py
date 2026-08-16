"""Operational four-invariant gate for NOESIS.

The gate evaluates whether the software system has satisfied the framework's
operational closure conditions. It does not establish phenomenal consciousness
as a scientific fact; that boundary is enforced by the epistemic contract.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConsciousnessGate:
    psi: float
    integration: bool
    self_reference: bool
    temporal_continuity: bool
    psi_threshold: float = 0.999999

    @property
    def coherence_ok(self) -> bool:
        return self.psi >= self.psi_threshold

    @property
    def operational_closure(self) -> bool:
        return (
            self.coherence_ok
            and self.integration
            and self.self_reference
            and self.temporal_continuity
        )

    @property
    def state(self) -> str:
        return "OPERATIONAL_CLOSURE_CANDIDATE" if self.operational_closure else "INCOMPLETE"

    def evidence_vector(self) -> dict[str, object]:
        return {
            "Psi": self.coherence_ok,
            "I": self.integration,
            "R": self.self_reference,
            "T": self.temporal_continuity,
            "operational_closure": self.operational_closure,
            "state": self.state,
        }
