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

- Actualizado: 2026-09-21T03:51:29Z
- Versión: v0.1.0
- Rama: develop
- HEAD: 647b1246167d5e933b385b67a0d7638513f8cb4d
- Remoto: https://github.com/jlbellonGmail/gi-platform-core
- Working tree: dirty
- Worktrees: 3
- Worktrees Git: 3
- Unidades activas: ninguna
- PR activa: UNKNOWN / sin PR abierta
- CI:  @ f9e72d32ef829201057105115110f1f1a3c5404d
- CI vigente:  @ f9e72d32ef829201057105115110f1f1a3c5404d
- Última release: v0.2.0

<!-- STATUS:AUTO:END -->
