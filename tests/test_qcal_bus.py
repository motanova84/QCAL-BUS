"""
Tests de integración y unidad para QCAL-BUS.
Corren en modo simulado (QCAL_REAL_TESTS=0) sin dependencias externas.
"""

import csv
import json
import os
import sys
import tempfile
from io import StringIO
from pathlib import Path

import pytest

# Asegurar que el root del repo esté en sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("QCAL_REAL_TESTS", "0")

import mcp_network.resonance as resonance
import qcal_mesh_sync as bus


# ---------------------------------------------------------------------------
# mcp_network.resonance
# ---------------------------------------------------------------------------

class TestResonance:
    def test_sim_psi_in_range(self):
        psi = resonance._sim_psi("test-node")
        assert 0.95 <= psi <= 1.0

    def test_sim_psi_deterministic(self):
        assert resonance._sim_psi("abc") == resonance._sim_psi("abc")

    def test_sim_psi_different_for_different_ids(self):
        assert resonance._sim_psi("node-a") != resonance._sim_psi("node-b")

    def test_check_node_resonance_keys(self):
        result = resonance.check_node_resonance("test-node")
        assert "psi" in result
        assert "resonance" in result
        assert "qcal" in result
        assert 0.0 <= result["psi"] <= 1.0

    def test_resonance_label_coherencia_total(self):
        assert resonance._resonance_label(0.999999) == "COHERENCIA_TOTAL"
        assert resonance._resonance_label(1.0) == "COHERENCIA_TOTAL"

    def test_resonance_label_alta(self):
        assert resonance._resonance_label(0.995) == "RESONANCIA_ALTA"

    def test_resonance_label_media(self):
        assert resonance._resonance_label(0.97) == "RESONANCIA_MEDIA"

    def test_resonance_label_derivando(self):
        assert resonance._resonance_label(0.5) == "DERIVANDO"

    def test_field_coherence_nonempty(self):
        ids = ["riemann-mcp-server", "141-hz", "navier-mcp-server"]
        fc = resonance.field_coherence(ids)
        assert 0.0 < fc <= 1.0

    def test_field_coherence_empty(self):
        assert resonance.field_coherence([]) == 0.0


# ---------------------------------------------------------------------------
# qcal_mesh_sync — helpers
# ---------------------------------------------------------------------------

class TestMeshSyncHelpers:
    def test_load_catalog(self):
        catalog = bus.load_catalog()
        assert "meta" in catalog
        assert "nodes" in catalog
        assert len(catalog["nodes"]) == catalog["meta"]["total_nodes"]

    def test_calculate_emission_zero_nodes(self):
        assert bus.calculate_emission(1.0, {}) == 0.0

    def test_calculate_emission_positive(self):
        nodes = {"a": {"harmonic_factor": 1.0}, "b": {"harmonic_factor": 1.0}}
        emission = bus.calculate_emission(1.0, nodes)
        assert emission > 0

    def test_ensure_ledger_creates_file(self, tmp_path, monkeypatch):
        ledger = tmp_path / "ledger" / "emissions_log.csv"
        monkeypatch.setattr(bus, "LEDGER_PATH", ledger)
        bus.ensure_ledger()
        assert ledger.exists()
        with ledger.open() as f:
            header = next(csv.reader(f))
        assert header == ["timestamp", "global_psi", "emission_amount", "status", "transaction_id"]

    def test_append_emission(self, tmp_path, monkeypatch):
        ledger = tmp_path / "ledger" / "emissions_log.csv"
        monkeypatch.setattr(bus, "LEDGER_PATH", ledger)
        nodes = {"n": {"harmonic_factor": 1.0}}
        result = bus.append_emission(0.9999, nodes)
        assert result["status"] == "RESONANCIA_SATURADA"
        assert "πCODE-888" in result["transaction_id"]
        rows = bus.read_emissions_log(tail=10)
        assert len(rows) == 1

    def test_read_emissions_log_tail(self, tmp_path, monkeypatch):
        ledger = tmp_path / "ledger" / "emissions_log.csv"
        monkeypatch.setattr(bus, "LEDGER_PATH", ledger)
        nodes = {"n": {"harmonic_factor": 1.0}}
        for _ in range(5):
            bus.append_emission(0.9999, nodes)
        rows = bus.read_emissions_log(tail=3)
        assert len(rows) == 3


