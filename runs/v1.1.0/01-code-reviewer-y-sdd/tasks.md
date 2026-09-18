# Tasks: Code Reviewer agent + SDD + correcciones de contrato

Cada tarea es pequeña, verificable, y referencia el/los `AC-N` de
`spec.md` que satisface. Orden sugerido, no estrictamente secuencial
salvo donde se indica dependencia.

## Eje 1 — `code-reviewer-agent`

- **T-01** — Escribir `.agentic/roles/code-reviewer-agent.md` con la
  estructura descrita en `plan.md` §2.1.
  Verificación: el archivo existe, no está vacío, y contiene las
  secciones "Checklist de auditoria", "Tu output: code-review-N.md" y
  "Modo MILESTONE".
  Traza: AC-1.

- **T-02** — Agregar `roles.code-reviewer-agent` a `.agentic/agents.json`
  copiando la forma de `roles.reviewer-agent` (mismo `claude.model`,
  `claude.effort`, `codex.model`, `codex.model_reasoning_effort`,
  `opencode.model`, `opencode.reasoningEffort`), con
  `claude.tools = ["Read", "Grep", "Glob"]` y
  `opencode.permission = { edit: deny, bash: deny, webfetch: deny }`.
  Verificación: `.agentic/agents.json` sigue siendo JSON válido; el
  bloque nuevo tiene exactamente esos campos.
  Traza: AC-2. Depende de T-01 (necesita `prompt` apuntando a un
  archivo existente antes de correr `sync-agentic-adapters.ps1`).

- **T-03** — Agregar `roles.code-reviewer-agent` a
  `.agentic/models.json` copiando exactamente `roles.reviewer-agent`.
  Verificación: JSON válido; `default`/`fallback` idénticos a
  `reviewer-agent`.
  Traza: AC-3.

- **T-04** — Ejecutar `scripts/sync-agentic-adapters.ps1` (regenerar)
  y luego `scripts/sync-agentic-adapters.ps1 -Check` (validar).
  Verificación: ambas corridas terminan en exit code 0; existen
  `.claude/agents/code-reviewer-agent.md`,
  `.codex/code-reviewer-agent.config.toml`, y `opencode.json` contiene
  `agent.code-reviewer-agent`. Confirmar que no hubo que tocar
  `scripts/sync-agentic-adapters.ps1` (o, si hizo falta, que el cambio
  siguió siendo genérico, sin lista hardcodeada de nombres de agente).
  Traza: AC-4. Depende de T-01, T-02, T-03.

- **T-05** — Actualizar `AGENTS.md`: sección "Circuito" (orden
  `Builder → QA → Code Reviewer → READY_FOR_PR`, renumerar pasos),
  "Retornos permitidos" (agregar `code-reviewer-agent → builder-agent`),
  "Artefactos" (agregar `code-review-N.md`), "Formato de veredicto"
  (mencionar los tres tipos de archivo), corregir "4 agentes" → "5
  agentes", y el contrato mínimo de artefactos descripto al inicio de
  "Circuito" (agregar `plan.md`, `tasks.md`, `code-review-N.md`).
  Verificación manual reproducible: leer el archivo, confirmar que no
  queda ninguna mención residual a "4 agentes" ni al orden viejo sin
  Code Reviewer (`grep -n "4 agentes" AGENTS.md` no matchea).
  Traza: AC-5, AC-6.

- **T-06** — Actualizar `scripts/ready-for-pr.ps1`: agregar
  `code-review-N.md` a `$evidenceSection` en ambas ramas (`Feature` y
  `Milestone`).
  Verificación: leer el diff; confirmar que ambos bloques
  (`if ($Mode -eq "Milestone")` / `else`) mencionan
  `$($info.RunDir)/code-review-N.md`.
  Traza: AC-8.

