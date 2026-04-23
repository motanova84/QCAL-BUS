"""
mcp_network.resonance
=====================
Módulo de resonancia para la malla QCAL-EPR.

Modos de operación:
  - SIMULADO (por defecto / QCAL_REAL_TESTS=0):
      Genera valores Ψ deterministas basados en el mcp_id para pruebas
      reproducibles sin dependencias externas.
  - REAL (QCAL_REAL_TESTS=1):
      Intenta conectar al endpoint HTTP configurado para cada nodo MCP
      (variable de entorno QCAL_NODE_<MCP_ID>_URL) y leer su estado de
      resonancia.  Si la conexión falla, cae de vuelta al modo simulado
      para ese nodo individual.
"""

from __future__ import annotations

import hashlib
import math
import os
import urllib.error
import urllib.request
import json

_REAL_TESTS = os.getenv("QCAL_REAL_TESTS", "0").strip() == "1"

# Frecuencia de referencia del ecosistema QCAL
F0_HZ = float(os.getenv("QCAL_F0_HZ", "141.7001"))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sim_psi(mcp_id: str) -> float:
    """Genera un valor Ψ simulado determinista en [0.95, 1.0] para el mcp_id."""
    digest = int(hashlib.sha256(mcp_id.encode()).hexdigest(), 16)
    # Mapea el hash a [0.95, 1.0]
    return 0.95 + (digest % 1_000_000) / 20_000_000


def _resonance_label(psi: float) -> str:
    if psi >= 0.999999:
        return "COHERENCIA_TOTAL"
    if psi >= 0.99:
        return "RESONANCIA_ALTA"
    if psi >= 0.95:
        return "RESONANCIA_MEDIA"
    return "DERIVANDO"


def _env_key(mcp_id: str) -> str:
    """Convierte un mcp_id en nombre de variable de entorno seguro."""
    return "QCAL_NODE_" + mcp_id.upper().replace("-", "_") + "_URL"


# ---------------------------------------------------------------------------
# Consulta real (HTTP)
# ---------------------------------------------------------------------------

def _real_check(mcp_id: str) -> dict:
    """Consulta el endpoint HTTP de un nodo MCP y retorna su estado."""
    env_key = _env_key(mcp_id)
    base_url = os.getenv(env_key, "").strip().rstrip("/")
    if not base_url:
        raise RuntimeError(
            f"URL no configurada para {mcp_id!r}. "
            f"Define la variable de entorno {env_key}."
        )
    if not base_url.startswith("https://"):
        raise ValueError(
            f"La URL del nodo {mcp_id!r} debe usar HTTPS. "
            f"Valor actual: {base_url!r}"
        )
    url = f"{base_url}/api/resonance"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as resp:  # noqa: S310
        payload = json.loads(resp.read().decode())
    psi = float(payload["psi"])
    return {
        "mcp_id": mcp_id,
        "psi": psi,
        "resonance": _resonance_label(psi),
        "source": "real",
        "qcal": payload.get("qcal", {"modo_real": True}),
    }


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

def check_node_resonance(mcp_id: str) -> dict:
    """
    Retorna el estado de resonancia del nodo identificado por *mcp_id*.

    Retorna un dict con al menos las claves:
      - ``psi``       (float [0, 1])
      - ``resonance`` (str)
      - ``qcal``      (dict con ``modo_real``: bool)
    """
    if _REAL_TESTS:
        try:
            return _real_check(mcp_id)
        except Exception as exc:
            import sys as _sys
            print(f"[QCAL] resonance fallback para {mcp_id!r}: {exc}", file=_sys.stderr)

    psi = _sim_psi(mcp_id)
    return {
        "mcp_id": mcp_id,
        "psi": psi,
        "resonance": _resonance_label(psi),
        "source": "simulated",
        "qcal": {"modo_real": False, "f0_hz": F0_HZ},
    }


def field_coherence(mcp_ids: list[str]) -> float:
    """
    Calcula la coherencia de campo Ψ_CAMPO para una lista de nodos.

    Usa la media geométrica de los valores Ψ individuales para amplificar
    el efecto de nodos con baja resonancia (más sensible que la media aritmética).
    """
    if not mcp_ids:
        return 0.0
    psis = [check_node_resonance(mid)["psi"] for mid in mcp_ids]
    log_sum = sum(math.log(p) for p in psis if p > 0)
    return math.exp(log_sum / len(psis))
