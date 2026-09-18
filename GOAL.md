# GOAL — GI-PLATFORM-CORE v0.1.0

## Propósito

Construir un núcleo común, neutral respecto del dominio, reusable por
múltiples productos y verticales, independiente de UI y consumible mediante
contratos públicos versionados.

## Problema que resuelve

Evita que cada producto vuelva a implementar tenancy, identidad, membresías,
autorización contextual, aislamiento y auditoría de forma incompatible.

## Responsabilidades del Core

- Modelar `Organization` como entidad principal de tenancy.
- Modelar `Site`, perteneciente a una `Organization`.
- Gestionar identidad base mediante `UserProfile`.
- Gestionar pertenencia multi-tenant mediante `OrganizationMembership`.
- Resolver `Role`, `Permission`, `MembershipRole` y acceso por sede.
- Proveer `TenantContext`, autorización contextual, aislamiento y auditoría.
- Exponer contratos públicos versionados y casos de uso server-side.

## Límites del Core

El Core no depende de Dental ni de ninguna vertical, no contiene UI/UX ni
reglas de negocio verticales. No implementa pacientes, profesionales, Party,
CRM, ventas, compras, facturación, finanzas, inventarios, órdenes de trabajo,
inmobiliaria, cooperativas, chatbot ni Voice.

## Principios arquitectónicos

- Dirección de dependencias: `producto/vertical → Core`.
- Separación: `UI/UX → API/contratos → Application/Use Cases →
  Domain/Business Rules → Ports → Infrastructure/Data`.
- La identidad no concede acceso por sí sola: se requiere membership activa,
  roles, permisos y contexto de Organization/Site cuando corresponda.
- Denegar por defecto y fallar cerrado ante contexto o pertenencia inválidos.
- Sin acceso directo de UI a tablas privadas.
- Contratos públicos versionados con SemVer; v0.1.0 es experimental y
  compatible dentro de la serie `0.1.x` salvo cambios documentados.

## Relación con módulos y verticales

Las verticales consumen los casos de uso y contratos del Core. `gi-vertical-
dental` y `gi-clinicadental` son conceptos separados del Core: el primero
representa una integración vertical y el segundo una aplicación consumidora.
Ninguno se importa ni se referencia desde este repositorio.

## Primera vertical consumidora

La primera aplicación consumidora será `GI-CLINICADENTAL`, fuera del alcance
de este repositorio y sin acceso durante esta implementación.

## Objetivo v0.1.0

Entregar los módulos base de tenancy, identidad y autorización contextual;
contratos JSON consumibles; adaptadores de persistencia/auditoría por ports;
aislamiento entre Organizations; acceso por Site; seguridad básica y pruebas
automatizadas reproducibles.

Chat, Voice, WhatsApp, Web, Mobile y Desktop serán canales futuros que
consuman los mismos casos de uso server-side; no se implementan en v0.1.0.

## Fuera de alcance v0.1.0

Dental y cualquier regla de otras verticales; pacientes, profesionales,
Party, CRM, ventas, compras, facturación, finanzas, inventarios, órdenes de
trabajo, inmobiliaria, cooperativas, chatbot, Voice, UI, proveedores de
identidad externos, base de datos concreta, despliegue y APIs HTTP concretas.

## Condiciones de éxito

- Una Organization puede tener múltiples Sites.
- Un usuario puede pertenecer a múltiples Organizations.
- Ninguna operación autorizada cruza Organizations.
- Los permisos se evalúan contra membership, roles y contexto.
- El acceso por Site se respeta.
- Las operaciones relevantes generan auditoría estructurada.
- Los contratos públicos son serializables y consumibles sin conocer tablas.
- No existen dependencias hacia GI-CLINICADENTAL ni una vertical.
- La documentación, implementación, pruebas y evidencia coinciden.
