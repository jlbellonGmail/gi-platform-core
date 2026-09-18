# Spec: Operational readiness docs

## Identificacion

- Work unit: 05-operational-readiness-docs
- Modo: FEATURE
- Items (solo MILESTONE): N/A

## Alcance

Incluye:

1. **Checklist de branch protection de GitHub.** Agregar a la sección
   "Setup manual (una sola vez, no automatizable)" de `AGENTS.md` un
   checklist operativo, con comandos `gh` exactos y ejecutables
   copy-paste, para configurar en la rama `develop` del repositorio real
   en GitHub los cuatro requisitos que pide el ítem de `ROADMAP.md`:
   (a) exigir pull request antes de mergear, (b) exigir que el status
   check del job de CI esté en verde, (c) exigir al menos 1 aprobación,
   (d) descartar (dismiss) aprobaciones obsoletas cuando hay un push
   nuevo a la PR.
2. **Nota de troubleshooting sobre EDR/antivirus agresivo en Windows.**
   Documentar el síntoma, la causa, el alcance real del problema (solo
   local, no corrompe git ni afecta CI/merge) y la solución exacta
   (`git worktree remove --force` + `git worktree add` en un path nuevo)
   para el caso en que `local-feature-reconcile.ps1`/`ready-for-pr.ps1`
   queden bloqueados al correr como proceso de fondo en una máquina
   Windows con EDR agresivo.

Ambos puntos son documentación operativa/setup para quien mantiene el
circuito (no producto), ninguno justifica una PR propia por separado, y
el humano ya confirmó explícitamente esa cohesión al pedir esta feature
— ver "Contexto y fuentes" para el detalle de por qué esto no dispara el
gate de tamaño/descomposición de Milestone (no aplica: es una sola
Feature con un único ítem de `ROADMAP.md`, no un Milestone).

Explícitamente NO incluye:

- Ejecutar el/los comando(s) `gh api` contra un repositorio GitHub real:
  es un paso manual del humano (la sección "Setup manual" ya documenta
  pasos de este tipo, como el remoto de GitHub o GitHub Pages), no una
  automatización que corra el circuito agéntico ni un script nuevo en
  `scripts/`.
- Configurar branch protection sobre `main`. El circuito automatizado
  (`ready-for-pr.ps1`, `complete-approved-pr.ps1`, los workflows de
  Actions) solo crea y mergea PRs contra `develop` (ver `AGENTS.md`,
  sección "Git"); `main` solo recibe merges desde `develop` en el
  momento de un release, fuera del circuito por feature. Ver "Supuestos".
- Modificar `.github/workflows/ci.yml` o cualquier otro workflow. El
  nombre exacto del job de CI (`test`) se documenta tal como existe hoy
  en este worktree; la feature `04-ci-wiring-product-tests` (en curso en
  paralelo, no mergeada a `develop` al momento de esta spec) puede
  cambiarlo, y esta spec lo declara como dependencia explícita no
  bloqueante (ver "Supuestos" y "Casos borde").
- Escribir o modificar ningún script de `scripts/*.ps1`. La solución al
  bloqueo de EDR es un procedimiento manual documentado
  (`git worktree remove --force` + `git worktree add`), no un cambio de
  comportamiento de `local-feature-reconcile.ps1` ni de `ready-for-pr.ps1`.
- Agregar un mecanismo automático que detecte o repare bloqueos de EDR:
  el troubleshooting documentado es reactivo (el operador lo sigue
  cuando observa el síntoma), no una automatización nueva del circuito.
- Cualquier decisión de arquitectura de stack de producto: este template
  sigue sin código de producto propio.

## Contexto y fuentes

El ítem `05-operational-readiness-docs` de `ROADMAP.md` pide
explícitamente dos piezas de documentación operativa independientes
entre sí en su origen técnico, pero agrupadas por el humano en una sola
Feature por su cohesión real (ambas son documentación de setup/
mantenimiento del circuito, ninguna justifica su propia PR). El pedido
humano adicional (no está en `ROADMAP.md`) aporta el detalle operativo
concreto de ambos puntos y fue tomado como fuente autoritativa de nivel
1 ("Instrucción o clarificación humana vigente") según la precedencia de
fuentes de `AGENTS.md`.

Fuentes consultadas:

