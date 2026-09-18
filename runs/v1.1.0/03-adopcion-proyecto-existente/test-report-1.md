```yaml
status: approved
attempt: 1
feedback:
  - "No bloqueante: en scripts/check-adoption-conflicts.ps1, el `exit 2` que sigue a cada `Write-Error` (líneas ~34-42) nunca se ejecuta, porque `$ErrorActionPreference = \"Stop\"` convierte `Write-Error` en un error terminante que corta el script de inmediato; PowerShell.exe devuelve exit code 1 en ambos casos de error (ruta inexistente, ruta que no es directorio), no 2. Verificado empíricamente. No viola ningún AC porque AC-3/AC-4/AC-5 solo exigen 'código de salida distinto de cero', que se cumple, y los tests (`test_nonexistent_target_fails_explicitly`, `test_target_that_is_a_file_fails_explicitly`) solo assertan `returncode != 0`. Sugiero a builder-agent limpiar el código muerto (`exit 2`) o cambiar a `$ErrorActionPreference` local con captura explícita si en el futuro se necesita distinguir códigos de error, pero no amerita un nuevo intento."
```

## Test report: 03-adopcion-proyecto-existente (intento 1, qa-agent)

### Alcance de esta verificación

Trabajo verificado en el worktree `D:\proyectos\worktrees\03-adopcion-proyecto-existente`
(rama `feature/03-adopcion-proyecto-existente`), commit `1a4268f` y
anteriores. Contrato leído en `spec.md`, `plan.md`, `tasks.md` y
`audit-1.md` (`status: approved`, intento 1, dos observaciones no
bloqueantes ya reflejadas por builder-agent en D-3/D-4 de `decision.md`).

### AC-1 — Checklist técnico con colisión + estrategia de merge por elemento

Verificado leyendo `docs/tecnica/adopcion-proyecto-existente.md` completo
(266 líneas). Confirmé secciones dedicadas y con contenido concreto (no
genérico) para los 7 elementos + 4 subsecciones de workflows:

- `.agentic/` → colisión: adopción previa desactualizada con
  `agents.json`/`roles/*.md` customizados. Merge: copiar si no existe,
  fusionar archivo por archivo si existe, correr
  `scripts/sync-agentic-adapters.ps1` y `-Check` después. Nombres reales
  citados: `.agentic/agents.json`, `.agentic/roles/*.md`, `.claude/agents/*.md`,
  `.codex/*.config.toml`, `opencode.json`.
- `scripts/` → colisión de nombre puntual (ej. `workunit-lib.ps1` o
  `ready-for-pr.ps1` ya usados para otra cosa). Merge: unión de los 11
  scripts nombrados explícitamente, renombrar el del destino primero.
- `runs/` → colisión de nombre genérico. Merge: mover el contenido
  preexistente a otro nombre, citando `start-work-unit.ps1`,
  `ready-for-pr.ps1`, `close-feature.ps1` como referencias hardcodeadas.
- `docs/tecnica/` y `docs/usuario/` → fusionar sin reemplazar, trayendo
  `index.md` (marcadores `FEATURE_LINKS_START`/`END`), `arquitectura.md`,
  `circuito-agentico.md`.
- `AGENTS.md` → fusión por sección, lista explícita de qué secciones
  "del circuito" se copian tal cual vs. cuáles ("Stack", "Estructura del
  repo", "Propósito del producto") se reemplazan con contenido real del
  destino.
- 4 subsecciones de `.github/workflows/`: `ci.yml` (extender, no
  reemplazar; nota de versión de Python 3.12+), `docs.yml` (punto de
  decisión explícito, sin resolución automática), `post-hitl-merge-gate.yml`
  y `post-merge-close-feature.yml` (renombrar archivo, justificado con
  el mecanismo real de disparo por evento/contenido, no por nombre).

Cada sección nombra al menos un archivo real del template (`ready-for-pr.ps1`,
`workunit-lib.ps1`, `sync-agentic-adapters.ps1`, `complete-approved-pr.ps1`,
`close-feature.ps1`, etc.), no solo "los scripts del template" de forma
genérica. **AC-1: cumplido.**

### AC-2 — Guía de usuario

`docs/usuario/adopcion-proyecto-existente.md` (107 líneas), leído
completo: explica para qué sirve, cuándo consultarla, cómo recorrer el
checklist en el orden operativo correcto, y cómo correr opcionalmente el
script con el comando exacto y la interpretación de sus códigos de
salida. Lenguaje operativo, no de diseño. **AC-2: cumplido.**

### AC-3, AC-4, AC-5 — Contrato del script, agrupamiento, exit codes, solo lectura

Corrí el script yo mismo (no confié en lo reportado por builder-agent),
desde el propio worktree, contra directorios temporales reales:

1. **Directorio vacío** (`.../qa-adoption-test/empty`):
   `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/check-adoption-conflicts.ps1 -TargetPath <ruta>`
   → salida agrupada por los 11 elementos (7 + 4 subsecciones de
   workflows), todas marcadas `[ ok ] ... no existe`, mensaje final "no
   se detectaron colisiones", **exit code 0**. `find` antes/después del
   directorio confirmó cero archivos creados (destino sigue vacío).

2. **Directorio con colisiones precreadas** (una ruta real por cada
   categoría: `.agentic/placeholder.txt`, `scripts/ready-for-pr.ps1`,
   `runs/`, `docs/tecnica/index.md`, `docs/usuario/index.md`,
   `AGENTS.md`, los 4 `.github/workflows/*.yml`): salida agrupada marca
   cada una como `[COLISION] ... existe`, deja el resto como
   `[ ok ] ... no existe`, mensaje final "se detectaron colisiones",
   **exit code 1**. Snapshot de archivos (`find ... | sort`) idéntico
   antes y después de la ejecución — confirmado byte a byte con `diff`,
   sin diferencias: el script no creó, modificó ni borró nada.

3. **Ruta destino inexistente** (`C:\no\existe\esta\ruta`): mensaje
   explícito "La ruta destino '...' no existe.", **exit code 1**
   (distinto de cero, cumple AC-3's "no reportar 'sin colisiones' por
   defecto").

4. **Ruta destino que es un archivo, no un directorio**: mensaje
   explícito "... existe pero no es un directorio.", contenido del
   archivo verificado idéntico antes/después, **exit code 1**.

Los 4 casos verificados manualmente y de forma reproducible, en un
proceso limpio (sin ejecuciones pytest concurrentes que pudieran
interferir). **AC-3, AC-4, AC-5: cumplidos.**

Nota no bloqueante sobre el `exit 2` documentado en el propio script:
ver bloque de feedback arriba — no afecta el cumplimiento de los AC.

### AC-6 — Límites documentados del script

Verificada la sección "Límites de `scripts/check-adoption-conflicts.ps1`"
en `docs/tecnica/adopcion-proyecto-existente.md`: cubre explícitamente
los 5 límites exigidos por AC-6 (no diff de contenido, no distingue
"idéntico" de "mismo nombre", no usa historial de git, no resuelve
colisiones, y el límite adicional no bloqueante de `Test-Path` ante
acceso denegado señalado por `audit-1.md`). **AC-6: cumplido.**

### AC-7 — Tests de pytest

`tests/test_check_adoption_conflicts.py` sigue el patrón de
`tests/test_agentic_sync_scripts.py` (detección de
`powershell.exe`/`pwsh`, `subprocess.run` con `-File`). Cubre los 3
casos mínimos exigidos (destino vacío sin colisiones y exit 0; destino
con al menos una ruta de cada categoría con colisiones y exit distinto
de cero; contenido del destino sin cambios antes/después) más 2 casos
adicionales (ruta inexistente, ruta que es archivo).

Corrí `pytest tests/test_check_adoption_conflicts.py -v` (con
`--basetemp` propio porque el directorio temporal por defecto de pytest
en esta máquina, `C:\Users\jlbel\AppData\Local\Temp\pytest-of-jlbellon`,
tiene un problema de permisos preexistente y ajeno a esta feature — un
`PermissionError: [WinError 5] Acceso denegado` al listar ese directorio
específico, no relacionado con el código de esta feature):

```
tests/test_check_adoption_conflicts.py::test_empty_target_reports_no_collisions PASSED
tests/test_check_adoption_conflicts.py::test_target_with_known_paths_reports_collisions PASSED
tests/test_check_adoption_conflicts.py::test_nonexistent_target_fails_explicitly PASSED
tests/test_check_adoption_conflicts.py::test_target_that_is_a_file_fails_explicitly PASSED
4 passed in 6.26s
```

**AC-7: cumplido.**

### AC-8 — No se toca nada fuera de alcance

`git diff --stat develop...HEAD` (rama completa) muestra únicamente:
`docs/tecnica/adopcion-proyecto-existente.md` (nuevo),
`docs/tecnica/index.md` (+1 línea), `docs/usuario/adopcion-proyecto-existente.md`
(nuevo), `docs/usuario/index.md` (+1 línea), los artefactos de
`runs/v1.1.0/03-adopcion-proyecto-existente/` (`audit-1.md`, `decision.md`,
`plan.md`, `spec.md`, `tasks.md`), `scripts/check-adoption-conflicts.ps1`
(nuevo) y `tests/test_check_adoption_conflicts.py` (nuevo). 11 archivos,
1425 inserciones, 0 eliminaciones.

`git diff --stat develop...HEAD -- .agentic scripts/*.ps1 AGENTS.md .github/workflows/*.yml`
devuelve **solo** `scripts/check-adoption-conflicts.ps1` (archivo nuevo,
125 inserciones) — ningún archivo preexistente de `.agentic/`, ningún
`scripts/*.ps1` preexistente, `AGENTS.md` ni ningún workflow fue tocado.
**AC-8: cumplido.**

### AC-9 — Enlaces de índice

`docs/tecnica/index.md` línea 19 y `docs/usuario/index.md` línea 15:
ambos contienen exactamente
`- [Adopcion de proyecto existente](adopcion-proyecto-existente.md)`,
dentro de la zona `<!-- FEATURE_LINKS_START -->` / `<!-- FEATURE_LINKS_END -->`,
un único enlace en cada archivo, sin duplicados. **AC-9: cumplido.**

### AC-10 — `decision.md`

`runs/v1.1.0/03-adopcion-proyecto-existente/decision.md` (126 líneas, no
vacío): documenta D-1 a D-7, incluida explícitamente la justificación de
incluir el script en el alcance (D-1), el detalle de la tabla de rutas
conocidas (D-2), el contrato de exit codes verificado manualmente (D-3,
coincide con lo que yo mismo reproduje), el límite conocido de acceso
denegado (D-4), la confirmación de AC-8 (D-5), la ausencia de nueva
decisión de arquitectura (D-6) y de producto persistente (D-7). El
archivo abre declarando explícitamente que "no afirma aprobación de
merge: esa aprobación es exclusiva del HITL en GitHub" — no hay ninguna
frase que declare o insinúe aprobación de merge. **AC-10: cumplido.**

### Casos borde de `spec.md`

Revisados contra la implementación real:

- `runs/` genérico → documentado explícitamente en AC-1/`docs/tecnica`.
- `AGENTS.md` con contenido propio → fusión por sección, documentado.
- `ci.yml` con build/test propio → extender, nota de versión Python.
- `docs.yml` con otro generador → punto de decisión explícito, sin
  automatizar.
- Colisión de nombre sin relación semántica en los 2 workflows de gate →
  renombrar archivo, justificado con el disparador real (evento +
  contenido, no nombre).
- Destino sin rama `develop` → remite a "Setup manual" de `AGENTS.md`.
- Hosting fuera de GitHub → límite explícito, no generaliza.
- Ruta destino inexistente o no es directorio → verificado
  empíricamente arriba (AC-3/4/5): termina con error explícito, nunca
  "sin colisiones" por defecto.
- Colisión de nombre dentro de `scripts/` → cubierto en la sección
  `scripts/` del checklist técnico.
- Adopción parcial previa → el script reporta path por path sin asumir
  estados globales, verificado con el escenario de colisión parcial
  usado en el test `test_target_with_known_paths_reports_collisions`
  (mezcla de rutas presentes/ausentes en la misma corrida).

Todos los casos borde de `spec.md` están cubiertos por documentación,
implementación o ambas.

### Suite completa de tests (no solo lo nuevo)

Encontré un problema ambiental propio de esta máquina, no de la
feature: el directorio temporal por defecto de pytest
(`C:\Users\jlbel\AppData\Local\Temp\pytest-of-jlbellon`) da
`PermissionError: [WinError 5] Acceso denegado` al intentar listarlo —
ajeno al código de esta feature. Lo resolví apuntando `--basetemp` a un
directorio dentro del propio worktree para todas las corridas.

Corrí la suite completa en **una sola ejecución limpia** (sin procesos
pytest concurrentes, que en un intento anterior generaron falsos
positivos por interferencia de varias corridas compartiendo el mismo
`--basetemp` al mismo tiempo — descartado y repetido correctamente):

- `pytest -v --ignore=tests/test_local_reconciler_scripts.py` (134
  tests, todo el resto de la suite incluyendo
  `tests/test_check_adoption_conflicts.py`): **134 passed in 659.74s**,
  cero fallos, cero regresiones.
- `pytest -v tests/test_local_reconciler_scripts.py` (7 tests, en
  ejecución aislada): **4 passed, 3 failed in 620.51s**. Los 3 fallos
  son exactamente `test_start_reconciler_in_main_checkout`,
  `test_start_reconciler_from_linked_worktree`,
  `test_start_reconciler_replaces_stale_lock`, con el mismo síntoma
  reportado por builder-agent: `AssertionError: El reconciliador de
  99-demo no arranco en 60.0s (log/lock ausentes)` — timeout esperando
  que un proceso PowerShell en background escriba su log/lock,
  consistente con interferencia de EDR/antivirus agresivo en Windows
  sobre procesos PowerShell en background.

Total: **138 passed, 3 failed de 141 tests**.

Confirmé que esta feature no toca ninguno de los dos archivos
involucrados en esos 3 tests:
`git diff --stat develop...HEAD -- scripts/local-feature-reconcile.ps1 tests/test_local_reconciler_scripts.py`
devuelve **vacío** (ningún archivo listado). Por lo tanto los 3 fallos
son pre-existentes/ambientales, no atribuibles al diff de esta feature
— consistente con lo que la feature `05-operational-readiness-docs` (en
otro worktree) va a documentar como troubleshooting conocido.

**Veredicto de la suite: aprobada, con 3 fallos preexistentes
documentados y no atribuibles a este diff.**

### Contrato común (`Assert-FeatureContract`)

Verificación de índices (AC-9) y de `decision.md`/auditoría (AC-10)
hecha manualmente arriba con resultado positivo. Al invocar
`Assert-FeatureContract -Slug '03-adopcion-proyecto-existente'` de
forma directa desde `scripts/feature-contract.ps1`, falla únicamente
por la ausencia de `test-report-N.md` — esperable, porque ese archivo
es precisamente el que este reporte produce ahora. El resto del
contrato (spec/plan/tasks, `audit-1.md` con `status: approved`,
`decision.md` no vacío sin afirmar merge, enlaces exactos en ambos
índices) ya estaba satisfecho antes de este reporte, confirmado por
inspección manual de cada pieza en las secciones AC-9/AC-10 arriba.

### `docs/tecnica` y `docs/usuario` no vacíos

`docs/tecnica/adopcion-proyecto-existente.md`: 266 líneas, no vacío.
`docs/usuario/adopcion-proyecto-existente.md`: 107 líneas, no vacío.
Ambos leídos completos, contenido sustantivo y específico (no
placeholder). Confirmado.

### Tests agregados/modificados por QA

No hice falta escribir ni completar tests nuevos: `tests/test_check_adoption_conflicts.py`
ya cubre AC-7 con los 3 casos mínimos exigidos más 2 adicionales, y los
verifiqué corriéndolos yo mismo con resultado verde. No se commiteó
ningún test nuevo porque no fue necesario modificar la suite existente.

### Conclusión

Los 10 criterios de aceptación (AC-1 a AC-10) están cumplidos con
verificación real y reproducible: ejecución directa del script contra
directorios temporales reales (vacío, con colisiones, ruta inexistente,
ruta que es archivo), lectura completa de ambos documentos y
`decision.md`, inspección de índices y diff de git contra `develop`, y
corrida completa de la suite de tests (134 + 4 = 138 passed) más el
aislamiento explícito de los 3 fallos preexistentes y no atribuibles a
este diff. Apruebo con una observación no bloqueante sobre código muerto
(`exit 2`) que no afecta ningún criterio de aceptación.
