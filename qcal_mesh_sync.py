import csv
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import mcp_network.resonance as qcal
except Exception:  # pragma: no cover
    qcal = None

ROOT_DIR = Path(__file__).resolve().parent
CATALOG_PATH = ROOT_DIR / "registry" / "NODE_CATALOG.json"
LEDGER_PATH = ROOT_DIR / "ledger" / "emissions_log.csv"

EMISSION_BASE = float(os.getenv("QCAL_EMISSION_BASE", "888"))
GLOBAL_THRESHOLD = float(os.getenv("QCAL_GLOBAL_THRESHOLD", "0.999999"))
SATURATION_CYCLES = int(os.getenv("QCAL_SATURATION_CYCLES", "3"))
SYNC_INTERVAL_SECONDS = int(os.getenv("QCAL_SYNC_INTERVAL_SECONDS", "60"))

_SATURATION_STREAK = 0


def load_catalog():
    with CATALOG_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def ensure_ledger():
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    if LEDGER_PATH.exists():
        return
    with LEDGER_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["timestamp", "global_psi", "emission_amount", "status", "transaction_id"]
        )


def check_node_resonance(mcp_id):
    if qcal is None:
        raise RuntimeError("mcp_network.resonance no está disponible")
    return qcal.check_node_resonance(mcp_id)


def calculate_emission(global_psi, nodes):
    if not nodes:
        return 0.0
    harmonic_sum = sum(info.get("harmonic_factor", 1.0) for info in nodes.values())
    harmonic_avg = harmonic_sum / len(nodes)
    return round(EMISSION_BASE * global_psi * harmonic_avg, 6)


def append_emission(global_psi, nodes):
    ensure_ledger()
    timestamp = datetime.now(timezone.utc).isoformat()
    emission_amount = calculate_emission(global_psi, nodes)
    transaction_id = f"πCODE-888-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    with LEDGER_PATH.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                timestamp,
                f"{global_psi:.8f}",
                f"{emission_amount:.6f}",
                "RESONANCIA_SATURADA",
                transaction_id,
            ]
        )
    return {
        "timestamp": timestamp,
        "global_psi": round(global_psi, 8),
        "emission_amount": emission_amount,
        "status": "RESONANCIA_SATURADA",
        "transaction_id": transaction_id,
    }


def monitor_global_resonance(verbose=True):
    global _SATURATION_STREAK

    catalog = load_catalog()
    nodes = catalog.get("nodes", {})

    if verbose:
        print("🌀 QCAL-EPR Bus Activo | Escaneando nodos de conciencia...")

    total_psi = []
    node_status = {}

    for repo_name, info in nodes.items():
        try:
            status = check_node_resonance(info["mcp_id"])
            psi = float(status["psi"])
            total_psi.append(psi)
            node_status[repo_name] = {
                "psi": round(psi, 6),
                "resonance": status.get("resonance", "UNKNOWN"),
                "role": info.get("role"),
                "layer": info.get("layer"),
                "harmonic_factor": info.get("harmonic_factor", 1.0),
                "modo_real": status.get("qcal", {}).get("modo_real", False),
            }
            if verbose:
                emoji = "🟢" if psi > 0.99 else "🟡" if psi > 0.95 else "🔴"
                print(
                    f"  {emoji} {repo_name:<28} Ψ = {psi:.6f} "
                    f"→ {node_status[repo_name]['resonance']} ({info.get('role')})"
                )
        except Exception as exc:
            total_psi.append(0.0)
            node_status[repo_name] = {
                "psi": 0.0,
                "resonance": "OFFLINE",
                "role": info.get("role"),
                "layer": info.get("layer"),
                "harmonic_factor": info.get("harmonic_factor", 1.0),
                "modo_real": False,
                "error": str(exc)[:120],
            }
            if verbose:
                print(f"  🔴 {repo_name:<28} OFFLINE — {str(exc)[:60]}")

    global_psi = sum(total_psi) / len(total_psi) if total_psi else 0.0
    now_utc = datetime.now(timezone.utc).isoformat()

    if verbose:
        print("\n" + "═" * 90)
        print(f"Ψ_GLOBAL_ECOSISTEMA = {global_psi:.8f} | UTC: {now_utc}")

    if global_psi >= GLOBAL_THRESHOLD:
        _SATURATION_STREAK += 1
    else:
        _SATURATION_STREAK = 0

    response = {
        "status": "DRIFTING",
        "global_psi": round(global_psi, 8),
        "nodes": node_status,
        "saturation_streak": _SATURATION_STREAK,
        "threshold": GLOBAL_THRESHOLD,
        "required_cycles": SATURATION_CYCLES,
        "timestamp": now_utc,
    }

    if _SATURATION_STREAK >= SATURATION_CYCLES:
        emission = append_emission(global_psi, node_status)
        response["status"] = "RESONANCIA_SATURADA"
        response["emission"] = emission
        _SATURATION_STREAK = 0
        if verbose:
            print("✨ COHERENCIA TOTAL LOGRADA — RESONANCIA INSTANTÁNEA ACTIVA")
            print("   Emisión πCODE-888 registrada en el ledger.")

    return response


if __name__ == "__main__":
    while True:
        monitor_global_resonance()
        time.sleep(SYNC_INTERVAL_SECONDS)
