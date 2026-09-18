# AUDIT-2026-08-30-34773af-baseline-v1-1

**Auditoría piloto — candidata a BASELINE oficial — Framework v1.1**

Evidencia reproducible: `.audit/evidence/2026-08-30-34773af-baseline-v1-1/`

---

## ADENDA DE CORRECCIÓN METODOLÓGICA (post-emisión, mismo commit `34773af`)

Este informe fue revisado tras su emisión inicial por seis observaciones
metodológicas concretas recibidas sobre el borrador original. Ninguna
implicó volver a inspeccionar código, documentación funcional,
configuración, workflows, tests o agentes — solo corregir la
interpretación del framework y, en un caso, ejecutar una verificación
adicional que era razonablemente posible y no se había realizado.
Cambios aplicados:

1. **Q6.5 reclasificado de N/A a criterio aplicable y puntuado.** El
   perfil TEMPLATE declara explícitamente que "documentación compilada"
   hace aplicable Q6.5, y el repositorio sí produce ese artefacto
   (`mkdocs.yml` + `docs.yml`). Se ejecutó la verificación que antes se
   había dejado como "no verificado por limitación de entorno" —
   instalar `mkdocs-material` y correr `mkdocs build --strict` era
   razonable y seguro — con resultado real: `exit 0`. Ver
   `12-mkdocs-build-verification.txt` y hallazgo **F-007** (nuevo).
2. **Recalculo completo** de puntos aplicables, obtenidos, score bruto
   normalizado, hallazgos y camino a 100 (secciones E, F, N).
3. **Sección Q corregida.** F-004 es el único hallazgo que activa el
   Quality Gate G2, pero no es el único que impide 100/100 mientras
   F-001, F-002, F-003, F-005 y F-007 sigan abiertos.
4. **Corrección propuesta para F-004 endurecida.** Se elimina la opción
   de "notificación posterior" como suficiente para recuperación
   completa de Q6.2; se exige un control que efectivamente prevenga o
   revierta, no solo detecte y avise.
5. **F-006 reclasificado de MINOR puntuable a `SUGGESTION`.** No hay
   riesgo objetivo demostrado no cubierto por otro mecanismo (Actions
   oficiales de primera parte, repo privado de un solo mantenedor, sin
   contribuciones externas no confiables, `pull_request_target` ya usa
   el patrón seguro de checkout de rama confiable). Convertirlo en
   requisito habría sido exactamente el "requisito por checklist" que
   `AUDIT_RULES.md` prohíbe.
6. **Validación de consistencia matemática repetida** con los números
   corregidos (sección N): `puntos obtenidos + puntos recuperables
   obligatorios = puntos aplicables` se cumple de forma exacta.

**Resultado de la corrección:** consistencia metodológica **PASS**.
Score bruto corregido: **92.25/100** (antes 92.09, sobre una base
aplicable distinta). Score final: **79/100** (sin cambio — el mismo
Quality Gate G2 seguía siendo el más restrictivo antes y después de la
corrección).

## ADENDA DE CORRECCIÓN METODOLÓGICA — SEGUNDA RONDA (mismo commit `34773af`)

Tras la primera ronda de corrección quedó una última inconsistencia:
**F-007 penalizaba Q6.5 por la falta de ejecución histórica de
`docs.yml`, pese a que la evidencia directamente reunida
(`mkdocs build --strict` → `exit 0`) ya demuestra que el artefacto de
"documentación compilada" se construye correctamente y de forma
reproducible.** Q6.5 en `QUALITY_SCORE.md` se llama textualmente
"Build y artefactos reproducibles" — pregunta por la reproducibilidad
del build, no por si el pipeline de despliegue ya se ejecutó
alguna vez en producción. Penalizar la ausencia de ejecución de
`docs.yml` sobre `main` es exactamente el mismo error que ya se evitó al
puntuar Q6.4 (versionado): `AUDIT_RULES.md` §45 y `QUALITY_SCORE.md`
prohíben penalizar automáticamente una capacidad declarada como
futura/prospectiva por el simple hecho de no haber sido ejercida
todavía, y el release a `main` sigue siendo, en este repositorio, una
decisión humana pendiente, no una obligación actual.

Revisado explícitamente: no existe ningún otro defecto objetivo de
reproducibilidad del build en sí (la ejecución fue limpia, determinista,
sin advertencias promovidas a error por `--strict`, y usa exactamente el
comando oficial de `docs.yml`). Por lo tanto:

1. **F-007 se elimina como hallazgo puntuable.** La ausencia de
   ejecución histórica de `docs.yml` sobre `main` pasa a ser
   NO VERIFICADO CONTEXTUAL (sección L): no resta puntos, no activa
   ningún Quality Gate y no forma parte del camino obligatorio a 100.
2. **Q6.5 = COMPLETO = 2.00/2.00**, respaldado por evidencia ejecutable
   real (V-025).
3. Recalculado el informe completo (secciones B, C, E, F, G, H, I, K, L,
   M, N, O, Q) con los nuevos números.

**Resultado de esta segunda corrección:**

```text
Puntos aplicables:              100.00
Puntos obtenidos:               92.75
Score bruto:                    92.75/100
Puntos recuperables obligatorios: 7.25
Validación: 92.75 + 7.25 = 100.00  ✓ exacta
Score final:                    79/100 (Gate G2, F-004 CRITICAL, sin cambio)
Consistencia metodológica:      PASS
```

Con esta segunda corrección, y sin ninguna inconsistencia pendiente
identificada, esta auditoría queda confirmada como **BASELINE oficial**
del framework v1.1 sobre el commit `34773af`.

---

## A. IDENTIFICACIÓN

```text
Repositorio: template (jlbellonGmail/template)
Ruta: D:\proyectos\template
Branch: chore/auditoria-baseline-v1.1
Commit: 34773af3b03d0bd84b0c88f621353a7dfd6a83ed
Tag: N/A (no existen tags en el repositorio)
Fecha: 2026-08-30
Worktree: LIMPIO (git status: "nothing to commit, working tree clean")
Perfil: TEMPLATE v1.1
QUALITY_SCORE: v1.1
AUDIT_RULES: v1.1
Nivel de confianza: ALTA
```

Confirmación explícita solicitada por el piloto: el commit auditado es
exactamente `34773af3b03d0bd84b0c88f621353a7dfd6a83ed` (verificado con
`git rev-parse HEAD` antes de cualquier otra operación — ver
`00-identificacion.txt`).

---

## B. VEREDICTO EJECUTIVO

```text
Score bruto: 92.75/100 (normalizado sobre 100 puntos aplicables; sin N/A)
Quality Gate aplicado: G2 — CRITICAL abierto (F-004)
Score final: 79/100
Confianza: ALTA
Estado: APTO CON CORRECCIONES
Consistencia metodológica: PASS
```

**Resumen ejecutivo:** el repositorio implementa de forma sólida y
verificable el circuito agéntico que declara: 5 agentes con
responsabilidades y permisos bien delimitados, fuente única de verdad en
`.agentic/` con adaptadores generados y sin drift (verificado en vivo),
suite de 171 tests que pasa en verde en la ejecución oficial de CI sobre
el commit exacto auditado, y una cadena de trazabilidad completa
(spec→plan→tasks→auditoría→decisión→test-report→code-review) evidenciada
con una feature real. La arquitectura es coherente, sin duplicación
manual peligrosa, sin scripts huérfanos y sin secretos expuestos.
El mecanismo de "documentación compilada" (`mkdocs build --strict`) se
verificó ejecutándolo realmente: `exit 0`.

Sin embargo, existe un hallazgo **CRITICAL** que activa un Quality Gate:
no existe ningún control técnico — ni nativo de GitHub (bloqueado por
límite de plan, verificado en vivo) ni alternativo (ningún workflow
rechaza o revierte pushes directos) — que impida escribir directamente
en `develop` sin pasar por PR. Esto ya ocurrió en la práctica (~15
commits directos documentados por el propio repo en agosto de 2026) y
hoy se sostiene únicamente por disciplina humana, lo cual el propio
perfil TEMPLATE excluye explícitamente como "enforcement técnico
completo". Existen además dos defectos MAJOR reales (un residuo
documental y un quality gate de CI con `continue-on-error`), y dos
defectos MINOR adicionales (discrepancia numérica entre el README y la
suite real de tests, y modelo de evolución del template no declarado
explícitamente). El mecanismo de "documentación compilada" (Q6.5) se
verificó ejecutándolo realmente (`mkdocs build --strict`, exit 0) y
obtiene puntuación completa: la ausencia de una ejecución histórica del
pipeline de despliegue sobre `main` no lo penaliza, porque el release a
`main` sigue siendo una decisión humana declarada como futura, no una
obligación actual — el mismo razonamiento ya aplicado a Q6.4.

Ninguno de estos cinco hallazgos puntuables (F-001, F-002, F-003, F-004,
F-005) es un `SUGGESTION`: todos restan puntos y forman parte del camino
obligatorio a 100/100, que se reconstruye exactamente en la sección N.
**Cerrar solo F-004 no alcanza para llegar a 100/100** — libera el
Quality Gate G2 (el score final sube a 95.00), pero los otros cuatro
hallazgos seguirían restando puntos hasta que también se cierren (ver
sección Q). Dos observaciones adicionales se evaluaron y se
reclasificaron como `SUGGESTION`/contextuales, sin puntos: el pinning de
GitHub Actions a SHA (sin riesgo objetivo demostrado en este contexto) y
la falta de ejecución histórica del pipeline completo de `docs.yml`
(capacidad prospectiva, no penalizable) — ver sección K y L.

