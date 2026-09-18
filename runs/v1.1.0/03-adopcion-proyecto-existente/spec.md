# Spec: Adopción del circuito en un proyecto existente

## Identificación

- Work unit: 03-adopcion-proyecto-existente
- Modo: FEATURE
- Items (solo MILESTONE): N/A

## Alcance

Incluye:

1. `docs/tecnica/adopcion-proyecto-existente.md`: checklist de colisiones
   probables al mezclar este template sobre un repositorio que ya tiene
   código propio, cubriendo exactamente los 7 elementos que enumera el
   ítem de `ROADMAP.md`: `.agentic/`, `scripts/`, `runs/`,
   `docs/tecnica/`, `docs/usuario/`, `AGENTS.md`, y los 4 workflows de
   `.github/workflows/` (`ci.yml`, `docs.yml`,
   `post-hitl-merge-gate.yml`, `post-merge-close-feature.yml`) tratados
   individualmente. Para cada elemento: qué colisión concreta es probable
   (no una advertencia genérica) y una guía de merge accionable (fusionar,
   renombrar, mantener ambos, reemplazar, o extender un job/step
   existente), con ejemplos que usan nombres reales de archivo de este
   propio template.
2. `docs/usuario/adopcion-proyecto-existente.md`: guía de uso de ese
   checklist para quien ejecuta la adopción (cuándo consultarlo, cómo
   recorrerlo, cómo apoyarse opcionalmente en el script del punto 3).
3. `scripts/check-adoption-conflicts.ps1`: script opcional, de solo
   lectura, que —corrido contra un directorio destino— reporta qué rutas
   conocidas definidas por este template ya existen ahí, agrupadas por
   elemento del checklist del punto 1. Se decide **incluirlo en el
   alcance** de esta feature (ver "Contexto y fuentes" para la
   justificación de esta decisión, delegada explícitamente por el pedido
   humano), acotado a detección de existencia de rutas — no hace diff de
   contenido ni usa historial de git.
4. Los dos `.md` de documentación técnica/usuario, `decision.md` y los
   enlaces de índice exigidos siempre por el circuito para esta propia
   feature (`03-adopcion-proyecto-existente`).

Explícitamente NO incluye:

- Modificar ningún archivo existente de `.agentic/`, `scripts/*.ps1`
  preexistentes, `AGENTS.md` o los 4 workflows de `.github/workflows/`
  de **este** repositorio — la feature es aditiva (documentación nueva +
  script nuevo), no una migración real de ningún proyecto concreto.
- Ejecutar la adopción sobre ningún repositorio destino real: no hay tal
  repositorio en el alcance de este trabajo; el resultado es una guía y
  una herramienta reutilizables para cuando alguien adopte el template.
- Automatizar el merge en sí (copiar, fusionar o sobrescribir archivos
  automáticamente en un destino). El script del punto 3 solo detecta y
  reporta; la resolución de cada colisión la hace el humano siguiendo el
  checklist.
- Diff de contenido, comparación semántica de archivos o uso de
  historial de git para inferir qué existía "antes" de mezclar el
  template en el destino. Ver justificación en "Contexto y fuentes".
