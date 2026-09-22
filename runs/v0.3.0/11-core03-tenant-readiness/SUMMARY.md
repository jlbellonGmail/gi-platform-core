# 11-core03-tenant-readiness — Cierre Tenant

Versión: v0.3.0
Estado: READY_FOR_PR
Tipo: Feature
SDD: FULL
PR: pendiente de crear hacia develop
Merge: no autorizado; requiere decisión humana

## Objetivo

Consolidar CORE03 bajo Tenant, verificar Supabase, contratos Python/HTTP,
seguridad multi-tenant, documentación y readiness para consumidores.

## Resultado

Tenant/tenant_id es la denominación canónica de persistencia y contratos
nuevos. Supabase remoto fue validado con tablas, RLS, FKs y funciones de
identidad. Los contratos Organization publicados se conservan como adaptadores
legacy explícitos, sin contaminar la persistencia ni los contratos nuevos.

## Cambios principales

Migración CORE03, adaptador Supabase, contrato v0.3.0, rutas `/v1/tenants`,
documentación de arquitectura/integración y evidencias Template v2.

## Validación

25 pruebas focalizadas pasan; compileall y diff-check pasan. La verificación
remota confirmó tablas Tenant, RLS, 13 FKs, funciones tenant-scoped y ausencia
de objetos/columnas Organization.

## Decisiones

Se preservan temporalmente métodos/rutas/contratos Organization publicados como
adaptadores explícitos porque son contratos existentes; los consumidores nuevos
deben usar Tenant. No se incorporan datos comerciales, suscripciones o billing.

## Incidencias

La migración histórica `rename_sites_to_locations` sólo aplica a instalaciones
que aún tienen `sites`; no se ejecuta sobre una base nueva ya creada con
`locations`.

## Detalle

No se modificaron otros repositorios, no se creó release ni se hizo merge.
