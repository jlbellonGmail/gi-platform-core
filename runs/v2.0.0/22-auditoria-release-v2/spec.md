# Spec — F17 Auditoría final y release v2.0.0

## Objetivo

Demostrar con evidencia vigente que v2.0.0 es publicable y cerrar F17 mediante
PR, merge y release sin reescribir historia ni crear T05/F18.

## Criterios de aceptación

- AC-1: la auditoría .audit usa el perfil TEMPLATE vigente, registra score,
  riesgos y segunda pasada adversarial.
- AC-2: la suite canónica, evals, integrity, status, security y supply-chain
  tienen resultados reproducibles; los fallos ambientales se separan de
  regresiones.
- AC-3: Planner, Builder y Reviewer permanecen desacoplados por capacidad;
  SDD LIGHT/STANDARD/FULL, convergence, routing, MCP y skills quedan
  verificados con evidencia.
- AC-4: el wait de CI tiene timeout y polling controlado, sin espera infinita.
- AC-5: existe revisión final independiente y code-review vigente sobre el
  diff final; no hay defectos CRITICAL ni HIGH bloqueante.
- AC-6: se crean docs tecnica/22-auditoria-release-v2.md,
  docs usuario/22-auditoria-release-v2.md, decision.md y enlaces exactos
  en ambos índices.
- AC-7: F17 pasa a READY_FOR_PR sólo con contrato completo y no a [x] antes
  del merge; el cierre posterior es idempotente.
- AC-8: el dry-run de release valida develop/main/tag v1.1.0 y la secuencia
  de publicación sin mutar; v2.0.0 sólo se etiqueta después del merge estable.

## Clarificaciones realizadas

No hay decisiones funcionales pendientes. La autorización humana del pedido
permite merge y publicación sólo cuando todos los gates estén verdes.

## Decisiones pendientes bloqueantes

Ninguna.
