# Propuesta de Fase 00

Planner: subagente funcional, sesión independiente. Alcance: gobernanza v2,
sin runtime nuevo. Instrucción humana vigente autoriza Planner → Reviewer →
Builder → verificación → Reviewer; `chore/*` aplica porque no existía ítem
del roadmap para este bootstrap. No se simula el contrato Feature/Milestone.

## Intención verificable y plan

1. 00.1: elegir `PRINCIPLES.md`, justificándolo primero en arquitectura;
   formalizar los 18 principios con consecuencias operativas.
2. 00.2: tabla de responsabilidades sin fuentes duplicadas; AGENTS dirige
   comportamiento y remite a principios, documentación y roadmap.
3. 00.3: registrar baseline exacta; migración incremental, reversible y
   brownfield; mantener motor v1 hasta sustitución probada.
4. 00.4: matriz de componentes con conservar/simplificar/adaptar/reemplazar/
   eliminar, evidencia y condición de evolución, sin eliminar código ahora.
5. 00.5: invariantes, permisos READ/WRITE/EXEC/NETWORK/SECRETS/MCP/TOOLS/
   PUSH/MERGE/RELEASE/DESTRUCTIVE, límites de autonomía y fail-safe.
6. 00.6: métricas con denominador, umbral y evidencia; separar aceptación
   actual de objetivos futuros. Vincular los 14 problemas v1 a fases.

Documentos: principios; fundamentos técnicos y guía de usuario; enmienda
de transición en AGENTS; arquitectura e índices; ROADMAP maestro v2;
STATUS con contexto manual y observación automática; expediente de evidencia.
No modificar scripts, dependencias, workflows, roles ni adaptadores.

## Supervisor y continuación

Sólo diseño del supervisor mínimo: estados, transiciones, checkpoint,
invalidación de evidencia, falta de progreso y delegación a scripts existentes.
No crear CLI vacía ni implementar ASSESS. La entrada temporal es el
orquestador disponible siguiendo el procedimiento documentado.

Roadmap conserva IDs históricos 00–05. Fase 00 es bootstrap de gobernanza
cuya integración se deriva del estado MERGED de esta PR, sin checkbox
Feature huérfano. Fases 01–17 usan IDs 06–22, indicando la fase en cada ítem.
Cada fase puede concluir justificadamente que no necesita implementación.

## Verificación y revisión

Tests existentes completos disponibles en Windows; CI Linux y Windows;
schemas y adaptadores; diff contra baseline para garantizar motor intacto;
enlaces locales; coherencia de documentación; tag local/remoto inmutable;
STATUS update/check; revisión adversarial independiente sobre diff final.
No se reclama una auditoría global ni una puntuación nueva de `.audit`.
Hallazgos materiales retornan a Builder y se vuelven a verificar.

## Riesgos atendidos

- La arquitectura objetivo no habilita LIGHT ni tres roles en runtime v1.
- Chore requiere merge humano directo; gates Feature no aplican.
- STATUS automático es observación fechada; no puede contener el SHA del
  commit que lo incluirá. Revalidar antes de actuar, sin loops de commits.
- Herramientas de esta sesión no equivalen a Skills/MCP canónicos instalados.
- No copiar cambios ajenos del checkout principal.
