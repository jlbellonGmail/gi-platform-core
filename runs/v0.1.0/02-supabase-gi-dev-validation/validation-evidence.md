# Validation evidence — Supabase gi-dev

## Veredicto

```yaml
status: approved
attempt: 1
environment: gi-dev
secrets_recorded: false
```

## Resultado externo

- Preflight del project ref: PASS.
- Bootstrap mediante `CoreService` y `SupabaseCoreStore`: PASS.
- Bootstrap idempotente: PASS; no se reportaron duplicados.
- `organizations`: HTTP 200, 1 fila visible.
- `locations`: HTTP 200, 0 filas visibles.
- `user_profiles`: HTTP 200, 1 fila visible.
- `organization_memberships`: HTTP 200, 1 fila visible.
- `roles`: HTTP 200, 0 filas visibles.
- `permissions`: HTTP 200, 0 filas visibles.
- `membership_roles`: HTTP 200, 0 filas visibles.
- `location_access`: HTTP 200, 0 filas visibles.
- `audit_events`: HTTP 200, 1 fila devuelta por el validador limitado a una fila.
- RLS autenticada y aislamiento sintético: PASS.

No se registraron JWT, passwords, claves, emails, UUIDs ni payloads de
autenticación. No se ejecutaron eliminaciones ni se modificaron policies.
