# Tasks: Integridad post-HITL y ready-for-pr

Cada tarea es pequeña, verificable, y referencia el/los `AC-N` de
`spec.md` que satisface. Los tres ejes (GAP A/B/C) son independientes
entre sí y pueden implementarse en cualquier orden; dentro de cada eje,
respetar las dependencias indicadas.

## Eje A — GAP A: aprobación HITL vinculada al commit vigente

- **T-01** — Agregar `headRefOid` a los campos `--json` pedidos por
  `gh pr view` en `scripts/complete-approved-pr.ps1`.
  Verificación: el `$pr` resultante expone `.headRefOid` sin lanzar
  error de propiedad inexistente en ningún camino del script.
  Traza: AC-1, AC-2.

- **T-02** — Implementar `Get-LatestApprovedReviewCommit` (o nombre
  equivalente) en `scripts/complete-approved-pr.ps1`, que invoca
  `gh api repos/:owner/:repo/pulls/{n}/reviews --paginate`, filtra por
  `state -eq "APPROVED"`, ordena por `submitted_at` descendente y
  devuelve el `commit_id` de la más reciente (o `$null` si no hay
  ninguna).
  Verificación: función unitariamente invocable con un JSON de reviews
  de prueba (puede probarse indirectamente vía T-04/T-05 con `gh` fake).
  Traza: AC-1.
  Depende de: T-01 (necesita el número de PR ya resuelto en el flujo).

- **T-03** — Insertar la validación stale/no-stale en el flujo
  principal de `scripts/complete-approved-pr.ps1`, entre la
  comprobación de `reviewDecision -eq "APPROVED"` y `Wait-PrChecks`:
  si no coincide `commit_id` con `headRefOid` (o no hay ninguna
  `APPROVED`), escribir `post-hitl-gate-N.md` con `status: rejected` y
  feedback explícito sobre aprobación obsoleta, respetar
  `-CommentOnFailure`, y terminar sin invocar `gh pr merge`.
  Verificación: lectura manual del diff confirma que el `throw` ocurre
  antes de cualquier llamada a `pr merge`.
  Traza: AC-1.
  Depende de: T-02.

- **T-04** — Extender el fake `gh` de
  `tests/test_complete_approved_pr_script.py` (`write_fake_gh`) para
  responder `headRefOid` en `pr view` y para responder a la consulta de
  reviews (`pulls`/`reviews` en los argumentos) con un array JSON
  configurable por `FAKE_GH_MODE`.
  Verificación: los tests existentes (`success`, `checks_fail`,
  `review_required`, `wrong_base`) siguen pasando sin cambiar sus
  aserciones.
  Traza: AC-11.
  Depende de: T-01, T-02, T-03 (el fake debe reflejar la forma real que
  el script ahora consume).

- **T-05** — Agregar `test_complete_approved_pr_rejects_stale_approval`
  (`FAKE_GH_MODE=stale_approval`): `headRefOid` distinto del
  `commit_id` de la única review `APPROVED`. Verificar `returncode !=
  0`, ausencia de `pr merge` en el log, y `post-hitl-gate-1.md` con
  `status: rejected` y mensaje reconocible sobre aprobación obsoleta.
  Verificación: `pytest tests/test_complete_approved_pr_script.py -k stale`
  pasa.
  Traza: AC-1, AC-8.
  Depende de: T-04.

- **T-06** — Agregar
  `test_complete_approved_pr_uses_most_recent_approved_review`: dos
  reviews `APPROVED` con `commit_id` y `submitted_at` distintos; la más
  reciente coincide con `headRefOid`. Verificar que el gate procede a
  `pr checks`/`pr merge` (no rechaza).
  Verificación: el test pasa y ejercita el camino de ordenamiento por
  `submitted_at`.
  Traza: AC-2, AC-8.
  Depende de: T-04.

