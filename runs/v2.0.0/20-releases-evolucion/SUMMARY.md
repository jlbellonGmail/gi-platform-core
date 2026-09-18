# F15 — Releases y evolución determinísticos

Estado: en implementación · Versión: v2.0.0 · Tipo: Feature · SDD: FULL · PR: pendiente · Merge: pendiente

## Objetivo

Preparar un mecanismo profesional para validar releases sin depender de memoria humana.

## Resultado

Se agrega un gate read-only SemVer, parametrizado por versión, que bloquea releases prematuras y protege tags históricos.

## Cambios principales

`release-readiness.ps1`, generalización de integridad por versión y documentación de release/hotfix.

## Validación

Pendiente de ejecución final del circuito en esta rama.

## Decisiones

F15 no publica v2.0.0; F17 consume el mecanismo.

## Incidencias

La publicación remota requiere la PR y decisión humana previstas por el contrato.

## Detalle

Ver spec, plan, tasks, audit, QA, code review y documentación enlazada.