- **`ROADMAP.md`** (ítem `05-operational-readiness-docs`, sin bloque
  `Referencias:`): define el alcance mínimo — checklist de branch
  protection (require PR, status check, approval, dismiss stale
  approvals) con comandos `gh` exactos, y nota de troubleshooting sobre
  bloqueos de `local-feature-reconcile.ps1`/`ready-for-pr.ps1` por EDR
  agresivo en Windows.
- **`docs/producto/contexto-producto.md`**: existe pero todas sus
  secciones están "Por definir" (el template todavía no tiene producto
  propio). No aporta restricciones ni reglas de negocio para esta
  feature — es documentación puramente operativa del circuito, no de
  producto.
- **`AGENTS.md`**: sección "Setup manual (una sola vez, no
  automatizable)" ya existe con el patrón exacto a extender (bullets con
  pasos manuales de una sola vez, algunos con comandos exactos). Sección
  "Git" confirma que el circuito automatizado solo crea/mergea PRs
  contra `develop`, nunca contra `main` directamente, y establece la
  regla dura "Nunca commitear directo a `develop`... ni nunca directo a
  `main`" sin excepción declarada para administradores — fuente decisiva
  para resolver la Fase CLARIFY de `enforce_admins` (ver
  "Clarificaciones realizadas"). Sección "CI/CD" confirma que
  `.github/workflows/ci.yml` corre pytest en un job llamado `test`.
- **`.claude/rules/`**: confirmado vacío (solo `.gitkeep`), sin reglas
  de dominio adicionales que apliquen.
- **`docs/tecnica/circuito-agentico.md`**: documenta hoy la mecánica del
  circuito multiherramienta (roles, adaptadores, router de modelos, gate
  post-HITL) y ya menciona el reconciliador local en la sección "Gate
  post-HITL". Es el documento técnico existente más cercano a la
  mecánica de `local-feature-reconcile.ps1`/`ready-for-pr.ps1`, por lo
  que es el lugar natural para la nota de troubleshooting en vez de un
  archivo nuevo (ver "Supuestos").
- **`.github/workflows/ci.yml`** (estado actual de este worktree, previo
  a la feature `04-ci-wiring-product-tests`): un único job `test` sin
  `name:` de override, por lo que GitHub muestra el status check como
  `test`. Esta feature (`04`) corre en paralelo en otro worktree y
  probablemente separe ese job en `circuit-tests`/`product-tests`; no
  está mergeada a `develop` al momento de esta spec. Ver "Supuestos" y
  "Casos borde" para cómo se declara esta dependencia sin bloquear.
- **`scripts/local-feature-reconcile.ps1`** y **`scripts/ready-for-
  pr.ps1`**: leídos completos. Confirman que `ready-for-pr.ps1` lanza
  `local-feature-reconcile.ps1 -StartBackground` como proceso PowerShell
  de fondo (`Start-Process ... -WindowStyle Hidden`), con un lock file
  (`.pid`) y logs (`.log`/`.err.log`) bajo
  `<git-common-dir>/feature-reconcilers/`. El reconciliador de fondo
  hace polling de `origin/develop:ROADMAP.md` y, cuando detecta cierre
  remoto, ejecuta `git worktree remove` y `git branch -d` sobre el
  worktree/rama de la feature. Un EDR agresivo que intercepte o bloquee
  ese proceso de PowerShell en background puede dejarlo colgado o
  impedirle completar las operaciones de archivo del worktree, sin que
  esto afecte el estado remoto de `ROADMAP.md`, CI ni el merge (que son
  responsabilidad de GitHub Actions, no de este proceso local).
- **`scripts/feature-contract.ps1`**: confirma que el estado del
  reconciliador vive en `Get-FeatureStateDir` (`<git-common-dir>/
  feature-reconcilers/`), fuera de cualquier worktree, por lo que
  remover el worktree con `--force` no corrompe ese estado ni el
  historial de git remoto.
- **`docs/tecnica/index.md`** / **`docs/usuario/index.md`**: confirman
  el formato exacto de enlace dentro del bloque
  `<!-- FEATURE_LINKS_START -->` / `<!-- FEATURE_LINKS_END -->`
  (`- [Título](slug.md)`), gestionado por
  `scripts/update-doc-indexes.ps1`.
