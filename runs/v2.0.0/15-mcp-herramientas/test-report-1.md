# QA F10

```yaml
status: approved
attempt: 1
```

## Evidencia

- `pytest -q`: 241 passed.
- `scripts/sync-agentic-adapters.ps1 -Check`: passed.
- `git diff --check`: passed.
- Los negativos cubren modo/carga inválidos, write sin autorización, secreto requerido faltante, fallback opcional y JSON inválido.

No se usaron credenciales ni red real.
