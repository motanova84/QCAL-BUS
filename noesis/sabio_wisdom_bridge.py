"""Bridge lessons from NOESISSOFIA's PECADO EL ERROR into NOESIS memory.

This adapter imports only the epistemic meaning of a failed attempt: the
failure remains a failure record and is never promoted to a counterexample or
proof without its own certificate.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from noesis.epistemic_memory import EpistemicMemory, FailureRecord


@dataclass(frozen=True)
class WisdomLesson:
    target_id: str
    lesson: str
    source_principle: str = "PECADO EL ERROR"


def record_solver_failure(
    memory: EpistemicMemory,
    *,
    target_id: str,
    repository: str,
    commit: str,
    strategy: str,
    failure_class: str,
    root_cause: str,
    lesson: str,
    reproducible: bool = True,
    failure_id: str | None = None,
) -> str:
    """Persist a failed attempt as a deterministic epistemic lesson."""
    record = FailureRecord(
        failure_id=failure_id or f"FAIL-{target_id}-{strategy}",
        target_id=target_id,
        repository=repository,
        commit=commit,
        strategy=strategy,
        result="FAIL",
        failure_class=failure_class,
        root_cause=root_cause,
        reproducible=reproducible,
        lesson=lesson,
    )
    return memory.add(record)


def lesson_from_wisdom_block(block: Mapping[str, object]) -> WisdomLesson:
    """Convert a NOESISSOFIA wisdom block into an auditable lesson object."""
    error = str(block.get("error_description", ""))
    context = str(block.get("context", "General learning context"))
    return WisdomLesson(
        target_id=str(block.get("wisdom_id", "UNKNOWN")),
        lesson=f"Error observed: {error}. Context: {context}.",
    )
