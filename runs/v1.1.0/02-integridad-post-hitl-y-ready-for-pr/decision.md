# Decision: 02-integridad-post-hitl-y-ready-for-pr - Integridad Post Hitl Y Ready For Pr

## Estado

Estado tecnico: ready_for_pr.

La aprobacion de merge es exclusivamente del HITL en GitHub sobre la PR.
Este documento no otorga ni implica esa aprobacion.

## Evidencias revisadas

Estos son los artefactos esperados del circuito para esta feature; no
implica que todos ya existieran ni hubieran sido leídos en el momento
exacto en que se escribió esta lista (p. ej. `code-review-1.md` se
produce en un paso posterior del circuito, después de `test-report-1.md`):

- `runs/v1.1.0/02-integridad-post-hitl-y-ready-for-pr/spec.md`
- `runs/v1.1.0/02-integridad-post-hitl-y-ready-for-pr/plan.md`
- `runs/v1.1.0/02-integridad-post-hitl-y-ready-for-pr/tasks.md`
- `runs/v1.1.0/02-integridad-post-hitl-y-ready-for-pr/audit-1.md`
- `runs/v1.1.0/02-integridad-post-hitl-y-ready-for-pr/test-report-1.md`
- `runs/v1.1.0/02-integridad-post-hitl-y-ready-for-pr/code-review-1.md`

## Decisiones demostrables

- GAP A: se agrego headRefOid a gh pr view y una funcion Get-LatestApprovedReviewCommit que consulta gh api .../reviews --paginate --slurp, aplana el array de paginas resultante y compara el commit_id de la ultima review APPROVED (por submitted_at) contra headRefOid; si no coincide o no hay ninguna APPROVED, el gate rechaza sin invocar gh pr merge.
- GAP B: Assert-FeatureContract/Assert-WorkUnitContract (sin -RequireReadyRoadmap) se invocan en ready-for-pr.ps1 antes de cualquier mutacion o commit de ROADMAP.md, en Feature y en Milestone, incluyendo simetricamente la rama ya-en-READY_FOR_PR/todos-ya-Ready; la llamada final con -RequireReadyRoadmap se mantiene sin cambios despues de la mutacion.
- GAP C: el bloque evidenceSection de ready-for-pr.ps1 (Feature y Milestone) y la linea del checklist que citaba test-report-N.md ahora resuelven el path real con Get-LatestVerdictArtifact en vez de referenciar los literales audit-N.md/test-report-N.md/code-review-N.md.
- Se extendieron tests/test_complete_approved_pr_script.py, tests/test_feature_contract_scripts.py y tests/test_milestone_ready_for_pr.py con casos nuevos para stale approval, multiples reviews, bloqueo de mutacion de ROADMAP.md ante contrato roto (Feature y Milestone) y evidencia real en el body de la PR (Feature y Milestone), sin debilitar ninguna aserción preexistente.
- No se toco scripts/feature-contract.ps1 ni scripts/workunit-lib.ps1: -RequireReadyRoadmap ya era aditivo, confirmado leyendo el codigo antes de decidir no tocar su firma.

## Resultado

La feature queda apta para integrarse/cerrarse cuando GitHub confirme merge contra `develop` y el cierre automatico marque `ROADMAP.md`.
