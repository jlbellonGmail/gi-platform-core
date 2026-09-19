# Integrity evidence — Feature 02

```yaml
status: PASS
scope: 02-supabase-gi-dev-validation
environment: gi-dev
head: HEAD
base: develop
secrets_recorded: false
```

## Validaciones ejecutadas

- `python scripts/bootstrap_validate_supabase.py --env-file C:\Proyectos\gi-platform-core\.env`: PASS; destino gi-dev verificado, bootstrap idempotente completado/verificado.
- `python scripts/validate_supabase_core.py --expect-visible organizations`: PASS; las 9 tablas respondieron HTTP 200 y `organizations` devolvió 1 fila autorizada.
- Prueba de aislamiento RLS sintético: PASS.
- `pytest`: PASS según `runs/v0.1.0/02-supabase-gi-dev-validation/test-report-1.md`.
- `sync-agentic-adapters.ps1 -Check`, `validate-supply-chain.ps1` y `check-integrity.ps1`: PASS según la evidencia de QA.

No se registraron JWT, contraseñas, claves, UUIDs ni payloads de autenticación.
No se ejecutaron eliminaciones ni se modificaron políticas RLS.

