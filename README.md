# GI-PLATFORM-CORE

Core reusable v0.1.0 para productos y verticales GI. Provee tenancy,
identidad base, memberships, roles, permisos, autorización contextual,
aislamiento y auditoría sin depender de Dental ni de una UI.

La procedencia de esta baseline es:

- Template: v2.0.0
- SHA: `f5d4b6cc029c34c0d0c05831bfd28134276fa167`

La primera work unit funcional es `01-core-platform-v010`; su estado y
evidencia se mantienen en `ROADMAP.md` y `runs/`. La integración de Dental y
la aplicación consumidora viven en repositorios separados.

## Instalación local

El paquete no tiene dependencias de runtime externas y requiere Python 3.12+:

```powershell
python -m pip install .
```

Para desarrollo y tests:

```powershell
python -m pip install -r requirements-dev.txt
pytest -q
```

El ejemplo reproducible está en `examples/core_integration.py`. La aplicación
anfitriona puede sustituir `InMemoryCoreStore` por `SupabaseCoreStore` y debe
mantener la clave Supabase sólo en backend/server-side.

Para comprobar una instancia Supabase sin mutar datos:

```powershell
python scripts/validate_supabase_core.py --public-only
python scripts/validate_supabase_core.py --expect-visible organizations
```

La segunda variante requiere `SUPABASE_ACCESS_TOKEN` de un usuario autenticado
y sólo debe usarse con datos de prueba conocidos.

Las releases publican el wheel automáticamente como artefacto de GitHub cuando
un humano crea un tag SemVer `vX.Y.Z`; el workflow no crea tags ni releases.

## Comprobaciones

```powershell
pytest -v
pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\sync-agentic-adapters.ps1 -Check
pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-supply-chain.ps1
```
