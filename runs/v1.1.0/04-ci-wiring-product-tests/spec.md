# Spec: CI wiring product tests

## Identificacion

- Work unit: 04-ci-wiring-product-tests
- Modo: FEATURE

## Alcance

Incluye:

- Separar el job único `test` de `.github/workflows/ci.yml` en dos jobs
  top-level: `circuit-tests` (el pytest actual del circuito, sin cambios
  de comportamiento) y `product-tests` (job nuevo, placeholder, con un
  marcador inequívoco de dónde pegar el build/test real del stack
  cuando un proyecto real nazca de este template y lo defina).
- Documentar explícitamente si `product-tests` debe ser un check
  requerido/bloqueante en branch protection mientras es solo un
  placeholder, para que quede una referencia consistente para el
  checklist de branch protection de `05-operational-readiness-docs`
  (feature separada, no implementada acá).
- Actualizar la sección "CI/CD" de `AGENTS.md` para que describa los dos
  jobs reales en vez del job único `test` que ya no existe.
- Agregar verificación automatizada (test de circuito) de la estructura
  mínima del workflow actualizado.
- La documentación estándar de la feature (`docs/tecnica/`,
  `docs/usuario/`, `decision.md`, enlaces de índice).

Explícitamente NO incluye:

- Configurar branch protection real de GitHub (marcar checks como
  requeridos en la UI/API de GitHub). Es la feature
  `05-operational-readiness-docs`, que sí depende de la decisión tomada
  acá sobre si `product-tests` debe listarse como requerido.
- Agregar build/test real de ningún stack de producto: este template no
  tiene stack propio (ver "Stack" en `AGENTS.md`). El job `product-tests`
  queda deliberadamente vacío de contenido real.
- Tocar `post-hitl-merge-gate.yml`, `post-merge-close-feature.yml` ni
  `docs.yml`: ningún AC de esta spec requiere editarlos.
- Tocar `scripts/*.ps1`, `.agentic/` o el router de modelos.
- Agregar cualquier dependencia nueva de build o runtime, o cualquier
  entrada nueva en `docs/tecnica/arquitectura.md` sobre stack de
  producto: esta feature es exclusivamente reestructuración de CI del
  propio circuito.

## Contexto y fuentes

