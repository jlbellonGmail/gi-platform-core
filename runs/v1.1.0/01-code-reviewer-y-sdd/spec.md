# Spec: Code Reviewer agent + Spec-Driven Development (SPEC→PLAN→TASKS) + correcciones de contrato

## Alcance

Incluye:

1. **Quinto agente `code-reviewer-agent`** (read-only), que revisa el DIFF
   FINAL (código, tests, scripts, config, docs técnicas afectadas)
   DESPUÉS de que QA aprueba, no antes. Nuevo orden del circuito:
   `Builder → QA → Code Reviewer → READY_FOR_PR`. Si `Code Reviewer`
   rechaza, el circuito vuelve a `Builder → QA → Code Reviewer` (no a
   `analyst-agent`). Produce `code-review-N.md` con el mismo bloque YAML
   de veredicto (`status`, `attempt`, `feedback`) que `audit-N.md` y
   `test-report-N.md`.
2. **Formalización de Spec-Driven Development**: dos artefactos nuevos
   producidos por `analyst-agent` junto a `spec.md`: `plan.md` (CÓMO —
   estrategia de implementación, arquitectura afectada, componentes,
   contratos, compatibilidad, dependencias, estrategia de tests, impacto
   operacional) y `tasks.md` (tareas ejecutables y verificables,
   trazables a un requisito/criterio de aceptación de la spec).
   `reviewer-agent` pasa a auditar los tres artefactos juntos:
   coherencia y trazabilidad requisito→plan→tarea.
3. **Corrección de 3 bugs reales** en `scripts/feature-contract.ps1`,
   `scripts/close-feature.ps1` y las referencias `$schema` rotas de
   `.agentic/agents.json` / `.agentic/models.json`, más creación de un
   schema real para el manifest de milestone (`work-unit.json`).
4. **Actualización de documentación del propio circuito** (`AGENTS.md`,
   `ROADMAP.md` encabezado, `scripts/ready-for-pr.ps1`,
   `docs/tecnica/circuito-agentico.md`,
   `docs/usuario/circuito-agentico.md`, `.agentic/README.md`) para
   reflejar 5 agentes, el nuevo orden y SDD.

Explícitamente NO incluye (ver "Riesgos / supuestos" para el detalle de
por qué quedan afuera):

- Automatizar GitHub branch protection / rulesets reales del
  repositorio. Es configuración manual de GitHub que el humano debe
  aplicar. Esta feature puede documentar el comando/acción exacta en
  `docs/tecnica/`, pero no la ejecuta ni la scriptea.
- Reforzar `complete-approved-pr.ps1` para comparar el SHA de la última
  review aprobatoria contra el HEAD actual de la PR ("stale approval").
- Tests de concurrencia real entre dos procesos cerrando a la vez, o
  locks distribuidos nuevos más allá de lo que ya cubre
  `local-feature-reconcile.ps1`.
- Un tercer modo (EPIC) del circuito. Solo existen `Feature` y
  `Milestone`.
- Invocar modelos reales de ningún proveedor (esto sigue siendo
  configuración/prompt, no ejecución de LLM).

## Contexto

El circuito agéntico actual (`analyst → reviewer → builder → qa`) no
tiene una revisión técnica final del código después de que QA modifica
o agrega tests — un cambio que QA introduce puede quedar sin revisar. El
template tampoco separa formalmente el "qué/por qué" (spec) del
"cómo" (plan) y del desglose ejecutable (tasks), lo cual dificulta que
`builder-agent` tenga un plan de implementación explícito y trazable
antes de escribir código.

Además, una auditoría del código real detectó que el contrato común
(`Assert-FeatureContract`/`Assert-WorkUnitContract`) nunca valida el
contenido del último veredicto real: solo comprueba que exista un
archivo `audit-N.md`/`test-report-N.md` no vacío, seleccionado con
orden lexicográfico (`audit-1, audit-10, audit-2`) en vez de numérico.
Esto permite que un intento rechazado o mal formado pase el contrato.
También se detectó que `New-DecisionFile` escribe una afirmación de
aprobación de merge que no corresponde (el único HITL es la aprobación
de la PR en GitHub), que `close-feature.ps1` tiene un bug de reintento
de push reproducible, y que `.agentic/agents.json` / `.agentic/models.json`
referencian un directorio `.agentic/schemas/` que no existe.

