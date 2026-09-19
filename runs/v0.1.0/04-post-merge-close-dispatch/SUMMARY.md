# Summary

Estado: READY_FOR_PR
Versión: v0.1.0
Tipo: Feature
SDD: runs/v0.1.0/04-post-merge-close-dispatch/sdd.json
PR: pendiente de creación
Merge: no realizado

## Objetivo

Hacer reejecutable el cierre oficial post-merge sin permitir cierres de PR,
ramas o work units arbitrarias.

## Resultado

El workflow acepta dispatch manual sólo con inputs que forman exactamente una
Feature versionada y continúa usando `close-feature.ps1`.

## Cambios principales

Se agregó `workflow_dispatch` y validación de `pr_number`, `branch`, `version`
y `slug`.

## Validación

Pruebas estructurales y gates de la Template ejecutados.

## Decisiones

La autorización del dispatch no sustituye la comprobación de PR mergeada del
script oficial.

## Incidencias

Issue #3 evidenció que el evento automático no se emitió tras un merge con
`GITHUB_TOKEN`.

## Detalle

No se modificó el guard, el Core, Supabase ni las políticas RLS.

