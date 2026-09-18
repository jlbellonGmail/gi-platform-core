# Spec F10

## Objetivo

Preparar el acceso declarativo a capacidades externas sin agregar servidores
hipotéticos ni comprometer la seguridad F11.

## Criterios de aceptación

- AC-1: `.agentic/mcp.json` tiene un schema existente y el catálogo vacío es válido.
- AC-2: cada herramienta declara capacidad, modo, permisos, riesgo, requisitos, optional y carga `on-demand`.
- AC-3: read-only y write/action consumen capacidades distintas de F11.
- AC-4: autorización scoped, secreto faltante, fallback y bloqueo requerido son verificables.
- AC-5: no se registran secretos, no se saltean gates y no se acopla a un proveedor.
- AC-6: existen docs técnica/usuario, decisión, índices y evidencia de revisión/QA.
