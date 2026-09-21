# Spec

## Identificación

- Ítem: `05-person-identity-linking`
- Versión: `v0.2.0`
- Compatibilidad: CoreApi v0.1.0 no cambia; operaciones nuevas son v0.2.0.

## Requisitos verificables

1. Resolver por `user_id` y `external_subject` dentro de organización activa,
   con usuario y membership activos; fallar cerrado y JSON-safe.
2. Link/unlink requieren actor autenticado, tenant autenticado y permisos
   namespaced; nunca crean o modifican membership.
3. Aislar organizaciones, no inferir por atributos personales y auditar todas
   las operaciones.
4. Definir idempotencia y conflicto concurrente por `(organization, person)`.
5. Exponer biblioteca y WSGI HTTP con health/readiness y configuración segura.
6. Persistir detrás de CoreStore y documentar el límite de auditoría no
   distribuida.

## Fuentes y decisiones

El modelo de auth existente usa `UserProfile.external_subject`, memberships,
roles, permisos y `TenantContext`; el host mantiene la validación del token.
El repositorio no tenía HTTP, por lo que se eligió WSGI estándar para Python
>=3.12 y sin dependencia runtime nueva.
