# F13 — STATUS, observabilidad y reentrada

## Objetivo
Proveer una vista humana breve y un snapshot verificable para retomar el repositorio sin depender de memoria, distinguiendo actividad Git real, staleness y errores.

## Criterios de aceptación
- AC-1 `STATUS.md` conserva manual y AUTO único, con versión, estado operativo y siguiente acción.
- AC-2 `update-status.ps1` es idempotente, no destructivo y expone JSON sin persistir por defecto.
- AC-3 JSON/AUTO incluyen HEAD, branch, remoto, working tree, worktrees, unidades derivables, PR, CI y release, usando UNKNOWN cuando no verificable.
- AC-4 `check-status.ps1` distingue STALE, INCONSISTENTE, TEMPORAL y ERROR_REAL y da acción.
- AC-5 Sólo worktrees Git y ramas reconocibles cuentan como unidades activas; residuos físicos siguen reglas T04.
- AC-6 existe documentación técnica/usuario, índices exactos, decisión y SUMMARY.
- AC-7 se preserva `check-integrity.ps1`.
