# Summary

Estado: READY_FOR_PR
Versión: v0.1.0
Tipo: Feature
SDD: runs/v0.1.0/03-post-hitl-versioned-evidence/sdd.json
PR: pendiente de creación
Merge: no realizado

## Objetivo

Versionar dinámicamente las rutas de evidencia del gate Post-HITL.

## Resultado

El workflow resuelve autorización, revisión independiente e integridad con
la versión y slug derivados de la rama de la PR.

## Cambios principales

Se eliminaron las rutas rígidas y se agregaron pruebas para más de una versión.

## Validación

Pruebas unitarias y gates de la Template ejecutados en esta work unit.

## Decisiones

La fuente de versión es `steps.feature.outputs.version`, coherente con el
contrato de ramas de Feature.

## Incidencias

El defecto original hacía que Features v0.1.0 buscaran evidencias bajo v2.0.0.

## Detalle

No se tocaron código funcional del Core, datos Supabase ni políticas RLS.