- **T-07** — Confirmar que
  `test_complete_approved_pr_merges_after_green_checks`,
  `test_complete_approved_pr_returns_builder_feedback_when_checks_fail`,
  `test_complete_approved_pr_requires_hitl_approval_before_checks`,
  `test_complete_approved_pr_blocks_wrong_base_branch` y
  `test_complete_approved_pr_is_rerunnable_after_checks_turn_green`
  siguen pasando sin modificar sus aserciones (solo su fixture de `gh`
  fake si hizo falta en T-04).
  Verificación: `pytest tests/test_complete_approved_pr_script.py` en
  verde completo.
  Traza: AC-11.
  Depende de: T-04, T-05, T-06.

## Eje B — GAP B: orden transaccional en `ready-for-pr.ps1`

- **T-08** — En la rama Feature de `scripts/ready-for-pr.ps1`, insertar
  una llamada a `Assert-FeatureContract -Slug $Slug -Title $info.Title`
  (sin `-RequireReadyRoadmap`) inmediatamente antes del bloque que hace
  `Set-Content`/`git commit` sobre `ROADMAP.md`.
  Verificación: lectura del diff confirma que la llamada ocurre antes
  de cualquier mutación de archivo o `git commit` en esa rama.
  Traza: AC-3.

- **T-09** — Repetir T-08 para la rama Milestone, usando
  `Assert-WorkUnitContract -Slug $Slug -Mode Milestone -Title
  $info.Title` sin `-RequireReadyRoadmap`, antes del bloque
  `Assert-RoadmapItemsTransition` + mutación + commit.
  Verificación: lectura del diff confirma el orden; la rama "todos ya
  Ready" también ejecuta esta validación antes de continuar al
  push/PR.
  Traza: AC-4.

- **T-10** — Confirmar que las llamadas existentes con
  `-RequireReadyRoadmap` (Feature y Milestone) se mantienen intactas,
  ahora ejecutándose después de la mutación, sin cambiar su firma ni su
  ubicación relativa al resto del flujo (push, `Get-ExistingPr`, `gh pr
  create`).
  Verificación: lectura del diff — ninguna llamada a
  `Assert-FeatureContract`/`Assert-WorkUnitContract -RequireReadyRoadmap`
  fue eliminada ni movida antes de la mutación.
  Traza: AC-5.
  Depende de: T-08, T-09.

- **T-11** — Agregar `test_ready_for_pr_blocks_roadmap_mutation_when_contract_fails`
  (Feature) en `tests/test_feature_contract_scripts.py`: usar
  `prepare_ready_repo`, borrar `decision.md` (o similar) antes de correr
  `READY_FOR_PR`, capturar `git log`/contenido de `ROADMAP.md` antes y
  después. Verificar `returncode != 0`, `ROADMAP.md` sin cambios,
  ningún commit nuevo.
  Verificación: el test pasa.
  Traza: AC-3, AC-9.
  Depende de: T-08.

- **T-12** — Agregar el equivalente de T-11 para modo Milestone (nuevo
  fixture con manifest de 2+ items y un item con doc técnica faltante).
  Verificación: el test pasa; ningún item cambia de estado.
  Traza: AC-4, AC-9.
  Depende de: T-09.

- **T-13** — Confirmar que `test_ready_for_pr_creates_pr_after_expected_missing_pr`,
  `test_ready_for_pr_reuses_existing_pr_without_duplicate` y
  `test_ready_for_pr_blocks_real_gh_error` siguen pasando sin modificar
  sus aserciones.
  Verificación: `pytest tests/test_feature_contract_scripts.py -k ready_for_pr`
  en verde.
  Traza: AC-5, AC-11.
  Depende de: T-08, T-09, T-10.

## Eje C — GAP C: evidencia real en el cuerpo de la PR

- **T-14** — En la rama Feature de `scripts/ready-for-pr.ps1`, resolver
  `$auditArtifact`/`$qaArtifact`/`$codeReviewArtifact` con
  `Get-LatestVerdictArtifact` justo antes de armar `$evidenceSection`, y
  reemplazar los literales `audit-N.md`/`test-report-N.md`/
  `code-review-N.md` por `$($auditArtifact.Path)` /
  `$($qaArtifact.Path)` / `$($codeReviewArtifact.Path)`.
  Verificación: lectura del diff confirma que no queda ningún literal
  `-N.md` en la rama Feature del script.
  Traza: AC-6.
  Depende de: T-08 (la resolución de artefactos debe ocurrir después de
  que el contrato ya garantizó que existen y están aprobados).

