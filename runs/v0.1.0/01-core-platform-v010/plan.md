# Plan — Core Platform v0.1.0

1. Definir entidades inmutables e invariantes de tenancy, identidad y RBAC.
2. Exponer `CoreStore` como port y `InMemoryCoreStore` como adaptador local.
3. Implementar casos de uso en `CoreService` con autorización deny-by-default.
4. Emitir auditoría para mutaciones y decisiones de autorización.
5. Exponer `CoreApi` como contrato transport-neutral SemVer `0.1.0`.
6. Cubrir comportamiento y aislamiento con pytest.
7. Documentar diseño, uso, límites y procedencia; ejecutar gates del repo.
