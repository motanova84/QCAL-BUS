"""NOESIS epistemic memory: validated lessons from attempts.

A failure is retained as evidence about a strategy under explicit conditions.
It is never treated as proof that the target claim is false unless a separate
counterexample artifact establishes that fact.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Iterable


FAILURE_CLASSES = frozenset({
    "LOGICAL", "DEPENDENCY", "DOMAIN", "IMPLEMENTATION", "EXPERIMENTAL", "COUNTEREXAMPLE"
})


@dataclass(frozen=True)
class FailureRecord:
    failure_id: str
    target_id: str
    repository: str
    commit: str
    strategy: str
    result: str
    failure_class: str
    root_cause: str
    reproducible: bool
    lesson: str
    invalidates: tuple[str, ...] = ()
    enables: tuple[str, ...] = ()
    next_candidates: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.result != "FAIL":
            raise ValueError("FailureRecord.result must be FAIL")
        if self.failure_class not in FAILURE_CLASSES:
            raise ValueError(f"unknown failure class: {self.failure_class}")


class EpistemicMemory:
    """Append-only, deterministic memory for failed or rejected strategies."""

    def __init__(self, records: Iterable[FailureRecord] = ()) -> None:
        self._records = list(records)

    @property
    def records(self) -> tuple[FailureRecord, ...]:
        return tuple(self._records)

    def add(self, record: FailureRecord) -> str:
        self._records.append(record)
        return self.record_hash(record)

    @staticmethod
    def record_hash(record: FailureRecord) -> str:
        payload = json.dumps(asdict(record), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return sha256(payload.encode("utf-8")).hexdigest()

    def prior_failures(self, target_id: str, strategy: str | None = None) -> tuple[FailureRecord, ...]:
        return tuple(r for r in self._records if r.target_id == target_id and (strategy is None or r.strategy == strategy))

    def lessons_for(self, target_id: str) -> tuple[str, ...]:
        return tuple(r.lesson for r in self.prior_failures(target_id) if r.lesson)

    def to_dict(self) -> dict:
        records = [asdict(r) for r in self._records]
        payload = {"schema": "NOESIS-EPISTEMIC-MEMORY/1.0", "records": records}
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        payload["sha256"] = sha256(canonical.encode("utf-8")).hexdigest()
        return payload

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "EpistemicMemory":
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        records = [FailureRecord(**r) for r in raw.get("records", [])]
        return cls(records)
