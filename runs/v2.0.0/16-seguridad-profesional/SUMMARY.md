# F11 — Seguridad profesional

Estado: READY_FOR_PR · Versión: v2.0.0 · Tipo: Feature · SDD: FULL · PR: #54 · Merge: pendiente

## Objetivo

Máxima autonomía compatible con el riesgo mediante permisos progresivos,
fail-safe, reversibilidad y trazabilidad.

## Resultado

Política declarativa provider/model agnostic, validador de autorización scoped,
CI con mínimo privilegio y marco consumible por F10.

## Cambios principales

- `.agentic/security-policy.json` y schema.
- `scripts/security-policy.ps1` con deny-by-default y validación de scopes.
- Tests negativos y permisos de CI de sólo lectura.
- Documentación técnica y de usuario.

## Validación

236 tests verdes en el HEAD reconciliado; contrato, adaptadores y checks
focalizados aprobados.

## Decisiones

Merge sólo sobre PR/HEAD vigente; MCP queda para F10 y supply chain para F12.

## Incidencias

Advertencia XML ambiental de PowerShell sin impacto en tests ni secretos.

## Detalle

[spec](spec.md) · [plan](plan.md) · [tasks](tasks.md) · [audit](audit-1.md) · [QA](test-report-2.md) · [code review](code-review-2.md) · [decision](decision.md)
