# AUDIT-2026-08-29-05ce680 — BASELINE PROVISIONAL

> **Estado histórico:** BASELINE PROVISIONAL — NO OFICIAL
>
> Esta auditoría fue ejecutada con el framework 1.0. Su revisión posterior
> detectó inconsistencias metodológicas que motivaron la versión 1.1.
> El score se conserva como evidencia histórica, pero no debe utilizarse como
> baseline oficial ni como referencia matemática para la remediación actual.

**Tipo:** Auditoría piloto — BASELINE PROVISIONAL
**Framework:** `.audit/` (QUALITY_SCORE 1.0, AUDIT_RULES 1.0, perfil TEMPLATE 1.0)
**Auditor:** Claude (Sonnet 5), vía Claude Code
**Modo:** Solo lectura + verificaciones ejecutables seguras. Sin remediación.

---

## A. IDENTIFICACIÓN

```text
Repositorio:            template (jlbellonGmail/template)
Ruta:                   D:\proyectos\template
Branch:                 develop
Commit:                 05ce680a5f4dc0c9affb6b3d06cf3ca5f1eb5e49
Tag:                    N/A (no existen tags en el repositorio)
Fecha:                  2026-08-29
Sistema operativo:      Windows 11 Pro for Workstations
Runtime/tooling:        PowerShell 7.6.4 (pwsh), Python 3.14 (local) / 3.12 (CI), pytest 8.x, gh CLI autenticado
Worktree:               LIMPIO (git status vacío antes de cualquier operación)
Perfil:                 TEMPLATE 1.0
QUALITY_SCORE:          1.0
AUDIT_RULES:            1.0
Nivel de confianza:     ALTA
```

Esta es la **primera auditoría piloto registrada** en `.audit/history/SCORE_HISTORY.md`; se conserva como `BASELINE PROVISIONAL` y no constituye la baseline oficial del repositorio.

---

## B. VEREDICTO EJECUTIVO

```text
Score bruto:            80.87/100  (79.25 puntos obtenidos / 98 puntos aplicables — Q6.5 es N/A)
Quality Gate aplicado:  G2 — CRITICAL abierto (F-002) → tope 79/100
Score final:            79/100
Confianza:              ALTA
Estado:                 APTO CON CORRECCIONES
```

**Resumen ejecutivo**: el repositorio es, en términos generales, un template agéntico
maduro, con gobernanza, trazabilidad y documentación muy por encima del promedio —
incluyendo evidencia notable de autocorrección real (el propio proyecto ya diagnosticó
y corrigió, en PRs anteriores a esta auditoría, varios de los defectos clásicos de
templates: `Dockerfile` roto, scripts huérfanos, timeouts mal unificados, commits
directos a `develop`). Sin embargo, esta auditoría encontró un defecto **CRITICAL**
verificado por inspección directa del workflow: el único control de CI que protege la
integridad de la fuente única de verdad multiherramienta (`sync-agentic-adapters.ps1
-Check`) tiene `continue-on-error: true`, por lo que su fallo real **no** bloquea el
único status check requerido (`circuit-tests`). Esto es exactamente el patrón "control
esencial fácilmente evitable" que `QUALITY_SCORE.md` define como CRITICAL, y activa el
Quality Gate G2, limitando el score final a 79/100 pese a que el score bruto (80.87)
ya lo hubiera superado.

También se encontró un residuo real y verificado (`docs/producto/informe-ejecutivo-2026.md`,
una transcripción de sesión de IA cortada a mitad de un `<tool_call>`, sin ninguna
referencia desde la documentación) y una discrepancia numérica verificable entre lo que
declara `README.md` ("196+ tests") y lo que la suite realmente tiene (171 tests,
confirmado de forma independiente en tres fuentes: recuento local, log de CI y el propio
`docs/tecnica/criterios-evaluacion-repo.md`).

El repositorio **puede usarse** como base de un proyecto nuevo hoy mismo sin bloqueos
funcionales, pero no puede certificarse como `TEMPLATE DE REFERENCIA 100/100` hasta
cerrar los hallazgos CRITICAL y MAJOR listados abajo.

---

## C. ALCANCE Y LIMITACIONES

**Inspeccionado**: estructura completa del repositorio (154 archivos trackeados),
`AGENTS.md`/`CLAUDE.md`/`README.md`/`ROADMAP.md` completos, los 4 workflows de
`.github/workflows/`, los 12 scripts de `scripts/*.ps1`, `.agentic/` completo
(roles, agents.json, models.json, mcp.json, schemas), adaptadores generados
(`.claude/agents/*.md`, `.codex/*.toml`, `opencode.json`, `.mcp.json`), toda
`docs/` (técnica, usuario, producto), todos los `runs/00` a `runs/05` (spec, plan,
tasks, audit, test-report, code-review, decision), historial Git completo,
configuración remota de GitHub vía `gh` autenticado.

**Ejecutado**: `scripts/sync-agentic-adapters.ps1 -Check` (localmente, PASS);
`pytest` (dos corridas locales parciales + inspección directa del log completo de
la ejecución oficial en GitHub Actions vía `gh run view --log`); `pytest
--collect-only` (recuento total de tests); múltiples greps/comandos de
verificación tomados literalmente de `docs/tecnica/criterios-evaluacion-repo.md`
(el propio checklist de auto-auditoría del repositorio) para no inventar
verificaciones no oficiales; `gh api repos/.../branches/develop/protection`
(branch protection real, en vivo); `gh repo view` (visibilidad real);
`git ls-remote --heads origin` (ramas remotas reales).

