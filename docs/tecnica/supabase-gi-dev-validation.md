# Integración y validación de Supabase gi-dev

La validación externa conserva la separación entre el Core y Supabase:
`SupabaseCoreStore` es el adaptador de persistencia y `CoreService` mantiene
las reglas de dominio. La migración existente y sus políticas RLS no cambian.

## Bootstrap

`scripts/bootstrap_validate_supabase.py` autentica al usuario de prueba con
`/auth/v1/token`, valida que el host de `SUPABASE_URL` sea exactamente el
project ref introducido para gi-dev y solicita la clave server-side mediante
`getpass`. No guarda secretos ni los pasa a subprocesos.

El identificador de prueba se deriva de forma determinista del `sub` del JWT.
Antes de escribir, el script carga el estado con `SupabaseCoreStore` y rechaza
duplicados o entidades equivalentes no sintéticas. Las únicas mutaciones son
las operaciones de `CoreService.create_organization`, `create_user` y
`add_membership`; cada una conserva la auditoría normal del Core. Si una
ejecución falla después de una mutación, una nueva ejecución completa sólo lo
que falte y no duplica filas.

## RLS

La validación read-only existente se ejecuta con el JWT y exige visible
`organizations`. Luego se leen las tablas mediante PostgREST autenticado y se
comprueba que los perfiles pertenecen al `sub`, las memberships al perfil,
los roles a organizaciones visibles, los vínculos a memberships visibles y
los eventos al actor visible. No se crean datos de aislamiento adicionales y
no se relajan las políticas.
