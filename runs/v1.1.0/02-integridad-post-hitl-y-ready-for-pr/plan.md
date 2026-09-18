# Plan: Integridad post-HITL y ready-for-pr

Este plan describe el CÓMO para cada AC de `spec.md`. No repite el QUÉ
ni el POR QUÉ. Toda referencia `AC-N` remite a
`runs/v1.1.0/02-integridad-post-hitl-y-ready-for-pr/spec.md`.

## 1. Arquitectura afectada

Ningún cambio toca stack de producto (el template sigue sin código de
producto, `docs/tecnica/arquitectura.md` no requiere entrada nueva).
Todo el trabajo es sobre el motor del circuito agéntico:

- `scripts/complete-approved-pr.ps1` — núcleo de GAP A (AC-1, AC-2).
- `scripts/ready-for-pr.ps1` — núcleo de GAP B (AC-3, AC-4, AC-5) y de
  GAP C (AC-6, AC-7).
- `scripts/feature-contract.ps1` — **no se modifica su firma ni su
  lógica de validación**. Se reutiliza tal cual:
  `Assert-FeatureContract`/`Assert-WorkUnitContract` (invocadas sin
  `-RequireReadyRoadmap` para la validación temprana) y
  `Get-LatestVerdictArtifact` (ya dot-sourced en `ready-for-pr.ps1`,
  línea 12, vía `. (Join-Path $PSScriptRoot "feature-contract.ps1")`)
  para resolver el archivo real de evidencia.
- `scripts/workunit-lib.ps1` — no se modifica. `Assert-RoadmapItemsTransition`
  ya es transaccional para el estado de ROADMAP en sí (no muta, solo
  valida); el problema de GAP B era el orden de la validación de
  contrato *alrededor* de esa función, no la función en sí.
- `tests/test_complete_approved_pr_script.py`,
  `tests/test_feature_contract_scripts.py` — extendidos con los nuevos
  casos (AC-8, AC-9, AC-10) preservando los existentes (AC-11).

No se toca `scripts/local-feature-reconcile.ps1`,
`scripts/start-work-unit.ps1`, `scripts/wait-pr-ci.ps1`,
`scripts/update-doc-indexes.ps1`, `scripts/close-feature.ps1`,
`scripts/resolve-agentic-model.ps1`, `.agentic/*`, ni
`.github/workflows/*.yml` — ningún AC de esta spec lo requiere.

## 2. Componentes y contratos nuevos/modificados

### 2.1 GAP A — `scripts/complete-approved-pr.ps1` (AC-1, AC-2)

- **Contrato de `gh pr view`**: agregar `headRefOid` a la lista de
  campos `--json` ya pedida (`number,state,baseRefName,headRefName,url,reviewDecision`
  → agregar `headRefOid`). El objeto `$pr` resultante expone
  `$pr.headRefOid` como el SHA del commit actual del head de la PR.
- **Nueva función `Get-LatestApprovedReviewCommit`** (o nombre
  equivalente), ubicada junto a las demás funciones auxiliares del
  script (antes del bloque de ejecución principal, mismo estilo que
  `Wait-PrChecks`/`Format-Checks`):
  - Recibe `$GitHubCliPath` y el número de PR.
  - Invoca `gh api repos/:owner/:repo/pulls/{n}/reviews --paginate`
    (usar `Invoke-Gh` ya existente, reutilizando su manejo de
    exit codes/errores) para cubrir el caso borde de paginación.
  - Parsea el JSON resultante (array de reviews), filtra por
    `state -eq "APPROVED"`, ordena por `submitted_at` descendente y
    devuelve el `commit_id` de la primera (más reciente). Si el
    conjunto filtrado está vacío, devuelve `$null` (caso borde
    defensivo de spec).
- **Nueva validación en el flujo principal**, inmediatamente después de
  la comprobación existente `$pr.reviewDecision -ne "APPROVED"` (línea
  ~293-295 actual) y antes de `Wait-PrChecks`:
  - Llamar a `Get-LatestApprovedReviewCommit`.
  - Si devuelve `$null` o el `commit_id` obtenido no coincide con
    `$pr.headRefOid`: escribir `post-hitl-gate-N.md` con
    `Write-GateReport -Status "rejected"` y feedback que indique
    explícitamente "la aprobación humana quedó obsoleta tras un push
    posterior a la PR; se requiere que el humano vuelva a aprobar la
    revisión vigente (commit `$($pr.headRefOid)`), no un cambio de
    builder-agent" (AC-1). Respetar el flag `-CommentOnFailure` ya
    existente para comentar en la PR, igual que en el camino de checks
    fallidos. Terminar con `throw` (mismo patrón que el resto del
    script) sin invocar `gh pr merge`.
  - Si coincide: continuar el flujo existente sin cambios (AC-2).

