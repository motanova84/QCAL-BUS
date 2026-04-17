# QCAL-BUS (qcal-mesh-bus)

Repositorio maestro para orquestación de malla QCAL-EPR.

## Estructura

```
qcal-mesh-bus/
├── qcal_mesh_sync.py
├── registry/NODE_CATALOG.json
├── dashboard/malla_qcal_epr.py
├── ledger/emissions_log.csv
├── qcal.json
└── .env.example
```

## Funciones

- Monitoreo global de resonancia de nodos MCP.
- Cálculo de `Ψ_GLOBAL_ECOSISTEMA`.
- Emisión a ledger (`πCODE-888`) cuando `Ψ_GLOBAL >= 0.999999` por 3 ciclos consecutivos.
- Dashboard HTTP en puerto `8505`.

## Uso rápido

```bash
python qcal_mesh_sync.py
```

```bash
python dashboard/malla_qcal_epr.py
```

Dashboard: `http://localhost:8505`
