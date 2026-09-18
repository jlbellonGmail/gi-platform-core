# Spec: 00-fuente-unica-router-modelos

## Objetivo

Evolucionar el template para que la configuracion agentica tenga una
fuente canonica multiherramienta y para que OpenCode pueda resolver
modelos de forma controlada antes de iniciar una etapa.

## Alcance

- Centralizar roles, modelos, fallback, MCP y skills portables en
  `.agentic/` y `.agents/skills/`.
- Regenerar adaptadores de Claude Code, Codex y OpenCode desde esa fuente.
- Agregar un router OpenCode-first con `run.yaml`, allowlists, variantes
  separadas del modelo, fallback Go -> Zen -> OpenRouter explicito y
  evidencia `model-routing.jsonl`.
- Agregar gate post-HITL para que una PR aprobada se mergee solo si
  Actions queda en verde despues de la aprobacion.

## Criterios de aceptacion

- Existe `docs/tecnica/fuente-unica-router-modelos.md`.
- Existe `docs/usuario/fuente-unica-router-modelos.md`.
- Existe `runs/v1.1.0/00-fuente-unica-router-modelos/decision.md`.
- `docs/tecnica/index.md` contiene exactamente un enlace a
  `fuente-unica-router-modelos.md`.
- `docs/usuario/index.md` contiene exactamente un enlace a
  `fuente-unica-router-modelos.md`.
- `scripts/sync-agentic-adapters.ps1 -Check` valida adaptadores generados.
- Los tests del router y del gate post-HITL pasan sin consumir creditos
  reales.
- `ROADMAP.md` queda en `[-]` antes del merge y no se marca `[x]` hasta
  que la PR sea mergeada contra `develop`.
