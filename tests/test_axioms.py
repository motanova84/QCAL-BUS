#!/usr/bin/env python3
"""VALIDACIÓN DE AXIOMAS QCAL-BUS - Versión ∞³ 141.7001 Hz"""

import unittest
import math
from typing import List, Tuple

F0 = 141.7001
NUM_NODOS = 33
UMBRAL_SATURACION = 0.999999
CICLOS_REQUERIDOS = 3
EPSILON = 1e-12

class EstadoSistema:
    def __init__(self, nodos: List[int], fases: List[float], coherencias: List[float]):
        assert len(nodos) == len(fases) == len(coherencias) == NUM_NODOS
        self.nodos = nodos
        self.fases = fases
        self.coherencias = coherencias
    
    @property
    def coherencia_global(self) -> float:
        return sum(self.coherencias) / len(self.coherencias)
    
    @property
    def frecuencia_fundamental(self) -> float:
        return F0

class Historial:
    def __init__(self):
        self.registros: List[Tuple[float, float]] = []
    
    def agregar(self, tiempo: float, coherencia: float):
        self.registros.append((tiempo, coherencia))
    
    def verificar_emision(self) -> bool:
        if len(self.registros) < CICLOS_REQUERIDOS:
            return False
        ultimas = [c for _, c in self.registros[-CICLOS_REQUERIDOS:]]
        return all(c >= UMBRAL_SATURACION for c in ultimas)

def calcular_celeridad(f_ini, f_fin, p_ini, p_fin):
    delta_fase = abs(f_fin - f_ini)
    delta_psi = abs(p_fin - p_ini) + EPSILON
    return (delta_fase / delta_psi) * F0

class TestAxiomasQCAL(unittest.TestCase):
    def setUp(self):
        self.nodos_base = list(range(NUM_NODOS))
        self.fases_base = [0.0] * NUM_NODOS
        self.coherencias_base = [0.5] * NUM_NODOS
        self.estado_base = EstadoSistema(
            self.nodos_base, self.fases_base, self.coherencias_base
        )
    
    def test_axioma1_frecuencia_constante(self):
        self.assertEqual(self.estado_base.frecuencia_fundamental, F0)
    
    def test_axioma2_coherencia_acotada(self):
        psi = self.estado_base.coherencia_global
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)
    
    def test_axioma3_emision(self):
        historial = Historial()
        for i in range(CICLOS_REQUERIDOS):
            historial.agregar(i, UMBRAL_SATURACION)
        self.assertTrue(historial.verificar_emision())
    
    def test_axioma4_num_nodos(self):
        self.assertEqual(len(self.estado_base.nodos), NUM_NODOS)
    
    def test_axioma5_celeridad(self):
        nu = calcular_celeridad(0, 1, 0.5, 0.8)
        self.assertGreater(nu, 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)