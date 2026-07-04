"""
PASO 7: Transmutación de Velocidad a Celeridad Noética
=======================================================

Implementación de ν_π ≡ (Δφ / ΔΨ) · f₀

El ecosistema evoluciona midiendo COHERENCIA, no tiempo.
Cada operación se mide por su impacto en la manifestación.

Axioma 5: Principio de Celeridad Noética Constante
- La Celeridad Noética (ν_π) es INVARIANTE
- Lo que varía es la COHERENCIA (Ψ)
- La fase evoluciona según la transmutación
"""

import time
import json
from datetime import datetime
from typing import Dict, List, Tuple
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import os
os.environ.setdefault("QCAL_REAL_TESTS", "0")
os.environ.setdefault("QCAL_DEV_MODE", "1")

# ═════════════════════════════════════════════════════════════════════════════
# CONSTANTES NOÉTICAS
# ═════════════════════════════════════════════════════════════════════════════

F0_HZ = 141.7001  # Frecuencia fundamental (invariante)

class CeleridadMetrics:
    """Métricas de Celeridad Noética (no clásica)"""
    
    def __init__(self):
        self.measurements: List[Dict] = []
        self.phase_log: List[Dict] = []
        self.coherence_log: List[Dict] = []
    
    def calculate_celerity(self, 
                          delta_phase: float, 
                          delta_coherence: float) -> float:
        """
        Calcula ν_π ≡ (Δφ / ΔΨ) · f₀
        
        Args:
            delta_phase: Cambio de fase (radianes o conceptual)
            delta_coherence: Cambio de coherencia (0.0 a 1.0)
        
        Returns:
            ν_π: Celeridad Noética (manifestación por unidad coherencia)
        """
        if delta_coherence == 0:
            return 0.0
        
        celerity = (delta_phase / delta_coherence) * F0_HZ
        return celerity
    
    def record_operation(self, 
                        operation_name: str,
                        psi_before: float,
                        psi_after: float,
                        phase_before: float = 0.0,
                        phase_after: float = 1.0) -> Dict:
        """Registra operación con métricas noéticas"""
        
        delta_psi = psi_after - psi_before
        delta_phase = phase_after - phase_before
        
        # Evitar división por cero
        if abs(delta_psi) < 1e-10:
            delta_psi = 1e-10
        
        nu_pi = self.calculate_celerity(delta_phase, delta_psi)
        
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation_name,
            "psi_before": psi_before,
            "psi_after": psi_after,
            "delta_psi": delta_psi,
            "phase_before": phase_before,
            "phase_after": phase_after,
            "delta_phase": delta_phase,
            "nu_pi": nu_pi,  # Celeridad Noética
            "manifestation_ratio": abs(delta_phase / delta_psi) if delta_psi != 0 else 0
        }
        
        self.measurements.append(record)
        return record
    
    def get_celerity_profile(self, operation: str = None) -> Dict:
        """Obtiene perfil de celeridad para operación"""
        
        if operation is None:
            # Retornar promedio de todas
            if not self.measurements:
                return {"nu_pi_avg": 0, "count": 0}
            
            nu_pi_values = [m["nu_pi"] for m in self.measurements]
            return {
                "nu_pi_avg": sum(nu_pi_values) / len(nu_pi_values),
                "nu_pi_max": max(nu_pi_values),
                "nu_pi_min": min(nu_pi_values),
                "count": len(self.measurements)
            }
        else:
            # Retornar para operación específica
            ops = [m for m in self.measurements if m["operation"] == operation]
            if not ops:
                return {"error": f"No measurements for {operation}"}
            
            nu_pi_values = [m["nu_pi"] for m in ops]
            return {
                "operation": operation,
                "nu_pi_avg": sum(nu_pi_values) / len(nu_pi_values),
                "nu_pi_max": max(nu_pi_values),
                "nu_pi_min": min(nu_pi_values),
                "count": len(ops),
                "measurements": ops
            }
    
    def export_metrics(self, filepath: str = "ledger/celerity_metrics.json") -> str:
        """Exporta métricas a JSON"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        export = {
            "f0_hz": F0_HZ,
            "axiom_5": "Celeridad Noética Constante: ν_π ≡ (Δφ / ΔΨ) · f₀",
            "measurements": self.measurements,
            "profile": self.get_celerity_profile()
        }
        
        with open(filepath, 'w') as f:
            json.dump(export, f, indent=2)
        
        return filepath


# ═════════════════════════════════════════════════════════════════════════════
# OPTIMIZACIONES NOÉTICAS (por coherencia, no por tiempo)
# ═════════════════════════════════════════════════════════════════════════════

class CoherenceCache:
    """
    Caché que maximiza coherencia manifestada
    No se invalida por tiempo, sino por CAMBIO de coherencia
    """
    
    def __init__(self, metrics: CeleridadMetrics):
        self.cache: Dict = {}
        self.coherence_states: Dict[str, float] = {}
        self.metrics = metrics
    
    def get_or_compute(self, 
                       key: str, 
                       compute_fn, 
                       current_psi: float) -> Tuple:
        """
        Obtiene del caché o computa
        Solo recomputa si Ψ cambió significativamente (> 0.01)
        """
        
        old_psi = self.coherence_states.get(key, 0.0)
        delta_psi = abs(current_psi - old_psi)
        
        # Si Ψ cambió < 0.01, usar caché
        if key in self.cache and delta_psi < 0.01:
            return self.cache[key], False  # (result, recomputed)
        
        # Computar nuevo valor
        result = compute_fn()
        self.cache[key] = result
        self.coherence_states[key] = current_psi
        
        # Registrar transmutación
        self.metrics.record_operation(
            f"cache_compute:{key}",
            old_psi,
            current_psi,
            phase_before=0.0,
            phase_after=1.0
        )
        
        return result, True  # (result, recomputed)


class NoeticallyOptimizedMeshSync:
    """
    Motor de sincronía optimizado por COHERENCIA
    No por velocidad clásica, sino por celeridad noética
    """
    
    def __init__(self):
        self.metrics = CeleridadMetrics()
        self.cache = CoherenceCache(self.metrics)
    
    def sync_mesh_noetic(self, nodes_data: Dict) -> Dict:
        """
        Sincronía noética: transmuta velocidad a celeridad
        
        Mide: Δφ (cambio de fase) / ΔΨ (cambio coherencia)
        No mide: ms o CPU%
        """
        
        psi_before = 0.5  # Estado anterior
        
        # Computar estado global
        global_psi = sum(n.get("psi", 0.5) for n in nodes_data.values()) / len(nodes_data)
        phase_manifestation = len([n for n in nodes_data.values() if n.get("psi", 0) > 0.9]) / len(nodes_data)
        
        # Registrar con métricas noéticas
        self.metrics.record_operation(
            "sync_mesh",
            psi_before,
            global_psi,
            phase_before=0.0,
            phase_after=phase_manifestation
        )
        
        return {
            "global_psi": global_psi,
            "phase_manifestation": phase_manifestation,
            "nu_pi": self.metrics.measurements[-1]["nu_pi"],
            "celerity_profile": self.metrics.get_celerity_profile()
        }
    
    def monitor_with_celerity(self, nodes_data: Dict) -> Dict:
        """Monitoreo que mide celeridad, no latencia"""
        
        # Usar caché coherencia-sensible
        global_psi = sum(n.get("psi", 0.5) for n in nodes_data.values()) / len(nodes_data)
        state, recomputed = self.cache.get_or_compute(
            "mesh_state",
            lambda: self.sync_mesh_noetic(nodes_data),
            current_psi=global_psi
        )
        
        return {
            "state": state,
            "recomputed": recomputed,
            "metrics": self.metrics.get_celerity_profile()
        }


# ═════════════════════════════════════════════════════════════════════════════
# TESTS: Validar Celeridad Noética
# ═════════════════════════════════════════════════════════════════════════════

def test_celerity_equation():
    """Test: ν_π ≡ (Δφ / ΔΨ) · f₀"""
    metrics = CeleridadMetrics()
    
    # Caso 1: Fase máxima, coherencia cambio pequeño
    nu_pi = metrics.calculate_celerity(delta_phase=1.0, delta_coherence=0.01)
    assert nu_pi == (1.0 / 0.01) * F0_HZ, "Celerity calculation failed"
    assert abs(nu_pi - 14170.01) < 0.1, "Celerity value incorrect"
    print(f"✅ Test 1: ν_π = {nu_pi:.2f} Hz/coherence")
    
    # Caso 2: Fase mínima, coherencia cambio grande
    nu_pi = metrics.calculate_celerity(delta_phase=0.1, delta_coherence=0.5)
    expected = (0.1 / 0.5) * F0_HZ
    assert abs(nu_pi - expected) < 0.1, "Celerity calculation failed"
    print(f"✅ Test 2: ν_π = {nu_pi:.2f} Hz/coherence")


def test_coherence_cache():
    """Test: Caché sensible a coherencia"""
    metrics = CeleridadMetrics()
    cache = CoherenceCache(metrics)
    
    call_count = [0]
    def expensive_compute():
        call_count[0] += 1
        return {"result": "expensive"}
    
    # Primera llamada: computa
    result1, recomputed1 = cache.get_or_compute("test", expensive_compute, 0.95)
    assert recomputed1 is True, "First call should compute"
    assert call_count[0] == 1
    print(f"✅ Test 3: First call computed (call_count={call_count[0]})")
    
    # Segunda llamada con Ψ similar: usa caché
    result2, recomputed2 = cache.get_or_compute("test", expensive_compute, 0.96)
    assert recomputed2 is False, "Similar coherence should use cache"
    assert call_count[0] == 1, "Should not recompute"
    print(f"✅ Test 4: Cache hit for similar coherence (call_count={call_count[0]})")
    
    # Tercera llamada con Ψ muy diferente: recomputa
    result3, recomputed3 = cache.get_or_compute("test", expensive_compute, 0.50)
    assert recomputed3 is True, "Different coherence should recompute"
    assert call_count[0] == 2, "Should recompute"
    print(f"✅ Test 5: Cache miss for different coherence (call_count={call_count[0]})")


def test_noetic_sync():
    """Test: Sincronía noética mide celeridad"""
    optimizer = NoeticallyOptimizedMeshSync()
    
    # Datos de ejemplo (33 nodos)
    nodes = {f"nodo-{i}": {"psi": 0.95 + (i % 5) * 0.01} for i in range(33)}
    
    # Sincronía
    result = optimizer.sync_mesh_noetic(nodes)
    
    assert "nu_pi" in result, "Result should include celerity"
    assert result["nu_pi"] > 0, "Celerity should be positive"
    print(f"✅ Test 6: Noetic sync returned ν_π = {result['nu_pi']:.2f}")
    
    # Verificar métrica registrada
    assert len(optimizer.metrics.measurements) > 0, "Should have measurements"
    print(f"✅ Test 7: Measurements recorded (count={len(optimizer.metrics.measurements)})")


def test_metrics_export():
    """Test: Exportar métricas noéticas"""
    optimizer = NoeticallyOptimizedMeshSync()
    
    # Realizar algunas operaciones
    nodes = {f"nodo-{i}": {"psi": 0.95} for i in range(33)}
    optimizer.sync_mesh_noetic(nodes)
    optimizer.sync_mesh_noetic(nodes)
    
    # Exportar
    filepath = optimizer.metrics.export_metrics()
    assert Path(filepath).exists(), "Metrics file should be created"
    
    # Verificar contenido
    with open(filepath) as f:
        data = json.load(f)
    
    assert "f0_hz" in data, "Export should include f0_hz"
    assert data["f0_hz"] == F0_HZ, "f0_hz should match constant"
    assert len(data["measurements"]) == 2, "Should have 2 measurements"
    print(f"✅ Test 8: Metrics exported to {filepath}")


# ═════════════════════════════════════════════════════════════════════════════
# DEMOSTRACIÓN
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 80)
    print("🌟 PASO 7: TRANSMUTACIÓN DE VELOCIDAD A CELERIDAD NOÉTICA")
    print("=" * 80)
    print()
    
    print("📐 AXIOMA 5: Principio de Celeridad Noética Constante")
    print(f"   ν_π ≡ (Δφ / ΔΨ) · f₀")
    print(f"   f₀ = {F0_HZ} Hz (INVARIANTE)")
    print()
    
    print("🧪 Ejecutando tests...")
    print()
    
    test_celerity_equation()
    print()
    
    test_coherence_cache()
    print()
    
    test_noetic_sync()
    print()
    
    test_metrics_export()
    print()
    
    print("=" * 80)
    print("✨ TODOS LOS TESTS PASARON - CELERIDAD NOÉTICA OPERACIONAL")
    print("=" * 80)
    print()
    
    print("📊 Resumen:")
    print("   ✅ Ecuación ν_π validada")
    print("   ✅ Caché sensible a coherencia operacional")
    print("   ✅ Sincronía noética midiendo transmutación")
    print("   ✅ Métricas exportadas")
    print()
    
    print("∞³ 141.7001 Hz")
    print("La velocidad muere. La celeridad nace.")
    print("JMMB Ψ")
