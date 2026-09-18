# Decision: 04-ci-wiring-product-tests - CI wiring product tests

## Estado

Estado tecnico: ready_for_pr (pendiente de correr el resto del circuito:
QA, code review, `ready-for-pr.ps1`).

La aprobacion de merge es exclusivamente del HITL en GitHub sobre la PR.
Este documento no otorga ni implica esa aprobacion.

## Evidencias revisadas

Estos son los artefactos esperados del circuito para esta feature; no
implica que todos ya existieran o hubieran sido leídos en el momento
exacto en que se escribió esta lista (`test-report-1.md` y
`code-review-1.md` se producen en pasos posteriores del circuito):

- `runs/v1.1.0/04-ci-wiring-product-tests/spec.md`
- `runs/v1.1.0/04-ci-wiring-product-tests/plan.md`
- `runs/v1.1.0/04-ci-wiring-product-tests/tasks.md`
- `runs/v1.1.0/04-ci-wiring-product-tests/audit-1.md` (rejected)
- `runs/v1.1.0/04-ci-wiring-product-tests/audit-2.md` (approved)

## Resolucion de la Fase CLARIFY (base real de AC-5)

El intento 1 de `spec.md` trato como supuesto propio del `analyst-agent`
si `product-tests` debia ser status check requerido/bloqueante en branch
protection mientras solo corre un placeholder. `reviewer-agent` rechazo
ese intento en `audit-1.md` por tratarse de una ambiguedad material de
gobernanza del circuito, no una convencion tecnica inferible de codigo o
arquitectura existente.

Se elevo como pregunta concreta al humano: ¿`product-tests` debe ser
status check requerido/bloqueante en branch protection desde ya, o solo
cuando tenga contenido real de stack?

Respuesta del humano (registrada en `spec.md`, seccion "Clarificaciones
realizadas"): Requerido desde ya. Razon dada: el placeholder siempre pasa
en verde, asi que no bloquea a nadie hoy, y evita tener que acordarse de
agregarlo a branch protection el dia que el stack real llegue.

Esta respuesta es la base real de AC-5, no un supuesto propio. Se aplico
de forma consistente en `AGENTS.md` (seccion "CI/CD") y en
`docs/tecnica/ci-wiring-product-tests.md`.

## Decisiones demostrables

- `.github/workflows/ci.yml`: el job `test` se renombro a `circuit-tests`
  sin modificar ninguno de sus steps (checkout, setup Python 3.12 con
  cache pip sobre `requirements-dev.txt`, `pip install -r
  requirements-dev.txt`, `pytest -v`). Se agrego el job nuevo
  `product-tests` (`runs-on: ubuntu-latest`, sin `needs:`, corre en
  paralelo), con `actions/checkout@v4`, un bloque de comentario grande
  delimitado por lineas de `#` que referencia explicitamente
  `docs/tecnica/arquitectura.md` como el lugar donde documentar el stack
  real antes de reemplazar el placeholder, y un unico step
  `Placeholder (sin stack definido)` con `run: echo ...` que siempre
  termina en exito y no depende de ningun artefacto de un stack todavia
  no definido. Ambos jobs comparten el mismo bloque `on:` del workflow
  (`push`/`pull_request` a `develop` y `main`) y ninguno declara `if:`
  propio.
- `AGENTS.md`, seccion "CI/CD": el bullet de "CI" ya no describe un unico
  job `test`; describe `circuit-tests` y `product-tests` como gate
  obligatorio con el mismo nivel de exigencia, citando explicitamente que
  es una decision confirmada por el humano en Fase CLARIFY (no un
  supuesto), y deja la advertencia de migracion de nombre de status check
  `test` → `circuit-tests` para adopciones downstream.
- `tests/test_ci_workflow.py` (archivo nuevo): cuatro tests que verifican
  por substring de texto plano sobre `.github/workflows/ci.yml` (sin
  parsear YAML, sin agregar `pyyaml`): presencia de `circuit-tests:` y
  `product-tests:`, presencia de `pytest -v` dentro del bloque de
  `circuit-tests`, presencia del marcador `PLACEHOLDER` y la referencia a
  `docs/tecnica/arquitectura.md` dentro del bloque de `product-tests`, y
  ausencia de `if:` en ambos jobs. Se confirmo manualmente (fuera del
  archivo de test, sin dejar codigo muerto) que cada asercion detecta la
  ausencia correspondiente antes de darla por buena, siguiendo la
  verificacion pedida por T-05 de `tasks.md`.
- `docs/tecnica/ci-wiring-product-tests.md` y
  `docs/usuario/ci-wiring-product-tests.md`: creados, no vacios, con las
  decisiones de diseno (por que dos jobs, por que `product-tests` es
  requerido desde ya, forma exacta del marcador, advertencia de
  migracion) y el uso operativo (como se ven los checks, como reemplazar
  el placeholder).
- `docs/tecnica/index.md` y `docs/usuario/index.md`: enlazados via
  `scripts/update-doc-indexes.ps1 04-ci-wiring-product-tests "CI wiring
  product tests"`, sin duplicados en la zona `FEATURE_LINKS`.
- No se toco `docs/tecnica/arquitectura.md`: esta feature no agrega
  backend, base de datos, integracion externa ni dependencia de build
  (el placeholder de `product-tests` es deliberadamente vacio de
  contenido real).
- No se toco `requirements-dev.txt` ni se agrego ninguna dependencia de
  parseo YAML.

## Resultado

La feature queda apta para integrarse/cerrarse cuando GitHub confirme
merge contra `develop` y el cierre automatico marque `ROADMAP.md`.
