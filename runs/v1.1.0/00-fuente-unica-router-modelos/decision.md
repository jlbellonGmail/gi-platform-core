# Decision: 00-fuente-unica-router-modelos - Fuente unica router modelos

## Estado

Feature lista para PR y pendiente de merge real contra `develop`.

## Evidencias revisadas

- `runs/v1.1.0/00-fuente-unica-router-modelos/spec.md`
- `runs/v1.1.0/00-fuente-unica-router-modelos/audit-1.md`
- `runs/v1.1.0/00-fuente-unica-router-modelos/test-report-1.md`
- `docs/tecnica/fuente-unica-router-modelos.md`
- `docs/usuario/fuente-unica-router-modelos.md`

## Decisiones demostrables

- `.agentic/` es la fuente canonica para roles, modelos, fallback y MCP.
- `.agents/skills/` es la fuente canonica de skills portables; los mirrors
  de herramienta se generan.
- `scripts/sync-agentic-adapters.ps1` es el unico generador/validador de
  adaptadores Claude, Codex y OpenCode.
- `scripts/resolve-agentic-model.ps1` resuelve modelos OpenCode con
  allowlists, variantes separadas y fallback explicito.
- `scripts/complete-approved-pr.ps1` implementa el gate post-HITL:
  mergea solo con checks verdes posteriores a la aprobacion humana y
  devuelve feedback a builder si fallan.

## Resultado

La feature no se marca `[x]` localmente. El cierre final ocurre solo
cuando la PR mergeada contra `develop` active el workflow post-merge.
