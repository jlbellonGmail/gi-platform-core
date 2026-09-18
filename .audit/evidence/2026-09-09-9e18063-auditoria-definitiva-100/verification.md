# Ledger de verificación — auditoría definitiva 100/100

**Commit auditado:** `9e18063ad8fc02624da6596b8f31163a8852a45c`
**Repositorio:** `jlbellonGmail/template`
**Relacionado con:**
- `../../reports/AUDIT-2026-09-09-9e18063-final-100.md`
- `../../reports/AUDIT-2026-09-09-9e18063-segunda-pasada-adversarial.md`

Toda la evidencia de esta carpeta fue recolectada durante la ejecución real
de la auditoría final y su segunda pasada adversarial obligatoria (misma
sesión). No se ha fabricado ni reconstruido artificialmente ningún dato:
son copias exactas de las salidas ya obtenidas en esa ejecución. Ver
`AUDIT_RULES.md` §67-69 y `evidence/README.md` §23 (evidencia histórica no
sustituye verificación actual, pero aquí se trata de la misma verificación
ya ejecutada, solo persistida).

---

## Pasada 1 — Auditoría final independiente

### V-001 — CI oficial verde sobre el commit exacto auditado

**Objetivo:** confirmar que los 4 checks obligatorios están en `success`
directamente sobre `9e18063`.
**Comando/Método:** `gh api repos/{owner}/{repo}/commits/9e18063.../check-runs`
**Resultado:** `circuit-tests`, `product-tests`, `local-reconciler-tests`,
`guard-develop` → `conclusion: success`.
**Estado:** PASS
**Evidencia:** `pasada-1-auditoria-final/check-runs-audited-commit-9e18063.json`

### V-002 — Metadatos completos de la PR que mergeó el commit auditado

**Objetivo:** verificar mecanismo de merge (F-001) — humano vs. bot,
`reviewDecision`.
**Comando/Método:** `gh pr view 23 --json ...`
**Resultado:** `mergedBy.is_bot=false`, `mergedBy.login=jlbellonGmail`,
`reviewDecision=""`, `mergeCommit.oid=9e18063...`.
**Estado:** PASS
**Evidencia:** `pasada-1-auditoria-final/pr23-full.json`

### V-003 — `close-feature` no actúa sobre rama `chore/*` (F-005)

**Objetivo:** confirmar que el cierre automático post-merge detecta que
`chore/remediacion-final-96-a-100` no matchea `feature/NN-slug` ni
`milestone/slug` y no toca `ROADMAP.md`.
**Comando/Método:** log del run `post-merge-close-feature.yml`
correspondiente a PR#23.
**Resultado:** el job registra explícitamente que la rama no sigue el
patrón esperado y termina sin cierre automático.
**Estado:** PASS
**Evidencia:** `pasada-1-auditoria-final/close-feature-run-log-pr23.txt`

### V-004 — `guard-develop-branch.yml`: disparo real histórico + no interferencia con merges legítimos

