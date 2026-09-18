# F06 — Tests, CI y `.audit`

Estado: DONE · Versión: v2.0.0 · Tipo: Feature
PR: [#46](https://github.com/jlbellonGmail/template/pull/46) · Merge: `43cbf9b`

## Objetivo

Base mínima profesional y determinística para tests, CI y auditoría global.

## Resultado

La suite existente se conserva por valor; se agregan invariantes de `.audit`
y se robustece el launcher Windows con argumentos `-File`. CI mantiene
`circuit`, `product` y reconciliación como responsabilidades separadas.

## Validación

La suite focalizada, el contrato y los adaptadores pasan. CI de la PR y de
`develop` quedaron verdes. Los tres timeouts históricos se investigaron y se
resolvieron separando el launcher del motor de lifecycle: el job Windows
mantiene ambos gates y los escenarios de cierre se ejecutan en foreground
para no depender del árbol de procesos del host.

## Decisiones

`.audit` no se fusiona con Reviewer ni se convierte en scoring agentic. No se
inicia ninguna fase posterior.

## Paralelización futura

F07 requiere esta base y queda pendiente. F09 y F11 pueden evaluarse en
paralelo por dependencias reales cuando corresponda; F08 espera evidencia de
F07 y F10 espera la política relevante de seguridad si se afectan permisos o
confianza.

## Incidencias

La limitación ambiental local queda documentada; no hay evidencia de un bug
reproducible en CI. Las advertencias de Node.js 20 en Actions no bloquean.

## Evidencia

[spec](spec.md) · [plan](plan.md) · [tasks](tasks.md) · [audit](audit-1.md) ·
[QA](test-report-1.md) · [code review](code-review-1.md) · [decision](decision.md)
