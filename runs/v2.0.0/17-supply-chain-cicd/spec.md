# Spec F12 — Supply chain y CI/CD profesional

## Objetivo

Reducir riesgos concretos de automatización preservando gates, Windows y el
desacople del stack de producto.

## Criterios de aceptación

- AC-1: toda Action externa crítica usa SHA completo y versión comentada.
- AC-2: workflows con permisos mínimos y sin `write-all`.
- AC-3: dependencias del circuito y Docs reproducibles con versiones fijas.
- AC-4: gate PowerShell con pruebas negativas para pinning y dependencias.
- AC-5: docs técnica/usuario, `decision.md` y enlaces exactos en índices.
- AC-6: F15 no se implementa; release readiness queda documentado.

## Supuestos y clarificaciones

El template no tiene producto ni stack Node; no hay decisión material pendiente.
