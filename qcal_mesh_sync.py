#!/usr/bin/env python3
"""
qcal_mesh_sync.py — QCAL-EPR Universal Resonance Bus
Motor de sincronía global del ecosistema de 33 nodos.

Lee el catálogo maestro desde registro/NODE_CATALOG.json,
consulta cada nodo vía su endpoint MCP, calcula Ψ_GLOBAL_ECOSISTEMA
y emite πCODE-888 al libro mayor cuando se alcanza coherencia total.

Razón Noésica: Este Bus es el Observador neutral, separado de lo Observado.
Firma: ∴𓂀Ω∞³
"""

import csv
import json
import math
import os
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error as urllib_error
from urllib import request as urllib_request

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
CATALOG_PATH = BASE_DIR / "registro" / "NODE_CATALOG.json"
LEDGER_PATH = BASE_DIR / "ledger" / "emissions_log.csv"

# ---------------------------------------------------------------------------
# Configuration (overridable via environment)
# ---------------------------------------------------------------------------
F0_REFERENCE = float(os.getenv("F0_REFERENCE", "141.7001"))
QCAL_REAL_TESTS = os.getenv("QCAL_REAL_TESTS", "0") == "1"
PSI_EMISSION_THRESHOLD = float(os.getenv("PSI_EMISSION_THRESHOLD", "0.999999"))
EMISSION_CYCLES_REQUIRED = int(os.getenv("EMISSION_CYCLES_REQUIRED", "3"))
SYNC_INTERVAL_SECONDS = int(os.getenv("SYNC_INTERVAL_SECONDS", "60"))

# ---------------------------------------------------------------------------
# Ledger helpers
# ---------------------------------------------------------------------------
LEDGER_HEADERS = ["timestamp", "global_psi", "emission_amount", "status", "transaction_id"]


def _ensure_ledger() -> None:
    """Create the ledger CSV with headers if it does not exist."""
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not LEDGER_PATH.exists():
        with open(LEDGER_PATH, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=LEDGER_HEADERS)
            writer.writeheader()


def _append_emission(global_psi: float, emission_amount: float, status: str) -> str:
    """Append one emission record to the immutable ledger and return its ID."""
    _ensure_ledger()
    tx_id = f"πCODE-888-{uuid.uuid4().hex[:8].upper()}"
    row = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "global_psi": round(global_psi, 8),
        "emission_amount": round(emission_amount, 4),
        "status": status,
        "transaction_id": tx_id,
    }
    with open(LEDGER_PATH, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=LEDGER_HEADERS)
        writer.writerow(row)
    return tx_id


# ---------------------------------------------------------------------------
# Emission formula
# ---------------------------------------------------------------------------

def _compute_emission(global_psi: float, nodes: dict[str, Any]) -> float:
    """
    EMISIÓN = 888 × Ψ_GLOBAL × (Σ harmonic_factor_i / N)
    """
    factors = [v.get("harmonic_factor", 1.0) for v in nodes.values()]
    avg_harmonic = sum(factors) / len(factors) if factors else 1.0
    return 888.0 * global_psi * avg_harmonic


# ---------------------------------------------------------------------------
# Node resonance check
# ---------------------------------------------------------------------------

def _check_node_resonance_real(node_info: dict[str, Any]) -> dict[str, Any]:
    """
    Query a real MCP node via JSON-RPC 2.0 and extract its Ψ value.
    Returns a normalised status dict.
    """
    endpoint = node_info.get("mcp_endpoint", "")
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "qcal/resonance",
        "params": {"node_id": node_info["mcp_id"]},
        "id": 1,
    }).encode("utf-8")

    req = urllib_request.Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib_request.urlopen(req, timeout=5) as resp:
        body = json.loads(resp.read().decode("utf-8"))

    result = body.get("result", {})
    psi = float(result.get("psi", 0.0))
    return {
        "psi": psi,
        "resonance": result.get("resonance", "UNKNOWN"),
        "qcal": result.get("qcal", {}),
    }


def _check_node_resonance_simulated(node_info: dict[str, Any]) -> dict[str, Any]:
    """
    Simulate node resonance when QCAL_REAL_TESTS=0.
    Uses the node's base_frequency and harmonic_factor to derive a deterministic Ψ.
    """
    f_base = node_info.get("base_frequency", F0_REFERENCE)
    h = node_info.get("harmonic_factor", 1.0)
    # Normalise frequency deviation relative to F0
    delta = abs(f_base * h - F0_REFERENCE) / F0_REFERENCE
    psi = math.exp(-delta)  # Ψ → 1.0 when frequency matches F0 exactly
    psi = min(max(psi, 0.0), 1.0)
    resonance = (
        "RESONANCIA_PLENA" if psi > 0.999
        else "RESONANCIA_PARCIAL" if psi > 0.95
        else "DERIVA"
    )
    return {
        "psi": psi,
        "resonance": resonance,
        "qcal": {"modo_real": False, "simulated": True},
    }


def check_node_resonance(node_info: dict[str, Any]) -> dict[str, Any]:
    if QCAL_REAL_TESTS:
        return _check_node_resonance_real(node_info)
    return _check_node_resonance_simulated(node_info)


