# F06 — Tests, CI y `.audit`

## Objetivo

Consolidar validaciones determinísticas, reproducibles y proporcionales para
el circuito v2 sin acoplarlo a modelos, proveedores ni stack de producto.

## Criterios de aceptación

- AC-1: pytest protege contratos, regresiones, lifecycle y escenarios negativos
  de F01–F05 con mensajes accionables y sin duplicación intencional.
- AC-2: CI conserva jobs separados para circuito, producto y reconciliación
  Windows; los tres gates son explícitos y bloqueantes donde corresponde.
- AC-3: `.audit` conserva su perfil TEMPLATE, reglas, evidencia e informes
  independientes de Reviewer y de `runs/`.
- AC-4: LIGHT/STANDARD/FULL mantienen validación proporcional mediante el
  contrato adaptativo existente; F06 no agrega scoring agentic.
- AC-5: los timeouts Windows del reconciliador quedan diagnosticados y
  distinguen limitación ambiental local de fallo reproducible en CI.
- AC-6: se documenta la separación de product-tests y la recomendación de
  paralelización, sin iniciar F07–F17.
- AC-7: existen `docs/tecnica/tests-ci-audit.md`,
  `docs/usuario/tests-ci-audit.md`, sus enlaces exactos, este run y
  `decision.md`.

## Decisiones pendientes bloqueantes

Ninguna.
