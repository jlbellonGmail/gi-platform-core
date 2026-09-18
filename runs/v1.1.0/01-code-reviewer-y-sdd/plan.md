# Plan: Code Reviewer agent + SDD + correcciones de contrato

Este plan describe el CÓMO para cada AC de `spec.md`. No repite el QUÉ
ni el POR QUÉ (eso vive en `spec.md`). Toda referencia `AC-N` remite a
`runs/v1.1.0/01-code-reviewer-y-sdd/spec.md`.

## 1. Arquitectura afectada

Ningún cambio toca stack de producto: este template no tiene código de
producto (`docs/tecnica/arquitectura.md` así lo declara). Todo el
trabajo es sobre el motor del circuito agéntico
(`scripts/*.ps1`, `.agentic/`, `AGENTS.md`, `docs/`, `tests/`).
Componentes afectados:

- `scripts/feature-contract.ps1` — núcleo de los cambios de Eje 2/Eje 3.
- `scripts/close-feature.ps1` — fix de retry de push (Eje 3, AC-20/21/22).
- `scripts/ready-for-pr.ps1` — evidencia de PR (AC-8), sin cambios de
  lógica de contrato (delega en `Assert-FeatureContract`/
  `Assert-WorkUnitContract`, que ya incorporan los nuevos requisitos).
- `.agentic/agents.json`, `.agentic/models.json` — nueva entrada de rol
  (AC-2, AC-3) + `$schema` ahora resoluble (AC-23).
- `.agentic/roles/code-reviewer-agent.md` (nuevo, AC-1),
  `.agentic/roles/analyst-agent.md` (AC-10),
  `.agentic/roles/reviewer-agent.md` (AC-11, AC-12).
- `.agentic/schemas/agents.schema.json`,
  `.agentic/schemas/models.schema.json`,
  `.agentic/schemas/work-unit.schema.json` (nuevos, AC-23/AC-25).
- `AGENTS.md`, `ROADMAP.md` (encabezado), `docs/tecnica/circuito-agentico.md`,
  `docs/usuario/circuito-agentico.md`, `.agentic/README.md`,
  `docs/tecnica/arquitectura.md` (AC-5, AC-9, AC-26, AC-27).
- `requirements-dev.txt` (AC-26: agrega `jsonschema`).
- `tests/*.py` — nuevos y ampliados (ver sección 6).

No se toca `scripts/complete-approved-pr.ps1`,
`scripts/local-feature-reconcile.ps1`, `scripts/start-work-unit.ps1`,
`scripts/wait-pr-ci.ps1`, `scripts/update-doc-indexes.ps1`,
`scripts/resolve-agentic-model.ps1`, ni `.github/workflows/*.yml` — no
hay AC que lo requiera. `scripts/sync-agentic-adapters.ps1` no necesita
cambios de lógica (AC-4): ya deriva agentes de
`agents.roles.PSObject.Properties`; solo se regenera con la nueva
entrada de `agents.json`.

## 2. Componentes y contratos nuevos/modificados

### 2.1 `code-reviewer-agent` (Eje 1)

- Nuevo archivo `.agentic/roles/code-reviewer-agent.md` (AC-1),
  redactado con la misma estructura que `.agentic/roles/reviewer-agent.md`:
  intro de responsabilidad, "Checklist de auditoría" (técnica, no de
  spec), "Tu output: code-review-N.md", "Modo MILESTONE".
- `.agentic/agents.json`: agregar bloque `roles.code-reviewer-agent`
  copiando la forma exacta de `roles.reviewer-agent` (AC-2), cambiando
  solo `description` y `prompt`.
- `.agentic/models.json`: agregar bloque `roles.code-reviewer-agent`
  copiando byte a byte el contenido de `roles.reviewer-agent` (AC-3).
- Regenerar adaptadores: `scripts/sync-agentic-adapters.ps1` (sin
  `-Check`), luego confirmar con `-Check` (AC-4). No tocar manualmente
  ningún archivo bajo `.claude/agents/`, `.codex/`, `opencode.json`.

### 2.2 `code-review-N.md` como artefacto de contrato (Eje 1 + Eje 3)

Contrato: mismo bloque YAML de veredicto documentado en `AGENTS.md`
("Formato de veredicto"), reutilizado sin cambios de forma — solo se
amplía la sección para nombrar `code-review-N.md` junto a `audit-N.md`
y `test-report-N.md` (AC-6).

### 2.3 Parseo de veredicto y selección de último intento (Eje 3, núcleo)

Nueva función en `scripts/feature-contract.ps1`:

