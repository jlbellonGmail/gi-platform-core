# Spec F07

## Criterios de aceptación

- AC-1: existe una suite declarativa de diez escenarios A–J que cubre
  profundidad, roles, convergencia, escalamiento, bloqueo, no-progress,
  stale review, evidencia insuficiente y fuera de alcance.
- AC-2: el runner produce JSONL reproducible con expected, actual, pass,
  reason, métricas, versión de suite y RunId, y falla opcionalmente con código
  no cero.
- AC-3: los perfiles smoke/normal/full son selecciones deterministas y las
  métricas son comprensibles.
- AC-4: escenarios y resultados no contienen identidad de proveedor/modelo;
  `.audit` y tests determinísticos permanecen separados.
- AC-5: se crean `docs/tecnica/agentic-evals.md`,
  `docs/usuario/agentic-evals.md`, `runs/v2.0.0/12-agentic-evals/decision.md`
  y enlaces exactos en ambos índices.

## Clarificaciones realizadas

Ninguna: el pedido humano define explícitamente alcance, escenarios y
separación con F08.

## Decisiones pendientes bloqueantes

Ninguna.
