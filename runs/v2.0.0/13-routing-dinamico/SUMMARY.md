# F08 — Routing dinámico por capacidades y evidencia

Estado: implementación y validación local
Versión: v2.0.0
Tipo: Feature
SDD: FULL
PR: pendiente
Merge: pendiente

## Objetivo

Elegir implementaciones por capacidades requeridas, riesgo, profundidad SDD,
disponibilidad, costo, latencia, contexto y seguridad, sin fijar roles a
proveedores concretos.

## Resultado

`.agentic/models.json` incorpora un catálogo declarativo pequeño de
implementaciones y políticas LIGHT/STANDARD/FULL. `resolve-agentic-model.ps1`
lo consume con selección determinística, fallback compatible y evidencia
JSONL compacta. La evidencia F07 se acepta como señal relativa trazable;
ausencia o evidencia inválida no inventa métricas ni cambia la política base.

## Cambios principales

- Catálogo de capacidades e implementaciones en `.agentic/models.json`.
- Selección determinística y filtros fail-safe en el router existente.
- Evidencia de señales y decisión en JSONL.

## Validación

Se cubren compatibilidad legacy, selección por capacidades y profundidad,
fallback, bloqueo sin candidatos, contexto, disponibilidad, seguridad y
configuración inválida. Los resultados completos quedan en
`test-report-1.md`.

## Decisiones

Se conserva la infraestructura existente y se agrega routing como extensión
provider-agnostic, sin invocar servicios externos.

## Incidencias

Ninguna funcional. La suite completa de 236 tests tarda varios minutos en
Windows por sus escenarios de lifecycle.

## Detalle

La implementación usa configuración declarativa pequeña y aliases sólo como
identidad de implementación, nunca como roles conceptuales.

## Evidencia

- [spec](spec.md) · [plan](plan.md) · [tasks](tasks.md)
- [auditoría](audit-1.md) · [QA](test-report-1.md) · [code review](code-review-1.md)
- [decisión](decision.md)
