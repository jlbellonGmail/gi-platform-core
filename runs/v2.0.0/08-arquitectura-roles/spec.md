# Spec: Arquitectura de roles por capacidades

## Identificación
- Work unit: 08-arquitectura-roles
- Modo: FEATURE
- Versión: v2.0.0 / F03

## Alcance
Reducir la arquitectura conceptual a Planner, Builder y Reviewer, definidos
por responsabilidades y capacidades, consumiendo ASSESS y SDD adaptativo.
Conservar compatibilidad operacional mediante aliases históricos. No incluye
CONVERGENCE, routing dinámico completo ni F04.

## Contexto y fuentes
ROADMAP identifica F03 como arquitectura de roles. CONSTITUTION exige roles
por capacidad, determinismo y complejidad proporcional. F01 aporta ASSESS
determinista y F02 LIGHT/STANDARD/FULL. El código actual confirma cinco
adaptadores y un router por rol; el solapamiento real es QA/code review con
Reviewer. T01 confirma runs versionados. La instrucción humana vigente fija
la arquitectura objetivo y la autorización de cierre.

## Criterios de aceptación
- AC-01: Existen sólo Planner, Builder y Reviewer como roles canónicos, con capacidades explícitas.
- AC-02: Ningún rol canónico está ligado conceptualmente a proveedor o modelo; aliases históricos no crean agentes.
- AC-03: Reviewer absorbe QA, code review y validación, conserva independencia y Builder no puede autoaprobarse.
- AC-04: Planner consume ASSESS y la profundidad LIGHT/STANDARD/FULL existente sin reimplementarla ni modificar F04.
- AC-05: Adaptadores se regeneran desde `.agentic/` y routing/lifecycle/autorización existentes siguen funcionando.
- AC-06: El mensaje de `start-work-unit.ps1` usa la ruta versionada real.
- AC-07: Existen docs técnica/usuario, decisión, índices exactos y SUMMARY de F03.
- AC-08: Tests de regresión y validaciones determinísticas quedan verdes.

## Casos borde a contemplar
Alias histórico solicitado; adaptador generado obsoleto; ruta legacy sin existir;
ASSESS inválido; SDD LIGHT; Reviewer ejecutado con el mismo modelo físico;
estado ROADMAP/STATUS inconsistente.

## Supuestos
Los nombres de artefactos del contrato v1 se preservan aunque las capacidades
se consoliden. ASSESS sigue siendo la única fuente de riesgo/profundidad.

## Clarificaciones realizadas
No fueron necesarias: la instrucción humana vigente y la evidencia del repo
resuelven el alcance material.

## Decisiones pendientes bloqueantes
Ninguna.
