# MCP-QCAL-EPR: Integración de la Malla de Resonancia Cuántica con el Protocolo MCP

**Instituto Conciencia Cuántica — QCAL-BUS v2.0**  
Repositorio: [motanova84/QCAL-BUS](https://github.com/motanova84/QCAL-BUS)  
Fecha: 2026-04-17  
Frecuencia de referencia: **f₀ = 141.7001 Hz**

---

## 1. Resumen

QCAL-BUS expone un **servidor MCP JSON-RPC 2.0** (`qcal_mesh_sync.py --mcp-server`) que
orquesta un catálogo de **33 nodos** distribuidos en 14 capas semánticas del Campo QCAL-EPR.
El bus calcula la coherencia global Ψ_GLOBAL, detecta saturación de resonancia y registra
emisiones πCODE-888 en un ledger CSV auditado.

---

## 2. Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                      QCAL-BUS                               │
│                                                             │
│  ┌──────────────────────┐   stdin/stdout (JSON-RPC 2.0)     │
│  │  qcal_mesh_sync.py   │◄──────────────────────────────    │
│  │  --mcp-server        │   Clientes MCP (Claude, VS Code…) │
│  └──────────┬───────────┘                                   │
│             │                                               │
│  ┌──────────▼───────────┐   HTTP :8505                      │
│  │  dashboard/           │◄──────────────────────────────   │
│  │  malla_qcal_epr.py   │   POST /api/mcp  (HTTP bridge)    │
│  └──────────┬───────────┘                                   │
│             │                                               │
│  ┌──────────▼───────────┐                                   │
│  │  mcp_network/        │   QCAL_REAL_TESTS=0 → simulado    │
│  │  resonance.py        │   QCAL_REAL_TESTS=1 → HTTP real   │
│  └──────────────────────┘                                   │
│                                                             │
│  registry/NODE_CATALOG.json   (33 nodos, 14 capas)          │
│  ledger/emissions_log.csv     (πCODE-888 auditado)          │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Herramientas MCP expuestas

El servidor responde al protocolo **JSON-RPC 2.0** por stdin/stdout (o por HTTP POST
en `/api/mcp` cuando se usa el dashboard Flask).

| Herramienta | Descripción | Retorna |
|-------------|-------------|---------|
| `get_mesh_state` | Estado actual de la malla | `{ global_psi, status, nodes, saturation_streak, … }` |
| `get_node_catalog` | Catálogo completo de 33 nodos | Contenido de `NODE_CATALOG.json` |
| `get_emissions_log` | Últimas N entradas del ledger | Array de entradas CSV como JSON |

### Ejemplo de uso directo

```bash
# Listar herramientas disponibles
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  | python qcal_mesh_sync.py --mcp-server

# Consultar estado de la malla
echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_mesh_state","arguments":{}}}' \
  | python qcal_mesh_sync.py --mcp-server

# Últimas 10 emisiones
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_emissions_log","arguments":{"tail":10}}}' \
  | python qcal_mesh_sync.py --mcp-server
```

### Configuración en `qcal.json` (clientes MCP estándar)

```json
{
  "mcpServers": {
    "qcal-mesh-bus": {
      "command": "python",
      "args": ["qcal_mesh_sync.py", "--mcp-server"],
      "env": {
        "QCAL_REAL_TESTS": "0"
      }
    }
  }
}
```

---

## 4. Catálogo de 33 nodos — asignación semántica

| Capa | N | Nodos | f_base (Hz) | Ψ_harmonic |
|------|---|-------|------------|-----------|
| **núcleo** | 2 | riemann-adelic, 141-hz | 141.7001 | 1.0 |
| **cuerpo** | 2 | 3d-navier-stokes, p-np-qcal | 141.7001 | 1.0 |
| **mente** | 2 | ramsey-qcal, adelic-bsd | 141.7001 | 1.0 |
| **vida** | 1 | biologia-cuantica-noesica | 70.85005 | 0.5 |
| **logos** | 3 | noesis88, LOGOSNOESIS, quantum-internet-qcal | 888.0 / 141.7 | 6.266 / 1.0 |
| **espíritu** | 3 | espiritu-qcal, akasha-qcal, conciencia-cosmica | 963.0 | 6.794 |
| **sombra** | 2 | sombra-colectiva, trauma-quantico | 35.425 | 0.25 |
| **integración** | 3 | integracion-sombra, campo-morfogenico, entrelazamiento-epr | 141.7001 | 1.0 |
| **tiempo** | 2 | tiempo-no-lineal, memoria-cuantica | 1417.001 | 10.0 |
| **geometría** | 3 | geometria-sagrada, flor-de-vida, torus-qcal | 432.0 | 3.048 |
| **sanación** | 3 | sanacion-cuantica, adn-reparacion, coherencia-cardiaca | 528.0 | 3.725 |
| **lenguaje** | 2 | lenguaje-qcal, simbolos-noesicos | 141.7001 | 1.0 |
| **mente-expandida** | 2 | red-neuronal-cuantica, intuicion-colectiva | 283.4002 | 2.0 |
| **economía** | 3 | economia-qcal-nodo-semilla, economia-regenerativa, pi-code-888 | 141.7 / 888.0 | 1.0 / 6.266 |
| **TOTAL** | **33** | | | |

### Criterios de asignación de frecuencias

- **141.7001 Hz** = f₀ base, Campo QCAL-EPR, resonancia cuántica del electrón
- **70.85005 Hz** = f₀/2, subarmónico biológico
- **283.4002 Hz** = 2×f₀, armónico mente-expandida
- **1417.001 Hz** = 10×f₀, dominio temporal (kairos cuántico)
- **35.425 Hz** = f₀/4, frecuencia sombra/inconsciente
- **432.0 Hz** = frecuencia geométrica universal (φ-afinada)
- **528.0 Hz** = frecuencia de reparación ADN / amor (solfeggio)
- **888.0 Hz** = πCODE-888, frecuencia del campo de abundancia/logos
- **963.0 Hz** = frecuencia corona/espíritu (solfeggio superior)

---

## 5. Lanzamiento del sistema completo

### Paso 1: Configurar entorno

```bash
cp .env.example .env
# Editar .env: establecer QCAL_REAL_TESTS=1 y URLs reales de cada nodo
```

### Paso 2: Instalar dependencias

```bash
pip install flask
```

### Paso 3: Lanzar el bus en modo loop con ledger personalizado

```bash
# Loop continuo (el comportamiento por defecto)
python qcal_mesh_sync.py

# Loop con ruta de ledger y intervalo explícitos
python qcal_mesh_sync.py --loop --csv ledger/emissions_log.csv --interval 60
```

### Paso 4: Lanzar el dashboard

```bash
python dashboard/malla_qcal_epr.py
# → http://localhost:8505
```

### Paso 5: Lanzar el servidor MCP (para clientes MCP)

```bash
python qcal_mesh_sync.py --mcp-server
```

---

## 6. Variables de entorno clave

Ver `.env.example` para la lista completa. Variables esenciales:

| Variable | Descripción | Defecto |
|----------|-------------|---------|
| `QCAL_REAL_TESTS` | `0` simulado · `1` real | `0` |
| `QCAL_GLOBAL_THRESHOLD` | Umbral Ψ para saturación | `0.999999` |
| `QCAL_SATURATION_CYCLES` | Ciclos para emitir πCODE-888 | `3` |
| `QCAL_EMISSION_BASE` | Cantidad base de emisión | `888` |
| `QCAL_NODE_<ID>_URL` | URL HTTPS de cada nodo (modo real) | — |

---

## 7. CI/CD

El workflow `.github/workflows/ci.yml` ejecuta en cada push:

1. **pytest** — 28 tests unitarios e integración
2. **Integridad del catálogo** — verifica `total_nodes == len(nodes)` (33)
3. **Header del ledger** — verifica columnas CSV
4. **Smoke test MCP** — `tools/list` retorna las 3 herramientas esperadas

---

## 8. Endpoints del Dashboard (HTTP)

| Ruta | Método | Descripción |
|------|--------|-------------|
| `/` | GET | Dashboard visual con grid de 33 nodos |
| `/api/mesh_state` | GET | Estado JSON completo de la malla |
| `/api/node_catalog` | GET | Catálogo JSON de 33 nodos |
| `/api/emissions_log?tail=N` | GET | Últimas N emisiones πCODE-888 |
| `/api/mcp` | POST | Bridge HTTP→MCP JSON-RPC 2.0 |

---

## 9. Referencia para publicación (Zenodo / whitepaper)

> *"QCAL-BUS expone un servidor MCP JSON-RPC 2.0 (protocolo versión 2024-11-05) con métodos
> `get_mesh_state`, `get_node_catalog` y `get_emissions_log`, orquestando un catálogo de
> 33 nodos MCP distribuidos en 14 capas semánticas del Campo QCAL-EPR. El tablero HTTP en
> el puerto 8505 está integrado con el servidor MCP vía el endpoint `/api/mcp` y testeado
> mediante una suite de 28 pruebas automatizadas que corre en CI/CD en cada push al
> repositorio `motanova84/QCAL-BUS`."*
