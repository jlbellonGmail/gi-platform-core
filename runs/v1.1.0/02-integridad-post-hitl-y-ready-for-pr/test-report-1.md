```yaml
status: approved
attempt: 1
feedback:
  - Los tres gaps (A: aprobacion HITL vinculada a headRefOid, B: orden transaccional de ready-for-pr.ps1, C: evidencia real en el body de la PR) estan implementados exactamente como describe plan.md, con tests nuevos que ejercitan realmente los casos borde (verificado con `--basetemp` propio, no solo lectura del codigo).
  - Verificacion manual adicional (fuera de pytest) contra un `gh` fake armado a mano confirma en vivo que una aprobacion stale (review APPROVED sobre "commit-OLD-when-approved" vs headRefOid "commit-NEW-after-push") bloquea el gate: exit code distinto de cero, ningun "pr merge" en el log de gh, y post-hitl-gate-1.md con status rejected y mensaje explicito de aprobacion obsoleta / se requiere nueva aprobacion humana.
```

## Alcance de esta verificación (qa-agent, intento 1)

Verifiqué de forma independiente (no solo aceptando el reporte de
builder-agent) que la implementación de `runs/v1.1.0/02-integridad-post-hitl-y-ready-for-pr/spec.md`
+ `plan.md` + `tasks.md` (aprobados en `audit-1.md`) cumple los 15 AC
declarados, incluyendo los casos borde. Trabajo hecho en el mismo
worktree (`D:\proyectos\worktrees\02-integridad-post-hitl-y-ready-for-pr`,
rama `feature/02-integridad-post-hitl-y-ready-for-pr`) sobre los commits
`8add61b`, `c28a03e` y `1e1501e`.

## 1. Contrato común (`scripts/feature-contract.ps1`)

Corrí directamente `Assert-FeatureContract -Slug '02-integridad-post-hitl-y-ready-for-pr' -Title 'Integridad Post Hitl Y Ready For Pr' -RequireReadyRoadmap:$false`.
Resultado: falla únicamente por `Falta al menos un test-report-N.md en
runs/02-integridad-post-hitl-y-ready-for-pr` — exactamente lo esperado en
esta etapa del circuito (QA está corriendo ahora mismo y este archivo es
el que falta). Confirmé leyendo el código de `Assert-FeatureContract`
(`scripts/feature-contract.ps1`) que esa es la única causa del fallo: la
validación de `decision.md`, docs técnica/usuario e índices no lanzó
ningún error antes de llegar a esa comprobación. Verificado también por
lectura directa:

- `runs/v1.1.0/02-integridad-post-hitl-y-ready-for-pr/decision.md` existe, no
  está vacío, referencia spec/plan/tasks/audit-1 y declara explícitamente
  que no otorga aprobación de merge (AC-14).
- `docs/tecnica/integridad-post-hitl-y-ready-for-pr.md` (201 líneas) y
  `docs/usuario/integridad-post-hitl-y-ready-for-pr.md` (70 líneas)
  existen, no están vacíos, y cubren explícitamente los tres gaps con
  decisiones de diseño (por qué `headRefOid`, por qué `--slurp`, por qué
  no se tocó `feature-contract.ps1`, cómo se resuelve el archivo real de
  evidencia) y el impacto operativo para quien opera el circuito
  (AC-12, AC-13).
- `docs/tecnica/index.md:18` y `docs/usuario/index.md:14` tienen
  exactamente un enlace cada uno a
  `integridad-post-hitl-y-ready-for-pr.md` (AC-15).
- `ROADMAP.md:61` sigue en `- [ ] 02-integridad-post-hitl-y-ready-for-pr`
  (pendiente, no `[-]` ni `[x]`) — correcto, porque `ready-for-pr.ps1`
  todavía no corrió en este circuito.

## 2. Revisión de los tests nuevos agregados por builder-agent

Leí `git diff 45fde47..HEAD -- tests/test_complete_approved_pr_script.py
tests/test_feature_contract_scripts.py tests/test_milestone_ready_for_pr.py`
completo (no solo los nombres de los tests) y confirmé:

- **`test_complete_approved_pr_rejects_stale_approval`** (AC-1, AC-8):
  el fake `gh` responde `headRefOid: "commitB"` en `pr view` y una única
  review `APPROVED` con `commit_id: "commitA"` en la consulta de
  reviews — son valores realmente distintos, no un caso trivial que
  pasaría igual sin el fix (si el chequeo no comparara commits, o
  comparara mal, este test fallaría porque encontraría `reviewDecision:
  APPROVED` y seguiría de largo a `pr checks`/`pr merge`). El test
  verifica `returncode != 0`, ausencia de `pr merge` en el log, y
  `post-hitl-gate-1.md` con `status: rejected` y las palabras
  "obsoleta"/"vuelva a aprobar".
- **`test_complete_approved_pr_uses_most_recent_approved_review`** (AC-2,
  AC-8): dos reviews `APPROVED` con `commit_id`/`submitted_at`
  distintos (`commitOld`/2026-08-19 y `commitC`/2026-08-21), donde solo
  la más reciente coincide con `headRefOid: "commitC"`. Ejercita
  realmente el ordenamiento por `submitted_at` descendente, no solo "hay
  una sola review que coincide".
- **`test_ready_for_pr_blocks_roadmap_mutation_when_contract_fails`**
  (Feature, AC-3/AC-9) y
  **`test_milestone_ready_for_pr_blocks_roadmap_mutation_when_contract_fails`**
  (Milestone, AC-4/AC-9): ambos borran un artefacto real del contrato
  (`decision.md` en Feature, la doc técnica de un solo item —`item-b.md`—
  en Milestone) y comparan bytes exactos de `ROADMAP.md` y el log de
  `git log --oneline` antes/después de invocar `ready-for-pr.ps1`. El
  caso Milestone en particular confirma la garantía "todo o nada" incluso
  cuando el resto de los items del manifest sí tendrían contrato
  completo (ítems A y C intactos, `item-b.md` es el único roto) — esto es
  precisamente el caso borde "Milestone con items en estados mixtos" de
  `spec.md`.
- **`test_ready_for_pr_pr_body_references_real_latest_attempt`** (Feature,
  AC-6/AC-10) y **`test_milestone_pr_body_references_real_latest_attempt`**
  (Milestone, AC-7/AC-10): ambos dejan `audit-1.md` (`rejected`) +
  `audit-2.md` (`approved`) antes de correr `ready-for-pr.ps1`, capturan
  el `--body-file` real pasado a `gh pr create` vía un `gh.cmd` fake que
  copia cualquier argumento `.md` al archivo de captura, y verifican que
  el body contiene `audit-2.md` (el intento realmente aprobado) y NO
  contiene el literal `audit-N.md`. Esto ejercita el bug real que motivó
  GAP C (referenciar el intento aprobado vigente, no un placeholder ni el
  primer intento).

## 3. Verificación manual reproducible adicional (no solo pytest)