- **T-15** — Repetir T-14 para la rama Milestone del mismo bloque
  `$evidenceSection`.
  Verificación: lectura del diff confirma que no queda ningún literal
  `-N.md` en la rama Milestone del script.
  Traza: AC-7.
  Depende de: T-09.

- **T-16** — Extender el fake `gh`/fixture de
  `tests/test_feature_contract_scripts.py` para capturar el contenido
  del `--body-file` pasado a `gh pr create` en un archivo de log
  adicional (siguiendo el patrón `FAKE_GH_LOG` de
  `test_complete_approved_pr_script.py`).
  Verificación: un test simple confirma que el archivo de log capturado
  contiene el body completo.
  Traza: AC-10.

- **T-17** — Agregar `test_ready_for_pr_pr_body_references_real_latest_attempt`
  (Feature): dejar `audit-1.md` (rejected) + `audit-2.md` (approved) en
  el repo de prueba antes de correr `READY_FOR_PR` en modo
  `missing_then_create`; verificar que el body capturado contiene
  `audit-2.md` y no contiene la subcadena `audit-N.md`.
  Verificación: el test pasa.
  Traza: AC-6, AC-10.
  Depende de: T-14, T-16.

- **T-18** — Agregar el equivalente de T-17 para modo Milestone.
  Verificación: el test pasa.
  Traza: AC-7, AC-10.
  Depende de: T-15, T-16.

## Eje D — Documentación y cierre del circuito (obligatorio, todas las features)

- **T-19** — Escribir
  `docs/tecnica/integridad-post-hitl-y-ready-for-pr.md` con las
  decisiones de diseño de los tres gaps (comparación de `headRefOid`,
  reordenamiento sin tocar `feature-contract.ps1`, resolución de
  artefacto real vía `Get-LatestVerdictArtifact`) y los casos borde
  relevantes de `spec.md`.
  Verificación: el archivo existe y no está vacío.
  Traza: AC-12.

- **T-20** — Escribir
  `docs/usuario/integridad-post-hitl-y-ready-for-pr.md` con el
  propósito de la feature y qué debe hacer quien opera el circuito si
  ve un `post-hitl-gate-N.md` con feedback de aprobación obsoleta.
  Verificación: el archivo existe y no está vacío.
  Traza: AC-13.

- **T-21** — Ejecutar
  `scripts/update-doc-indexes.ps1 02-integridad-post-hitl-y-ready-for-pr
  "Integridad Post Hitl Y Ready For Pr"` (o el título elegido por
  Builder) para enlazar ambos documentos en la zona `FEATURE_LINKS` de
  `docs/tecnica/index.md` y `docs/usuario/index.md`.
  Verificación: `Assert-IndexLink` (vía `Assert-FeatureContract`) pasa
  para ambos índices.
  Traza: AC-15.
  Depende de: T-19, T-20.

- **T-22** — Crear `runs/v1.1.0/02-integridad-post-hitl-y-ready-for-pr/decision.md`
  (vía `New-DecisionFile` o equivalente) con decisiones demostrables de
  esta feature, sin afirmar aprobación de merge.
  Verificación: el archivo existe, no está vacío, y `Assert-NonEmptyFile`
  lo acepta.
  Traza: AC-14.

- **T-23** — Correr `pytest tests/` completo y confirmar 0 fallos,
  incluyendo todos los tests nuevos (T-05, T-06, T-11, T-12, T-17,
  T-18) y todos los preexistentes citados en T-07 y T-13.
  Verificación: exit code 0 de la suite completa.
  Traza: AC-8, AC-9, AC-10, AC-11.
  Depende de: T-01 a T-18.