**No pudo verificarse**:
- Una corrida **local** 100% completa y verde de `pytest tests/` en esta máquina
  Windows: la corrida con `tmp_path` por defecto falla en bloque por un
  `PermissionError` de limpieza de temp ajeno al repo (limitación de entorno); la
  corrida con `--basetemp` propio avanzó limpiamente (~57% de los nodos, todos en
  verde) hasta colgarse en `tests/test_local_reconciler_scripts.py`, un problema que
  el propio repositorio ya diagnosticó a fondo y documentó como interferencia de
  EDR/antivirus con procesos `powershell.exe` ocultos lanzados desde `python.exe`
  (`docs/tecnica/circuito-agentico.md`, sección Troubleshooting). Se compensó esta
  limitación inspeccionando directamente el log completo de la ejecución oficial en
  GitHub Actions (Linux, sin ese problema), que es evidencia de nivel 1
  (comportamiento verificado) según la jerarquía de `AUDIT_RULES.md`.
- Ejecución real de `.github/workflows/docs.yml`: dispara solo en push a `main`, y
  `main` no existe todavía en el remoto (`git ls-remote` confirmado). No hay
  evidencia de que el pipeline de publicación de docs se haya ejecutado nunca.
- Contenido real de `.claude/settings.local.json` (archivo local, gitignorado,
  fuera del alcance del template versionado — correctamente excluido de Git).

**Accesos remotos disponibles**: GitHub API autenticado (`gh`) con permisos
`repo`, `workflow`; se usó para branch protection, visibilidad, logs de Actions.
**Accesos remotos no disponibles**: ninguno relevante detectado.

---

## D. CONTRATO DETECTADO

| ID | Capacidad/Requisito | Clasificación | Fuente | Estado |
| -- | -------------------- | -------------- | ------ | ------ |
| C1 | Circuito agéntico de 5 roles (Analyst→Reviewer→Builder→QA→Code Reviewer) | OBLIGATORIO | `AGENTS.md` | VERIFICADO |
| C2 | Único HITL formal (MERGE/NO MERGE sobre PR) | OBLIGATORIO | `AGENTS.md` | VERIFICADO (tests de `complete-approved-pr.ps1` cubren stale-approval, checks fallidos, re-run) |
| C3 | Fuente única de verdad `.agentic/` con adaptadores generados y `-Check` de drift | OBLIGATORIO | `AGENTS.md`, `docs/tecnica/arquitectura.md` | VERIFICADO en generación; **CRITICAL** en enforcement de CI (ver F-002) |
| C4 | JSON Schema real para `.agentic/agents.json`, `models.json`, `work-unit.json` | OBLIGATORIO | `docs/tecnica/arquitectura.md` | VERIFICADO (tests pasan en CI) |
| C5 | `docs/tecnica/<slug>.md` + `docs/usuario/<slug>.md` + enlaces de índice por feature | OBLIGATORIO | `AGENTS.md` | VERIFICADO (6/6 items `[x]` con documentación e índice 1:1) |
| C6 | `ROADMAP.md` nunca marca `[x]` antes del merge | OBLIGATORIO | `AGENTS.md` | VERIFICADO (estados coherentes, cierre automatizado probado por tests) |
| C7 | CI con job `circuit-tests` (pytest) obligatorio y `product-tests` placeholder declarado | OBLIGATORIO | `AGENTS.md`, `.github/workflows/ci.yml` | VERIFICADO en ejecución; el nombre coincide con lo documentado |
| C8 | Branch protection real sobre `develop` (4 requisitos) | RECOMENDADO / DECLARADO COMO LIMITACIÓN CONOCIDA | `AGENTS.md` (sección "Setup manual") | VERIFICADO que NO existe protección técnica activa (403 en vivo); el propio `AGENTS.md` ya lo declara honestamente como limitación de plan, no de configuración |
| C9 | Motor de scripts en PowerShell, Windows como plataforma primaria | DECLARADO EXPLÍCITAMENTE (decisión de arquitectura) | `docs/tecnica/arquitectura.md` | VERIFICADO — decisión coherente y bien documentada, incluida la excepción real (`local-feature-reconcile.ps1`) |
| C10 | Modo MILESTONE además de Feature | OBLIGATORIO (declarado como soportado) | `AGENTS.md` | VERIFICADO (tests dedicados: `test_milestone_contract.py`, `test_milestone_ready_for_pr.py`, `test_milestone_close_feature.py`) |
| C11 | Guía de adopción en proyecto existente + script de detección de colisiones | OPCIONAL (feature 03) | `docs/usuario/adopcion-proyecto-existente.md` | VERIFICADO (script y tests presentes y pasando) |
| C12 | Versionado SemVer con tags en `main` | DECLARADO PROSPECTIVAMENTE, aún no ejercido | `AGENTS.md` sección "Versionado" | NO VERIFICADO (nunca ejecutado — no hay tags ni rama `main`) |
| C13 | Publicación de docs vía MkDocs a GitHub Pages en push a `main` | DECLARADO, aún no ejercido | `.github/workflows/docs.yml` | NO VERIFICADO (nunca disparado — `main` no existe) |
| C14 | Contexto de producto persistente (`docs/producto/contexto-producto.md`) | OBLIGATORIO cuando exista | `AGENTS.md` | VERIFICADO (poblado, coherente, sin contenido de negocio inventado) |

---

## E. MATRIZ DE PUNTUACIÓN

| Área                          |  Máximo | Obtenido | Estado |
| ----------------------------- | ------: | -------: | ------ |
| Q1 Conformidad                |      12 |     9.75 | PARCIAL |
| Q2 Reutilización              |      12 |     9.75 | PARCIAL |
| Q3 Arquitectura               |      12 |    11.25 | MENOR |
| Q4 Documentación/DX           |      12 |    11.25 | MENOR |
| Q5 Calidad/Tests              |      16 |    12.25 | PARCIAL |
| Q6 Git/CI/CD/Release          |  14 (aplicable de 16; Q6.5 N/A) |     7.75 | PARCIAL |
| Q7 Seguridad                  |      12 |    10.75 | MENOR |
| Q8 Automatización/Gobernanza  |       8 |      6.5 | MENOR |
| **TOTAL (aplicable)**         | **98**  | **79.25** | — |