- **T-07** — Actualizar `docs/tecnica/circuito-agentico.md` y
  `docs/usuario/circuito-agentico.md`: mencionar 5 roles, el nuevo
  orden, y `code-review-N.md`/SDD.
  Verificación: ambos archivos no vacíos, contienen la palabra
  "Code Reviewer" y "plan.md"/"tasks.md".
  Traza: AC-9, AC-15 (parcial, ver T-14).

- **T-08** — Actualizar `.agentic/README.md` y `ROADMAP.md` (línea de
  encabezado) para no contradecir el nuevo orden.
  Verificación: `ROADMAP.md` línea de encabezado menciona "Code
  Reviewer"; `.agentic/README.md` no requiere cambio funcional si no
  contradice nada — confirmar con lectura que sigue siendo consistente
  (mencionar `.agentic/schemas/` como parte de la fuente canónica).
  Traza: AC-27, y consistencia general con AC-5/AC-9.

## Eje 2 — SDD

- **T-09** — Actualizar `.agentic/roles/analyst-agent.md`: agregar que
  el rol produce `plan.md` y `tasks.md` como parte estándar de su
  output (con su formato esperado, mismo nivel de detalle que la
  sección "Tu output: spec.md" ya tiene), aclarando que `spec.md`
  sigue siendo QUÉ+POR QUÉ sin detalle de implementación.
  Verificación: el archivo contiene una sección nueva "Tu output:
  plan.md" y "Tu output: tasks.md" (o equivalente), no vacías.
  Traza: AC-10.

- **T-10** — Actualizar `.agentic/roles/reviewer-agent.md`: checklist
  ampliada para auditar `plan.md`+`tasks.md` junto con `spec.md`
  (coherencia, trazabilidad requisito→plan→tarea), y actualizar
  sección "Modo MILESTONE" para aclarar que son únicos por work unit
  pero deben cubrir cada item.
  Verificación: el archivo menciona explícitamente "plan.md",
  "tasks.md" y "trazabilidad".
  Traza: AC-11, AC-12.

- **T-11** — Modificar `Assert-WorkUnitContract` en
  `scripts/feature-contract.ps1` (ambos modos) para exigir
  `Assert-NonEmptyFile "$($info.RunDir)/plan.md"` y
  `Assert-NonEmptyFile "$($info.RunDir)/tasks.md"`, junto a la
  exigencia ya existente de `spec.md`.
  Verificación: test automatizado (ver T-16) confirma fallo si falta
  cualquiera de los dos, y éxito cuando ambos existen junto al resto.
  Traza: AC-13.

## Eje 3 — Bugs (contrato, decision, close-feature, schemas)

- **T-12** — Implementar `Get-LatestVerdictArtifact` y
  `Assert-LatestVerdictApproved` en `scripts/feature-contract.ps1`
  según el diseño de `plan.md` §2.3 (parseo de bloque ```` ```yaml ````,
  selección por número entero real, validación de `status`/`attempt`,
  mensajes de error identificables).
  Verificación: unidad cubierta por T-17/T-18/T-19 abajo.
  Traza: AC-15.

- **T-13** — Reemplazar en `Assert-WorkUnitContract` (modo `Feature` y
  modo `Milestone`) el uso de `Get-FirstExistingArtifact` +
  `Assert-NonEmptyFile` para `audit-*.md`/`test-report-*.md` por
  `Assert-LatestVerdictApproved` (prefijos `audit`, `test-report`), y
  agregar la llamada equivalente para `code-review` (nueva, ligada a
  T-11 del Eje 1/AC-7). Eliminar `Get-FirstExistingArtifact` del
  archivo si, tras el cambio, no queda ningún llamador restante
  (confirmar con grep antes de borrar).
  Verificación: grep confirma cero usos de `Get-FirstExistingArtifact`
  fuera del propio archivo si se eliminó, o que sigue usándose en algún
  otro punto documentado si se conserva.
  Traza: AC-7, AC-15.

- **T-14** — Escribir tests que reproducen los escenarios exactos de
  la auditoría (orden lexicográfico vs. numérico, último intento
  rechazado con uno previo aprobado, YAML malformado, `attempt`
  desalineado del nombre de archivo) en
  `tests/test_feature_contract_scripts.py` y
  `tests/test_milestone_contract.py`, actualizando también los
  fixtures de "run completo válido" existentes al nuevo formato real
  de veredicto (fence ```` ```yaml ```` + `attempt` coincidente).
  Verificación: `pytest tests/test_feature_contract_scripts.py
  tests/test_milestone_contract.py -q` pasa completo, incluidos los
  casos nuevos negativos (deben fallar el script bajo prueba con el
  mensaje esperado, verificado con `assert` sobre `stderr`/excepción).
  Traza: AC-16, AC-17.