### 2.2 GAP B — `scripts/ready-for-pr.ps1` (AC-3, AC-4, AC-5)

- **Reordenar, no reescribir, la secuencia de validación.** El diseño
  aprovecha que `Assert-FeatureContract`/`Assert-WorkUnitContract` sin
  `-RequireReadyRoadmap` ya validan todo lo "caro" (decision.md, docs,
  índices, último veredicto aprobado) sin exigir el estado de
  `ROADMAP.md`. Nuevo orden dentro de cada rama de `Mode`:
  1. Guard clauses baratas ya existentes que **no mutan** nada
     (`ya figura como [x] → throw`, `ya está en READY_FOR_PR → log`,
     lectura de `$roadmap`) se mantienen donde están: son lectura pura.
  2. **Nueva llamada temprana**: `Assert-FeatureContract -Slug $Slug
     -Title $info.Title` (Feature) o `Assert-WorkUnitContract -Slug
     $Slug -Mode Milestone -Title $info.Title` (Milestone), **sin**
     `-RequireReadyRoadmap`, ejecutada antes de cualquier
     `Set-Content`/`git add`/`git commit` sobre `ROADMAP.md`. Si esta
     llamada lanza excepción, el script termina sin haber tocado
     `ROADMAP.md` (AC-3, AC-4).
  3. Solo si (2) no lanzó excepción: el bloque de mutación+commit ya
     existente (regex `.Replace`, `Set-Content`, `Invoke-Checked git
     add`/`git commit`) se ejecuta exactamente como hoy.
  4. La llamada final ya existente, `Assert-FeatureContract -Slug $Slug
     -Title $info.Title -RequireReadyRoadmap` (Feature) o
     `Assert-WorkUnitContract ... -RequireReadyRoadmap` (Milestone), se
     mantiene **después** de la mutación como confirmación de
     integridad post-mutación (detecta, por ejemplo, entradas
     duplicadas o ambiguas en `ROADMAP.md` que el reemplazo por regex
     no detectaría por sí solo). Esta llamada ya existe hoy; solo deja
     de ser la primera y única validación real.
  - Este diseño **no requiere cambiar la firma ni el cuerpo de
    `Assert-FeatureContract`/`Assert-WorkUnitContract`** en
    `scripts/feature-contract.ps1`: ambas ya soportan ejecutarse sin
    `-RequireReadyRoadmap` para cubrir exactamente el subconjunto de
    checks que debe correr antes de la mutación.