Esta feature corrige esos bugs y extiende el circuito en la misma
pasada porque los tres ejes tocan el mismo archivo central
(`scripts/feature-contract.ps1`) y el mismo conjunto de documentación
del propio circuito — separarlos generaría conflictos de merge y
documentación inconsistente a mitad de camino.

## Convención de nombres de documentación usada en esta spec

Siguiendo el patrón ya establecido por `Get-WorkUnitInfo -Mode Feature`
en `scripts/workunit-lib.ps1` (y el ejemplo real
`00-fuente-unica-router-modelos` → `docs/tecnica/fuente-unica-router-modelos.md`),
el slug de esta feature (`01-code-reviewer-y-sdd`) produce
`docSlug = code-reviewer-y-sdd`. Los criterios de aceptación de
documentación de esta spec usan por lo tanto
`docs/tecnica/code-reviewer-y-sdd.md` y
`docs/usuario/code-reviewer-y-sdd.md` (NO `01-code-reviewer-y-sdd.md`).
Ver "Riesgos / supuestos".

## Criterios de aceptación

Cada criterio lleva un identificador `AC-N` para que `plan.md` y
`tasks.md` puedan referenciarlo explícitamente (trazabilidad).

### Eje 1 — `code-reviewer-agent`

- **AC-1**: Existe `.agentic/roles/code-reviewer-agent.md` con el prompt
  funcional canónico del rol, mismo estilo que `analyst-agent.md` y
  `reviewer-agent.md`: pregunta central "¿la implementación está
  técnicamente bien construida?", instrucción explícita de revisar el
  DIFF FINAL después de QA (no antes), checklist de auditoría técnica
  (calidad de implementación vs. spec/plan/tasks, cobertura real de
  tests agregados por QA, manejo de errores, seguridad básica,
  legibilidad, ausencia de código muerto/deuda evidente no declarada),
  instrucción de producir `code-review-N.md` con el bloque YAML de
  veredicto, instrucción de que un rechazo vuelve a `Builder → QA →
  Code Reviewer` (no a `analyst-agent`), y sección "Modo MILESTONE"
  equivalente a la de `reviewer-agent.md` (un único `code-review-N.md`
  por work unit, pero evaluando el diff de cada item).
- **AC-2**: `.agentic/agents.json` tiene una cuarta entrada
  `roles.code-reviewer-agent` con: `description`, `prompt:
  ".agentic/roles/code-reviewer-agent.md"`, `claude.tools` limitado a
  `["Read", "Grep", "Glob"]` (sin `Write`/`Edit`/`Bash`), `claude.model`
  y `claude.effort` iguales a los de `reviewer-agent`, bloque `codex`
  con el mismo `model`/`model_reasoning_effort` que `reviewer-agent`, y
  bloque `opencode` con `mode: "subagent"`, mismo `model` y
  `reasoningEffort` que `reviewer-agent`, y `permission` con
  `edit: "deny"`, `bash: "deny"`, `webfetch: "deny"`.
- **AC-3**: `.agentic/models.json` tiene una entrada
  `roles.code-reviewer-agent` con el mismo `default` y la misma lista
  `fallback` (go/zen/openrouter-free) que `roles.reviewer-agent`, sin
  introducir ningún proveedor o modelo no presente ya en
  `providers`.
- **AC-4**: Ejecutar `scripts/sync-agentic-adapters.ps1` (sin `-Check`)
  y luego `scripts/sync-agentic-adapters.ps1 -Check` termina en éxito
  (exit code 0) y genera/actualiza, sin edición manual:
  `.claude/agents/code-reviewer-agent.md`,
  `.codex/code-reviewer-agent.config.toml`, y una entrada
  `agent.code-reviewer-agent` dentro de `opencode.json`. No se agrega
  ninguna lista manual nueva de nombres de agentes dentro de
  `scripts/sync-agentic-adapters.ps1`: la iteración sigue derivándose
  de `agents.roles.PSObject.Properties`, igual que hoy.
