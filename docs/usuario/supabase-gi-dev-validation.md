# Validación autenticada de Supabase gi-dev

El procedimiento único es `scripts/bootstrap_validate_supabase.py`. Ejecuta
un preflight estricto del project ref, autentica interactivamente al usuario
de prueba, solicita con entrada oculta una clave server-side y usa
`CoreService` con `SupabaseCoreStore`.

La clave server-side debe obtenerse sólo del proyecto gi-dev, en Supabase
Dashboard → Project Settings → API → Secret key (o `service_role` en
proyectos que todavía muestran el nombre legado). No se copia al repositorio,
no se guarda en `.env` ni se pasa como argumento.

Desde la worktree de la Feature, ejecutar una única orden:

```powershell
python scripts/bootstrap_validate_supabase.py --env-file C:\Proyectos\gi-platform-core\.env
```

El comando solicita el project ref verificado, el email, la contraseña oculta
y la clave server-side oculta. La contraseña, el JWT y la clave sólo viven en
memoria durante la ejecución.

El identificador sintético es determinista: los primeros 12 caracteres del
SHA-256 del `sub` del JWT. Por ello una segunda ejecución no duplica la
organización, el perfil ni la membership. Sólo se crean, si faltan:

- `core.organizations`: `GI DEV RLS TEST <identificador>`.
- `core.user_profiles`: perfil cuyo `external_subject` es el `sub` exacto.
- `core.organization_memberships`: membership activa entre ambos.
- Los eventos de auditoría emitidos por los casos de uso del Core.

No se crean roles, permisos, locations ni accesos. El comando termina con
error si encuentra duplicados, un perfil no sintético para el usuario, una
membership sintética inactiva o un project ref que no coincide exactamente
con el host de `SUPABASE_URL`.

Después del bootstrap ejecuta el validador read-only autenticado y comprueba
que las filas visibles de perfiles, organizaciones, memberships, roles,
membership roles, location access, auditoría y permisos quedan dentro del
alcance permitido por las políticas vigentes. No modifica las políticas ni
elimina datos.
