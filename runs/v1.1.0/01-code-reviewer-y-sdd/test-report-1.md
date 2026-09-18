```yaml
status: rejected
attempt: 1
feedback:
  - "BUG REAL (no de entorno): Get-LatestVerdictArtifact en scripts/feature-contract.ps1 (linea 108, `Get-Content -LiteralPath $path -Raw -Encoding UTF8`) no maneja el caso de un archivo de veredicto (audit-N.md/test-report-N.md/code-review-N.md) que existe con 0 bytes. `Get-Content -Raw` sobre un archivo vacio devuelve $null en esta version de PowerShell, y `[regex]::Match($null, ...)` en la linea siguiente lanza una excepcion .NET cruda sin capturar (`ArgumentNullException`, mensaje 'El valor no puede ser nulo. Nombre del parametro: input'), en vez del throw controlado con diagnostico legible que exige AC-15(f)/AC-17 ('mensaje que identifica la ruta exacta del archivo y la causa concreta'). El contrato SI rechaza el run (returncode != 0, no hay riesgo de que pase indebidamente), pero el mensaje de error no identifica el archivo (`audit-2.md`) ni la causa, violando la letra explicita de AC-17 ('mensaje de error que un humano puede entender sin leer el codigo fuente del script') y la mitad 'vacio' del escenario que describe AC-16 y su propio caso borde en spec.md ('con el bloque YAML presente pero...' no aplica aqui, pero el caso 'audit-2.md vacio o inexistente' de AC-16 SI lo nombra explicitamente)."
  - "Agregue el test `test_contract_fails_with_readable_message_when_latest_attempt_file_is_empty` en tests/test_feature_contract_scripts.py que reproduce el escenario exacto (audit-1.md rechazado + audit-2.md existente con 0 bytes) y falla contra la implementacion actual, confirmando el bug con evidencia ejecutable. No lo corregi yo mismo (no me corresponde como QA); vuelve a builder-agent. La correccion sugerida (no vinculante) es que Get-LatestVerdictArtifact trate `$content -eq $null` como 'sin bloque yaml' con el mismo throw ya usado para el caso de fence ausente, en vez de dejar que la excepcion de .NET se propague sin capturar."
  - "GAP DE COBERTURA (AC-19) YA CORREGIDO POR MI: no existia ningun test que verificara que el contenido generado por New-DecisionFile no contiene 'MERGE aprobado' ni afirma que la PR fue mergeada, y que si contiene una referencia explicita a HITL/GitHub -- pese a que T-15 de tasks.md declaraba explicitamente esa verificacion como parte de su criterio de Verificacion, y AC-19 de spec.md la exige como criterio de aceptacion independiente. La implementacion real de New-DecisionFile (lineas 330-387 de scripts/feature-contract.ps1) SI cumple el AC-19 correctamente (no escribe 'MERGE aprobado', escribe 'Estado tecnico: ready_for_pr.', menciona HITL/GitHub, y agrega plan.md/tasks.md/code-review-1.md a Evidencias revisadas para AC-18), pero no habia ningun test automatizado que lo confirmara. Agregue `test_decision_file_does_not_claim_merge_and_references_hitl` en tests/test_feature_contract_scripts.py, que pasa contra el codigo actual. No es un bug de implementacion -- es una cobertura de test faltante que builder-agent debe considerar cerrada con este commit, pero senalo el gap porque motiva parte del veredicto de este intento (T-15 no se cumplio integramente segun su propia definicion de Verificacion)."
  - "Resto de AC-14/16/17/20/21/22/23/24/25 de Eje 2/Eje 3: cobertura real confirmada, no solo 'el archivo existe'. Detalle en el cuerpo del reporte."
  - "Suite completa (excluyendo tests/test_local_reconciler_scripts.py por el bloqueo de EDR de Windows ya documentado y no relacionado con esta feature -- sin cambios de esta feature en ese archivo ni en scripts/local-feature-reconcile.ps1): 116 passed, 1 failed. El unico failed es el test nuevo que reproduce el bug de arriba, agregado deliberadamente por mi para dejar evidencia ejecutable; no es un fallo de mis propios tests, es la confirmacion del bug real."
  - "scripts/sync-agentic-adapters.ps1 -Check sigue en verde tras mis cambios (no toque .agentic/ ni adaptadores generados)."
  - "Documentacion (AC-28/AC-29/AC-30/AC-31/AC-32) verificada presente, no vacia, y con enlaces exactos en ambos indices -- ver detalle abajo. code-review-1.md no existe todavia en runs/v1.1.0/01-code-reviewer-y-sdd/, pero esto es esperado por el nuevo orden del circuito (Builder -> QA -> Code Reviewer -> READY_FOR_PR): corresponde que code-reviewer-agent lo produzca despues de este test-report, no antes."
```