- Soporte a hosting distinto de GitHub (GitLab, Bitbucket, Azure DevOps,
  etc.) para los 4 workflows: la guía asume GitHub Actions + `gh` CLI,
  ya asumido en el resto de `AGENTS.md` ("Herramientas locales
  requeridas", "CI/CD"). Se documenta como límite explícito, no se
  generaliza a otros hostings.
- `docs/producto/contexto-producto.md` como elemento propio del
  checklist: el ítem de `ROADMAP.md` enumera exactamente 7 elementos y
  no lo incluye. Se lo menciona en la doc solo como nota adyacente si
  ayuda a la claridad, no como un elemento del checklist con su propia
  guía de merge.
- Cambiar `.github/workflows/ci.yml` para separar jobs
  `circuit-tests`/`product-tests`: eso es el ítem `04-ci-wiring-product-
  tests` de `ROADMAP.md`, ya identificado como trabajo relacionado pero
  fuera de esta feature. Esta spec documenta la estrategia de merge de
  `ci.yml` contra la estructura **actual** (un solo job `test`), con una
  nota de que la separación futura simplificará ese merge.

## Contexto y fuentes

Este template (`AGENTS.md`, sección "Proyecto: template") es
explícitamente reutilizable: está pensado para arrancar circuitos nuevos,
pero el ítem `03-adopcion-proyecto-existente` de `ROADMAP.md` reconoce que
la ruta real más común no es un repositorio vacío, sino un proyecto
existente con su propio código, su propio `AGENTS.md` (o equivalente),
su propia CI y potencialmente sus propias carpetas `scripts/`, `runs/`
o `docs/`. Sin una guía explícita de colisiones, adoptar el circuito
arriesga sobrescribir en silencio código o configuración real del
proyecto destino.

Fuentes consultadas y qué aportó cada una, según la precedencia de
`AGENTS.md`:

1. **Ítem de `ROADMAP.md`** (máxima precedencia aplicable aquí): fija de
   forma exacta y cerrada los 7 elementos a cubrir en el checklist, y
   deja explícitamente delegada al analyst la decisión de incluir o no
   el script de detección ("Decide vos, como analyst, si este script
   entra en el alcance..."). Esto no es una ambigüedad material: es una
   decisión técnica que el propio pedido humano autoriza a tomar sin
   volver a preguntar.
2. **`docs/producto/contexto-producto.md`**: existe en el repo pero
   todas sus secciones están "Por definir" — este template no tiene
   producto propio todavía. No aporta reglas de negocio ni restricciones
   específicas para esta feature; se trata como contexto vacío, tal como
   prevé `AGENTS.md`.
3. **`AGENTS.md` completo**: fuente principal de qué hace cada elemento
   del checklist (estructura del repo, los 10 pasos del circuito,
   contrato de artefactos, Modo MILESTONE, herramientas locales
   requeridas, CI/CD, setup manual) y de las reglas de dominio que
   ninguna guía de adopción puede contradecir (no inventar contenido de
   negocio, no asumir stack no declarado).
4. **`.claude/rules/`**: confirmado vacío (solo `.gitkeep`); no aporta
   reglas adicionales.
5. **`docs/tecnica/arquitectura.md`**: dos decisiones ya tomadas
   relevantes para el checklist de `.agentic/` — que ese directorio es
   la fuente canónica multiherramienta con adaptadores generados, y que
   el contexto de producto/Fase CLARIFY ya están integrados en
   `analyst-agent`/`reviewer-agent`/`builder-agent` (no hay un sexto
   agente ni un `MODE` nuevo que la guía de adopción deba explicar por
   separado).
6. **`docs/tecnica/circuito-agentico.md`**: detalla el contenido exacto
   de `.agentic/` (`roles/`, `agents.json`, `models.json`, `mcp.json`,
   `schemas/`, `run.example.yaml`), los adaptadores generados que nunca
   deben tocarse a mano, y el comportamiento real del gate post-HITL —
   usado para escribir la guía de merge de `.agentic/` y de
   `post-hitl-merge-gate.yml` con precisión.
7. **Código y estructura real del repo** (inspeccionados directamente):
   contenido exacto de `scripts/*.ps1` (11 scripts nombrados
   específicamente), `.github/workflows/*.yml` (4 archivos, sus
   triggers y jobs reales), `docs/tecnica/index.md` y
   `docs/usuario/index.md` (formato exacto de los marcadores
   `FEATURE_LINKS_START`/`FEATURE_LINKS_END` que
   `scripts/update-doc-indexes.ps1` edita), y `tests/*.py` (patrón ya
   usado en `tests/test_agentic_sync_scripts.py` para invocar scripts
   PowerShell desde pytest con detección de `powershell.exe`/`pwsh`).

**Justificación de incluir el script en el alcance** (decisión delegada
por el pedido humano, no ambigüedad material): un detector de existencia
de rutas conocidas es de complejidad acotada (sin diff de contenido ni
dependencia de historial de git), sigue el mismo patrón que el resto de
`scripts/*.ps1` (PowerShell, testeado con pytest), y aporta valor real
repetible como pre-chequeo antes de mezclar el template o como
post-chequeo para confirmar qué quedó pisado. Extender el script a
comparación semántica de contenido o inferencia basada en historial de
git se descarta explícitamente por desproporcionado frente al valor
(requeriría asumir que el destino tiene el template como remoto/subtree
accesible, algo que no se puede garantizar en un repositorio destino
genérico) — se documenta como límite explícito del script, no como
trabajo pendiente oculto.

## Criterios de aceptación

- **AC-1**: Existe `docs/tecnica/adopcion-proyecto-existente.md`, no
  vacío, con una sección dedicada a cada uno de los 7 elementos del
  ítem de `ROADMAP.md` (`.agentic/`, `scripts/`, `runs/`,
  `docs/tecnica/`, `docs/usuario/`, `AGENTS.md`, y una subsección por
  cada uno de los 4 workflows de `.github/workflows/`: `ci.yml`,
  `docs.yml`, `post-hitl-merge-gate.yml`,
  `post-merge-close-feature.yml`). Cada sección describe explícitamente
  (a) qué colisión concreta es probable para ese elemento y (b) una
  guía de merge accionable (fusionar, renombrar, mantener ambos,
  reemplazar, o extender un job/step existente), con al menos un
  ejemplo que use nombres reales de archivo de este template (por
  ejemplo, nombrar explícitamente `ready-for-pr.ps1` o
  `workunit-lib.ps1` al hablar de `scripts/`, no solo "los scripts del
  template").
- **AC-2**: Existe `docs/usuario/adopcion-proyecto-existente.md`, no
  vacío, dirigido a quien ejecuta la adopción (no a quien mantiene el
  código): explica para qué sirve esta guía, cuándo consultarla (antes o
  durante de mezclar este template sobre un proyecto existente), cómo
  recorrer el checklist de AC-1, y cómo correr opcionalmente
  `scripts/check-adoption-conflicts.ps1` como apoyo.
- **AC-3**: Existe `scripts/check-adoption-conflicts.ps1` que acepta un
  parámetro de ruta destino (por defecto el directorio actual desde el
  que se invoca) y, sin requerir que esa ruta sea un repositorio git ni
  que el template ya esté mezclado ahí, reporta qué rutas conocidas
  definidas por el template (correspondientes a los 7 elementos del
  checklist de AC-1) ya existen en ese destino.
- **AC-4**: La salida del script agrupa los resultados por elemento del
  checklist (mismo agrupamiento que AC-1), distingue claramente qué
  rutas existen (colisión potencial) de cuáles no, y el script termina
  con código de salida `0` cuando no detecta ninguna colisión y con
  código de salida distinto de cero cuando detecta al menos una.
- **AC-5**: El script es de solo lectura: no crea, modifica ni borra
  ningún archivo o directorio dentro de la ruta destino analizada,
  verificable comparando el estado del directorio destino antes y
  después de ejecutarlo.
- **AC-6**: `docs/tecnica/adopcion-proyecto-existente.md` documenta
  explícitamente los límites de `scripts/check-adoption-conflicts.ps1`:
  no compara contenido ni hace diff, no distingue si un archivo
  detectado es idéntico al del template o solo comparte el nombre, no
  usa historial de git para inferir qué existía antes de mezclar el
  template, y no resuelve ninguna colisión automáticamente — el
  checklist de AC-1 sigue siendo la fuente de la guía de merge.
- **AC-7**: Existen tests de pytest en
  `tests/test_check_adoption_conflicts.py`, siguiendo el patrón de
  invocación de scripts PowerShell ya usado en
  `tests/test_agentic_sync_scripts.py` (detección de
  `powershell.exe`/`pwsh`, `subprocess.run` con `-File`), que cubren al
  menos: (a) un directorio destino vacío no reporta ninguna colisión y
  termina en código de salida `0`; (b) un directorio destino con al
  menos una ruta conocida de cada categoría del checklist pre-creada
  reporta esas colisiones específicas y termina en código de salida
  distinto de cero; (c) el contenido del directorio destino queda
  exactamente igual antes y después de la ejecución en ambos casos.
- **AC-8**: El diff final de esta feature no modifica ningún archivo
  preexistente de `.agentic/`, `scripts/*.ps1` (fuera de agregar el
  nuevo `scripts/check-adoption-conflicts.ps1`), `AGENTS.md` ni
  `.github/workflows/*.yml` de este repositorio — solo agrega
  documentación nueva, un script nuevo, un test nuevo y los artefactos
  de `runs/v1.1.0/03-adopcion-proyecto-existente/`.
- **AC-9**: Existen enlaces exactos y únicos a
  `adopcion-proyecto-existente.md` en la zona `FEATURE_LINKS` de
  `docs/tecnica/index.md` y de `docs/usuario/index.md`, agregados con
  `scripts/update-doc-indexes.ps1 03-adopcion-proyecto-existente
  "<Título>"`.
- **AC-10**: Existe `runs/v1.1.0/03-adopcion-proyecto-existente/decision.md`,
  no vacío, con decisiones demostrables desde spec/plan/tasks/auditoría/
  implementación (incluida explícitamente la decisión de incluir el
  script de detección en el alcance), sin afirmar aprobación de merge.

## Casos borde a contemplar

- **`runs/` es un nombre genérico**: un proyecto destino puede ya tener
  una carpeta `runs/` para un propósito no relacionado (salidas de
  benchmarks, corridas de entrenamiento, etc.). A diferencia de otros
  elementos, `runs/` está profundamente referenciado por nombre fijo en
  `scripts/*.ps1` y en `AGENTS.md`; renombrarlo requeriría cambios de
  código fuera del alcance de esta feature, así que la guía debe dejar
  explícito que la opción realista es mover el contenido preexistente
  del destino a otro nombre, no renombrar la carpeta del circuito.
- **`AGENTS.md` ya existe con contenido propio del proyecto** (stack,
  convenciones, u otro sistema de instrucciones para agentes IA): un
  reemplazo directo destruye contexto real del proyecto. La guía debe
  distinguir qué secciones son "del circuito" (no negociables, se
  copian tal cual) de cuáles son "del proyecto" (Stack, Estructura del
  repo, Propósito del producto) y deben conservarse con el contenido
  real del destino.
- **`ci.yml` ya existe con build/test propios del destino**: sobrescribir
  pierde cobertura real. La guía debe indicar agregar el paso/job de
  `pytest` del circuito sin reemplazar los pasos existentes, y señalar
  el riesgo de versiones de Python en conflicto entre el `setup-python`
  del destino y el `3.12` que usa el template.
- **`docs.yml` ya existe con otro generador de sitio** (Jekyll,
  Docusaurus, VuePress): la guía no puede resolver esto de forma
  automática — documenta el punto de decisión (mantener ambos
  workflows apuntando a rutas distintas, o migrar el sitio del destino a
  MkDocs) como algo que el equipo que adopta debe decidir explícitamente.
- **Colisión de nombre de archivo sin relación semántica** en
  `post-hitl-merge-gate.yml` / `post-merge-close-feature.yml` (el
  destino ya tiene un workflow con ese nombre para otra cosa): dado que
  los nombres de archivo de GitHub Actions son arbitrarios y estos dos
  workflows se referencian entre sí y con los scripts por contenido, no
  por nombre de archivo, renombrar el archivo del template es una
  estrategia segura sin tocar más wiring.
- **Destino sin rama `develop`**, o con un único branch por defecto: los
  4 workflows referencian `develop`/`main` explícitamente; la guía debe
  remitir al bloque "Setup manual" de `AGENTS.md` antes de copiar los
  workflows.
- **Destino hospedado fuera de GitHub**: los 4 workflows y `gh` CLI
  asumen GitHub. La guía debe señalarlo como límite explícito, no
  intentar generalizar.
- **Ruta destino inexistente o no es un directorio** al correr
  `scripts/check-adoption-conflicts.ps1`: el script debe terminar con
  error explícito, no reportar "sin colisiones" por defecto.
- **Colisión de nombre de archivo dentro de `scripts/`** (el destino ya
  tiene, por ejemplo, un script propio llamado igual que uno del
  circuito, aunque sea coincidencia): la guía debe indicar renombrar el
  script del destino (o el del template, evaluando impacto en
  `AGENTS.md`/otros scripts que lo invocan por nombre) antes de copiar,
  y el script de detección debe reportarlo igual que cualquier otra
  colisión, sin intentar decidir cuál de los dos archivos "gana".
- **Adopción parcial previa**: si el destino ya tiene mezclada una parte
  del template (por ejemplo `.agentic/` pero no `scripts/`), el script
  debe reportar la existencia real path por path, sin asumir que un
  estado parcial es "ya adoptado" ni "no adoptado".

## Supuestos

- **Hosting GitHub ya asumido por el circuito**: `AGENTS.md` ya requiere
  `gh` CLI y da por sentado GitHub Actions en toda la sección "CI/CD" y
  "Herramientas locales requeridas". Esta feature no introduce esa
  asunción: la hereda, y por eso documenta explícitamente que la guía de
  adopción de los 4 workflows no cubre otros hostings.
- **PowerShell/pwsh como herramienta ya requerida independientemente del
  stack del destino**: igual que el resto de `scripts/*.ps1`,
  `scripts/check-adoption-conflicts.ps1` se implementa en PowerShell,
  consistente con `AGENTS.md` ("Herramientas locales requeridas") y con
  el patrón de tests ya usado en `tests/test_agentic_sync_scripts.py`.
- **Detección de colisiones limitada a existencia de rutas** (sin diff
  de contenido ni historial de git): decisión técnica delegada
  explícitamente por el pedido humano ("Opcional... decide vos"), no una
  ambigüedad material. Se documenta como límite explícito del script en
  AC-6, no como trabajo pendiente oculto.
- **La lista de rutas que conoce el script se mantiene manualmente
  alineada con el checklist de `docs/tecnica/adopcion-proyecto-
  existente.md`** (no se genera parseando el Markdown en tiempo de
  ejecución): este template no tiene tooling de parsing de documentación
  existente, y agregarlo sería desproporcionado para una lista fija de
  ~7 categorías. Se documenta el acoplamiento manual como riesgo
  conocido a mantener si el checklist cambia en el futuro.
- **Formato de spec vigente**: se usa la plantilla de `spec.md` con
  "Identificación", "Contexto y fuentes", "Supuestos", "Clarificaciones
  realizadas" y "Decisiones pendientes bloqueantes" ya adoptada en
  `AGENTS.md`/`analyst-agent` tras la feature `33f8bca`, aunque las
  specs de features previas (`00`-`02`) usaron un formato anterior sin
  esas secciones — no se retrofitean specs ya cerradas.

## Clarificaciones realizadas

Ninguna. La única decisión con más de una respuesta razonable (si
incluir el script de detección de colisiones) fue delegada
explícitamente al analyst por el propio pedido humano, no quedó como
ambigüedad material sin resolver.

## Decisiones pendientes bloqueantes

Ninguna.
