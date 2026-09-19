# 02-supabase-gi-dev-validation

Estado: validado localmente; pendiente PR.
Versión: v0.1.0.
Tipo: Feature.
SDD: FULL.
PR: pendiente.
Merge: no realizado.

## Objetivo

Preparar y validar de forma reproducible el acceso RLS autenticado de gi-dev
con datos sintéticos mínimos y sin modificar políticas.

## Resultado

El procedimiento interactivo quedó implementado y ejecutado exitosamente
contra gi-dev con credenciales introducidas localmente por el operador.

## Cambios principales

- Bootstrap idempotente mediante `CoreService` y `SupabaseCoreStore`.
- Preflight exacto del project ref y validación de aislamiento RLS.
- Documentación y prueba unitaria del procedimiento.

## Validación

La validación autenticada pasó: nueve tablas HTTP 200, una organization
visible y aislamiento RLS sintético aprobado. Los gates finales de la Feature
continúan en ejecución.

## Decisiones

No se crean roles, permisos, locations ni accesos; no se modifican policies.

## Incidencias

La ejecución externa usó interacción local segura y una clave server-side
exclusiva de gi-dev; ningún secreto quedó en evidencia.

## Detalle

La evidencia final debe registrar sólo estados, conteos y veredictos; nunca
JWTs, contraseñas, claves, IDs sensibles ni payloads de autenticación.
