# Spec: 03-post-hitl-versioned-evidence

## Objetivo

Corregir el gate Post-HITL para que las evidencias se resuelvan usando la
versión y el slug derivados de la rama de la PR.

## Alcance

El cambio se limita al workflow de gobernanza y a pruebas estáticas. No
modifica el Core, Supabase ni las políticas RLS.

## Criterios de aceptación

- No existe una ruta `runs/v2.0.0` rígida en el workflow.
- Las tres evidencias usan `steps.feature.outputs.version` y `slug`.
- Versiones distintas producen directorios de evidencia distintos.