```text
Puntos obtenidos:      79.25
Puntos aplicables:     98   (100 − 2 de Q6.5, N/A justificado)
Score bruto (normalizado): 79.25 / 98 × 100 = 80.87
Quality Gate:           G2 (CRITICAL abierto: F-002) → tope 79
Score final:            79.00 / 100
```

---

## F. DETALLE POR SUBCRITERIO

| ID | Criterio | Máx. | Nivel | Obtenido | Evidencia | Hallazgo | Justificación |
| -- | -------- | ---: | ----- | -------: | --------- | -------- | ------------- |
| Q1.1 | Propósito y alcance | 3 | COMPLETO | 3.00 | `AGENTS.md` párrafo inicial, `README.md`, `arquitectura.md` | — | Propósito, alcance, restricciones y stack "sin definir todavía" quedan explícitos y sin ambigüedad |
| Q1.2 | Capacidades prometidas presentes | 3 | MENOR | 2.25 | V-003, V-006, V-015 | F-004 | Circuito, CI, docs, tests y adaptadores existen y funcionan; el número de tests declarado en README (196+) no coincide con el real (171) |
| Q1.3 | Coherencia entre fuentes | 3 | PARCIAL | 1.50 | V-008, V-013, V-015 | F-001, F-002, F-004 | Tres discrepancias reales verificadas entre lo documentado/prometido y el comportamiento real |
| Q1.4 | Requisitos obligatorios incompletos | 3 | COMPLETO | 3.00 | ROADMAP 6/6 `[x]`, contrato de features verificado por tests | — | No hay features declaradas terminadas que estén realmente a medias |
| Q2.1 | Inicialización reproducible | 3 | COMPLETO | 3.00 | V-002, V-003 (pasos de README ejecutados y verificados) | — | Los 2 pasos documentados en README (`sync-agentic-adapters -Check`, `pytest`) funcionan tal como se describen |
| Q2.2 | Ausencia de residuos | 3 | PARCIAL | 1.50 | V-013 | F-001, F-009 | Residuo real y verificado en `docs/producto/`, zona que el propio contrato del proyecto declara como de un solo archivo canónico; resto del repo limpio |
| Q2.3 | Configuración y personalización | 3 | COMPLETO | 3.00 | `ROADMAP.md` "Propósito del producto: Por definir...", `docs/producto/contexto-producto.md` | — | Queda explícito qué debe completar el consumidor y qué no tocar |
| Q2.4 | Portabilidad y extensibilidad | 3 | MENOR | 2.25 | `arquitectura.md` decisión "motor de scripts en PowerShell" | — | Limitación real (reconciliador Windows-only) pero honesta, acotada y sin impacto en CI/gate/cierre remoto |
| Q3.1 | Estructura coherente | 3 | COMPLETO | 3.00 | Inventario completo (154 archivos) | — | Separación clara `.agentic/`, `docs/`, `scripts/`, `tests/`, `runs/` |
| Q3.2 | Separación de responsabilidades | 3 | COMPLETO | 3.00 | V-002 (0 drift) | — | Fuente única + adaptadores generados, verificado en ejecución real |
| Q3.3 | Simplicidad y duplicación | 3 | MENOR | 2.25 | V-013, V-017 | F-001 | Un residuo real; por lo demás sin scripts huérfanos ni duplicación manual peligrosa detectada |
| Q3.4 | Evolución | 3 | COMPLETO | 3.00 | `arquitectura.md` (3 decisiones documentadas acumulativamente), schemas JSON reales | — | Historial de decisiones aditivo, no se sobreescribe |
| Q4.1 | README funcional | 3 | MENOR | 2.25 | V-015 | F-004 | Onboarding claro pero con una cifra factual verificablemente incorrecta |
| Q4.2 | Instalación/bootstrap | 3 | COMPLETO | 3.00 | V-002, V-003 | — | Pasos documentados = pasos reales |
| Q4.3 | Operaciones habituales | 2 | COMPLETO | 2.00 | `ready-for-pr.ps1`, `wait-pr-ci.ps1`, etc., todos documentados y referenciados | — | — |
| Q4.4 | Convenciones de contribución | 2 | COMPLETO | 2.00 | `AGENTS.md` íntegro | — | Extremadamente detallado como fuente única de proceso |
| Q4.5 | Ejemplos y troubleshooting | 2 | COMPLETO | 2.00 | `docs/tecnica/circuito-agentico.md` sección Troubleshooting, `adopcion-proyecto-existente.md` | — | Troubleshooting del problema EDR es ejemplar en nivel de detalle |
| Q5.1 | Controles automáticos | 3 | PARCIAL | 1.50 | Inspección de `scripts/`, ausencia de linter para PowerShell/Markdown | — | Existe validación de schema y de drift; no hay lint/análisis estático para el lenguaje dominante del repo (PowerShell, 3576 líneas) |
| Q5.2 | Estrategia de pruebas | 3 | COMPLETO | 3.00 | Estructura de `tests/` (contrato, e2e, schema, CI-integration, comportamiento vía subprocess) | — | Proporcional al riesgo de un template de automatización |
| Q5.3 | Tests ejecutables y pasando | 4 | COMPLETO | 4.00 | V-003, V-006 | — | 161 passed + 10 skipped (razón documentada) verificado en el log real de CI |
| Q5.4 | Protección frente a regresiones | 3 | COMPLETO | 3.00 | `criterios-evaluacion-repo.md` (C2, B2, B3 convertidos en checks/tests reales) | — | Evidencia concreta de bugs históricos → tests permanentes |
| Q5.5 | Quality gates | 3 | DÉBIL | 0.75 | V-008 | F-002 | `continue-on-error: true` sobre el check de drift de adaptadores — el gate existe pero es evitable sin fallar el CI |
| Q6.1 | Estrategia Git | 3 | COMPLETO | 3.00 | `develop`/`feature`/`milestone`, worktrees | — | Coherente y documentado |
| Q6.2 | Protección de ramas | 3 | DÉBIL | 0.75 | V-009 | F-003 | Sin protección técnica real (403 verificado en vivo); mitigación es puramente de proceso y ya falló una vez históricamente |
| Q6.3 | CI reproducible y confiable | 3 | PARCIAL | 1.50 | V-007, V-008 | F-002 (causa raíz compartida con Q5.5/Q8.3) | El job principal (`pytest`) sí es un gate real; el step de drift no lo es |
| Q6.4 | Versionado y releases | 3 | PARCIAL | 1.50 | V-011 | — | Mecanismo bien diseñado y documentado, pero nunca ejercido (sin tags, sin `main`) |
| Q6.5 | Build y artefactos | 2 | N/A | N/A | — | — | El template no empaqueta binarios, imágenes ni paquetes; no hay artefacto de build aplicable |
| Q6.6 | Compatibilidad/rollback | 2 | PARCIAL | 1.00 | Ausencia de declaración explícita del modelo (snapshot/updatable/generator) | — | Se infiere modelo "snapshot" por diseño (git clone, sin CLI generador) pero no está declarado explícitamente como tal |
| Q7.1 | Gestión de secretos | 3 | COMPLETO | 3.00 | V-014 | — | Sin secretos reales encontrados |
| Q7.2 | Dependencias | 2 | MENOR | 1.50 | `requirements-dev.txt` (2 deps, solo `>=`, sin lockfile ni bot de actualización) | — | Riesgo real pero bajo dado el tamaño mínimo de superficie |
| Q7.3 | Seguridad CI/CD | 2 | COMPLETO | 2.00 | Lectura de los 4 workflows | — | `pull_request_target` usa checkout de `develop` confiable, no del head de la PR; permisos acotados |
| Q7.4 | Defaults seguros | 2 | COMPLETO | 2.00 | Inspección de configuración | — | Nada inseguro detectado; no hay stack de producto con defaults que evaluar |
| Q7.5 | Supply chain | 3 | MENOR | 2.25 | Ausencia de `LICENSE`, sin bot de dependencias | — | Repositorio privado sin declaración explícita de términos de reutilización; no crítico pero real |
| Q8.1 | Fuente única de verdad | 2 | COMPLETO | 2.00 | V-002 | — | 0 drift verificado en ejecución real |
| Q8.2 | Responsabilidades y límites | 2 | COMPLETO | 2.00 | `.agentic/agents.json`, `opencode.json` permisos por rol | — | Roles, herramientas y permisos explícitos por agente |
| Q8.3 | Fail-safe | 2 | DÉBIL | 0.50 | V-008 | F-002 (causa raíz compartida) | El fail-safe del HITL/gate post-aprobación está bien probado; el fail-safe del check de drift está roto por diseño (`continue-on-error`) |
| Q8.4 | Trazabilidad | 2 | COMPLETO | 2.00 | `runs/05-.../decision.md` (Fase CLARIFY documentada con pregunta/respuesta real) | — | Cadena requisito→spec→auditoría→implementación→decisión→PR reconstruible |

