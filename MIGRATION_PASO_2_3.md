# MIGRACIÓN PASO 2 → PASO 3

## Resumen

Se consolida `registry/NODE_CATALOG.json` como única fuente de verdad del catálogo QCAL-BUS.

- Ruta legacy eliminada: `registro/NODE_CATALOG.json`
- Ruta canónica activa: `registry/NODE_CATALOG.json`

## Cambio de estructura

### Antes

- `registro/NODE_CATALOG.json` (legacy)
- `registry/NODE_CATALOG.json` (catálogo unificado)

### Ahora

- `registry/NODE_CATALOG.json` (único catálogo operativo)

## Guía de actualización

1. Reemplazar cualquier referencia a `registro/NODE_CATALOG.json` por `registry/NODE_CATALOG.json`.
2. Verificar que los consumidores usen `qcal_mesh_sync.CATALOG_PATH`.
3. No mantener copias paralelas del catálogo en otras carpetas.

## Mapeo de compatibilidad (legacy → unificado)

| Campo legacy (`registro/`) | Campo actual (`registry/`) | Estado |
|---|---|---|
| `meta.name` | `meta.name` | compatible |
| `meta.version` | `meta.version` | compatible |
| `meta.f0_reference_hz` | `meta.f0_reference_hz` | compatible |
| `meta.total_nodes` | `meta.total_nodes` | compatible |
| `nodes.*.mcp_id` | `nodes.*.mcp_id` | compatible |
| `nodes.*.role` | `nodes.*.role` | compatible |
| `nodes.*.layer` | `nodes.*.layer` | compatible |
| `nodes.*.base_frequency` | `nodes.*.base_frequency` | compatible |
| `nodes.*.harmonic_factor` | `nodes.*.harmonic_factor` | compatible |
| `nodes.*.mcp_endpoint` | `nodes.*.mcp_endpoint` | compatible |

Campos adicionales en `registry/` (enriquecidos) como `github_repo`, `github_url`, `description`, `lean_*` y metadatos extendidos se consideran extensión no rompiente para consumidores existentes.
