#!/usr/bin/env python3
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import qcal_mesh_sync as bus  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("QCAL-RESONANCE")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="activate_qcal_resonance",
        description="FASE 4 — activación operacional y monitoreo continuo de Ψ_GLOBAL.",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=bus.SYNC_INTERVAL_SECONDS,
        help="Intervalo entre ciclos de monitoreo en segundos.",
    )
    parser.add_argument(
        "--cycles",
        type=int,
        default=None,
        help="Número de ciclos a ejecutar antes de salir. Por defecto corre indefinidamente.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Reduce la salida del monitor y conserva solo logging estructurado.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    preflight = bus.run_preflight_checks()
    mesh_state = preflight["mesh_state"]
    health = preflight["health"]
    catalog = preflight["catalog"]

    logger.info("FASE 4 — activación operacional iniciada")
    logger.info("Catálogo: %s (%s nodos)", catalog["catalog_path"], catalog["total_nodes"])
    logger.info("Ledger: %s", preflight["ledger"]["path"])
    logger.info("MCP Bridge HTTP: %s", preflight["mcp"]["bridge_path"])
    logger.info(
        "Health check inicial: %s/%s nodos online | Ψ_GLOBAL=%.8f | status=%s",
        health["online_nodes"],
        health["total_nodes"],
        mesh_state.get("global_psi", 0.0),
        mesh_state.get("status", "UNKNOWN"),
    )

    if catalog["issues"]:
        for issue in catalog["issues"]:
            logger.warning("Preflight: %s", issue)

    bus.run_monitor_loop(
        iterations=args.cycles,
        interval_seconds=args.interval,
        verbose=not args.quiet,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
