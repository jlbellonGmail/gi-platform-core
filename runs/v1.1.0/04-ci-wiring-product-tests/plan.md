# Plan: CI wiring product tests

## 1. Arquitectura afectada

Toca exclusivamente:

- `.github/workflows/ci.yml` (AC-1 a AC-5).
- `AGENTS.md`, sección "CI/CD" (AC-5, AC-6).
- `tests/` — un test nuevo o extensión de uno existente (AC-7).
- `docs/tecnica/ci-wiring-product-tests.md` (AC-8).
- `docs/usuario/ci-wiring-product-tests.md` (AC-9).
- `docs/tecnica/index.md` y `docs/usuario/index.md` (AC-10).
- `runs/v1.1.0/04-ci-wiring-product-tests/decision.md` (AC-11).

Explícitamente NO toca: `scripts/*.ps1`, `.agentic/`, ningún otro
workflow (`post-hitl-merge-gate.yml`, `post-merge-close-feature.yml`,
`docs.yml`), `requirements-dev.txt` (no hay dependencia nueva),
`docs/tecnica/arquitectura.md` (no hay decisión de arquitectura nueva:
no se agrega backend, base de datos, integración externa ni dependencia
de build), ni `docs/producto/contexto-producto.md` (esta feature es
infraestructura del circuito, no conocimiento de producto).

## 2. Componentes y contratos nuevos/modificados

- **Job `circuit-tests` en `ci.yml`** (AC-1, AC-2): renombre directo del
  job `test` actual, mismos steps exactos (`actions/checkout@v4`,
  `actions/setup-python@v5` con `python-version: "3.12"` y cache pip
  sobre `requirements-dev.txt`, `pip install -r requirements-dev.txt`,
  `pytest -v`). Ningún step cambia de contenido.
- **Job `product-tests` en `ci.yml`** (AC-1, AC-3, AC-4, AC-5): job
  nuevo, `runs-on: ubuntu-latest`, sin `needs:` respecto de
  `circuit-tests` (corre en paralelo). Steps: `actions/checkout@v4` +
  un bloque de comentario grande e inconfundible (por ejemplo delimitado
  con una línea de `#` repetidos) que indica textualmente "agregar acá
  los pasos reales de build/test del stack de producto cuando se defina
  — ver docs/tecnica/arquitectura.md", seguido de un único step
  placeholder (`run: echo ...`) que siempre termina en éxito y no
  depende de ningún artefacto/paquete de un stack todavía no definido.
- **`AGENTS.md`, sección "CI/CD"** (AC-5, AC-6): reemplazar el bullet
  actual que describe un único job `test` por una descripción de los dos
  jobs reales (`circuit-tests`, `product-tests`), su propósito y que
  ambos son gate obligatorio (mismo nivel de exigencia, confirmado en
  Fase CLARIFY con el humano), dejando la referencia explícita para el
  checklist de branch protection de `05-operational-readiness-docs`.
- **Test de estructura del workflow** (AC-7): nuevo archivo
  `tests/test_ci_workflow.py` (o una función agregada a
  `tests/test_feature_contract_scripts.py`, decidido por builder-agent
  según cuál mantenga mejor la cohesión del archivo existente) que lee
  `.github/workflows/ci.yml` como texto plano y hace aserciones de
  substring: presencia de `circuit-tests:`, presencia de `product-tests:`,
  presencia de `pytest -v` dentro del bloque de `circuit-tests`,
  presencia del texto del marcador de `product-tests`. Sigue el mismo
  patrón que `test_workflow_yaml_is_valid` en
  `tests/test_feature_contract_scripts.py` (líneas 687-698 del archivo
  actual), sin parsear YAML.
- **`docs/tecnica/ci-wiring-product-tests.md`** (AC-8): documenta por
  qué se separó en dos jobs, por qué `product-tests` se documenta como
  requerido desde ya (razonamiento confirmado por el humano en Fase
  CLARIFY, ver "Clarificaciones realizadas" de `spec.md`), la forma
  exacta del marcador, y la advertencia de migración de nombre de status
  check para adopciones downstream.