- **`runs/v1.1.0/02-integridad-post-hitl-y-ready-for-pr/spec.md`** y
  **`docs/tecnica/integridad-post-hitl-y-ready-for-pr.md`**: la feature
  `02` dejó explícitamente fuera de alcance "configurar branch
  protection / rulesets reales de GitHub" y documentó "Recomendación
  operativa (no automatizada)" pidiendo activar en `develop` protección
  equivalente a "Require approval of the most recent reviewable push",
  remitiendo esa configuración real a fuera del repo. Esta feature
  atiende esa deuda documentada (aunque el checklist pedido acá es el
  set clásico de 4 requisitos del ítem `05`, no exactamente "most recent
  reviewable push", que es una capacidad más nueva de GitHub Rulesets —
  ver "Supuestos").
- **Código/tests existentes**: no hay tests de pytest que verifiquen
  contenido de `AGENTS.md` o `docs/tecnica/*.md` como texto; el patrón
  existente del repo trata la documentación como verificación manual
  reproducible, no automatizada por pytest (confirmado también por el
  criterio de aceptación estándar de "verificación manual reproducible
  cuando corresponda" de `AGENTS.md`, sección "Circuito", paso 4).

Esta versión 2 de la spec resuelve el feedback de `audit-1.md`: (a) el
valor de `enforce_admins` dejó de ser un supuesto unilateral y pasó por
Fase CLARIFY, con la respuesta registrada en "Clarificaciones
realizadas"; (b) se agregó el caso borde faltante sobre la semántica de
reemplazo total del `PUT` de branch protection, con su propio criterio
de aceptación (AC-4).

## Criterios de aceptación

- **AC-1**: `AGENTS.md`, sección "Setup manual (una sola vez, no
  automatizable)", contiene un bullet nuevo "**Branch protection de
  GitHub**" con un checklist de exactamente estos 4 requisitos aplicados
  a la rama `develop`: (a) exigir pull request antes de mergear, (b)
  exigir en verde el status check del job de CI actual (nombre `test`),
  (c) exigir al menos 1 aprobación, (d) descartar (dismiss) aprobaciones
  obsoletas cuando hay push nuevo a la PR.
- **AC-2**: Ese mismo bullet incluye el/los comando(s) `gh` exactos,
  ejecutables copy-paste (sin placeholders inventados salvo `{owner}`/
  `{repo}`, resueltos automáticamente por `gh api` desde el contexto del
  repositorio), que aplican esos 4 requisitos sobre `develop` de forma
  declarativa (una sola invocación reproducible, sin efectos
  destructivos sobre datos o historial del repositorio). El payload
  documentado fija `enforce_admins: true`, para que los administradores
  del repositorio queden también sujetos a la protección, sin excepción
  de bypass — ver "Clarificaciones realizadas". Debe quedar documentada
  la justificación técnica de por qué `gh api` es seguro/confiable para
  esta operación (ver "Contexto y fuentes"/"Supuestos"), en vez de solo
  pasos manuales de UI.
- **AC-3**: El bullet deja explícito, junto al comando, que el nombre
  del status check (`test`) corresponde al job único y actual de
  `.github/workflows/ci.yml` en este worktree, y que si la feature
  `04-ci-wiring-product-tests` renombra o separa ese job al mergearse,
  este checklist debe actualizarse antes de aplicarse (dependencia
  declarada explícitamente, no bloqueante para esta spec).
- **AC-4**: El bullet advierte explícitamente que el `PUT` de branch
  protection documentado **reemplaza toda la configuración de branch
  protection existente sobre `develop`, no la fusiona incrementalmente**
  con reglas ya configuradas manualmente desde la UI de GitHub (por
  ejemplo "require signed commits", "require linear history",
  restricciones de push por equipo), y recomienda correr primero el
  comando de verificación de solo lectura (`GET`, ya documentado por
  AC-2) antes de volver a ejecutar el `PUT` — en particular en el
  escenario ya cubierto por AC-3 de actualizar el nombre del status
  check — para no pisar en silencio protecciones adicionales.
- **AC-5**: `docs/tecnica/circuito-agentico.md` contiene una sección
  nueva de troubleshooting sobre bloqueos de
  `local-feature-reconcile.ps1`/`ready-for-pr.ps1` en máquinas Windows
  con EDR/antivirus agresivo, con: síntoma observable, causa (el EDR
  interfiere con el proceso PowerShell de fondo), alcance del impacto
  (exclusivamente local; no corrompe el estado de git remoto ni afecta
  CI/merge) y la solución exacta con los comandos `git worktree remove
  --force <path>` seguido de `git worktree add <path-nuevo> <rama>`.
