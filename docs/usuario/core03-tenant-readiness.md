# Integración Tenant de Core

Los consumidores integran Core mediante la biblioteca Python o la API HTTP.
El identificador `tenant_id` es opaco y debe viajar en el contexto autenticado;
no se acepta que el body elija el actor o el tenant.

La operación HTTP de validación usa `POST /v1/tenants/{tenant_id}/identity-validation`.
Los vínculos usan `POST` y `DELETE` sobre
`/v1/tenants/{tenant_id}/identity-links`. Las respuestas incluyen
`contract_version`, `tenant_id` y los datos públicos de identidad, nunca el
store ni credenciales.

GI-COMMON-TENANTS, GI-COMMON-PERSONS, CRM y GI-CLINICADENTAL mantienen sus
propios datos y dependen solamente de estos contratos. Core no implementa
datos comerciales, personas operativas, suscripciones ni facturación.

Las rutas y métodos `organization*` publicados se consideran transición
legacy; las integraciones nuevas deben usar Tenant.
