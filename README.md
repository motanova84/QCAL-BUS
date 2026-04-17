# QCAL-BUS (qcal-mesh-bus)

Repositorio maestro para orquestación de malla QCAL-EPR.

## Estructura

```
qcal-mesh-bus/
├── qcal_mesh_sync.py          ← Motor principal + servidor MCP JSON-RPC
├── mcp_network/
│   ├── __init__.py
│   └── resonance.py           ← Módulo de resonancia (sim/real)
├── registry/NODE_CATALOG.json ← 33 nodos registrados en todas las capas
├── dashboard/malla_qcal_epr.py← Dashboard HTTP (Flask, puerto 8505)
├── ledger/emissions_log.csv   ← Registro de emisiones πCODE-888
├── tests/test_qcal_bus.py     ← Suite de tests (28 casos)
├── .github/workflows/ci.yml   ← CI/CD: tests + integridad de catálogo
├── qcal.json
└── .env.example
```

## Capas de la Malla (33 nodos)

| Capa | Nodos |
|------|-------|
| núcleo | riemann-adelic, 141-hz |
| cuerpo | 3d-navier-stokes, p-np-qcal |
| mente | ramsey-qcal, adelic-bsd |
| vida | biologia-cuantica-noesica |
| logos | noesis88, LOGOSNOESIS, quantum-internet-qcal |
| espíritu | espiritu-qcal, akasha-qcal, conciencia-cosmica |
| sombra | sombra-colectiva, trauma-quantico |
| integración | integracion-sombra, campo-morfogenico, entrelazamiento-epr |
| tiempo | tiempo-no-lineal, memoria-cuantica |
| geometría | geometria-sagrada, flor-de-vida, torus-qcal |
| sanación | sanacion-cuantica, adn-reparacion, coherencia-cardiaca |
| lenguaje | lenguaje-qcal, simbolos-noesicos |
| mente-expandida | red-neuronal-cuantica, intuicion-colectiva |
| economía | economia-qcal-nodo-semilla, economia-regenerativa, pi-code-888 |

## Funciones

- Monitoreo global de resonancia de los 33 nodos MCP.
- Cálculo de `Ψ_GLOBAL_ECOSISTEMA` (media aritmética de todos los nodos).
- Emisión a ledger (`πCODE-888`) cuando `Ψ_GLOBAL >= 0.999999` por 3 ciclos consecutivos.
- Servidor MCP JSON-RPC 2.0 (stdin/stdout) con tres herramientas expuestas.
- Dashboard HTTP en puerto `8505` con visualización de nodos y ledger.

## Uso rápido

### Loop de monitoreo continuo
```bash
python qcal_mesh_sync.py
```

### Servidor MCP (protocolo JSON-RPC 2.0, stdin/stdout)
```bash
python qcal_mesh_sync.py --mcp-server
```

### Herramientas MCP disponibles
| Herramienta | Descripción |
|-------------|-------------|
| `get_mesh_state` | Estado actual de la malla (Ψ_GLOBAL + todos los nodos) |
| `get_node_catalog` | Catálogo completo de 33 nodos |
| `get_emissions_log` | Últimas N entradas del ledger de emisiones |

### Dashboard
```bash
python dashboard/malla_qcal_epr.py
```
Rutas disponibles:
- `http://localhost:8505/` — Dashboard visual
- `http://localhost:8505/api/mesh_state` — Estado JSON
- `http://localhost:8505/api/node_catalog` — Catálogo JSON
- `http://localhost:8505/api/emissions_log` — Ledger JSON
- `http://localhost:8505/api/mcp` (POST) — Endpoint HTTP MCP JSON-RPC

## Configuración

Copia `.env.example` a `.env` y ajusta las variables:

```bash
cp .env.example .env
```

Variables clave:

| Variable | Descripción | Por defecto |
|----------|-------------|-------------|
| `QCAL_REAL_TESTS` | `0` = simulado, `1` = conexiones reales | `0` |
| `QCAL_GLOBAL_THRESHOLD` | Umbral para RESONANCIA_SATURADA | `0.999999` |
| `QCAL_SATURATION_CYCLES` | Ciclos consecutivos para emitir | `3` |
| `QCAL_EMISSION_BASE` | Base πCODE para cálculo de emisión | `888` |
| `QCAL_NODE_<ID>_URL` | URL de cada nodo MCP (modo real) | — |

## Tests

```bash
QCAL_REAL_TESTS=0 pytest tests/ -v
```

> Nota: el dashboard usa el servidor de desarrollo de Flask y está pensado para entorno local.

