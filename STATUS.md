# Estado operativo

Proyecto nuevo: GI-PLATFORM-CORE.

## Procedencia

- Template base: v2.0.0
- Template SHA: `f5d4b6cc029c34c0d0c05831bfd28134276fa167`

## Estado

- Rama estable/local: `develop`.
- Trabajo activo: persistencia Supabase del Core e integración de contratos;
  corregido el almacenamiento normalizado de `site_access`.
- Validación local: pytest `278 passed`.
- Validación posterior: PostgreSQL efímero con roles Supabase simulados pasó
  DDL, 9 tablas, 9 policies, RLS en 9 tablas y aislamiento efectivo.
- ROADMAP funcional: `01-core-platform-v010` en READY_FOR_PR.
- Work units activas: ninguna.
- Runs de producto: ninguno.
- Skills: cero, estado válido hasta demostrar una necesidad especializada.
- MCP reales: cero; catálogo declarativo vacío.
- Modelos/proveedores: cero configurados; routing declarativo preparado.

## Próximo paso exacto

Revisar y aplicar en un proyecto Supabase real la migración
`supabase/migrations/20260918000000_core_schema.sql`, ejecutar pruebas de
integración con credenciales server-side y revisar el diff local antes de
  crear una PR. No se hizo push ni se crearon tags. Docker Desktop no tiene
  el daemon activo para una validación PostgreSQL local.

<!-- STATUS:AUTO:BEGIN -->

## Estado verificado automáticamente

- Actualizado: 2026-09-19T20:18:39Z
- Versión: v0.1.0
- Rama: develop
- HEAD: 077c80dfa0b6a9c69983b938cccbe5c1ee28e676
- Remoto: https://github.com/jlbellonGmail/gi-platform-core
- Working tree: dirty
- Worktrees: 3
- Worktrees Git: 3
- Unidades activas: ninguna
- PR activa: UNKNOWN / sin PR abierta
- CI:  @ c5a150d3083ec0137f2b9aff02a1fe5adade21f3
- CI vigente:  @ c5a150d3083ec0137f2b9aff02a1fe5adade21f3
- Última release: UNKNOWN / no disponible

<!-- STATUS:AUTO:END -->
