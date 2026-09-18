# GI-PLATFORM-CORE v0.1.0 — diseño técnico

## Capas

El paquete `gi_platform_core` mantiene la dirección:
`API/contratos → Application/Use Cases → Domain → Ports → Adapters`.
Los contratos públicos viven en `contracts.py`; los casos de uso en
`application.py`; las entidades e invariantes en `domain.py`; los puertos en
`ports.py`; y el adaptador determinista actual en `adapters.py`. No existe
dependencia de UI, framework web, base de datos ni vertical.

## Módulos y entidades

`Organization` es el tenant raíz. `Site` siempre referencia una
Organization. `UserProfile` representa identidad de aplicación.
`OrganizationMembership` une un usuario con una Organization y contiene el
alcance de Sites permitido. `Role` pertenece a una Organization y referencia
permisos por código; `MembershipRole` asigna roles a memberships.

## Tenant context y autorización

`TenantContext` contiene `user_id`, `organization_id` y un `site_id`
opcional. Una decisión requiere membership activa, role asignado, permiso
coincidente y, cuando hay Site, pertenencia del Site a la Organization y
acceso explícito en la membership. Las búsquedas nunca aceptan una entidad
de otra Organization. El resultado es deny-by-default.

## Ports, adaptadores y persistencia

`CoreStore` es el port de persistencia y auditoría. v0.1.0 incluye
`InMemoryCoreStore` para pruebas y uso local reproducible. Una integración
productiva deberá implementar el mismo port con su almacenamiento, sin
mover reglas al adaptador. No se elige todavía una base de datos.

## Auditoría y seguridad

Las mutaciones y decisiones de autorización emiten `AuditEvent` con actor,
Organization, Site, acción, resultado y metadata. La validación rechaza
identificadores/nombres vacíos y códigos de permiso no namespaced. La
autorización falla cerrada para membership ausente/inactiva, Site ajeno,
permiso ausente o role de otra Organization.

## Contratos y versionado

`CoreApi` es una fachada neutral de transporte y devuelve diccionarios con
`contract_version: "0.1.0"`. HTTP, eventos, RPC u otros adaptadores pueden
envolverla sin acceder a entidades privadas. El contrato usa SemVer; durante
`0.x`, cambios incompatibles incrementan el minor cuando se formalice la
política pública y los parches mantienen compatibilidad dentro de `0.1.x`.

## Pruebas

`tests/test_core_platform.py` verifica multiplicidad de Sites, pertenencia
multi-Organization, roles/permisos, aislamiento, alcance por Site, auditoría,
membership inactiva y consumibilidad del contrato. Las pruebas no requieren
servicios externos.