- **AC-6**: Debe existir `docs/tecnica/operational-readiness-docs.md`,
  no vacío, con las decisiones de diseño/implementación relevantes (por
  qué `gh api` sobre UI manual, por qué solo `develop` y no `main`, por
  qué `enforce_admins: true`, por qué el troubleshooting vive en
  `circuito-agentico.md`).
- **AC-7**: Debe existir `docs/usuario/operational-readiness-docs.md`,
  no vacío, con el propósito de la feature y cómo usar ambos checklists
  (cuándo correr el comando de branch protection, cuándo seguir el
  procedimiento de troubleshooting de EDR).
- **AC-8**: Debe existir
  `runs/v1.1.0/05-operational-readiness-docs/decision.md`, con decisiones
  demostrables desde spec/plan/tasks/auditoría/implementación, sin
  afirmar aprobación de merge.
- **AC-9**: Deben existir enlaces exactos y únicos a
  `operational-readiness-docs.md` en la zona `FEATURE_LINKS` de
  `docs/tecnica/index.md` y `docs/usuario/index.md` respectivamente (vía
  `scripts/update-doc-indexes.ps1`).

## Casos borde a contemplar

- **Repo sin remoto de GitHub configurado todavía**: el comando `gh api`
  fallará si no hay un remoto GitHub válido en el directorio actual. El
  checklist debe advertir este prerequisito (coherente con el bullet
  existente "Remoto GitHub" de la misma sección "Setup manual").
- **Usuario sin permisos de administrador sobre el repositorio**: el
  endpoint de branch protection exige permisos de admin; `gh api`
  devuelve un error 403/404 claro. El checklist debe advertir este
  prerequisito explícitamente, sin prometer que el comando funciona con
  cualquier nivel de permiso.
- **Nombre de status check desactualizado** (por ejemplo, la feature
  `04` ya se mergeó y renombró el job): aplicar el comando con el nombre
  viejo (`test`) dejaría un status check requerido que nunca se reporta,
  bloqueando todo merge futuro contra `develop`. El checklist debe
  indicar cómo verificar el nombre real vigente antes de aplicar el
  comando (mirar el nombre del job en la pestaña Actions de una PR
  reciente, o `gh api repos/{owner}/{repo}/commits/{sha}/check-runs`) en
  vez de asumirlo ciegamente.
