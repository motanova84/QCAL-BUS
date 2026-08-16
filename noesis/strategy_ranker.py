"""Deterministic strategy ranking for the NOESIS Oracle.

The ranker recommends exploration order; it cannot certify truth.
"""
from __future__ import annotations

from dataclasses import dataclass
from noesis.epistemic_memory import EpistemicMemory


@dataclass(frozen=True)
class Strategy:
    name: str
    evidence: float = 0.0
    dependency_coverage: float = 0.0
    historical_success: float = 0.0
    cost: float = 0.0
    prior_failures: int = 0

    def score(self) -> float:
        # Transparent heuristic. Keep the formula stable for reproducibility.
        return (
            0.35 * self.evidence
            + 0.30 * self.dependency_coverage
            + 0.25 * self.historical_success
            - 0.05 * self.cost
            - 0.05 * min(self.prior_failures, 5) / 5.0
        )


def rank_strategies(target_id: str, strategies: list[Strategy], memory: EpistemicMemory) -> list[dict]:
    ranked: list[dict] = []
    for strategy in strategies:
        failures = memory.prior_failures(target_id, strategy.name)
        effective = Strategy(
            name=strategy.name,
            evidence=strategy.evidence,
            dependency_coverage=strategy.dependency_coverage,
            historical_success=strategy.historical_success,
            cost=strategy.cost,
            prior_failures=len(failures),
        )
        ranked.append({
            "strategy": effective.name,
            "score": round(effective.score(), 12),
            "prior_failures": len(failures),
            "status": "CANDIDATE",
        })
    return sorted(ranked, key=lambda item: (-item["score"], item["strategy"]))
