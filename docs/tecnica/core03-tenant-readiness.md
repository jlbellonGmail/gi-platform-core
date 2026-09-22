# CORE03 — Tenant readiness

## Modelo canónico

Core identifica el límite técnico mediante `tenant_id`, un identificador opaco
que conserva los UUID existentes. Tenant contiene únicamente identidad técnica,
estado, membresías, roles, permisos, contexto de ubicación, autorización,
auditoría y vínculos opacos de identidad.

Core no contiene titulares comerciales, personas de negocio, suscripciones ni
facturación. Esos datos corresponden a GI-COMMON-TENANTS y GI-COMMON-PERSONS;
CRM y GI-CLINICADENTAL consumen los contratos públicos de Core.

## Persistencia y seguridad

Las tablas canónicas son `core.tenants`, `core.memberships`,
`core.locations`, `core.roles`, `core.identity_links` y las tablas auxiliares
de permisos, roles de membresía, acceso a ubicaciones y auditoría. La
migración `20260921000000_core03_tenants.sql` renombra tablas y columnas sin
cambiar UUIDs ni relaciones, elimina restos de compatibilidad y mantiene RLS.

La migración de `sites` sólo se aplica a instalaciones históricas que todavía
contienen esas tablas. Una instalación nueva usa `20260918000000_core_schema.sql`,
`20260920000000_identity_links.sql` y luego CORE03.

## Contratos

La biblioteca Python expone `Tenant`, `TenantContext(tenant_id=...)`,
`create_tenant`, `list_tenants`, membresías, roles, permisos, autorización y
resolución/link de identidad. La API HTTP canónica usa
`/v1/tenants/{tenant_id}/identity-validation` y
`/v1/tenants/{tenant_id}/identity-links`.

Los contratos v0.1.0/v0.2.0 son publicados y se conservan como adaptadores
legacy explícitos; no son el modelo interno ni la persistencia canónica. La
migración CORE03 no deja tablas, vistas ni columnas `organization*`.

## Integración de consumidores

Los consumidores deben enviar `tenant_id` desde su contexto autenticado y no
acceder a tablas Core. COMMON-TENANTS administra información comercial fuera
de Core; PERSONS, CRM y DENTAL mantienen sus datos propios y usan Core para
identidad, membresía, autorización y aislamiento.
