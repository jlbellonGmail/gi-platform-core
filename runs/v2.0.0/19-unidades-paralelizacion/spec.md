# F14 — Especificación

## Objetivo

Automatizar work units paralelas con identidad estable, reconciliación
pre-merge, invalidación stale, gobernanza explícita y cleanup seguro Windows.

## Criterios de aceptación

- AC-1: cada unidad registra versión, modo, identidad canónica, rama,
  worktree, run, base y HEAD.
- AC-2: detecta avance de develop y reconcilia por merge; conflictos
  semánticos quedan bloqueados.
- AC-3: una reconciliación invalida CI, review y autorización dependientes del
  HEAD.
- AC-4: STATUS observa Features, Milestones y Maintenance sin sufijos frágiles.
- AC-5: cleanup clasifica ausencia, residual vacío, contenido y metadata activa.
- AC-6: el gate soporta SingleMaintainer y MultiMaintainer explícitos.
- AC-7: Maintenance normal, correctiva e histórica conserva cierre idempotente.
- AC-8: existen documentación, decisión y enlaces exactos.

## Supuestos y decisiones pendientes bloqueantes

Ninguna. Se conserva el contrato legacy y no se inicia F16.
