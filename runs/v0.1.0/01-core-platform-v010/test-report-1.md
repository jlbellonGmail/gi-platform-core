# Test Report 1 — QA

## Veredicto

```yaml
status: approved
attempt: 1
feedback: []
```

## Resultado

- `pytest -q tests/test_core_platform.py`: 7 passed.
- `pytest -q tests/test_agentic_schemas.py tests/test_agents_e2e.py`: 24 passed.
- `pytest -q tests/test_agentic_sync_scripts.py`: 6 passed.
- `check-integrity.ps1`: PASS.
- `check-status.ps1`: PASS con warnings regenerables sin remoto.
- `sync-agentic-adapters.ps1 -Check`: PASS.
- `validate-supply-chain.ps1`: PASS.

## Cobertura funcional

Verificados múltiples Sites, memberships multi-Organization, deny-by-default,
roles/permisos, acceso por Site, aislamiento, auditoría y serialización pública.