**Objetivo:** confirmar que el guard técnico (mitigación de F-004) tiene
evidencia de ejecución real, no solo presencia estática.
**Comando/Método:** `gh run list`/`gh run view` sobre
`guard-develop-branch.yml`.
**Resultado:** corrida histórica con violación real detectada
(2026-08-30) + corridas limpias posteriores a merges vía PR (incluida la
que sigue al merge de PR#23) sin falsos positivos.
**Estado:** PASS
**Evidencia:** `pasada-1-auditoria-final/guard-develop-run-1737.json`,
`pasada-1-auditoria-final/guard-develop-run-postpr23.json`,
`pasada-1-auditoria-final/guard-develop-runs.json`

### V-005 — Visibilidad del repositorio y limitación de branch protection nativa

**Objetivo:** confirmar que el repo es privado y que la protección nativa
de rama sigue devolviendo `403` (consistente con lo documentado en
`AGENTS.md`, sección "Setup manual").
**Comando/Método:** `gh repo view --json isPrivate,visibility`;
`gh api repos/.../branches/develop/protection`.
**Resultado:** `isPrivate=true`; `403 Upgrade to GitHub Pro...`.
**Estado:** PASS (comportamiento documentado, no defecto)
**Evidencia:** `pasada-1-auditoria-final/repo-visibility.json`,
`pasada-1-auditoria-final/branch-protection-check.json`

### V-006 — Suite pytest local: investigación de flakiness (NV-01)

**Objetivo:** determinar causa raíz de fallos no deterministas en
corridas locales de `pytest -v tests/` y clasificarlos frente a
`AUDIT_RULES.md` §15/§16/§19 Caso B.
**Comando/Método:** 3 corridas completas + 1 corrida aislada de los 3
tests fallidos de la primera corrida.
**Resultado:** conjuntos de fallos distintos y no solapados entre
corridas completas; 100% de aciertos en corridas aisladas; traceback real
con `Permission denied` sobre un archivo de configuración git en
directorio temporal de Windows.
**Estado:** NO VERIFICADO — LIMITACIÓN DEL ENTORNO (no penaliza Q5.3; CI
oficial = V-001 = PASS)
**Evidencia:** `pasada-1-auditoria-final/pytest-local-flakiness-note.md`,
`pasada-1-auditoria-final/pytest-local-run2-full.txt`

---

## Pasada 2 — Segunda pasada adversarial (intento de refutación)

### V-007 — Reconfirmación aislada e independiente de los 3 tests de la corrida 1

**Objetivo:** intentar refutar NV-01 buscando si los mismos 3 tests
vuelven a fallar en una repetición fresca e independiente.
**Comando/Método:**
`pytest -v tests/test_close_feature_script.py::test_already_closed_feature_is_idempotent_and_does_not_create_empty_commit tests/test_feature_contract_scripts.py::test_contract_rejects_link_outside_managed_zone tests/test_local_reconciler_scripts.py::test_reconciler_never_removes_dirty_worktree --tb=long`
**Resultado:** `3 passed in 45.58s` — cuarta confirmación independiente.
**Estado:** PASS (refuerza NV-01 como limitación de entorno, no defecto)
**Evidencia:** `pasada-2-adversarial/pytest-rerun-adversarial-isolated-3tests.txt`

### V-008 — Precedente histórico de fallos reales de `local-reconciler-tests` en CI oficial

**Objetivo:** buscar si el CI oficial (`windows-latest`) también ha
mostrado flakiness alguna vez, para descartar que "CI verde" sea una
falsa sensación de estabilidad.
**Comando/Método:** `gh run list --workflow=ci.yml`, `gh run view --log-failed`
sobre los 4 runs fallidos históricos (2026-09-02, rama
`chore/remediacion-final-100`).
**Resultado:** los 4 fallos corresponden a un bug real, determinista y ya
corregido (arranque del reconciliador en Windows CI, "no arranco en
60.0s") — no a flakiness ambiental. Corregido en el mismo PR antes de
mergear (F-003 de la reauditoría v1.1, ya cerrado). Desde el fix
(commit `62433d1`, 2026-09-04) hasta `9e18063`: 4 corridas consecutivas
100% verdes en `develop`, sin recurrencia.
**Estado:** PASS (no aplica a `9e18063`; refuerza que CI distingue bugs
reales de ruido, y que el bug histórico está cerrado)
**Evidencia:** `pasada-2-adversarial/historical-ci-local-reconciler-failures-20260902.txt`

### V-009 — Permisos por defecto del repositorio para `GITHUB_TOKEN` (SUGGESTION-01)

**Objetivo:** determinar si la ausencia de bloque `permissions:` explícito
en `ci.yml` representa un riesgo material.
**Comando/Método:** `gh api repos/.../actions/permissions/workflow`.
**Resultado:** `default_workflow_permissions: "read"`,
`can_approve_pull_request_reviews: false`. `ci.yml` tampoco usa
`GITHUB_TOKEN`/`secrets.*` en ningún job.
**Estado:** PASS (riesgo neutralizado por configuración real del
repositorio, no solo por ausencia de uso) — se mantiene como
`SUGGESTION`, 0 puntos perdidos.
**Evidencia:** `pasada-2-adversarial/repo-workflow-default-permissions.json`

### V-010 — Reconfirmación fresca de metadatos de PR#23 (intento de reapertura F-001)

**Objetivo:** repetir la verificación de V-002 de forma independiente en
la segunda pasada, buscando cualquier discrepancia.
**Comando/Método:** `gh pr view 23 --json mergedBy,reviewDecision,reviews,mergeCommit,baseRefName,headRefName,state`
**Resultado:** idéntico a V-002 (`mergedBy` humano, `reviewDecision` vacío,
`state=MERGED`, `mergeCommit.oid=9e18063...`). Sin discrepancia.
**Estado:** PASS
**Evidencia:** `pasada-2-adversarial/pr23-merge-metadata-refresh.json`

---

## Nota sobre Actions de terceros (SUGGESTION-02)

Verificación adicional sin archivo dedicado (salida trivial, documentada
directamente aquí por brevedad, ver `evidence/README.md` §22): barrido de
`uses:` en los 5 workflows del repo. Resultado: únicamente
`actions/checkout@v4` y `actions/setup-python@v5` (ambas de primera
parte, `actions/*`). Cero Actions de terceros en todo el repositorio.
Confirma que el riesgo de supply chain por pinning-por-tag es mínimo.
