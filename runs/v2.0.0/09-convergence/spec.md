# Spec — F04 Convergence

## Objetivo
Coordinar ciclos autónomos Builder ↔ Reviewer con estado mínimo, progreso
verificable y salida segura proporcional a LIGHT/STANDARD/FULL.

## Criterios de aceptación

- AC-1: consumir ASSESS y SDD sin reclasificar ni redefinir roles.
- AC-2: emitir estados APPROVED, NEEDS_HUMAN_DECISION, BLOCKED y
  FAILED_SAFELY; CHANGES_REQUESTED es intermedio.
- AC-3: representar findings estructurados, progreso y no-progreso, con límite
  configurable y detección de fingerprint repetido.
- AC-4: preservar independencia del Reviewer y agnosticismo de proveedor.
- AC-5: crear `docs/tecnica/convergence.md`, `docs/usuario/convergence.md`,
  `runs/v2.0.0/09-convergence/decision.md` y sus enlaces exactos en ambos
  índices.

## Clarificaciones realizadas
La instrucción humana vigente fija el alcance F04 y autoriza el recorrido
end-to-end. No quedan decisiones pendientes bloqueantes.
