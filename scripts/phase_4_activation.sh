#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="${1:-all}"

start_monitor() {
  python "${ROOT_DIR}/scripts/activate_qcal_resonance.py" "${@:2}" &
  MONITOR_PID=$!
}

start_dashboard() {
  python "${ROOT_DIR}/dashboard/malla_qcal_epr.py" &
  DASHBOARD_PID=$!
}

cleanup() {
  if [[ -n "${MONITOR_PID:-}" ]]; then
    kill "${MONITOR_PID}" 2>/dev/null || true
  fi
  if [[ -n "${DASHBOARD_PID:-}" ]]; then
    kill "${DASHBOARD_PID}" 2>/dev/null || true
  fi
}

case "${MODE}" in
  all)
    start_monitor "$@"
    start_dashboard
    trap cleanup EXIT
    python "${ROOT_DIR}/qcal_mesh_sync.py" --mcp-server
    ;;
  monitor)
    python "${ROOT_DIR}/scripts/activate_qcal_resonance.py" "${@:2}"
    ;;
  dashboard)
    python "${ROOT_DIR}/dashboard/malla_qcal_epr.py"
    ;;
  mcp)
    python "${ROOT_DIR}/qcal_mesh_sync.py" --mcp-server
    ;;
  validate)
    python "${ROOT_DIR}/scripts/mcp_client_test.py" "${@:2}"
    ;;
  *)
    echo "Uso: $0 [all|monitor|dashboard|mcp|validate] [args...]" >&2
    exit 1
    ;;
esac
