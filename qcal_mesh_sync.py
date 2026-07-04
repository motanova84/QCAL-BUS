"""
qcal_mesh_sync.py
=================
Motor principal de la malla QCAL-EPR.

Modos de ejecución:
  1. Loop continuo (por defecto o con --loop):
       python qcal_mesh_sync.py
       python qcal_mesh_sync.py --loop
       python qcal_mesh_sync.py --loop --csv ledger/emissions_log.csv

  2. Servidor MCP (protocolo JSON-RPC 2.0 por stdin/stdout):
       python qcal_mesh_sync.py --mcp-server

     Herramientas MCP expuestas:
       - get_mesh_state    → monitor_global_resonance()
       - get_node_catalog  → catálogo completo de nodos
       - get_emissions_log → últimas N entradas del ledger
"""

import argparse
import csv
import json
import logging
import os
import sys
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
LEDGER_TAIL_DEFAULT = int(os.getenv("QCAL_LEDGER_TAIL", "50"))

_STATE = {"saturation_streak": 0}
_STREAK_LOCK = threading.Lock()
OFFLINE_ERROR_TRUNCATE = 120


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def load_catalog() -> dict:
    if not CATALOG_PATH.exists():
        logger.error("Fisura detectada: No se encuentra el catálogo en %s", CATALOG_PATH)
        raise FileNotFoundError(f"Catálogo no encontrado: {CATALOG_PATH}")
    try:
        with CATALOG_PATH.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as exc:
        logger.error("Error de Coherencia: JSON mal formado en el catálogo: %s", exc)
        raise


def ensure_ledger() -> None:
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


def calculate_emission(global_psi: float, nodes: dict) -> float:
    if not nodes:
        return 0.0
    harmonic_sum = sum(info.get("harmonic_factor", 1.0) for info in nodes.values())
    harmonic_avg = harmonic_sum / len(nodes)
    return round(EMISSION_BASE * global_psi * harmonic_avg, 6)


def append_emission(global_psi: float, nodes: dict) -> dict:
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


def read_emissions_log(tail: int = LEDGER_TAIL_DEFAULT) -> list[dict]:
    """Retorna las últimas *tail* entradas del ledger como lista de dicts."""
    ensure_ledger()
    rows = []
    with LEDGER_PATH.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
    return rows[-tail:] if tail > 0 else rows


def validate_catalog_integrity(catalog: dict | None = None) -> dict:
    """Valida integridad estructural y operativa mínima del catálogo."""
    catalog = catalog or load_catalog()
    meta = catalog.get("meta", {})
    nodes = catalog.get("nodes", {})
    issues = []

    if not isinstance(nodes, dict):
        issues.append("nodes debe ser un objeto JSON")
        nodes = {}

    total_nodes = len(nodes)
    expected_nodes = meta.get("total_nodes")
    if expected_nodes is not None and expected_nodes != total_nodes:
        issues.append(
            f"meta.total_nodes={expected_nodes} no coincide con nodes={total_nodes}"
        )

    missing_endpoints = sorted(
        node_name
        for node_name, info in nodes.items()
        if not info.get("mcp_endpoint")
    )
    if missing_endpoints:
        issues.append(f"Nodos sin mcp_endpoint: {', '.join(missing_endpoints)}")

    noesis_endpoint = nodes.get("noesis88", {}).get("mcp_endpoint")
    if noesis_endpoint != "http://localhost:8513/jsonrpc":
        issues.append("noesis88 debe apuntar a http://localhost:8513/jsonrpc")

    return {
        "ok": not issues,
        "issues": issues,
        "total_nodes": total_nodes,
        "expected_nodes": expected_nodes,
        "missing_endpoints": missing_endpoints,
        "catalog_path": str(CATALOG_PATH),
    }


def run_preflight_checks() -> dict:
    """Ejecuta validaciones pre-operacionales para FASE 4."""
    catalog = load_catalog()
    catalog_report = validate_catalog_integrity(catalog)
    ensure_ledger()
    mesh_state = sync_mesh_with_real_sources()
    nodes = mesh_state.get("nodes", {}) if isinstance(mesh_state.get("nodes", {}), dict) else {}
    offline_nodes = sorted(
        node_name
        for node_name, info in nodes.items()
        if info.get("resonance") == "OFFLINE"
    )

    return {
        "catalog": catalog_report,
        "ledger": {
            "ok": LEDGER_PATH.exists(),
            "path": str(LEDGER_PATH),
        },
        "mcp": {
            "ok": True,
            "bridge_path": "/api/mcp",
            "tools": sorted(_MCP_TOOLS),
        },
        "health": {
            "ok": catalog_report["ok"],
            "total_nodes": len(nodes),
            "offline_nodes": offline_nodes,
            "online_nodes": max(0, len(nodes) - len(offline_nodes)),
        },
        "mesh_state": mesh_state,
    }


def run_monitor_loop(
    iterations: int | None = None,
    interval_seconds: int | None = None,
    verbose: bool = True,
) -> None:
    """Ejecuta el monitor de resonancia en loop continuo o acotado."""
    interval = SYNC_INTERVAL_SECONDS if interval_seconds is None else interval_seconds
    cycle = 0

    while iterations is None or cycle < iterations:
        try:
            monitor_global_resonance(verbose=verbose)
        except Exception as exc:  # pragma: no cover
            print(f"⚠️ Error en ciclo de sincronía: {exc}")

        cycle += 1
        if iterations is not None and cycle >= iterations:
            break
        time.sleep(interval)


