from noesis.discovery_layer import discover, load_registry


def test_registry_is_explicitly_read_only():
    registry = load_registry()
    assert registry["policy"]["mutations_allowed"] is False
    assert registry["policy"]["default_mode"] == "read_only"


def test_discovery_targets_only_declared_services(monkeypatch):
    calls = []

    def fake_probe(service, *args):
        calls.append((service["host"], service["port"]))
        return type(
            "Result",
            (),
            {"as_dict": lambda self: {"service_id": service["id"], "state": "REACHABLE"}},
        )()

    monkeypatch.setattr("noesis.discovery_layer.probe_tcp", fake_probe)
    monkeypatch.setattr("noesis.discovery_layer.probe_http", fake_probe)
    result = discover(timeout=0.01)
    declared = {(s["host"], s["port"]) for s in load_registry()["services"]}
    assert set(calls).issubset(declared)
    assert "snapshot_sha256" in result


def test_reference_frequency_is_exact():
    registry = load_registry()
    assert registry["policy"]["reference_frequency_hz"] == 141.7001


def test_registry_has_no_duplicate_service_ids():
    ids = [s["id"] for s in load_registry()["services"]]
    assert len(ids) == len(set(ids))


def test_ssh_probe_is_connect_only():
    registry = load_registry()
    ssh = next(s for s in registry["services"] if s["role"] == "ssh")
    assert ssh["health_mode"] == "tcp_connect"
    assert ssh["access"] == "read_only"