- **`docs/usuario/ci-wiring-product-tests.md`** (AC-9): explica, para
  quien opera el repo, cómo se ven los dos checks en la pestaña
  "Checks" de una PR/Actions, y los pasos concretos para reemplazar el
  placeholder de `product-tests` cuando el proyecto real defina su
  stack.
- **Índices** (AC-10): actualización de
  `docs/tecnica/index.md`/`docs/usuario/index.md` vía
  `scripts/update-doc-indexes.ps1`.
- **`decision.md`** (AC-11): documento canónico de decisiones
  demostrables de esta feature.

## 3. Compatibilidad y migración

No hay datos ni artefactos persistentes que migrar: es un cambio de
configuración de CI. El único riesgo de compatibilidad es de nombre de
status check: el job pasa de llamarse `test` a `circuit-tests`. En este
propio template no hay branch protection configurada todavía (setup
manual pendiente, ítem `05-operational-readiness-docs`), así que no hay
ninguna configuración existente que romper acá. Se documenta como
advertencia explícita en `docs/tecnica/ci-wiring-product-tests.md` para
que cualquier proyecto real que ya haya adoptado este template y
configurado branch protection con el nombre `test` sepa que debe
actualizarlo al adoptar esta feature.

## 4. Dependencias

Ninguna dependencia nueva. No se modifica `requirements-dev.txt`: el
test de estructura del workflow (AC-7) se implementa con lectura de
texto plano (`pathlib`/`open` + aserciones de substring), igual que el
precedente ya existente en el repo, evitando agregar `pyyaml` u otra
librería de parseo YAML sin una decisión de arquitectura que la
justifique.

## 5. Impacto operacional

Quien mire la pestaña "Checks" de una PR o de un push a `develop`/`main`
verá dos checks separados en vez de uno: `circuit-tests` y
`product-tests`. Nadie necesita instalar herramientas nuevas
localmente. Quien configure branch protection en el futuro (ítem 05)
deberá marcar ambos jobs como status checks requeridos, según lo
documentado acá y confirmado por el humano en Fase CLARIFY. Quien
mantenga el proyecto real que nazca de este template tiene un único
lugar obvio (el step placeholder de `product-tests`) donde pegar los
pasos reales de su stack.

## 6. Estrategia de tests

- **AC-1, AC-2, AC-7**: cubiertos por el nuevo test de pytest
  (`tests/test_ci_workflow.py` o extensión equivalente), que falla si
  falta cualquiera de los dos jobs, si `pytest -v` desaparece del job
  `circuit-tests`, o si el marcador de `product-tests` desaparece.
  Cubre el caso borde "estabilidad del test de estructura" de `spec.md`
  usando substrings estables, no indentación exacta.
- **AC-3, AC-4**: verificados manualmente viendo el check
  `product-tests` en verde en el CI de la propia PR de esta feature
  (evidencia reproducible: link al run de Actions en `test-report-N.md`
  de QA). Cubre el caso borde "`product-tests` no debe fallar por
  dependencias inexistentes" porque el runner de la PR de esta misma
  feature no tiene ningún stack de producto instalado.
- **AC-5, AC-6**: verificados por lectura directa de
  `AGENTS.md`/`docs/tecnica/ci-wiring-product-tests.md` (no requieren
  test automatizado: son texto de documentación). Cubre el caso borde
  "adopción downstream con branch protection ya configurada" mediante
  la advertencia explícita documentada.
- **AC-8, AC-9, AC-10, AC-11**: verificados por existencia y contenido
  no vacío de cada archivo, y por presencia del enlace exacto en la
  zona `FEATURE_LINKS` de ambos índices — mismo mecanismo que ya usa
  `Assert-FeatureContract` para toda feature del circuito.
- Los tests de circuito preexistentes (`tests/test_feature_contract_scripts.py`
  y el resto de `tests/`) deben seguir pasando sin modificación de sus
  aserciones existentes, dado que esta feature no toca ningún script
  `.ps1`.
