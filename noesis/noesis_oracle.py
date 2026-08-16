"""NOESIS Oracle: choose what to investigate next, never what is true.

The Oracle consumes evidence, bottleneck candidates and epistemic memory.
Its output is explicitly advisory and remains below the proof boundary.
"""
from __future__ import annotations

from dataclasses import dataclass
from noesis.epistemic_memory import EpistemicMemory
from noesis.strategy_ranker import Strategy, rank_strategies


@dataclass(frozen=True)
class OracleDecision:
    target_id: str
    candidates: tuple[dict, ...]
    epistemic_status: str = "CANDIDATE"


def advise(target_id: str, strategies: list[Strategy], memory: EpistemicMemory) -> OracleDecision:
    ranked = rank_strategies(target_id, strategies, memory)
    return OracleDecision(target_id=target_id, candidates=tuple(ranked))


def from_bottleneck(target_id: str, memory: EpistemicMemory) -> OracleDecision:
    """Return a conservative default strategy set for an unresolved target."""
    strategies = [
        Strategy("formalize_missing_lemma", evidence=0.8, dependency_coverage=0.6, cost=0.7),
        Strategy("reproduce_existing_result", evidence=0.7, dependency_coverage=0.8, cost=0.5),
        Strategy("search_counterexample", evidence=0.5, dependency_coverage=0.4, cost=0.4),
    ]
    return advise(target_id, strategies, memory)
