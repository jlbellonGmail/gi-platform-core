# GI-PLATFORM-CORE

Proyecto nuevo inicializado desde Template v2.0.0.

## Estado inicial

El repositorio contiene únicamente la infraestructura reusable del circuito
agentic: Planner, Builder, Reviewer, ASSESS, SDD adaptativo, gates, CI,
worktrees, lifecycle, auditoría, routing declarativo y políticas de MCP y
Skills. No se ha definido todavía funcionalidad ni arquitectura de producto.

La procedencia de esta baseline es:

- Template: v2.0.0
- SHA: `f5d4b6cc029c34c0d0c05831bfd28134276fa167`

La primera work unit funcional es `01-core-platform-v010`; su estado y
evidencia se mantienen en `ROADMAP.md` y `runs/`.

## Comprobaciones

```powershell
pytest -v
pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\sync-agentic-adapters.ps1 -Check
pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-supply-chain.ps1
```
