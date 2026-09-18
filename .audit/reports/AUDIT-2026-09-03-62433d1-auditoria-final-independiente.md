# Auditoría FINAL e INDEPENDIENTE — commit 62433d19efe725a9999d5a5d5071660ffb7b131d

> ## ⚠️ INVALIDADO — 2026-09-09
>
> Este informe fue sometido a una revisión metodológica adversarial explícita a
> pedido del humano, antes de aceptar su resultado como baseline oficial. La
> revisión encontró que 6 de los 8 hallazgos (F-001 parcialmente, F-002, F-003,
> F-006, F-007, F-008) incorporaron requisitos no exigidos literalmente por
> `.audit/` v1.1.0, y que la clasificación de F-001 como `CRITICAL` (que activó
> el Quality Gate G2 y capó el score en 79/100) no está sostenida por el texto
> normativo. Conforme a `.audit/reports/README.md` §14 y §20, este informe queda
> marcado **INVALIDADO — no debe usarse como baseline oficial**. Se conserva
> íntegro y sin modificaciones adicionales como registro histórico del estado de
> razonamiento en esa fecha, conforme a §11 ("informe inmutable").
>
> **Resultado metodológicamente válido para este mismo commit:**
> ver `AUDIT-2026-09-09-62433d1-revision-adversarial.md` → **96/100 bruto = 96/100 final**, sin Quality Gate activo.

Framework aplicado: `.audit/` v1.1.0 (`README.md`, `QUALITY_SCORE.md`, `AUDIT_RULES.md`, `AUDIT_PROMPT.md`, `profiles/TEMPLATE.md`). Auditorías históricas (`audit-framework-v1.1.0`, reauditorías previas) **no se usan como ancla ni como fuente de puntuación** — toda evidencia de este informe fue recolectada desde cero contra el commit exacto indicado, con `gh`/`git` en vivo.

---

## A. IDENTIFICACIÓN

```text
Repositorio: jlbellonGmail/template (privado)
Ruta: D:\proyectos\template
Branch auditado: chore/auditoria-final-100 (worktree de trabajo de esta auditoría; el contenido evaluado es el commit fijo indicado abajo, no el HEAD de esta rama)
Commit: 62433d19efe725a9999d5a5d5071660ffb7b131d
Tag: (ninguno — no existe release de producto todavía; solo audit-framework-v1.1.0, fuera de alcance)
Fecha de auditoría: 2026-09-03
Worktree: D:\proyectos\template (checkout limpio, `git status --short` vacío)
Perfil: TEMPLATE (`.audit/profiles/TEMPLATE.md`) — repo se autodescribe como "Template base para arrancar un proyecto nuevo"
QUALITY_SCORE: .audit/QUALITY_SCORE.md (v1.1.0)
AUDIT_RULES: .audit/AUDIT_RULES.md (v1.1.0)
Nivel de confianza: ALTA
```

El commit auditado corresponde al merge commit de la PR #21 (`chore/remediacion-final-100` → `develop`), `mergedAt: 2026-09-04T00:47:37Z` (UTC; `2026-09-03 21:47:36 -0300` en hora local del autor), `mergedBy: jlbellonGmail` (humano).

---

## B. VEREDICTO EJECUTIVO

```text
Score bruto: 81.25/100
Score final: 79/100
Quality Gate aplicado: G2 — CRITICAL (F-001)
Confianza: ALTA
Estado: APTO CON CORRECCIONES
```

```text
Consistencia metodológica: PASS
```

