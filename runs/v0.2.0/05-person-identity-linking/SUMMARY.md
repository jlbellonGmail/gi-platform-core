# 05-person-identity-linking

Estado: en implementación
Versión: v0.2.0
Tipo: Feature
SDD: FULL
PR: pendiente de crear hacia develop
Merge: no autorizado; requiere decisión humana

## Objetivo

Implementar vínculo tenant-aware entre una referencia Person opaca y una
identidad de acceso Core por biblioteca y HTTP.

## Resultado

Implementación funcional con contrato v0.2.0 compatible con v0.1.0, WSGI,
Supabase RPC, auditoría, pruebas y documentación.

## Cambios principales

Dominio, CoreStore, CoreService/CoreApi, adaptadores, migración, HTTP, OpenAPI,
contratos versionados y documentación.

## Validación

Tests específicos y regresivos verdes; suite completa con un fallo transitorio
de permisos Git temporal repetido y verde aisladamente. Supply chain, compileall,
JSON y diff check verdes.

## Decisiones

Autenticación inyectada por el host; WSGI estándar; atomicidad por puerto y sin
promesa de transacción distribuida para auditoría.

## Incidencias

El entorno Windows produjo una denegación transitoria al indexar un objeto Git
temporal durante la suite completa; no reproduce al repetir el test aislado.

## Detalle

Implementación de vínculo tenant-aware entre una referencia opaca de Person y
un UserProfile de Core, compatible con CoreApi v0.1.0 y publicado como CoreApi
v0.2.0. Incluye biblioteca, WSGI HTTP, puertos/adaptadores, SQL Supabase,
auditoría, pruebas y documentación.

Fuentes: `AGENTS.md`, `CONSTITUTION.md`, `docs/tecnica/arquitectura.md`,
`docs/tecnica/core-contract-v010.md`, código y migraciones vigentes.

Supuesto explícito: el host es la autoridad de autenticación y entrega
`AuthenticatedActor`; Core no puede verificar credenciales sin inventar un
proveedor incompatible. La auditoría no comparte transacción distribuida con
PostgREST y esa limitación queda documentada y testeada en los puertos.
