# Contexto de producto

## Propósito

GI-PLATFORM-CORE es un núcleo común, neutral respecto del dominio y reusable
por múltiples productos y verticales.

## Modelo funcional estable de v0.1.0

- `Organization` es la entidad principal de tenancy.
- `Site` pertenece a una `Organization`.
- Un usuario puede pertenecer a múltiples Organizations mediante
  `OrganizationMembership`.
- La autorización combina identidad, membership, roles, permisos,
  Organization y Site/contexto.
- El aislamiento entre Organizations es una invariante del Core.

## Verticales y canales

El Core no depende de Dental ni de ninguna vertical. La primera aplicación
consumidora será `GI-CLINICADENTAL`; `gi-vertical-dental` y `gi-clinicadental`
son conceptos separados del Core. Chat, Voice, WhatsApp, Web, Mobile y
Desktop son canales futuros que consumen los mismos casos de uso server-side.

Las reglas específicas de Dental y de cualquier otra vertical permanecen
fuera de este documento y de este repositorio.

## Procedencia

La infraestructura inicial proviene de Template v2.0.0, SHA
`f5d4b6cc029c34c0d0c05831bfd28134276fa167`.
