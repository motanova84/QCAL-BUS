from noesis.epistemic_memory import EpistemicMemory, FailureRecord
from noesis.noesis_oracle import from_bottleneck
from noesis.strategy_ranker import Strategy, rank_strategies


def test_failure_is_retained_and_hash_is_deterministic():
    memory = EpistemicMemory()
    record = FailureRecord(
        failure_id="FAIL-001",
        target_id="claim.alpha",
        repository="QCAL-BUS",
        commit="abc123",
        strategy="formalize_missing_lemma",
        result="FAIL",
        failure_class="LOGICAL",
        root_cause="missing premise",
        reproducible=True,
        lesson="The candidate needs an explicit premise.",
    )
    first = memory.add(record)
    second = memory.record_hash(record)
    assert first == second
    assert memory.lessons_for("claim.alpha") == ("The candidate needs an explicit premise.",)


def test_failed_strategy_is_penalized_but_not_declared_impossible():
    memory = EpistemicMemory([
        FailureRecord(
            failure_id="FAIL-002",
            target_id="claim.alpha",
            repository="QCAL-BUS",
            commit="abc123",
            strategy="formalize",
            result="FAIL",
            failure_class="DEPENDENCY",
            root_cause="dependency absent",
            reproducible=True,
            lesson="Add dependency first.",
        )
    ])
    ranked = rank_strategies(
        "claim.alpha",
        [Strategy("formalize", evidence=1.0), Strategy("reproduce", evidence=0.5)],
        memory,
    )
    assert all(item["status"] == "CANDIDATE" for item in ranked)
    assert ranked[0]["strategy"] == "reproduce"


def test_oracle_never_returns_proven_state():
    decision = from_bottleneck("claim.open", EpistemicMemory())
    assert decision.epistemic_status == "CANDIDATE"
    assert decision.candidates
    assert all(item["status"] == "CANDIDATE" for item in decision.candidates)