**Resumen ejecutivo:** el circuito agéntico documentado (SDD de 5 agentes, único HITL, gate post-HITL, cierre automático) está bien diseñado, bien testeado en aislamiento (189 tests de circuito pasando, `local-reconciler-tests` verde en GitHub Actions real sobre el commit exacto auditado, `sync-agentic-adapters.ps1 -Check` sin drift) y sin secretos expuestos. Sin embargo, la reconstrucción de la historia real de GitHub (21 PRs mergeadas, revisadas una a una vía `gh api`/`gh pr view`) demuestra que **el mecanismo de merge automático post-HITL que documentan `AGENTS.md` (paso 9) y `README.md` (paso 3) nunca ha sido, en la práctica, el mecanismo real de merge**: las 21 PRs mergeadas hasta la fecha, incluida la que produjo el commit auditado, fueron mergeadas directamente por el humano vía GitHub con `reviewDecision` vacío (nunca `APPROVED`) — el script `complete-approved-pr.ps1`, que es el único punto del repo que ejecuta `gh pr merge` real, nunca ha completado esa ejecución con éxito en la historia observable del repo. Adicionalmente, el commit auditado en sí (PR #21) fue producido sin ningún artefacto del circuito SDD (`spec.md`, `plan.md`, `tasks.md`, `audit-N.md`, `test-report-N.md`, `code-review-N.md`, `decision.md`) pese a modificar `AGENTS.md`, `ci.yml` y scripts/tests del propio circuito. Esto activa el Quality Gate G2 (CRITICAL) y limita el score final a 79/100 pese a un score bruto de 81.25/100.

---

## C. ALCANCE Y LIMITACIONES

**Inspeccionado:** árbol completo de archivos trackeados (215 archivos vía `git ls-files`), `AGENTS.md`/`CLAUDE.md`/`README.md`/`ROADMAP.md` completos, los 5 workflows de `.github/workflows/`, `scripts/feature-contract.ps1`, `scripts/complete-approved-pr.ps1`, `scripts/local-feature-reconcile.ps1` (revisión dirigida), `tests/test_local_reconciler_scripts.py`, `tests/test_guard_develop_branch_workflow.py`, `docs/tecnica/*.md` y `docs/usuario/*.md` (índices y contenido de arquitectura/circuito), `docs/producto/contexto-producto.md` (existe), `.gitignore`, `requirements-dev.txt`, `pytest.ini`, `.mcp.json`, `opencode.json`, `mkdocs.yml` (existencia).

**Ejecutado:** `pytest -v` completo (excepto `test_local_reconciler_scripts.py`, Windows-only, cuya evidencia se tomó de GitHub Actions real sobre el commit exacto en lugar de reejecución local redundante), `pwsh ./scripts/sync-agentic-adapters.ps1 -Check`, barrido de secretos por regex sobre todos los archivos trackeados, `git merge-base --is-ancestor` sobre las 11 ramas remotas no-`develop`, `git ls-remote --heads origin`.

**Verificado vía GitHub API/CLI en vivo (no simulado, no histórico):** `check-runs` del commit exacto auditado, `gh pr view 21` completo, `gh api .../pulls/21/reviews`, `gh api .../issues/21/timeline`, `gh run view --log` de los jobs `complete-approved-pr` y `close-feature` de la PR #21, `gh pr list --state merged` (las 21 PRs mergeadas del repo, con `reviewDecision` y `mergedBy` de cada una), `gh api .../branches/develop/protection`, `gh api .../rulesets`, `gh repo view --json visibility,isPrivate`, `gh issue list --state all`.

**No pudo verificarse:** disparo real de un incidente en `guard-develop-branch.yml` (push directo a `develop` real) — el repo nunca tuvo uno (0 issues creados en toda su historia), por lo que la lógica de revert/restore solo tiene cobertura estructural/unitaria (`tests/test_guard_develop_branch_workflow.py`), nunca un ejercicio end-to-end real. Publicación real de GitHub Pages (`docs.yml` nunca se disparó: no existe `main` todavía, comportamiento esperado por diseño). Reproducción exacta de `product-tests` más allá del placeholder (no aplica: sin stack de producto todavía, documentado explícitamente como tal).

**Limitaciones del entorno:** `branches/develop/protection` y `rulesets` devuelven `403` (plan GitHub actual, repo privado) — confirmado en vivo en esta auditoría, consistente con lo ya documentado en `AGENTS.md`.

**Accesos remotos disponibles:** `gh` autenticado con acceso de lectura completo a Actions, PRs, issues, branches del repo `jlbellonGmail/template`. No se realizó ninguna escritura remota (sin comentarios, sin cierres, sin merges, sin pushes).

---

## D. CONTRATO DETECTADO

| ID | Capacidad/Requisito | Clasificación | Fuente | Estado |
| -- | -------------------- | -------------- | ------ | ------ |
| C-01 | Circuito de 5 agentes (analyst→reviewer→builder→qa→code-reviewer) con artefactos `spec/plan/tasks/audit-N/test-report-N/code-review-N/decision.md` por feature | OBLIGATORIO | AGENTS.md | Presente e implementado (`Assert-WorkUnitContract`), pero **no aplicado** al propio commit auditado (ver F-003) |
| C-02 | Único HITL: aprobación humana en GitHub + gate post-HITL que verifica `reviewDecision == APPROVED` y ejecuta el merge real | OBLIGATORIO | AGENTS.md paso 9, README paso 3 | Implementado en código (`complete-approved-pr.ps1`), pero **nunca ejercido con éxito real** en 21/21 merges históricos (ver F-001) |
| C-03 | `ROADMAP.md` con estados `[ ]`/`[-]`/`[x]` y transición atómica | OBLIGATORIO | AGENTS.md | Presente y consistente (6/6 items `[x]`, sin estados colgantes) |
| C-04 | Cierre post-merge automático (`post-merge-close-feature.yml` → `close-feature.ps1`) | OBLIGATORIO | AGENTS.md paso 10 | Implementado; para ramas `feature/`/`milestone/` funciona; para `chore/*` hace no-op correcto (no hay item de ROADMAP que cerrar) |
| C-05 | Enforcement técnico compensatorio de `develop` sin protección nativa (`guard-develop-branch.yml`) | OBLIGATORIO (decisión HITL documentada) | AGENTS.md, "Setup manual" | Presente, testeado estructuralmente, nunca disparado por un incidente real; **no verifica aprobación de revisión**, solo asociación commit↔PR mergeada (ver F-001) |
| C-06 | CI con 3 jobs gate obligatorio (`circuit-tests`, `product-tests`, `local-reconciler-tests`) | OBLIGATORIO | AGENTS.md "CI/CD" | Presente, verde en el commit exacto auditado (evidencia real de Actions) |
| C-07 | Sincronización única `.agentic/` → adaptadores generados (`.claude/agents/*`, `.codex/*`, `opencode.json`, `.mcp.json`) | OBLIGATORIO | AGENTS.md | Presente, `sync-agentic-adapters.ps1 -Check` sin drift |
| C-08 | Documentación por feature (`docs/tecnica/<slug>.md` + `docs/usuario/<slug>.md` + enlace exacto en ambos índices) | OBLIGATORIO | AGENTS.md | Presente para las 6 features reales del ROADMAP; **ausente** para el cambio que produjo el commit auditado (PR #21, sin `runs/` ni docs nuevas) |
| C-09 | Quick Start reproducible en `README.md` (clonar → activar circuito → flujo completo) | OBLIGATORIO (implícito, DX) | README.md | **No reproducible tal como está escrito** (ver F-004) |
| C-10 | Sin stack de producto fijo; `product-tests` placeholder transparente | OBLIGATORIO (decisión de alcance) | AGENTS.md "Stack" | Correctamente implementado, placeholder autodocumentado |
| C-11 | Rama `chore/*` para trabajo de gobernanza/auditoría/remediación | NO DOCUMENTADO / AMBIGUO | Observado en 13/21 PRs reales, ausente de AGENTS.md/README | Patrón real, recurrente, no reconocido por ningún gate ni por la estrategia Git documentada (ver F-002, F-005) |
| C-12 | `main` y primer tag de release | OPCIONAL (condicionado a evento futuro) | AGENTS.md "Git" | Correctamente ausente — no ha ocurrido el evento de primera release, estado esperado |

---

## E. MATRIZ DE PUNTUACIÓN

| Área                          |  Máximo | Obtenido | Estado |
| ------------------------------ | ------: | -------: | ------ |
| Q1 Conformidad                 |      12 |     9.00 | MENOR/PARCIAL |
| Q2 Reutilización               |      12 |    11.25 | MENOR |
| Q3 Arquitectura                |      12 |     9.75 | MENOR/DÉBIL |
| Q4 Documentación/DX            |      12 |     8.75 | PARCIAL |
| Q5 Calidad/Tests               |      16 |    15.25 | MENOR |
| Q6 Git/CI/CD/Release           |      16 |    12.25 | PARCIAL/DÉBIL |
| Q7 Seguridad                   |      12 |    10.00 | MENOR/PARCIAL |
| Q8 Automatización/Gobernanza   |       8 |     5.00 | DÉBIL |
| **TOTAL (bruto)**              | **100** | **81.25**|        |
| **TOTAL (final, tras G2)**     | **100** | **79.00**|        |

---

## F. DETALLE POR SUBCRITERIO

| ID | Criterio | Máx. | Nivel | Obtenido | Evidencia | Hallazgo | Justificación |
| -- | -------- | ---: | ----- | -------: | --------- | -------- | ------------- |
| Q1.1 | Propósito y alcance | 3 | COMPLETO | 3.00 | AGENTS.md completo, "Stack" explícito | — | Alcance sin ambigüedad, límites de dominio declarados |
| Q1.2 | Capacidades prometidas realmente presentes | 3 | PARCIAL | 1.50 | `all-merged-prs-review-status.json`: 21/21 PRs con `reviewDecision:""`, `mergedBy` humano | F-001 | El merge automático post-HITL, capacidad central documentada, nunca se ejecutó con éxito real |
| Q1.3 | Coherencia doc/config/implementación | 3 | PARCIAL | 1.50 | `complete-approved-pr-run-log-pr21.txt`; README paso 3 vs `feature-contract.ps1:422-431` | F-001, F-004 | Dos contradicciones documentadas-vs-observadas independientes |
| Q1.4 | Ausencia de requisitos obligatorios incompletos | 3 | COMPLETO | 3.00 | Revisión íntegra de AGENTS.md | — | Sin huecos obligatorios detectados más allá de lo ya listado |
| Q2.1 | Inicialización reproducible | 3 | MENOR | 2.25 | README PASO 2 paso 3 falla en un checkout limpio | F-004 | Pasos 1–2 funcionan; el paso 3 documentado no es ejecutable tal cual |
| Q2.2 | Ausencia de residuos específicos del origen | 3 | COMPLETO | 3.00 | Barrido regex de secretos: 0 matches; sin datos de cliente/negocio | — | — |
| Q2.3 | Configuración y personalización claras | 3 | COMPLETO | 3.00 | `.agentic/run.example.yaml`, precedencia documentada | — | — |
| Q2.4 | Portabilidad y extensibilidad | 3 | COMPLETO | 3.00 | Excepción Windows-only documentada y aislada (README "Compatibilidad") | — | — |
| Q3.1 | Estructura coherente | 3 | COMPLETO | 3.00 | `runs/`, `.agentic/`, `docs/`, `scripts/`, `tests/` bien delimitados | — | — |
| Q3.2 | Separación de responsabilidades | 3 | COMPLETO | 3.00 | Permisos por rol (`analyst-agent` read-only, `builder`/`qa` write) | — | — |
| Q3.3 | Simplicidad y ausencia de duplicación | 3 | COMPLETO | 3.00 | Fuente única `.agentic/` sin drift (`sync -Check` PASS) | — | — |
| Q3.4 | Capacidad de mantenimiento y evolución | 3 | DÉBIL | 0.75 | `find runs -iname "*remediacion-final-100*"` → sin resultados | F-003 | El propio commit auditado evade el mecanismo de evolución que la arquitectura declara obligatorio |
| Q4.1 | README funcional | 3 | MENOR | 2.25 | README.md íntegro | F-004 | Claro y bien estructurado, pero su propio Quick Start no es ejecutable |
| Q4.2 | Instalación y bootstrap reproducibles | 3 | PARCIAL | 1.50 | `scripts/feature-contract.ps1` líneas 422-431 | F-004 | Bootstrap de "primera feature" documentado omite todos los prerrequisitos reales |
| Q4.3 | Operaciones habituales documentadas | 2 | COMPLETO | 2.00 | `docs/tecnica/circuito-agentico.md` | — | — |
| Q4.4 | Convenciones de contribución | 2 | PARCIAL | 1.00 | 13/21 PRs reales usan `chore/*`, no documentado en ningún lado | F-005 | El patrón de contribución más usado en la práctica no está documentado |
| Q4.5 | Ejemplos y troubleshooting | 2 | COMPLETO | 2.00 | README "🆘 ¿Problemas?", troubleshooting EDR en arquitectura.md | — | — |
| Q5.1 | Controles automáticos de calidad | 3 | COMPLETO | 3.00 | `sync-agentic-adapters.ps1 -Check` PASS | — | — |
| Q5.2 | Estrategia de pruebas adecuada | 3 | COMPLETO | 3.00 | Cobertura de contrato, workunit, router, reconciliador | — | — |
| Q5.3 | Pruebas ejecutables y pasando | 4 | COMPLETO | 4.00 | 189 passed local + `local-reconciler-tests` verde en GHA sobre el commit exacto | — | — |
| Q5.4 | Protección frente a regresiones críticas | 3 | MENOR | 2.25 | `gh issue list --state all` → `[]`; solo tests estructurales de `guard-develop-branch.yml` | F-008 | Revert/restore de guard-develop nunca se ejerció en un incidente real; limitación ya reconocida por el propio AGENTS.md |
| Q5.5 | Quality gates automatizados | 3 | COMPLETO | 3.00 | 3 jobs requeridos, sin `continue-on-error`, verdes en el commit exacto | — | — |
| Q6.1 | Estrategia Git definida y coherente | 3 | PARCIAL | 1.50 | 13/21 PRs (`chore/*`) fuera de la estrategia documentada | F-002 | El patrón de ramas realmente dominante no forma parte de la estrategia declarada |
| Q6.2 | Protección de ramas y controles de integración | 3 | DÉBIL | 0.75 | `branch-protection-403.json`; `all-merged-prs-review-status.json` | F-001 | Sin protección nativa (justificado) y con el control compensatorio (gate post-HITL) sin ejercicio real exitoso en 21/21 casos |
| Q6.3 | CI reproducible y confiable | 3 | COMPLETO | 3.00 | `check-runs-audited-commit.json`: 4/4 `success` | — | — |
| Q6.4 | Versionado y releases | 3 | COMPLETO | 3.00 | Sin `main`/tag de producto — estado esperado pre-release, documentado como tal | — | — |
| Q6.5 | Build y artefactos reproducibles | 2 | COMPLETO | 2.00 | Sin stack de producto; placeholder transparente en `ci.yml` | — | — |
| Q6.6 | Compatibilidad, migraciones o rollback | 2 | COMPLETO | 2.00 | Fallback manual documentado (`git worktree remove` + `git branch -d`), `force-with-lease` en guard-develop | — | — |
| Q7.1 | Gestión de secretos | 3 | COMPLETO | 3.00 | Barrido regex 0 matches; `.gitignore` cubre `.env*` | — | — |
| Q7.2 | Gestión de dependencias | 2 | COMPLETO | 2.00 | `requirements-dev.txt` mínimo, con comentarios y cotas de versión | — | — |
| Q7.3 | Seguridad de CI/CD y automatizaciones | 2 | MENOR | 1.50 | `grep "uses: actions/"` → todos por tag mutable (`@v4`/`@v5`), sin pinning por SHA | F-006 | Gap de hardening de supply chain de bajo riesgo real (actions oficiales de GitHub) pero real |
| Q7.4 | Defaults seguros | 2 | COMPLETO | 2.00 | Permisos least-privilege declarados y testeados en `guard-develop-branch.yml` | — | — |
| Q7.5 | Supply chain y cumplimiento básico | 3 | PARCIAL | 1.50 | `ls LICENSE*` → no existe | F-007 | Repo explícitamente posicionado como template reutilizable, sin licencia declarada |
| Q8.1 | Fuente única de verdad | 2 | COMPLETO | 2.00 | `.agentic/` → adaptadores generados, sin drift | — | — |
| Q8.2 | Responsabilidades y límites definidos | 2 | COMPLETO | 2.00 | Permisos por agente explícitos en `.agentic/agents.json`/`opencode.json` | — | — |
| Q8.3 | Flujos deterministas y fail-safe | 2 | DÉBIL | 0.50 | `complete-approved-pr-run-log-pr21.txt`: skip silencioso reportado como `success` | F-002 | Patrón de "falso éxito" — el gate no distingue "no aplica" de "verificado y correcto" |
| Q8.4 | Trazabilidad | 2 | DÉBIL | 0.50 | Ausencia total de `runs/` para el cambio auditado | F-003 | El commit auditado no es trazable a spec/plan/tasks/decision alguno |

---

## G. LEDGER DE VERIFICACIÓN

| ID | Verificación | Comando/Método | Resultado | Estado | Evidencia |
| -- | ------------ | --------------- | --------- | ------ | --------- |
| V-01 | Commit exacto auditado | `git log -1 --format=... 62433d1...` | `Merge pull request #21 from jlbellonGmail/chore/remediacion-final-100`, autor Jose Luis Bellon, 2026-09-03 21:47:36 -0300 | PASS | shell output, este informe §A |
| V-02 | Worktree limpio | `git status --short` | vacío | PASS | shell output |
| V-03 | Suite de tests del circuito (no-Windows) | `pytest -v --ignore=tests/test_local_reconciler_scripts.py` | 189 passed, 1 warning (cache, no funcional), 498.63s | PASS | `bg9reo4u0.output` (scratchpad) |
| V-04 | Suite Windows-only del reconciliador | Evidencia GitHub Actions real sobre el commit exacto (no reejecución local) | `local-reconciler-tests`: `conclusion: success` | PASS | `check-runs-audited-commit.json` |
| V-05 | Adaptadores agénticos sin drift | `pwsh ./scripts/sync-agentic-adapters.ps1 -Check` | "Adaptadores agenticos sincronizados." | PASS | shell output |
| V-06 | Checks de CI sobre el commit exacto | `gh api .../commits/62433d1.../check-runs` | 4/4 `conclusion: success` (`guard-develop`, `circuit-tests`, `local-reconciler-tests`, `product-tests`) | PASS | `check-runs-audited-commit.json` |
| V-07 | Estado de revisión de la PR que produjo el commit | `gh pr view 21 --json reviewDecision,reviews,mergedBy` | `reviewDecision:""`, `reviews:[]`, `mergedBy: jlbellonGmail` | **FAIL** (contradice C-02) | `pr21-full.json` |
| V-08 | Estado de revisión de las 21 PRs mergeadas del repo | `gh pr list --state merged --limit 30 --json ...` | 21/21 con `reviewDecision:""`; 21/21 `mergedBy` humano | **FAIL** (contradice C-02, sistemático) | `all-merged-prs-review-status.json` |
| V-09 | Ejecución real del gate post-HITL sobre la PR #21 | `gh run view <id> --log` (job `complete-approved-pr`) | Detecta rama `chore/remediacion-final-100`, no matchea `feature/NN-slug` ni `milestone/slug`, hace `skip=true`, termina `success` sin verificar ni mergear nada | **FAIL** (contradice C-02) | `complete-approved-pr-run-log-pr21.txt` |
| V-10 | Rastro SDD (`runs/`) del cambio que produjo el commit auditado | `find . -iname "*remediacion-final-100*"`, `ls runs/` | Sin resultados — no existe `runs/*remediacion-final-100*` ni artefacto alguno | **FAIL** (contradice C-01, C-08) | shell output, este informe §D |
| V-11 | Protección nativa de rama `develop` | `gh api .../branches/develop/protection` | `403 Upgrade to GitHub Pro or make this repository public...` | Esperado/documentado, PASS respecto de lo declarado en AGENTS.md | `branch-protection-403.json` |
| V-12 | Visibilidad del repositorio | `gh repo view --json visibility,isPrivate` | `{"isPrivate":true,"visibility":"PRIVATE"}` | Confirma contexto de V-11 | `repo-visibility.json` |
| V-13 | Incidentes reales disparados por `guard-develop-branch.yml` | `gh issue list --state all --limit 20` | `[]` — nunca se disparó un incidente real | Limitación transparente, ya documentada en AGENTS.md | `issues-all-empty.json` |
| V-14 | Barrido de secretos reales | regex AKIA/ghp_/gho_/PRIVATE KEY/xox../sk- sobre todo `git ls-files` | 0 matches | PASS | shell output |
| V-15 | Reproducibilidad literal del Quick Start (`README.md`) | Lectura de `Assert-WorkUnitContract` (`scripts/feature-contract.ps1:411-431`) contra PASO 2/paso 3 de README | `Assert-NonEmptyFile` lanza `throw` por `spec.md` inexistente antes de llegar a ningún otro chequeo | **FAIL** (contradice C-09) | shell output, `scripts/feature-contract.ps1` |
| V-16 | Ramas remotas obsoletas ya mergeadas | `git merge-base --is-ancestor origin/<rama> origin/develop` × 11 | 11/11 `YES` (ya mergeadas, refs no borradas) | Housekeeping, no bloqueante | shell output |
| V-17 | Pinning de GitHub Actions | `grep "uses: actions/" .github/workflows/*.yml` | 100% por tag mutable (`@v4`/`@v5`), 0% por SHA | MENOR | shell output |
| V-18 | Existencia de `LICENSE` | `ls LICENSE*` | No existe | MENOR (repo se autodescribe como template reutilizable) | shell output |

---

## H. HALLAZGOS

| ID | Tipo | Severidad | Hallazgo | Evidencia | Criterio | Puntos |
| -- | ---- | --------- | -------- | --------- | -------- | -----: |
| F-001 | Comportamiento crítico contradictorio / control esencial evitable | **CRITICAL** | El merge automático post-HITL nunca ha sido, en la práctica, el mecanismo real de merge del repo | V-07, V-08, V-09 | Q1.2, Q1.3, Q6.2 | -5.25 |
| F-002 | Fail-safe engañoso / estrategia Git incompleta | MAJOR | El gate reporta `success` incluso cuando no verifica nada (ramas `chore/*`, 13/21 PRs reales); esa estrategia de rama no está documentada | V-09, C-11 | Q6.1, Q8.3 | -3.00 |
| F-003 | Trazabilidad SDD rota en el propio commit auditado | MAJOR | El commit auditado se produjo sin `spec.md`/`plan.md`/`tasks.md`/`audit-N.md`/`test-report-N.md`/`code-review-N.md`/`decision.md` | V-10 | Q3.4, Q8.4 | -3.00 |
| F-004 | Documentación no reproducible | MAJOR | El Quick Start de `README.md` (paso 3) no es ejecutable tal como está escrito | V-15 | Q1.3 (compartido con F-001), Q2.1, Q4.1, Q4.2 | -3.00 |
| F-005 | Convención de contribución no documentada | MINOR | El patrón `chore/*`, usado en 13/21 PRs reales (62%), no aparece en ninguna convención documentada | C-11 | Q4.4 | -1.00 |
| F-006 | Supply chain — pinning de Actions | MINOR | Todas las GitHub Actions usadas están fijadas por tag mutable, no por SHA | V-17 | Q7.3 | -0.50 |
| F-007 | Ausencia de LICENSE en template reutilizable | MINOR | No existe archivo `LICENSE` pese a que el repo se presenta explícitamente como template para clonar y reutilizar | V-18 | Q7.5 | -1.50 |
| F-008 | Revert/restore de `guard-develop-branch.yml` sin ejercicio real | MINOR | La lógica de reversión nunca se disparó en un incidente real (0 issues en la vida del repo); solo cobertura estructural/unitaria | V-13 | Q5.4 | -0.75 |

Total puntos perdidos: **18.75** (100 − 81.25 = 18.75 ✓).

### F-001 — El merge automático post-HITL nunca ha sido el mecanismo real de merge

```text
Descripción: AGENTS.md (paso 9) y README.md (PASO 3) documentan que, tras la
aprobación humana en GitHub, un gate automatizado (`complete-approved-pr.ps1`,
invocado por `.github/workflows/post-hitl-merge-gate.yml`) verifica
`reviewDecision == "APPROVED"`, espera checks post-aprobación en verde, y
ejecuta `gh pr merge` de forma automática. La reconstrucción completa e
independiente de las 21 PRs mergeadas en la historia real del repo
(`gh pr list --state merged --json reviewDecision,mergedBy`) muestra que las
21 tienen `reviewDecision` vacío (nunca "APPROVED") y las 21 fueron mergeadas
directamente por el humano (`mergedBy: jlbellonGmail`). El log real de
ejecución del job `complete-approved-pr` sobre la PR #21 (la que produjo el
commit auditado) confirma que el gate detectó que la rama no matchea
`feature/NN-slug` ni `milestone/slug`, puso `skip=true` y terminó en
`success` sin verificar aprobación ni ejecutar merge alguno — y para las
PRs `feature/*` (p.ej. PR #9), el propio gate corrió con
`conclusion: failure` (porque `reviewDecision` tampoco era "APPROVED" ahí)
y aun así la PR terminó mergeada por el humano directamente, sin que nada
en el sistema lo bloqueara.

Impacto: el "único punto de intervención humana" declarado como principio
de diseño central del proyecto (AGENTS.md, primer párrafo) no tiene, en la
práctica observada, ningún control técnico que impida a un humano (o a
cualquier cuenta con permisos de escritura) mergear una PR sin pasar por
revisión GitHub real ni por el gate automatizado — ni siquiera cuando el
gate corrió y falló explícitamente. Sin protección nativa de rama
(confirmado 403 por plan de GitHub) el gate post-HITL era, por diseño, el
único control técnico compensatorio real; la evidencia muestra que ese
control nunca fue el mecanismo real de merge en ningún caso histórico.

Causa raíz: ROOT-001 (ver sección I).

Corrección mínima suficiente: (a) documentar explícitamente en AGENTS.md
que el merge manual vía GitHub es la práctica real aceptada — degradando
el discurso de "único HITL con enforcement técnico" a lo que realmente
es — o (b) hacer que `complete-approved-pr.ps1`/su workflow sea el único
camino técnicamente posible de merge (por ejemplo, revocando permisos de
merge directo al humano vía configuración de equipo/organización, o
añadiendo una verificación en `guard-develop-branch.yml` que también
exija `reviewDecision == APPROVED` antes de aceptar el commit como
legítimo, no solo que pertenezca a una PR mergeada).

Verificación de cierre: repetir V-07/V-08/V-09 sobre las próximas N PRs
mergeadas tras la corrección y confirmar `reviewDecision: APPROVED` +
`mergedBy` correspondiente a la identidad que ejecuta el gate (o, si se
opta por (a), confirmar que la documentación ya no promete un enforcement
técnico que no existe).

Puntos recuperables: +5.25 (Q1.2 +1.5, Q1.3 +1.5 de los 3.0 compartidos
con F-004, Q6.2 +2.25).
```

### F-002 — Fail-safe engañoso del gate + estrategia Git incompleta

```text
Descripción: el mismo job que en F-001 reporta `success` para ramas
`chore/*` sin haber verificado nada, en vez de reportar "no aplica" de
forma distinguible de "verificado y aprobado". Esto es exactamente el
patrón de "falso éxito" (checks verdes que no representan una
verificación real) que el propio perfil TEMPLATE.md señala como riesgo
en su guía de Q8.3. El patrón de rama `chore/*` que dispara este no-op es
además el más usado en la práctica real (13 de 21 PRs mergeadas, 62%) y
no figura en ninguna parte de la estrategia Git documentada en AGENTS.md.

Impacto: un revisor humano o una herramienta externa que solo mire el
check `Post-HITL merge gate` en verde no puede distinguir "se verificó
la aprobación y se mergeó automáticamente" de "no se verificó nada
porque el nombre de rama no matchea". Esto reduce el valor de la señal
verde a cero para el 62% de las PRs reales del repo.

Causa raíz: ROOT-001.

Corrección mínima suficiente: hacer que el job falle (o reporte un
estado `neutral`/`skipped` explícito, nunca `success`) cuando la rama no
matchea ningún patrón reconocido, y agregar `chore/<slug>` como patrón de
rama reconocido y documentado explícitamente en AGENTS.md con sus propias
reglas (o eliminar el patrón, forzando todo trabajo de gobernanza a pasar
por `feature/`/`milestone/`).

Verificación de cierre: disparar un run del workflow contra una rama con
nombre no reconocido y confirmar que el conclusion ya no es `success`.

Puntos recuperables: +3.00 (Q6.1 +1.5, Q8.3 +1.5).
```

### F-003 — Trazabilidad SDD rota en el propio commit auditado

```text
Descripción: PR #21 modificó `AGENTS.md`, `.github/workflows/ci.yml`,
`scripts/local-feature-reconcile.ps1`, `scripts/sync-agentic-adapters.ps1`
y 3 archivos de `tests/`, en 5 commits reales. No existe ningún
`runs/*remediacion-final-100*` ni ningún artefacto `spec.md`, `plan.md`,
`tasks.md`, `audit-N.md`, `test-report-N.md`, `code-review-N.md` ni
`decision.md` asociado a este cambio.

Impacto: el commit exacto que esta auditoría tiene la obligación de
evaluar es, él mismo, un caso donde el circuito SDD que el proyecto
declara obligatorio ("Este documento... No es negociable por ningún
agente individual") no se aplicó. No es una feature de producto
(el repo no tiene stack todavía), pero sí modifica el propio motor del
circuito y su CI — exactamente el tipo de cambio de mayor impacto
gobernado por AGENTS.md.

Causa raíz: ROOT-001.

Corrección mínima suficiente: definir explícitamente en AGENTS.md si
existe una categoría de cambio ("gobernanza/mantenimiento del propio
circuito") exenta del circuito SDD completo y, si es así, qué artefacto
mínimo de trazabilidad exige en su lugar; o, si no debe existir esa
excepción, aplicar el circuito completo (spec/plan/tasks/audit/decision)
a este tipo de cambios también.

Verificación de cierre: confirmar que el próximo cambio de esta
naturaleza tiene `runs/` completo, o que AGENTS.md documenta
explícitamente por qué no lo necesita.

Puntos recuperables: +3.00 (Q3.4 +2.25, Q8.4 +0.75... nota: Q8.4 máximo
es 2, pérdida real fue 1.5, recuperable total de Q8.4 es +1.5; el total
del hallazgo es Q3.4 +2.25 + Q8.4 +1.5 = +3.75. Ver ajuste consolidado en
sección N).

Puntos recuperables: +3.75 (Q3.4 +2.25, Q8.4 +1.5).
```

### F-004 — Quick Start de `README.md` no reproducible

```text
Descripción: README.md, PASO 2, indica ejecutar en secuencia:
(1) `sync-agentic-adapters.ps1`, (2) `pytest -v tests/`,
(3) `ready-for-pr.ps1 -Mode Feature -Slug 01-mi-feature`. El paso 3 invoca
`Assert-FeatureContract` → `Assert-WorkUnitContract`
(`scripts/feature-contract.ps1:411-431`), que exige de forma bloqueante
`decision.md`, `spec.md`, `plan.md`, `tasks.md`, doc técnica, doc usuario,
y el último intento de `audit-N`/`test-report-N`/`code-review-N` con
status `approved` — ninguno de los cuales existe tras solo los pasos 1-2.
El script lanza `throw "Falta el archivo requerido: ..."` inmediatamente.
El README nunca menciona `start-work-unit.ps1` ni el resto del circuito de
5 agentes descrito en AGENTS.md.

Impacto: un adoptador nuevo que siga el Quick Start literalmente, tal
como el README promete ("tener tu proyecto operativo en menos de 5
minutos"), falla en el primer intento de usar el circuito, sin ninguna
pista en el propio README sobre qué le falta.

Causa raíz: independiente de ROOT-001 (documentación aspiracional escrita
sin verificar contra las precondiciones reales del script).

Corrección mínima suficiente: reescribir PASO 2/PASO 3 del README para
reflejar el flujo real completo (arrancar con `start-work-unit.ps1`,
pasar por spec/plan/tasks/audit antes de `ready-for-pr.ps1`), o
explicitar que PASO 3 solo es válido después de completar el circuito
descrito en AGENTS.md.

Verificación de cierre: ejecutar el Quick Start actualizado en un
checkout limpio y confirmar que no lanza ningún `throw` inesperado antes
del punto que el README describe.

Puntos recuperables: +4.50 (Q2.1 +0.75, Q4.1 +0.75, Q4.2 +1.5; la porción
de Q1.3 compartida con F-001 se contabiliza una sola vez en F-001 para
evitar doble conteo).
```

### F-005 — Convención `chore/*` no documentada

```text
Descripción: 13 de las 21 PRs mergeadas del repo (62%) usan el patrón
`chore/<slug>`, no mencionado en ninguna parte de AGENTS.md ni README.md
como convención de rama válida.

Impacto: cualquier agente o colaborador nuevo que lea solo AGENTS.md no
puede saber que este patrón existe, cuándo usarlo, ni qué garantías
(o falta de ellas, ver F-001/F-002) aplican cuando se usa.

Causa raíz: ROOT-001.

Corrección mínima suficiente: agregar una sección explícita a AGENTS.md
que documente el patrón `chore/<slug>`, su propósito (mantenimiento del
propio circuito, no features de producto) y sus reglas de gate/revisión.

Verificación de cierre: `grep -c "chore/" AGENTS.md` > 0 con contenido
normativo, no solo mención incidental.

Puntos recuperables: +1.00 (Q4.4).
```

### F-006 — GitHub Actions fijadas por tag mutable

```text
Descripción: las 5 workflows del repo usan `actions/checkout@v4` y
`actions/setup-python@v5` — tags mutables, no SHA de commit fijo.

Impacto: riesgo de supply chain bajo (son actions oficiales de GitHub)
pero real — un tag puede repuntar a un commit distinto sin que el repo lo
note.

Causa raíz: independiente.

Corrección mínima suficiente: fijar cada `uses:` a su SHA de commit
exacto (con comentario del tag equivalente al lado, práctica estándar).

Verificación de cierre: `grep "uses: actions/" .github/workflows/*.yml`
muestra únicamente SHAs de 40 caracteres.

Puntos recuperables: +0.50 (Q7.3).
```

### F-007 — Sin `LICENSE`

```text
Descripción: no existe archivo `LICENSE`/`LICENSE.md` en la raíz del
repo, pese a que README.md se dirige explícitamente a terceros que
clonan el template ("Bienvenido al template AI-Native... Clona el
template y ejecuta el Paso 1").

Impacto: ambigüedad legal para cualquier adoptador externo sobre los
términos bajo los que puede reutilizar el template.

Causa raíz: independiente.

Corrección mínima suficiente: agregar `LICENSE` con los términos que el
humano decida (o documentar explícitamente que el repo es privado de uso
interno exclusivo y no está destinado a distribución externa, si esa es
la intención real).

Verificación de cierre: `ls LICENSE*` encuentra el archivo, o AGENTS.md
declara explícitamente la intención de no distribución.

Puntos recuperables: +1.50 (Q7.5).
```

### F-008 — Revert/restore de `guard-develop-branch.yml` sin ejercicio real

```text
Descripción: 0 issues creados en la historia completa del repo
(`gh issue list --state all` → `[]`), lo que significa que la lógica de
reversión/restauración de pushes directos a `develop` nunca se disparó
en un incidente real; solo tiene cobertura mediante 18 tests
estructurales/unitarios (`tests/test_guard_develop_branch_workflow.py`)
que aseveran YAML, regex y flags, no comportamiento end-to-end real.

Impacto: bajo — esta limitación ya está transparentemente reconocida por
el propio AGENTS.md ("Limitación conocida verificada en este
repositorio"). No es una omisión oculta, es un riesgo residual
documentado y aceptado por el humano.

Causa raíz: independiente (limitación de superficie de prueba, no de
diseño).

Corrección mínima suficiente: ejercicio controlado y documentado (en un
repo de prueba o fork) de un push directo real a `develop` para verificar
el comportamiento end-to-end al menos una vez, dejando la evidencia como
referencia.

Verificación de cierre: existe un registro (issue o documento) de al
menos un disparo real, exitoso, del mecanismo de revert/restore.

Puntos recuperables: +0.75 (Q5.4).
```

---

## I. CAUSAS RAÍZ

| ID | Causa raíz | Hallazgos relacionados | Impacto |
| -- | ---------- | ----------------------- | ------- |
| ROOT-001 | El circuito no reconoce ni gobierna el patrón real de rama `chore/*` (62% de las PRs mergeadas): el gate post-HITL no lo verifica (solo `feature/`/`milestone/`), el enforcement compensatorio (`guard-develop-branch.yml`) solo exige pertenencia a una PR mergeada (no aprobación), y en la práctica **ningún** merge histórico —tampoco los `feature/*`— pasó realmente por el camino automatizado de verificación+merge que la documentación describe como el mecanismo real | F-001, F-002, F-003, F-005 | CRITICAL — el control de gobernanza central del proyecto ("único HITL con enforcement técnico") no tiene, hoy, ningún ejercicio real que lo confirme; el commit exacto auditado es producto directo de este patrón |

F-004, F-006, F-007 y F-008 son hallazgos independientes, sin causa raíz compartida entre sí ni con ROOT-001.

---

## J. QUÉ SOBRA

| Elemento | Clasificación | Evidencia | Motivo |
| -------- | -------------- | --------- | ------ |
| 11 ramas remotas obsoletas ya mergeadas (`feature/00...05-*` duplicadas de una segunda pasada, `chore/reauditoria-*`, etc.) | ELIMINAR | `git ls-remote --heads origin` + `git merge-base --is-ancestor` (11/11 `YES`) | Residuo de que ningún merge histórico pasó por el flujo `gh pr merge ... --delete-branch` real (siempre bypaseado por merge manual humano, ver F-001) — no afecta funcionalidad, es limpieza |
| Segunda PR duplicada para `feature/00-fuente-unica-router-modelos` (PR #1 y #2, mismo headRefName) | REVISAR | `all-merged-prs-review-status.json` | Posible reintento/corrección temprana del proyecto; no impacta el commit auditado, mencionado por completitud |

No se identificó código muerto, scripts huérfanos, ni dependencias sin uso en la superficie revisada.

---

## K. QUÉ FALTA

### OBLIGATORIO PARA 100/100

- Cerrar F-001: hacer que el mecanismo de merge automático post-HITL sea real (o redocumentar honestamente la práctica real de merge manual).
- Cerrar F-002: eliminar el patrón de "success" silencioso cuando el gate no verifica nada.
- Cerrar F-003: aplicar (o documentar explícitamente una excepción para) el circuito SDD a cambios de gobernanza del propio circuito.
- Cerrar F-004: corregir el Quick Start de README para que sea ejecutable tal cual está escrito.
- Cerrar F-005: documentar la convención `chore/*`.
- Cerrar F-006: fijar Actions por SHA.
- Cerrar F-007: agregar `LICENSE` o declarar explícitamente "uso interno, no distribuible".
- Cerrar F-008: ejercicio real documentado del mecanismo de revert/restore.

### MEJORAS OPCIONALES

```text
NO RESTAN PUNTOS
NO ACTIVAN QUALITY GATES
NO BLOQUEAN 100/100
NO FORMAN PARTE DEL CAMINO OBLIGATORIO A 100
```

- Borrar las 11 ramas remotas obsoletas (housekeeping, sección J).
- Investigar y documentar el propósito de la PR duplicada #1/#2.

---

## L. NO VERIFICADO

| Capacidad | Motivo | Impacto en puntuación | Cómo verificarlo después |
| --------- | ------ | ---------------------- | -------------------------- |
| Disparo real de `guard-develop-branch.yml` ante un push directo genuino | Nunca ocurrió en la historia del repo (0 issues) | Ya reflejado en F-008 (Q5.4) | Forzar un push directo controlado en un entorno de prueba/fork y observar el resultado real |
| Publicación real de `docs.yml` a GitHub Pages | No existe `main` todavía — condición de diseño, no defecto | Ninguno (Q6.4 ya evaluado como COMPLETO en el estado esperado) | Verificar tras el evento de primera release |
| Comportamiento de `product-tests` más allá del placeholder | No hay stack de producto definido todavía — decisión de alcance explícita | Ninguno (ya evaluado como COMPLETO) | Verificar cuando el stack real se defina en `docs/tecnica/arquitectura.md` |

---

## M. QUALITY GATES

```text
G1 BLOCKER: PASS (ningún hallazgo BLOCKER — sin secretos expuestos, sin pérdida de datos, sin bootstrap de entorno imposible, sin operación destructiva insegura)
G2 CRITICAL: FAIL — F-001 activa este gate → cap 79/100
G3 VERIFICACIÓN ESENCIAL: PASS (bootstrap de entorno —clonar, sincronizar adaptadores, correr pytest— funciona; CI principal verde en el commit exacto; suite principal de tests pasando; la falla de F-004 es del paso de "demostrar el circuito con una feature real", no del bootstrap del entorno en sí, y ya está capturada como MAJOR en Q1/Q2/Q4, no se reinterpreta aquí como G3 para evitar doble conteo)
```

Gate más restrictivo aplicado: **G2 (cap 79/100)**. Score bruto 81.25 > 79 → score final = 79/100.

---

## N. CAMINO MATEMÁTICO A 100

```text
Score actual (bruto): 81.25

F-001 → +5.25  (Q1.2 +1.50, Q1.3 +1.50, Q6.2 +2.25)  [también elimina el Gate G2]
F-002 → +3.00  (Q6.1 +1.50, Q8.3 +1.50)
F-003 → +3.75  (Q3.4 +2.25, Q8.4 +1.50)
F-004 → +4.50  (Q2.1 +0.75, Q4.1 +0.75, Q4.2 +1.50)  [Q1.3 ya contabilizado en F-001]
F-005 → +1.00  (Q4.4)
F-006 → +0.50  (Q7.3)
F-007 → +1.50  (Q7.5)
F-008 → +0.75  (Q5.4)

Suma de recuperables: 5.25+3.00+3.75+4.50+1.00+0.50+1.50+0.75 = 20.25
```

Nota de consistencia: la suma aritmética de "puntos recuperables" por hallazgo (20.25) es mayor que "puntos perdidos" (18.75) porque Q1.3 (3 puntos totales, 1.5 perdidos) está **causado conjuntamente** por F-001 y F-004; el detalle de cada hallazgo lista su contribución conceptual completa a su(s) subcriterio(s), pero al sumar el camino real a 100 sobre la matriz de subcriterios (no sobre hallazgos) la cifra correcta y no duplicada es:

```text
Q1.2 +1.50, Q1.3 +1.50 (una sola vez), Q2.1 +0.75, Q3.4 +2.25, Q4.1 +0.75,
Q4.2 +1.50, Q4.4 +1.00, Q5.4 +0.75, Q6.1 +1.50, Q6.2 +2.25, Q7.3 +0.50,
Q7.5 +1.50, Q8.3 +1.50, Q8.4 +1.50

Total = 18.75

Score bruto esperado tras cerrar F-001..F-008: 81.25 + 18.75 = 100.00
```

Validación obligatoria antes de normalización:

```text
puntos obtenidos (81.25) + puntos recuperables obligatorios (18.75) = puntos aplicables (100.00)  ✓
```

Para eliminar el Gate G2 específicamente (sin necesidad de llegar a 100), basta con cerrar **F-001** de forma demostrable (el próximo merge real de una PR debe mostrar `reviewDecision: APPROVED` ejecutado por el gate automatizado, o la documentación debe dejar de prometer un enforcement técnico que no existe).

---

## O. PLAN DE REMEDIACIÓN

```text
Prioridad: 1 (CRITICAL)
Hallazgo: F-001
Archivo(s): AGENTS.md, README.md, .github/workflows/post-hitl-merge-gate.yml, scripts/complete-approved-pr.ps1, .github/workflows/guard-develop-branch.yml
Cambio exacto: (a) documentar honestamente la práctica real de merge manual si se acepta como definitiva, o (b) hacer que guard-develop-branch.yml también exija reviewDecision==APPROVED (no solo pertenencia a PR mergeada) para no revertir el commit, cerrando la vía de bypass
Motivo: el "único HITL con enforcement técnico" es la promesa de diseño central del proyecto; hoy no tiene ningún caso real que la confirme
Riesgo: (b) es más invasivo — puede requerir ajustar el flujo de trabajo real del humano; (a) es de bajo riesgo pero reduce la promesa de gobernanza del proyecto
Puntos recuperables: +5.25 (y elimina el Gate G2, +2 puntos adicionales de techo: 79→81.25 posible de inmediato solo por eliminar el gate, incluso antes de sumar los +5.25)
Verificación: repetir V-07/V-08/V-09 sobre la siguiente PR real mergeada

Prioridad: 2 (MAJOR)
Hallazgo: F-002
Archivo(s): .github/workflows/post-hitl-merge-gate.yml, AGENTS.md
Cambio exacto: cambiar el resultado del job a algo distinto de success cuando la rama no matchea ningún patrón reconocido; documentar chore/<slug> como patrón válido con sus propias reglas
Motivo: un check verde debe significar "verificado", nunca "no evaluado"
Riesgo: bajo — cambio acotado a un job de CI
Puntos recuperables: +3.00
Verificación: disparar el workflow contra una rama no reconocida y confirmar que ya no reporta success

Prioridad: 3 (MAJOR)
Hallazgo: F-003
Archivo(s): AGENTS.md (o runs/ del cambio correspondiente)
Cambio exacto: definir explícitamente si cambios de gobernanza del propio circuito requieren circuito SDD completo o un artefacto mínimo alternativo, y aplicarlo
Motivo: trazabilidad del propio commit auditado
Riesgo: bajo
Puntos recuperables: +3.75
Verificación: el próximo cambio de esta naturaleza tiene runs/ completo o excepción documentada

Prioridad: 3 (MAJOR)
Hallazgo: F-004
Archivo(s): README.md
Cambio exacto: reescribir PASO 2/PASO 3 para reflejar el flujo real (start-work-unit.ps1 → circuito completo → ready-for-pr.ps1)
Motivo: bootstrap reproducible tal como se documenta
Riesgo: bajo
Puntos recuperables: +4.50
Verificación: ejecutar el Quick Start actualizado en checkout limpio sin errores inesperados

Prioridad: 4 (MINOR)
Hallazgo: F-005
Archivo(s): AGENTS.md
Cambio exacto: agregar sección normativa sobre chore/<slug>
Puntos recuperables: +1.00
Verificación: grep "chore/" AGENTS.md con contenido normativo

Prioridad: 4 (MINOR)
Hallazgo: F-008
Archivo(s): N/A (ejercicio operativo, no cambio de código)
Cambio exacto: ejercicio controlado documentado de un push directo real
Puntos recuperables: +0.75
Verificación: evidencia de al menos un disparo real exitoso

Prioridad: 4 (MINOR)
Hallazgo: F-007
Archivo(s): LICENSE (nuevo)
Cambio exacto: agregar licencia o declarar uso interno no distribuible
Puntos recuperables: +1.50
Verificación: ls LICENSE* encuentra el archivo, o AGENTS.md declara la intención

Prioridad: 4 (MINOR)
Hallazgo: F-006
Archivo(s): .github/workflows/*.yml
Cambio exacto: fijar actions/checkout y actions/setup-python por SHA
Puntos recuperables: +0.50
Verificación: grep confirma SHAs de 40 caracteres
```

---

## P. SEGUNDA PASADA DE 100

```text
N/A
```

El score provisional (81.25 bruto / 79 final) no es 100/100 — la segunda pasada de refutación obligatoria (§36 AUDIT_PROMPT, §94-95 AUDIT_RULES, §98 profile TEMPLATE) **no corresponde** en este ciclo. Corresponderá únicamente cuando, tras remediar F-001 a F-008 y volver a auditar desde cero contra el commit resultante, la puntuación provisional vuelva a alcanzar 100/100.

---

## Q. CERTIFICACIÓN FINAL

> ¿Puede este repositorio considerarse actualmente un TEMPLATE PROFESIONAL DE REFERENCIA?

```text
NO
```

El diseño del circuito agéntico es sólido, bien testeado en aislamiento y sin secretos ni residuos de origen. Pero la evidencia real de GitHub —no simulada, no histórica de auditorías previas, recolectada de cero en esta sesión— muestra que su promesa de gobernanza central (único HITL con enforcement técnico real) no se ha ejercido con éxito ni una sola vez en 21/21 merges reales, incluido el que produjo el commit exacto auditado, y que ese mismo commit se produjo sin ningún artefacto del circuito SDD que el proyecto declara obligatorio. Un template de referencia debe demostrar, con evidencia y no solo con diseño, que el proceso que documenta es el proceso que realmente ocurre. Hoy no lo demuestra. Es un **APTO CON CORRECCIONES** (79/100, gate CRITICAL activo) con una ruta de remediación clara, acotada y matemáticamente completa hacia 100/100 (sección N/O).