# ---------------------------------------------------------------------------
# Main monitor
# ---------------------------------------------------------------------------

def monitor_global_resonance(verbose: bool = True) -> dict:
    catalog = load_catalog()
    meta = catalog.get("meta", {})
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
                    f"  {emoji} {repo_name:<30} Ψ = {psi:.6f} "
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
                print(f"  🔴 {repo_name:<30} OFFLINE — {str(exc)[:OFFLINE_ERROR_TRUNCATE]}")

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
        "coherence": meta.get("coherence", "C = 244.36"),
        "precision": meta.get("precision", "99.78%"),
        "total_nodes": node_count,
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


# ---------------------------------------------------------------------------
# MCP JSON-RPC 2.0 server (stdin/stdout)
# ---------------------------------------------------------------------------

_MCP_TOOLS = {
    "get_mesh_state": {
        "description": "Retorna el estado actual de la malla QCAL-EPR incluyendo Ψ_GLOBAL y todos los nodos.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    "get_node_catalog": {
        "description": "Retorna el catálogo completo de nodos MCP registrados en la malla QCAL.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    "get_emissions_log": {
        "description": "Retorna las últimas entradas del ledger de emisiones πCODE-888.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "tail": {
                    "type": "integer",
                    "description": "Número de entradas a retornar (por defecto 50).",
                    "default": 50,
                }
            },
        },
    },
}


def _mcp_list_tools() -> dict:
    return {"tools": [{"name": k, **v} for k, v in _MCP_TOOLS.items()]}


def _mcp_call_tool(name: str, arguments: dict) -> dict:
    if name == "get_mesh_state":
        result = monitor_global_resonance(verbose=False)
        return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]}

    if name == "get_node_catalog":
        catalog = load_catalog()
        return {"content": [{"type": "text", "text": json.dumps(catalog, ensure_ascii=False)}]}

    if name == "get_emissions_log":
        tail = int(arguments.get("tail", LEDGER_TAIL_DEFAULT))
        entries = read_emissions_log(tail=tail)
        return {"content": [{"type": "text", "text": json.dumps(entries, ensure_ascii=False)}]}

    return {"isError": True, "content": [{"type": "text", "text": f"Herramienta desconocida: {name!r}"}]}


def _mcp_handle(request: dict):
    """Procesa una solicitud JSON-RPC 2.0 y retorna la respuesta (o None para notificaciones)."""
    if not isinstance(request, dict):
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Solicitud inválida"}}

    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if not isinstance(method, str) or not method:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": "Campo 'method' faltante o inválido"}}

    def ok(result: dict) -> dict:
        return {"jsonrpc": "2.0", "id": req_id, "result": result}

    def err(code: int, message: str) -> dict:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}

    if method == "initialize":
        return ok({
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "qcal-mesh-bus", "version": "2.0.0"},
        })

    if method == "tools/list":
        return ok(_mcp_list_tools())

    if method == "tools/call":
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        return ok(_mcp_call_tool(tool_name, arguments))

    # Notificaciones (sin id) — no requieren respuesta
    if req_id is None:
        return None

    return err(-32601, f"Método no encontrado: {method!r}")


def run_mcp_server() -> None:
    """Bucle principal del servidor MCP (stdin/stdout, JSON-RPC 2.0)."""
    for raw_line in sys.stdin:
        raw_line = raw_line.strip()
        if not raw_line:
            continue
        try:
            request = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}}
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
            continue

        response = _mcp_handle(request)
        if response is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            sys.stdout.flush()


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qcal_mesh_sync",
        description="Motor de sincronía de la malla QCAL-EPR",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--mcp-server",
        action="store_true",
        help="Inicia el servidor MCP JSON-RPC 2.0 en stdin/stdout.",
    )
    mode.add_argument(
        "--loop",
        action="store_true",
        help="Corre el monitor en loop continuo (comportamiento por defecto cuando no se pasa ningún flag).",
    )
    parser.add_argument(
        "--csv",
        metavar="PATH",
        default=None,
        help="Ruta al archivo CSV del ledger de emisiones (sobreescribe LEDGER_PATH).",
    )
    parser.add_argument(
        "--interval",
        metavar="SECONDS",
        type=int,
        default=None,
        help="Intervalo entre ciclos en segundos (sobreescribe QCAL_SYNC_INTERVAL_SECONDS).",
    )
    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    args = _build_arg_parser().parse_args()

    if args.csv:
        LEDGER_PATH = Path(args.csv).resolve()

    if args.interval is not None:
        SYNC_INTERVAL_SECONDS = args.interval

    if args.mcp_server:
        run_mcp_server()
    else:
        # --loop or no flag → continuous monitoring loop
        run_monitor_loop(interval_seconds=SYNC_INTERVAL_SECONDS)
def sync_mesh_with_real_sources():
    """
    Sincroniza la malla completa con manejo de errores robusto y
    detección dinámica de mcp_network. Punto de entrada público del orquestador.
    """
    try:
        return monitor_global_resonance(verbose=False)
    except FileNotFoundError:
        return {"global_psi": 0.0, "status": "CATALOG_NOT_FOUND"}
    except json.JSONDecodeError:
        return {"global_psi": 0.0, "status": "JSON_MALFORMED"}