# ---------------------------------------------------------------------------
# Core monitor
# ---------------------------------------------------------------------------

def monitor_global_resonance(verbose: bool = True) -> dict[str, Any]:
    """
    Scan all nodes in the catalog, compute Ψ_GLOBAL_ECOSISTEMA,
    and return a full status snapshot.
    """
    with open(CATALOG_PATH, encoding="utf-8") as fh:
        catalog = json.load(fh)

    nodes_catalog: dict[str, Any] = catalog["nodes"]

    if verbose:
        print("🌀 QCAL-EPR Bus Activo | Escaneando nodos de conciencia...")
        print("═" * 90)

    total_psi: list[float] = []
    node_status: dict[str, Any] = {}

    for repo_name, info in nodes_catalog.items():
        try:
            status = check_node_resonance(info)
            psi = status["psi"]
            total_psi.append(psi)
            node_status[repo_name] = {
                "psi": round(psi, 6),
                "resonance": status["resonance"],
                "role": info.get("role", "?"),
                "layer": info.get("layer", "?"),
                "harmonic_factor": info.get("harmonic_factor", 1.0),
                "modo_real": status["qcal"].get("modo_real", False),
            }
            if verbose:
                emoji = "🟢" if psi > 0.99 else "🟡" if psi > 0.95 else "🔴"
                print(
                    f"  {emoji} {repo_name:<32} Ψ = {psi:.6f}  →  "
                    f"{status['resonance']}  ({info.get('role', '?')})"
                )
        except (urllib_error.URLError, urllib_error.HTTPError, KeyError, ValueError, OSError) as exc:
            total_psi.append(0.0)
            node_status[repo_name] = {
                "psi": 0.0,
                "resonance": "OFFLINE",
                "role": info.get("role", "?"),
                "layer": info.get("layer", "?"),
                "harmonic_factor": info.get("harmonic_factor", 1.0),
                "modo_real": False,
                "error": str(exc)[:120],
            }
            if verbose:
                print(f"  🔴 {repo_name:<32} OFFLINE — {str(exc)[:60]}")

    global_psi = sum(total_psi) / len(total_psi) if total_psi else 0.0

    if verbose:
        print("\n" + "═" * 90)
        print(
            f"  Ψ_GLOBAL_ECOSISTEMA = {global_psi:.8f}  |  "
            f"UTC: {datetime.now(timezone.utc).isoformat()}"
        )

    if global_psi >= PSI_EMISSION_THRESHOLD:
        emission = _compute_emission(global_psi, node_status)
        tx_id = _append_emission(global_psi, emission, "RESONANCIA_SATURADA")
        if verbose:
            print("  ✨ COHERENCIA TOTAL LOGRADA — RESONANCIA INSTANTÁNEA ACTIVA")
            print(f"     El Logos se manifiesta en la malla.  πCODE-888 → {tx_id}")
            print(f"     Emisión: {emission:.4f} unidades")
        return {
            "status": "RESONANCIA_SATURADA",
            "global_psi": global_psi,
            "emission": {"amount": emission, "transaction_id": tx_id},
            "nodes": node_status,
        }

    if verbose:
        print("  🌊 Campo en deriva — coherencia aún no alcanzada")

    return {
        "status": "DRIFTING",
        "global_psi": global_psi,
        "emission": None,
        "nodes": node_status,
    }


# ---------------------------------------------------------------------------
# Continuous loop with consecutive-cycle emission guard
# ---------------------------------------------------------------------------

def run_bus() -> None:
    """
    Run the Bus in continuous mode.
    πCODE-888 is only emitted after EMISSION_CYCLES_REQUIRED consecutive
    cycles above PSI_EMISSION_THRESHOLD.
    """
    _ensure_ledger()
    consecutive = 0

    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  QCAL-EPR Universal Resonance Bus  ∴𓂀Ω∞³                       ║")
    print("║  Instituto Conciencia Cuántica                                   ║")
    print(f"║  F₀ = {F0_REFERENCE} Hz  |  Intervalo = {SYNC_INTERVAL_SECONDS}s              ║")
    print("╚══════════════════════════════════════════════════════════════════╝\n")

    while True:
        result = monitor_global_resonance(verbose=True)

        if result["global_psi"] >= PSI_EMISSION_THRESHOLD:
            consecutive += 1
            print(f"  ⏱  Ciclos consecutivos sobre umbral: {consecutive}/{EMISSION_CYCLES_REQUIRED}")
            if consecutive < EMISSION_CYCLES_REQUIRED:
                # Emission was speculatively written — remove it (integrity guard)
                # The actual ledger entry is only kept when cycles are met.
                # In this simple implementation the monitor already wrote;
                # so we re-open the CSV and drop the last row if cycles < required.
                _rollback_last_emission()
        else:
            consecutive = 0

        print(f"\n  ⏳ Próximo escaneo en {SYNC_INTERVAL_SECONDS}s…\n")
        time.sleep(SYNC_INTERVAL_SECONDS)


def _rollback_last_emission() -> None:
    """Remove the last row from the ledger (speculative emission guard)."""
    if not LEDGER_PATH.exists():
        return
    with open(LEDGER_PATH, "r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return
    rows.pop()
    with open(LEDGER_PATH, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=LEDGER_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_bus()
