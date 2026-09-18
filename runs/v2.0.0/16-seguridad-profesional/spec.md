# Spec — F11 Seguridad profesional

## Objetivo

Establecer controles determinísticos de seguridad proporcionales al riesgo,
preservando autonomía local y separación Builder/Reviewer/HITL.

## Criterios de aceptación

- AC-1: existe una política provider/model agnostic con capacidades READ,
  MODIFY_LOCAL, EXECUTE, NETWORK, GIT/REMOTE WRITE, MERGE, DESTRUCTIVE y
  SECRET_ACCESS, con perfiles LIGHT/STANDARD/FULL y deny por defecto.
- AC-2: el validador bloquea política inválida, scope de otra unidad, acción o
  rama distinta y secretos en autorización.
- AC-3: CI declara sólo lectura y no persiste credenciales en jobs de lectura.
- AC-4: la política clasifica MCP read-only, MCP write/action y credenciales
  para que F10 pueda consumirla; F10 no se implementa.
- AC-5: workflows y lifecycle conservan aislamiento, PR, aprobación vigente,
  HEAD actual, fail-safe y cleanup acotado.
- AC-6: existen docs/tecnica/seguridad-profesional.md,
  docs/usuario/seguridad-profesional.md y enlaces exactos en ambos índices.
- AC-7: existe runs/v2.0.0/16-seguridad-profesional/decision.md y negative
  tests focalizados; no se implementa F12.

## Clarificaciones realizadas

La instrucción humana confirma máxima autonomía compatible con riesgo, sin
vault propio, sin MCP y sin supply-chain completa.

## Decisiones pendientes bloqueantes

Ninguna.