# Test Report 1: 01-code-reviewer-y-sdd

## Veredicto

`rejected`, intento 1. Motivo: un bug real de implementacion en
`scripts/feature-contract.ps1` (`Get-LatestVerdictArtifact`) reproducido
con un test automatizado nuevo, que viola la letra de AC-17 (mensaje de
error legible/identificable) para el caso borde de un archivo de
veredicto existente pero vacio (0 bytes) como intento numericamente mas
reciente. Vuelve a `builder-agent`.

## Que verifique

### 1. Cobertura real de tests existentes (Eje 2 / Eje 3)

Revise linea por linea `tests/test_feature_contract_scripts.py`,
`tests/test_milestone_contract.py`, `tests/test_close_feature_script.py`,
`tests/test_milestone_close_feature.py`, `tests/test_agentic_schemas.py`
y `tests/test_agentic_sync_scripts.py` contra cada AC de Eje 2/Eje 3 del
spec:

- **AC-14** (contrato falla sin `plan.md`/`tasks.md`, pasa con ambos, en
  Feature y Milestone): cubierto por
  `test_contract_fails_when_plan_or_tasks_is_missing` (parametrizado
  `plan.md`/`tasks.md`) y `test_milestone_contract_missing_plan_or_tasks_is_rejected`
  (mismo patron), mas `test_contract_passes_with_full_valid_run` /
  `test_milestone_contract_happy_path` para el camino feliz. Real, no
  solo "el archivo existe".
- **AC-15/AC-16** (orden numerico real, no lexicografico):
  `test_contract_uses_real_numeric_order_not_lexicographic` crea
  `audit-2.md` rechazado + `audit-10.md` aprobado y confirma que el
  contrato PASA (10 gana sobre 2 por valor entero, no por string).
  `test_contract_fails_when_latest_real_attempt_is_rejected` invierte el
  caso (10 rechazado sobre 2 aprobado) y confirma que el contrato FALLA
  identificando `audit-10.md` en el mensaje. Equivalentes en
  `test_milestone_contract_uses_real_numeric_order_not_lexicographic` /
  `test_milestone_contract_fails_when_latest_real_attempt_is_rejected`.
  El escenario exacto de la auditoria original (`audit-1.md` rechazado +
  `audit-2.md` inexistente) esta cubierto por
  `test_contract_fails_when_previous_attempt_rejected_and_no_later_attempt_exists`
  -- pero solo la mitad "inexistente" del comentario del propio test
  ("vacio/inexistente"); la mitad "vacio" NO estaba cubierta y resulto
  ser un bug real (ver seccion 2).
- **AC-17** (bloque yaml ausente, `attempt` no coincide con archivo,
  mensaje legible): `test_contract_fails_when_yaml_block_is_missing`
  (contenido plano sin fences, exige "bloque" en el mensaje) y
  `test_contract_fails_when_attempt_does_not_match_filename`
  (`code-review-1.md` con `attempt: 2` dentro, exige "no coincide" en el
  mensaje). Equivalentes Milestone en
  `test_milestone_contract_fails_when_yaml_block_is_missing`. Ademas
  `test_contract_fails_when_status_value_is_malformed` cubre
  especificamente el caso borde de `status: Approved` (mayuscula
  distinta) tratado como invalido, no como aprobado por default -- exige
  "invalido" en el mensaje. Real y especifico, no generico.
- **AC-18/AC-19** (wording de `New-DecisionFile`): la implementacion es
  correcta (verificado leyendo scripts/feature-contract.ps1 lineas
  330-387: no escribe "MERGE aprobado", escribe "Estado tecnico:
  ready_for_pr.", aclara HITL/GitHub, agrega plan.md/tasks.md/
  code-review-1.md a Evidencias revisadas), pero NO habia ningun test
  automatizado que lo confirmara pese a que T-15 de tasks.md declaraba
  esa verificacion como parte de su criterio. Agregue
  `test_decision_file_does_not_claim_merge_and_references_hitl` (pasa).
