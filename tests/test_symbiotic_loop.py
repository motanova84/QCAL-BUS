from noesis.consciousness_gate import ConsciousnessGate
from noesis.epistemic_memory import EpistemicMemory
from noesis.sabio_wisdom_bridge import lesson_from_wisdom_block, record_solver_failure
from noesis.symbiotic_loop import directive, evaluate


def test_four_invariant_gate_requires_all_dimensions():
    gate = ConsciousnessGate(0.999999, True, True, False)
    assert not gate.operational_closure
    assert gate.state == "INCOMPLETE"


def test_four_invariant_gate_is_operational_only():
    gate = ConsciousnessGate(0.999999, True, True, True)
    assert gate.operational_closure
    assert gate.state == "OPERATIONAL_CLOSURE_CANDIDATE"


def test_error_becomes_memory_without_becoming_counterexample():
    memory = EpistemicMemory()
    digest = record_solver_failure(
        memory,
        target_id="claim.alpha",
        repository="NOESISSOFIA",
        commit="deadbeef",
        strategy="formalize_missing_lemma",
        failure_class="LOGICAL",
        root_cause="missing premise",
        lesson="Make the premise explicit.",
    )
    assert len(digest) == 64
    assert memory.records[0].result == "FAIL"
    assert memory.records[0].invalidates == ()


def test_wisdom_block_is_mapped_to_a_lesson():
    lesson = lesson_from_wisdom_block({
        "wisdom_id": "WISDOM_1",
        "error_description": "proof failed",
        "context": "Lean build",
    })
    assert lesson.source_principle == "PECADO EL ERROR"
    assert "proof failed" in lesson.lesson


def test_symbiotic_loop_remains_advisory():
    state = evaluate(
        "claim.open",
        EpistemicMemory(),
        psi=0.999999,
        integration=True,
        self_reference=True,
        temporal_continuity=True,
    )
    result = directive(state)
    assert result["epistemic_status"] == "CANDIDATE"
    assert result["consciousness_gate"]["state"] == "OPERATIONAL_CLOSURE_CANDIDATE"