# ---------------------------------------------------------------------------
# monitor_global_resonance
# ---------------------------------------------------------------------------

class TestMonitorGlobalResonance:
    def test_returns_expected_keys(self):
        result = bus.monitor_global_resonance(verbose=False)
        for key in ("status", "global_psi", "nodes", "saturation_streak", "threshold", "timestamp"):
            assert key in result

    def test_global_psi_in_range(self):
        result = bus.monitor_global_resonance(verbose=False)
        assert 0.0 <= result["global_psi"] <= 1.0

    def test_all_33_nodes_present(self):
        result = bus.monitor_global_resonance(verbose=False)
        assert len(result["nodes"]) == 33


# ---------------------------------------------------------------------------
# MCP JSON-RPC server
# ---------------------------------------------------------------------------

class TestMCPServer:
    def test_initialize(self):
        req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        resp = bus._mcp_handle(req)
        assert resp["result"]["protocolVersion"] == "2024-11-05"
        assert resp["result"]["serverInfo"]["name"] == "qcal-mesh-bus"

    def test_tools_list(self):
        req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
        resp = bus._mcp_handle(req)
        names = [t["name"] for t in resp["result"]["tools"]]
        assert "get_mesh_state" in names
        assert "get_node_catalog" in names
        assert "get_emissions_log" in names

    def test_tools_call_get_mesh_state(self):
        req = {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
               "params": {"name": "get_mesh_state", "arguments": {}}}
        resp = bus._mcp_handle(req)
        content = json.loads(resp["result"]["content"][0]["text"])
        assert "global_psi" in content

    def test_tools_call_get_node_catalog(self):
        req = {"jsonrpc": "2.0", "id": 4, "method": "tools/call",
               "params": {"name": "get_node_catalog", "arguments": {}}}
        resp = bus._mcp_handle(req)
        catalog = json.loads(resp["result"]["content"][0]["text"])
        assert "nodes" in catalog

    def test_tools_call_get_emissions_log(self, tmp_path, monkeypatch):
        ledger = tmp_path / "ledger" / "emissions_log.csv"
        monkeypatch.setattr(bus, "LEDGER_PATH", ledger)
        req = {"jsonrpc": "2.0", "id": 5, "method": "tools/call",
               "params": {"name": "get_emissions_log", "arguments": {"tail": 5}}}
        resp = bus._mcp_handle(req)
        entries = json.loads(resp["result"]["content"][0]["text"])
        assert isinstance(entries, list)

    def test_unknown_tool(self):
        req = {"jsonrpc": "2.0", "id": 6, "method": "tools/call",
               "params": {"name": "nonexistent", "arguments": {}}}
        resp = bus._mcp_handle(req)
        assert resp["result"]["isError"] is True

    def test_unknown_method(self):
        req = {"jsonrpc": "2.0", "id": 7, "method": "unknown/method", "params": {}}
        resp = bus._mcp_handle(req)
        assert "error" in resp

    def test_notification_returns_none(self):
        req = {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}
        resp = bus._mcp_handle(req)
        assert resp is None

    def test_run_mcp_server_tools_list(self, monkeypatch, capsys):
        """Verifica el bucle completo stdin→stdout del servidor MCP."""
        payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}) + "\n"
        monkeypatch.setattr("sys.stdin", StringIO(payload))
        bus.run_mcp_server()
        captured = capsys.readouterr()
        resp = json.loads(captured.out.strip())
        names = [t["name"] for t in resp["result"]["tools"]]
        assert "get_mesh_state" in names
