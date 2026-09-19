# GI-PLATFORM-CORE v0.1.0

GI-PLATFORM-CORE ofrece capacidades comunes para productos y verticales:
Organizations, Sites, identidad, memberships, roles, permisos, autorización
contextual, aislamiento y auditoría.

Una persona puede pertenecer a varias Organizations. Cada Site pertenece a
una sola Organization y el acceso a un Site se concede explícitamente en la
membership. Para autorizar una operación se envía el usuario, la
Organization, el permiso y opcionalmente el Site; el Core responde una
decisión versionada y registra la comprobación.

La primera aplicación consumidora prevista es `GI-CLINICADENTAL`, pero esa
aplicación, `gi-vertical-dental` y sus reglas de dominio están fuera de este
repositorio. Chat, Voice, WhatsApp, Web, Mobile y Desktop son canales futuros
que usarán los mismos casos de uso server-side.

La integración actual es transport-neutral mediante `CoreApi`; no expone
tablas ni requiere una UI. Para producción, la aplicación anfitriona puede
registrar `SupabaseCoreStore` con su URL y clave server-side y aplicar la
migración `supabase/migrations/20260918000000_core_schema.sql`. La clave no
se configura dentro del Core ni se expone al navegador.

## Consumo como paquete

Desde el repositorio anfitrión se instala la versión publicada o el checkout
del Core:

```powershell
python -m pip install gi-platform-core==0.1.0
```

El ejemplo completo de inicialización está en
`examples/core_integration.py`. La aplicación anfitriona puede usar
`InMemoryCoreStore` para tests y `SupabaseCoreStore` en backend. Las entidades
y reglas específicas de Dental no se agregan al Core.

## Construcción y publicación

La publicación de v0.1.0 se realiza como wheel Python asociado a la release
del repositorio. Desde un checkout limpio:

```powershell
python -m pip install --upgrade pip
python -m pip wheel . --no-deps --wheel-dir dist
```

El archivo `dist/gi_platform_core-0.1.0-py3-none-any.whl` es el artefacto que
deben instalar los repositorios consumidores. El workflow
`.github/workflows/publish-core-package.yml` construye el wheel y lo adjunta a
la release GitHub cuando un humano publica un tag SemVer correspondiente. El
consumidor debe fijar la versión explícita; no debe instalar `develop`
implícitamente.

La validación read-only del entorno Supabase se ejecuta con:

```powershell
python scripts/validate_supabase_core.py --public-only
python scripts/validate_supabase_core.py --expect-visible organizations
```

La segunda orden requiere `SUPABASE_ACCESS_TOKEN`. El validador no muta datos;
la aplicación de migraciones se realiza por el procedimiento autorizado del
proyecto Supabase y se verifica antes de ejecutar la validación autenticada.
