# 10-evidencias-adaptativas

Estado: mergeada y cerrada
Versión: v2.0.0
Tipo: Feature
SDD: FULL
PR: #42
Merge: sí

## Objetivo
Hacer proporcional la evidencia al nivel SDD, manteniendo SUMMARY como entrada humana.

## Resultado
Contrato adaptativo implementado con compatibilidad legacy y validación semántica de SUMMARY, JSON máquina y veredictos vigentes.

## Cambios principales
- LIGHT, STANDARD y FULL tienen requisitos declarativos distintos.
- ready-for-pr consume la política y no enlaza archivos inexistentes.
- Convergencia JSON se valida sin documento por iteración.

## Validación
6 escenarios F05 y 48 pruebas focalizadas pasaron; `Assert-WorkUnitContract` valida el run.

## Decisiones
`sdd.json` es la frontera adaptativa; sin él se preserva legacy.

## Incidencias
Ninguna funcional. F06 queda fuera de alcance.

## Detalle
[spec](spec.md) · [plan](plan.md) · [tasks](tasks.md) · [audit](audit-1.md) · [QA](test-report-1.md) · [code review](code-review-1.md) · [decision](decision.md) · [evidencia SDD](sdd.json) · [convergencia](convergence.json)

## Paralelización futura
F06 debe seguir secuencialmente para revisar tests, CI y `.audit`. No se inicia ninguna fase aquí.