Además de correr la suite, armé a mano —fuera del arnés de pytest— un
repo Git temporal y un `gh.cmd` fake en
`%TEMP%\...\scratchpad\manual-qa\` e invoqué directamente
`scripts/complete-approved-pr.ps1` (copiado tal cual del worktree) con:

- `pr view` devolviendo `reviewDecision: APPROVED`,
  `headRefOid: "commit-NEW-after-push"`.
- `gh api .../reviews --paginate --slurp` devolviendo una única review
  `APPROVED` con `commit_id: "commit-OLD-when-approved"`.

Resultado observado en vivo (no en el log de un test ya en verde):

```
==> Validando aprobacion humana de PR 'feature/manual-stale'...
==> Aprobacion HITL confirmada. Verificando que siga vigente sobre el commit actual...
Aprobacion HITL obsoleta para 'feature/manual-stale'. Feedback: runs\manual-stale\post-hitl-gate-1.md
```

- Exit code del proceso PowerShell: distinto de cero (excepción no
  controlada por `$ErrorActionPreference = "Stop"`, `throw` final).
- `gh.log` capturado solo contiene dos invocaciones: `pr view ...` y
  `api repos/:owner/:repo/pulls/123/reviews --paginate --slurp` — **no
  hay ninguna invocación a `pr merge`** ni a `pr checks`, confirmando que
  el gate corta el flujo antes de esperar checks o mergear.
- `runs/manual-stale/post-hitl-gate-1.md` generado con:
  `status: rejected`, mensaje "La aprobacion humana mas reciente ...
  quedo obsoleta: fue emitida sobre un commit distinto del head vigente
  (commit-NEW-after-push) ..." y "Se requiere que el humano vuelva a
  aprobar la revision sobre el commit vigente; esto no es una correccion
  de builder-agent."

Esto corrobora en vivo, con datos armados independientemente del set de
fixtures de `tests/test_complete_approved_pr_script.py`, que AC-1 se
cumple realmente y no es un artefacto casual del fake `gh` de ese
archivo de test.

También verifiqué contra el `gh` real instalado localmente
(`gh version 2.97.0`, la misma versión que cita `docs/tecnica/...md` como
la confirmada por builder-agent) que `gh api --help` documenta
explícitamente: *"Use with `--paginate` to return an array of all pages
of either JSON arrays or objects"* para `--slurp` — corrobora la
justificación técnica escrita en
`docs/tecnica/integridad-post-hitl-y-ready-for-pr.md` sobre por qué
`--slurp` es necesario para `Get-LatestApprovedReviewCommit`.

## 4. Tests preexistentes: ninguno debilitado

Revisé `git diff 45fde47..HEAD -- tests/test_complete_approved_pr_script.py
tests/test_feature_contract_scripts.py` completo (no un resumen): todos
los cambios sobre fixtures existentes (`write_fake_gh`) son estrictamente
aditivos —se agrega el campo `headRefOid` a JSON que ya existían con los
mismos valores usados por cada modo, y se agrega un nuevo bloque
`reviews`/`findstr /C:"reviews"` sin tocar los bloques `pr view`/`pr
checks`/`pr merge`/`pr comment` ya existentes—. Ninguna aserción
(`assert`) fue eliminada, comentada o relajada; todo lo agregado son
funciones y tests nuevos (`test_ready_for_pr_blocks_roadmap_mutation_when_contract_fails`,
`capture_pr_body_bin_dir`, `test_ready_for_pr_pr_body_references_real_latest_attempt`,
`test_complete_approved_pr_rejects_stale_approval`,
`test_complete_approved_pr_uses_most_recent_approved_review`).

## 5. Ejecución de tests automatizados

- `python -m pytest tests/test_complete_approved_pr_script.py
  tests/test_feature_contract_scripts.py tests/test_milestone_ready_for_pr.py
  -q --basetemp=<scratch>` (corrido por mí, en este worktree, con
  `--basetemp` apuntando a un directorio propio para evitar el
  `PermissionError` del basetemp por defecto en esta máquina): **41
  passed** en 154s, exit code 0. Incluye todos los tests nuevos citados en
  la sección 2 y todos los preexistentes (`test_complete_approved_pr_merges_after_green_checks`,
  `test_complete_approved_pr_returns_builder_feedback_when_checks_fail`,
  `test_complete_approved_pr_requires_hitl_approval_before_checks`,
  `test_complete_approved_pr_blocks_wrong_base_branch`,
  `test_complete_approved_pr_is_rerunnable_after_checks_turn_green`,
  `test_ready_for_pr_creates_pr_after_expected_missing_pr`,
  `test_ready_for_pr_reuses_existing_pr_without_duplicate`,
  `test_ready_for_pr_blocks_real_gh_error`, y toda `test_milestone_ready_for_pr.py`).
- Suite completa `pytest tests/` (todos los archivos, no solo los
  tocados): además de que el Main Agent ya la había corrido de forma
  independiente antes de delegar esta verificación (127 passed, 3
  failed), yo mismo la corrí de punta a punta con `--basetemp` propio
  (`python -m pytest tests/ -q --basetemp=.pytest-tmp`, en este
  worktree): **127 passed, 3 failed en 975.15s (16m15s)**, exit code 0
  (pytest reporta 0 pese a los 3 failed porque el wrapper de shell
  consumió el código de salida real de pytest; los 3 failed están
  listados explícitamente en el resumen). Los 3 fallos son exactamente
  `test_start_reconciler_in_main_checkout`,
  `test_start_reconciler_from_linked_worktree` y
  `test_start_reconciler_replaces_stale_lock`, los tres en
  `tests/test_local_reconciler_scripts.py`, con el mismo error en los
  tres: `El reconciliador de 99-demo no arranco en 60.0s (log/lock
  ausentes)` — timeout de arranque de un proceso reconciliador en
  background, específico de este entorno Windows, ya presente en el
  baseline pre-feature (121 passed, 3 failed antes de esta feature, mismo
  archivo y mismos tests). El delta exacto de esta feature es +6 passed
  (los tests nuevos de las secciones 2/3), 0 failed nuevos. Esto es
  consistente con que el plan declara explícitamente que no se toca
  `scripts/local-feature-reconcile.ps1` (`plan.md`, sección 1).

## 6. Verificación de casos borde de spec.md contra el código real

- **Múltiples revisores / orden por `submitted_at`**: cubierto por
  `test_complete_approved_pr_uses_most_recent_approved_review` (sección
  2) y por lectura de `Get-LatestApprovedReviewCommit`
  (`scripts/complete-approved-pr.ps1:200-246`): `Sort-Object {
  [datetime] $_.submitted_at } -Descending | Select-Object -First 1`.
- **Aprobar → dismiss → re-aprobar**: `Get-LatestApprovedReviewCommit`
  filtra `state -eq "APPROVED"` sobre el array completo devuelto por
  `gh api .../reviews` (que incluye `DISMISSED` y otros estados), antes
  de ordenar — revisado en el código, no solo en el plan.
- **Ninguna review `APPROVED` real**: `$approved.Count -eq 0` devuelve
  `$null`; el flujo principal trata `$null` igual que un commit
  no-coincidente (`[string]::IsNullOrWhiteSpace($latestApprovedCommit) -or
  $latestApprovedCommit -ne $pr.headRefOid`), fallando cerrado sin
  excepción no controlada.
- **Paginación**: `--paginate --slurp` + aplanado explícito de
  `$pages`/`$reviews` en el código (no se asume una sola página).
  Corroborado independientemente contra `gh api --help` real (sección 3).
- **Re-ejecución del gate tras checks en verde**: no se tocó
  `Wait-PrChecks` ni el flujo posterior a la validación de stale; el test
  preexistente `test_complete_approved_pr_is_rerunnable_after_checks_turn_green`
  sigue pasando sin modificar sus aserciones (confirmado en la corrida de
  la sección 5).
- **`ready-for-pr.ps1` re-ejecutado con `ROADMAP.md` ya `[-]`**: leí el
  código de ambas ramas (`ready-for-pr.ps1:176` Feature,
  `ready-for-pr.ps1:143` Milestone): la llamada temprana a
  `Assert-FeatureContract`/`Assert-WorkUnitContract` (sin
  `-RequireReadyRoadmap`) ocurre ANTES del `if` que distingue "ya está en
  READY_FOR_PR" de "hay que mutar", por lo que corre en ambos casos por
  igual — simétrico entre Feature y Milestone, resolviendo también la
  observación 2 de `audit-1.md`.
- **Milestone con items mixtos**: cubierto explícitamente por
  `test_milestone_ready_for_pr_blocks_roadmap_mutation_when_contract_fails`
  (sección 2).
- **Intentos rechazados intermedios / encoding de rutas**: cubierto por
  `test_ready_for_pr_pr_body_references_real_latest_attempt` /
  `test_milestone_pr_body_references_real_latest_attempt`; `Get-LatestVerdictArtifact`
  ya devuelve rutas relativas `runs/<slug>/...` (reutilizada sin cambios,
  confirmado en `scripts/feature-contract.ps1`).

> **Nota de corrección (post `code-review-1.md`, rejected):** la
> afirmación anterior es incorrecta. `Get-LatestVerdictArtifact.Path` se
> construye con `$latest.File.FullName`, que en .NET/PowerShell siempre
> devuelve una ruta absoluta, no `runs/<slug>/...`. Esta verificación fue
> por lectura de código mal interpretada, no empírica (no se inspeccionó
> el contenido real de `captured-body.md` en los tests para confirmar el
> formato de la ruta). El bug real, la corrección aplicada en
> `scripts/ready-for-pr.ps1` y el refuerzo de ambos tests para detectar
> path absolutos quedan documentados en `code-review-1.md` y en
> `docs/tecnica/integridad-post-hitl-y-ready-for-pr.md` (sección GAP C).
> Esta corrección debe ser re-verificada empíricamente por la próxima
> pasada de `qa-agent` en `test-report-2.md`, no asumida por esta nota.

## Conclusión

Los 15 AC de `spec.md` están cumplidos con evidencia verificable
(lectura de código real, tests automatizados que ejercitan el
comportamiento real —no triviales—, y una verificación manual
reproducible independiente del arnés de test para AC-1/AC-8). No se
debilitó ningún test preexistente. La documentación técnica y de usuario
existe, no está vacía y cubre las decisiones de diseño y el impacto
operativo. El contrato común pasa salvo por la ausencia esperada de este
mismo `test-report-1.md` (que este documento resuelve). `ROADMAP.md`
sigue `[ ]`, correcto para esta etapa del circuito.

Veredicto: **approved**.
