```yaml
status: approved
attempt: 2
feedback:
  - "Verificación independiente y empírica (no solo lectura de código) del fix de GAP C aplicado en el commit ed04acb: escribí un script ad hoc que reutiliza los mismos helpers de tests/test_feature_contract_scripts.py (make_contract_repo, capture_pr_body_bin_dir, etc.) para invocar realmente scripts/ready-for-pr.ps1 con audit-1.md (rejected) + audit-2.md (approved), y luego imprimí el contenido íntegro de captured-body.md. La línea real del body es 'Auditoria: runs/99-demo-feature/audit-2.md' (y análogas para QA/code review) — ruta relativa, sin separador de unidad de disco (':\\') y sin el path absoluto del repo temporal del test, en ninguna de sus dos formas (backslash o forward-slash)."
  - "Suite de tests dirigida a los tres GAP (tests/test_feature_contract_scripts.py, tests/test_milestone_ready_for_pr.py, tests/test_complete_approved_pr_script.py): 41 passed, incluidos los dos tests reforzados por builder-agent (test_ready_for_pr_pr_body_references_real_latest_attempt, test_milestone_pr_body_references_real_latest_attempt) que ahora fallarían explícitamente si el body contuviera un path absoluto."
  - "Suite completa pytest tests/: 126 passed, 4 failed en una corrida (947s). Los 3 failed esperados (baseline preexistente, no relacionado a esta feature, documentado en test-report-1.md §5) son los tres de tests/test_local_reconciler_scripts.py (timeout de arranque del reconciliador en background, específico de este entorno Windows). El 4to failed (test_milestone_item_already_claimed_by_existing_manifest_is_rejected, error 'Permission denied' al escribir un objeto git) es un fallo de contención de recursos del entorno compartido (antivirus/procesos concurrentes), no una regresión de esta feature: confirmado no reproducible al correrlo en aislamiento inmediatamente después (1 passed en 9.2s), y el commit ed04acb no toca ni scripts/workunit-lib.ps1 ni tests/test_start_work_unit.py."
  - "docs/tecnica/integridad-post-hitl-y-ready-for-pr.md, plan.md §2.3 y test-report-1.md §6 ya no afirman que Get-LatestVerdictArtifact.Path devuelve una ruta relativa: los tres documentan ahora, con precisión, que .FullName siempre es absoluta y que la corrección real recompone la ruta relativa en el punto de uso dentro de ready-for-pr.ps1, sin tocar Get-LatestVerdictArtifact ni Assert-LatestVerdictApproved."
  - "Assert-FeatureContract falla en este momento exactamente por una única causa esperada en esta etapa del circuito: 'El ultimo intento de code review (code-review-1.md, attempt 1) no esta approved (status: rejected)' — el mismo patrón que test-report-1.md §1 documentó para la ausencia esperada de test-report-1.md en su momento. decision.md, docs técnica/usuario e índices no generan ningún error antes de llegar a esa comprobación."
```

## Alcance de esta verificación (qa-agent, intento 2)

