# Decisiones: 03-adopcion-proyecto-existente

Este archivo registra decisiones demostrables tomadas durante spec, plan,
tasks, auditoría e implementación de esta feature. No afirma aprobación
de merge: esa aprobación es exclusiva del HITL en GitHub (paso 9 del
circuito descrito en `AGENTS.md`).

## D-1: Incluir `scripts/check-adoption-conflicts.ps1` en el alcance

El ítem `03-adopcion-proyecto-existente` de `ROADMAP.md` delega
explícitamente en el analyst la decisión de incluir o no un script de
detección de colisiones ("Decide vos, como analyst, si este script entra
en el alcance..."). `spec.md` (sección "Contexto y fuentes",
"Justificación de incluir el script en el alcance") documenta esta
decisión: se incluye porque es de complejidad acotada (solo existencia
de rutas vía `Test-Path`, sin diff de contenido ni dependencia de
historial de git), sigue el mismo patrón ya validado en
`scripts/*.ps1` + `tests/*.py` (ver `tests/test_agentic_sync_scripts.py`
como referencia de patrón) y aporta valor real y repetible como
pre-chequeo antes de mezclar el template, o post-chequeo para confirmar
qué quedó pisado. Se descarta explícitamente extenderlo a diff de
contenido o inferencia por historial de git por desproporcionado frente
al valor, documentado como límite explícito en
`docs/tecnica/adopcion-proyecto-existente.md` (sección "Límites de
`scripts/check-adoption-conflicts.ps1`"), no como trabajo pendiente
oculto.

Implementación resultante: `scripts/check-adoption-conflicts.ps1`
(parámetro `-TargetPath`, default `.`), solo lectura, con una tabla
interna `[ordered]` de rutas conocidas agrupadas por los mismos 7+4
elementos que el checklist de `docs/tecnica/adopcion-proyecto-existente.md`.

## D-2: Alcance de la tabla de rutas conocidas del script

La tabla interna del script se mantiene manualmente alineada con el
checklist de `docs/tecnica/adopcion-proyecto-existente.md` (no se
genera parseando el Markdown). Rutas cubiertas, una por cada elemento:

- `.agentic/` → la carpeta completa (`.agentic`).
- `scripts/` → los 11 scripts reales del circuito, nombrados
  explícitamente (`resolve-agentic-model.ps1`,
  `sync-agentic-adapters.ps1`, `update-doc-indexes.ps1`,
  `wait-pr-ci.ps1`, `start-work-unit.ps1`, `workunit-lib.ps1`,
  `local-feature-reconcile.ps1`, `close-feature.ps1`,
  `feature-contract.ps1`, `complete-approved-pr.ps1`,
  `ready-for-pr.ps1`).
- `runs/` → la carpeta completa.
- `docs/tecnica/` → `index.md`, `arquitectura.md`, `circuito-agentico.md`.
- `docs/usuario/` → `index.md`, `circuito-agentico.md`.
- `AGENTS.md` → el archivo.
- Los 4 workflows de `.github/workflows/` (`ci.yml`, `docs.yml`,
  `post-hitl-merge-gate.yml`, `post-merge-close-feature.yml`) →
  individualmente, cada uno su propio elemento en el reporte agrupado
  del script (misma agrupación que el checklist de AC-1 en `spec.md`).

Esta lista fue verificada contra el contenido real de `scripts/` y
`.github/workflows/` de este repositorio antes de escribirla (`ls
scripts/*.ps1`, `ls .github/workflows/`), no inventada.

## D-3: Contrato de exit codes del script

`scripts/check-adoption-conflicts.ps1` termina con:

- Código de salida distinto de cero (falla temprana, antes de imprimir
  ningún reporte de colisiones) si `$TargetPath` no existe o existe pero
  no es un directorio — cubre el caso borde de `spec.md` ("Ruta destino
  inexistente o no es un directorio"), evitando reportar "sin
  colisiones" por una ruta inválida (AC-3, caso borde correspondiente).
- Código `0` si, tras validar la ruta, ninguna ruta conocida existe en el
  destino (AC-4).
- Código `1` si al menos una ruta conocida existe en el destino (AC-4).

Verificado manualmente (ver `test-report` de QA para el detalle
reproducible) contra: directorio vacío (exit 0), directorio con al menos
una ruta conocida de cada categoría precreada (exit 1, reporte agrupado
por elemento), ruta inexistente (exit distinto de cero, mensaje
explícito "no existe"), y ruta que es un archivo en vez de directorio
(exit distinto de cero, mensaje explícito "no es un directorio" — caso
adicional cubierto además del mínimo pedido por AC-3).

## D-4: Límite conocido y no resuelto de acceso denegado

Siguiendo la observación no bloqueante de `audit-1.md`, se documenta (no
se resuelve con lógica adicional) que `Test-Path` de PowerShell puede
devolver `$false` ante una ruta con acceso denegado, lo que el script
reportaría como "no existe" en vez de "no se pudo inspeccionar". Ver
`docs/tecnica/adopcion-proyecto-existente.md`, sección "Límites de
`scripts/check-adoption-conflicts.ps1`", último punto. Se decide no
agregar manejo especial (por ejemplo, intentar `Get-Item` con captura de
excepción de acceso) porque el spec no lo exige como criterio de
aceptación y el auditor lo marcó explícitamente como no bloqueante, a
criterio del builder.

## D-5: No se toca ningún archivo preexistente fuera de alcance

Confirmado (AC-8, T-07) que el diff de esta feature contra `develop` solo
agrega archivos nuevos: `docs/tecnica/adopcion-proyecto-existente.md`,
`docs/usuario/adopcion-proyecto-existente.md`,
`scripts/check-adoption-conflicts.ps1`,
`tests/test_check_adoption_conflicts.py`,
`runs/v1.1.0/03-adopcion-proyecto-existente/*`, más las ediciones acotadas de
`docs/tecnica/index.md`/`docs/usuario/index.md` dentro de sus marcadores
`FEATURE_LINKS_START`/`FEATURE_LINKS_END` vía
`scripts/update-doc-indexes.ps1`. No se modifica ningún archivo
preexistente de `.agentic/`, ningún `scripts/*.ps1` preexistente,
`AGENTS.md` ni ningún `.github/workflows/*.yml`.

## D-6: No hay decisión nueva de arquitectura

Esta feature no agrega backend, base de datos, integración externa ni
dependencia de build: el único artefacto nuevo de código
(`scripts/check-adoption-conflicts.ps1`) usa PowerShell, ya establecido
como herramienta requerida en `AGENTS.md` ("Herramientas locales
requeridas"), y los tests nuevos reutilizan `pytest` ya declarado en
`requirements-dev.txt`. Por lo tanto no se agrega ninguna sección nueva a
`docs/tecnica/arquitectura.md` (consistente con `plan.md` sección 4).

## D-7: No hay decisión nueva de producto persistente

Esta feature es documentación operativa + una herramienta de apoyo
standalone para adoptar el circuito en otro repositorio: no introduce
ninguna regla de negocio, flujo de usuario ni conocimiento funcional
nuevo sobre el producto de este template (que sigue sin tener producto
propio — `docs/producto/contexto-producto.md` sigue con todas sus
secciones "Por definir"). No corresponde actualizar
`docs/producto/contexto-producto.md` como parte de cerrar esta feature.
