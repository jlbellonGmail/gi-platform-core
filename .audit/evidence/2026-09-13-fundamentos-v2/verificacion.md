# Verificación de Fase 00

Alcance: fundamentos documentales y gobernanza en `chore/fundamentos-v2`.
Referencia de calidad: `.audit/QUALITY_SCORE.md`, `AUDIT_RULES.md` y perfil
TEMPLATE. Es una revisión acotada, no una auditoría global ni un nuevo score.
La evidencia distingue diseño DOCUMENTADO de motor v1 EJECUTADO/VERIFICADO.

## Comandos reproducibles

Desde el worktree, con PowerShell 7 y Python con requirements-dev instalados:

```powershell
py -3.14 -m pytest -q
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/sync-agentic-adapters.ps1 -Check
git diff --check
git diff --exit-code v1.1.0 -- scripts tests .agentic .agents .claude .codex .opencode .github opencode.json .mcp.json requirements-dev.txt
git rev-parse v1.1.0 'v1.1.0^{commit}'
git ls-remote origin refs/tags/v1.1.0 'refs/tags/v1.1.0^{}'
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/update-status.ps1
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/check-status.ps1
```

En CI se usa Python 3.12: `pytest -v` (Ubuntu) y la suite específica del
reconciliador (Windows), más validación de adaptadores. `product-tests`
sigue siendo el placeholder declarado, no una prueba de producto real.

Los contratos Feature/Milestone se ejercitan mediante sus tests existentes.
No se invoca `ready-for-pr` ni un contrato de feature sobre esta rama chore:
no hay work unit ni manifiesto que lo justifique. La PR se crea con `gh pr
create --base develop`, se verifican sus checks y el merge lo decide y
ejecuta el humano. No hay cierre automático de checkbox para este bootstrap.

## Resultado

- Suite completa del motor conservado: **204 passed in 406.45s (0:06:46)**,
  exit 0, Windows, `py -3.14 -m pytest -q`. No skips ni fallos reportados.
- Adaptadores `-Check`: exit 0.
- Comparación de scripts/tests/config/adaptadores/workflows/dependencias con
  `v1.1.0`: diff vacío, exit 0. No se reemplazó código maduro.
- `main` remoto, objeto del tag y commit desreferenciado conservan los hashes
  de [baseline](baseline.md). STATUS ajeno conserva su hash registrado.
- Revisión adversarial final: `revision-final.md`, `status: approved`, sin
  deficiencias materiales abiertas. STATUS se refrescó en el worktree correcto
  y `check-status.ps1` pasó con advertencia esperable de CI aún inexistente.
- Pendientes operativos: commit/push, PR contra `develop` y CI de esa PR; sólo
  después corresponde detenerse para HITL.
