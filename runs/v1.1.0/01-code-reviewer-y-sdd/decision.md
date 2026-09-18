# Decision: 01-code-reviewer-y-sdd - Code Reviewer Y Sdd

## Estado

Estado tecnico: ready_for_pr.

La aprobacion de merge es exclusivamente del HITL en GitHub sobre la PR.
Este documento no otorga ni implica esa aprobacion.

## Evidencias revisadas

- `runs/v1.1.0/01-code-reviewer-y-sdd/spec.md`
- `runs/v1.1.0/01-code-reviewer-y-sdd/plan.md`
- `runs/v1.1.0/01-code-reviewer-y-sdd/tasks.md`
- `runs/v1.1.0/01-code-reviewer-y-sdd/audit-1.md`
- `runs/v1.1.0/01-code-reviewer-y-sdd/test-report-1.md`
- `runs/v1.1.0/01-code-reviewer-y-sdd/code-review-1.md`

## Decisiones demostrables

- `.agentic/roles/code-reviewer-agent.md` (nuevo) sigue exactamente la
  estructura de `.agentic/roles/reviewer-agent.md` (checklist, formato de
  output, seccion "Modo MILESTONE") y deja explicito que revisa el DIFF
  FINAL despues de que `qa-agent` aprueba, y que un rechazo vuelve a
  `builder-agent`, nunca a `analyst-agent` (AC-1, AC-7, spec.md Eje 1).
- `.agentic/agents.json` y `.agentic/models.json` agregan
  `roles.code-reviewer-agent` copiando exactamente la clase de modelo,
  esfuerzo y cadena de fallback de `roles.reviewer-agent`, sin introducir
  proveedor nuevo (AC-2, AC-3). `scripts/sync-agentic-adapters.ps1` no
  necesito cambios de logica: sigue derivando la lista de agentes de
  `agents.roles.PSObject.Properties`; se corrio sin `-Check` y luego con
  `-Check` (exit 0) despues de terminar TODOS los cambios a
  `.agentic/roles/*.md` (code-reviewer-agent, analyst-agent,
  reviewer-agent), atendiendo la nota no bloqueante de `audit-1.md`
  (AC-4).
- `Get-LatestVerdictArtifact`/`Assert-LatestVerdictApproved` en
  `scripts/feature-contract.ps1` reemplazan `Get-FirstExistingArtifact`
  (orden lexicografico, eliminada del archivo: sin otros llamadores
  confirmados por grep) para `audit-*.md`, `test-report-*.md` y
  `code-review-*.md`: seleccionan el intento de mayor numero ENTERO real,
  parsean el bloque ```` ```yaml ```` y validan `status`/`attempt` con
  comparacion case-sensitive (`-cne`), rechazando valores como `Approved`
  con mayuscula como malformados en vez de aprobados por default
  (AC-15, AC-16, AC-17, casos borde de spec.md).
- `Assert-WorkUnitContract` (modo `Feature` y `Milestone`) ahora exige
  `plan.md`, `tasks.md` y un `code-review-N.md` aprobado ademas de
  `spec.md`/`audit-N.md`/`test-report-N.md`, con la misma funcion
  `Assert-NonEmptyFile` para plan/tasks (AC-7, AC-13).
- `New-DecisionFile` ya no escribe "MERGE aprobado por evidencias del
  circuito agentico." Este mismo archivo (`runs/v1.1.0/01-code-reviewer-y-sdd/
  decision.md`) es evidencia demostrable de esa correccion: la seccion
  "Estado" dice "Estado tecnico: ready_for_pr" y aclara que el merge es
  exclusivamente HITL via GitHub, y "Evidencias revisadas" ya incluye
  `plan.md`, `tasks.md` y `code-review-1.md` (AC-18).
- `scripts/close-feature.ps1` (modo `Feature` y `Milestone`), cuando el
  estado local ya es `already-closed`, ahora hace `git fetch` y compara
  `origin/$baseBranch:ROADMAP.md` antes de la verificacion final: si el
  remoto no tiene el cierre, pushea el commit local pendiente; si ya lo
  tiene, no hace nada. Reproducido con tests que simulan un push fallido
  (hook `pre-receive` que rechaza) seguido de una reejecucion exitosa,
  en ambos modos (AC-20, AC-21, AC-22).
- `.agentic/schemas/agents.schema.json`, `.agentic/schemas/
  models.schema.json` y `.agentic/schemas/work-unit.schema.json` (JSON
  Schema Draft 2020-12 reales) resuelven la referencia `$schema` antes
  rota de `.agentic/agents.json`/`.agentic/models.json`, validados con
  `jsonschema` (Python) en `tests/test_agentic_schemas.py` con casos
  positivos y negativos por schema; la dependencia queda documentada en
  `docs/tecnica/arquitectura.md` como decision explicita de arquitectura
  (AC-23, AC-24, AC-25, AC-26).
- `AGENTS.md`, `ROADMAP.md` (encabezado), `docs/tecnica/
  circuito-agentico.md`, `docs/usuario/circuito-agentico.md` y
  `.agentic/README.md` describen el circuito con 5 roles y el nuevo
  orden `Builder → QA → Code Reviewer → READY_FOR_PR`, sin ninguna
  mencion residual a "4 agentes" (AC-5, AC-6, AC-9, AC-27).
- Suite completa de pytest verde (incluidos los tests nuevos de esta
  feature: `tests/test_agentic_schemas.py`, casos ampliados en
  `tests/test_feature_contract_scripts.py`, `tests/
  test_milestone_contract.py`, `tests/test_close_feature_script.py`,
  `tests/test_milestone_close_feature.py` y `tests/
  test_agentic_sync_scripts.py`) antes de entregar a QA.

## Resultado

La feature queda apta para integrarse/cerrarse cuando GitHub confirme merge contra `develop` y el cierre automatico marque `ROADMAP.md`.
