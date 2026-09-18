# Tasks: Operational readiness docs

- **T-01** — Redactar en `AGENTS.md`, sección "Setup manual (una sola
  vez, no automatizable)", el bullet "Branch protection de GitHub"
  siguiendo el esqueleto de la sección 2.1 de `plan.md`: los 4
  requisitos (PR obligatoria, status check `test` en verde, ≥1
  aprobación, dismiss stale approvals) aplicados a `develop` con
  `enforce_admins: true`, el comando `gh api` completo con el payload
  JSON, el paso de validación local `ConvertFrom-Json`, el comando de
  verificación de solo lectura (`GET`), la advertencia explícita de que
  el `PUT` reemplaza (no fusiona) la configuración existente, la nota de
  dependencia con la feature `04-ci-wiring-product-tests`, y la
  alternativa manual de UI (incluido el equivalente de "Do not allow
  bypassing").
  Verificación: `Select-String -Path AGENTS.md -Pattern "Branch protection de GitHub"`
  encuentra el bullet; el bloque JSON copiado pasa
  `$json | ConvertFrom-Json` sin error en PowerShell; el texto menciona
  explícitamente `"enforce_admins": true`, `dismiss_stale_reviews`,
  `required_approving_review_count`, `contexts` (o `checks`), `develop`,
  y la advertencia de reemplazo total con el `GET` previo.
  Traza: AC-1, AC-2, AC-3, AC-4.

- **T-02** — Agregar en `docs/tecnica/circuito-agentico.md` la sección
  "Troubleshooting: EDR/antivirus agresivo bloquea el reconciliador
  local (Windows)" con el contenido de la sección 2.2 de `plan.md`
  (síntoma, causa, alcance, comandos `git worktree remove --force` +
  `git worktree add`, advertencia sobre cambios sin commitear, nota
  sobre el lock file fuera del worktree).
  Verificación: la sección existe, es no vacía, y menciona
  explícitamente `local-feature-reconcile.ps1`, `ready-for-pr.ps1`,
  `git worktree remove --force` y `git worktree add`.
  Traza: AC-5.

- **T-03** — Escribir `docs/tecnica/operational-readiness-docs.md` con
  las decisiones de diseño de T-01 y T-02 (por qué `gh api`, por qué
  `develop` y no `main`, por qué `enforce_admins: true` con referencia
  explícita a la Fase CLARIFY resuelta en `spec.md`, por qué el `PUT`
  reemplaza y cómo se mitiga con el `GET` previo, por qué el
  troubleshooting vive en `circuito-agentico.md`, referencia a la deuda
  dejada por `02-integridad-post-hitl-y-ready-for-pr`) y los casos borde
  cubiertos.
  Verificación: el archivo existe y no está vacío
  (`Assert-NonEmptyFile` del contrato lo exige).
  Traza: AC-6.

- **T-04** — Escribir `docs/usuario/operational-readiness-docs.md` con
  el propósito de la feature y cómo usar ambos checklists (cuándo correr
  el comando de branch protection —incluyendo revisar primero con el
  `GET` qué hay configurado—, qué hacer si el reconciliador local queda
  bloqueado).
  Verificación: el archivo existe y no está vacío.
  Traza: AC-7.

- **T-05** — Crear `runs/v1.1.0/05-operational-readiness-docs/decision.md` con
  decisiones demostrables desde spec/plan/tasks/auditoría/
  implementación de T-01 a T-04, incluida explícitamente la resolución
  de la Fase CLARIFY sobre `enforce_admins` (pregunta, respuesta,
  valor final `true`), sin afirmar aprobación de merge.
  Verificación: el archivo existe, no está vacío, y referencia
  explícitamente las decisiones de T-01/T-02 (branch protection,
  incluida la Fase CLARIFY de `enforce_admins`, y troubleshooting EDR).
  Traza: AC-8.
  Depende de: T-01, T-02, T-03, T-04.

- **T-06** — Ejecutar
  `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\update-doc-indexes.ps1 05-operational-readiness-docs "Operational Readiness Docs"`
  para enlazar `operational-readiness-docs.md` en ambos índices.
  Verificación: `docs/tecnica/index.md` y `docs/usuario/index.md`
  contienen exactamente un enlace nuevo a `operational-readiness-docs.md`
  dentro del bloque `FEATURE_LINKS`.
  Traza: AC-9.
  Depende de: T-03, T-04.

- **T-07** — Correr `pytest -v` completo y confirmar que sigue en verde
  (no debe romperse ningún test existente del circuito, ya que esta
  feature no toca código ni scripts).
  Verificación: `pytest -v` termina sin fallos.
  Traza: AC-1 a AC-9 (regresión).
  Depende de: T-01, T-02, T-03, T-04, T-05, T-06.