Este es un reintento de QA después de que `code-reviewer-agent` rechazó
el intento 1 (`code-review-1.md`) por un bug real en GAP C: el body de
la PR generado por `scripts/ready-for-pr.ps1` filtraba una ruta absoluta
del filesystem del agente/CI al espacio público de GitHub, en violación
del caso borde explícito de `spec.md` ("sin rutas absolutas del entorno
del agente"). `builder-agent` corrigió esto en el commit `ed04acb`. Esta
verificación es independiente: no doy por buena la corrección solo
porque el mensaje de commit la describe correctamente — la ejecuté y
observé el resultado real.

## 1. Lectura del diff del fix (`ed04acb`)

`git show ed04acb` confirma que el cambio queda contenido exactamente
donde `code-review-1.md` señaló, sin tocar la firma de
`Get-LatestVerdictArtifact` ni a su otro consumidor
(`Assert-LatestVerdictApproved`):

- En `scripts/ready-for-pr.ps1`, inmediatamente después de resolver
  `$auditArtifact`/`$qaArtifact`/`$codeReviewArtifact` (que siguen
  usando `Get-LatestVerdictArtifact` sin cambios), se recomponen tres
  variables nuevas (`$auditPath`, `$qaPath`, `$codeReviewPath`) como
  `"$($info.RunDir)/$(Split-Path -Leaf $artefacto.Path)"`, y son esas
  variables — no `.Path` directamente — las que se interpolan en
  `$evidenceSection` (ramas Feature y Milestone) y en la línea del
  checklist que menciona el archivo de QA.
- Los dos tests de GAP C (`test_ready_for_pr_pr_body_references_real_latest_attempt`
  en `tests/test_feature_contract_scripts.py` y
  `test_milestone_pr_body_references_real_latest_attempt` en
  `tests/test_milestone_ready_for_pr.py`) se refuerzan con exactamente
  las aserciones que `code-review-1.md` pidió: presencia de la ruta
  relativa exacta (`runs/<slug>/audit-2.md` /
  `runs/milestone-<slug>/audit-2.md`), y ausencia de `":\\"` (separador
  de unidad de disco Windows) y del path absoluto del repo temporal del
  propio test, en ambas variantes de separador.
- `docs/tecnica/integridad-post-hitl-y-ready-for-pr.md`, `plan.md` §2.3,
  `test-report-1.md` §6 y `decision.md` se corrigen para dejar de
  afirmar que `Get-LatestVerdictArtifact.Path` ya era relativa.

No hay cambios fuera de este alcance: el diff no toca GAP A ni GAP B, ni
ningún script/test ajeno a la corrección de GAP C y a la documentación
que describía el bug incorrectamente.

## 2. Verificación empírica directa del body de la PR (no solo lectura de código)

Esto es exactamente lo que `code-review-1.md` señaló que faltó en la
verificación de QA intento 1 (verificación por lectura de código mal
interpretada, no empírica). Para no repetir ese error, escribí un script
ad hoc (descartado al terminar, no forma parte del repo) que importa
`tests/test_feature_contract_scripts.py` como módulo y reutiliza sus
helpers reales (`make_contract_repo`, `git`, `run_ps`, `run_file`,
`capture_pr_body_bin_dir`, `git_env`, `verdict_block`, las mismas
constantes `CONTRACT`/`UPDATE_INDEXES`/`READY_FOR_PR`) para:

1. Crear un repo de prueba real con `audit-1.md` (`rejected`) y
   `audit-2.md` (`approved`).
2. Ejecutar `scripts/ready-for-pr.ps1` de verdad contra ese repo, con un
   `gh` fake que captura el body real de la PR en un archivo
   (`capture_pr_body_bin_dir`, el mismo mecanismo que usan los tests).
3. Leer e imprimir el contenido íntegro de `captured-body.md`.

Resultado observado (`ready-for-pr.ps1` retornó código 0):

```
## Evidencias

- Spec: runs/99-demo-feature/spec.md
- Plan: runs/99-demo-feature/plan.md
- Tasks: runs/99-demo-feature/tasks.md
- Decision: runs/99-demo-feature/decision.md
- Auditoria: runs/99-demo-feature/audit-2.md
- QA: runs/99-demo-feature/test-report-1.md
- Code review: runs/99-demo-feature/code-review-1.md
...
- [ ] Tests reportados en runs/99-demo-feature/test-report-1.md
```

Y las cuatro comprobaciones explícitas sobre el string completo del
body:

- `"runs/99-demo-feature/audit-2.md" in body` → `True`
- `":\\" in body` (separador de unidad de disco Windows) → `False`
- ruta absoluta del repo temporal del test, forma backslash → `False`
- ruta absoluta del repo temporal del test, forma forward-slash →
  `False`

Esto confirma con evidencia directa, no por lectura de código, que:

- la ruta insertada en el body es relativa y sigue el mismo formato que
  el resto de la sección de evidencias (`$info.RunDir`-relativo);
- no hay ningún path absoluto del filesystem local (ni con separador
  `:\` ni con la ruta del directorio temporal del test) filtrado al
  cuerpo público de la PR;
- el fix resuelve exactamente el defecto señalado en `code-review-1.md`,
  no una variante distinta del problema.

## 3. Suite de tests dirigida a los tres GAP

```
python -m pytest tests/test_feature_contract_scripts.py \
  tests/test_milestone_ready_for_pr.py \
  tests/test_complete_approved_pr_script.py -q --basetemp=.pytest-final
```

Resultado: **41 passed en 137.52s**, exit code 0. Incluye los dos tests
reforzados de GAP C con las nuevas aserciones de "sin ruta absoluta"
(`test_ready_for_pr_pr_body_references_real_latest_attempt`,
`test_milestone_pr_body_references_real_latest_attempt`), y todos los
tests preexistentes/nuevos de GAP A y GAP B sin modificar ni debilitar
ninguna aserción respecto a `test-report-1.md`.

## 4. Suite completa (`pytest tests/`)

`python -m pytest tests/ -q --basetemp=.pytest-tmp`: **126 passed, 4
failed en 947.49s (0:15:47)**.

- 3 de los 4 failed son exactamente el baseline preexistente ya
  documentado en `test-report-1.md` §5
  (`test_start_reconciler_in_main_checkout`,
  `test_start_reconciler_from_linked_worktree`,
  `test_start_reconciler_replaces_stale_lock`, todos en
  `tests/test_local_reconciler_scripts.py`, mismo mensaje "El
  reconciliador de 99-demo no arranco en 60.0s (log/lock ausentes)"),
  sin relación con el commit `ed04acb` (que no toca
  `scripts/local-feature-reconcile.ps1`).
- El 4to failed
  (`test_milestone_item_already_claimed_by_existing_manifest_is_rejected`
  en `tests/test_start_work_unit.py`) fue distinto al baseline conocido:
  `error: unable to write file .../objects/.../<hash>: Permission
  denied` al hacer `git commit` dentro del repo temporal del test. Lo
  investigué en vez de descartarlo sin más: el commit `ed04acb` no toca
  `scripts/workunit-lib.ps1` ni `tests/test_start_work_unit.py`, y al
  correr ese mismo test en aislamiento inmediatamente después
  (`python -m pytest
  tests/test_start_work_unit.py::test_milestone_item_already_claimed_by_existing_manifest_is_rejected
  -q --basetemp=.pytest-tmp2`) pasó limpio (**1 passed en 9.20s**). Es
  consistente con contención de recursos del entorno (procesos
  concurrentes de otros proyectos en la misma máquina Windows durante la
  corrida completa de 16 minutos, antivirus bloqueando momentáneamente
  la escritura de un objeto git), no con una regresión introducida por
  esta feature. No es un patrón nuevo respecto al ya conocido de
  `test_local_reconciler_scripts.py`: ambos son fallos de timing/recursos
  específicos de este entorno Windows compartido, no de la lógica bajo
  prueba.

Delta neto respecto al baseline de `test-report-1.md` (127 passed, 3
failed antes de esta corrección; nota: los números totales de tests
difieren levemente por la reejecución completa en un entorno distinto,
pero la composición de fallos preexistentes es idéntica): 0 fallos
nuevos atribuibles al código de esta feature.

## 5. Contrato común (`Assert-FeatureContract`)

```powershell
. .\scripts\feature-contract.ps1
Assert-FeatureContract -Slug '02-integridad-post-hitl-y-ready-for-pr'
```

Resultado: falla con un único mensaje — `El ultimo intento de code
review (code-review-1.md, attempt 1) no esta approved (status:
rejected)`. Esto es exactamente lo esperado en esta etapa del circuito:
`code-review-1.md` está `rejected` por diseño (es el veredicto que
originó este reintento de QA) y todavía no existe un `code-review-2.md`
aprobado — ese es el siguiente paso del circuito, no de este reporte.
Verificado que ninguna otra validación del contrato falla antes de
llegar a esa comprobación:

- `runs/v1.1.0/02-integridad-post-hitl-y-ready-for-pr/decision.md` existe, no
  está vacío, y su nota sobre evidencias esperadas fue aclarada en el
  commit `ed04acb`.
- `docs/tecnica/integridad-post-hitl-y-ready-for-pr.md` y
  `docs/usuario/integridad-post-hitl-y-ready-for-pr.md` existen, no
  están vacíos, y `docs/tecnica/index.md`/`docs/usuario/index.md`
  enlazan exactamente ese slug una sola vez (confirmado con `grep`).
- `spec.md`, `plan.md`, `tasks.md`, `audit-1.md` (approved) y
  `test-report-1.md` (approved) existen y son consistentes.

Este patrón (contrato fallando por exactamente una causa esperada de la
etapa actual del circuito) es el mismo que documentó `test-report-1.md`
§1 para la ausencia de `test-report-1.md` en su momento — no es un
defecto nuevo, es el comportamiento correcto de
`Assert-FeatureContract` mientras el circuito está en curso.

## 6. Documentación corregida

Confirmé por lectura directa que las tres correcciones de documentación
pedidas por `code-review-1.md` están presentes y son precisas:

- `docs/tecnica/integridad-post-hitl-y-ready-for-pr.md` (sección "GAP C")
  ahora explica correctamente que `.FullName` siempre es absoluta, cita
  el bug real detectado en `code-review-1.md`, y describe la corrección
  real aplicada (recomposición de ruta relativa en el punto de uso, sin
  tocar `Get-LatestVerdictArtifact`).
- `plan.md` §2.3 incluye una nota explícita "Corrección
  post-`code-review-1.md` (rejected)" que reconoce que la versión
  anterior del plan asumía sin verificar que `.Path` ya era relativa, y
  documenta la corrección real con el mismo nivel de detalle.
- `test-report-1.md` §6 mantiene la afirmación original (para no
  reescribir retroactivamente lo que QA intento 1 reportó) pero le
  agrega una nota de corrección visible inmediatamente debajo, que
  reconoce que esa verificación fue "por lectura de código mal
  interpretada, no empírica" y remite a `code-review-1.md` y a esta
  corrección para el detalle real.

Ninguna de las tres sigue afirmando que la ruta ya era relativa sin
matizarlo.

## Conclusión

El fix de GAP C (`ed04acb`) es correcto y completo, verificado de forma
independiente y empírica (no solo por lectura de código, corrigiendo
exactamente el punto débil señalado en `code-review-1.md`): el body real
de la PR generado por `ready-for-pr.ps1` usa una ruta relativa
(`runs/<slug>/audit-N.md`), sin ningún path absoluto del filesystem del
agente/CI. La suite dirigida a los tres GAP pasa completa (41/41), la
suite completa no tiene regresiones atribuibles a este commit (los 4
fallos observados en una corrida son preexistentes o de contención de
recursos del entorno, confirmado por aislamiento), la documentación ya
no contiene la afirmación incorrecta señalada, y el contrato común solo
falla por la causa esperada de esta etapa del circuito (code review aún
no reaprobado).

Veredicto: **approved**. Corresponde continuar el circuito hacia
`code-reviewer-agent` (intento 2), que debe revisar el diff final
incluyendo `ed04acb` y este `test-report-2.md`.