```powershell
function Get-LatestVerdictArtifact {
    param(
        [Parameter(Mandatory = $true)] [string] $Directory,
        [Parameter(Mandatory = $true)] [string] $Prefix   # "audit" | "test-report" | "code-review"
    )
    # 1. Enumera archivos "$Prefix-<N>.md" en $Directory (regex ancla
    #    inicio/fin: "^$Prefix-(\d+)\.md$" sobre el nombre de archivo,
    #    no sobre la ruta completa).
    # 2. Si no hay ninguno, throw "Falta al menos un $Prefix-N.md en $Directory."
    # 3. Selecciona el de mayor [int] N (Sort-Object { [int]$_.Number } -Descending
    #    | Select-Object -First 1) -- NO Sort-Object Name.
    # 4. Lee el contenido, extrae el primer bloque ```yaml ... ``` con
    #    una regex multilinea simple (sin parser YAML completo: basta
    #    con extraer el contenido entre fences y aplicar 2 regex de
    #    linea, "^\s*status:\s*(\S+)\s*$" y "^\s*attempt:\s*(\d+)\s*$").
    # 5. Valida: bloque yaml presente (si no, throw con la ruta exacta
    #    y "no tiene bloque ```yaml"); status con match unico (si no,
    #    throw "status ausente o invalido"); attempt con match unico y
    #    numerico (si no, throw "attempt ausente o no numerico");
    #    attempt == N del nombre de archivo (si no, throw "attempt no
    #    coincide con el nombre de archivo: esperado N, encontrado attempt").
    # 6. Devuelve [pscustomobject]@{ Path; Attempt; Status }.
}

