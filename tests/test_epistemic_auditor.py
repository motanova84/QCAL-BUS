from noesis.epistemic_auditor import EvidenceRecord, EpistemicState, audit
from noesis.self_model import compute_self_model


def record(**overrides):
    data = dict(
        claim_id="qcal.f0",
        state=EpistemicState.MEASURED,
        provenance=True,
        reproducible=False,
        formal_verified=False,
        externally_reproduced=False,
        units_defined=True,
        domain_defined=True,
        derivation_available=True,
        uncertainty_reported=False,
    )
    data.update(overrides)
    return EvidenceRecord(**data)


def test_measurement_does_not_become_support():
    result = audit(record())
    assert result.state == "MEASURED"
    assert result.admissible


def test_formal_and_reproduced_can_reach_supported():
    result = audit(record(reproducible=True, formal_verified=True, externally_reproduced=True))
    assert result.state == "SUPPORTED"


def test_missing_contract_fields_block_admissibility():
    result = audit(record(derivation_available=False))
    assert not result.admissible
    assert "derivation_available" in result.missing_requirements


def test_self_model_is_only_a_metric():
    model = compute_self_model(0.999997, [0.999999, 0.999999])
    assert model.psi_self_model > 0.0
    assert not hasattr(model, "conscious")