- **AC-5**: `AGENTS.md` describe el circuito como
  `Builder (etapa 3) → QA (etapa 4) → Code Reviewer (nueva etapa 4.5 o
  5, renumerada) → READY_FOR_PR`, ya no dice "Cada uno de los 4 agentes"
  sino "Cada uno de los 5 agentes", agrega `code-reviewer-agent` como
  read-only/subagente al mismo nivel que `analyst-agent`/
  `reviewer-agent` en la enumeración del circuito, agrega la sección
  "Retornos permitidos" con la entrada
  `code-reviewer-agent → builder-agent cuando el code review es
  rejected`, y el contrato mínimo de artefactos exigidos ahora incluye
  `plan.md`, `tasks.md` y `code-review-N.md`.
- **AC-6**: `code-review-N.md` sigue exactamente el mismo formato de
  encabezado YAML que `audit-N.md`/`test-report-N.md`
  (`status: approved|rejected`, `attempt: <n>`, `feedback:` lista),
  documentado en `AGENTS.md` sección "Formato de veredicto" (ampliada
  para nombrar los tres tipos de archivo).
- **AC-7**: El contrato común (`Assert-FeatureContract` en modo Feature
  y `Assert-WorkUnitContract -Mode Milestone`) exige que exista
  `code-review-N.md` no vacío en `runs/<NN>-<slug>/` (o
  `runs/milestone-<slug>/` en Milestone) cuyo **último intento por
  orden numérico real** tenga `status: approved` en su bloque YAML;
  si no existe ningún `code-review-N.md`, o el último por número
  real no está `approved`, o el bloque YAML es inválido/falta, el
  contrato lanza una excepción con diagnóstico claro (ver AC-16..AC-19
  del Eje 3, que definen el mecanismo compartido con `audit-N.md` y
  `test-report-N.md`).
- **AC-8**: `scripts/ready-for-pr.ps1` incluye `code-review-N.md` en la
  sección de evidencias del cuerpo de la PR (`$evidenceSection`), tanto
  en modo `Feature` como en modo `Milestone`.
- **AC-9**: `docs/tecnica/circuito-agentico.md` y
  `docs/usuario/circuito-agentico.md` describen el circuito con 5
  roles (`Analyst → Reviewer → Builder → QA → Code Reviewer`) y
  mencionan `code-review-N.md` como artefacto del circuito.

### Eje 2 — SDD (spec + plan + tasks)

- **AC-10**: `.agentic/roles/analyst-agent.md` se actualiza para que,
  además de `spec.md`, el rol produzca `plan.md` y `tasks.md` como
  parte estándar de su output en toda invocación futura del circuito
  (no solo para esta feature puntual). El archivo documenta el formato
  esperado de ambos (ver AC-13/AC-14) y aclara que `spec.md` sigue
  siendo estrictamente QUÉ+POR QUÉ, sin detalle de implementación —
  ese detalle va en `plan.md`.
- **AC-11**: `.agentic/roles/reviewer-agent.md` se actualiza para
  auditar los tres artefactos (`spec.md` + `plan.md` + `tasks.md`)
  juntos: agrega a la checklist verificar coherencia entre los tres
  (el plan no contradice el alcance de la spec, las tasks cubren todos
  los criterios de aceptación de la spec y no inventan alcance nuevo),
  y trazabilidad explícita requisito→plan→tarea (cada AC de la spec
  debe poder rastrearse hasta al menos una sección del plan y al menos
  una task). Mantiene sin cambios los rechazos automáticos ya vigentes
  (docs, decision, índices, stack no autorizado, contenido de negocio
  inventado).
- **AC-12**: `.agentic/roles/reviewer-agent.md` sección "Modo
  MILESTONE" se actualiza para aclarar que `plan.md`/`tasks.md` son
  también únicos para todo el work unit, pero deben cubrir cada item
  del manifest individualmente (misma exigencia que ya aplica a los
  criterios de aceptación y casos borde del `spec.md`).
- **AC-13**: El contrato común exige `plan.md` y `tasks.md` no vacíos
  en `runs/<NN>-<slug>/` (modo Feature) y en `runs/milestone-<slug>/`
  (modo Milestone, un único par para todo el work unit), usando la
  misma función `Assert-NonEmptyFile` ya usada para `spec.md`. Falta de
  cualquiera de los dos hace fallar `Assert-FeatureContract`/
  `Assert-WorkUnitContract` con un mensaje que identifica el archivo
  faltante.