- **AC-20/AC-21/AC-22** (retry de push en `close-feature.ps1`):
  `test_retry_after_failed_push_completes_on_rerun` en
  `tests/test_close_feature_script.py` reproduce el escenario exacto con
  un remoto `git` real (repo bare) cuyo hook `pre-receive` rechaza el
  primer push (`exit 1`), confirma que la primera ejecucion falla sin
  limpiar el worktree y con el commit local ya en `[x]` pero el remoto
  todavia en `[-]`, luego quita el hook y confirma que la segunda
  ejecucion completa el push pendiente SIN crear un commit nuevo
  (`commit_count` igual antes/despues) y pasa la verificacion final
  contra `origin/develop`. Es una simulacion real de fallo de push (no
  un mock), exactamente lo que pedia AC-21. `test_rerun_after_success_does_not_create_commit`
  cubre AC-22 (remoto ya cerrado, dos ejecuciones seguidas, sin commit
  ni push adicional, mensaje "El remoto ya tiene el cierre"). Ambos
  tienen equivalente exacto para modo Milestone en
  `tests/test_milestone_close_feature.py`
  (`test_retry_after_failed_push_completes_on_rerun`,
  `test_rerun_after_success_does_not_create_commit`), y
  `test_partial_close_state_is_rejected_as_unrecoverable` confirma que el
  caso borde de cierre remoto parcial sigue siendo irrecuperable
  automaticamente (no se toco ese comportamiento).
- **AC-23/AC-24/AC-25** (schemas JSON reales): `tests/test_agentic_schemas.py`
  usa `jsonschema.validate` real (no solo "el archivo existe") contra
  `.agentic/agents.json`/`.agentic/models.json`/un manifest de milestone
  fixture, con un caso positivo y al menos un caso negativo por schema
  (rol sin `description`, campo desconocido dentro de `claude` con
  `additionalProperties: false`, `models.json` sin `providers`, fallback
  sin `variant`, manifest con `items` vacio, `mode` distinto de
  `"milestone"`, item sin prefijo numerico). Verifique ademas que
  `.agentic/agents.json`/`.agentic/models.json` resuelven de verdad su
  `$schema` relativo a un archivo real
  (`test_agents_json_referenced_schema_path_exists` /
  `test_models_json_referenced_schema_path_exists`).

### 2. Bug real encontrado (verificacion manual + test nuevo)

Verificacion manual pedida por el punto 5 de mi tarea: cree a mano, en
un directorio de prueba fuera del repo (`.qa-manual-check/`, borrado al
terminar), un `runs/99-manual-check/audit-1.md` con `status: rejected` y
un `runs/99-manual-check/audit-2.md` de 0 bytes (existente pero vacio, no
inexistente), y llame directamente a
`Assert-LatestVerdictApproved -Directory ... -Prefix audit -Label auditoria`
dot-sourceando `scripts/feature-contract.ps1`. Resultado observado con
mis propios ojos:

```
Excepcion al llamar a "Match" con los argumentos "2": "El valor no puede
ser nulo. Nombre del parametro: input"
```

en vez de un mensaje del tipo "El archivo .../audit-2.md no tiene bloque
de codigo yaml valido...". Confirme la causa exacta leyendo
`scripts/feature-contract.ps1` linea 108
(`$content = Get-Content -LiteralPath $path -Raw -Encoding UTF8`): sobre
un archivo de 0 bytes, `Get-Content -Raw` devuelve `$null` en esta
version de PowerShell (confirmado tambien de forma aislada:
`$c = Get-Content -Raw ...; $null -eq $c` -> `$true`), y la linea
siguiente (`[regex]::Match($content, $yamlFencePattern)`) no contempla
`$content -eq $null`, por lo que .NET lanza una `ArgumentNullException`
sin capturar en vez de que el script haga su propio `throw` controlado.

Traduje ese hallazgo a un test automatizado reproducible
(`tests/test_feature_contract_scripts.py::test_contract_fails_with_readable_message_when_latest_attempt_file_is_empty`),
que corri y confirme que falla contra el codigo actual (ver salida
completa de pytest en la seccion siguiente). El contrato SI protege
contra este caso (rechaza el run igual), pero el mensaje no es el
diagnostico legible que exige AC-15(f)/AC-17, y por eso rechazo este
intento: es un AC explicito de esta misma feature, no una mejora
opcional.

