# Spec CORE03

Tenant es la raíz técnica de aislamiento. `tenant_id` es opaco, estable y
preserva los identificadores existentes. Las operaciones de membresía,
ubicación, rol, permiso, identidad y autorización deben validar el mismo
tenant antes de conceder acceso.

La persistencia canónica no contiene `organizations`, `organization_memberships`
ni `organization_id`. Las interfaces legacy pueden traducir nombres antiguos
en memoria para consumidores publicados, pero no pueden cambiar el tenant del
contexto ni acceder al store.

Los contratos nuevos se versionan como v0.3.0 y exponen Tenant; la HTTP canónica
usa `/v1/tenants`. Core no depende de COMMON, Persons, CRM o Dental.
