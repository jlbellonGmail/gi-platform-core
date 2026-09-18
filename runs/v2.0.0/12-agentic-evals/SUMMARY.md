# F07 — Agentic Evals reproducibles

Estado: en validacion
Versión: v2.0.0
Tipo: Feature
SDD: FULL
PR: #52
Merge: pendiente

## Objetivo

Medir comportamiento observable del circuito con escenarios pequeños,
repetibles y agnósticos de proveedor/modelo, sin reemplazar los tests
determinísticos ni absorber `.audit`.

## Resultado

Runner declarativo en `scripts/agentic-evals.ps1`, diez escenarios versionados
en `evals/scenarios.json`, perfiles smoke/normal/full y resultados JSONL aptos
para consumo posterior de F08.

## Cambios principales

Runner PowerShell, fixtures declarativos, schema de resultados, pruebas
focalizadas y documentación técnica/usuario.

## Validación

Los diez escenarios pasan con `normal` y `full`; smoke ejecuta A/C/G. La suite
focalizada valida perfiles, fallo explicable, estructura y agnosticismo.

## Métricas

El resumen reporta pass rate, decisiones correctas, escalamientos,
convergencias exitosas, loops evitados y desviaciones de alcance detectadas.

## Alcance

F08 no se implementa: no hay routing ni selección de capacidades por modelo.

## Decisiones

Se usa comparación declarativa local y JSONL estable; no se añaden servicios
externos ni dependencias.

## Incidencias

Ninguna funcional conocida.

## Detalle

Ver documentación técnica, usuario y artefactos del run enlazados abajo.

## Evidencia

- [spec](spec.md) · [plan](plan.md) · [tasks](tasks.md)
- [ASSESS](assess.jsonl) · [resultados](eval-results.jsonl)
- [audit](audit-1.md) · [QA](test-report-1.md) · [code review](code-review-1.md)
- [decision](decision.md)
