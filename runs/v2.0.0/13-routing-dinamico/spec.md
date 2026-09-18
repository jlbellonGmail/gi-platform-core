# Spec F08

## Intención

Separar rol, capacidad, implementación y proveedor, y resolver la opción
adecuada a cada tarea con reglas declarativas y auditables.

## Criterios de aceptación

- AC-1: el router selecciona por capacidades y no por nombre fijo de proveedor.
- AC-2: LIGHT pondera eficiencia, STANDARD equilibrio y FULL calidad.
- AC-3: disponibilidad, contexto, seguridad y fallback se validan fail-safe.
- AC-4: consume `runs/v2.0.0/12-agentic-evals/eval-results.jsonl` como señal
  relativa, sin inventar métricas.
- AC-5: cada resolución registra rol, señales, selección, motivo y fallback
  en JSONL; Builder y Reviewer conservan separación lógica.
- AC-6: se crean `docs/tecnica/13-routing-dinamico.md`,
  `docs/usuario/13-routing-dinamico.md`, `decision.md` y enlaces exactos en
  ambos índices.

## Clarificaciones realizadas

No fueron necesarias: el objetivo, F07 y F11 aportan las decisiones
autoritativas requeridas.

## Decisiones pendientes bloqueantes

Ninguna.