function Assert-LatestVerdictApproved {
    param(
        [Parameter(Mandatory = $true)] [string] $Directory,
        [Parameter(Mandatory = $true)] [string] $Prefix,
        [Parameter(Mandatory = $true)] [string] $Label   # para mensajes, ej. "auditoria", "QA", "code review"
    )
    $artifact = Get-LatestVerdictArtifact -Directory $Directory -Prefix $Prefix
    Assert-NonEmptyFile $artifact.Path
    if ($artifact.Status -ne "approved") {
        throw "El ultimo intento de $Label ($($artifact.Path), attempt $($artifact.Attempt)) no esta approved (status: $($artifact.Status))."
    }
    return $artifact
}
```

`Assert-WorkUnitContract` (modo `Feature` y modo `Milestone`) reemplaza
las llamadas actuales a `Get-FirstExistingArtifact` + `Assert-NonEmptyFile`
para `audit-*.md` y `test-report-*.md` por:

```powershell
Assert-LatestVerdictApproved -Directory $info.RunDir -Prefix "audit" -Label "auditoria"
Assert-LatestVerdictApproved -Directory $info.RunDir -Prefix "test-report" -Label "QA"
Assert-LatestVerdictApproved -Directory $info.RunDir -Prefix "code-review" -Label "code review"
```

`Get-FirstExistingArtifact` se elimina de `scripts/feature-contract.ps1`
si, tras el cambio, no queda ningún otro llamador (confirmado por grep:
hoy solo se usa ahí, para `audit-*.md`/`test-report-*.md`). Si el
builder detecta otro uso al implementar, lo deja y lo documenta en
`docs/tecnica/code-reviewer-y-sdd.md` en vez de asumir.

### 2.4 `New-DecisionFile` (Eje 3, AC-18)

Reemplazar el bloque de líneas:

```
"## Estado"
""
"MERGE aprobado por evidencias del circuito agéntico."
```

por:

```
"## Estado"
""
"Estado tecnico: ready_for_pr."
""
"La aprobacion de merge es exclusivamente del HITL en GitHub sobre la PR."
"Este documento no otorga ni implica esa aprobacion."
```

y ampliar "Evidencias revisadas" agregando `plan.md`, `tasks.md` y
`code-review-1.md` a la lista ya existente (`spec.md`, `audit-1.md`,
`test-report-1.md`), sin volverlos dinámicos (mismo criterio que el
código actual: lista fija de nombres de primer intento, documentando la
limitación si ya no aplica).

### 2.5 `close-feature.ps1` — fix de retry de push (Eje 3, AC-20/21/22)

En ambos bloques (`Feature` y `Milestone`), cuando
`Assert-RoadmapCanClose`/`Assert-RoadmapItemsCanClose` devuelve
`"already-closed"`, agregar antes del bloque de "Verificando cierre
publicado":

```powershell
if ($closeState -eq "already-closed") {
    Write-Host "==> ... ya esta marcada [x] localmente. Verificando si el push esta pendiente..."
    Invoke-Checked "git" @("fetch", "origin", $baseBranch)
    $remoteRoadmap = Get-CheckedOutput "git" @("show", "origin/$baseBranch`:ROADMAP.md")
    $remoteClosed = <misma comprobacion que Assert-RoadmapClosedOnce / Assert-RoadmapItemsClosedOnce, pero sin throw -- version "Test-" que devuelve bool>
    if (-not $remoteClosed) {
        Write-Host "==> El remoto todavia no tiene el cierre. Pusheando commit local pendiente..."
        Invoke-Checked "git" @("push", "origin", $baseBranch)
    }
    else {
        Write-Host "==> El remoto ya tiene el cierre. Nada que pushear."
    }
}
else {
    # ... bloque de commit+push existente, sin cambios ...
}
```

Se agrega una función helper `Test-RoadmapClosedOnce`/
`Test-RoadmapItemsClosedOnce` (variantes booleanas de las
`Assert-*` existentes, o se reutilizan las `Assert-*` envueltas en
`try/catch` — decisión de implementación libre para el builder, con
la única restricción de no duplicar la regex de estado). El bloque de
"Verificando cierre publicado en origin/$baseBranch" que ya existe al
final del script queda intacto y sigue siendo la verificación final
autoritativa (para no relajar la garantía ya existente).

No se cambia el comportamiento cuando `$closeState -ne "already-closed"`
(caso normal, ya pushea).

### 2.6 Schemas JSON (Eje 3, AC-23/24/25/26)

- `.agentic/schemas/agents.schema.json`: JSON Schema (declarar
  `"$schema": "https://json-schema.org/draft/2020-12/schema"`) que
  exige `roles` como objeto con al menos una propiedad, cada valor con
  `description` (string), `prompt` (string), `claude` (objeto con
  `tools` array de string, `model` string, `effort` string), `codex`
  (objeto con `model`, `model_reasoning_effort`), `opencode` (objeto
  con `mode`, `model`, `reasoningEffort`, `permission` objeto). Decidir
  `additionalProperties` explícitamente (recomendado: `true` a nivel
  raíz de cada rol para no romper con campos futuros menores, `false`
  dentro de `claude`/`codex`/`opencode` para detectar typos reales —
  documentar la elección en `docs/tecnica/code-reviewer-y-sdd.md`).
- `.agentic/schemas/models.schema.json`: exige `validVariants` (array
  no vacío de string), `fallbackAliases` (objeto), `providers` (objeto
  no vacío, cada valor con `credentialEnv` array y `models` array no
  vacío), `roles` (objeto no vacío, cada valor con `default` — objeto
  con `model`/`variant` — y `fallback` — array no vacío de objetos con
  `label`/`model`/`variant`).
- `.agentic/schemas/work-unit.schema.json`: exige `schemaVersion`
  (integer, `const: 1`), `mode` (`const: "milestone"`), `slug` (string,
  patrón `^[a-z0-9]+(-[a-z0-9]+)*$`), `items` (array, `minItems: 1`,
  cada item string con patrón `^[0-9]{2}-[a-z0-9]+(-[a-z0-9]+)*$`).
- Dependencia de validación: agregar `jsonschema` a
  `requirements-dev.txt` (versión fijada con `>=` igual que `pytest`).
  Documentar en `docs/tecnica/arquitectura.md` como decisión nueva
  (AC-26): qué se agrega, por qué ahora, por qué este enfoque (validar
  JSON Schema real en vez de asserts manuales) y qué sigue igual
  (ningún stack de producto).

## 3. Compatibilidad y migración

- El repo solo tiene una feature cerrada (`00-fuente-unica-router-modelos`,
  `[x]`) y esta feature en curso (`01-code-reviewer-y-sdd`). No hay
  ningún run en estado intermedio (`READY_FOR_PR` o activo) que se
  rompa por el endurecimiento del contrato: nadie más está corriendo
  `ready-for-pr.ps1`/`close-feature.ps1` sobre un run viejo sin
  `plan.md`/`tasks.md`/`code-review-N.md`.
- Esta misma feature (`01-code-reviewer-y-sdd`) debe cumplir el
  contrato nuevo que ella misma introduce: `builder-agent` debe crear
  `runs/v1.1.0/01-code-reviewer-y-sdd/code-review-1.md` con veredicto
  `approved` (producido por la primera invocación real del nuevo
  `code-reviewer-agent`) antes de que `ready-for-pr.ps1` pueda
  ejecutarse para esta feature. Esto es intencional: valida el circuito
  nuevo usándolo sobre sí mismo.
- No hay cambio de formato en `spec.md` existente de features futuras:
  se agregan dos archivos nuevos (`plan.md`, `tasks.md`), no se cambia
  la forma de `spec.md`.
- El manifest `work-unit.json` no cambia de forma (no se le agrega
  `$schema`), así que ningún Milestone en curso (no hay ninguno activo
  hoy) se ve afectado.

## 4. Dependencias

- Nueva dependencia de test: `jsonschema` (Python), agregada a
  `requirements-dev.txt`. Ninguna dependencia de producto — este
  template no tiene código de producto.
- No se agrega ningún módulo PowerShell externo: el parseo YAML
  simplificado (sección 2.3) se implementa con regex nativas de
  PowerShell, sin `ConvertFrom-Yaml` ni módulos de terceros, porque el
  formato del bloque de veredicto es deliberadamente simple (2 líneas
  clave-valor conocidas) y no requiere un parser YAML completo.

## 5. Impacto operacional

- `builder-agent` de aquí en adelante debe, para cada feature nueva,
  escribir `code-review-N.md` recién después de que `qa-agent` aprobó,
  y solo después de que `code-reviewer-agent` (nuevo subagente) corrió
  sobre el diff final. Esto agrega una etapa más al circuito, con su
  correspondiente vuelta posible a `builder-agent` si rechaza.
- `ready-for-pr.ps1` no cambia su interfaz (mismos parámetros
  `-Slug`/`-Title`/`-Mode`), solo se endurece lo que
  `Assert-FeatureContract`/`Assert-WorkUnitContract` exige antes de
  dejar pasar a la creación de la PR.
- `close-feature.ps1` no cambia su interfaz tampoco; el fix es interno.
- Ningún workflow de GitHub Actions (`ci.yml`,
  `post-hitl-merge-gate.yml`, `post-merge-close-feature.yml`) necesita
  cambios: siguen invocando los mismos scripts con los mismos
  parámetros; el contrato más estricto se aplica transparentemente.

## 6. Estrategia de tests

- `tests/test_feature_contract_scripts.py` (existente): actualizar los
  fixtures que hoy escriben `audit-1.md`/`test-report-1.md` con
  contenido plano (`"status: approved\n"`) para que usen el formato
  real con fence ```` ```yaml ```` y `attempt: 1` coincidente. Agregar
  fixtures para `plan.md`, `tasks.md`, `code-review-1.md` en los
  helpers de "run completo válido" ya existentes, para no romper los
  tests de camino feliz.
