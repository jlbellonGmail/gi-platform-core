# F04 — Convergence autónoma Builder–Reviewer

Estado: mergeada y cerrada  
Versión: v2.0.0  
Tipo: Feature  
PR: #39  
Merge: 21e601d

## Objetivo
Coordinar correcciones Builder ↔ Reviewer con progreso verificable y salida segura.

## Resultado
Contrato JSON determinístico con aprobación, escalamiento, bloqueo y fallo seguro; ciclos proporcionales ASSESS/SDD.

## Cambios principales
`scripts/convergence.ps1`, pruebas pytest y documentación mínima técnica y de usuario.

## Validación
211 tests de circuito pasaron localmente sin la suite Windows lenta del reconciliador; CI pasó `circuit-tests`, `local-reconciler-tests` y `product-tests`.

## Decisiones
Presupuesto por defecto 2/4/6; `MaxIterations` permite extensión sin acoplar modelos. Reviewer permanece independiente y Builder no aprueba.

## Incidencias
El primer workflow post-HITL fue rechazado por ausencia de GitHub Review; el merge autorizado se ejecutó después mediante el gate local scoped. Ningún residuo de implementación.

## Detalle
[spec](spec.md) · [plan](plan.md) · [tasks](tasks.md) · [audit](audit-1.md) · [QA](test-report-1.md) · [code review](code-review-1.md) · [decision](decision.md)

## Paralelización futura
F05 consume esta salida; F06/F07 dependen de contratos posteriores. F08 puede avanzar con sus prerrequisitos propios, sin iniciar aquí ninguna fase.
