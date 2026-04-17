import csv
import json
import logging
import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("QCAL-BUS")

try:
    import mcp_network.resonance as qcal
except ImportError:  # pragma: no cover
    logger.warning("Capa mcp_network.resonance no detectada. Operando en Modo Degradado.")
    qcal = None

ROOT_DIR = Path(__file__).resolve().parent
CATALOG_PATH = ROOT_DIR / "registry" / "NODE_CATALOG.json"
LEDGER_PATH = ROOT_DIR / "ledger" / "emissions_log.csv"

EMISSION_BASE = float(os.getenv("QCAL_EMISSION_BASE", "888"))
GLOBAL_THRESHOLD = float(os.getenv("QCAL_GLOBAL_THRESHOLD", "0.999999"))
SATURATION_CYCLES = int(os.getenv("QCAL_SATURATION_CYCLES", "3"))
SYNC_INTERVAL_SECONDS = int(os.getenv("QCAL_SYNC_INTERVAL_SECONDS", "60"))

_STATE = {"saturation_streak": 0}
_STREAK_LOCK = threading.Lock()
OFFLINE_ERROR_TRUNCATE = 120


def load_catalog():
    if not CATALOG_PATH.exists():
        logger.error("Fisura detectada: No se encuentra el catálogo en %s", CATALOG_PATH)
        raise FileNotFoundError(f"Catálogo no encontrado: {CATALOG_PATH}")
    try:
        with CATALOG_PATH.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as exc:
        logger.error("Error de Coherencia: JSON mal formado en el catálogo: %s", exc)
        raise


def ensure_ledger():
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    if LEDGER_PATH.exists():
        return
    with LEDGER_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["timestamp", "global_psi", "emission_amount", "status", "transaction_id"]
        )


def extract_node_id(node):
    """Extrae el identificador canónico con jerarquía de prioridad."""
    return node.get("id") or node.get("mcp_id") or node.get("node_id") or node.get("name") or "unknown_node"


def format_error_msg(error, length=50):
    """Truncado inteligente de errores para diagnósticos limpios."""
    msg = str(error)
    return (msg[:length] + "...") if len(msg) > length else msg


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
                "error": str(exc)[:OFFLINE_ERROR_TRUNCATE],
            }
            logger.error("Falla en llamada MCP para %s: %s", repo_name, str(exc)[:OFFLINE_ERROR_TRUNCATE])
            if verbose:
                print(f"  🔴 {repo_name:<28} OFFLINE — {str(exc)[:OFFLINE_ERROR_TRUNCATE]}")

    node_count = len(total_psi)
    global_psi = sum(total_psi) / node_count if node_count else 0.0
    now_utc = datetime.now(timezone.utc).isoformat()

    if verbose:
        print("\n" + "═" * 90)
        print(f"Ψ_GLOBAL_ECOSISTEMA = {global_psi:.8f} | UTC: {now_utc}")

    with _STREAK_LOCK:
        if global_psi >= GLOBAL_THRESHOLD:
            _STATE["saturation_streak"] += 1
        else:
            _STATE["saturation_streak"] = 0

        current_streak = _STATE["saturation_streak"]

    response = {
        "status": "DRIFTING",
        "global_psi": round(global_psi, 8),
        "nodes": node_status,
        "saturation_streak": current_streak,
        "threshold": GLOBAL_THRESHOLD,
        "required_cycles": SATURATION_CYCLES,
        "timestamp": now_utc,
    }

    if current_streak >= SATURATION_CYCLES:
        emission = append_emission(global_psi, node_status)
        response["status"] = "RESONANCIA_SATURADA"
        response["emission"] = emission
        with _STREAK_LOCK:
            _STATE["saturation_streak"] = 0
        if verbose:
            print("✨ COHERENCIA TOTAL LOGRADA — RESONANCIA INSTANTÁNEA ACTIVA")
            print("   Emisión πCODE-888 registrada en el ledger.")

    return response


def sync_mesh_with_real_sources():
    """
    Sincroniza la malla completa con manejo de errores robusto y
    detección dinámica de mcp_network. Punto de entrada público del orquestador.
    """
    try:
        return monitor_global_resonance()
    except FileNotFoundError:
        return {"global_psi": 0.0, "status": "CATALOG_NOT_FOUND"}
    except json.JSONDecodeError:
        return {"global_psi": 0.0, "status": "JSON_MALFORMED"}
    catalog = load_catalog()
    nodes_data = catalog.get("nodes", {})

    if isinstance(nodes_data, dict):
        nodes = [
            {
                "id": info.get("mcp_id", repo_name),
                "name": repo_name,
            }
            for repo_name, info in nodes_data.items()
        ]
    elif isinstance(nodes_data, list):
        nodes = nodes_data
    else:
        nodes = []

    print("🌀 Escaneando Malla QCAL-EPR...")

    total_psi = []
    node_results = []

    for node in nodes:
        node_id = extract_node_id(node)
        if node_id == "unknown_node":
            continue

        try:
            res = check_node_resonance(node_id)
            psi = float(res.get("psi", 0.0))
            modo_real = bool(res.get("qcal", {}).get("modo_real", False))
            fuente_fisica = res.get("checks", {}).get("fuente_fisica", "DESCONOCIDA")
        except Exception as exc:
            psi = 0.0
            modo_real = False
            fuente_fisica = f"OFFLINE ({format_error_msg(exc)})"

        status_icon = "💠" if modo_real else "🌐"
        print(
            f"{status_icon} Nodo: {node_id:<25} | Ψ: {psi:.6f} | Fuente: {fuente_fisica}"
        )

        total_psi.append(psi)
        node_results.append(
            {
                "id": node_id,
                "psi": round(psi, 6),
                "modo_real": modo_real,
                "fuente_fisica": fuente_fisica,
            }
        )

    node_count = len(total_psi)
    global_psi = sum(total_psi) / node_count if node_count else 0.0
    return {"global_psi": round(global_psi, 8), "nodes": node_results}


if __name__ == "__main__":
    while True:
        try:
            sync_mesh_with_real_sources()
        except Exception as exc:  # pragma: no cover
            logger.error("Error en ciclo de sincronía: %s", exc)
        time.sleep(SYNC_INTERVAL_SECONDS)