- Nuevos tests en `tests/test_feature_contract_scripts.py` (o un
  archivo nuevo `tests/test_feature_contract_verdict_parsing.py` si el
  builder prefiere separar por legibilidad):
  - orden numérico real (`audit-10.md` aprobado + `audit-2.md`
    rechazado → contrato pasa; caso inverso → falla con el mensaje
    esperado);
  - último intento rechazado con intento previo aprobado → falla;
  - archivo sin bloque yaml → falla con mensaje identificable;
  - `attempt` no coincide con el nombre de archivo → falla;
  - falta `plan.md`/`tasks.md`/`code-review-N.md` → falla cada uno por
    separado con mensaje que identifica el archivo faltante.
- `tests/test_milestone_contract.py` (existente): mismas
  actualizaciones de fixtures, mismos casos de orden numérico /
  malformado, aplicados a la ruta Milestone.
- `tests/test_close_feature_script.py` (existente): agregar el
  escenario de "commit local ya en `[x]`, remoto todavía en `[-]`,
  push pendiente" simulando el fallo de push (por ejemplo, con un
  remoto local `git` cuyo estado se manipula directamente en el
  fixture, o con un segundo repo bare como remoto real de test si el
  archivo ya usa ese patrón — revisar el fixture existente antes de
  decidir el mecanismo concreto) y confirmando que una segunda
  ejecución completa el push y pasa la verificación final. Agregar
  también el caso "reejecución cuando el remoto ya está cerrado" (no
  debe fallar ni reintentar push).
- `tests/test_milestone_close_feature.py` (existente): mismo escenario
  de retry de push, para el modo Milestone.
- `tests/test_agentic_sync_scripts.py` (existente): agregar
  verificación de que, tras `sync-agentic-adapters.ps1`, existe
  `.claude/agents/code-reviewer-agent.md` con `tools: Read, Grep, Glob`
  y sin `Write`/`Edit`/`Bash`, y que `-Check` sigue pasando.
- Nuevo test (Python, sin pytest de PowerShell) para los schemas JSON:
  `tests/test_agentic_schemas.py` — valida `.agentic/agents.json`
  contra `.agentic/schemas/agents.schema.json`,
  `.agentic/models.json` contra
  `.agentic/schemas/models.schema.json`, y al menos un manifest de
  Milestone (real o fixture) contra
  `.agentic/schemas/work-unit.schema.json`, con un caso positivo y un
  caso negativo por schema usando `jsonschema.validate` /
  `jsonschema.exceptions.ValidationError`.
- QA corre la suite completa (`pytest tests/`) además de los nuevos
  tests, como ya exige `.agentic/roles/qa-agent.md`.
