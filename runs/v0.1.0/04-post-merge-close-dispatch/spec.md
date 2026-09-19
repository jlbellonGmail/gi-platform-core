# Spec: 04-post-merge-close-dispatch

## Objetivo

Permitir ejecutar de forma manual y validada el workflow oficial de cierre
post-merge cuando GitHub no emite el evento `pull_request_target: closed`
por tratarse de un merge realizado con `GITHUB_TOKEN`.

## Alcance

Sólo se modifica el workflow de cierre y sus pruebas estructurales. El cierre
sigue delegándose en `scripts/close-feature.ps1`, que verifica que la PR esté
mergeada contra `develop`.

## Criterios de aceptación

- El workflow conserva el disparador automático existente.
- `workflow_dispatch` exige PR, rama, versión y slug.
- Los inputs deben corresponder exactamente a una rama Feature versionada.
- El script oficial sigue siendo el único mecanismo que modifica ROADMAP.
- No se relaja el guard de `develop` ni se usa force-push.