---

## C. ALCANCE Y LIMITACIONES

**Inspeccionado:** estructura completa del repositorio; `README.md`,
`AGENTS.md`, `ROADMAP.md`, `CLAUDE.md`; todo `docs/` (técnica, usuario,
producto); `.agentic/` (roles, agents.json, models.json, mcp.json,
schemas); `.claude/`, `.codex/`, `.opencode/` (adaptadores generados);
`scripts/*.ps1` (12 scripts); `tests/*.py` (16 archivos, 171 tests);
`.github/workflows/*.yml` (4 workflows); `.gitignore`; `.mcp.json`;
`opencode.json`; historial Git completo (104 commits); `runs/` (6
features completas con su cadena de artefactos).

**Ejecutado:**
- `python -m pytest` (suite completa y con exclusión selectiva del
  archivo con limitación de entorno conocida — ver abajo).
- `python -m pytest --collect-only -q` (recuento real de tests: 171).
- `pwsh -File ./scripts/sync-agentic-adapters.ps1 -Check` (verificación
  en vivo de drift entre `.agentic/` y sus adaptadores generados).
- Validación real de `.agentic/agents.json` y `.agentic/models.json`
  contra sus JSON Schemas (`jsonschema.validate`).
- `gh api repos/.../branches/develop/protection` (verificación en vivo
  de branch protection real, no documentada).
- `gh api repos/.../actions/permissions/workflow` (verificación en vivo
  del permiso por defecto de `GITHUB_TOKEN`).
- `gh run list` / `gh run view --json jobs` sobre el run de CI
  correspondiente exactamente al commit `34773af` (headSha verificado
  igual al HEAD auditado).
- Búsqueda de secretos, hardcodes, residuos de origen, TODO/FIXME reales
  (excluyendo falsos positivos de la palabra española "todo").
- Verificación del check B3 propio del repo (scripts huérfanos) y B1
  (consistencia índices de documentación ↔ `ROADMAP.md`).
- `pip install mkdocs-material && mkdocs build --strict` (el comando
  exacto declarado en `docs.yml`), ejecutado hacia un directorio de
  destino temporal fuera del repositorio: `exit 0`, sin errores. Ver
  `12-mkdocs-build-verification.txt`.