No corregi `scripts/feature-contract.ps1` yo mismo -- corresponde a
`builder-agent`. Sugerencia no vinculante: tratar `$null -eq $content`
como equivalente a "sin bloque yaml" con el mismo `throw` ya usado en la
linea 112-114 para el caso de fence ausente.

### 3. Suite completa

Corri `pytest -v --ignore=tests/test_local_reconciler_scripts.py` dos
veces en esta maquina (antes y despues de agregar mis dos tests nuevos),
usando `--basetemp` explicito porque el `tmp` por defecto de esta maquina
esta bloqueado por el mismo problema de EDR de Windows ya documentado
para `test_local_reconciler_scripts.py` (no relacionado con el contenido
de ningun test, confirmado porque afecta la creacion del propio
directorio temporal de pytest, no un script del circuito).

- Antes de mis cambios: **115 passed** (confirma el resultado que ya
  habia visto el Main Agent, reproducido independientemente por mi).
- Despues de agregar mis 2 tests nuevos: **116 passed, 1 failed** -- el
  unico failed es
  `test_contract_fails_with_readable_message_when_latest_attempt_file_is_empty`,
  que documenta el bug real de la seccion 2. El otro test nuevo
  (`test_decision_file_does_not_claim_merge_and_references_hitl`) pasa.

No corri `tests/test_local_reconciler_scripts.py` en ningun momento, tal
como se me indico explicitamente -- ese archivo y
`scripts/local-feature-reconcile.ps1` no tienen cambios en el diff de
esta feature (`git diff --stat develop...HEAD` confirma cero lineas
tocadas en ambos), y el problema es 100% reproducible en esta maquina por
el EDR bloqueando el script tras su primera ejecucion real, no por logica
rota. El CI real corre en `ubuntu-latest`, donde esto no aplica. No es
motivo de rechazo.

### 4. `scripts/sync-agentic-adapters.ps1 -Check`

Corrido despues de mis cambios (que no tocan `.agentic/` ni ningun
adaptador generado): termina con "Adaptadores agenticos sincronizados."
y exit code 0.

### 5. Documentacion y contrato comun

- `docs/tecnica/code-reviewer-y-sdd.md`: existe, no vacio (10848 bytes),
  cubre los 3 ejes con decisiones de diseno concretas (por que un quinto
  agente en vez de ampliar `qa-agent`, permisos read-only, limitacion
  conocida de reset de intentos, etc.).
- `docs/usuario/code-reviewer-y-sdd.md`: existe, no vacio (3725 bytes).
- `runs/v1.1.0/01-code-reviewer-y-sdd/decision.md`: existe, no vacio, no
  contiene "MERGE aprobado", menciona HITL/GitHub explicitamente.
- `docs/tecnica/index.md` / `docs/usuario/index.md`: exactamente un
  enlace `- [Code Reviewer Y Sdd](code-reviewer-y-sdd.md)` en cada uno,
  dentro de la zona `FEATURE_LINKS_START`/`FEATURE_LINKS_END`.
- `runs/v1.1.0/01-code-reviewer-y-sdd/code-review-1.md`: NO existe todavia. Esto
  es lo esperado por el nuevo orden del circuito que esta misma feature
  introduce (`Builder -> QA -> Code Reviewer -> READY_FOR_PR`):
  `code-reviewer-agent` corre despues de que QA (yo) termine, no antes.
  No lo cuento como fallo de contrato de documentacion para este reporte.

## Que corresponde ahora

Vuelve a `builder-agent` (no a `analyst-agent`: es un bug de
implementacion en un caso borde ya descripto por el propio spec, no un
problema de alcance/diseno) para:

1. Corregir `Get-LatestVerdictArtifact` en `scripts/feature-contract.ps1`
   para que un archivo de veredicto vacio (0 bytes) produzca el mismo
   tipo de `throw` controlado y diagnostico que ya existe para "sin
   bloque yaml", en vez de dejar propagar la excepcion .NET cruda.
2. Confirmar que
   `tests/test_feature_contract_scripts.py::test_contract_fails_with_readable_message_when_latest_attempt_file_is_empty`
   pasa despues del fix (ya esta escrito y commiteado por mi en esta
   rama).
3. Volver a correr la suite completa
   (`pytest -v --ignore=tests\test_local_reconciler_scripts.py`) para
   confirmar 117 passed, 0 failed.
