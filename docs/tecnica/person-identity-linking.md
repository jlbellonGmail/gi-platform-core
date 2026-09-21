# Vinculación de identidad Person — CoreApi v0.2.0

Core almacena únicamente la referencia opaca `person_id` y la vincula a un
`UserProfile` existente dentro de una `Organization`. No importa la entidad
`Person` del vertical ni busca por email, teléfono o documento; tampoco crea o
modifica memberships. Las operaciones nuevas son aditivas sobre CoreApi
v0.1.0 y usan `contract_version: 0.2.0`.

La resolución exige organización, usuario y membership activos, más coincidencia
exacta de `user_id` y `external_subject`. Los fallos de resolución son
`not_found` para evitar filtraciones cross-tenant. Link y unlink requieren
`organization:identity_link` y `organization:identity_unlink`; actor y tenant
provienen del contexto autenticado. El link es único por
`(organization_id, person_id)`: el mismo link es idempotente, otro usuario da
`409 conflict`, y unlink repetido devuelve `removed: false`. Cada operación
audita resolución, link o unlink sin metadata sensible.

El servicio HTTP es un adaptador WSGI de biblioteca estándar: `create_app` y
`python -m gi_platform_core.http_server`. El host inyecta su autenticador
actual mediante `CORE_AUTH_MODULE=paquete:funcion`, que devuelve
`AuthenticatedActor`; Core no parsea JWT ni inventa tokens. Endpoints:
`GET /healthz`, `GET /readyz`, `POST /v1/organizations/{id}/identity-validation`,
`POST /v1/organizations/{id}/identity-links` y
`DELETE /v1/organizations/{id}/identity-links/{person_id}`.

El store en memoria usa lock. Supabase usa las funciones SQL con advisory lock
transaccional. La auditoría se escribe por el puerto existente después de la
operación; no se promete una transacción distribuida.