- **El `PUT` reemplaza, no fusiona, la configuración existente**: el
  endpoint de branch protection de GitHub sobrescribe por completo la
  configuración vigente de la rama con el payload enviado — no hace un
  merge incremental con reglas ya activas configuradas manualmente
  desde la UI (por ejemplo "require signed commits", "require linear
  history", restricciones de push por equipo/usuario). Si esas reglas
  existieran y se reaplica el `PUT` documentado sin incluirlas en el
  payload, se pierden silenciosamente. El checklist debe advertir esta
  semántica explícitamente y recomendar correr primero el `GET` de
  verificación (ya documentado) para revisar qué hay configurado antes
  de reemplazar — en particular antes de cualquier re-ejecución, como la
  del caso borde anterior de status check desactualizado.
- **Re-ejecución del comando de branch protection**: el `PUT` de la API
  de branch protection es declarativo/idempotente respecto de sí mismo
  — volver a correrlo con el mismo payload dos veces seguidas no crea
  duplicados ni falla la segunda vez —, pero no es "aditivo" respecto de
  configuración externa a ese payload (ver ítem anterior). El checklist
  debe distinguir ambas cosas: seguro re-ejecutar el mismo payload, no
  seguro re-ejecutarlo sin revisar antes si hay reglas adicionales que
  perderías.
- **JSON del payload inválido por error de tipeo al copiar/pegar**: debe
  documentarse un paso de verificación local sin credenciales (validar
  el JSON con `ConvertFrom-Json` en PowerShell antes de enviarlo) para
  que un error de sintaxis se detecte antes de llamar a la API real.
- **Lock file (`.pid`) del reconciliador apuntando a un proceso muerto o
  bloqueado por el EDR**: el troubleshooting debe indicar que, si
  `local-feature-reconcile.ps1 -StartBackground` reporta "ya existe un
  reconciliador" pero el proceso real está bloqueado/inerte, el
  operador puede seguir igual el procedimiento de `git worktree remove
  --force` sin necesidad de matar el proceso a mano primero, porque el
  estado del reconciliador (`<git-common-dir>/feature-reconcilers/`)
  vive fuera del worktree y no bloquea esa operación de git.
- **Cambios sin commitear en el worktree bloqueado**: `git worktree
  remove --force` descarta cualquier cambio local no commiteado en ese
  worktree. El troubleshooting debe advertir explícitamente este riesgo
  antes de recomendar el `--force`, y sugerir revisar `git status` en el
  worktree bloqueado si es accesible antes de forzar la remoción.
- **Accesibilidad/responsive**: no aplica — ambos artefactos son
  documentación Markdown en texto plano, sin UI ni componente visual
  nuevo.

## Supuestos

- **Rama protegida = `develop`, no `main`**: el circuito automatizado
  (`ready-for-pr.ps1`, `complete-approved-pr.ps1`, los workflows de
  Actions) solo crea y mergea PRs contra `develop` por feature (ver
  `AGENTS.md`, sección "Git": "`main` — solo recibe merges desde
  `develop` vía PR, cuando se decide hacer un release"). El checklist de
  esta feature documenta protección para `develop`, que es la rama
  relevante para el único HITL del circuito; proteger `main` queda fuera
  de alcance porque es una decisión de release del humano, no de este
  circuito por feature.
- **`gh api` es seguro/confiable para esta operación (decisión técnica,
  no CLARIFY)**: aplicar branch protection vía `gh api --method PUT
  repos/{owner}/{repo}/branches/develop/protection` es una operación
  declarativa sobre configuración del repositorio (no sobre datos,
  código o historial), reversible (se puede volver a aplicar con otro
  payload o desactivar desde la misma API/UI), aunque de reemplazo total
  respecto de configuración externa al payload (ver "Casos borde"). Por
  eso se documenta como comando `gh` ejecutable en vez de únicamente
  pasos manuales de la UI de GitHub. Se documenta también, como
  alternativa, los pasos exactos de UI equivalentes por si el operador
  no confía en correr el comando o `gh` no está disponible en su
  máquina.
- **Nombre del status check = `test`**: se basa en el estado ACTUAL de
  `.github/workflows/ci.yml` en este worktree (job único `test`, sin
  `name:` de override, por lo que GitHub Actions expone el check como
  `test`). Si la feature `04-ci-wiring-product-tests` (en curso en
  paralelo) separa ese job en `circuit-tests`/`product-tests` antes de
  que se aplique este checklist, el nombre documentado quedará
  desactualizado — se declara como dependencia explícita, no como
  ambigüedad material bloqueante (ver AC-3 y "Casos borde").
- **Ubicación del troubleshooting de EDR**: se agrega a
  `docs/tecnica/circuito-agentico.md` (no un archivo nuevo) porque ese
  documento ya es la fuente técnica del comportamiento de
  `local-feature-reconcile.ps1`/`ready-for-pr.ps1` y del gate post-HITL;
  agregar un archivo nuevo solo para una nota de troubleshooting
  fragmentaría documentación relacionada sin necesidad.
- **Sin nuevas dependencias de build/backend**: ninguna de las dos
  piezas de esta feature agrega backend, base de datos, integración
  externa o dependencia de build; no se requiere entrada nueva en
  `docs/tecnica/arquitectura.md`.

## Clarificaciones realizadas

- **Pregunta**: ¿`enforce_admins` debe ser `true` o `false` en el
  payload de branch protection documentado, dado que el ítem de
  `ROADMAP.md` no lo especifica (solo pide PR obligatoria, status check,
  1 aprobación y dismiss stale approvals) y esto determina si los
  administradores del repositorio pueden bypassear esa misma protección?
  **Respuesta**: `true`. Los administradores también deben quedar
  sujetos a la protección — consistente con la regla dura ya existente
  en `AGENTS.md` ("Nunca commitear directo a `develop`... ni nunca
  directo a `main`"), sin excepción, aceptando que en un incidente
  operativo excepcional no haya bypass automático disponible para
  admins.

## Decisiones pendientes bloqueantes

Ninguna.