---

## G. LEDGER DE VERIFICACIÓN

Ver `.audit/evidence/2026-08-29-05ce680-baseline-provisional/verification.md` (17 verificaciones, V-001 a
V-017) para el detalle completo con comando, resultado, estado y archivo de
evidencia de cada una.

---

## H. HALLAZGOS

| ID | Tipo | Severidad | Hallazgo | Evidencia | Criterio | Puntos |
| -- | ---- | --------- | -------- | --------- | -------- | -----: |
| F-001 | SOBRA / RESIDUO | MAJOR | `docs/producto/informe-ejecutivo-2026.md` es una transcripción de sesión de IA sin editar, cortada a mitad de un `<tool_call>` | V-013 | Q2.2, Q3.3 | -1.50 (Q2.2) + parte de -0.75 (Q3.3) |
| F-002 | RIESGO / CONTRADICTORIO | CRITICAL | `continue-on-error: true` en el único check de drift de adaptadores agénticos dentro del job de CI requerido | V-008, `.github/workflows/ci.yml:28-30` | Q1.3, Q5.5, Q6.3, Q8.3 | Ver ROOT-001 |
| F-003 | RIESGO | MAJOR | Sin protección técnica real de rama sobre `develop` (403 verificado en vivo); ya incumplida una vez históricamente | V-009, V-012 | Q6.2 | -2.25 |
| F-004 | CONTRADICTORIO | MINOR | README.md declara "196+ tests"; el recuento real y verificado es 171 | V-006, V-015 | Q1.2, Q1.3, Q4.1 | Ver ROOT-002 |
| F-005 | SOBRA / RESIDUO | SUGGESTION | Username local real (`jlbel`) en texto de troubleshooting dentro de `runs/03-.../test-report-1.md` y `runs/05-.../test-report-1.md` (evidencia histórica inmutable, no plantilla reutilizable) | grep directo | Q2.2 | 0 (no puntuable, ya reflejado parcialmente en F-001) |
| F-006 | FALTA | MINOR | Sin `LICENSE`; repositorio privado sin declaración explícita de términos de reutilización | Inspección de raíz del repo | Q7.5 | -0.75 |
| F-007 | NO VERIFICADO | SUGGESTION | `.github/workflows/docs.yml` nunca se ejecutó realmente (dispara solo en push a `main`, que no existe) | V-011 | Q6.4, Q6.5(N/A) | 0 (no puntuable — mecanismo coherente y prospectivo, no contradicción) |
| F-008 | FALTA | MINOR | Sin lockfile ni bot de actualización de dependencias (`requirements-dev.txt` con solo 2 dependencias `>=`) | Inspección de `requirements-dev.txt` | Q7.2 | -0.50 |
| F-009 | FALTA | MINOR | Sin declaración explícita del modelo de evolución del template (snapshot/updatable/generador) | Inspección de `AGENTS.md`/`arquitectura.md` | Q6.6 | -1.00 |
| F-010 | NO VERIFICADO | SUGGESTION | Sin linter/análisis estático para PowerShell (3576 líneas de scripts) ni para Markdown | Inspección de `scripts/`, ausencia de config de linter | Q5.1 | -1.50 |

