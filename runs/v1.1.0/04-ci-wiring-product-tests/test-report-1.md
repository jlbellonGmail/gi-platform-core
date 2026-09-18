```yaml
status: approved
attempt: 1
feedback:
  - "Nota (no bloqueante): tests/test_local_reconciler_scripts.py tiene 3/7 tests que fallan por un problema ambiental preexistente (procesos powershell en background bloqueados, ver detalle abajo). Confirmado con git diff que esta feature no toca scripts/local-feature-reconcile.ps1 ni tests/test_local_reconciler_scripts.py. No se atribuye a este diff."
```

# QA report: 04-ci-wiring-product-tests (intento 1)

## Alcance verificado

Se verificó la implementación del commit `fda5b75` en el worktree
`D:\proyectos\worktrees\04-ci-wiring-product-tests` (rama
`feature/04-ci-wiring-product-tests`) contra `runs/v1.1.0/04-ci-wiring-product-tests/spec.md`
(versión 2, con Fase CLARIFY resuelta), `plan.md`, `tasks.md`,
`audit-1.md` (rejected) y `audit-2.md` (approved).

## Verificación por criterio de aceptación

### AC-1 — `ci.yml` declara exactamente dos jobs top-level con los mismos triggers

Verificado leyendo `.github/workflows/ci.yml` completo:

```yaml
on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [develop, main]

jobs:
  circuit-tests:
    ...
  product-tests:
    ...
```

Solo hay un bloque `on:` a nivel de workflow (sin overrides por job) y
ningún job declara `if:` propio. Confirmado con
`grep -n "if:" .github/workflows/ci.yml` → sin resultados. **PASS**.

### AC-2 — `circuit-tests` reproduce exactamente el job `test` anterior

Revisado el diff con `git show fda5b75 -- .github/workflows/ci.yml`: el
job renombrado conserva exactamente los mismos steps que el job `test`
original — `actions/checkout@v4`, `actions/setup-python@v5` con
`python-version: "3.12"`, `cache: "pip"`,
`cache-dependency-path: requirements-dev.txt`, `pip install -r
requirements-dev.txt`, y `pytest -v`. No hay ningún cambio de
comportamiento observable, solo el rename del job de `test` a
`circuit-tests`. **PASS**.

### AC-3 — `product-tests` existe, corre siempre, y tiene marcador inequívoco

El job `product-tests` no tiene `if:`, por lo tanto corre siempre que el
workflow se dispara. Contiene un bloque de comentario delimitado por
líneas de `#` con el texto literal `PLACEHOLDER: build/test del stack de
producto.` que referencia explícitamente `docs/tecnica/arquitectura.md`
como el lugar donde documentar la decisión de stack antes de reemplazar
el placeholder. **PASS**.

### AC-4 — `product-tests` pasa en verde de forma determinística sin dependencias externas

El único step real es
`run: echo "product-tests: sin stack de producto definido todavia. Ver docs/tecnica/arquitectura.md."`,
que no invoca ninguna herramienta de un stack no definido y siempre
termina en éxito (código de salida 0 de `echo`). Verificación manual
reproducible: ejecuté el mismo comando `echo "..."` en bash local, código
de salida `0`. No se pudo observar el check real en GitHub Actions porque
esta feature no tiene PR abierta todavía en este momento del circuito (el
AC exige verlo en verde "en el CI de la propia PR de esta feature", lo
cual ocurre en el paso 7-8 del circuito, posterior a QA); el contenido
del job garantiza determinísticamente ese resultado. **PASS** (con nota:
la verificación visual final en GitHub Actions ocurre en el paso 8 del
circuito, fuera del alcance temporal de este reporte).

### AC-5 y AC-6 — Documentación consistente sobre obligatoriedad igual de ambos jobs, citando Fase CLARIFY

