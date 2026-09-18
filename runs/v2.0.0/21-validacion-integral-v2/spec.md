# F16 - Validacion integral v2

## Objetivo
Demostrar con evidencia reproducible que los circuitos v2 son coherentes,
seguros, portables y auditables antes de iniciar F17.

## Criterios de aceptacion
- AC-1: Las suites reales, integrity, status, seguridad, MCP, supply-chain y evals se ejecutan y registran con resultado real.
- AC-2: LIGHT, STANDARD y FULL conservan evidencia proporcional y FULL no es el default.
- AC-3: Roles, routing, convergence, governance single/multi-maintainer, stale, paralelizacion, conflictos, maintenance, cierre y cleanup tienen cobertura trazable.
- AC-4: La portabilidad se evalua desde las fuentes canonicas sin adaptar el Template a OpenCode.
- AC-5: v1.1.0 permanece intacta y v2.0.0 no se publica ni se taggea.
- AC-6: Se crean esta evidencia, `docs/tecnica/validacion-integral-v2.md`, `docs/usuario/validacion-integral-v2.md` y sus enlaces exactos.

## Supuestos y clarificaciones
La autorizacion humana del pedido cubre la ejecucion E2E y el merge de esta
feature. El entorno local disponible usa Python 3.14; CI usa Python 3.12.
No hay stack de producto, servidores MCP reales ni telemetria de costo.

## Decisiones pendientes bloqueantes
Ninguna.