- **T-15** — Modificar `New-DecisionFile` según `plan.md` §2.4: quitar
  "MERGE aprobado...", agregar "Estado tecnico: ready_for_pr." y la
  aclaración de HITL, y sumar `plan.md`/`tasks.md`/`code-review-1.md` a
  "Evidencias revisadas".
  Verificación: test (nuevo o ampliado en
  `tests/test_feature_contract_scripts.py`) que genera un
  `decision.md` con `New-DecisionFile` y hace `assert` de que NO
  contiene "MERGE aprobado" y SÍ contiene "ready_for_pr" y una mención
  a HITL/GitHub.
  Traza: AC-18, AC-19.

- **T-16** — Test que confirma que el contrato falla limpiamente si
  falta `plan.md` o `tasks.md`, y pasa cuando ambos existen junto al
  resto de artefactos ya exigidos (spec, decision, docs, índices,
  audit/test-report/code-review aprobados).
  Verificación: `pytest` verde sobre el caso nuevo, en ambos modos
  Feature y Milestone.
  Traza: AC-14.

- **T-17** — Implementar el fix de retry de push en
  `scripts/close-feature.ps1` según `plan.md` §2.5, para el bloque
  `Feature`.
  Verificación: cubierta por T-19.
  Traza: AC-20 (parcial, Feature).

- **T-18** — Aplicar el mismo fix al bloque `Milestone` de
  `scripts/close-feature.ps1`.
  Verificación: cubierta por T-19.
  Traza: AC-20 (parcial, Milestone).

- **T-19** — Escribir/ampliar tests en
  `tests/test_close_feature_script.py` y
  `tests/test_milestone_close_feature.py` que reproducen: (a) commit
  local creado, push simulado como fallido, reejecución exitosa que
  pushea el pendiente y pasa la verificación final; (b) reejecución
  cuando el remoto ya tiene el cierre completo, sin error y sin push
  adicional que falle.
  Verificación: `pytest tests/test_close_feature_script.py
  tests/test_milestone_close_feature.py -q` pasa completo.
  Traza: AC-21, AC-22.

- **T-20** — Crear `.agentic/schemas/agents.schema.json` según
  `plan.md` §2.6.
  Verificación: el archivo es JSON Schema válido (parseable) y describe
  los campos reales de `.agentic/agents.json` actual (incluyendo la
  entrada `code-reviewer-agent` agregada en T-02).
  Traza: AC-23.

- **T-21** — Crear `.agentic/schemas/models.schema.json` según
  `plan.md` §2.6.
  Verificación: JSON Schema válido, describe los campos reales de
  `.agentic/models.json` actual (incluyendo `roles.code-reviewer-agent`
  de T-03).
  Traza: AC-23.

- **T-22** — Crear `.agentic/schemas/work-unit.schema.json` según
  `plan.md` §2.6.
  Verificación: JSON Schema válido, describe la forma fija documentada
  en `Read-WorkUnitManifest`/`Write-WorkUnitManifest`.
  Traza: AC-25.

- **T-23** — Agregar `jsonschema` a `requirements-dev.txt`.
  Verificación: `pip install -r requirements-dev.txt` instala sin
  error en el entorno de CI/local.
  Traza: AC-26 (parcial).

