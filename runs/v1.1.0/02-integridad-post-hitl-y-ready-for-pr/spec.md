# Spec: Integridad post-HITL y ready-for-pr

## Alcance

Incluye:

1. **GAP A — aprobación HITL vinculada al commit vigente de la PR.**
   `scripts/complete-approved-pr.ps1` debe rechazar (fallar cerrado, sin
   mergear) cuando la aprobación humana más reciente (`reviewDecision:
   APPROVED`) fue emitida contra un commit anterior al `headRefOid`
   actual de la PR ("aprobación stale"), típicamente porque
   `builder-agent` pusheó un fix después de que el humano aprobó. El
   gate debe obtener el commit real sobre el que se emitió la última
   review `APPROVED` (vía `gh api repos/:owner/:repo/pulls/{n}/reviews`)
   y compararlo contra el head actual de la PR, sin asumir que el
   branch protection de GitHub ("dismiss stale reviews"/"require
   approval of the most recent push") esté configurado.
2. **GAP B — orden transaccional en `ready-for-pr.ps1`.** El contrato
   completo (`decision.md`, docs técnica/usuario, enlaces de índice,
   último veredicto aprobado de auditoría/QA/code review) debe validarse
   **antes** de mutar y commitear `ROADMAP.md` (`[ ]`→`[-]`), tanto en
   modo Feature como en modo Milestone. Si el contrato falla, no debe
   quedar ningún commit local que haya cambiado el estado de
   `ROADMAP.md`.
3. **GAP C — evidencia real en el cuerpo de la PR.** La sección de
   evidencias del PR body que arma `ready-for-pr.ps1` debe referenciar
   el nombre de archivo real del último intento aprobado de
   `audit-N.md`, `test-report-N.md` y `code-review-N.md` (usando
   `Get-LatestVerdictArtifact`, ya existente en
   `scripts/feature-contract.ps1`), no el placeholder literal `-N.md`.
   Aplica igual a modo Feature y modo Milestone.

Explícitamente NO incluye:

- Configurar branch protection / rulesets reales de GitHub (p. ej.
  "Require approval of the most recent reviewable push"). Es
  configuración manual del humano en GitHub; esta feature es la
  compensación defensiva en script para el caso en que esa
  configuración no esté activa o no sea suficiente. Se documenta como
  recomendación operativa en `docs/tecnica/`, no se automatiza.
- Cambiar el límite de tamaño o la guía de agrupación de items en modo
  MILESTONE.
- Tocar los workflows de GitHub Actions
  (`post-hitl-merge-gate.yml`, `post-merge-close-feature.yml`) más allá
  de lo que ya invocan (`complete-approved-pr.ps1`, `ready-for-pr.ps1`).
  Ningún AC de esta spec requiere editar YAML de Actions.
- Tocar `scripts/resolve-agentic-model.ps1`, `.agentic/models.json` o
  cualquier aspecto del router de modelos.
- Reescribir retroactivamente el cuerpo de PRs ya creadas con el
  placeholder genérico antes de esta feature.
- Agregar reintentos automáticos de aprobación humana: cuando GAP A
  detecta una aprobación stale, la resolución es que el humano vuelva a
  aprobar la PR sobre el commit vigente — no hay ningún mecanismo nuevo
  que reintente esto sin intervención humana.

## Contexto

El circuito agéntico tiene un único punto de intervención humana: la
aprobación de la PR en GitHub (`AGENTS.md`, sección "Único HITL").
`scripts/complete-approved-pr.ps1` es el gate que corre después de esa
aprobación y decide si mergea. Hoy ese gate solo verifica
`reviewDecision == APPROVED` en el momento en que corre, sin comprobar
contra qué commit se emitió esa aprobación. Si GitHub no tiene
configurado "dismiss stale reviews" o "require approval of the most
recent push" en la protección de la rama `develop`, un push posterior a
la aprobación (por ejemplo, un fix de `builder-agent` en respuesta a un
`post-hitl-gate-N.md` rechazado, o cualquier otro push a la misma rama
de PR) puede quedar mergeado sin que el humano haya visto ni aprobado
ese código nuevo. Esto rompe la garantía central del circuito: que el
único HITL efectivamente revisó el código que se mergea.

Por otro lado, `scripts/ready-for-pr.ps1` (el script que marca
`ROADMAP.md` como `[-] READY_FOR_PR` y crea/reutiliza la PR) muta y
commitea `ROADMAP.md` **antes** de correr la validación real del
contrato (`Assert-FeatureContract`/`Assert-WorkUnitContract
-RequireReadyRoadmap`, que exige `decision.md`, docs técnica/usuario,
enlaces de índice y el último veredicto real aprobado). Si esa
validación falla después de la mutación, queda un commit local con
`ROADMAP.md` en `[-]` sin que el contrato realmente haya pasado —un
estado inconsistente que además puede confundir a un reintento manual
del circuito.

Finalmente, el cuerpo de la PR que arma `ready-for-pr.ps1` usa literales
fijos (`audit-N.md`, `test-report-N.md`, `code-review-N.md`) en vez de
apuntar al archivo real del último intento aprobado (que puede ser
`audit-1.md`, `audit-3.md`, etc.), dificultando que quien revisa la PR
encuentre la evidencia real sin adivinar el número de intento.

Estos tres problemas ya fueron identificados como deuda conocida: la
spec de `01-code-reviewer-y-sdd` declaró explícitamente fuera de alcance
"reforzar `complete-approved-pr.ps1` para comparar el SHA de la última
review aprobatoria contra el HEAD actual de la PR ('stale approval')".
Esta feature cierra esa deuda y corrige los otros dos bugs relacionados
con integridad del circuito post-HITL / pre-PR detectados en el mismo
código.

## Criterios de aceptación

### GAP A — aprobación HITL vinculada al commit vigente

- **AC-1**: Si la última review con `state: APPROVED` de la PR fue
  emitida sobre un commit distinto del `headRefOid` actual de la PR
  (aprobación stale), `scripts/complete-approved-pr.ps1` termina con
  código de salida distinto de cero, **no** ejecuta `gh pr merge`, y
  escribe `runs/<slug>/post-hitl-gate-N.md` con `status: rejected` y un
  mensaje de feedback que indica explícitamente que la aprobación quedó
  obsoleta tras un push posterior y que se requiere una nueva
  aprobación humana sobre el commit vigente (no un cambio de
  `builder-agent`).
- **AC-2**: Si la última review `APPROVED` fue emitida exactamente sobre
  el `headRefOid` actual de la PR (caso no-stale, incluyendo el caso de
  una sola aprobación y el caso de múltiples reviews de distintos
  revisores donde la más reciente por fecha de envío coincide con el
  head), `scripts/complete-approved-pr.ps1` continúa el flujo existente
  sin cambios de comportamiento: espera checks post-aprobación y mergea
  solo si quedan verdes (comportamiento ya cubierto por los tests
  actuales de `tests/test_complete_approved_pr_script.py`, que deben
  seguir pasando).

### GAP B — orden transaccional en `ready-for-pr.ps1`

- **AC-3**: En modo Feature, si la validación completa del contrato
  (`decision.md`, `docs/tecnica/<slug>.md`, `docs/usuario/<slug>.md`,
  enlaces exactos de índice, último veredicto aprobado de auditoría/QA/
  code review) falla, `scripts/ready-for-pr.ps1` termina con código de
  salida distinto de cero **sin** haber modificado `ROADMAP.md` ni
  haber creado ningún commit nuevo en el repositorio (verificable con
  `git log`/`git status` antes y después de la corrida).
- **AC-4**: En modo Milestone, si la validación completa del contrato
  del work unit falla para al menos un item del manifest (por ejemplo,
  falta la doc técnica de un solo item de varios), `scripts/ready-for-
  pr.ps1` termina con código de salida distinto de cero sin haber
  modificado el estado de **ningún** item en `ROADMAP.md` (ni siquiera
  los items cuyo propio contrato individual sí estaría completo),
  preservando la garantía de "todo o nada" ya existente para la
  transición de estado en sí (`Assert-RoadmapItemsTransition`), pero
  extendiéndola a la validación de contrato completa.
- **AC-5**: Cuando la validación completa del contrato pasa, el
  comportamiento observable de `scripts/ready-for-pr.ps1` es idéntico al
  actual: `ROADMAP.md` pasa de `[ ]`/`[~]` a `[-]` (Feature) o todos los
  items pasan a `[-]` en un único commit (Milestone), se pushea la
  rama, y se crea la PR o se reutiliza la existente sin duplicados.

### GAP C — evidencia real en el cuerpo de la PR

- **AC-6**: En modo Feature, cuando `ready-for-pr.ps1` crea una PR nueva,
  el cuerpo de la PR referencia el nombre de archivo real del último
  intento aprobado de auditoría, QA y code review (por ejemplo
  `audit-2.md` si ese es el intento aprobado vigente), no el literal
  `audit-N.md`/`test-report-N.md`/`code-review-N.md`.
- **AC-7**: En modo Milestone, el cuerpo de la PR generada por `ready-
  for-pr.ps1` referencia igualmente el nombre de archivo real (único
  set de veredictos a nivel de work unit) del último intento aprobado de
  auditoría, QA y code review, no el literal genérico.

### Cobertura de tests automatizados

- **AC-8**: Existen tests de pytest para AC-1 y AC-2, siguiendo el
  patrón de fake `gh` ya usado en `tests/test_complete_approved_pr_script.py`
  (`FAKE_GH_MODE`/`FAKE_GH_LOG`), agregando al menos un modo que
  devuelva `headRefOid` distinto del `commit_id` de la última review
  `APPROVED` (caso stale) y un modo donde coincidan (caso no-stale).
- **AC-9**: Existen tests de pytest para AC-3 y AC-4, siguiendo el
  patrón de repos git temporales de `tests/test_feature_contract_scripts.py`
  (`make_contract_repo`/`prepare_ready_repo`), que verifican que al
  romper un elemento del contrato (por ejemplo, borrar `decision.md` o
  la doc técnica de un item) antes de correr `ready-for-pr.ps1`, el
  script falla y `ROADMAP.md`/el historial de commits quedan
  exactamente como estaban antes de la corrida.
- **AC-10**: Existen tests de pytest para AC-6 y AC-7 que verifican que
  el cuerpo de la PR (capturado desde el `--body-file` pasado al `gh`
  fake, o desde el archivo temporal que el script genera antes de
  invocar `gh pr create`) contiene el nombre de archivo real del último
  intento aprobado y no contiene el literal `-N.md`.
- **AC-11**: Todos los tests preexistentes en
  `tests/test_complete_approved_pr_script.py` y
  `tests/test_feature_contract_scripts.py` —incluyendo explícitamente
  `test_ready_for_pr_creates_pr_after_expected_missing_pr`— siguen
  pasando después de esta feature. Las fixtures/fakes de `gh` de esos
  archivos pueden necesitar extenderse para responder a los nuevos
  argumentos (`headRefOid` en `pr view`, la llamada a
  `gh api .../pulls/.../reviews`), pero ninguna aserción de
  comportamiento existente (código de salida, mensajes de error,
  invocación o no de `pr merge`/`pr create`) se debilita ni se elimina
  para poder pasar.

### Documentación y trazabilidad del circuito (obligatorios)

- **AC-12**: Debe existir
  `docs/tecnica/integridad-post-hitl-y-ready-for-pr.md`, no vacío, con
  las decisiones de diseño/implementación de los tres gaps (por qué se
  compara contra `headRefOid` y no solo `reviewDecision`, por qué se
  reordena la validación en `ready-for-pr.ps1` sin tocar la firma de
  `Assert-FeatureContract`/`Assert-WorkUnitContract`, cómo se resuelve
  el archivo real de evidencia en el body de la PR).
- **AC-13**: Debe existir
  `docs/usuario/integridad-post-hitl-y-ready-for-pr.md`, no vacío, con
  el propósito de la feature (qué riesgo real evita) y cómo se
  manifiesta para quien opera el circuito (qué mensaje ve si su
  aprobación quedó stale, qué debe hacer).
- **AC-14**: Debe existir
  `runs/v1.1.0/02-integridad-post-hitl-y-ready-for-pr/decision.md`, con
  decisiones demostrables desde spec/plan/tasks/auditoría/
  implementación, sin afirmar aprobación de merge.
- **AC-15**: Deben existir enlaces exactos y únicos a esos dos `.md` en
  la zona `FEATURE_LINKS` de `docs/tecnica/index.md` y
  `docs/usuario/index.md` respectivamente.

## Casos borde a contemplar

- **Múltiples revisores**: si dos revisores humanos aprueban la PR en
  distintos momentos y contra distintos commits, el gate debe usar la
  review `APPROVED` más reciente por `submitted_at`, no la primera ni
  una al azar, para decidir stale/no-stale.
- **Aprobar → dismiss → re-aprobar**: el endpoint de reviews de GitHub
  devuelve todas las reviews históricas, incluidas las `DISMISSED`. El
  gate debe filtrar por `state == APPROVED` sobre el conjunto completo y
  tomar la más reciente de ese subconjunto, ignorando reviews
  descartadas o en otros estados (`CHANGES_REQUESTED`, `COMMENTED`,
  `PENDING`).
- **Ninguna review `APPROVED` real pese a `reviewDecision: APPROVED`**:
  caso defensivo (no debería ocurrir en GitHub real, pero el script no
  debe asumirlo): si la consulta a `gh api .../reviews` no devuelve
  ninguna review en estado `APPROVED`, el gate debe fallar cerrado
  (rechazar, no mergear) con un mensaje diagnosticable, no lanzar una
  excepción no controlada ni mergear igual.
- **Paginación de reviews**: una PR con más reviews que el tamaño de
  página por defecto de la API de GitHub debe seguir identificando
  correctamente la más reciente `APPROVED` (usar el flag de paginación
  disponible de `gh api`, no asumir una sola página).
- **Re-ejecución del gate tras checks en verde** (ya cubierto por
  `test_complete_approved_pr_is_rerunnable_after_checks_turn_green`):
  la nueva verificación de commit debe seguir permitiendo reintentos
  del gate sobre la misma aprobación válida sin exigir nada nuevo del
  humano mientras el commit no cambie entre reintentos.
- **`ready-for-pr.ps1` re-ejecutado cuando `ROADMAP.md` ya está `[-]`**:
  el script debe seguir validando el contrato completo (y bloquear el
  push/creación de PR si falla) incluso cuando no hay ninguna mutación
  de `ROADMAP.md` pendiente, por ejemplo si alguien borró `decision.md`
  después de una corrida previa exitosa.
- **Milestone con items en estados mixtos** (algunos ya `[-]`, otros
  `[ ]`): la validación de contrato completo debe cubrir a todos los
  items del manifest antes de tocar `ROADMAP.md`, sin asumir que los ya
  `[-]` están automáticamente en regla.
- **Intentos rechazados intermedios**: si existe `audit-3.md` (rejected)
  después de `audit-2.md` (approved), el contrato ya exige que el
  **último** intento numérico sea `approved` para pasar
  (`Assert-LatestVerdictApproved`); por lo tanto, cuando se llega a
  construir el cuerpo de la PR, el archivo que referencia GAP C es
  siempre el intento aprobado vigente, nunca uno intermedio rechazado.
- **Encoding / caracteres especiales en el path del artefacto**: el
  nombre de archivo de evidencia insertado en el body de la PR debe
  seguir el mismo formato de ruta relativa (`runs/<slug>/audit-N.md`)
  que el resto de la sección de evidencias, sin rutas absolutas del
  entorno del agente.

## Riesgos / supuestos

- **Supuesto sobre disponibilidad de `gh api`**: se asume que el mismo
  GitHub CLI (`gh`) ya requerido por `AGENTS.md` soporta `gh api
  repos/:owner/:repo/pulls/{n}/reviews` resolviendo `:owner/:repo` desde
  el remoto Git del directorio de trabajo, igual que ya hace `gh pr
  view`/`gh pr checks` sin `-R` explícito en el código actual. No se
  agrega ninguna herramienta ni dependencia nueva.
- **Supuesto sobre "único HITL"**: cuando GAP A rechaza una aprobación
  stale, la resolución sigue siendo la misma persona aprobando la misma
  PR en GitHub —solo que debe reemitir esa aprobación sobre el commit
  vigente—. Esto no introduce un segundo punto de checkpoint humano
  distinto: es el mismo botón "Approve" de siempre, ejercido de nuevo.
  Se documenta explícitamente en `docs/tecnica/` para que quede claro
  que no viola la regla de "único HITL" de `AGENTS.md`.
  `post-hitl-merge-gate.yml` ya se dispara también en
  `pull_request: synchronize` (push nuevo a la PR), así que un nuevo
  push del humano re-aprobando no requiere tocar el workflow.
- **Decisión de diseño para GAP B**: en vez de modificar la firma de
  `Assert-FeatureContract`/`Assert-WorkUnitContract`, se aprovecha que
  el switch `-RequireReadyRoadmap` ya es aditivo (confirmado leyendo
  `scripts/feature-contract.ps1`): invocarlas **sin** ese switch ya
  valida decision.md/docs/índices/veredictos sin exigir el estado de
  ROADMAP. La corrección de orden vive enteramente en
  `scripts/ready-for-pr.ps1` (dónde se llama cada validación), no en
  `feature-contract.ps1`. Esto reduce el riesgo de regresión sobre el
  contrato ya usado por otras features.
- **No se toca branch protection real de GitHub**: la defensa de GAP A
  es una compensación en script, no un reemplazo de configurar
  "Require approval of the most recent reviewable push" en GitHub. Se
  recomienda esa configuración en `docs/tecnica/`, pero no se puede
  verificar ni aplicar desde este repo (es config del hosting, fuera
  del alcance de un cambio de código).
- **No se agrega arquitectura nueva**: ninguno de los tres gaps agrega
  backend, base de datos, integración externa o dependencia de build;
  no se requiere ninguna entrada nueva en `docs/tecnica/arquitectura.md`
  más allá de lo que ya documenta el uso de `gh` como herramienta
  requerida.
