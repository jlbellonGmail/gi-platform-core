# T01 — Normalización documental transversal

Estado: DONE
Versión: v2.0.0
Tipo: Maintenance / Transversal
PR: #33 — [v2.0.0][T01] Normalización documental transversal
Merge: 038d61b

## Objetivo

Reducir ambigüedad documental entre F02 y F03 sin crear una fase funcional
ni imponer artefactos SDD innecesarios.

## Resultado

Se adoptó `CONSTITUTION.md`, se ordenaron ROADMAP y STATUS para lectura
humana, se versionaron los runs y se añadió soporte explícito de identidad
versionada para futuras features.

## Cambios principales

- runs históricos clasificados en `v1.1.0` y `v2.0.0` sin duplicación.
- SUMMARY uniforme para cada run relevante.
- `fundamentos-v2` quedó como referencia técnica, no como fuente operativa.
- T01 permanece separada de F01–F17 y F03 sigue pendiente.

## Validación

Regresión pytest, proyección de `start-work-unit`, contrato y verificación
de enlaces se ejecutan antes de publicar la PR.

## Decisiones

La compatibilidad legacy de scripts se conserva cuando es ejercida por el
circuito existente; la interfaz versionada es explícita mediante `-Version`.

## Incidencias

Ninguna conocida dentro del alcance.

## Detalle

[spec](spec.md) · [plan](plan.md) · [tasks](tasks.md) · [audit](audit-1.md) ·
[QA](test-report-1.md) · [code review](code-review-1.md) · [decision](decision.md)
