# GI-PLATFORM-CORE v0.1.0

GI-PLATFORM-CORE ofrece capacidades comunes para productos y verticales:
Organizations, Sites, identidad, memberships, roles, permisos, autorización
contextual, aislamiento y auditoría.

Una persona puede pertenecer a varias Organizations. Cada Site pertenece a
una sola Organization y el acceso a un Site se concede explícitamente en la
membership. Para autorizar una operación se envía el usuario, la
Organization, el permiso y opcionalmente el Site; el Core responde una
decisión versionada y registra la comprobación.

La primera aplicación consumidora prevista es `GI-CLINICADENTAL`, pero esa
aplicación, `gi-vertical-dental` y sus reglas de dominio están fuera de este
repositorio. Chat, Voice, WhatsApp, Web, Mobile y Desktop son canales futuros
que usarán los mismos casos de uso server-side.

La integración actual es transport-neutral mediante `CoreApi`; no expone
tablas ni requiere una UI o una base de datos concreta.
