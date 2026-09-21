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

- Actualizado: 2026-09-21T03:32:03Z
- Versión: v0.1.0
- Rama: docs/v0.2.1-status-final
- HEAD: f37dd345aa6dbb9c094bdae04aec470412d31a4d
- Remoto: https://github.com/jlbellonGmail/gi-platform-core.git
- Working tree: dirty
- Worktrees: 8
- Worktrees Git: 8
- Unidades activas: = [feature/v0.1.0-02-supabase-gi-dev-validation]; = [feature/v0.1.0-03-post-hitl-versioned-evidence]; = [feature/v0.1.0-04-post-merge-close-dispatch]; = [feature/v0.2.1-06-release-readiness-current-roadmap]; = [feature/v0.2.1-07-release-evidence]; = [feature/v0.2.1-08-release-evidence-pr]
- PR activa: UNKNOWN / sin PR abierta
- CI: UNKNOWN / sin CI verificable
- CI vigente: UNKNOWN / sin CI verificable
- Última release: UNKNOWN / no disponible

<!-- STATUS:AUTO:END -->