**No pudo verificarse (limitación de entorno del auditor, no defecto del
repo):**
- `tests/test_local_reconciler_scripts.py` (7 de 171 tests) se cuelga en
  esta máquina Windows lanzando procesos `python.exe`/PowerShell
  ocultos. Se reprodujo exactamente la causa raíz que el propio repo ya
  documenta en `docs/tecnica/circuito-agentico.md`
  ("Troubleshooting: EDR/antivirus agresivo bloquea el reconciliador
  local"). No es un defecto nuevo. Se resolvió mediante evidencia de
  mayor jerarquía: el mismo commit `34773af` fue ejecutado íntegramente
  en CI (`ubuntu-latest`, sin restricción de EDR) con resultado
  `success` en ambos jobs — ver `02-ci-verification.txt`.
- `mkdocs gh-deploy --force` (el paso de despliegue real de `docs.yml`,
  distinto del paso de build): deliberadamente NO ejecutado, porque
  publicaría de verdad una rama `gh-pages` — una operación de
  despliegue real prohibida durante la auditoría (`AUDIT_RULES.md`
  §17). NO VERIFICADO por diseño de la auditoría, no por limitación de
  entorno. Sin impacto en la puntuación de Q6.5 (ver sección L):
  el paso de *build*, que es lo que Q6.5 evalúa ("reproducibilidad" del
  artefacto), sí se verificó con éxito real.
- Ejecución real histórica de `docs.yml` en su contexto oficial (evento
  `push` a `main`): no puede haber ocurrido porque `main` no existe en
  el remoto (V-013). Sin impacto en la puntuación: mismo razonamiento
  prospectivo ya aplicado a Q6.4 (el release a `main` es una decisión
  humana futura, no una obligación actual — ver sección L).
- Configuración remota adicional de GitHub no cubierta por los dos
  endpoints consultados (p. ej. secret scanning, Dependabot alerts):
  NO VERIFICADO, sin impacto material dado el perfil de riesgo (2
  dependencias Python de bajo riesgo, sin superficie de secretos).

**Accesos disponibles:** GitHub CLI (`gh`) autenticado con acceso de
lectura al repositorio real y a la API de branch protection/permissions;
sin acceso a configuración de organización más allá de lo expuesto por
esos endpoints.

---

## D. CONTRATO DETECTADO

| ID | Capacidad/Requisito | Clasificación | Fuente | Estado |
| -- | -------------------- | -------------- | ------ | ------ |
| C-01 | Circuito agéntico de 5 roles (analyst→reviewer→builder→qa→code-reviewer) con único HITL | OBLIGATORIO | `AGENTS.md` | VERIFICADO |
| C-02 | Fuente única `.agentic/` que genera adaptadores Claude/Codex/OpenCode | OBLIGATORIO | `AGENTS.md`, `scripts/sync-agentic-adapters.ps1` | VERIFICADO (sin drift) |
| C-03 | Contrato mínimo de artefactos por feature (`spec.md`…`decision.md`) validado por script común | OBLIGATORIO | `AGENTS.md`, `scripts/feature-contract.ps1` | VERIFICADO (ejemplo real inspeccionado) |
| C-04 | CI con job `circuit-tests` obligatorio y `product-tests` placeholder también obligatorio | OBLIGATORIO | `AGENTS.md`, `.github/workflows/ci.yml` | VERIFICADO (ambos jobs, verde en HEAD) |
| C-05 | Nunca commitear directo a `develop`/`main` salvo excepciones documentadas | OBLIGATORIO (declarado como regla dura) | `AGENTS.md` | INCUMPLIDO TÉCNICAMENTE — solo disciplina humana, sin enforcement (ver F-004) |
| C-06 | Cierre automático post-merge de `ROADMAP.md` vía GitHub Actions | OBLIGATORIO | `AGENTS.md`, `.github/workflows/post-merge-close-feature.yml` | VERIFICADO (diseño; no se forzó un merge real durante la auditoría por ser operación no de solo lectura) |
| C-07 | Modo Milestone como variante del circuito Feature | OPCIONAL | `AGENTS.md`, `scripts/workunit-lib.ps1` | VERIFICADO (tests dedicados en verde) |
| C-08 | Sin stack de producto propio; `product-tests` es placeholder deliberado | OBLIGATORIO (declarado) | `AGENTS.md`, `ci.yml` | VERIFICADO (coherente, no hay código de producto) |
| C-09 | Versionado SemVer + tags al hacer release a `main` | FUTURO / PROSPECTIVO | `AGENTS.md` sección "Versionado" | NO EJERCIDO — coherente con estado declarado (no penalizable, ver sección L) |
| C-10 | Contexto de producto persistente en `docs/producto/contexto-producto.md` | RECOMENDADO | `AGENTS.md` | VERIFICADO (poblado, 140 líneas) |
| C-11 | Documentación técnica/usuario por feature con enlaces exactos en índices | OBLIGATORIO | `AGENTS.md` | VERIFICADO (6/6 features, 1:1) |
| C-12 | Windows + PowerShell como plataforma primaria del motor de scripts (decisión explícita) | OBLIGATORIO (alcance declarado) | `docs/tecnica/arquitectura.md` | VERIFICADO (documentado, coherente, con excepción y troubleshooting declarados) |

---

## E. MATRIZ DE PUNTUACIÓN

| Área                          |  Máximo | Aplicable | Obtenido | Estado |
| ----------------------------- | ------: | --------: | -------: | ------ |
| Q1 Conformidad                |      12 |        12 |    11.25 | MENOR  |
| Q2 Reutilización              |      12 |        12 |    10.50 | MENOR  |
| Q3 Arquitectura               |      12 |        12 |    12.00 | COMPLETO |
| Q4 Documentación/DX           |      12 |        12 |    11.25 | MENOR  |
| Q5 Calidad/Tests              |      16 |        16 |    14.50 | MENOR  |
| Q6 Git/CI/CD/Release          |      16 |        16 |    13.25 | PARCIAL (gate) |
| Q7 Seguridad                  |      12 |        12 |    12.00 | COMPLETO |
| Q8 Automatización/Gobernanza  |       8 |         8 |     8.00 | COMPLETO |
| **TOTAL (aplicable = 100)**   | **100** |   **100** |**92.75** | — |

```text
Puntos obtenidos:              92.75
Puntos aplicables:             100.00  (sin criterios N/A)
Score bruto normalizado:       92.75 / 100 × 100 = 92.75
Quality Gate:                  G2 (CRITICAL abierto, F-004) → máximo 79
Score final:                   79.00
```

**Nota de corrección (dos rondas aplicadas sobre este mismo informe):**

1. Primera ronda: en la emisión original, Q6.5 se había marcado
   incorrectamente `N/A`. El perfil TEMPLATE incluye explícitamente
   "documentación compilada" como artefacto aplicable, y el repositorio
   sí lo produce (`mkdocs.yml` + `docs.yml`). Esto subió los puntos
   aplicables de 98 a 100.
2. Segunda ronda: tras verificar realmente el build (`mkdocs build
   --strict` → `exit 0`, evidencia V-025), se corrigió una penalización
   indebida sobre Q6.5 (antes MENOR/1.50 por un hallazgo F-007 que
   penalizaba la falta de ejecución histórica del *pipeline completo*
   de `docs.yml`, no del build en sí). Q6.5 pregunta por
   "reproducibilidad del build" — ya demostrada — no por si el
   despliegue ya ocurrió en producción; y el release a `main` sigue
   siendo, igual que en Q6.4, una capacidad prospectiva no penalizable
   por falta de ejercicio. Q6.5 pasa a **COMPLETO = 2.00/2.00**. Esto
   sube los puntos obtenidos de 92.25 a 92.75.

El score final permanece en 79 en ambas rondas porque el mismo Quality
Gate G2 (F-004, CRITICAL) sigue siendo más restrictivo que el score
bruto en los tres cálculos (92.09 → 92.25 → 92.75, todos > 79).

---

## F. DETALLE POR SUBCRITERIO

| ID | Criterio | Máx. | Nivel | Obtenido | Evidencia | Hallazgo | Justificación |
| -- | -------- | ---: | ----- | -------: | --------- | -------- | ------------- |
| Q1.1 | Propósito y alcance | 3 | COMPLETO | 3.00 | `README.md`, `AGENTS.md` §"Proyecto", `ROADMAP.md` §"Propósito del producto" | — | Propósito, alcance, límites (sin stack propio) y precondiciones consistentes en las tres fuentes. |
| Q1.2 | Capacidades prometidas presentes | 3 | COMPLETO | 3.00 | CI verde en HEAD, adapters sin drift, docs presentes | — | Todo lo prometido (CI, tests, agentes, docs) existe realmente. |
| Q1.3 | Coherencia entre fuentes | 3 | MENOR | 2.25 | `05-readme-test-count-mismatch.txt`, `06-informe-ejecutivo-residue.txt` | F-003, F-001 | README dice "196+ tests" (real: 171); `informe-ejecutivo-2026.md` afirma "194 tests" y "100% completo, no falta nada". Contradicciones acotadas, no estructurales. |
| Q1.4 | Ausencia de requisitos obligatorios incompletos | 3 | COMPLETO | 3.00 | Contrato de artefactos verificado con ejemplo real | — | No hay capacidades declaradas como terminadas que estén realmente rotas o pendientes. |
| Q2.1 | Inicialización reproducible | 3 | COMPLETO | 3.00 | Quick-start ejecutado: sync-adapters → pytest → estructura operativa | — | Camino de adopción reproducible sin conocimiento oculto. |
| Q2.2 | Ausencia de residuos del origen | 3 | PARCIAL | 1.50 | `06-informe-ejecutivo-residue.txt` | F-001 | `docs/producto/informe-ejecutivo-2026.md` es una transcripción de sesión de IA cortada a mitad de un `<tool_call>`, sin ninguna referencia desde los índices de documentación ni `mkdocs.yml`. Residuo real, acotado (no propaga secretos ni rompe funcionamiento). |
| Q2.3 | Configuración y personalización claras | 3 | COMPLETO | 3.00 | `README.md` placeholders genéricos, `AGENTS.md` reglas de dominio | — | Claro qué debe cambiar el consumidor (stack en `arquitectura.md`) y qué no se toca. |
| Q2.4 | Portabilidad y extensibilidad | 3 | COMPLETO | 3.00 | `docs/tecnica/arquitectura.md` "Decisión: motor de scripts en PowerShell" | — | Dependencia de plataforma explícita, documentada, coherente con el alcance declarado, con excepción y troubleshooting propios (caso ejemplo del propio perfil TEMPLATE §8). |
| Q3.1 | Estructura coherente | 3 | COMPLETO | 3.00 | Inventario completo | — | Separación clara y navegable: `.agentic/`, `scripts/`, `tests/`, `docs/{tecnica,usuario,producto}`, `runs/`. |
| Q3.2 | Separación de responsabilidades | 3 | COMPLETO | 3.00 | `scripts/workunit-lib.ps1` compartido, `.agentic/roles/*.md` fuente única | — | Lógica común centralizada, no mezclada con configuración específica de cada agente/herramienta. |
| Q3.3 | Simplicidad y duplicación | 3 | COMPLETO | 3.00 | `11-orphan-scripts-and-traceability.txt` (B3: sin huérfanos), `03-adapters-check.txt` (sin drift) | (causa compartida con F-001, no re-penalizado) | Sin scripts muertos, sin TODO/FIXME reales, sin duplicación manual divergente entre adaptadores. |
| Q3.4 | Evolución | 3 | COMPLETO | 3.00 | `.agentic/` versionado, `workunit-lib.ps1` reutilizado por Feature y Milestone | — | Puede extenderse sin multiplicar copias manuales de la misma regla. |
| Q4.1 | README funcional | 3 | MENOR | 2.25 | `05-readme-test-count-mismatch.txt` | F-003 | README claro y bien estructurado, pero con una afirmación numérica incorrecta ("196+ tests" vs. 171 reales). |
| Q4.2 | Instalación y bootstrap | 3 | COMPLETO | 3.00 | Quick-start de 3 pasos verificado | — | Ruta única y reproducible, sin divergencia entre README/CI/autor. |
| Q4.3 | Operaciones habituales | 2 | COMPLETO | 2.00 | `AGENTS.md` (circuito, ready-for-pr, wait-pr-ci, etc.) | — | Inicializar, validar, versionar y liberar están documentados. |
| Q4.4 | Convenciones de contribución | 2 | COMPLETO | 2.00 | `AGENTS.md` completo (Git, CI/CD, roadmap, dominio) | — | Reglas de contribución exhaustivas y sin ambigüedad. |
| Q4.5 | Ejemplos y troubleshooting | 2 | COMPLETO | 2.00 | `docs/tecnica/circuito-agentico.md` §Troubleshooting (EDR), README §"¿Problemas?" | — | Troubleshooting concreto y verificado como exacto durante esta misma auditoría. |
| Q5.1 | Controles automáticos | 3 | COMPLETO | 3.00 | pytest + `jsonschema` real + drift-check existen y corren | — | Controles proporcionales al tipo de proyecto (script/config, no código de producto). |
| Q5.2 | Estrategia de pruebas | 3 | COMPLETO | 3.00 | 171 tests: contrato, workunit, milestone, router de modelos, e2e, schemas | — | Pruebas de contrato/estructura, proporcionales y de alto valor para un template. |
| Q5.3 | Tests ejecutables y pasando | 4 | COMPLETO | 4.00 | `01-pytest-local.txt`, `02-ci-verification.txt` | — | Verificado por dos vías independientes: 164/164 en local (excluyendo el archivo con limitación de entorno documentada) y ambos jobs de CI en verde exactamente sobre el commit `34773af`. |
| Q5.4 | Protección frente a regresiones | 3 | COMPLETO | 3.00 | `docs/tecnica/criterios-evaluacion-repo.md` (checks A1–E2 con historial real de hallazgos corregidos) | — | El propio repo demuestra un proceso que detectó y corrigió regresiones reales (Dockerfile roto, scripts huérfanos, timeouts, nombre de status check). |
| Q5.5 | Quality gates | 3 | PARCIAL | 1.50 | `07-ci-continue-on-error.txt` | F-002 | El único status check requerido (`circuit-tests`) incluye un paso de verificación de drift con `continue-on-error: true`: un fallo real de ese control no bloquea el merge. El gate principal (pytest) sí es duro. |
| Q6.1 | Estrategia Git | 3 | COMPLETO | 3.00 | `AGENTS.md` §Git | — | `develop`/`feature`/`milestone` coherente y documentado. |
| Q6.2 | Protección de ramas | 3 | DÉBIL | 0.75 | `04-branch-protection-and-governance.txt` | F-004 | Branch protection nativa bloqueada por plan (verificado en vivo, `403`); sin control técnico alternativo (ningún workflow rechaza/revierte push directo); incidente histórico real de ~15 commits directos ya documentado por el propio repo. |
| Q6.3 | CI reproducible | 3 | COMPLETO | 3.00 | `02-ci-verification.txt` | (causa compartida con F-002, no re-penalizado) | CI ejecuta el comando oficial (`pytest -v`), reproducible localmente, verde en el commit exacto auditado. |
| Q6.4 | Versionado y releases | 3 | COMPLETO | 3.00 | `AGENTS.md` §"Versionado (tags)" | — | Mecanismo declarado explícitamente como futuro/prospectivo (ligado a la decisión de release a `main`, que aún no existe); el commit SHA ya funciona hoy como identificador reproducible de versión (esta misma auditoría lo demuestra). No penalizable como capacidad no ejercida (regla Q6.4/AUDIT_RULES §45). |
| Q6.5 | Build y artefactos | 2 | COMPLETO | 2.00 | `12-mkdocs-build-verification.txt` (V-025) | — | Aplicable: el perfil TEMPLATE incluye "documentación compilada" explícitamente en Q6.5 ("Build y artefactos **reproducibles**"), y el repositorio la produce (`mkdocs.yml`/`docs.yml`). El build se verificó ejecutándolo realmente con el comando oficial (`mkdocs build --strict`), resultado `exit 0`, limpio y determinista — evidencia E4 directa de reproducibilidad. La ausencia de una ejecución histórica del *pipeline de despliegue* sobre `main` no penaliza este criterio: `main` no existe porque el release es una decisión humana declarada como futura (mismo razonamiento no penalizable ya aplicado a Q6.4), y Q6.5 pregunta por la reproducibilidad del build, no por si ya se desplegó en producción. |
| Q6.6 | Compatibilidad/rollback | 2 | MENOR | 1.50 | Búsqueda de "snapshot"/"actualiza template" sin declaración explícita de política | F-005 | El modelo de evolución (snapshot: clonar y divergir, sin sincronización posterior) es inferible de la mecánica del quick-start pero no está declarado explícitamente como política inequívoca. |
| Q7.1 | Gestión de secretos | 3 | COMPLETO | 3.00 | `09-secrets-search.txt` | — | Sin secretos reales; coincidencias son referencias documentales/`github.token` estándar. |
| Q7.2 | Gestión de dependencias | 2 | COMPLETO | 2.00 | `requirements-dev.txt` (2 deps, pinning mínimo `>=`) | — | Superficie mínima, dependencias oficiales de bajo riesgo; lockfile no justificado por el riesgo real. |
| Q7.3 | Seguridad de CI/CD | 2 | COMPLETO | 2.00 | `08-action-pinning.txt`, `04-branch-protection-and-governance.txt` (default_workflow_permissions=read) | — (ver F-006 histórico, reclasificado a `SUGGESTION`) | Permisos por defecto seguros (`read`, verificado en vivo) y uso correcto de `pull_request_target` (checkout de `develop` confiable, no del head de la PR). Las Actions se referencian por tag mayor (`@v4`/`@v5`, no SHA), pero son de primera parte (GitHub oficial), en un repo privado de un solo mantenedor sin contribuciones externas no confiables: no hay evidencia de un riesgo objetivo no cubierto por otro mecanismo, por lo que no se penaliza (ver F-006 en sección K, `SUGGESTION`). |
| Q7.4 | Defaults seguros | 2 | COMPLETO | 2.00 | `.gitignore` (`.env*` ignorado salvo `.env.example`), permisos por defecto `read` | — | Sin defaults inseguros detectados. |
| Q7.5 | Supply chain y cumplimiento | 3 | COMPLETO | 3.00 | Repo privado sin promesa de distribución externa | — | Ausencia de `LICENSE`/SBOM no penalizable: repo privado, sin distribución declarada, superficie de riesgo mínima. |
| Q8.1 | Fuente única de verdad | 2 | COMPLETO | 2.00 | `.agentic/` + adaptadores generados, sin drift verificado | (causa compartida con F-002, no re-penalizado) | Diseño de fuente única real y funcionando; el gate blando de su verificación ya se penalizó en Q5.5. |
| Q8.2 | Responsabilidades y límites | 2 | COMPLETO | 2.00 | `.agentic/agents.json`, `.agentic/roles/builder-agent.md` | — | Roles, permisos, HITL único y retornos permitidos explícitos y sin ambigüedad. |
| Q8.3 | Fail-safe | 2 | COMPLETO | 2.00 | `close-feature.ps1`/`complete-approved-pr.ps1`: `$ErrorActionPreference="Stop"`, `throw` en cada validación | — | Estados ambiguos/parciales se rechazan explícitamente en vez de completarse en silencio. |
| Q8.4 | Trazabilidad | 2 | COMPLETO | 2.00 | `11-orphan-scripts-and-traceability.txt` (cadena completa `runs/05-.../`) | — | Cadena requisito→spec→plan→tasks→auditoría→decisión→test→review verificada con un ejemplo real y sustancial (1364 líneas). |

---

## G. LEDGER DE VERIFICACIÓN

| ID | Verificación | Comando/Método | Resultado | Estado | Evidencia |
| -- | ------------ | --------------- | --------- | ------ | --------- |
| V-001 | Identificación del commit auditado | `git rev-parse HEAD` | `34773af3b03d0bd84b0c88f621353a7dfd6a83ed` | PASS | `00-identificacion.txt` |
| V-002 | Estado del worktree | `git status` | Limpio, nada por commitear | PASS | `00-identificacion.txt` |
| V-003 | Suite pytest local (default, sin `--basetemp`) | `python -m pytest -v` | `42 passed, 129 errors` — causa única: `PermissionError` en `%TEMP%` del entorno del auditor | NO VERIFICADO (LIMITACIÓN DE ENTORNO) | — |
| V-004 | Suite pytest local con `--basetemp` propio, excluyendo el único archivo afectado por interferencia de EDR | `python -m pytest -q --basetemp=<tmp> --ignore=tests/test_local_reconciler_scripts.py` | `164 passed, 1 warning in 571.97s` | PASS (VERIFICADO) | `01-pytest-local.txt` |
| V-005 | Recuento real de tests | `python -m pytest --collect-only -q` | `171 tests collected` | PASS (VERIFICADO) | `05-readme-test-count-mismatch.txt` |
| V-006 | CI oficial sobre el commit exacto auditado | `gh run view <run-id-headSha=34773af> --json jobs` | `circuit-tests: success` (incluye step "Tests (pytest)" y "Validar adaptadores agenticos"), `product-tests: success` | PASS (VERIFICADO) | `02-ci-verification.txt` |
| V-007 | Historial reciente de CI en `develop` | `gh run list --branch develop --limit 5` | 5/5 runs recientes con `conclusion: success` | PASS | `02-ci-verification.txt` |
| V-008 | Drift de adaptadores agénticos | `pwsh -File ./scripts/sync-agentic-adapters.ps1 -Check` | `Adaptadores agenticos sincronizados.` (exit 0) | PASS | `03-adapters-check.txt` |
| V-009 | Branch protection real sobre `develop` | `gh api repos/.../branches/develop/protection` | `403 Upgrade to GitHub Pro or make this repository public` | VERIFICADO (confirma limitación documentada) | `04-branch-protection-and-governance.txt` |
| V-010 | Visibilidad del repositorio | `gh repo view --json visibility,isPrivate` | `{"isPrivate":true,"visibility":"PRIVATE"}` | VERIFICADO | `04-branch-protection-and-governance.txt` |
| V-011 | Permiso por defecto de `GITHUB_TOKEN` | `gh api repos/.../actions/permissions/workflow` | `{"default_workflow_permissions":"read", "can_approve_pull_request_reviews":false}` | VERIFICADO (default seguro) | `04-branch-protection-and-governance.txt` |
| V-012 | Commits directos a `develop` fuera de PR | `git log --first-parent develop --oneline \| grep -v "Merge pull request"` | ~15 commits directos concentrados en incidente de agosto 2026 (anterior a PR #10); desde PR #10 en adelante, únicamente merges | PASS (post-incidente) / hallazgo histórico confirmado | `04-branch-protection-and-governance.txt` |
| V-013 | Existencia de rama `main` en remoto | `git ls-remote --heads origin` | Solo existe `develop`; `main` no existe todavía | VERIFICADO — coherente con release declarado como futuro | `04-branch-protection-and-governance.txt` |
| V-014 | Residuo `docs/producto/informe-ejecutivo-2026.md` | `git log --follow`, lectura completa, `grep` de referencias en índices/`mkdocs.yml` | Introducido en `48b0e8c`, cero referencias, contenido = transcripción de IA cortada con afirmaciones obsoletas | FAIL (hallazgo F-001) | `06-informe-ejecutivo-residue.txt` |
| V-015 | Conteo de tests declarado en README vs. real | `README.md:68` = "196+ tests"; V-005 = 171 reales | Discrepancia de -25 | FAIL (hallazgo F-003) | `05-readme-test-count-mismatch.txt` |
| V-016 | Paso "Validar adaptadores agenticos" en CI, ¿gate real? | Inspección de `.github/workflows/ci.yml` líneas 28-30 | `continue-on-error: true`; un fallo real no cambia la conclusión del job requerido | FAIL (hallazgo F-002) | `07-ci-continue-on-error.txt` |
| V-017 | Búsqueda de secretos/credenciales reales | `grep -rniE` sobre patrones de tokens/keys/passwords en archivos trackeados | Sin coincidencias reales | PASS | `09-secrets-search.txt` |
| V-018 | Pinning de GitHub Actions | Inspección de `uses:` en los 4 workflows | Todas las Actions son de primera parte (`actions/*`), referenciadas por tag mayor (`@v4`/`@v5`), no por SHA | MENOR (hallazgo F-006) | `08-action-pinning.txt` |
| V-019 | Validación real de JSON Schema | `jsonschema.validate()` sobre `agents.json`/`models.json` | Ambos válidos contra su schema | PASS | `10-schema-validation.txt` |
| V-020 | Scripts huérfanos (check B3 propio del repo) | `for f in scripts/*.ps1; do grep -rlq "$name" ... \|\| echo huerfano; done` | Sin huérfanos | PASS | `11-orphan-scripts-and-traceability.txt` |
| V-021 | Consistencia índices de documentación vs. `ROADMAP.md` (check B1 propio del repo) | Lectura de `docs/tecnica/index.md`, `docs/usuario/index.md`, `ROADMAP.md` | 6 items `[x]` ↔ 6 enlaces en el bloque `FEATURE_LINKS` de cada índice, 1:1. Los 3 "extra" detectados por el `comm` automático (`arquitectura`, `circuito-agentico`, `criterios-evaluacion-repo`) son enlaces transversales "Ver también" fuera del bloque autogenerado, no inconsistencias reales | PASS (verificado por inspección manual tras falso positivo del script) | — |
| V-022 | Cadena de trazabilidad completa de una feature real | `ls runs/05-operational-readiness-docs/` | `spec.md, plan.md, tasks.md, audit-1.md, audit-2.md, decision.md, test-report-1.md, code-review-1.md` — 1364 líneas totales, ningún artefacto vacío ni ornamental | PASS | `11-orphan-scripts-and-traceability.txt` |
| V-023 | `mkdocs build --strict` (primer intento, sin instalar dependencia) | `mkdocs build --strict` | `mkdocs: command not found` en este entorno | Reintentado tras instalar la dependencia — ver V-025 | — |
| V-024 | Bloqueo de `tests/test_local_reconciler_scripts.py` en Windows local | Ejecución completa de la suite sin exclusión | Cuelgue reproducido lanzando procesos `python.exe` ocultos; causa raíz coincide exactamente con `docs/tecnica/circuito-agentico.md` §Troubleshooting | NO VERIFICADO LOCALMENTE — VERIFICADO vía CI (V-006) | `01-pytest-local.txt` |
| V-025 | `mkdocs build --strict` (reintento tras `pip install mkdocs-material`) | `pip install --quiet mkdocs-material && mkdocs build --strict --site-dir <scratch>` | Exit code `0`. "Documentation built in 1.05 seconds". Sin errores; solo mensajes `INFO` (páginas fuera de `nav`) que `--strict` no promueve a error | PASS (VERIFICADO — evidencia E4, ejecución real satisfactoria) | `12-mkdocs-build-verification.txt` |
| V-026 | Ejecución real histórica del pipeline completo de `docs.yml` (build + `gh-deploy`) | `git ls-remote --heads origin \| grep main`; inspección de `docs.yml` (`on: push: branches: [main]`) | `main` no existe en el remoto → el workflow nunca se disparó realmente en este repositorio; el paso `gh-deploy` no se ejecutó deliberadamente en esta auditoría (operación de despliegue real prohibida) | NO VERIFICADO CONTEXTUAL — sin impacto en puntuación (capacidad prospectiva ligada al release futuro a `main`, mismo criterio ya aplicado a Q6.4; no es un hallazgo puntuable) | `12-mkdocs-build-verification.txt` |

---

## H. HALLAZGOS

| ID | Tipo | Severidad | Hallazgo | Evidencia | Criterio | Puntos |
| -- | ---- | --------- | -------- | --------- | -------- | -----: |
| F-001 | SOBRA / OBSOLETO | MAJOR | Residuo documental: `docs/producto/informe-ejecutivo-2026.md` | V-014 | Q2.2 | -1.50 |
| F-002 | RIESGO / INCORRECTO | MAJOR | Quality gate de CI con `continue-on-error: true` sobre el único status check requerido | V-016 | Q5.5 | -1.50 |
| F-003 | CONTRADICTORIO | MINOR (×2 criterios) | Discrepancia de conteo de tests entre README/doc obsoleta y realidad | V-015 | Q1.3 (-0.75), Q4.1 (-0.75) | -1.50 |
| F-004 | RIESGO / FALTA | **CRITICAL** | Sin enforcement técnico real contra commits directos a `develop` | V-009, V-012 | Q6.2 | -2.25 |
| F-005 | INCOMPLETO | MINOR | Modelo de evolución del template (snapshot) no declarado explícitamente | Búsqueda documental sin resultado | Q6.6 | -0.50 |

**Total de puntos perdidos: 7.25** (idéntico al total de puntos
recuperables del camino a 100, ver sección N).

**Notas de reclasificación (dos observaciones evaluadas y descartadas
como hallazgos puntuables tras la corrección metodológica de este
informe):**

- El pinning de Actions a SHA (identificado originalmente como "F-006"
  en el borrador de este informe) se reclasificó como `SUGGESTION` — ver
  "F-006 (histórico, reclasificado)" al final de esta sección y la
  sección K.
- La falta de ejecución histórica del pipeline completo de `docs.yml`
  (identificado originalmente como "F-007" en una corrección
  intermedia de este informe) se retiró por completo como hallazgo: el
  build en sí se verificó con éxito real (V-025), Q6.5 evalúa
  reproducibilidad del build (no ejecución histórica de despliegue), y
  la falta de un release a `main` es una capacidad prospectiva no
  penalizable (mismo criterio que Q6.4). Ver "F-007 (retirado)" al
  final de esta sección y la sección L.

Ninguna de las dos resta puntos, activa Quality Gates, ni forma parte
del camino obligatorio a 100.

### F-001 — Residuo documental: `docs/producto/informe-ejecutivo-2026.md`

**Descripción:** el archivo, introducido en el commit `48b0e8c`
("feat: completar template AI-NIVELE 100%..."), es literalmente la
transcripción cruda de una sesión de asistente de IA, cortada a mitad de
una llamada a herramienta (`<tool_call>...`). No es documentación
funcional: es un artefacto accidental de proceso. Contiene además
afirmaciones ya falsas en el momento de esta auditoría ("194 tests
pytest totalmente implementados y pasando" cuando la suite real tiene
171; "100% COMPLETO", "No hay schemas ni tests faltantes").

**Evidencia:** `git log --follow` confirma que nunca se modificó desde
su introducción; `grep` sobre `docs/index.md`, `docs/tecnica/index.md`,
`docs/usuario/index.md` y `mkdocs.yml` no encuentra ninguna referencia al
archivo — está completamente desconectado de la navegación de
documentación real.

**Impacto:** un consumidor nuevo que explore `docs/producto/` puede
tropezar con este archivo y tomar como ciertas afirmaciones obsoletas
sobre el estado del proyecto (contradice Q1.3). No propaga secretos ni
rompe funcionamiento, por eso la severidad es MAJOR y no CRITICAL.

**Causa raíz:** ROOT-003 — falta de limpieza de un artefacto de sesión
de IA antes de commitear una feature marcada como "100% completa".

**Corrección mínima suficiente:** eliminar
`docs/producto/informe-ejecutivo-2026.md` del árbol (no aporta valor
como documentación real; su contenido sustantivo, si lo tuviera, ya vive
en `docs/producto/contexto-producto.md`).

**Verificación de cierre:** `git ls-files | grep informe-ejecutivo`
debe devolver vacío, y `docs/index.md` no debe requerir cambios (nunca lo
referenció).

**Puntos recuperables:** +1.50 (Q2.2).

### F-002 — Quality gate de CI con `continue-on-error: true`

**Descripción:** `.github/workflows/ci.yml` líneas 28-30, dentro del job
`circuit-tests` (el único status check requerido según `AGENTS.md`),
declara:

```yaml
- name: Validar adaptadores agenticos
  run: pwsh -NoProfile -ExecutionPolicy Bypass -File ./scripts/sync-agentic-adapters.ps1 -Check
  continue-on-error: true
```

Un fallo real de este paso (drift entre `.agentic/` y sus adaptadores
generados) **no** cambia la conclusión del job, por lo que no bloquea el
merge de una PR hacia `develop`. El paso "Tests (pytest)" del mismo job,
en cambio, sí es un gate duro (sin `continue-on-error`).

**Evidencia:** inspección directa de `ci.yml`; confirmado en vivo que en
el estado actual el check pasaría igual (`sync-agentic-adapters.ps1
-Check` retorna éxito real, sin drift — V-008), por lo que hoy no hay
consecuencia práctica, pero el gate no protegería si apareciera drift.

**Impacto:** el patrón coincide exactamente con lo que
`AUDIT_RULES.md` §44 describe como "fallo silenciado" — un mecanismo que
puede convertir un error real en éxito aparente. Riesgo real para la
propiedad "fuente única de verdad" (Q8.1) que el propio template declara
como valor central.

**Causa raíz:** ROOT-001 — decisión de diseño (probablemente para no
bloquear CI mientras se estabilizaba el adaptador en Linux) que quedó
sin revertir.

**Corrección mínima suficiente:** eliminar `continue-on-error: true` de
ese step, dejándolo como gate duro igual que el step de tests.

**Verificación de cierre:** provocar drift deliberado y confirmar que el
job `circuit-tests` reporta `failure`.

**Puntos recuperables:** +1.50 (Q5.5).

### F-003 — Discrepancia de conteo de tests

**Descripción:** `README.md:68` afirma "196+ tests de validación
estructural"; el conteo real (`pytest --collect-only`) es 171. El mismo
número incorrecto (194) aparece también dentro del residuo F-001.

**Evidencia:** V-015.

**Impacto:** bajo — no afecta funcionamiento, pero es una afirmación
cuantitativa verificable y falsa dentro del punto de entrada principal
del repositorio (README).

**Causa raíz:** ROOT-004 — el número no se actualizó tras una
consolidación/refactor de la suite de tests.

**Corrección mínima suficiente:** actualizar `README.md:68` a "171
tests" (o a una fórmula no numérica que no quede desactualizada, p. ej.
"la suite completa de `tests/`").

**Verificación de cierre:** `python -m pytest --collect-only -q` debe
coincidir con el número declarado en `README.md`.

**Puntos recuperables:** +0.75 (Q1.3) + +0.75 (Q4.1) = +1.50.

### F-004 — Sin enforcement técnico real contra commits directos a `develop`

**Descripción:** `AGENTS.md` declara como regla dura "nunca commitear
directo a `develop`", pero:

1. La branch protection nativa de GitHub está bloqueada por límite de
   plan (`403 Upgrade to GitHub Pro or make this repository public`),
   verificado en vivo (V-009).
2. No existe ningún workflow que detecte, rechace o revierta un push
   directo a `develop`: los tres workflows relevantes
   (`post-hitl-merge-gate.yml`, `post-merge-close-feature.yml`) solo se
   disparan en eventos de PR (`pull_request_review`, `pull_request:
   synchronize`, `pull_request_target: closed`), nunca en `push`.
3. El propio repositorio documenta que esto ya ocurrió: ~15 commits
   directos a `develop` en agosto de 2026 (mensajes "template 10/10",
   etc.) introdujeron un `Dockerfile` roto, scripts huérfanos con
   errores de sintaxis y una feature ficticia no registrada en
   `ROADMAP.md` — incidente limpiado recién en el PR #10.

**Evidencia:** V-009, V-012, `AGENTS.md` sección "Setup manual" (el
propio repo ya admite textualmente esta limitación).

**Impacto:** este es exactamente el ejemplo que `QUALITY_SCORE.md`
enumera como CRITICAL: "controles esenciales fácilmente evitables". El
"único HITL" es la premisa de gobernanza central de todo el circuito
agéntico que este template vende como su valor principal; hoy es
trivialmente evitable con un `git push origin develop` directo, sin
ninguna barrera técnica, y ya causó daño real una vez. El perfil TEMPLATE
exime explícitamente de penalización cuando existe "un control técnico
alternativo verificable" — se buscó activamente y no existe ninguno.

**Causa raíz:** ROOT-002 — limitación de plan de GitHub (repo privado)
sin mecanismo compensatorio implementado.

**Corrección mínima suficiente (corregida):** una mera notificación
posterior a un push directo ya ocurrido **no constituye enforcement
técnico completo** — detecta el incidente después del hecho, pero no lo
previene ni lo corrige, y por lo tanto no equivale al objetivo de
control que `AUDIT_RULES.md` §45 exige ("gate técnico previo al merge",
"workflow que rechaza integraciones no autorizadas", "automatización que
impide o revierte cambios fuera del circuito"). Las únicas correcciones
que recuperan Q6.2 a COMPLETO son:

(a) subir el repositorio a GitHub Pro o hacerlo público para habilitar
branch protection nativa real (verificable repitiendo V-009 y
confirmando `200` en vez de `403`); o

(b) un control técnico alternativo que efectivamente **prevenga o
revierta** el cambio no autorizado, no solo lo detecte — por ejemplo,
un workflow en `push` a `develop` que, al detectar que el commit no
proviene de un merge de PR conocido, revierta automáticamente ese commit
(`git revert` + push automatizado) o lo aísle (p. ej. moviéndolo a una
rama de cuarentena y restaurando `develop` al último estado válido)
antes de que cualquier otro proceso lo consuma.

Un workflow que solo **detecta y notifica** (sin prevenir ni revertir)
es una mejora real sobre el estado actual, pero no es "suficientemente
equivalente" a branch protection: en el mejor de los casos movería Q6.2
de DÉBIL (25%) a PARCIAL (50%) — recuperando solo una fracción de los
+2.25 puntos (+0.75 de los +2.25), no la totalidad. Solo (a) o una
variante real de (b) que efectivamente prevenga/revierta recuperan el
criterio completo.

**Verificación de cierre:** repetir V-009 y confirmar `200` en vez de
`403` (opción a); o, para la opción (b), provocar deliberadamente un push
directo de prueba a `develop` y confirmar que el control lo revierte o
lo aísla automáticamente, no solo que emite una notificación.

**Puntos recuperables:** +2.25 (Q6.2), condicionados a que la
corrección elegida sea realmente preventiva/correctiva y no meramente
notificativa. Cerrar este hallazgo con una corrección completa además
**libera el Quality Gate G2**, permitiendo que el score final vuelva a
igualar al score bruto normalizado — pero, como se aclara en la sección
Q, eso por sí solo no basta para llegar a 100/100 mientras F-001, F-002,
F-003 y F-005 sigan abiertos.

### F-005 — Modelo de evolución del template no declarado explícitamente

**Descripción:** el mecanismo real de adopción (clonar, crear `develop`,
trabajar independientemente) es consistente con un modelo "snapshot"
(sin sincronización posterior con el template origen), pero ningún
documento lo declara así de forma explícita e inequívoca.

**Evidencia:** búsqueda de "snapshot"/"actualiza template"/"sincroniza
template" sin resultado relevante en `README.md`/`AGENTS.md`.

**Impacto:** bajo — un consumidor razonable puede inferirlo
correctamente de la mecánica descrita, pero el perfil TEMPLATE pide que
quede "suficientemente claro" sin depender de inferencia.

**Causa raíz:** omisión editorial, no defecto de diseño.

**Corrección mínima suficiente:** agregar una frase explícita en
`README.md` o `docs/tecnica/arquitectura.md`, p. ej.: "Este template es
de tipo *snapshot*: al clonarlo, el proyecto resultante evoluciona de
forma independiente, sin mecanismo de sincronización posterior con este
repositorio."

**Verificación de cierre:** inspección de la frase agregada.

**Puntos recuperables:** +0.50 (Q6.6).

### F-007 (retirado) — Pipeline de publicación de documentación nunca ejecutado de punta a punta

**Estado: RETIRADO como hallazgo puntuable** (corrección de segunda
ronda sobre este informe). Se conserva este apartado únicamente para
trazabilidad, siguiendo la regla de no ocultar en silencio una
reevaluación (`AUDIT_RULES.md` §66).

**Razonamiento original (incorrecto):** el paso de despliegue real,
`mkdocs gh-deploy --force`, nunca se ha ejecutado en su contexto oficial
de CI porque `docs.yml` solo se dispara con `push` a `main`, y `main` no
existe en el remoto (V-013, V-026). El borrador intermedio de este
informe penalizaba Q6.5 por esa ausencia de ejecución histórica.

**Por qué se retira:** Q6.5 en `QUALITY_SCORE.md` se define
textualmente como "Build y artefactos **reproducibles**" — evalúa si el
artefacto se construye de forma correcta y reproducible, no si el
pipeline de despliegue ya se ejecutó en producción. Esta auditoría
reunió evidencia directa y ejecutable de esa reproducibilidad
(`mkdocs build --strict` con el comando exacto de `docs.yml`, resultado
`exit 0`, limpio y determinista — V-025). La falta de un release a
`main` es, igual que en Q6.4, una capacidad declarada como
futura/prospectiva (decisión humana pendiente, no obligación actual):
`AUDIT_RULES.md` §45 y `QUALITY_SCORE.md` prohíben penalizar
automáticamente una capacidad así por el simple hecho de no haber sido
ejercida todavía. No se encontró ningún otro defecto objetivo de
reproducibilidad del build que justificara mantener una pérdida de
puntos en Q6.5.

**Tratamiento final:** la ausencia de ejecución histórica del pipeline
completo pasa a ser NO VERIFICADO CONTEXTUAL (ver sección L) — no resta
puntos, no activa ningún Quality Gate y no forma parte del camino
obligatorio a 100. Q6.5 = COMPLETO = 2.00/2.00 (ver sección F).

### F-006 (histórico, reclasificado como `SUGGESTION`) — GitHub Actions sin pinning a SHA

**Descripción:** los 4 workflows referencian `actions/checkout@v4` y
`actions/setup-python@v5` por tag mayor mutable, no por SHA de commit
fijo.

**Evidencia:** V-018.

**Por qué se reclasifica (corrección aplicada a este informe):** el
borrador original penalizaba esto como MINOR puntuable en Q7.3 sin
demostrar un riesgo objetivo real no cubierto por otro mecanismo —
exactamente el patrón que `AUDIT_RULES.md` prohíbe ("no convertir en
requisito automático" una práctica de buena higiene sin evidencia de
necesidad real, y "no penalizar por preferencia del auditor"). Al
reevaluar con más rigor:

- Las dos únicas Actions usadas (`actions/checkout`, `actions/setup-python`)
  son de primera parte, mantenidas directamente por GitHub — no de un
  tercero desconocido cuyo tag pudiera reasignarse maliciosamente sin
  consecuencia reputacional severa para GitHub mismo.
- El repositorio es privado, de un solo mantenedor, sin flujo de
  contribuciones externas no confiables (V-010) — no hay superficie real
  de "PR de un desconocido" que un action comprometido pudiera explotar.
- El único workflow con el evento más sensible (`pull_request_target`,
  `post-merge-close-feature.yml`) ya usa el patrón correcto de mitigación
  (`checkout` explícito de `develop`, no del head de la PR no confiable).

No hay evidencia de un riesgo objetivo no cubierto por estos factores.
Por lo tanto, esto se reclasifica como `SUGGESTION`: **no resta puntos,
no activa Quality Gates, no bloquea 100/100 y no forma parte del camino
obligatorio a 100** (ver sección K, "Mejoras opcionales").

**Puntos recuperables:** N/A — no aplica, no es un hallazgo puntuable.

---

## I. CAUSAS RAÍZ

| ID | Causa raíz | Hallazgos relacionados | Impacto |
| -- | ---------- | ----------------------- | ------- |
| ROOT-001 | Step de verificación de drift en CI configurado con `continue-on-error: true` dentro del único job requerido | F-002 (penalizado en Q5.5); referenciado sin re-penalización en Q6.3 y Q8.1 | El gate principal (pytest) sigue siendo duro; solo el gate secundario de drift es blando. |
| ROOT-002 | Sin mecanismo técnico compensatorio ante la imposibilidad de branch protection nativa (límite de plan de GitHub) | F-004 (CRITICAL, Q6.2, activa Gate G2) | Único hallazgo que determina el score final por debajo del bruto. |
| ROOT-003 | Artefacto de sesión de IA commiteado sin limpieza durante una feature marcada "100% completa" | F-001 (Q2.2) | Residuo documental acotado, sin propagación de secretos. |
| ROOT-004 | Número de tests no actualizado tras consolidación de la suite | F-003 (Q1.3, Q4.1) | Discrepancia cuantitativa verificable, bajo impacto funcional. |

**Nota:** la ausencia de la rama `main` en el remoto (sin `ROOT` asignado
porque ya no está asociada a ningún hallazgo puntuable) se documenta
como hecho contextual en la sección L — ver "F-007 (retirado)" en la
sección H para el razonamiento completo de por qué esto no constituye
una causa raíz de pérdida de puntos.

---

## J. QUÉ SOBRA

| Elemento | Clasificación | Motivo |
| -------- | -------------- | ------ |
| `docs/producto/informe-ejecutivo-2026.md` | **ELIMINAR** | Transcripción cruda de sesión de IA, sin valor documental, sin referencias, con afirmaciones obsoletas (F-001). |
| Rama local `chore/audit-framework-v1.1` (ya mergeada a `develop` vía PR #13) | REVISAR (fuera del árbol versionado) | Observación de higiene local del entorno de este auditor, no parte del contenido commiteado del repositorio; no afecta la puntuación. Limpiar con `git branch -d chore/audit-framework-v1.1` si ya no se necesita. |

No se encontraron scripts muertos (V-020), dependencias no utilizadas,
ni duplicación manual peligrosa entre adaptadores (V-008 confirma
sincronización real).

---

## K. QUÉ FALTA

### OBLIGATORIO PARA 100/100

**Importante (corrección aplicada a esta sección):** F-004 es el único
hallazgo que activa el Quality Gate G2 (por eso el score final queda en
79 aunque el bruto sea 92.75), pero **no es el único que impide llegar a
100/100**. Los cinco puntos siguientes son todos obligatorios y
acumulativos — cerrar solo el primero sube el score final a 95.00
(libera el gate) pero no a 100:

1. Cerrar F-004 (CRITICAL): implementar branch protection real (opción
   a) o un control técnico que efectivamente **prevenga o revierta**
   pushes directos a `develop`, no solo los detecte/notifique (opción
   b) — ver la corrección endurecida en la sección H. **Esto además
   libera el Quality Gate G2**, pero por sí solo deja el score en 95.00,
   no en 100.
2. Cerrar F-002: quitar `continue-on-error: true` del step de
   verificación de adaptadores en `ci.yml`.
3. Cerrar F-001: eliminar `docs/producto/informe-ejecutivo-2026.md`.
4. Cerrar F-003: corregir el conteo de tests en `README.md` (y, al
   eliminar F-001, ese número obsoleto desaparece con él).
5. Cerrar F-005: declarar explícitamente el modelo "snapshot" del
   template.
### MEJORAS OPCIONALES

Estas **no restan puntos, no activan Quality Gates, no bloquean
100/100** y no forman parte del camino obligatorio anterior:

- **F-006 (histórico):** pinnear las Actions de los 4 workflows a SHA
  completo. Se reclasificó de MINOR puntuable a `SUGGESTION` en la
  corrección de este informe: no hay evidencia de un riesgo objetivo no
  cubierto por otro mecanismo (Actions oficiales de primera parte, repo
  privado de un solo mantenedor, sin contribuciones externas no
  confiables). Sigue siendo una buena práctica defendible, pero no es un
  requisito derivable de `QUALITY_SCORE.md`/`AUDIT_RULES.md` en este
  contexto concreto.
- **F-007 (retirado):** verificar una ejecución real y completa de
  `docs.yml` (build + `gh-deploy`) la primera vez que exista `main` con
  cambios en `docs/`. Se retiró como hallazgo puntuable en la segunda
  corrección de este informe: Q6.5 ya obtiene COMPLETO con la evidencia
  directa de reproducibilidad del build (V-025), y el release a `main`
  es una capacidad prospectiva no penalizable por falta de ejercicio
  (mismo criterio que Q6.4). Verificarlo cuando ocurra sigue siendo una
  buena práctica, no un requisito para 100/100.
- Agregar `mkdocs build --strict` como verificación en un job de CI
  disparado en PR (hoy `docs.yml` solo construye/despliega en push a
  `main`, que todavía no existe) — daría señal temprana sobre errores de
  `mkdocs` antes del primer release real.
- Considerar un `CHANGELOG.md` si en el futuro el equipo lo valora como
  complemento a `ROADMAP.md`/historial de PRs.
- Evaluar un bot de actualización de dependencias (Dependabot/Renovate)
  si la superficie de dependencias del stack de producto real crece más
  allá de las 2 actuales (`pytest`, `jsonschema`).

---

## L. NO VERIFICADO

| Elemento | Motivo | Impacto en puntuación | Cómo verificarlo después |
| -------- | ------ | ---------------------- | -------------------------- |
| `tests/test_local_reconciler_scripts.py` en este entorno local | Interferencia de EDR/antivirus con procesos PowerShell ocultos en Windows — causa raíz ya documentada por el propio repo | Ninguno: se usó evidencia de mayor jerarquía (CI real sobre el commit exacto, V-006) | Ejecutar en un entorno Windows sin EDR agresivo, o confiar en el resultado de CI (Linux, sin este problema) |
| `mkdocs gh-deploy --force` (paso de despliegue real de `docs.yml`) | Ejecutarlo publicaría de verdad una rama `gh-pages` — operación de despliegue real, prohibida durante la auditoría (`AUDIT_RULES.md` §17). El paso de *build* sí se verificó (V-025) | Ninguno: Q6.5 evalúa reproducibilidad del build (ya verificada con éxito), no ejecución histórica de despliegue; ver "F-007 (retirado)" en sección H | Verificar tras el primer push real a `main` con cambios en `docs/`, cuando se decida el primer release (mejora opcional, no requisito — sección K) |
| Ejecución real histórica completa de `docs.yml` | `main` no existe en el remoto (V-013, V-026) | Ninguno: capacidad prospectiva ligada a una decisión de release aún no tomada, mismo criterio no penalizable ya aplicado a Q6.4 | Verificar tras el primer push a `main` con cambios en `docs/` |
| Configuración de seguridad de GitHub más allá de branch protection y default workflow permissions (secret scanning, Dependabot alerts, etc.) | No cubierto por los endpoints de `gh api` consultados | Ninguno: superficie de riesgo mínima (2 dependencias oficiales) ya evaluada en Q7.2/Q7.5 | `gh api repos/.../vulnerability-alerts`, revisión manual en Settings → Security |

---

## M. QUALITY GATES

```text
G1 BLOCKER: PASS (sin BLOCKER abierto — sin pérdida de datos, sin secretos
            reales expuestos, bootstrap funcional, sin operación
            destructiva insegura detectada)
G2 CRITICAL: FAIL — F-004 abierto (sin enforcement técnico contra
             commits directos a `develop`, incidente histórico real
             confirmado) → puntuación final máxima 79/100
G3 VERIFICACIÓN ESENCIAL: PASS (suite principal de tests VERIFICADA en
             verde vía CI sobre el commit exacto auditado; CI principal
             funcional; bootstrap/validación reproducidos)
```

Gate más restrictivo aplicado: **G2 → score final = 79/100** (score
bruto normalizado 92.75 queda limitado a 79).

---

## N. CAMINO MATEMÁTICO A 100

```text
Score bruto normalizado actual: 92.75  (92.75 obtenidos / 100 aplicables × 100)
Score final actual (con Gate G2): 79.00

F-001 (Q2.2)              → +1.50
F-002 (Q5.5)              → +1.50
F-003 (Q1.3 + Q4.1)       → +0.75 +0.75 = +1.50
F-004 (Q6.2)              → +2.25   [cierra este hallazgo también libera el Gate G2]
F-005 (Q6.6)              → +0.50
                             ------
Total recuperable:          +7.25

Puntos obtenidos (92.75) + puntos recuperables obligatorios (7.25)
  = 100.00 = puntos aplicables (100.00)  ✓ Igualdad exacta verificada.

Score bruto proyectado tras cerrar todos los hallazgos:
  100.00 / 100 × 100 = 100.00
```

**Secuencia real de recuperación:** no basta con cerrar F-004 para
llegar a 100/100. El efecto de cerrar F-004 en aislamiento es:

```text
Cerrar solo F-004 (+2.25):
  Puntos obtenidos: 92.75 + 2.25 = 95.00 / 100 aplicables = 95.00 bruto
  Gate G2 ya no se activa (sin CRITICAL abierto) → score final = 95.00
  (sube desde 79, pero NO llega a 100: F-001, F-002, F-003 y F-005
  siguen abiertos y siguen restando 5.00 puntos)
```

Solo cerrando los **cinco** hallazgos puntuables (F-001, F-002, F-003,
F-004, F-005) —no solo F-004— el score bruto proyectado alcanza 100.00
y, al no quedar ningún CRITICAL abierto, el score final proyectado
también sube a 100/100, siempre que el resto de las condiciones de la
sección 25 de `QUALITY_SCORE.md` (sin BLOCKER/CRITICAL/MAJOR/MINOR
puntuables, confianza ALTA, etc.) se cumplan simultáneamente en la
reauditoría posterior sobre el nuevo commit — nunca editando
manualmente esta nota (`AUDIT_RULES.md` §66).

**Validación de consistencia repetida (obligatoria tras la corrección,
recalculada con los números de la segunda ronda):**

```text
[x] Toda pérdida de puntos tiene causa identificada (F-001, F-002,
    F-003, F-004, F-005 — cada una con ROOT-00X asociado)
[x] Todo hallazgo puntuable está materialmente relacionado con su
    criterio (ver columna "Justificación" de la sección F)
[x] Ninguna SUGGESTION resta puntos (F-006 histórico: 0 puntos, fuera
    de la tabla de hallazgos)
[x] Ninguna SUGGESTION activa gates (F-006 histórico no aparece en M)
[x] Ninguna SUGGESTION bloquea 100/100 (F-006 histórico está en la
    sección K, "Mejoras opcionales", no en "Obligatorio para 100/100")
[x] Ningún hallazgo puntuable penaliza una capacidad declarada como
    futura/prospectiva sin ejercer todavía (F-007 se retiró exactamente
    por violar esta regla respecto de Q6.5 — ver sección H)
[x] Todos los puntos perdidos aparecen en el camino obligatorio a 100
    (F-001..F-005 — cinco items, suman exactamente 7.25)
[x] Puntos obtenidos (92.75) + puntos recuperables obligatorios (7.25)
    = puntos aplicables (100.00) — igualdad exacta
[x] Los N/A están justificados (no queda ningún criterio N/A)
[x] Los Quality Gates derivan de hallazgos reales (G2 deriva de F-004,
    CRITICAL verificado en vivo — V-009, V-012)

Resultado de la validación: CONSISTENCIA METODOLÓGICA = PASS
```

---

## O. PLAN DE REMEDIACIÓN

| Prioridad | Hallazgo | Archivo(s) | Cambio exacto | Motivo | Riesgo | Puntos recuperables | Verificación |
| --------- | -------- | ---------- | -------------- | ------ | ------ | -------------------: | ------------- |
| 1 (CRITICAL) | F-004 | Configuración de GitHub (Settings/plan) + opcionalmente un nuevo workflow | Habilitar branch protection real (upgrade de plan o repo público) **o** agregar un workflow disparado en `push: [develop]` que efectivamente **prevenga o revierta** (no solo notifique) un commit que no provenga de un merge de PR conocido | Cerrar el único CRITICAL abierto y liberar el Quality Gate G2 | Bajo (no destructivo; requiere decisión humana sobre plan/visibilidad, ya señalada como pendiente en `AGENTS.md`) | +2.25 (solo si la corrección es preventiva/correctiva; una variante solo-notificación recupera como máximo +0.75) + libera el gate | Repetir V-009 (`200` en vez de `403`), o provocar un push directo de prueba y confirmar reversión/aislamiento automático real, no solo una notificación |
| 2 (MAJOR) | F-002 | `.github/workflows/ci.yml` líneas 28-30 | Quitar `continue-on-error: true` del step "Validar adaptadores agenticos" | Convertir el gate de drift en un control real, no solo nominal | Bajo (hoy no hay drift, el cambio no debería romper CI) | +1.50 | Provocar drift deliberado y confirmar `failure` del job |
| 3 (MAJOR) | F-001 | `docs/producto/informe-ejecutivo-2026.md` | Eliminar el archivo del árbol | Remover un residuo documental sin valor real y con afirmaciones obsoletas | Ninguno (sin referencias entrantes, confirmado en V-014) | +1.50 | `git ls-files \| grep informe-ejecutivo` vacío |
| 4 (MINOR) | F-003 | `README.md:68` | Actualizar "196+ tests" al conteo real vigente (o a una fórmula no numérica) | Coherencia entre documentación y realidad verificable | Ninguno | +1.50 | `pytest --collect-only -q` debe coincidir con lo declarado |
| 5 (MINOR) | F-005 | `README.md` o `docs/tecnica/arquitectura.md` | Declarar explícitamente el modelo "snapshot" de evolución del template | Eliminar dependencia de inferencia para el consumidor | Ninguno | +0.50 | Inspección de la frase agregada |
No se incluye ningún `SUGGESTION` en este plan. Dos observaciones se
evaluaron y se excluyeron del camino obligatorio a 100 durante la
corrección de este informe — ver sección K, "Mejoras opcionales": el
pinning de Actions a SHA (F-006 histórico, reclasificado como
`SUGGESTION`) y la verificación del pipeline completo de `docs.yml`
tras el primer release a `main` (F-007, retirado como hallazgo
puntuable porque Q6.5 ya obtiene COMPLETO con la evidencia directa de
reproducibilidad del build).

---

## P. SEGUNDA PASADA DE 100

```text
N/A — el score provisional consolidado (79/100, con score bruto 92.75/100)
no alcanzó 100/100 en ningún momento del proceso de puntuación, por lo
que la segunda pasada obligatoria de `AUDIT_RULES.md` §94 y
`AUDIT_PROMPT.md` §36 no aplica a esta ejecución.
```

---

## Q. CERTIFICACIÓN FINAL

> ¿Puede este repositorio considerarse actualmente un TEMPLATE
> PROFESIONAL DE REFERENCIA?

```text
NO — todavía no. F-004 es el motivo por el cual el score final (79)
queda por debajo del score bruto (92.75), pero NO es el único hallazgo
que impide 100/100: F-001, F-002, F-003 y F-005 siguen abiertos y
también restan puntos.
```

**Justificación exclusivamente basada en esta auditoría:** el
repositorio demuestra, con evidencia verificada de primera mano (no
documental), una arquitectura de circuito agéntico coherente, una fuente
única de verdad sin drift, una suite de pruebas real que pasa en la
ejecución oficial de CI sobre el commit exacto auditado, fail-safe
explícito en los scripts críticos, y una cadena de trazabilidad completa
y sustancial. Estos son exactamente los atributos que el perfil TEMPLATE
exige para la clasificación de referencia.

Sin embargo, dos hechos distintos e independientes impiden la
certificación hoy:

1. **El Quality Gate (por qué el score final es 79 y no 92.75):** ese
   mismo perfil exige explícitamente, en su lista de condiciones
   adicionales (`TEMPLATE.md` §98), "sin duplicación manual peligrosa
   conocida" y controles de integración verificados — y el propio
   `AGENTS.md` reconoce por escrito que la regla central de gobernanza
   del circuito ("nunca commitear directo a `develop`") no tiene hoy
   ningún enforcement técnico, solo disciplina humana, con un incidente
   real ya ocurrido que lo demuestra. `QUALITY_SCORE.md` clasifica
   textualmente este patrón ("controles esenciales fácilmente
   evitables") como CRITICAL (F-004), lo que activa el Quality Gate G2 y
   limita el score final a 79/100.
2. **Los puntos perdidos (por qué el score bruto es 92.75 y no 100, y
   por qué cerrar solo F-004 no basta):** incluso si F-004 se cerrara hoy
   mismo, el score subiría a 95.00/100 (ver sección N), no a 100,
   porque F-001 (residuo documental), F-002 (quality gate de CI con
   `continue-on-error`), F-003 (discrepancia de conteo de tests) y F-005
   (modelo de evolución no declarado) seguirían abiertos y puntuables.
   Ninguno de estos cuatro es un `SUGGESTION` — todos restan puntos
   reales. (Q6.5 ya obtiene COMPLETO: el build de documentación se
   verificó reproducible con éxito real — V-025 — y no se penaliza por
   la falta de un release a `main` todavía no decidido, el mismo
   criterio no penalizable ya aplicado a Q6.4.)

La certificación cambiaría a **SÍ** solo cuando los **cinco** hallazgos
puntuables (F-001, F-002, F-003, F-004, F-005) estén cerrados —no solo
F-004— y una reauditoría posterior sobre el nuevo commit confirme que
ningún hallazgo nuevo apareció en el diff de la corrección (ver sección
N para el camino matemático completo). Esa reauditoría nunca debe editar
manualmente esta nota (`AUDIT_RULES.md` §66); debe generar un informe
nuevo sobre el commit corregido.

---

## Nota sobre auditoría histórica previa (framework v1.0)

Conforme a la regla 20/21 del piloto, esta auditoría se realizó de forma
independiente desde cero, sin usar como entrada el score, las
severidades, las conclusiones, los puntos ni los hallazgos de
`.audit/reports/AUDIT-2026-08-29-05ce680-baseline-provisional.md`. Solo
después de completar la puntuación propia (sección E–N de este informe)
se consultó ese informe histórico para comparar divergencias, sin alterar
el resultado propio para hacerlo coincidir:

- **Convergencia real:** ambas auditorías, trabajando de forma
  independiente sobre commits distintos (`05ce680` vs. `34773af`),
  identificaron de forma coincidente los mismos cuatro hallazgos
  centrales — el residuo `informe-ejecutivo-2026.md`, el
  `continue-on-error` del CI, la discrepancia de conteo de tests, y la
  ausencia de enforcement técnico sobre `develop` — lo cual es una señal
  positiva de reproducibilidad metodológica entre auditores/commits
  (`AUDIT_RULES.md` §36).
- **Divergencia relevante:** la auditoría histórica (v1.0, commit
  `05ce680`) clasificó el hallazgo de branch protection como parte de su
  hallazgo F-00X sin necesariamente aplicarle severidad CRITICAL ni Gate
  G2 explícito con el mismo razonamiento documentado aquí; esta auditoría
  v1.1 sí lo hace, citando el ejemplo textual de `QUALITY_SCORE.md`
  ("controles esenciales fácilmente evitables"). Se registra esta
  divergencia de criterio para que quede disponible en el histórico del
  framework (`AUDIT_RULES.md` §69–71), sin que ello implique modificar el
  resultado de esta auditoría.
- El resto de los hallazgos, puntos exactos y la matriz completa de esta
  auditoría son de producción propia e independiente, no una copia ni un
  ajuste del informe histórico.

---

**Registro:** esta ejecución (revisada mediante dos rondas de corrección
metodológica documentadas al inicio de este informe) es completa,
consistente (`Consistencia metodológica: PASS`, validación repetida en
la sección N tras ambas correcciones) y confiable (`Confianza: ALTA`),
sobre el mismo commit auditado desde el inicio (`34773af`), por lo que
se registra como **primera BASELINE oficial del framework v1.1**,
reflejada en `SCORE_HISTORY.md` con los valores finales corregidos
(score bruto 92.75, score final 79).
