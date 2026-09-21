# Plan

1. Extender dominio/puertos con relación opaca y operaciones atómicas.
2. Implementar reglas de resolución, autorización, aislamiento, idempotencia y
   auditoría en CoreService/CoreApi.
3. Implementar adaptadores InMemory/Supabase y migración SQL segura.
4. Implementar WSGI inyectando autenticación del host.
5. Publicar contrato/manifest v0.2.0, documentación y runner local.
6. Ejecutar tests unitarios, de contrato, adaptador, HTTP, cross-tenant,
   concurrencia, supply-chain y contrato de work unit.
