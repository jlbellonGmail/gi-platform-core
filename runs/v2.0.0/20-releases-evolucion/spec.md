# Spec F15 — Releases y evolución determinísticos

## Objetivo

Definir una validación reproducible de candidatos SemVer y dejar explícito el
flujo `develop` → `main` → tag → release, sin publicar v2.0.0 durante F15.

## Criterios de aceptación

- AC-1: un gate read-only valida versión, branch, SHA, árbol, ROADMAP, CI,
  integridad, main/develop, tag y evidencia de F17.
- AC-2: un candidato prematuro o con cualquier condición negativa se rechaza.
- AC-3: tags son inmutables y v1.1.0 conserva objeto anotado y commit exacto.
- AC-4: el flujo documenta PR develop→main, metadata breve, hotfix y runs por
  versión, sin invadir F16/F17 ni rehacer F12.
- AC-5: crear `docs/tecnica/releases-evolucion.md`,
  `docs/usuario/releases-evolucion.md`, `runs/v2.0.0/20-releases-evolucion/decision.md`
  y enlaces exactos en ambos índices.

## Supuestos y clarificaciones

SemVer usa la forma `vMAJOR.MINOR.PATCH`. F15 prepara el mecanismo; F17 es la
única unidad que puede decidir/publicar v2.0.0. F12 continúa siendo la fuente
de supply-chain y CI.

## Decisiones pendientes bloqueantes

Ninguna.