- **T-24** — Documentar la nueva dependencia de test en
  `docs/tecnica/arquitectura.md` como sección `## Decisión: ...` nueva
  (qué se agrega, por qué ahora, por qué este enfoque, qué sigue
  igual).
  Verificación manual: la sección existe y sigue el mismo formato que
  la decisión ya presente ("fuente canónica agentica y router de
  modelos").
  Traza: AC-26.

- **T-25** — Escribir `tests/test_agentic_schemas.py`: valida
  `.agentic/agents.json` contra `agents.schema.json`,
  `.agentic/models.json` contra `models.schema.json`, y un manifest de
  Milestone (real o fixture) contra `work-unit.schema.json`, con un
  caso positivo y uno negativo por schema.
  Verificación: `pytest tests/test_agentic_schemas.py -q` pasa
  completo, incluyendo los 3 casos negativos (deben lanzar
  `jsonschema.exceptions.ValidationError` o equivalente).
  Traza: AC-24, AC-25.

- **T-26** — Ampliar `tests/test_agentic_sync_scripts.py` con la
  verificación de que `.claude/agents/code-reviewer-agent.md` generado
  tiene `tools: Read, Grep, Glob` (sin `Write`/`Edit`/`Bash`) y que
  `sync-agentic-adapters.ps1 -Check` sigue pasando con el rol nuevo.
  Verificación: `pytest tests/test_agentic_sync_scripts.py -q` pasa.
  Traza: AC-4.

## Documentación de la propia feature (obligatorias, sin excepción)

- **T-27** — Escribir `docs/tecnica/code-reviewer-y-sdd.md`: decisiones
  de diseño de los 3 ejes (nuevo agente y su aislamiento read-only,
  formato de veredicto compartido y su parseo, wording de
  `decision.md`, fix de retry de `close-feature.ps1`, schemas y su
  elección de `additionalProperties`, nueva dependencia de test).
  Verificación: archivo no vacío.
  Traza: AC-28.

- **T-28** — Escribir `docs/usuario/code-reviewer-y-sdd.md`: qué cambia
  para quien opera el circuito (nuevo agente, nuevo orden, nuevos
  archivos `plan.md`/`tasks.md`/`code-review-N.md`, cómo regenerar
  adaptadores).
  Verificación: archivo no vacío.
  Traza: AC-29.

- **T-29** — Ejecutar `scripts/update-doc-indexes.ps1 01-code-reviewer-y-sdd
  "<Titulo derivado del slug>"` (o el mecanismo equivalente que usa
  `builder-agent`) para enlazar ambos documentos en
  `docs/tecnica/index.md` y `docs/usuario/index.md` dentro de la zona
  `FEATURE_LINKS_START`/`FEATURE_LINKS_END`, sin duplicados.
  Verificación: `Assert-IndexLink` (parte de `Assert-FeatureContract`)
  pasa para ambos índices.
  Traza: AC-31, AC-32.

- **T-30** — Crear `runs/v1.1.0/01-code-reviewer-y-sdd/decision.md` con
  `New-DecisionFile` (ya corregido por T-15) y completar
  "Decisiones demostrables" con las decisiones reales tomadas durante
  la implementación (no genéricas).
  Verificación: archivo no vacío, no contiene "MERGE aprobado".
  Traza: AC-18, AC-30.

## Orden de dependencias críticas

1. T-01 → T-02/T-03 → T-04 (el rol debe existir antes de regenerar
   adaptadores).
2. T-12 → T-13 (la función de parseo debe existir antes de conectarla
   al contrato).
3. T-11 y T-13 pueden ir en paralelo pero ambos deben estar antes de
   T-16 (test de contrato completo).
4. T-17/T-18 antes de T-19 (fix antes de test que lo confirma).
5. T-20/T-21/T-22/T-23 antes de T-25 (schemas y dependencia antes del
   test que los usa).
6. Todo lo anterior antes de T-27/T-28/T-29/T-30 (la documentación de
   cierre describe decisiones ya tomadas, no antICIPAdas).
