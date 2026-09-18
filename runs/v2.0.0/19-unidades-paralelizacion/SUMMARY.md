# F14 — Unidades y paralelización

Estado: DONE
Versión: v2.0.0
Tipo: Feature
SDD: FULL
PR: pendiente de creación
Merge: pendiente

## Objetivo

Formalizar identidad canónica, aislamiento, reconciliación pre-merge,
gobernanza single/multi-maintainer y cleanup seguro de worktrees.

## Resultado

Se incorporó lifecycle determinístico con registro explícito de unidad,
reconciliación segura contra origin/develop, invalidación de evidencia stale,
clasificación de residuos Windows y una ruta single-maintainer auditable.

## Cambios principales

- workunit-lib.ps1 expone identidad canónica estable.
- unit-lifecycle.ps1 inspecciona/reconcilia y registra base/HEAD.
- cleanup-work-unit.ps1 clasifica y difiere residuos sin borrar contenido.
- update-status.ps1 observa Feature, Milestone y Maintenance.
- complete-approved-pr.ps1 implementa governance explícita.

## Validación

La suite pytest existente pasó en la verificación inicial (30 tests focalizados).
Se ejecutará la suite completa y check-integrity.ps1 antes de crear la PR.

## Decisiones

Se conserva compatibilidad con manifests y scripts legacy. No se agrega
scheduler, daemon Windows, Sysinternals obligatorio ni heurística ours/theirs.

## Incidencias

La CI y el número de PR se completarán durante el cierre E2E.

## Detalle

F16 no se ejecuta y v2.0.0 no se publica desde esta unidad.