- **Milestone — caso "todos ya Ready"**: cuando `$readyItems.Count -eq
  $items.Count` (rama que hoy solo hace `Write-Host` sin mutar), la
  nueva llamada temprana de validación de contrato (paso 2) debe seguir
  ejecutándose igual, porque aunque no haya mutación de ROADMAP.md
  pendiente, sí puede haber push/creación de PR más adelante en el
  script que no debe proceder si el contrato está roto (caso borde de
  spec: "`ready-for-pr.ps1` re-ejecutado cuando `ROADMAP.md` ya está
  `[-]`").

### 2.3 GAP C — `scripts/ready-for-pr.ps1` (AC-6, AC-7)

- En el punto donde hoy se arma `$evidenceSection` (bloque `@"..."@`
  con los literales `audit-N.md`/`test-report-N.md`/`code-review-N.md`,
  tanto en la rama Milestone como en la rama Feature), resolver antes
  tres variables usando la función ya disponible:
  - `$auditArtifact = Get-LatestVerdictArtifact -Directory $info.RunDir -Prefix "audit"`
  - `$qaArtifact = Get-LatestVerdictArtifact -Directory $info.RunDir -Prefix "test-report"`
  - `$codeReviewArtifact = Get-LatestVerdictArtifact -Directory $info.RunDir -Prefix "code-review"`
  - Estas llamadas ocurren **después** de que la validación de contrato
    de la sección 2.2 ya pasó, por lo que los tres archivos existen y
    el último intento de cada uno ya es `approved`
    (`Assert-LatestVerdictApproved` corrió antes con éxito) — no hace
    falta repetir la validación de estado aprobado en este punto, solo
    resolver el path real.
  - Reemplazar los literales `$($info.RunDir)/audit-N.md`,
    `$($info.RunDir)/test-report-N.md`,
    `$($info.RunDir)/code-review-N.md` (ambas ramas, Feature y
    Milestone) por una referencia a la ruta relativa real del archivo
    resuelto.
  - **Corrección post-`code-review-1.md` (rejected):** este plan
    originalmente asumía, sin haberlo verificado contra el código real,
    que `Get-LatestVerdictArtifact.Path` ya devolvía una ruta relativa.
    Es falso: esa propiedad se construye con `$latest.File.FullName`, y
    `System.IO.FileInfo.FullName` en .NET/PowerShell siempre devuelve
    una ruta absoluta. Interpolar `$($auditArtifact.Path)` /
    `$($qaArtifact.Path)` / `$($codeReviewArtifact.Path)` directamente
    filtraba esa ruta absoluta al cuerpo público de la PR (caso borde de
    encoding/rutas en spec.md: "sin rutas absolutas del entorno del
    agente"). La implementación final NO cambia
    `Get-LatestVerdictArtifact` (para no afectar a
    `Assert-LatestVerdictApproved`, su otro consumidor); en su lugar,
    `ready-for-pr.ps1` recompone la ruta relativa en el punto de uso:
    `"$($info.RunDir)/$(Split-Path -Leaf $auditArtifact.Path)"` (y
    análogas para QA/code review), y son esas variables (`$auditPath`,
    `$qaPath`, `$codeReviewPath`) las que se interpolan en
    `$evidenceSection` y en el checklist.
  - Milestone usa el mismo `$info.RunDir` (`runs/milestone-<slug>/`) —
    un único set de veredictos a nivel de work unit, tal como ya lo
    trata `Assert-WorkUnitContract` para Milestone.

## 3. Compatibilidad y migración

No hay datos ni artefactos existentes que migrar:

- El formato de `ROADMAP.md`, `decision.md`, `audit-N.md`,
  `test-report-N.md`, `code-review-N.md` y los manifests de Milestone
  (`work-unit.json`) no cambian.
- PRs ya creadas antes de esta feature con el placeholder genérico en
  su cuerpo no se reescriben retroactivamente (explícitamente fuera de
  alcance en spec.md); solo las PRs creadas después de este cambio
  tienen el nuevo comportamiento.
- Aprobaciones humanas ya emitidas y ya mergeadas antes de esta feature
  no se re-evalúan: el chequeo de GAP A solo aplica a corridas futuras
  de `complete-approved-pr.ps1`.
- El reordenamiento de GAP B es puramente de secuencia de llamadas
  dentro de un mismo proceso de PowerShell (no cambia el formato de
  ningún archivo en disco), por lo que no hay incompatibilidad con
  ninguna corrida anterior ya completada.

## 4. Dependencias

No se agrega ninguna dependencia nueva:

- GAP A usa `gh api`, subcomando ya incluido en el mismo binario `gh`
  que `AGENTS.md` ya exige como herramienta local requerida (sección
  "Herramientas locales requeridas"). No se agrega ningún paquete de
  Python ni módulo de PowerShell nuevo.
- GAP B y GAP C reutilizan funciones PowerShell ya existentes en
  `scripts/feature-contract.ps1` sin agregar nada a
  `requirements-dev.txt` ni a ningún manifiesto de dependencias.
- Ningún cambio requiere una entrada nueva en
  `docs/tecnica/arquitectura.md` (no hay backend, base de datos,
  integración externa ni dependencia de build nueva).

## 5. Impacto operacional

- **Nuevo modo de falla visible para el humano**: si su aprobación
  queda stale, `post-hitl-merge-gate.yml` (que invoca
  `complete-approved-pr.ps1` con `-CommentOnFailure` en CI) comentará
  la PR indicando que debe volver a aprobar sobre el commit vigente.
  Esto no requiere que `builder-agent` haga ningún cambio de código; es
  una acción exclusiva del humano en la UI de GitHub (re-click en
  "Approve"). Se documenta en `docs/usuario/` para que quien opera el
  circuito entienda que este mensaje no significa "código roto".
- **`ready-for-pr.ps1` puede fallar más temprano que antes** en
  corridas donde el contrato está incompleto: antes dejaba un commit
  local con `ROADMAP.md` en `[-]` aunque el contrato fallara después;
  ahora falla sin dejar ningún commit, lo cual es estrictamente más
  seguro para quien reintenta el circuito (no hay que revertir nada
  manualmente).
- **El cuerpo de la PR es más útil para el revisor humano**: en vez de
  tener que adivinar qué número de intento fue el aprobado, el enlace
  en el cuerpo de la PR apunta directo al archivo real.
- No hay nuevos comandos ni flags de cara al usuario: las firmas de
  `scripts/complete-approved-pr.ps1` y `scripts/ready-for-pr.ps1`
  (parámetros) no cambian.

## 6. Estrategia de tests

- **GAP A (AC-1, AC-2, AC-8)** — `tests/test_complete_approved_pr_script.py`:
  - Extender `write_fake_gh` para responder también a `pr view --json
    ...,headRefOid` (agregar el campo al JSON ya devuelto por cada
    modo existente) y a una nueva invocación que matchee `pulls` y
    `reviews` en los argumentos (equivalente a `gh api
    repos/:owner/:repo/pulls/123/reviews`), devolviendo un array JSON
    de reviews con `commit_id`, `state`, `submitted_at`.
  - Nuevo modo `stale_approval`: `pr view` devuelve `headRefOid:
    "commitB"`, la consulta de reviews devuelve una única review
    `APPROVED` con `commit_id: "commitA"`. Verificar: `returncode != 0`,
    `"pr merge" not in log`, el reporte generado empieza con
    `status: rejected` y contiene una frase reconocible sobre
    aprobación obsoleta / nueva aprobación requerida. Cubre AC-1 y el
    caso borde "ninguna review coincide con el head".
  - Modo `success` existente (y los demás ya cubiertos) se extiende
    para que `pr view` también incluya `headRefOid` igual al
    `commit_id` de la única review `APPROVED` devuelta por el fake de
    reviews — así el camino feliz sigue probando merge real (AC-2,
    AC-11: no debilita `test_complete_approved_pr_merges_after_green_checks`
    ni `test_complete_approved_pr_is_rerunnable_after_checks_turn_green`).
  - Nuevo test para el caso borde "múltiples reviews, la más reciente
    `APPROVED` coincide con el head aunque una anterior no": el fake de
    reviews devuelve dos entradas `APPROVED` con `commit_id` distintos
    y `submitted_at` distintos; se verifica que el gate usa la de
    `submitted_at` más reciente.
- **GAP B (AC-3, AC-4, AC-9)** — `tests/test_feature_contract_scripts.py`:
  - Nuevo test basado en `prepare_ready_repo`, pero rompiendo un
    elemento del contrato (por ejemplo, eliminar `decision.md` o
    corromper `code-review-1.md` a `status: rejected`) antes de invocar
    `READY_FOR_PR`. Verificar: `returncode != 0`, `ROADMAP.md` en disco
    idéntico al commiteado (`- [ ] 99-demo-feature` sigue pendiente),
    y `git log` no tiene ningún commit nuevo ("docs: marcar ... como
    ready for pr") respecto del commit previo a la corrida.
  - Equivalente en modo Milestone (nuevo fixture análogo a
    `prepare_ready_repo` pero con `-Mode Milestone` y un manifest de 2+
    items, uno de ellos con doc técnica faltante): verificar que
    ningún item cambia de estado en `ROADMAP.md`.
  - Confirmar explícitamente (test dedicado o aserción agregada a los
    existentes) que `test_ready_for_pr_creates_pr_after_expected_missing_pr`
    y `test_ready_for_pr_reuses_existing_pr_without_duplicate` siguen
    en verde sin modificar sus aserciones (AC-11): ambos ya parten de
    un contrato completo (`make_contract_repo` + `New-DecisionFile` +
    `UPDATE_INDEXES`, commiteado antes de invocar `ready-for-pr.ps1`),
    por lo que el reordenamiento no debería afectar su resultado.
- **GAP C (AC-6, AC-7, AC-10)** — `tests/test_feature_contract_scripts.py`:
  - Extender `prepare_ready_repo` (o un fixture derivado) para dejar
    más de un intento de `audit-N.md`/`test-report-N.md`/
    `code-review-N.md` (por ejemplo `audit-1.md` rejected + `audit-2.md`
    approved) antes de correr `ready-for-pr.ps1` en el modo
    `missing_then_create`, y capturar el `--body-file` pasado a `gh pr
    create` (el fake de `gh` puede volcar su contenido a un archivo de
    log adicional, siguiendo el patrón de `FAKE_GH_LOG` de
    `test_complete_approved_pr_script.py`). Verificar que el body
    contiene `audit-2.md` (el intento real aprobado) y no contiene la
    subcadena literal `audit-N.md`.
  - Equivalente en modo Milestone.
- **Regresión general (AC-11)**: correr toda la suite `pytest tests/`
  al final de la implementación y confirmar 0 fallos, sin marcar
  ningún test existente como `xfail`/`skip` para lograrlo.