### F-001 — Residuo: `docs/producto/informe-ejecutivo-2026.md`

**Descripción**: el archivo contiene una transcripción literal de una sesión de un
agente de IA ("SITUACIÓN ACTUAL - 100% COMPLETO", listas de "✅ Completo" por
agente, un plan de acción "Sesión 1 / Sesión 2"), y termina abruptamente en:

```text
Voy a escribir el contenido en `docs/producto/contexto-producto.md`. El
archivo ya existe con estructura, solo falta el contenido sustantivo.
<tool_call>
<function=read>
<parameter=filePath>
D:\proyectos\template\docs\producto\contexto-producto.md
```

Fue introducido en el commit `48b0e8c` (2026-08-25, "feat: completar template
AI-NIVELE 100%...") junto con el `Dockerfile` roto y la feature ficticia
"Ejemplo Completo" que `docs/tecnica/criterios-evaluacion-repo.md` ya documenta
como corregidos — pero este archivo específico sobrevivió esa limpieza y sigue
trackeado hoy. No tiene ninguna referencia desde `docs/index.md`,
`docs/tecnica/index.md`, `docs/usuario/index.md` ni `mkdocs.yml` (verificado con
`grep -rl`, cero resultados).

**Impacto**: `docs/producto/` es, por contrato propio del proyecto
(`AGENTS.md`), el lugar de un único archivo canónico
(`contexto-producto.md`). Un segundo archivo huérfano con contenido de sesión
sin editar, con afirmaciones desactualizadas ("194 tests", "runs/03-ejemplo-completo"
que ya no existe) degrada exactamente el criterio que el perfil TEMPLATE pondera
más ("especialmente crítica" para Q2): ausencia de residuos del origen.

**Causa raíz**: no hay una verificación automática de "todo archivo bajo `docs/`
debe estar enlazado desde su índice o justificado explícitamente" — el check B1
de `criterios-evaluacion-repo.md` solo compara en un sentido (slugs de ROADMAP
vs. enlaces del índice), no detecta archivos huérfanos sin enlazar.

**Corrección mínima suficiente**: eliminar `docs/producto/informe-ejecutivo-2026.md`.

**Verificación de cierre**: `git ls-files | grep informe-ejecutivo` debe devolver
vacío; `grep -rl "informe-ejecutivo"` sobre todo el repo debe devolver vacío.

**Puntos recuperables**: +1.50 en Q2.2, +0.75 en Q3.3 (total +2.25 puntos brutos).

### F-002 — CRITICAL: gate de drift de adaptadores silenciado en CI

**Descripción**: `.github/workflows/ci.yml`, líneas 28-30:

```yaml
- name: Validar adaptadores agenticos
  run: pwsh -NoProfile -ExecutionPolicy Bypass -File ./scripts/sync-agentic-adapters.ps1 -Check
  continue-on-error: true
```

`continue-on-error: true` significa que si `sync-agentic-adapters.ps1 -Check`
detecta divergencia (exit code distinto de 0), el step se marca en rojo en la UI
pero la conclusión del **job** `circuit-tests` sigue siendo `success` — y
`circuit-tests` es el único status check que `AGENTS.md` documenta como
requerido para mergear a `develop`. En la práctica, hoy un PR con adaptadores
desincronizados **pasaría CI igual**. Se verificó que este flag existe desde la
introducción misma del step (commit `48b0e8c`, el mismo commit de F-001) y nunca
se retiró en los 5 commits posteriores que sí tocaron ese mismo bloque de YAML
(arreglos de path separator, encoding, sintaxis). No existe ninguna mención de
`continue-on-error` ni justificación en `AGENTS.md`, `docs/tecnica/*.md` ni en
ningún mensaje de commit.

**Impacto**: exactamente el patrón que `QUALITY_SCORE.md` cita como ejemplo
textual de severidad CRITICAL ("controles esenciales fácilmente evitables") y
que `AUDIT_RULES.md` (#44) pide vigilar explícitamente ("fallos silenciados").
Contradice la narrativa central del propio repositorio sobre por qué existe
`.agentic/` como fuente única de verdad ("el modo `-Check` falla si detecta
divergencia", `AGENTS.md`).

**Causa raíz** (ROOT-001): el step se agregó probablemente para no bloquear CI
mientras se estabilizaba el propio script en un runner Linux (siguiendo la
misma serie de commits `ci: fix path separator`, `ci: fix encoding issues`,
`ci: sync opencode.json - fix adapter drift`), y el `continue-on-error` nunca se
retiró una vez estabilizado. Esta única causa explica el descuento aplicado de
forma proporcional (no triplicada) en Q1.3, Q5.5, Q6.3 y Q8.3.

**Corrección mínima suficiente**: eliminar la línea `continue-on-error: true`
del step "Validar adaptadores agenticos" en `.github/workflows/ci.yml`. Antes de
retirarlo, confirmar que el propio script corre limpio en Linux (ya verificado:
el step reportó éxito real en el run `33281358971`), para no convertir en gate
duro algo que hoy falla espuriamente.

**Verificación de cierre**: abrir un PR que introduzca deliberadamente un drift
(por ejemplo, editar a mano `opencode.json` sin regenerarlo) y confirmar que el
job `circuit-tests` termina en `failure`, no en `success`.

**Puntos recuperables**: +1.50 en Q1.3 (proporcional, compartido con F-001/F-004),
+2.25 en Q5.5, +1.50 en Q6.3, +1.50 en Q8.3. Además, al cerrar este hallazgo se
levanta el Quality Gate G2, permitiendo que el score final iguale al score bruto.

### F-003 — Sin protección técnica real de rama

**Descripción**: `gh api repos/jlbellonGmail/template/branches/develop/protection`
devuelve, en vivo, `403 Upgrade to GitHub Pro or make this repository public to
enable this feature`. Esto confirma exactamente lo que `AGENTS.md` ya declara
honestamente en su sección "Setup manual" → "Limitación conocida verificada en
este repositorio". El historial confirma que esta ausencia de control técnico ya
se tradujo en un incidente real: ~15 commits directos a `develop` en agosto de
2026 (ver V-012), solo remediados manualmente en el PR #10.

**Impacto**: la regla dura "nunca commitear directo a `develop`" depende
enteramente de disciplina de proceso (el check A1 propio del repo), no de un
control técnico. Esto es real y ya demostró materializarse una vez.

**Causa raíz**: limitación de plan de GitHub (repo privado, plan sin Pro) — no
es una decisión de configuración corregible por un agente ni por este audit.

**Corrección mínima suficiente**: decisión humana explícita (no delegable a un
agente): actualizar a GitHub Pro o hacer público el repositorio, y entonces sí
aplicar el payload de `branch protection` ya preparado en `AGENTS.md`.

**Verificación de cierre**: repetir V-009; debe devolver la configuración real
(no 403) con `required_status_checks.contexts: ["circuit-tests"]`,
`enforce_admins: true`, `required_approving_review_count: 1`,
`dismiss_stale_reviews: true`.

**Puntos recuperables**: +2.25 en Q6.2. (Nota: esta corrección depende de una
decisión de negocio del humano, no es ejecutable dentro del circuito agéntico.)

### F-004 — Cifra de tests desactualizada en README

**Descripción**: `README.md:68` declara "196+ tests de validación estructural".
El recuento real, verificado de forma independiente en tres fuentes coincidentes
(recuento local `pytest --collect-only` = 171; log de CI = 161 passed + 10
skipped = 171; `docs/tecnica/criterios-evaluacion-repo.md` = "171 tests, 168 en
verde"), es 171. Adicionalmente,
`tests/test_agents_e2e.py::test_196_or_more_tests_approx` tiene un nombre que
sugiere un piso de 196, pero su aserción real tolera de 140 a 250 — por eso pasa
igual con 171, pero el nombre induce a error a quien lo lea.

**Impacto**: bajo (no afecta funcionamiento), pero es una afirmación fáctica
verificablemente incorrecta en el documento que un consumidor nuevo lee primero.

**Causa raíz** (ROOT-002): el número parece haber quedado congelado desde una
versión anterior de la suite (el `informe-ejecutivo-2026.md` de F-001 también
dice "194 tests", una cifra distinta y también desactualizada) y nunca se
recalculó al actualizar README.

**Corrección mínima suficiente**: cambiar "196+ tests" por "171 tests" (o un
umbral honesto tipo "170+") en `README.md:68`; opcionalmente renombrar
`test_196_or_more_tests_approx` a algo como `test_test_count_within_expected_range`.

**Verificación de cierre**: `python -m pytest --collect-only -q tests/` debe
coincidir con la cifra citada en README.

**Puntos recuperables**: +0.75 en Q1.2, +0.75 en Q4.1 (proporcional, comparte
causa con la narrativa desactualizada de F-001).

### F-006 — Sin `LICENSE`

**Descripción**: no existe `LICENSE`/`LICENSE.md` en la raíz. El repositorio es
privado (verificado, V-010) y no hay una declaración explícita de "uso interno
únicamente" ni de términos de reutilización si en el futuro se comparte o se
hace público.

**Impacto**: bajo mientras el repo siga privado y de uso personal; se vuelve
relevante si se planea distribución externa.

**Corrección mínima suficiente**: agregar `LICENSE` (o una nota explícita en
`README.md` de "uso privado, no licenciado para redistribución" si esa es la
intención).

**Verificación de cierre**: presencia de `LICENSE` o declaración explícita
equivalente.

**Puntos recuperables**: +0.75 en Q7.5.

### F-008 — Sin lockfile ni bot de dependencias

**Descripción**: `requirements-dev.txt` fija únicamente `pytest>=8.0.0` y
`jsonschema>=4.21.0`, sin cota superior ni lockfile, y no existe
`.github/dependabot.yml` ni equivalente.

**Impacto**: bajo dado que son solo 2 dependencias de test, pero es un gap real
frente a "mecanismo razonable para evitar quedar congelado con dependencias
obsoletas" (perfil TEMPLATE, sección 50).

**Corrección mínima suficiente**: agregar `.github/dependabot.yml` mínimo para
el ecosistema `pip`.

**Verificación de cierre**: presencia y validez de `.github/dependabot.yml`.

**Puntos recuperables**: +0.50 en Q7.2.

### F-009 — Modelo de evolución del template no declarado explícitamente

**Descripción**: ni `AGENTS.md` ni `docs/tecnica/arquitectura.md` declaran
explícitamente si este template sigue un modelo snapshot (el proyecto se
independiza al clonar) o si promete algún mecanismo de sincronización posterior
para proyectos ya creados. Se infiere snapshot por diseño (no hay CLI
generador, es clon directo de Git), pero no está dicho en ningún lado.

**Corrección mínima suficiente**: agregar una frase explícita en
`docs/tecnica/arquitectura.md` (por ejemplo, en la sección de la decisión
"motor de scripts en PowerShell" o en una nueva) declarando el modelo snapshot
y sus implicancias.

**Verificación de cierre**: presencia de la declaración explícita.

**Puntos recuperables**: +1.00 en Q6.6.

### F-010 — Sin lint/análisis estático para PowerShell/Markdown

**Descripción**: 3576 líneas de PowerShell en `scripts/*.ps1` sin
`PSScriptAnalyzer` ni equivalente configurado; tampoco hay `markdownlint` para
la extensa documentación en Markdown.

**Corrección mínima suficiente**: agregar un step de `PSScriptAnalyzer` (o
equivalente) al job `circuit-tests`, como control adicional no bloqueante al
inicio y bloqueante una vez estabilizado.

**Verificación de cierre**: el step corre y produce resultado real (no
`continue-on-error` permanente, para no repetir F-002).

**Puntos recuperables**: +1.50 en Q5.1.

---

## I. CAUSAS RAÍZ

| ID | Causa raíz | Hallazgos relacionados | Impacto |
| -- | ---------- | ----------------------- | ------- |
| ROOT-001 | `continue-on-error: true` agregado durante la estabilización del step de CI en Linux (commit `48b0e8c` y siguientes) y nunca retirado | F-002 (afecta Q1.3, Q5.5, Q6.3, Q8.3) | CRITICAL — activa Quality Gate G2 |
| ROOT-002 | Cifras de progreso ("194 tests", "196+ tests", "100% completo") copiadas entre documentos sin recalcularse contra la suite real | F-004 (y parcialmente la narrativa de F-001) | MINOR — afecta Q1.2, Q1.3, Q4.1 |

---

## J. QUÉ SOBRA

| Elemento | Clasificación | Motivo |
| -------- | -------------- | ------ |
| `docs/producto/informe-ejecutivo-2026.md` | ELIMINAR | Residuo de sesión de IA sin editar, huérfano, con cifras desactualizadas (ver F-001) |
| `continue-on-error: true` en el step "Validar adaptadores agenticos" | ELIMINAR | Convierte un gate real en un gate cosmético (ver F-002) |
| Duplicación menor: entrada "SDD" definida dos veces en `docs/producto/contexto-producto.md` (líneas ~126 y ~140, "Terminología") | SIMPLIFICAR | Redundancia trivial, sin contradicción de contenido — no puntuable, mejora opcional |

---

## K. QUÉ FALTA

### OBLIGATORIO PARA 100/100

- Retirar `continue-on-error: true` del step de validación de adaptadores en CI
  y verificar que un drift real hace fallar `circuit-tests` (F-002).
- Eliminar `docs/producto/informe-ejecutivo-2026.md` (F-001).
- Corregir la cifra de tests en `README.md` (F-004).
- Resolver la ausencia de protección técnica de rama, dentro de lo que permite
  el plan de GitHub — o, si la decisión humana es mantenerla así, dejar
  explícito que esto es una limitación aceptada permanentemente, no pendiente
  (F-003). Nota: esta es la única corrección de esta lista que depende de una
  decisión humana externa al circuito agéntico (upgrade de plan o repo
  público), no de un cambio de código.
- Agregar `LICENSE` o declaración explícita de términos de uso (F-006).
- Agregar mecanismo mínimo de actualización de dependencias (F-008).
- Declarar explícitamente el modelo de evolución del template (snapshot) (F-009).
- Agregar control de lint/análisis estático real para PowerShell (F-010).

### MEJORAS OPCIONALES

Estas **NO restan puntos** y no son necesarias para 100/100 salvo que se
conviertan en defectos verificables en el futuro:

- Renombrar `test_196_or_more_tests_approx` para que su nombre refleje su
  rango real (140–250).
- Consolidar la entrada duplicada "SDD" en la sección Terminología de
  `docs/producto/contexto-producto.md`.
- Considerar ejecutar al menos una vez el flujo completo de release
  (crear `main`, tag `v0.x.0`, verificar `docs.yml`) para pasar de "mecanismo
  documentado" a "mecanismo verificado en ejecución real" — actualmente
  PARCIAL no por defecto sino por falta de ejercicio real.

---

## L. NO VERIFICADO

| Elemento | Motivo | Impacto en puntuación | Cómo verificarlo después |
| -------- | ------ | ----------------------- | -------------------------- |
| Corrida local 100% completa de `pytest tests/` en Windows | Interferencia de EDR/antivirus con procesos `powershell.exe` ocultos lanzados desde `python.exe`, ya diagnosticada por el propio repo | Ninguno — compensado con el log completo de la ejecución oficial en CI (nivel 1 de evidencia) | Repetir en una máquina Windows sin ese EDR, o confiar en el log de CI como ya se hizo aquí |
| Ejecución real de `.github/workflows/docs.yml` | Nunca se disparó: no existe rama `main` | Reflejado como PARCIAL en Q6.4/Q6.6, no como defecto adicional | Crear `main`, hacer el primer release, observar el run de Actions |
| Contenido de `.claude/settings.local.json` | Archivo local, gitignorado, fuera del alcance del template versionado | Ninguno | N/A — correctamente fuera de Git |
| Vulnerabilidades conocidas en `pytest`/`jsonschema` | No se consultó una base de datos de CVE en vivo (fuera del alcance razonable de esta auditoría) | Ninguno adicional a F-008 | `pip-audit` o equivalente |

---

## M. QUALITY GATES

```text
G1 BLOCKER:              PASS (ningún BLOCKER abierto)
G2 CRITICAL:              FAIL — F-002 abierto → tope de score final en 79/100
G3 VERIFICACIÓN ESENCIAL:  PASS — el job principal de CI (`circuit-tests`,
                           que ejecuta pytest) está verde en el HEAD de
                           `develop` (run 33281358971); la limitación de
                           entorno local no constituye una verificación
                           esencial rota, sino una limitación ya documentada
                           por el propio proyecto y compensada con evidencia
                           de nivel 1 (log real de CI)
```

---

## N. CAMINO MATEMÁTICO A 100

```text
Score bruto actual (normalizado): 80.87
Score final actual (con gate G2): 79.00

Paso 1 — Cerrar F-002 (retirar continue-on-error y verificar enforcement real):
  Q1.3 +1.50, Q5.5 +2.25, Q6.3 +1.50, Q8.3 +1.50  → +6.75 puntos brutos
  Además: se levanta el Quality Gate G2 (deja de aplicar el tope de 79)

Paso 2 — Cerrar F-001 (eliminar informe-ejecutivo-2026.md):
  Q2.2 +1.50, Q3.3 +0.75 → +2.25 puntos brutos

Paso 3 — Cerrar F-004 (corregir cifra de tests en README):
  Q1.2 +0.75, Q4.1 +0.75 → +1.50 puntos brutos

Paso 4 — Cerrar F-003 (protección técnica real de rama, sujeta a decisión humana):
  Q6.2 +2.25 puntos brutos

Paso 5 — Cerrar F-006 (LICENSE o declaración de términos):
  Q7.5 +0.75 puntos brutos

Paso 6 — Cerrar F-008 (dependabot/lockfile mínimo):
  Q7.2 +0.50 puntos brutos

Paso 7 — Cerrar F-009 (declarar modelo snapshot):
  Q6.6 +1.00 puntos brutos

Paso 8 — Cerrar F-010 (lint real para PowerShell):
  Q5.1 +1.50 puntos brutos

Suma de puntos recuperables:
  6.75 + 2.25 + 1.50 + 2.25 + 0.75 + 0.50 + 1.00 + 1.50 = 16.50

Puntos obtenidos proyectados: 79.25 + 16.50 = 95.75
Puntos aplicables:            98 (Q6.5 sigue N/A)
Score bruto proyectado:       95.75 / 98 × 100 = 97.70

Nota: 97.70 < 100 porque los pasos de "mejora opcional" (sección K) no suman
puntos por definición, y porque Q6.4/Q6.6 seguirían sin el ejercicio real de un
release completo (ver "NO VERIFICADO"). Para llegar a 100/100 exacto además
haría falta ejecutar al menos un release real (crear main, tag, verificar
docs.yml) y confirmar Confianza ALTA sin ningún NO VERIFICADO pendiente
aplicable.
```

Si se activa un gate, el hallazgo exacto que debe cerrarse para eliminarlo es
**F-002** (único CRITICAL abierto, gate G2).

---

## O. PLAN DE REMEDIACIÓN

| Prioridad | Hallazgo | Archivo(s) | Cambio exacto | Motivo | Riesgo | Puntos recuperables | Verificación |
| --------- | -------- | ---------- | -------------- | ------ | ------ | -------------------: | ------------- |
| 1 (CRITICAL) | F-002 | `.github/workflows/ci.yml` | Eliminar `continue-on-error: true` (línea 30) del step "Validar adaptadores agenticos" | Levanta el Quality Gate G2 y restaura el gate real de fuente única de verdad | Bajo — el script ya corre limpio en Linux (verificado) | +6.75 (+ levanta el gate) | PR de prueba con drift deliberado debe fallar `circuit-tests` |
| 2 (MAJOR) | F-001 | `docs/producto/informe-ejecutivo-2026.md` | Eliminar el archivo | Elimina un residuo verificado, huérfano y con contenido desactualizado | Ninguno — no referenciado desde ningún lado | +2.25 | `git ls-files \| grep informe-ejecutivo` vacío |
| 3 (MAJOR) | F-003 | Configuración de GitHub (fuera del repo) | Decisión humana: upgrade a GitHub Pro o hacer público el repo, luego aplicar el payload de `branch protection` ya documentado en `AGENTS.md` | Cierra el único gap de enforcement técnico real sobre `develop` | Medio — decisión de costo/visibilidad que excede el alcance de un agente | +2.25 | `gh api .../branches/develop/protection` debe devolver configuración real, no 403 |
| 4 (MINOR) | F-004 | `README.md` | Cambiar "196+ tests" por la cifra real (171) en la línea 68 | Corrige una afirmación fáctica verificablemente incorrecta | Ninguno | +1.50 | `pytest --collect-only` coincide con la cifra citada |
| 5 (MINOR) | F-006 | raíz del repo | Agregar `LICENSE` o declaración explícita de términos de uso en `README.md` | Reduce ambigüedad sobre reutilización | Ninguno | +0.75 | Presencia del archivo/declaración |
| 6 (MINOR) | F-008 | `.github/dependabot.yml` (nuevo) | Agregar configuración mínima de Dependabot para `pip` | Evita congelamiento silencioso de las 2 dependencias de test | Ninguno | +0.50 | Archivo válido presente |
| 7 (MINOR) | F-009 | `docs/tecnica/arquitectura.md` | Agregar declaración explícita del modelo snapshot | Cierra una ambigüedad real sobre expectativas de actualización | Ninguno | +1.00 | Presencia de la declaración |
| 8 (MINOR) | F-010 | `.github/workflows/ci.yml` | Agregar step de `PSScriptAnalyzer` (inicialmente no bloqueante y documentado como tal, luego bloqueante) | Cierra el único gap de control automático de calidad sobre el lenguaje dominante del repo | Bajo — introducir gradualmente para no romper CI de golpe | +1.50 | Step corre y produce resultado real, sin `continue-on-error` permanente |

No se incluyen las `SUGGESTION` (F-005, F-007) en este plan obligatorio, según
`AUDIT_RULES.md` #63.

---

## P. SEGUNDA PASADA DE 100

```text
N/A — el score provisional (79.00, con score bruto 80.87) no alcanzó 100/100,
por lo que la segunda pasada obligatoria de AUDIT_RULES.md (#94) no aplica en
esta auditoría.
```

---

## Q. CERTIFICACIÓN FINAL

> ¿Puede este repositorio considerarse actualmente un TEMPLATE PROFESIONAL DE REFERENCIA?

**NO.**

Justificación exclusivamente basada en esta auditoría: el repositorio muestra
gobernanza, trazabilidad y documentación de nivel notablemente alto para un
template — incluida evidencia concreta y verificada de que el propio equipo ya
detectó y corrigió varios defectos clásicos de templates en auditorías
anteriores (`docs/tecnica/criterios-evaluacion-repo.md`). Sin embargo, esta
auditoría verificó por inspección directa un defecto CRITICAL real y activo
(F-002: el gate de integridad de la fuente única de verdad multiherramienta es
evitable sin fallar CI), lo que por definición de `QUALITY_SCORE.md` impide la
certificación `TEMPLATE DE REFERENCIA 100/100` (`Score final = 79/100`, tope
impuesto por Quality Gate G2) hasta que ese hallazgo — y los MAJOR
relacionados (F-001, F-003) — queden cerrados y reverificados en una nueva
auditoría sobre un commit posterior.