- **AC-14**: Existe al menos un test automatizado (pytest sobre
  `scripts/feature-contract.ps1`) que reproduce: contrato falla si
  falta `plan.md`; contrato falla si falta `tasks.md`; contrato pasa
  cuando ambos existen y no están vacíos junto con el resto de
  artefactos requeridos (incluyendo los nuevos de Eje 1/Eje 3). Debe
  cubrir modo Feature y modo Milestone.

### Eje 3 — Bugs del contrato y del cierre

- **AC-15**: `scripts/feature-contract.ps1` reemplaza el uso de
  `Get-FirstExistingArtifact` (orden lexicográfico) para
  `audit-*.md`, `test-report-*.md` y `code-review-*.md` por una
  función nueva que: (a) enumera los archivos que matchean
  `^<prefijo>-(\d+)\.md$` en el directorio del run; (b) selecciona el
  de mayor número entero (no lexicográfico) — con un test que confirma
  que `audit-10.md` se reconoce como posterior a `audit-2.md`; (c) lee
  el archivo y extrae el primer bloque delimitado por ```` ```yaml ````
  / ```` ``` ````; (d) dentro de ese bloque, exige exactamente una línea
  `status: approved` o `status: rejected` y exactamente una línea
  `attempt: <n>`; (e) exige que `<n>` coincida exactamente con el
  número del nombre de archivo; (f) si el status del último intento
  (por número real) es `rejected`, si falta el bloque YAML, si falta
  `status`, si falta `attempt`, o si `attempt` no coincide con el
  número del archivo, el contrato lanza una excepción con mensaje que
  identifica la ruta exacta del archivo y la causa concreta del
  rechazo (uno de: "sin bloque YAML", "status ausente/invalido",
  "attempt ausente/no numerico", "attempt no coincide con el nombre de
  archivo", "ultimo intento rejected").
- **AC-16**: Existen tests que reproducen explícitamente el escenario
  descripto en la auditoría: `audit-1.md` con `status: rejected` seguido
  de `audit-2.md` vacío o inexistente ya NO pasa el contrato (antes sí
  pasaba); un `audit-10.md` aprobado junto con un `audit-2.md`
  rechazado hace pasar el contrato porque el intento numéricamente más
  reciente (10) es el que cuenta, no el orden alfabético.
- **AC-17**: Existe al menos un test que confirma que un `audit-N.md`
  (o `test-report-N.md`/`code-review-N.md`) sin bloque ```` ```yaml ````,
  o con `attempt:` que no coincide con `N` en el nombre de archivo, hace
  fallar el contrato con un mensaje de error que un humano puede
  entender sin leer el código fuente del script.
- **AC-18**: `New-DecisionFile` (en `scripts/feature-contract.ps1`) ya
  no escribe la línea "MERGE aprobado por evidencias del circuito
  agéntico." Escribe en su lugar una sección "Estado" que dice algo
  equivalente a "Estado técnico: ready_for_pr" y aclara explícitamente
  que la aprobación de merge es exclusivamente del HITL vía GitHub
  (ni el circuito agéntico ni `decision.md` la otorgan). La sección
  "Evidencias revisadas" generada incluye referencias a `plan.md`,
  `tasks.md` y `code-review-1.md` además de `spec.md`, `audit-1.md`,
  `test-report-1.md`.
- **AC-19**: Existe un test que verifica que el contenido generado por
  `New-DecisionFile` no contiene la cadena "MERGE aprobado" ni ninguna
  afirmación de que la PR fue mergeada, y sí contiene una referencia
  explícita a que el merge depende de HITL/GitHub.
- **AC-20**: `scripts/close-feature.ps1`, en modo `Feature` y en modo
  `Milestone`, cuando el estado local ya es `already-closed`
  (ROADMAP.md local ya tiene `[x]` para el slug/todos los items), ya no
  se salta directamente a la verificación final: antes de esa
  verificación hace `git fetch origin $baseBranch` y compara
  `ROADMAP.md` en `origin/$baseBranch` contra el estado esperado. Si
  el remoto YA tiene el cierre (`[x]` sin `[-]` para el slug/todos los
  items), no hace nada más (no crea commit, no pushea). Si el remoto
  TODAVÍA no tiene el cierre (commit local pendiente de push), hace
  `git push origin $baseBranch` del commit ya existente antes de
  continuar a la verificación final. La operación es idempotente:
  reejecuciones consecutivas no fallan y no crean commits vacíos ni
  duplicados.
- **AC-21**: Existe un test (o secuencia de tests) que reproduce el
  escenario exacto reportado: (1) primera ejecución de
  `close-feature.ps1` cambia `[-]` a `[x]` localmente y commitea, pero
  el push subsiguiente falla (simulado, p. ej. remoto no accesible o
  rechazado); (2) una segunda ejecución del mismo script, con el mismo
  estado local (`ROADMAP.md` local ya en `[x]`, commit ya creado, remoto
  todavía en `[-]`), completa exitosamente: detecta que el remoto no
  tiene el cierre, pushea el commit pendiente, y la verificación final
  contra `origin/$baseBranch` pasa. Debe existir un test equivalente
  para modo `Milestone` (con todos los items).
- **AC-22**: Existe un test que confirma que ejecutar
  `close-feature.ps1` dos veces seguidas cuando el remoto YA tiene el
  cierre completo no falla, no crea un commit adicional, y no intenta
  pushear de nuevo (o si pushea, el push es un no-op sin error porque
  no hay nada nuevo).
- **AC-23**: Existen `.agentic/schemas/agents.schema.json` y
  `.agentic/schemas/models.schema.json`, JSON Schema válido (Draft
  2020-12 o el draft que declare `plan.md`), que describen realmente la
  forma de `.agentic/agents.json` y `.agentic/models.json`
  respectivamente (campos obligatorios: `roles`, cada rol con
  `description`, `prompt`, `claude`, `codex`, `opencode`; para
  `models.json`: `validVariants`, `fallbackAliases`, `providers`,
  `roles`). `.agentic/agents.json` y `.agentic/models.json` siguen
  referenciando `./schemas/agents.schema.json` y
  `./schemas/models.schema.json` respectivamente, y esa referencia ya
  no está rota (el archivo existe en esa ruta relativa a `.agentic/`).
- **AC-24**: Existe al menos un test automatizado que valida realmente
  `.agentic/agents.json` contra `.agentic/schemas/agents.schema.json`
  y `.agentic/models.json` contra
  `.agentic/schemas/models.schema.json` (validación estructural real,
  no solo "el archivo existe"), y al menos un test negativo por schema
  que confirma que un documento deliberadamente inválido (por ejemplo,
  un rol sin `description`, o `models.json` sin `providers`) falla la
  validación.
- **AC-25**: Existe `.agentic/schemas/work-unit.schema.json` que
  describe la forma fija del manifest de milestone documentada en
  `scripts/workunit-lib.ps1` (`Read-WorkUnitManifest`/
  `Write-WorkUnitManifest`): `schemaVersion` (entero, `1`), `mode`
  (string, `"milestone"`), `slug` (string, patrón slug en minúsculas
  sin prefijo numérico), `items` (array no vacío de strings con
  patrón `NN-slug-en-minusculas`). Existe al menos un test que valida
  un manifest real (por ejemplo, uno generado por
  `Write-WorkUnitManifest` en un test existente, o un fixture
  equivalente) contra ese schema, y al menos un test negativo (por
  ejemplo `items` vacío, o `mode` distinto de `"milestone"`) que falla
  la validación.
- **AC-26**: `docs/tecnica/arquitectura.md` documenta como una sección
  `## Decisión: ...` nueva la incorporación de una dependencia de test
  (`jsonschema` para Python, u otra que el `plan.md` elija) usada
  exclusivamente para validar los schemas del Eje 3, dejando explícito
  que es tooling del propio circuito (paralelo a `pytest`, ya exigido
  en `AGENTS.md`), no stack de producto.
- **AC-27**: `ROADMAP.md`, en su encabezado (la línea que hoy dice
  "...circuito agéntico de AGENTS.md: Analyst → Reviewer → Builder →
  QA → ..."), se actualiza para no contradecir el nuevo orden descrito
  en `AGENTS.md` (agrega `Code Reviewer` al flujo enumerado).

### Obligatorios en todo spec (sin excepción)

- **AC-28**: Debe existir `docs/tecnica/code-reviewer-y-sdd.md`, no
  vacío, con las decisiones de diseño/implementación relevantes de
  esta feature (nuevo agente, SDD, y los 3 bugs corregidos).
- **AC-29**: Debe existir `docs/usuario/code-reviewer-y-sdd.md`, no
  vacío, con el propósito de la feature y cómo verla/usarla (qué
  cambia para quien opera el circuito: nuevo agente, nuevos archivos
  `plan.md`/`tasks.md`/`code-review-N.md`, nuevo orden).
- **AC-30**: Debe existir `runs/v1.1.0/01-code-reviewer-y-sdd/decision.md`, no
  vacío, con decisiones demostrables desde spec/plan/tasks/auditoría/
  implementación (no ornamental, no afirma aprobación de merge — ver
  AC-18).
- **AC-31**: `docs/tecnica/index.md` contiene exactamente un enlace
  `- [Code Reviewer Y Sdd](code-reviewer-y-sdd.md)` (o el título que
  `Get-WorkUnitInfo` derive del slug) dentro de la zona
  `FEATURE_LINKS_START`/`FEATURE_LINKS_END`.
- **AC-32**: `docs/usuario/index.md` contiene exactamente un enlace
  equivalente al de AC-31 dentro de su propia zona
  `FEATURE_LINKS_START`/`FEATURE_LINKS_END`.

## Casos borde a contemplar

- Un `audit-N.md`/`test-report-N.md`/`code-review-N.md` con el bloque
  YAML presente pero `status` con un valor que no sea exactamente
  `approved` ni `rejected` (typo, mayúsculas distintas) debe tratarse
  como malformado, no como aprobado por default.
- Numeración no contigua de intentos (`audit-1.md`, `audit-3.md`, sin
  `audit-2.md`) — el contrato debe igual tomar el número más alto
  existente (`3`), no asumir secuencia perfecta.
- `code-review-N.md` ausente completamente (Code Reviewer nunca corrió)
  debe fallar el contrato igual que si faltara `audit-N.md` hoy.
- Reject de `code-reviewer-agent` después de que `qa-agent` ya había
  aprobado en un intento anterior: el circuito exige volver a pasar por
  QA si Builder tocó código/tests, no alcanza con que Code Reviewer
  vuelva a evaluar el mismo `test-report-N.md` viejo — esto es una
  regla de proceso (documentada en el rol y en AGENTS.md), no
  necesariamente hay forma de encodearla 100% en el contrato ejecutable
  sin comparar timestamps/hashes de commit; documentar la limitación
  explícitamente en `docs/tecnica/`.
- `close-feature.ps1`: el remoto (`origin/$baseBranch`) avanzó con
  OTROS commits (no relacionados) entre el commit local fallido y el
  reintento — el `git push` del commit pendiente debe seguir siendo
  válido si el commit local es fast-forward respecto al remoto
  actualizado; si no lo es (alguien reescribió historia), el script
  debe fallar con un mensaje claro, no forzar el push.
- `close-feature.ps1` en modo Milestone: estado remoto parcialmente
  cerrado (algunos items `[x]`, otros no) sigue siendo el caso
  irrecuperable automáticamente ya cubierto por
  `Assert-RoadmapItemsCanClose` — el fix del retry de push no debe
  alterar ese comportamiento existente.
- Validación de schema: un `agents.json`/`models.json` con campos
  adicionales no declarados en el schema — decidir explícitamente si
  el schema permite (`additionalProperties: true`) o prohíbe
  propiedades extra, y documentar la elección en `plan.md`.
- `sync-agentic-adapters.ps1 -Check` corriendo en CI (Linux) con
  `code-reviewer-agent` agregado — debe seguir funcionando sin
  diferencias de line endings/encoding respecto a los adaptadores ya
  generados para los otros 4 roles.
- Un `tasks.md` que declara una tarea sin trazabilidad explícita a
  ningún AC de `spec.md` — `reviewer-agent` debe rechazarlo
  automáticamente por la nueva regla de trazabilidad (AC-11).
- Milestone con items heterogéneos: `plan.md`/`tasks.md` únicos deben
  igual dejar explícito qué tareas corresponden a qué item del
  manifest, para que `builder-agent` no mezcle alcance entre items.

## Riesgos / supuestos

- **Nombre de los docs**: uso `docs/tecnica/code-reviewer-y-sdd.md` y
  `docs/usuario/code-reviewer-y-sdd.md` (sin el prefijo `01-`) porque
  es la convención ya implementada por `Get-WorkUnitInfo -Mode Feature`
  y ya usada por la feature `00-fuente-unica-router-modelos` →
  `fuente-unica-router-modelos.md`. El pedido original mencionaba
  literalmente `docs/tecnica/01-code-reviewer-y-sdd.md`; interpreto eso
  como una referencia informal del Main Agent al slug completo del
  run, no como una instrucción de romper la convención ya vigente en
  el código. Si el reviewer prefiere la forma literal con prefijo,
  es una corrección de una sola línea en `spec.md`/`plan.md`.
- **Modelo/esfuerzo de `code-reviewer-agent`**: reutilizo exactamente
  la misma clase de modelo, variante y cadena de fallback que
  `reviewer-agent` en `.agentic/agents.json`/`.agentic/models.json`,
  tal como pidió el Main Agent explícitamente ("reusar la misma clase
  de modelo/esfuerzo... sin inventar proveedor nuevo").
- **Nueva dependencia de test (`jsonschema` u otra librería de
  validación JSON Schema)**: la trato como tooling del propio circuito
  (paralelo a `pytest`, que `AGENTS.md` ya exige sin pasar por
  `docs/tecnica/arquitectura.md`), pero igual pido documentarla ahí
  como decisión explícita (AC-26) para no dejar ambigüedad frente a la
  regla dura de "no agregar dependencia de build sin decisión
  explícita". El `plan.md` debe elegir la librería concreta.
  Alternativa descartada: implementar un validador JSON Schema
  artesanal sin dependencia externa — la descarto porque el pedido es
  explícito en pedir "JSON Schemas reales... con validación real en
  tests, no ornamentales", y reinventar un motor de JSON Schema es más
  riesgo que agregar una librería de testing estándar.
- **`work-unit.schema.json` no se referencia desde dentro de los
  manifests que escribe `Write-WorkUnitManifest`** (no le agrego un
  campo `$schema` al JSON generado). Lo trato como un contrato de
  validación ejercido solo desde los tests, para no tocar el formato
  de archivo ya cubierto por tests existentes
  (`test_workunit_lib.py`, `test_start_work_unit.py`) y no arriesgar
  romper compatibilidad de un manifest ya committeado en algún
  Milestone en curso. Si el reviewer prefiere que el manifest
  autoreferencie su propio schema, es una extensión menor de
  `Write-WorkUnitManifest`.
- **Alcance de "revisar el diff después de QA"**: el circuito no tiene
  hoy un mecanismo automático que impida invocar `code-reviewer-agent`
  antes de que `qa-agent` haya aprobado (es una regla de secuencia
  documental, igual que hoy nada impide técnicamente invocar
  `builder-agent` antes que `reviewer-agent`). No agrego una
  verificación ejecutable nueva para esto porque sería inconsistente
  con el resto del circuito (que confía en el proceso descrito en
  `AGENTS.md`, no en gates técnicos intermedios); el contrato sí exige
  que el ARTEFACTO FINAL (`code-review-N.md` aprobado) exista antes de
  `READY_FOR_PR`, que es el gate real y verificable.
- **No agrego un mecanismo de "reset" de `test-report`/`code-review`
  attempts cuando Builder vuelve a tocar código**: sigo el mismo patrón
  ya existente para `audit-N.md`/`test-report-N.md` (numeración
  creciente manual por intento, sin invalidación automática de
  intentos previos). Ver caso borde correspondiente arriba.
- **Título derivado del slug para los índices de documentación**
  (AC-31/AC-32): uso el mismo algoritmo de capitalización por guiones
  que ya implementa `Get-WorkUnitInfo` (`code-reviewer-y-sdd` →
  "Code Reviewer Y Sdd"). No invento un título "más lindo" a mano
  porque el contrato (`Assert-IndexLink`) exige coincidencia exacta con
  `info.Title`, y ese es el valor que el script deriva automáticamente
  si no se pasa `-Title` explícito.