Leí `docs/tecnica/ci-wiring-product-tests.md` (sección "Por qué
`product-tests` es requerido/bloqueante desde ya, pese a estar vacío") y
la sección "CI/CD" de `AGENTS.md`. Ambos documentos:

- afirman explícitamente que `circuit-tests` y `product-tests` son
  "igualmente obligatorios/bloqueantes, con el mismo nivel de exigencia";
- citan la Fase CLARIFY como origen de la decisión, no como supuesto
  propio del analyst-agent ("decisión confirmada por el humano en Fase
  CLARIFY... no un supuesto de ningún agente" en `AGENTS.md`; sección
  dedicada con pregunta+respuesta textual en el doc técnico);
- son consistentes entre sí (mismo lenguaje "gate obligatorio con el
  mismo nivel de exigencia").

`docs/usuario/ci-wiring-product-tests.md` también refuerza esto
("**Los dos son obligatorios.**"). **PASS**.

### AC-7 — Test de pytest que verifica estructura del workflow

`tests/test_ci_workflow.py` contiene 4 tests. Corridos con
`pytest tests/test_ci_workflow.py -v`:

```
tests/test_ci_workflow.py::test_ci_workflow_declares_circuit_tests_and_product_tests_jobs PASSED
tests/test_ci_workflow.py::test_circuit_tests_job_runs_pytest PASSED
tests/test_ci_workflow.py::test_product_tests_job_has_placeholder_marker PASSED
tests/test_ci_workflow.py::test_both_jobs_share_same_workflow_triggers PASSED
4 passed in 0.06s
```

**Verificación de mutación (lo que pedía T-05 de `tasks.md`):** edité
temporalmente `.github/workflows/ci.yml` reemplazando el step
`run: pytest -v` por `run: echo "pytest removed for mutation test"`
dentro del job `circuit-tests`, y volví a correr la suite:

```
FAILED tests/test_ci_workflow.py::test_circuit_tests_job_runs_pytest - assert 'pytest -v' in '...'
1 failed, 3 passed in 0.42s
```

Confirmado que el test detecta realmente la ausencia (no es un test
tautológico). Revertí el cambio con `git checkout -- .github/workflows/ci.yml`
y confirmé `git status` limpio y la suite de nuevo en verde (4/4). Los
tests usan substrings estables (nombres de job, texto `PLACEHOLDER`,
ausencia de `if:`), sin depender de indentación exacta del YAML, cumpliendo
el caso borde "Estabilidad del test de estructura" de `spec.md`. **PASS**.

### AC-8, AC-9 — Docs técnica y de usuario no vacíos

`docs/tecnica/ci-wiring-product-tests.md` (148 líneas): cubre por qué dos
jobs, por qué `product-tests` es requerido desde ya (citando Fase
CLARIFY), forma exacta del marcador, advertencia de migración de nombre
de status check. No vacío. **PASS**.

`docs/usuario/ci-wiring-product-tests.md` (64 líneas): cubre para qué
sirve, qué se ve en "Checks"/Actions, cómo reemplazar el placeholder, qué
hacer si ya había branch protection con el nombre viejo. No vacío.
**PASS**.

### AC-10 — Enlaces exactos y únicos en ambos índices

```
docs/tecnica/index.md:19:- [CI wiring product tests](ci-wiring-product-tests.md)
docs/usuario/index.md:15:- [CI wiring product tests](ci-wiring-product-tests.md)
```

Un único enlace en cada índice, dentro de la zona `FEATURE_LINKS`
(confirmado leyendo el archivo completo, no solo el grep). **PASS**.

### AC-11 — `decision.md` no vacío, no afirma aprobación de merge, referencia Fase CLARIFY

`runs/v1.1.0/04-ci-wiring-product-tests/decision.md` (98 líneas): tiene sección
"Estado" que dice explícitamente "La aprobacion de merge es exclusivamente
del HITL en GitHub... Este documento no otorga ni implica esa aprobacion.";
sección dedicada "Resolucion de la Fase CLARIFY (base real de AC-5)" con
pregunta y respuesta del humano citadas; sección "Decisiones demostrables"
con el detalle real de cada archivo tocado. No vacío, no ornamental.
**PASS**.

## Casos borde verificados

- **Triggers compartidos**: confirmado por AC-1, sin `if:` en ningún job.
- **`product-tests` no falla por dependencias inexistentes**: confirmado
  por AC-4, único step es `echo`.
- **Reemplazo futuro del placeholder**: documentado explícitamente en
  ambos `.md` con instrucciones paso a paso de reemplazo completo (no
  acumulación).
- **Adopción downstream con branch protection ya configurada**: cubierto
  en sección "Advertencia de migración" de `docs/tecnica/` y en
  `docs/usuario/` ("Si ya tenías branch protection...").
- **Estabilidad del test de estructura**: confirmado por mutación (ver
  AC-7) — el test detecta ausencias reales sin depender de indentación
  exacta.

## Suite completa de tests (`pytest`)

Se ejecutó la suite completa de `tests/` (no solo lo nuevo), usando un
`--basetemp` explícito porque el directorio temp por defecto de Windows
(`%TEMP%\pytest-of-<user>`) estaba bloqueado por procesos residuales de
ejecuciones anteriores (mismo problema ambiental que se documenta abajo
para `test_local_reconciler_scripts.py`).

Resultados por módulo (todos con `--basetemp` propio, todos en verde
salvo lo indicado):

- `tests/test_ci_workflow.py`: 4 passed.
- `tests/test_close_feature_script.py`, `test_complete_approved_pr_script.py`,
  `test_feature_contract_scripts.py`, `test_milestone_close_feature.py`,
  `test_milestone_contract.py`, `test_milestone_ready_for_pr.py`,
  `test_model_router_scripts.py`, `test_product_context_compatibility.py`,
  `test_workunit_lib.py`: 124 passed (corridos juntos, excluyendo
  `test_local_reconciler_scripts.py` y `test_start_work_unit.py` para
  aislar el módulo lento/afectado).
- `tests/test_start_work_unit.py`: 10 passed.
- `tests/test_local_reconciler_scripts.py`: **3 failed, 4 passed** (ver
  nota ambiental abajo).

Total: 141 tests, 138 passed, 3 failed (todos en el mismo módulo,
problema ambiental preexistente).

### Nota sobre fallos en `tests/test_local_reconciler_scripts.py` (no atribuible a este diff)

Los 3 tests que fallan (`test_start_reconciler_in_main_checkout`,
`test_start_reconciler_from_linked_worktree`,
`test_start_reconciler_replaces_stale_lock`) fallan con el mismo síntoma:

```
AssertionError: El reconciliador de 99-demo no arranco en 60.0s (log/lock ausentes).
```

Esto ocurre porque el proceso `pwsh`/`powershell` que el script
`scripts/local-feature-reconcile.ps1` lanza en background no llega a
escribir su log/lock dentro del timeout de la prueba — problema ambiental
ya reportado por el builder-agent de esta misma feature y confirmado de
forma independiente por el builder-agent de la feature
`03-...`/documentado como troubleshooting conocido en
`05-operational-readiness-docs` (EDR agresivo en Windows interfiriendo con
procesos PowerShell en background). Confirmé además, corriendo
`Get-Process pwsh,powershell`, decenas de procesos `powershell`/`pwsh`
residuales de sesiones anteriores (algunos de hace más de un día) todavía
vivos en la máquina — evidencia directa del mismo problema ambiental, no
de una regresión de código.

Confirmación de que esta feature **no tocó** ninguno de los dos archivos
involucrados:

```
$ git diff --stat develop...HEAD -- scripts/local-feature-reconcile.ps1 tests/test_local_reconciler_scripts.py
(sin salida — ningún archivo modificado)
```

`git diff --stat develop...HEAD` completo confirma que los únicos
archivos tocados por esta feature son: `.github/workflows/ci.yml`,
`AGENTS.md`, `docs/tecnica/ci-wiring-product-tests.md`,
`docs/tecnica/index.md`, `docs/usuario/ci-wiring-product-tests.md`,
`docs/usuario/index.md`, `runs/v1.1.0/04-ci-wiring-product-tests/*.md`,
`tests/test_ci_workflow.py`. Ninguno relacionado con el reconciliador.
Se trata, por lo tanto, de un fallo preexistente/ambiental, documentado
aquí como nota y no como motivo de rechazo.

## Contrato común (`scripts/feature-contract.ps1`)

Se invocó `Assert-FeatureContract -Slug '04-ci-wiring-product-tests'`
antes de escribir este `test-report-1.md`: falló únicamente con
`Falta al menos un test-report-N.md en runs/04-ci-wiring-product-tests`,
que es exactamente el artefacto que este mismo reporte crea. Todas las
demás validaciones del contrato (spec/plan/tasks, `audit-N.md` con
veredicto `approved` como último intento real, `decision.md` sin afirmar
aprobación de merge, `docs/tecnica/<slug>.md` y `docs/usuario/<slug>.md`
existentes y enlazados exactamente en ambos índices) pasaron sin error
antes de llegar a ese chequeo. Con este archivo ya escrito, el contrato
queda satisfecho.

## Documentación (verificación directa, no solo el contrato)

- `docs/tecnica/ci-wiring-product-tests.md`: leído completo, 148 líneas,
  no vacío, contenido específico de la feature (no boilerplate).
- `docs/usuario/ci-wiring-product-tests.md`: leído completo, 64 líneas,
  no vacío, contenido específico de la feature.
- Enlaces en `docs/tecnica/index.md` (línea 19) y `docs/usuario/index.md`
  (línea 15), dentro de la zona `FEATURE_LINKS`, un único enlace cada uno.

## Cambios de tests hechos por QA en este intento

Ninguno. `tests/test_ci_workflow.py`, tal como lo entregó builder-agent,
cubre AC-7 correctamente (confirmado con la verificación de mutación
descripta arriba) y no requirió modificaciones. No hay commit nuevo de
tests que hacer en este intento — el único artefacto nuevo de QA es este
`test-report-1.md`.

## Veredicto

`approved`. Todos los AC-1 a AC-11 verificados con evidencia concreta
(lectura directa de diff/archivos, ejecución real de tests, verificación
de mutación reproducible, y verificación de contrato). El único fallo de
suite completa detectado (`tests/test_local_reconciler_scripts.py`, 3/7)
es un problema ambiental preexistente no causado por este diff, confirmado
con `git diff --stat` y con evidencia de procesos residuales en el
sistema — se documenta como nota en el bloque de veredicto, no bloquea la
aprobación.
