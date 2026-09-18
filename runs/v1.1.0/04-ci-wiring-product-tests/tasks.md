# Tasks: CI wiring product tests

- **T-01** — Renombrar el job `test` de `.github/workflows/ci.yml` a
  `circuit-tests`, sin modificar ninguno de sus steps existentes
  (checkout, setup Python 3.12 con cache pip, `pip install -r
  requirements-dev.txt`, `pytest -v`).
  Verificación: `git diff .github/workflows/ci.yml` muestra únicamente
  el cambio de nombre del job (más el bloque de comentario existente
  que se reemplaza en T-02); `pytest -v` local sigue pasando igual que
  antes.
  Traza: AC-1, AC-2.

- **T-02** — Agregar el job `product-tests` a
  `.github/workflows/ci.yml`: `runs-on: ubuntu-latest`, sin `needs:`,
  con `actions/checkout@v4`, un bloque de comentario marcador
  inconfundible que referencia `docs/tecnica/arquitectura.md` como el
  lugar donde documentar el stack real antes de agregar pasos aquí, y un
  único step placeholder (`run: echo ...`) que siempre termina en
  éxito.
  Verificación: revisión visual del YAML; el check `product-tests`
  aparece y queda en verde en el CI de la propia PR de esta feature.
  Traza: AC-1, AC-3, AC-4.
  Depende de: T-01.

- **T-03** — Confirmar que ambos jobs (`circuit-tests`,
  `product-tests`) comparten exactamente los mismos triggers del
  workflow (`push`/`pull_request` a `develop` y `main`), sin ningún
  `if:` a nivel de job que excluya a alguno.
  Verificación: inspección del bloque `on:` (nivel de workflow, no de
  job) y ausencia de `if:` en ambos jobs.
  Traza: AC-1.
  Depende de: T-01, T-02.

- **T-04** — Actualizar la sección "CI/CD" de `AGENTS.md`: reemplazar la
  descripción del job único `test` por la descripción de
  `circuit-tests` y `product-tests`, dejando explícito que ambos son
  gate obligatorio con el mismo nivel de exigencia (decisión confirmada
  por el humano en Fase CLARIFY, no un supuesto), como referencia para
  el checklist de branch protection de `05-operational-readiness-docs`.
  Verificación: lectura de `AGENTS.md` — ya no menciona un job único
  llamado `test`.
  Traza: AC-5, AC-6.
  Depende de: T-01, T-02.

- **T-05** — Agregar un test de pytest (`tests/test_ci_workflow.py` u
  otra ubicación que mantenga cohesión con `tests/test_feature_contract_scripts.py`)
  que verifique, sobre el contenido de texto plano de
  `.github/workflows/ci.yml`: presencia de `circuit-tests:`, presencia
  de `product-tests:`, presencia de `pytest -v` dentro del bloque de
  `circuit-tests`, y presencia del texto del marcador de
  `product-tests`. Sin agregar dependencia nueva de parseo YAML.
  Verificación: `pytest -v tests/test_ci_workflow.py` (o el archivo
  elegido) pasa; comentando temporalmente uno de los dos jobs el test
  falla (confirmación manual de que el test realmente detecta la
  ausencia antes de dejarlo definitivo).
  Traza: AC-7.
  Depende de: T-01, T-02.

- **T-06** — Escribir `docs/tecnica/ci-wiring-product-tests.md` con las
  decisiones de diseño: por qué dos jobs, por qué `product-tests` queda
  documentado como requerido/bloqueante desde ya pese a estar vacío
  (decisión confirmada por el humano en Fase CLARIFY, ver
  "Clarificaciones realizadas" de `spec.md` — no un supuesto propio),
  forma exacta del marcador, y la advertencia de migración de nombre de
  status check para adopciones downstream.
  Verificación: el archivo existe y no está vacío.
  Traza: AC-5, AC-8.
  Depende de: T-01, T-02.

- **T-07** — Escribir `docs/usuario/ci-wiring-product-tests.md` con el
  propósito de la feature y cómo verla/usarla: dónde se ven los dos
  checks en GitHub Actions/PR, y los pasos concretos para reemplazar el
  placeholder de `product-tests` cuando el proyecto real defina su
  stack.
  Verificación: el archivo existe y no está vacío.
  Traza: AC-9.
  Depende de: T-01, T-02.

- **T-08** — Ejecutar
  `scripts/update-doc-indexes.ps1 04-ci-wiring-product-tests "<Titulo>"`
  para agregar los enlaces exactos en la zona `FEATURE_LINKS` de
  `docs/tecnica/index.md` y `docs/usuario/index.md`.
  Verificación: ambos índices contienen el enlace exacto a los dos `.md`
  nuevos.
  Traza: AC-10.
  Depende de: T-06, T-07.

- **T-09** — Escribir `runs/v1.1.0/04-ci-wiring-product-tests/decision.md` con
  decisiones demostrables desde `spec.md`/`plan.md`/`tasks.md`/
  auditoría/implementación, sin afirmar aprobación de merge.
  Verificación: el archivo existe, no está vacío y no contiene ninguna
  afirmación de aprobación de merge.
  Traza: AC-11.
  Depende de: T-01 a T-08.