Fuentes consultadas y qué aportó cada una (ver "Política de fuentes y
trazabilidad" en `AGENTS.md`):

- **Ítem de `ROADMAP.md` (04-ci-wiring-product-tests)**: define el
  requisito funcional exacto — separar `ci.yml` en `circuit-tests`
  (obligatorio) y `product-tests` (marcador claro para agregar
  trivialmente el stack real). No trae bloque `Referencias:`.
- **Pedido humano adicional (no está en `ROADMAP.md`)**: aclara que
  `product-tests` debe quedar vacío/placeholder por ahora, y pide
  decidir explícitamente si debe ser requerido/bloqueante en branch
  protection ya, dejando esa decisión consistente con lo que espera el
  checklist de branch protection de `05-operational-readiness-docs`
  (feature separada).
- **`docs/producto/contexto-producto.md`**: existe pero todas sus
  secciones están "Por definir" — este template no tiene producto propio
  todavía. No aporta contexto funcional adicional a esta feature (es
  puramente de infraestructura del circuito, no de producto).
- **`AGENTS.md`**: sección "Stack" confirma que el template no tiene
  stack de producto fijo y que ningún agente debe asumir tecnología no
  declarada. Sección "CI/CD" describe el estado actual (`ci.yml` corre
  `pytest` sobre `tests/` en un único job, gate obligatorio) y anticipa
  que "se amplía con los tests de producto que correspondan cuando el
  stack real se defina — no antes": esta feature es exactamente esa
  ampliación estructural (el "dónde", no el "qué" del stack real).
- **`.claude/rules/`**: contiene solo `.gitkeep`, confirmado vacío. No
  aporta reglas de dominio adicionales.
- **`docs/tecnica/arquitectura.md`**: historial de decisiones de
  arquitectura (fuente canónica agéntica, JSON Schema, contexto de
  producto/CLARIFY). Ninguna decisión previa fija stack de producto ni
  restringe la estructura de `ci.yml`. Esta feature no agrega ninguna
  entrada nueva a este archivo porque no introduce backend, base de
  datos, integración externa ni dependencia de build.
- **`.github/workflows/ci.yml` (contenido real, leído completo)**: hoy
  tiene un único job `test` (`runs-on: ubuntu-latest`) que hace
  checkout, instala Python 3.12 con cache de pip, `pip install -r
  requirements-dev.txt` y `pytest -v`, y ya trae un comentario indicando
  dónde agregar pasos de producto en el futuro — esta feature formaliza
  ese comentario en un job separado real, no solo un comentario dentro
  del job existente.
- **`docs/tecnica/index.md` / `docs/usuario/index.md`**: confirman el
  formato exacto de enlace dentro de la zona
  `<!-- FEATURE_LINKS_START -->...<!-- FEATURE_LINKS_END -->`.
- **Código y tests existentes (`tests/`)**: no existe ningún test que
  valide hoy la estructura de `ci.yml`. El único precedente de test
  sobre contenido de un workflow es
  `test_workflow_yaml_is_valid` en `tests/test_feature_contract_scripts.py`,
  que hace aserciones de substring de texto plano sobre
  `post-merge-close-feature.yml` y `post-hitl-merge-gate.yml`, sin
  parsear YAML ni depender de una librería nueva (`requirements-dev.txt`
  no incluye `pyyaml`). Esta feature sigue ese mismo patrón para no
  introducir una dependencia de test nueva sin declararla en
  `docs/tecnica/arquitectura.md`.
- **Ambigüedad material identificada y resuelta vía Fase CLARIFY**: si
  `product-tests` debe ser status check requerido/bloqueante en branch
  protection mientras es solo un placeholder no tenía evidencia previa
  en el repo (branch protection no está configurada todavía;
  `05-operational-readiness-docs` sigue pendiente) y es una decisión de
  gobernanza sobre el circuito (afecta qué bloquea un merge hacia
  `develop`/`main`), no una convención técnica inequívocamente
  inferible de código, arquitectura, tests o reglas globales
  existentes. En el primer intento de esta spec se resolvió (de forma
  incorrecta) como supuesto propio del `analyst-agent`; `reviewer-agent`
  lo marcó como `rejected` en `audit-1.md` por deber pasar por Fase
  CLARIFY. Se elevó como pregunta concreta al humano y su respuesta
  quedó registrada en "Clarificaciones realizadas": es la base real de
  AC-5, no un supuesto propio.

## Criterios de aceptación

- **AC-1**: `.github/workflows/ci.yml` declara exactamente dos jobs
  top-level, `circuit-tests` y `product-tests`, ambos activados por los
  mismos triggers vigentes del workflow (`push`/`pull_request` a
  `develop` y `main`), sin condicionales que excluyan a ninguno de los
  dos en ningún evento.
- **AC-2**: El job `circuit-tests` reproduce exactamente el
  comportamiento funcional del job `test` actual (checkout, setup Python
  3.12 con cache de pip sobre `requirements-dev.txt`, `pip install -r
  requirements-dev.txt`, `pytest -v`), sin ningún cambio de
  comportamiento observable.
- **AC-3**: El job `product-tests` existe, corre siempre (no queda
  condicionado/salteado), y contiene un marcador inequívoco (bloque de
  comentario + estructura reconocible) que indica el único lugar donde
  pegar los pasos reales de build/test cuando el proyecto real que use
  este template defina su stack, referenciando explícitamente
  `docs/tecnica/arquitectura.md` como el lugar donde esa decisión de
  stack debe documentarse primero.
- **AC-4**: Mientras no exista stack de producto real, `product-tests`
  pasa en verde de forma determinística en un runner limpio (no depende
  de artefactos, paquetes ni herramientas de ningún stack todavía no
  definido), verificable viendo el check en verde en el CI de la propia
  PR de esta feature.
- **AC-5**: Queda documentado explícitamente, de forma consistente entre
  `docs/tecnica/ci-wiring-product-tests.md` y `AGENTS.md`, que
  `circuit-tests` y `product-tests` deben tratarse como igualmente
  obligatorios/bloqueantes (mismo nivel de exigencia) — decisión
  confirmada por el humano en Fase CLARIFY (ver "Clarificaciones
  realizadas"), no un supuesto propio —, como referencia directa para el
  checklist de branch protection que implementará
  `05-operational-readiness-docs`.
- **AC-6**: La sección "CI/CD" de `AGENTS.md` refleja los dos jobs reales
  (`circuit-tests`, `product-tests`), su propósito y su condición de
  obligatoriedad, en vez de describir un único job `test`.
- **AC-7**: Existe al menos un test de pytest en `tests/` que verifica la
  estructura mínima del workflow actualizado (presencia de los nombres
  exactos de ambos jobs, presencia del step `pytest -v` dentro de
  `circuit-tests`, presencia del marcador textual de `product-tests`),
  usando el mismo patrón de aserciones de texto plano ya usado en
  `tests/test_feature_contract_scripts.py::test_workflow_yaml_is_valid`,
  sin agregar ninguna dependencia nueva de parseo YAML.
- **AC-8**: Debe existir `docs/tecnica/ci-wiring-product-tests.md`, no
  vacío, con las decisiones de diseño/implementación relevantes
  (por qué dos jobs, por qué `product-tests` se documenta como
  requerido desde ya pese a estar vacío, forma exacta del marcador).
- **AC-9**: Debe existir `docs/usuario/ci-wiring-product-tests.md`, no
  vacío, con el propósito de la feature y cómo verla/usarla (cómo se ven
  los dos checks en GitHub Actions, qué hacer para agregar el stack real
  cuando exista).
- **AC-10**: Deben existir enlaces exactos y únicos a esos dos `.md` en
  la zona `FEATURE_LINKS` de `docs/tecnica/index.md` y
  `docs/usuario/index.md` respectivamente.
- **AC-11**: Debe existir `runs/v1.1.0/04-ci-wiring-product-tests/decision.md`
  con decisiones demostrables desde spec/plan/tasks/auditoría/
  implementación, sin afirmar aprobación de merge.

## Casos borde a contemplar

- **Adopción downstream con branch protection ya configurada**: un
  proyecto real que ya haya nacido de este template y configurado un
  status check requerido llamado `test` (nombre del job viejo) deberá
  actualizarlo a `circuit-tests` (y agregar `product-tests`) al adoptar
  esta feature. Se documenta como advertencia explícita en
  `docs/tecnica/ci-wiring-product-tests.md`; en este template en sí no
  hay branch protection configurada todavía (setup manual pendiente,
  ítem 05), así que no hay migración real que ejecutar acá.
- **`product-tests` no debe fallar por dependencias inexistentes**: el
  placeholder no debe invocar ninguna herramienta que dependa de
  artefactos de un stack todavía no definido (por ejemplo, no debe
  intentar `npm ci` sin `package.json`); debe limitarse a pasos que
  siempre tengan éxito.
- **Reemplazo futuro del placeholder**: cuando un proyecto real agregue
  su stack, debe reemplazar el step placeholder completo (no agregar
  pasos reales al lado dejando el placeholder), para que `product-tests`
  no quede ejecutando un `echo` inútil junto a los pasos reales.
- **Triggers compartidos**: ambos jobs deben seguir disparándose en
  exactamente los mismos eventos (`push`/`pull_request` a `develop` y
  `main`) que hoy dispara el job único, sin que un `if:` mal puesto deje
  a uno de los dos jobs corriendo solo en un subconjunto de eventos.
- **Estabilidad del test de estructura**: el nuevo test de pytest debe
  basarse en substrings estables (nombres de job, texto del marcador),
  no en indentación exacta del YAML, para no romperse con
  reformateos menores que no cambian el comportamiento del workflow.

## Supuestos

- **`product-tests` corre en `ubuntu-latest`**, igual que
  `circuit-tests` y el job actual, porque no hay ninguna decisión de
  stack/runner distinta documentada en `docs/tecnica/arquitectura.md`.
  Si el stack real que se agregue después requiere otro runner, ese
  cambio queda fuera de esta feature.
- **No se agrega ninguna dependencia de parseo YAML** (por ejemplo
  `pyyaml`) para testear `ci.yml`: se reutiliza el patrón ya existente de
  aserciones de texto plano de
  `tests/test_feature_contract_scripts.py::test_workflow_yaml_is_valid`,
  evitando declarar una decisión de arquitectura nueva que esta feature
  no necesita.
- **Ambos jobs corren en paralelo**, sin relación `needs:` entre ellos,
  porque son verificaciones independientes entre sí (una del circuito,
  otra placeholder de producto) y no hay ninguna razón funcional para
  serializarlas.

## Clarificaciones realizadas

- **Pregunta**: ¿`product-tests` debe ser status check
  requerido/bloqueante en branch protection desde ya, o solo cuando
  tenga contenido real de stack?
  **Respuesta del humano**: Requerido desde ya. Razón dada: el
  placeholder siempre pasa en verde, así que no bloquea a nadie hoy, y
  evita tener que acordarse de agregarlo a branch protection el día que
  el stack real llegue.

  Esta respuesta es la base real de AC-5 y del contenido correspondiente
  de `docs/tecnica/ci-wiring-product-tests.md` y de la sección "CI/CD"
  de `AGENTS.md` — ya no es un supuesto propio del `analyst-agent` (en
  el primer intento de esta spec sí se había tratado como tal, lo cual
  motivó el `rejected` de `audit-1.md`).

## Decisiones pendientes bloqueantes

Ninguna.
