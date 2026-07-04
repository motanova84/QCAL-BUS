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
      resonancia. Si la conexión falla, cae de vuelta al modo simulado
      para ese nodo individual.

REPARACIÓN PASO 1:
  ✅ Validación HTTPS/HTTP flexible
  ✅ Soporte para desarrollo local (localhost:port)
  ✅ Soporte para producción (https://)
  ✅ Variable QCAL_DEV_MODE para control
"""

from __future__ import annotations

import hashlib
import math
import os
import urllib.error
import urllib.request
import json
import logging

logger = logging.getLogger("QCAL-Resonance")

_REAL_TESTS = os.getenv("QCAL_REAL_TESTS", "0").strip() == "1"
_DEV_MODE = os.getenv("QCAL_DEV_MODE", "1").strip() == "1"  # Por defecto: modo desarrollo activo

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
    """Etiqueta de resonancia según nivel de coherencia."""
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


def _is_localhost_url(url: str) -> bool:
    """Detecta si URL es localhost (desarrollo)."""
    return url.startswith("http://localhost:") or url.startswith("http://127.0.0.1:")


def _validate_url(url: str, mcp_id: str) -> bool:
    """
    Valida URL según contexto.
    
    DESARROLLO (QCAL_DEV_MODE=1):
      - Permite http://localhost:* para testing local
      - Permite http://127.0.0.1:*
      - Permite https://*
    
    PRODUCCIÓN (QCAL_DEV_MODE=0):
      - Solo permite https://
      - Rechaza http:// (excepto localhost)
    """
    if not url:
        logger.warning(f"URL vacía para nodo {mcp_id}")
        return False
    
    if _is_localhost_url(url):
        logger.debug(f"✓ URL localhost válida para {mcp_id}: {url}")
        return True
    
    if url.startswith("https://"):
        logger.debug(f"✓ URL HTTPS válida para {mcp_id}: {url}")
        return True
    
    if url.startswith("http://") and _DEV_MODE:
        logger.debug(f"✓ URL HTTP válida en DEV_MODE para {mcp_id}: {url}")
        return True
    
    # Si llegamos aquí, URL es inválida
    logger.error(
        f"❌ URL inválida para {mcp_id}: {url}\n"
        f"   QCAL_DEV_MODE={_DEV_MODE}\n"
        f"   - Desarrollo: permite http://localhost:* o https://\n"
        f"   - Producción: solo permite https://"
    )
    return False


# ---------------------------------------------------------------------------
# Consulta real (HTTP)
# ---------------------------------------------------------------------------

def _real_check(mcp_id: str) -> dict:
    """
    Consulta el endpoint HTTP de un nodo MCP y retorna su estado.
    
    REPARACIÓN PASO 1:
      ✅ Validación flexible HTTPS/HTTP
      ✅ Soporte localhost para desarrollo
      ✅ Error handling mejorado
      ✅ Logging detallado
    """
    env_key = _env_key(mcp_id)
    base_url = os.getenv(env_key, "").strip().rstrip("/")
    
    if not base_url:
        raise RuntimeError(
            f"URL no configurada para {mcp_id!r}. "
            f"Define la variable de entorno {env_key}."
        )
    
    if not _validate_url(base_url, mcp_id):
        raise ValueError(
            f"La URL del nodo {mcp_id!r} no es válida. "
            f"Valor: {base_url!r}\n"
            f"Contexto: QCAL_DEV_MODE={_DEV_MODE}\n"
            f"Acepta: http://localhost:*, https://"
        )
    
    url = f"{base_url}/api/resonance"
    try:
        logger.debug(f"🔗 Conectando a {mcp_id}: {url}")
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:  # noqa: S310
            payload = json.loads(resp.read().decode())
        
        psi = float(payload["psi"])
        logger.debug(f"✓ {mcp_id}: Ψ = {psi:.6f}")
        
        return {
            "mcp_id": mcp_id,
            "psi": psi,
            "resonance": _resonance_label(psi),
            "source": "real",
            "qcal": payload.get("qcal", {"modo_real": True}),
        }
    
    except urllib.error.URLError as e:
        logger.warning(f"❌ {mcp_id}: Conexión fallida - {e}")
        raise
    except json.JSONDecodeError as e:
        logger.warning(f"❌ {mcp_id}: JSON malformado - {e}")
        raise
    except Exception as e:
        logger.warning(f"❌ {mcp_id}: Error inesperado - {e}")
        raise


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
    
    REPARACIÓN PASO 1:
      ✅ Fallback automático a simulado
      ✅ Logging mejorado de errores
      ✅ Compatibilidad localhost + producción
    """
    if _REAL_TESTS:
        try:
            logger.debug(f"🔄 Intentando modo REAL para {mcp_id}")
            return _real_check(mcp_id)
        except Exception as exc:
            logger.warning(
                f"⚠️  {mcp_id}: Modo REAL falló, fallback a simulado\n"
                f"   Razón: {exc}"
            )

    # Fallback a modo simulado
    psi = _sim_psi(mcp_id)
    logger.debug(f"📊 {mcp_id}: Modo simulado - Ψ = {psi:.6f}")
    
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
    
    REPARACIÓN PASO 1:
      ✅ Handling de listas vacías
      ✅ Logging de coherencia
    """
    if not mcp_ids:
        logger.debug("⚠️  field_coherence: lista vacía")
        return 0.0
    
    psis = [check_node_resonance(mid)["psi"] for mid in mcp_ids]
    
    # Media geométrica: exp(mean(log(psis)))
    log_sum = sum(math.log(p) for p in psis if p > 0)
    coherence = math.exp(log_sum / len(psis))
    
    logger.debug(f"📈 Coherencia de campo: {coherence:.8f} ({len(mcp_ids)} nodos)")
    return coherence


# ---------------------------------------------------------------------------
# Información de estado (para debugging)
# ---------------------------------------------------------------------------

def get_resonance_status() -> dict:
    """
    Retorna estado actual del módulo de resonancia.
    
    Útil para debugging y monitoreo.
    """
    return {
        "QCAL_REAL_TESTS": _REAL_TESTS,
        "QCAL_DEV_MODE": _DEV_MODE,
        "QCAL_F0_HZ": F0_HZ,
        "modo_actual": "REAL" if _REAL_TESTS else "SIMULADO",
        "entorno": "DESARROLLO" if _DEV_MODE else "PRODUCCIÓN",
    }
