# Spec — SDD adaptativo

## Intención

Materializar SDD proporcional en tres profundidades usando exclusivamente la
clasificación producida por ASSESS, preservando el circuito v1.1.0 y evitando
gates o artefactos innecesarios en cambios simples.

## Criterios de aceptación

- AC-1: el motor consume una salida determinista válida de ASSESS y no vuelve
  a calcular riesgo o profundidad.
- AC-2: LIGHT, STANDARD y FULL emiten secuencias y evidencia mínima distintas,
  verificables y alineadas con `fundamentos-v2.md`.
- AC-3: entrada vacía, inválida, no ASSESS o no determinista falla cerradamente.
- AC-4: la salida es auditable, portable, no invoca IA/proveedores/MCP y no
  cambia permisos ni el contrato v1 vigente.
- AC-5: existen tests para las tres profundidades, JSONL y fallos cerrados.
- AC-6: existen `docs/tecnica/sdd-adaptativo.md`,
  `docs/usuario/sdd-adaptativo.md`, este expediente y enlaces exactos en ambos
  índices.
- AC-7: la autorización previa excepcional de esta ejecución queda separada
  de la aprobación HITL normal, explícita y trazable; el gate normal sigue
  rechazando una PR sin aprobación.

## Clarificaciones realizadas

No hubo decisiones funcionales pendientes: la unidad define una capacidad del
Template y las tres secuencias están fijadas por el pedido y fundamentos v2.

## Decisiones pendientes bloqueantes

Vacía.
