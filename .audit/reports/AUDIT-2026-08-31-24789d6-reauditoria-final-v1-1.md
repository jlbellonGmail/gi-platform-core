# AUDIT-2026-08-31-24789d6-reauditoria-final-v1-1

Reauditoría final independiente, ejecutada desde cero, sin usar como
entrada scores, hallazgos ni conclusiones de auditorías anteriores
(`.audit/reports/AUDIT-2026-08-29-*`, `AUDIT-2026-08-30-*`,
`AUDIT-2026-08-31-7964013-*`). Esas auditorías se consultan únicamente al
final, en la sección "Comparación histórica".

---

## ADENDA DE CORRECCIÓN METODOLÓGICA (post-emisión, mismo commit `24789d6`)

Este informe fue revisado tras su emisión inicial por dos observaciones
metodológicas concretas. Ninguna implicó volver a inspeccionar código,
documentación, configuración, workflows o tests: la evidencia ya
reunida (Sección G, en particular V12, V13, V14) ya sostenía la
corrección; solo se corrigió la interpretación del framework aplicada a
esa evidencia. Cambios aplicados:

1. **F-002 reclasificado de MAJOR puntuable a `SUGGESTION`.** La
   evidencia ya recolectada (V13: `03-guard-historical-403-failure-excerpt.txt`)
   muestra que, ante el fallo de `gh api`, el paso "Detectar violacion"
   termina con `##[error]Process completed with exit code 1` y el job
   completo queda `conclusion: failure` — visible en rojo en la pestaña
   Actions. Esto significa que Q8.3 ("los flujos no deben aparentar
   éxito cuando una operación crítica ha fallado") **no presenta un
   falso éxito**: el guard no afirma "sin violación" de cara al
   operador, afirma "el run falló". Que no exista además un estado
   `check-failed` explícito ni un issue de incidente dedicado a ese
   caso es una mejora de **observabilidad** (distinguir "violación
   descartada" de "verificación inconclusa" dentro del run rojo), no un
   requisito para cumplir Q8.3 tal como lo define `QUALITY_SCORE.md`.
   Se corrige: 0 puntos perdidos, no forma parte del camino obligatorio
   a 100, no activa ningún Quality Gate. Pasa a listarse junto con las
   demás mejoras opcionales en la Sección K.
2. **F-003 mantenido como NO VERIFICADO / MINOR, -1.00 en Q5.3, pero se
   endurece su cierre.** La corrección mínima suficiente y la
   verificación de cierre originales ofrecían la documentación manual
   explícita como alternativa suficiente a un job de CI real. Se
   elimina esa alternativa: recuperar Q5.3 exige evidencia **ejecutable
   real** de los 7 tests pasando (preferentemente un job `windows-latest`
   en CI, o cualquier otra ejecución reproducible y verificable por un
   tercero), no una nota de procedimiento manual sin ejecución asociada.
3. **Recálculo completo** de puntos por área, subcriterios, hallazgos,
   causas raíz, camino a 100 y plan de remediación (Secciones B, E, F,
   H, I, K, M, N, O, Q y RESULTADO FINAL).

**Resultado de la corrección:** consistencia metodológica **PASS**.
Score bruto corregido: **97.50/100** (antes 97.00). Score final:
**97.50/100** (sin cambio de Quality Gate: seguía sin activarse antes y
después). Puntos recuperables obligatorios: **2.50** (antes 3.00).
`97.50 + 2.50 = 100.00` — cierra exactamente.

---

## A. IDENTIFICACIÓN

```text
Repositorio: jlbellonGmail/template (GitHub, privado)
Ruta local: D:\proyectos\template
Branch: chore/reauditoria-final-v1.1
Commit: 24789d62e44f3eec2d44622f709ff5c024f70369 (24789d6)
Tag: audit-framework-v1.1.0 (ver hallazgo F-004; no es tag de release del
     producto)
Fecha: 2026-08-31
Worktree: LIMPIO (verificado con `git status` antes de cualquier
          operación; confirmado limpio nuevamente al cierre, salvo el
          artefacto de evidencia nuevo de esta propia auditoría)
Sistema operativo: Windows 11 Pro for Workstations (auditor)
Runtime/tooling relevante: Python 3.14 + pytest 9.1.1, PowerShell 5.1
  Desktop (`powershell.exe`) y PowerShell 7.6.4 Core (`pwsh`), Git,
  GitHub CLI 2.97.0 (autenticado, scopes: gist, read:org, repo, workflow),
  MkDocs 1.6.1 + mkdocs-material
QUALITY_SCORE: 1.1
AUDIT_RULES: 1.1
Perfil: TEMPLATE 1.1
Nivel de confianza: ALTA
```

HEAD verificado exactamente contra el commit exigido antes de cualquier
otra operación (`git rev-parse HEAD` = `24789d62e44f3eec2d44622f709ff5c024f70369`).
Branch verificado (`chore/reauditoria-final-v1.1`). Worktree limpio
confirmado (`git status` → "nothing to commit, working tree clean").

---

## B. VEREDICTO EJECUTIVO

```text
Score bruto: 97.50/100
Score final: 97.50/100
Quality Gate aplicado: ninguno (G1 PASS, G2 PASS, G3 PASS)
Confianza: ALTA
Estado: APTO CON CORRECCIONES
Consistencia metodológica: PASS
```

Resumen: el template tiene una implementación sólida del circuito
agéntico (5 roles, HITL único, contrato de artefactos, gate post-HITL,
cierre automatizado de ROADMAP.md, guard técnico de `develop` con 18
tests dedicados y evidencia real de funcionamiento correcto en el propio
commit auditado), documentación extensa y mayormente coherente, sin
secretos ni residuos reales, sin BLOCKER ni CRITICAL. Se encontraron 1
hallazgo MAJOR y 3 MINOR puntuables, más 1 hallazgo adicional
clasificado `SUGGESTION` (no puntuable), todos con evidencia
reproducible: (1) el script de sincronización de adaptadores agénticos
produce un falso positivo bajo Windows PowerShell Desktop —la
herramienta que `AGENTS.md` declara como requerida— mientras que CI y
`README.md` usan PowerShell Core; (2) [`SUGGESTION`, no puntuable] el
guard técnico de `develop` no distingue explícitamente, dentro de un
run ya visiblemente fallido, "violación descartada" de "verificación
inconclusa" ante un fallo inesperado de la API de GitHub durante la
detección — el run queda en rojo de todas formas, sin falso éxito, pero
sin un incidente auditable dedicado a ese caso concreto; (3) la suite de
tests del reconciliador local de Windows (7 tests) no tiene ningún
entorno —ni CI ni esta auditoría— donde se haya demostrado pasando en el
commit auditado; (4) `AGENTS.md` afirma en presente que "no hay ningún
tag" en el estado inicial del template, pero ya existe un tag/release
(`audit-framework-v1.1.0`); (5) `README.md` afirma "14 scripts
PowerShell" cuando existen 12.

---

## C. ALCANCE Y LIMITACIONES

**Inspeccionado:** estructura completa del repositorio, `AGENTS.md`,
`README.md`, `ROADMAP.md`, `.agentic/*`, `.github/workflows/*.yml`,
`scripts/*.ps1`, `tests/*.py`, `docs/` completo (técnica, usuario,
producto), `runs/00`..`05` y su trazabilidad, `.audit/*` (framework y
reportes históricos, solo al final).

**Ejecutado:**
- `git rev-parse HEAD`, `git status`, `git log`, `git branch -a`, `git tag`.
- `pytest -v` local, dos corridas completas (basetemp alternativo por
  una limitación de permisos del propio entorno del auditor).
- `pwsh`/`powershell.exe` `scripts/sync-agentic-adapters.ps1 -Check`
  bajo ambas ediciones de PowerShell, y `-AutoFix` en un
  `git worktree` aislado (no en el repo real) para diffear la
  divergencia exacta.
- `mkdocs build --strict` con `--site-dir` fuera del repo.
- Consultas en vivo a la API de GitHub: CI runs y jobs del commit exacto,
  logs de un run histórico fallido del guard, branch protection de
  `develop` (403 confirmado en vivo), default workflow permissions del
  repo, tags/releases existentes, visibilidad del repositorio.
- Búsqueda de secretos/residuos/hardcodes en todo el árbol versionado.
- Verificación cruzada de índices de documentación (`docs/tecnica/index.md`,
  `docs/usuario/index.md`) contra archivos reales y contra `ROADMAP.md`.
- Verificación de que los 12 scripts en `scripts/` están referenciados
  en `AGENTS.md`/`README.md`/tests (sin scripts huérfanos).

**No verificado / limitación del entorno:**
- `tests/test_local_reconciler_scripts.py` (7 tests): en el entorno de
  esta auditoría (Windows con las mismas condiciones que el propio
  proyecto documenta como riesgo: "EDR/antivirus agresivo bloquea el
  reconciliador local", ver `docs/tecnica/circuito-agentico.md`) los
  tests fallaron con el síntoma exacto documentado ("El reconciliador de
  99-demo no arranco en 60.0s"). CI nunca ejecuta estos tests (se
  saltan por diseño en Linux). Ver hallazgo F-003.
- Configuración de GitHub Pages: no verificable de forma no invasiva sin
  acceder a Settings vía UI; no se intentó (fuera del alcance de una
  auditoría de solo lectura sobre el repo).

---

## D. CONTRATO DETECTADO

| ID | Capacidad/Requisito | Clasificación | Fuente | Estado |
| -- | -------------------- | -------------- | ------ | ------ |
| C1 | Circuito agéntico de 5 roles (analyst→reviewer→builder→qa→code-reviewer) | OBLIGATORIO | AGENTS.md | VERIFICADO (`.agentic/roles/*.md`, `.claude/agents/*.md` generados, tests e2e) |
| C2 | Único HITL: decisión MERGE/NO MERGE sobre PR con CI verde | OBLIGATORIO | AGENTS.md | VERIFICADO (post-hitl-merge-gate.yml, tests dedicados) |
| C3 | Contrato de artefactos por feature (spec/plan/tasks/audit/test-report/code-review/decision/docs) | OBLIGATORIO | AGENTS.md, feature-contract.ps1 | VERIFICADO (6 items `[x]` en ROADMAP.md, todos con el set completo) |
| C4 | Guard técnico de `develop` (mitigación de branch protection no disponible) | OBLIGATORIO | AGENTS.md, guard-develop-branch.yml | VERIFICADO (mejora de observabilidad opcional identificada, F-002, `SUGGESTION`) |
| C5 | Cierre automático post-merge de ROADMAP.md | OBLIGATORIO | AGENTS.md, post-merge-close-feature.yml | DOCUMENTADO + IMPLEMENTADO (no se forzó un merge real durante la auditoría; evidencia indirecta: histórico de ROADMAP.md coherente en 6 items) |
| C6 | CI con dos jobs gate (`circuit-tests`, `product-tests`) | OBLIGATORIO | AGENTS.md, ci.yml | VERIFICADO (run real verde en el commit auditado) |
| C7 | Fuente única `.agentic/` + adaptadores generados + `-Check` de drift | OBLIGATORIO | AGENTS.md | PARCIALMENTE VERIFICADO (F-001: `-Check` da falso positivo bajo PowerShell Desktop) |
| C8 | Sin stack de producto propio; `product-tests` es placeholder deliberado | DECLARADO | AGENTS.md, ci.yml | VERIFICADO (coherente, sin contradicción) |
| C9 | Modo Milestone además de Feature | OBLIGATORIO (cuando aplica) | AGENTS.md, workunit-lib.ps1 | VERIFICADO (tests dedicados extensos, sin evidencia de uso real todavía, pero no exigido) |
| C10 | Windows/PowerShell como plataforma primaria, `pwsh` para portabilidad | DECLARADO | AGENTS.md, docs/tecnica/arquitectura.md, README.md | PARCIALMENTE COHERENTE (F-001: AGENTS.md usa `powershell` en sus propios ejemplos, README usa `pwsh`) |
| C11 | Sin tags/releases del producto antes de la primera release a `main` | OBLIGATORIO | AGENTS.md | CONTRADICHO EN SU LITERALIDAD por un tag no relacionado con el producto (F-004) |
| C12 | `docs/producto/contexto-producto.md` como contexto persistente | RECOMENDADO | AGENTS.md | VERIFICADO (existe, contenido real, no vacío) |

---

## E. MATRIZ DE PUNTUACIÓN

| Área                          |  Máximo | Obtenido | Estado |
| ----------------------------- | ------: | -------: | ------ |
| Q1 Conformidad con el contrato |      12 |    11.25 | MENOR en Q1.3 |
| Q2 Reutilización y limpieza    |      12 |    12.00 | COMPLETO |
| Q3 Arquitectura y mantenibilidad |    12 |    12.00 | COMPLETO |
| Q4 Documentación y DX          |      12 |    11.25 | MENOR en Q4.1 |
| Q5 Calidad, pruebas y regresión |     16 |    15.00 | MENOR en Q5.3 |
| Q6 Git, CI/CD, versionado y releases | 16 |   16.00 | COMPLETO |
| Q7 Seguridad y software supply chain | 12 |   12.00 | COMPLETO |
| Q8 Automatización y gobernanza  |       8 |     8.00 | COMPLETO |
| **TOTAL**                      | **100** | **97.50** |        |

Sin criterios `N/A` en esta auditoría (todos los subcriterios de
`QUALITY_SCORE.md` fueron aplicables al alcance de este template en el
commit auditado). Puntos aplicables = 100. Sin normalización necesaria.

---

## F. DETALLE POR SUBCRITERIO

| ID | Criterio | Máx. | Nivel | Obtenido | Evidencia | Hallazgo | Justificación |
| -- | -------- | ---: | ----- | -------: | --------- | -------- | ------------- |
| Q1.1 | Propósito y alcance | 3 | COMPLETO | 3.00 | AGENTS.md completo; ROADMAP.md "Propósito del producto: Por definir" (honesto, no ambiguo) | — | Alcance sin stack propio, declarado explícitamente y consistente en todo el árbol. |
| Q1.2 | Capacidades prometidas presentes | 3 | COMPLETO | 3.00 | 5 agentes, CI, guard, HITL, docs, milestone mode, router de modelos: todos verificados presentes | — | El único gap de "capacidad prometida" (drift-check) sí funciona; falla solo bajo una edición específica de PowerShell (penalizado en Q1.3). |
| Q1.3 | Coherencia entre fuentes | 3 | MENOR | 2.25 | Ver F-001, F-004 | F-001, F-004 | Dos contradicciones reales y verificadas entre `AGENTS.md`/`README.md`/estado observado; el resto del árbol documental es coherente. |
| Q1.4 | Ausencia de requisitos obligatorios incompletos | 3 | COMPLETO | 3.00 | ROADMAP.md: 6 items `[x]` completos con contrato íntegro, 1 item `[ ]` correctamente pendiente, 0 items `[-]` colgados | — | Sin features marcadas como terminadas que estén realmente incompletas. |
| Q2.1 | Inicialización reproducible | 3 | COMPLETO | 3.00 | README PASO 1-2 ejecutado conceptualmente contra el commit: `pwsh sync-agentic-adapters.ps1` (sin `-Check`), `pytest -v tests/` (verificado, ver Q5.3), `mkdocs build --strict` (PASS) | — | Camino de adopción documentado es consistente y no depende de conocimiento oculto. |
| Q2.2 | Ausencia de residuos específicos | 3 | COMPLETO | 3.00 | Búsqueda de secretos/emails/rutas personales: sin hallazgos fuera de evidencia histórica legítima en `runs/*/test-report-*.md` (excepción explícita del propio perfil TEMPLATE §Q2.2) | — | Sin contaminación real del origen. |
| Q2.3 | Configuración y personalización clara | 3 | COMPLETO | 3.00 | `docs/producto/contexto-producto.md` y ROADMAP marcan explícitamente "Por definir"; `docs/tecnica/arquitectura.md` es el punto de decisión de stack | — | Elementos a cambiar están identificados sin ambigüedad. |
| Q2.4 | Portabilidad y extensibilidad | 3 | COMPLETO | 3.00 | Decisión Windows/PowerShell explícita y documentada (`docs/tecnica/arquitectura.md`), con excepción única y honesta (reconciliador local) | — | Cumple el criterio de "plataforma específica declarada" del perfil; sin dependencias accidentales de máquina. |
| Q3.1 | Estructura coherente | 3 | COMPLETO | 3.00 | `runs/`, `.agentic/`, `docs/{tecnica,usuario,producto}/`, `scripts/`, `tests/` con propósito claro y estable | — | — |
| Q3.2 | Separación de responsabilidades | 3 | COMPLETO | 3.00 | 5 roles con tools/permission declarados por separado; `.agentic/roles/*.md` fuente única + adaptadores por herramienta | — | — |
| Q3.3 | Simplicidad y duplicación | 3 | COMPLETO | 3.00 | 12/12 scripts referenciados (sin huérfanos); sin duplicación manual detectada fuera de adaptadores requeridos | — | — |
| Q3.4 | Evolución | 3 | COMPLETO | 3.00 | Mecanismo de detección de drift (`sync-agentic-adapters.ps1 -Check`) existe arquitectónicamente; su bug de formato entre ediciones de PowerShell es un defecto de implementación puntual, no un defecto de diseño de la fuente única (penalizado en Q1.3) | — | — |
| Q4.1 | README funcional | 3 | MENOR | 2.25 | README.md línea 67: "scripts/ - Motor ejecutable (14 scripts PowerShell)"; conteo real: 12 | F-005 | Dato concreto, verificable y desactualizado en el punto de entrada principal del proyecto. |
| Q4.2 | Instalación y bootstrap | 3 | COMPLETO | 3.00 | Camino único y explícito en README (3 pasos), sin comandos contradictorios dentro del propio README | — | — |
| Q4.3 | Operaciones habituales | 2 | COMPLETO | 2.00 | AGENTS.md documenta ready-for-pr, wait-pr-ci, close-feature, start-work-unit, resolve-agentic-model con ejemplos ejecutables | — | — |
| Q4.4 | Convenciones de contribución | 2 | COMPLETO | 2.00 | AGENTS.md cumple el rol de CONTRIBUTING de forma extensa (circuito completo, retornos permitidos, reglas de dominio) | — | — |
| Q4.5 | Ejemplos y troubleshooting | 2 | COMPLETO | 2.00 | Sección EDR/antivirus en `docs/tecnica/circuito-agentico.md` es troubleshooting de alta calidad, verificado como exacto durante esta misma auditoría | — | — |
| Q5.1 | Controles automáticos | 3 | COMPLETO | 3.00 | Validación JSON Schema (`jsonschema`), validación de YAML de workflows, drift-check de adaptadores | — | — |
| Q5.2 | Estrategia de pruebas | 3 | COMPLETO | 3.00 | Tests de contrato, e2e, comportamiento de workflows (guard, gates), schemas, feature/milestone — proporcional al riesgo | — | — |
| Q5.3 | Tests ejecutables y pasando | 4 | MENOR | 3.00 | CI (commit exacto): 180 passed, 10 skipped (deliberados y documentados), 0 failed. Localmente: 3 tests de `test_local_reconciler_scripts.py` no pudieron verificarse pasando en ningún entorno de esta auditoría | F-003 | Evidencia fuerte para el 96%+ de la suite; 7 tests (3.7%) sin verificación de paso posible en ningún entorno disponible para esta auditoría. |
| Q5.4 | Protección frente a regresiones | 3 | COMPLETO | 3.00 | `test_guard_workflow_declares_least_privilege_permissions` y suite de 18 tests del guard, añadidos tras incidentes reales documentados en el historial | — | — |
| Q5.5 | Quality gates | 3 | COMPLETO | 3.00 | `circuit-tests` y `product-tests` ambos gate obligatorio (AGENTS.md, confirmado en ci.yml); QA/code-reviewer como gates internos del circuito | — | — |
| Q6.1 | Estrategia Git | 3 | COMPLETO | 3.00 | develop + feature//milestone worktrees, ciclo de vida pre/post-`main` documentado sin contradicciones | — | — |
| Q6.2 | Protección e integración | 3 | COMPLETO | 3.00 | Branch protection nativa no disponible (403 verificado en vivo); guard-develop-branch.yml como control alternativo extensamente testeado (18 tests) y con evidencia real de funcionamiento correcto en el propio commit auditado (run 33420464281) | — | Objetivo de control satisfecho por control técnico alternativo verificable, per perfil TEMPLATE §Q6.2. La mejora de observabilidad identificada (F-002) es `SUGGESTION`, no afecta este criterio. |
| Q6.3 | CI reproducible | 3 | COMPLETO | 3.00 | CI verde real en el commit exacto (circuit-tests + product-tests); sin `continue-on-error` ni patrones de falso-éxito en ci.yml | — | La divergencia `pwsh` (CI) vs `powershell` (AGENTS.md) para `sync-agentic-adapters.ps1` es la misma causa raíz que F-001, ya penalizada en Q1.3. |
| Q6.4 | Versionado y releases | 3 | COMPLETO | 3.00 | Release del producto declarada explícitamente como prospectiva/futura (sin `main` todavía); no exigible en el estado actual per regla explícita de AUDIT_RULES §45 | — | El tag `audit-framework-v1.1.0` no es el release del producto; su contradicción textual con AGENTS.md se evalúa en Q1.3, no aquí. |
| Q6.5 | Build y artefactos | 2 | COMPLETO | 2.00 | `mkdocs build --strict` verificado exitoso (exit 0) sobre el commit auditado | — | — |
| Q6.6 | Compatibilidad/rollback | 2 | COMPLETO | 2.00 | Modelo "snapshot" declarado explícitamente en `docs/tecnica/arquitectura.md`; sin promesa de sincronización posterior | — | — |
| Q7.1 | Gestión de secretos | 3 | COMPLETO | 3.00 | Búsqueda de patrones de secretos en todo el árbol versionado: sin coincidencias reales, solo nombres de variables de entorno documentadas | — | — |
| Q7.2 | Dependencias | 2 | COMPLETO | 2.00 | `requirements-dev.txt` mínimo (pytest, jsonschema), sin dependencias no usadas | — | — |
| Q7.3 | Seguridad de CI/CD | 2 | COMPLETO | 2.00 | 4/5 workflows con permisos mínimos explícitos; `ci.yml` sin bloque `permissions:` pero default_workflow_permissions del repo verificado en vivo = `read` (comportamiento efectivo seguro); `post-hitl-merge-gate.yml` hace checkout de código confiable de `develop`, no de la rama de la PR | — | Comportamiento efectivo verificado seguro (Nivel 3). Agregar `permissions: contents: read` explícito a `ci.yml` es mejora de defensa en profundidad, no defecto puntuable (ver Sección K, mejoras opcionales). |
| Q7.4 | Defaults seguros | 2 | COMPLETO | 2.00 | `--force-with-lease` atado a `AFTER`, nunca `--force` a secas; grupos de concurrencia en los 4 workflows con lógica crítica | — | — |
| Q7.5 | Supply chain | 3 | COMPLETO | 3.00 | Actions oficiales pinneadas a tag de versión mayor (`@v4`/`@v5`); sin LICENSE (repo privado sin distribución, justificado per perfil §25) | — | — |
| Q8.1 | Fuente única de verdad | 2 | COMPLETO | 2.00 | `.agentic/` canónico + adaptadores generados + drift-check arquitectónicamente sólido | — | — |
| Q8.2 | Responsabilidades y límites | 2 | COMPLETO | 2.00 | 5 roles con tools/permission/escalamiento declarados sin superposición ambigua | — | — |
| Q8.3 | Fail-safe | 2 | COMPLETO | 2.00 | V13: ante el fallo de `gh api`, el paso "Detectar violacion" termina con `##[error]Process completed with exit code 1` y el job queda `conclusion: failure`, visible en la pestaña Actions | F-002 (`SUGGESTION`, 0 puntos) | El criterio exige que los flujos "no aparenten éxito cuando una operación crítica ha fallado". El guard cumple: nunca aparenta éxito, el run queda en rojo. Que no distinga explícitamente "violación descartada" de "verificación inconclusa" dentro de ese run rojo (F-002) es una mejora de observabilidad, no un incumplimiento de Q8.3 tal como lo define `QUALITY_SCORE.md`. |
| Q8.4 | Trazabilidad | 2 | COMPLETO | 2.00 | `runs/<slug>/` con contrato completo, ROADMAP.md coherente con el estado real, PRs con evidencia | — | — |

**Suma de verificación:** Q1=11.25, Q2=12.00, Q3=12.00, Q4=11.25, Q5=15.00,
Q6=16.00, Q7=12.00, Q8=8.00. Total = 97.50.

---

## G. LEDGER DE VERIFICACIÓN

| ID | Verificación | Comando/Método | Resultado | Estado | Evidencia |
| -- | ------------ | --------------- | --------- | ------ | --------- |
| V01 | HEAD = commit exigido | `git rev-parse HEAD` | `24789d62e44f...` | PASS | 00-git-log.txt |
| V02 | Worktree limpio | `git status` | "nothing to commit" | PASS | (inline, sesión) |
| V03 | Suite de tests, CI real | `gh api .../actions/jobs/99581278882/logs` | 180 passed, 10 skipped, 0 failed | PASS | 09-ci-pytest-log.txt |
| V04 | CI verde en commit exacto | `gh api .../commits/24789d6.../check-runs` | circuit-tests, product-tests, guard-develop: los 3 success | PASS | 02-ci-run-24789d6.json, 02-guard-run-24789d6.json |
| V05 | Suite de tests local (Windows, ambas ediciones) | `pytest -v --basetemp=...` (2 corridas) | 187 passed, 3 failed (test_local_reconciler_scripts.py) | FAIL LOCAL / NO VERIFICADO — LIMITACIÓN DEL ENTORNO | 01-pytest-local.txt |
| V06 | Adapters drift-check bajo PowerShell Desktop | `powershell -File sync-agentic-adapters.ps1 -Check` | 2 archivos "divergentes" | FAIL (real, F-001) | 04-adapters-check.txt |
| V07 | Adapters drift-check bajo PowerShell Core | `pwsh -File sync-agentic-adapters.ps1 -Check` | "Adaptadores agenticos sincronizados" | PASS | (inline, sesión) |
| V08 | Diff real de la divergencia (worktree aislado) | `-AutoFix` en worktree separado + `git diff` | Solo formato de `ConvertTo-Json` para objetos vacíos difiere entre PSEdition | CONFIRMADO | 10-adapters-desktop-vs-core-divergence.md |
| V09 | mkdocs build reproducible | `mkdocs build --strict --site-dir <fuera del repo>` | exit 0 | PASS | 06-mkdocs-build.txt |
| V10 | Branch protection nativa de `develop` | `gh api .../branches/develop/protection` | 403 "Upgrade to GitHub Pro..." | NO DISPONIBLE (verificado en vivo, consistente con AGENTS.md) | (inline, sesión) |
| V11 | Rulesets nativos | `gh api .../rulesets` | 403 (mismo motivo) | NO DISPONIBLE (verificado en vivo) | (inline, sesión) |
| V12 | Guard-develop: ejecución real en el commit auditado | `gh api .../actions/jobs/99581279179/logs` | No-op correcto (push era merge de PR legítima) | PASS | 02-guard-run-24789d6.json |
| V13 | Guard-develop: incidente histórico real | `gh run view 33342778808` + logs | Fallo por 403 en `commits/{sha}/pulls`, causado por falta de `pull-requests: read` en ese momento (corregido en `155b9cb`, ancestro de HEAD); el paso terminó con `##[error]Process completed with exit code 1` y el job quedó `conclusion: failure` (visible en rojo) | CONFIRMADO — sin falso éxito (F-002, `SUGGESTION`: falta un estado explícito de "verificación inconclusa" dentro de ese run ya visiblemente fallido) | 03-guard-historical-403-failure-excerpt.txt |
| V14 | Permisos efectivos del token en el commit auditado | `gh api .../actions/jobs/99581279179/logs` (sección "GITHUB_TOKEN Permissions") | Contents:write, Issues:write, Metadata:read, PullRequests:read | CONFIRMADO (fix vigente) | (inline, sesión) |
| V15 | Secretos en el árbol versionado | grep de patrones de credenciales | Sin coincidencias reales | PASS | 05-secrets-grep-files.txt |
| V16 | Scripts huérfanos | referencias cruzadas de los 12 `.ps1` contra docs/tests | 12/12 referenciados | PASS | 08-scripts-referenced.txt |
| V17 | Índices de documentación completos | grep cruzado docs/tecnica, docs/usuario, index.md | 6/6 items enlazados en ambos índices | PASS | (inline, sesión) |
| V18 | Coherencia de ROADMAP.md | lectura directa | 6 `[x]` completos con contrato íntegro, 1 `[ ]`, 0 `[-]` colgados | PASS | (inline, sesión) |
| V19 | Permisos por defecto de Actions del repo | `gh api .../actions/permissions/workflow` | `default_workflow_permissions: read` | CONFIRMADO (mitiga ausencia de bloque explícito en ci.yml) | 11-actions-default-permissions.json |
| V20 | Tags/releases existentes | `git tag -l`, `gh release list` | `audit-framework-v1.1.0` (release publicado 2026-08-30) | CONFIRMADO (F-004) | 12-audit-framework-tag-release.txt |
| V21 | Conteo real de scripts vs README | `find scripts -name "*.ps1" \| wc -l` | 12 (README afirma 14) | CONFIRMADO (F-005) | (inline, sesión) |
| V22 | Esquemas JSON de `.agentic/` | `pytest tests/test_agentic_schemas.py tests/test_agents_e2e.py` | 24 passed | PASS | (inline, sesión) |
| V23 | `.opencode/node_modules` no versionado | `git ls-files .opencode/`, `git check-ignore` | 3 archivos trackeados (no node_modules); ignorado correctamente | PASS (no es residuo del template) | (inline, sesión) |
| V24 | Visibilidad del repositorio | `gh repo view --json visibility` | PRIVATE | CONFIRMADO (contexto para Q7.5/LICENSE) | (inline, sesión) |

---

## H. HALLAZGOS

| ID | Tipo | Severidad | Hallazgo | Evidencia | Criterio | Puntos |
| -- | ---- | --------- | -------- | --------- | -------- | -----: |
| F-001 | CONTRADICTORIO, INCORRECTO | MAJOR | `sync-agentic-adapters.ps1 -Check` da falso positivo bajo PowerShell Desktop (herramienta declarada requerida por AGENTS.md); AGENTS.md y README.md dan instrucciones contradictorias sobre qué intérprete usar para los mismos comandos | V06, V07, V08 | Q1.3 | -0.75 |
| F-002 | RIESGO (observabilidad) | `SUGGESTION` | El guard de `develop` escribe un "default seguro" (`violation=none`) antes de completar la verificación; un fallo inesperado de la API de GitHub durante la detección deja ese default sin generar un incidente auditable dedicado — pero el paso y el job sí terminan visiblemente en rojo (`exit code 1`, `conclusion: failure`), sin aparentar éxito en ningún momento | V12, V13, V14 | — (no puntuable) | 0 |
| F-003 | NO VERIFICADO | MINOR | 7 tests de `test_local_reconciler_scripts.py` no tienen ningún entorno (CI los salta por diseño en Linux; esta auditoría los bloqueó por la misma limitación de EDR/antivirus ya documentada por el propio proyecto) donde se demuestren pasando en el commit auditado | V05 | Q5.3 | -1.00 |
| F-004 | CONTRADICTORIO | MINOR | AGENTS.md afirma en presente "no hay ningún tag" en el estado inicial del template; ya existe `audit-framework-v1.1.0` (tag + release publicado) | V20 | Q1.3 (incluido en F-001) | (incluido) |
| F-005 | INCORRECTO, OBSOLETO | MINOR | README.md afirma "14 scripts PowerShell"; existen 12 | V21 | Q4.1 | -0.75 |

**Total de puntos perdidos: 2.50** (0.75 en Q1.3 combinando F-001+F-004,
0.75 en Q4.1 por F-005, 1.00 en Q5.3 por F-003). F-002 es `SUGGESTION`:
0 puntos perdidos, no forma parte del camino obligatorio a 100, no
activa ningún Quality Gate.

### F-001 — Falso positivo de `sync-agentic-adapters.ps1 -Check` bajo PowerShell Desktop

**Descripción:** `AGENTS.md`, sección "Herramientas locales requeridas",
declara "Windows PowerShell (`powershell.exe`)" como la herramienta
requerida para `scripts/*.ps1`, y todos sus propios ejemplos de comando
(incluido el de sincronizar/validar adaptadores tras editar `.agentic/`)
usan literalmente `powershell -NoProfile -ExecutionPolicy Bypass -File
...`. Ejecutar exactamente ese comando documentado
(`sync-agentic-adapters.ps1 -Check`) contra los archivos ya commiteados
en el HEAD auditado produce dos falsos "divergente": `.mcp.json` y
`opencode.json`. El mismo comando, mismo commit, bajo `pwsh` (PowerShell
7 Core) —el intérprete que usa `README.md` para los mismos comandos y
que usa `ci.yml` línea 29— pasa limpio. Un diff en un worktree aislado
confirma que la única diferencia es el formato de serialización de
`ConvertTo-Json` para objetos vacíos entre las ediciones Desktop y Core
de PowerShell, no una diferencia de contenido.

**Impacto:** un consumidor del template que siga literalmente
`AGENTS.md` (el documento que el propio perfil TEMPLATE reconoce como
"normativa operativa") en una máquina Windows estándar —PowerShell 5.1
viene preinstalado; PowerShell 7 requiere instalación aparte— obtiene un
falso `FAIL` en el mecanismo de detección de drift que la sección
"Configuración de modelos" de `AGENTS.md` presenta como paso obligatorio
tras editar `.agentic/`. Esto entrena a los operadores a desconfiar o
ignorar ese quality gate, exactamente el patrón de riesgo que
`AUDIT_RULES.md` §44 pide vigilar (aunque en dirección inversa: falso
fallo, no falso éxito).

**Causa raíz:** (a) `ConvertTo-Json` de PowerShell serializa hashtables
vacíos de forma distinta entre `$PSVersionTable.PSEdition = Desktop` y
`= Core`; (b) `AGENTS.md` y `README.md` no están alineados sobre qué
intérprete usar para los mismos scripts, y ninguno de los dos documentos
señala esta inconsistencia.

**Corrección mínima suficiente:** normalizar la generación de JSON en
`scripts/sync-agentic-adapters.ps1` para que sea determinista
independientemente de la edición de PowerShell (por ejemplo, evitar la
ruta de `ConvertTo-Json` que produce el formato inconsistente para
objetos vacíos, o post-procesar/normalizar espacios en blanco antes de
comparar/escribir), y unificar `AGENTS.md`/`README.md` para que
instruyan el mismo intérprete (`pwsh`, consistente con `ci.yml`) para
este script en particular, salvo la excepción ya documentada del
reconciliador local.

**Verificación de cierre:** `powershell -File
scripts/sync-agentic-adapters.ps1 -Check` y `pwsh -File
scripts/sync-agentic-adapters.ps1 -Check` deben devolver ambos exit 0
sobre los mismos archivos commiteados.

**Puntos recuperables:** 0.75 (Q1.3, junto con F-004).

### F-002 — Observabilidad incompleta del guard de `develop` ante fallo de API (`SUGGESTION`, no puntuable)

**Descripción:** en
`.github/workflows/guard-develop-branch.yml`, el paso "Detectar
violacion" escribe `echo "violation=none" >> "$GITHUB_OUTPUT"` como
"default seguro" ANTES de consultar la API de GitHub
(`commits/{sha}/pulls`) para cada commit del push. El script corre bajo
`set -euo pipefail`. Si esa llamada a la API falla por cualquier motivo
inesperado (permisos, rate limit, incidente de GitHub), el paso aborta
inmediatamente con el output `violation=none` ya escrito. Como los pasos
de remediación e incidente están condicionados a
`steps.guard.outputs.violation != 'none'`, ninguno se ejecuta: no se crea
un issue de incidente dedicado, no se revierte ni restaura nada.

**Por qué esto NO es un falso éxito (y por qué no es puntuable en
Q8.3):** el paso "Detectar violacion" en sí mismo, al fallar la llamada
a `gh api` bajo `set -euo pipefail`, termina con
`##[error]Process completed with exit code 1`, y el job completo del
workflow queda `conclusion: failure` — visible en rojo en la pestaña
Actions de GitHub. `QUALITY_SCORE.md` Q8.3 exige que "los flujos no
aparenten éxito cuando una operación crítica ha fallado"; este guard
nunca aparenta éxito en este escenario, aparenta (correctamente) que
algo falló. Lo que falta es más fino: un estado explícito que distinga,
dentro de ese run ya rojo, "se verificó y no hubo violación" de "no se
pudo verificar si hubo violación", junto con un incidente auditable
dedicado a este segundo caso. Eso es una mejora de **observabilidad**
sobre un control que ya falla de forma segura, no un requisito para que
el control cumpla Q8.3.

**Evidencia de que esto ya ocurrió en producción:** el run
`33342778808` (2026-08-30, commit `9616b12`, un merge de PR legítimo)
falló exactamente así: `gh: Resource not accessible by integration
(HTTP 403)` en la llamada a `commits/{sha}/pulls`, causado en ese
momento por la ausencia de `pull-requests: read` en el bloque
`permissions:` del workflow vigente en ese commit — y el job quedó
correctamente marcado `conclusion: failure`, visible como tal. Esa causa
puntual ya fue corregida en `155b9cb` ("Corregir permisos del guard de
develop"), ancestro del commit auditado, y se confirmó en vivo que el
run del guard sobre el propio commit auditado (`33420464281`) sí tiene
`PullRequests: read` concedido y se ejecutó correctamente (no-op, porque
el push era un merge de PR legítimo).

**Impacto:** bajo. Un operador que revise la pestaña Actions ve
correctamente que el guard falló y requiere atención; lo único que no
obtiene automáticamente es la distinción fina de "por qué" (violación
real vs. verificación inconclusa) ni un issue dedicado a ese matiz. No
hay ninguna ventana en la que el sistema comunique "todo bien" cuando no
lo estuvo.

**Causa raíz:** el valor por defecto de `violation` se fija antes de
que termine la clasificación real del push, en vez de después; esto no
genera un falso éxito porque el propio fallo de la llamada ya tumba el
paso bajo `set -e`, pero sí deja sin usar la oportunidad de dar
diagnóstico explícito dentro de ese fallo ya visible.

**Mejora sugerida (no obligatoria):** distinguir explícitamente "no
hubo violación" de "no se pudo determinar si hubo violación" (por
ejemplo, `violation=check-failed` cuando la llamada a `gh api` no
complete), y que ese tercer estado dispare la creación de un incidente
auditable dedicado ("el guard no pudo verificar este push; revisión
manual requerida"), en vez de depender únicamente de que el operador
abra el log del run rojo para entender la causa.

**Verificación de la mejora, si se aplica:** un test que simule un
fallo de `gh api` dentro del loop de commits demostraría que se crea un
issue de incidente con ese estado explícito, además de que el run siga
fallando visiblemente como ya lo hace hoy.

**Puntos recuperables:** ninguno (`SUGGESTION`: 0 puntos perdidos, no
forma parte del camino obligatorio a 100, no activa Quality Gates).

### F-003 — Suite de tests del reconciliador local sin entorno de verificación disponible

**Descripción:** `tests/test_local_reconciler_scripts.py` (7 tests)
tiene un `pytestmark` a nivel de módulo que los salta por completo si
`os.name != "nt"` — es decir, CI (que corre en `ubuntu-latest`) nunca
los ejecuta, por diseño. En el entorno de esta auditoría (Windows, con
PowerShell 5.1 disponible, cumpliendo la condición para que los tests
SÍ intenten ejecutarse) los 3 tests que llegaron a completarse fallaron
con el mensaje "El reconciliador de 99-demo no arranco en 60.0s
(log/lock ausentes)" — el síntoma exacto que
`docs/tecnica/circuito-agentico.md` documenta bajo "Troubleshooting:
EDR/antivirus agresivo bloquea el reconciliador local (Windows)".

**Impacto:** no existe, en esta auditoría, ningún entorno donde se haya
demostrado que estos 7 tests pasan sobre el commit auditado. Esto no
demuestra que el mecanismo esté roto (el propio proyecto ya documenta
esta clase exacta de bloqueo como una limitación ambiental conocida, no
como un defecto del script), pero sí impide otorgar evidencia de
ejecución completa para Q5.3 sobre el 100% de la suite.

**Causa raíz (por diseño, no defecto):** los tests ejercitan
`Start-Process -WindowStyle Hidden` real de PowerShell, un mecanismo
inherentemente específico de Windows y sensible a EDR/antivirus
agresivo, ya reconocido así por el propio equipo del proyecto.

**Clasificación de evidencia:** NO VERIFICADO — LIMITACIÓN DEL ENTORNO
(`AUDIT_RULES.md` §19, Caso B), no un defecto atribuible al proyecto.
Se puntúa como MINOR porque de todas formas impide alcanzar evidencia
completa de "tests ejecutables y pasando" (`QUALITY_SCORE.md` §16: "no
podrá recibir el 100%").

**Corrección mínima suficiente:** agregar un job de CI (preferentemente
opcional/no bloqueante, dado que es limpieza de conveniencia local, no
crítica) en `windows-latest` que ejecute específicamente
`tests/test_local_reconciler_scripts.py` y produzca un resultado
verificable por un tercero. **No es suficiente** documentar un
procedimiento de verificación manual sin ejecución asociada: eso deja
la capacidad exactamente en el mismo estado NO VERIFICADO que hoy, solo
que por escrito. La recuperación de puntos exige evidencia ejecutable
real, no una nota de procedimiento.

**Verificación de cierre:** un run de CI real (idealmente
`windows-latest`, o cualquier otro entorno reproducible y verificable
por un tercero) mostrando los 7 tests pasando sobre un commit dado.
Una nota de troubleshooting o de verificación manual puede acompañar
esa evidencia, pero no reemplazarla.

**Puntos recuperables:** 1.00 (Q5.3), condicionado a la evidencia
ejecutable descrita arriba.

### F-004 — Contradicción entre "no hay ningún tag" y el tag/release existente

**Descripción:** `AGENTS.md`, sección "Versionado (tags)", afirma:
"En el estado inicial del template..., antes de la primera release, no
hay ningún tag — es la misma etapa descrita ahí para `main`, no un caso
aparte." En el commit auditado ya existe el tag `audit-framework-v1.1.0`
y un GitHub Release publicado el 2026-08-30 ("Primera versión estable y
validada del framework de auditoría .audit"), ninguno de los dos
mencionado ni excepcionado en la sección de Versionado de `AGENTS.md`.

**Impacto:** bajo, dado que el tag está claramente nombrado y scoped al
framework `.audit/` interno, no al SemVer del producto (`vX.Y.Z`), y no
hay evidencia de que esto confunda el flujo real de release del
producto. Sigue siendo una afirmación literalmente falsa sobre el
estado observable del repositorio.

**Causa raíz:** `AGENTS.md` no distingue explícitamente entre
"versionado del producto que nace del template" (lo que describe toda
esa sección) y "versionado interno del propio framework de auditoría"
(un artefacto que el propio `.audit/README.md`/`AUDIT_RULES.md`
versionan de forma independiente, como `1.1`).

**Corrección mínima suficiente:** acotar la frase a "no hay ningún tag
de release del producto" o agregar una nota explícita reconociendo
tags/releases del framework `.audit/` como fuera del alcance de esa
sección.

**Verificación de cierre:** relectura de `AGENTS.md` confirmando que ya
no contradice `git tag -l` en su estado literal.

**Puntos recuperables:** incluido en los 0.75 de F-001 (mismo
subcriterio Q1.3).

### F-005 — Conteo de scripts desactualizado en README.md

**Descripción:** `README.md`, sección "Estructura importante", afirma
"`scripts/` - Motor ejecutable (14 scripts PowerShell)". El conteo real
en el commit auditado es 12 (`check-adoption-conflicts.ps1`,
`close-feature.ps1`, `complete-approved-pr.ps1`, `feature-contract.ps1`,
`local-feature-reconcile.ps1`, `ready-for-pr.ps1`,
`resolve-agentic-model.ps1`, `start-work-unit.ps1`,
`sync-agentic-adapters.ps1`, `update-doc-indexes.ps1`,
`wait-pr-ci.ps1`, `workunit-lib.ps1`).

**Impacto:** bajo (no afecta funcionalidad), pero es exactamente el
mismo patrón de defecto que el proyecto ya corrigió antes para el
conteo de tests (ver `docs/tecnica/*` de la baseline v1.1, línea
`tests/` de README ahora dice "correr `pytest -v tests/` para el número
y detalle actuales" en vez de un número fijo) — el conteo de scripts
reintrodujo el mismo anti-patrón sin que la corrección anterior lo
cubriera.

**Causa raíz:** número hardcodeado que no se actualizó cuando cambió la
cantidad real de scripts.

**Corrección mínima suficiente:** corregir "14" a "12", o —consistente
con la solución ya aplicada al conteo de tests— reemplazar el número
fijo por una referencia dinámica ("ver `scripts/` para el listado
actual").

**Verificación de cierre:** `find scripts -name "*.ps1" | wc -l`
coincide con el número en README.md, o el número fijo ya no existe.

**Puntos recuperables:** 0.75 (Q4.1).

---

## I. CAUSAS RAÍZ

| ID | Causa raíz | Hallazgos relacionados | Impacto |
| -- | ---------- | ----------------------- | ------- |
| ROOT-001 | Inconsistencia de intérprete PowerShell documentado (`powershell` en AGENTS.md vs `pwsh` en README.md/CI) combinada con una diferencia real de serialización JSON entre ediciones | F-001 | Q1.3 (único punto de descuento; impacto narrativo compartido con Q6.3, no re-descontado) |
| ROOT-002 | "Default seguro" del guard escrito antes de terminar la verificación real (no genera falso éxito: el paso y el job igual quedan en rojo) | F-002 | Ninguno puntuable — `SUGGESTION` de observabilidad; no afecta Q8.3 ni Q6.2 |
| ROOT-003 | Mecanismo Windows-only (`Start-Process -WindowStyle Hidden`) sin ruta de verificación automatizada en ningún SO | F-003 | Q5.3 |
| ROOT-004 | Ambigüedad de alcance en la sección "Versionado (tags)" de AGENTS.md (no distingue release de producto vs versionado interno de `.audit/`) | F-004 | Q1.3 (agrupado con F-001) |
| ROOT-005 | Número hardcodeado sin mantenimiento | F-005 | Q4.1 |

---

## J. QUÉ SOBRA

No se identificó ningún elemento que deba eliminarse. Específicamente
se revisó y se descartó como residuo real:

- `runs/*/test-report-*.md` con rutas personales de máquina
  (`C:\Users\jlbel\...`): **REVISAR únicamente si en el futuro se
  decide purgar evidencia histórica muy antigua**, pero hoy están
  explícitamente exceptuados por `.audit/profiles/TEMPLATE.md` §Q2.2
  (evidencia de troubleshooting legítima, contextualizada, sin
  secretos, no se propaga a proyectos nuevos).
- `.opencode/node_modules/`: no es residuo del template — no está
  trackeado en git, está correctamente ignorado (`.opencode/.gitignore`).
- Los 12 scripts de `scripts/`: todos referenciados, ninguno huérfano.

---

## K. QUÉ FALTA

### OBLIGATORIO PARA 100/100

1. Corregir F-001: hacer determinista `sync-agentic-adapters.ps1`
   respecto de la edición de PowerShell, y unificar `AGENTS.md`/
   `README.md` sobre qué intérprete usar (+0.75 en Q1.3, junto con F-004).
2. Corregir F-004: acotar la sección "Versionado (tags)" de `AGENTS.md`
   para no contradecir el tag/release existente del framework de
   auditoría (incluido en el mismo +0.75 de Q1.3).
3. Corregir F-003: dar a la suite de tests del reconciliador local un
   camino de verificación **ejecutable real** (CI `windows-latest`, o
   equivalente reproducible y verificable por un tercero — una nota de
   procedimiento manual sin ejecución asociada no es suficiente)
   (+1.00 en Q5.3).
4. Corregir F-005: actualizar o dinamizar el conteo de scripts en
   README.md (+0.75 en Q4.1).

### MEJORAS OPCIONALES

Estas NO restan puntos, NO activan Quality Gates, NO bloquean 100/100:

- **F-002:** distinguir explícitamente, dentro del run ya visiblemente
  fallido del guard de `develop`, "violación descartada" de
  "verificación inconclusa" (por ejemplo `violation=check-failed`), con
  un incidente auditable dedicado a ese segundo caso. El guard ya
  cumple Q8.3 sin esto (nunca aparenta éxito ante un fallo); esto
  mejora el diagnóstico, no corrige un incumplimiento.
- Agregar `permissions: contents: read` explícito a `.github/workflows/ci.yml`
  por defensa en profundidad, aunque el comportamiento efectivo ya es
  seguro (`default_workflow_permissions: read` verificado en vivo).
- Pinning por SHA completo (en vez de tag de versión mayor) para
  `actions/checkout` y `actions/setup-python`.
- Documentar explícitamente en `AGENTS.md` el orden de preferencia
  `pwsh` vs `powershell.exe` para cada script individual, no solo a
  nivel de sección general.

---

## L. NO VERIFICADO

| Elemento | Motivo | Impacto en puntuación | Cómo verificarlo después |
| -------- | ------ | ---------------------- | -------------------------- |
| 7 tests de `test_local_reconciler_scripts.py` pasando en Windows real | CI los salta por diseño (Linux); el entorno de esta auditoría golpeó la limitación de EDR/antivirus ya documentada por el propio proyecto | -1.00 en Q5.3 (F-003) | Ejecutar en una máquina Windows sin EDR agresivo, o agregar CI `windows-latest` opcional |
| Configuración de GitHub Pages (Settings → Pages → Source) | No verificable sin acceder a la UI de Settings; fuera del alcance de una auditoría de solo lectura vía API/CLI en este momento | Ninguno (no exigible todavía: `docs.yml` solo se activa tras la primera release a `main`, que no ha ocurrido) | `gh api repos/{owner}/{repo}/pages` una vez configurado, o verificación manual en Settings |
| Comportamiento del cierre automático post-merge (`post-merge-close-feature.yml`) en un merge real durante esta sesión | No se forzó un merge real para no violar la prohibición de modificar el proyecto durante la auditoría | Ninguno (evidencia indirecta suficiente: ROADMAP.md coherente en sus 6 items `[x]`, tests dedicados pasando en CI) | Observar el próximo merge real de una feature/milestone |

---

## M. QUALITY GATES

```text
G1 BLOCKER: PASS (sin hallazgos BLOCKER)
G2 CRITICAL: PASS (sin hallazgos CRITICAL; el único MAJOR (F-001) no activa este gate)
G3 VERIFICACIÓN ESENCIAL: PASS (CI principal verde en el commit exacto;
   suite principal de tests verificada en 180/190 vía CI oficial sin
   fallos; mkdocs build --strict exitoso; ningún mecanismo esencial
   falló durante la auditoría)
```

Ningún Quality Gate se activa. El score final es igual al score bruto.

---

## N. CAMINO MATEMÁTICO A 100

```text
Score actual: 97.50

F-001 + F-004 (Q1.3) → +0.75
F-005 (Q4.1)         → +0.75
F-003 (Q5.3)         → +1.00

Score bruto esperado tras remediación: 100.00
```

F-002 no aparece en este camino: es `SUGGESTION`, 0 puntos perdidos, no
forma parte del camino obligatorio a 100 (`AUDIT_RULES.md` §62,
`QUALITY_SCORE.md` §20).

Verificación de cierre:

```text
puntos obtenidos (97.50)
+
puntos recuperables obligatorios (0.75 + 0.75 + 1.00 = 2.50)
=
puntos aplicables (100.00)
```

Cierra exactamente. Sin criterios `N/A`, por lo que no aplica
normalización adicional.

---

## O. PLAN DE REMEDIACIÓN

| Prioridad | Hallazgo | Archivo(s) | Cambio exacto | Motivo | Riesgo | Puntos recuperables | Verificación |
| --------- | -------- | ---------- | -------------- | ------ | ------ | -------------------: | ------------- |
| 1 (MAJOR) | F-001 | `scripts/sync-agentic-adapters.ps1`, `AGENTS.md` | Normalizar formato JSON generado para objetos vacíos de forma independiente de PSEdition; unificar intérprete documentado (`pwsh`) para este script en AGENTS.md/README.md | Falso positivo reproducible en la herramienta declarada requerida | Bajo (cambio aislado al generador de JSON y a texto de documentación) | 0.75 | `-Check` exit 0 bajo `powershell.exe` y `pwsh` sobre los mismos archivos |
| 2 (MINOR) | F-003 | `.github/workflows/` (nuevo job) o mecanismo equivalente | Job CI ejecutable real (preferentemente `windows-latest`, no bloqueante) para `test_local_reconciler_scripts.py`; una nota de procedimiento manual sin ejecución asociada NO cierra este hallazgo | Sin entorno de verificación ejecutable disponible para el 3.7% de la suite | Bajo | 1.00 | Run de CI real (ideal `windows-latest`) mostrando los 7 tests pasando |
| 3 (MINOR) | F-004 | `AGENTS.md` | Acotar "no hay ningún tag" a "de release del producto" | Contradicción literal con tag/release existente del framework de auditoría | Muy bajo (solo texto) | (incluido en F-001) | Relectura confirma coherencia |
| 3 (MINOR) | F-005 | `README.md` | Corregir "14" → "12" o dinamizar el conteo | Dato desactualizado en el punto de entrada del proyecto | Muy bajo (solo texto) | 0.75 | Conteo real coincide con README |
| — (`SUGGESTION`) | F-002 | `.github/workflows/guard-develop-branch.yml` | Introducir estado explícito `check-failed` cuando la llamada a `gh api` no complete, con incidente auditable dedicado | Mejora de observabilidad sobre un control que ya falla de forma segura (no puntuable, ver Sección K) | Bajo (aditivo) | 0 (no forma parte del camino a 100) | Test simulando fallo de `gh api` → incidente creado con estado explícito |

---

## P. SEGUNDA PASADA DE 100

```text
N/A — el score provisional de esta auditoría es 97.50/100, no 100/100.
La segunda pasada obligatoria de AUDIT_RULES.md §94 y AUDIT_PROMPT.md
§36 solo aplica cuando el resultado provisional es 100/100. No aplica
aquí.
```

No obstante, y en el espíritu de la instrucción de refutar activamente
antes de cerrar, se realizó una revisión dirigida adicional buscando
específicamente: TODO/FIXME críticos (ninguno encontrado con impacto
real), tests cosméticos (no encontrados: los tests de contrato y de
comportamiento de workflows ejercitan lógica real, no solo existencia de
archivos), configuraciones no verificadas asumidas como verificadas
(ninguna: todo lo marcado VERIFICADO tiene comando/log asociado en la
Sección G), y dependencias ocultas (ninguna encontrada más allá de
`pytest`/`jsonschema`, ambas declaradas). Estos hallazgos negativos
respaldan la Confianza ALTA declarada, no reemplazan la ausencia de
segunda pasada formal (que no corresponde a un resultado <100).

---

## Q. CERTIFICACIÓN FINAL

> ¿Puede este repositorio considerarse actualmente un TEMPLATE
> PROFESIONAL DE REFERENCIA?

**NO, todavía no en el sentido estricto de `TEMPLATE DE REFERENCIA
100/100`** — queda 1 hallazgo MAJOR (F-001) y 3 MINOR (F-003, F-004,
F-005) puntuables, reales, reproducibles y con camino de corrección
concreto y de bajo riesgo, más 1 hallazgo adicional (F-002) clasificado
`SUGGESTION` que no bloquea 100/100 pero vale la pena resolver por
observabilidad. Sí puede considerarse un template **sólido y utilizable
en su estado actual** (score 97.50/100, sin BLOCKER ni CRITICAL, sin
Quality Gate activado, circuito agéntico funcionando de punta a punta
con evidencia real verificada en el propio commit auditado —incluido el
guard de `develop`, que falla de forma segura y visible ante errores
inesperados—), cuyas deficiencias son puntuales, acotadas, y ninguna de
ellas bloquea el uso del circuito descrito en `AGENTS.md`.

---

## Verificaciones ejecutadas (resumen)

Ver Sección G (Ledger de verificación) para el detalle completo con
comandos, resultados y evidencia persistida en
`.audit/evidence/2026-08-31-24789d6-reauditoria-final-v1-1/`.

## Estado del guard de `develop`

Extensamente testeado (18 tests dedicados en
`tests/test_guard_develop_branch_workflow.py`, todos pasando en CI),
con evidencia real de ejecución correcta en el propio commit auditado
(run `33420464281`, no-op correcto sobre un merge legítimo) y con un
incidente histórico real cuya causa puntual ya está corregida. Ese
incidente histórico (fallo de `gh api`) confirma además que el guard
falla de forma segura y visible ante un error inesperado (`exit code 1`,
job en rojo), sin aparentar éxito en ningún momento — F-002 (`SUGGESTION`)
solo señala una mejora de diagnóstico posible dentro de ese fallo ya
visible, no una falla de seguridad del control.

## Estado de `main`/release/`docs.yml`

Consistente con el "estado inicial del template" documentado en
`AGENTS.md`: `main` no existe todavía (confirmado: `git branch -a`
remoto no lista `main`), no hay tags de release del producto
(`vX.Y.Z`), y `docs.yml` no tiene ningún evento que lo dispare todavía
porque solo se activa con push a `main` — comportamiento correcto y
esperado, no un defecto, per la excepción explícita de
`AUDIT_RULES.md` §45 ("Versionado y releases no ejercidos... Si el
release está declarado únicamente como capacidad futura, prospectiva o
de ROADMAP, su falta de ejecución no debe penalizar la versión
actual"). La única salvedad real en esta área es F-004 (el tag interno
del framework de auditoría, no del producto).

## Consistencia metodológica

```text
[x] Toda pérdida de puntos tiene causa identificada
[x] Todo hallazgo puntuable está asociado a un criterio materialmente relacionado
[x] Ninguna SUGGESTION resta puntos
[x] Ninguna SUGGESTION bloquea 100/100
[x] Todos los puntos perdidos aparecen en el camino obligatorio a 100
[x] El camino proyectado alcanza exactamente los puntos aplicables (100.00)
[x] Los N/A están justificados (no se usó ningún N/A en esta auditoría)
[x] Los Quality Gates se derivan de hallazgos reales (ninguno se activó)
```

**Consistencia metodológica: PASS**

---

## Comparación histórica (solo al final, no usada como entrada)

Las auditorías previas registradas en `SCORE_HISTORY.md` son:

```text
2026-08-29  05ce680  BASELINE PROVISIONAL                    bruto 80.87  final 79.00
2026-08-30  34773af  BASELINE                                 bruto 92.75  final 79.00
2026-08-31  7964013  REAUDITORÍA PROVISIONAL — REQUIERE REVISIÓN  bruto 95.50  final 95.50
```

Ninguna auditoría anterior certificó 100/100; la más reciente
(`7964013`) cerró en 95.50/100, "APTO CON CORRECCIONES", explícitamente
marcada "REQUIERE REVISIÓN". Esta reauditoría independiente, ejecutada
desde cero sin usar esos resultados como entrada, encuentra **97.50/100**
(tras la corrección metodológica post-emisión documentada en la ADENDA
al inicio de este informe) sobre un commit posterior (`24789d6`, que
incluye además
`da1f60d` "Documentar ciclo de vida de main y releases", posterior a
`7964013`). Los 5 hallazgos de esta auditoría (F-001 a F-005) no
coinciden con ninguno de los hallazgos abiertos que dejó pendientes
`7964013` (los de esa auditoría ya fueron cerrados o superados por
commits posteriores, a juzgar por el estado actual verificado). Son
hallazgos nuevos para este historial, no regresiones: la evidencia
indica que existían ya antes de `7964013` (los scripts/documentos donde
se originan —`AGENTS.md`, `README.md`,
`scripts/sync-agentic-adapters.ps1`, `guard-develop-branch.yml`— no
tienen cambios sustanciales en las secciones afectadas entre `7964013` y
`24789d6`), simplemente no fueron cubiertos por la verificación cruzada
de ediciones de PowerShell, la lectura del log completo del incidente
histórico del guard, ni el contraste literal de `git tag -l` contra el
texto de la sección "Versionado (tags)" de `AGENTS.md`.

Esta comparación es contexto histórico, no evidencia para el resultado
de esta auditoría (`AUDIT_RULES.md` §67).

---

## RESULTADO FINAL

1. **Commit exacto auditado:** `24789d62e44f3eec2d44622f709ff5c024f70369` (24789d6)
2. **Score bruto:** 97.50/100
3. **Score final:** 97.50/100
4. **Puntos aplicables:** 100.00 (sin N/A)
5. **Confianza:** ALTA
6. **Quality Gates:** G1 PASS, G2 PASS, G3 PASS — ninguno activado
7. **Hallazgos puntuables:** F-001 (MAJOR, -0.75 Q1.3), F-003 (MINOR,
   -1.00 Q5.3), F-004 (MINOR, incluido en F-001), F-005 (MINOR, -0.75
   Q4.1)
8. **SUGGESTION separadas:** F-002 (observabilidad del guard de
   `develop` ante fallo de API — no puntuable, el control ya falla de
   forma segura y visible); permisos explícitos de defensa en
   profundidad en `ci.yml`; pinning por SHA completo de actions;
   documentar preferencia de intérprete por script individual
9. **Verificaciones ejecutadas:** 24 (ver Sección G)
10. **Estado del guard de `develop`:** funcional y extensamente
    testeado; falla de forma segura y visible ante un error inesperado
    de la API de GitHub (sin falso éxito); F-002 (`SUGGESTION`) señala
    una mejora de observabilidad posible, no un defecto de seguridad
11. **Estado de `main`/release/`docs.yml`:** consistente con el estado
    inicial documentado del template; sin defectos (salvo F-004, de
    alcance distinto)
12. **Camino matemático a 100:** cierra exactamente (97.50 + 2.50 = 100.00)
13. **Resultado de segunda pasada:** N/A (el provisional no fue 100/100)
14. **Comparación histórica:** ver sección dedicada arriba
15. **Consistencia metodológica:** PASS
16. **Recomendación final: APTO CON CORRECCIONES**

No se remedió ningún hallazgo durante esta auditoría. No se hizo commit
de cambios al proyecto (solo se agregaron artefactos nuevos en
`.audit/evidence/` y `.audit/reports/`). No se hizo push. No se creó
`main`. No se creó ningún release.
