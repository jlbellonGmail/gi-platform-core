# F10 — MCP y herramientas externas por capacidad

Estado: en validación  
Versión: v2.0.0  
Tipo: Feature  
SDD: FULL  
PR: pendiente  
Merge: pendiente

## Objetivo

Formalizar capacidades externas MCP bajo demanda sin introducir integraciones hipotéticas.

## Resultado

La necesidad demostrada era reparar el schema referenciado por `.agentic/mcp.json` y expresar capacidad, modo, riesgo, permisos, requisitos y carga bajo demanda. El catálogo permanece vacío porque no hay una necesidad externa de negocio.

## Cambios principales

Se agrega el schema MCP y `scripts/mcp-tools.ps1`, que devuelve `ALLOW`, `DENY`, `FALLBACK` o `BLOCKED` consumiendo la política F11. No ejecuta red ni acciones.

## Validación

241 tests verdes; adaptadores sincronizados; schema, fallback, autorización, secretos faltantes y configuración inválida cubiertos con mocks/fakes.

## Decisiones

Read-only consume `NETWORK_READ`; write/action consume `EXTERNAL_WRITE`. No se crean servidores, Skills artificiales, routing F08 ni supply chain F12.

## Incidencias

Ninguna funcional. ASSESS fue repetido con las rutas completas tras una invocación incompleta.

## Detalle

Ver `sdd.json`, `assess.jsonl`, `spec.md`, `plan.md`, `tasks.md`, `decision.md`, QA y code review en este run.
