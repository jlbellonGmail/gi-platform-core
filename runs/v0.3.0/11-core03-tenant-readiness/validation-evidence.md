# Evidencia de validación

## Local

- `pytest -q` focalizado: 37 passed.
- `python -m compileall -q gi_platform_core`: PASS.
- `sync-agentic-adapters.ps1 -Check`: PASS.
- `validate-supply-chain.ps1`: PASS; 6 workflows, acciones SHA-pinned y
  permisos explícitos.
- `git diff --check`: PASS.

## Supabase remoto

Verificación directa con `psycopg` contra `DATABASE_URL`:

- `tenants`, `memberships`, `locations`, `roles`, `identity_links`: presentes.
- RLS activo en las cinco tablas.
- 13 foreign keys.
- `link_identity(p_tenant_id, ...)` y `unlink_identity(p_tenant_id, ...)`.
- 0 columnas `organization_id`.
- 0 objetos `organization*` o `site*` en `core`.
- Conteos preservados: 1 tenant, 1 membership, 0 identity links.

El script read-only no se ejecutó desde el worktree porque `.env` es local y
no se replica entre worktrees; la verificación directa anterior sí utilizó la
misma conexión remota configurada y no mutó datos funcionales.
