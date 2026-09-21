# SUMMARY — Release readiness alineado al ROADMAP

Versión: v0.2.1  
Estado: en implementación  
Tipo: Feature  
SDD: FULL  
PR: pendiente de crear hacia develop  
Merge: no autorizado; requiere decisión humana

## Objetivo

Eliminar la dependencia rígida del gate de release respecto de fases históricas
de la Template y validar el alcance explícito de cada release contra el
ROADMAP vigente de Core.

## Alcance

- `scripts/release-readiness.ps1`
- pruebas de regresión del gate
- documentación técnica y evidencia versionada
- versión patch del paquete por la corrección de gobernanza

## Criterios de aceptación

1. El gate lee `runs/<version>/release-readiness/manifest.json`.
2. Rechaza items inexistentes, ambiguos o no cerrados.
3. Conserva los controles de árbol limpio, SHA, CI, integridad, tags y
   ancestro histórico.
4. No crea tags, releases, PRs ni cambios remotos.
5. No contiene referencias a las fases históricas 18–22.

## Resultado

Implementación preparada para validación QA y revisión independiente.

## Cambios principales

Gate de release, pruebas, documentación, manifiesto de alcance y versión patch.

## Validación

Las regresiones específicas pasan; los gates finales se ejecutarán sobre el
commit candidato.

## Decisiones

El manifiesto versionado es la fuente de alcance del candidato y el gate no
publica ni modifica estado remoto.

## Incidencias

La release v0.2.0 histórica no se modifica; la corrección se entrega como
v0.2.1.

## Detalle

Se mantiene la compatibilidad de los contratos públicos de Core; el cambio es
de gobernanza y empaquetado.
