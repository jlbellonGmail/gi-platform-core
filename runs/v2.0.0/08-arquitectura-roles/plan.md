# Plan: Arquitectura de roles por capacidades

## 1. Arquitectura afectada
`.agentic/agents.json`, `.agentic/models.json` y prompts canónicos pasan a
definir tres roles. Los adaptadores se regeneran. Scripts determinísticos,
contratos, lifecycle y workflows permanecen, salvo aliases de migración y el
mensaje versionado. F04 queda fuera.

## 2. Componentes y contratos nuevos/modificados
Planner recibe objetivo/contexto/restricciones/ASSESS/profundidad y devuelve
plan, riesgos, dependencias y evidencia (AC-01, AC-04). Builder materializa y
prueba (AC-01, AC-03). Reviewer emite APPROVED/CHANGES_REQUESTED/BLOCKED y
absorbe validaciones (AC-03). `roleAliases` permite entradas históricas sin
publicarlas como roles (AC-02, AC-05).

## 3. Compatibilidad y migración
Runs v1.1, artefactos `audit`, `test-report` y `code-review`, scripts y
workflows no se renombran. El router traduce aliases a capacidades canónicas.
No hay migración de datos ni cambio de stack (AC-05).

## 4. Dependencias
No se agregan dependencias. Se reutilizan ASSESS, materialize-sdd, pytest,
PowerShell, git y CI existentes (AC-04, AC-08).

## 5. Impacto operacional
Se ejecuta sync para generar tres adaptadores; `start-work-unit` muestra
`runs/v2.0.0/<slug>/spec.md`. La revisión sigue siendo independiente y los
gates determinísticos siguen siendo obligatorios (AC-03, AC-06).

## 6. Estrategia de tests
Schema/sync comprueban roles y mirrors; router comprueba aliases; tests de
start-work-unit comprueban ruta versionada; regresión pytest, contrato,
ASSESS/SDD y workflows cubren AC-04, AC-05 y AC-08.
