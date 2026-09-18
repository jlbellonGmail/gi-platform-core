# Plan: Adopción del circuito en un proyecto existente

## 1. Arquitectura afectada

Esta feature es documentación + un script nuevo, autocontenida y
aditiva. Toca:

- `docs/tecnica/adopcion-proyecto-existente.md` (nuevo).
- `docs/usuario/adopcion-proyecto-existente.md` (nuevo).
- `scripts/check-adoption-conflicts.ps1` (nuevo).
- `tests/test_check_adoption_conflicts.py` (nuevo).
- `docs/tecnica/index.md` y `docs/usuario/index.md` (edición acotada a
  la zona `FEATURE_LINKS`, vía `scripts/update-doc-indexes.ps1`, sin
  tocar el resto de su contenido).
- `runs/v1.1.0/03-adopcion-proyecto-existente/` (spec/plan/tasks/auditoría/
  decision/reportes propios de esta feature).

Explícitamente NO toca (AC-8): `.agentic/` (ningún archivo),
`scripts/*.ps1` preexistentes, `AGENTS.md`, ni ninguno de los 4
`.github/workflows/*.yml`. El script nuevo no se invoca desde ningún
workflow ni desde otro script del circuito: es una herramienta standalone
de uso manual por quien adopta el template en otro repositorio.

## 2. Componentes y contratos nuevos/modificados

### `docs/tecnica/adopcion-proyecto-existente.md`

Contrato: un documento Markdown con un encabezado `##` por cada uno de
los 7 elementos del checklist, y dentro del encabezado de
`.github/workflows/`, un `###` por cada uno de los 4 archivos. Cada
sección/subsección sigue el formato fijo:

```markdown
## <elemento>

**Colisión probable**: <descripción concreta, no genérica>

**Estrategia de merge**: <fusionar / renombrar / mantener ambos /
reemplazar / extender job-step>, con ejemplo usando nombres reales de
archivo.
```

Contenido mínimo por elemento (referencia para quien implemente, no
prosa final — el redactado real queda a criterio del builder siempre
que cumpla AC-1):

| Elemento | Colisión probable | Estrategia sugerida |
|---|---|---|
| `.agentic/` | Repo destino ya trae una adopción previa/desactualizada de este mismo template | Reemplazar con la versión del template salvo que el destino haya customizado `roles/*.md`/`agents.json`; en ese caso, diff manual antes de sobrescribir |
| `scripts/` | Colisión de **nombre de archivo** puntual (ej. si el destino ya tiene un `workunit-lib.ps1` propio) — la carpeta en sí casi nunca colisiona en contenido | Copiar los 11+ scripts del circuito junto a los del destino (unión); si hay colisión de nombre exacto, renombrar el script del destino primero |
| `runs/` | Nombre genérico ya usado por el destino para otro propósito (salidas de builds, corridas de tests, ML) | Mover el contenido preexistente del destino a otro nombre; `runs/` queda reservado para el circuito porque está hardcodeado en `scripts/*.ps1` |
| `docs/tecnica/` | El destino ya tiene su propia carpeta de docs técnicas con archivos reales | Fusionar: conservar archivos existentes del destino, agregar `index.md` (con marcadores `FEATURE_LINKS`), `arquitectura.md`, `circuito-agentico.md` del template |
| `docs/usuario/` | Igual que arriba, para documentación de usuario | Fusionar igual que `docs/tecnica/`: agregar `index.md` y `circuito-agentico.md` del template sin pisar contenido existente |
| `AGENTS.md` | El destino ya tiene su propio `AGENTS.md` (o instrucciones equivalentes para agentes IA) | Fusión por sección: copiar tal cual las secciones "del circuito" (Workflow, Circuito, Contexto de producto y bootstrap, Modo MILESTONE, Git, Versionado, CI/CD, Herramientas, Artefactos, Formato de veredicto, Configuración de modelos, Reglas adicionales, Reglas de dominio, Setup manual); reemplazar "Stack"/"Estructura del repo"/"Propósito del producto" con el contenido real del destino |
| `ci.yml` | El destino ya tiene su propio workflow de CI (mismo nombre u otro) con sus propios pasos de build/test | Agregar el paso `pytest -v` del circuito como paso/job adicional dentro del `ci.yml` existente, sin reemplazar los pasos del destino; vigilar versión de Python pineada en `setup-python` |
| `docs.yml` | El destino ya despliega documentación con otro generador (Jekyll, Docusaurus, VuePress) a GitHub Pages | Punto de decisión explícito del equipo: mantener ambos workflows apuntando a rutas/carpetas distintas, o migrar a MkDocs; no se resuelve automáticamente |
| `post-hitl-merge-gate.yml` | Colisión de nombre de archivo sin relación semántica con automatización propia del destino | Renombrar el archivo del template (los nombres de workflow de GitHub Actions son arbitrarios; el wiring real es por contenido, no por nombre) |
| `post-merge-close-feature.yml` | Igual que el anterior | Igual que el anterior |

Responde a: AC-1, AC-6 (la tabla de "Colisión probable"/"Estrategia" es
la base de la sección de límites del script).

### `docs/usuario/adopcion-proyecto-existente.md`

Contrato: Markdown orientado a operación, sin detalle de implementación:
para qué sirve, cuándo usarla, cómo recorrer el checklist técnico paso a
paso, y cómo correr opcionalmente el script (comando exacto, qué
significa cada código de salida). Responde a: AC-2.

### `scripts/check-adoption-conflicts.ps1`

Contrato:

```powershell
param(
    [string] $TargetPath = "."
)
```

Comportamiento:

1. Resuelve `$TargetPath` a ruta absoluta; si no existe o no es un
   directorio, termina con error explícito (código de salida distinto
   de cero) sin reportar "sin colisiones" (cubre el caso borde de ruta
   inválida).
2. Mantiene una tabla interna de rutas conocidas agrupadas por elemento
   del checklist, alineada manualmente con la tabla de la sección
   anterior (ver "Supuestos" de `spec.md` sobre este acoplamiento
   manual): para `.agentic/`, la carpeta completa; para `scripts/`, los
   11 nombres de archivo reales del circuito (`resolve-agentic-
   model.ps1`, `sync-agentic-adapters.ps1`, `update-doc-indexes.ps1`,
   `wait-pr-ci.ps1`, `start-work-unit.ps1`, `workunit-lib.ps1`, `local-
   feature-reconcile.ps1`, `close-feature.ps1`, `feature-contract.ps1`,
   `complete-approved-pr.ps1`, `ready-for-pr.ps1`); para `runs/`, la
   carpeta; para `docs/tecnica/`, `index.md`/`arquitectura.md`/
   `circuito-agentico.md`; para `docs/usuario/`, `index.md`/
   `circuito-agentico.md`; para `AGENTS.md`, el archivo; para
   `.github/workflows/`, los 4 archivos individualmente.
3. Para cada ruta conocida, verifica existencia con `Test-Path` sobre
   `$TargetPath` (sin leer ni escribir contenido).
4. Imprime el reporte agrupado por elemento (existe / no existe por
   ruta).
5. Devuelve código de salida `0` si ninguna ruta conocida existe en el
   destino, y código de salida `1` si al menos una existe.

No requiere `git`, no requiere que `$TargetPath` sea un repositorio, no
lee ni compara contenido de archivos. Responde a: AC-3, AC-4, AC-5.

### `tests/test_check_adoption_conflicts.py`

Contrato: sigue el patrón de `tests/test_agentic_sync_scripts.py`
(detección de `powershell.exe`/`pwsh` vía `shutil.which`, invocación con
`subprocess.run([..., "-File", str(SCRIPT), *args], cwd=..., env=...,
capture_output=True)`), usando `tmp_path` de pytest como directorio
destino temporal. Casos mínimos:

- Directorio destino vacío → código de salida `0`, sin colisiones
  reportadas.
- Directorio destino con al menos una ruta conocida de cada categoría
  pre-creada (archivos/carpetas vacíos o con contenido dummy, el
  contenido es irrelevante porque el script no lo lee) → código de
  salida `1`, reporte lista esas rutas específicas.
- Ruta destino inexistente → código de salida distinto de cero, mensaje
  de error explícito.
- El estado del directorio destino (listado de archivos/carpetas antes
  y después) es idéntico en ambos casos anteriores.

Responde a: AC-7.

### Índices de documentación

`scripts/update-doc-indexes.ps1 03-adopcion-proyecto-existente
"Adopción de proyecto existente"` agrega el enlace a
`docs/tecnica/index.md` y `docs/usuario/index.md` dentro de
`FEATURE_LINKS_START`/`FEATURE_LINKS_END`, reutilizando
`Get-FeatureInfo`/`Update-DocsIndex`/`Assert-IndexLink` ya existentes en
`scripts/feature-contract.ps1`, sin tocar el resto del contenido de
ambos índices. Responde a: AC-9.

### `runs/v1.1.0/03-adopcion-proyecto-existente/decision.md`

Contrato: el archivo canónico habitual (ver `AGENTS.md`, sección
"Artefactos"), con decisiones demostrables desde spec/plan/tasks/
auditoría/implementación, incluida explícitamente la justificación de
incluir el script en el alcance. Responde a: AC-10.

## 3. Compatibilidad y migración

No hay nada que migrar: esta feature no cambia el comportamiento de
ningún script, workflow ni agente existentes de este repositorio. Es
puramente aditiva (documentación nueva + un script nuevo standalone que
ningún otro componente invoca). No hay artefactos previos de otras
features que este cambio pueda romper, y `scripts/check-adoption-
conflicts.ps1` no participa del contrato validado por
`Assert-FeatureContract`/`Assert-WorkUnitContract` (no es un requisito
del circuito, es una herramienta de apoyo opcional para terceros que
adoptan el template).

## 4. Dependencias

Ninguna dependencia nueva de build ni runtime. El script nuevo reutiliza
PowerShell, ya declarado como herramienta requerida en `AGENTS.md`
("Herramientas locales requeridas"). Los tests nuevos reutilizan
`pytest`, ya declarado en `requirements-dev.txt`, y el mismo patrón de
invocación de scripts PowerShell desde `subprocess` ya usado en
`tests/test_agentic_sync_scripts.py` — no se agrega ningún paquete
Python nuevo. No se agrega ninguna entrada nueva a
`docs/tecnica/arquitectura.md` porque no se introduce backend, base de
datos, integración externa ni dependencia de build.

## 5. Impacto operacional

- Nuevo comando disponible para quien opera una adopción:
  `powershell -NoProfile -ExecutionPolicy Bypass -File
  .\scripts\check-adoption-conflicts.ps1 -TargetPath <ruta-destino>`.
- Nueva lectura obligatoria antes de mezclar el template sobre un
  proyecto existente: `docs/tecnica/adopcion-proyecto-existente.md` (para
  quien mantiene el código) y `docs/usuario/adopcion-proyecto-
  existente.md` (para quien ejecuta la adopción).
- No cambia ningún comando ni interfaz existente del circuito
  (`ready-for-pr.ps1`, `start-work-unit.ps1`, etc. quedan idénticos).
- No agrega pasos al circuito de esta u otras features del propio
  template: el script y la guía son para uso *externo*, contra un
  repositorio destino distinto de este.

## 6. Estrategia de tests

- `tests/test_check_adoption_conflicts.py` (nuevo): cubre AC-3, AC-4,
  AC-5 y los casos borde de "ruta destino inexistente" y "estado del
  destino sin cambios" de `spec.md`, siguiendo el patrón ya validado en
  `tests/test_agentic_sync_scripts.py` para invocar `.ps1` desde pytest
  de forma portable (`powershell.exe` en Windows, `pwsh` en otras
  plataformas, con `pytest.skip` si no está disponible).
- Regresión: correr la suite completa (`pytest -v`) para confirmar que
  agregar el script nuevo y los cambios de índice no rompen ningún test
  existente (cubre AC-8 desde el ángulo de "no tocar nada fuera de
  alcance" — si algún test existente fallara, señalaría que se tocó algo
  fuera del alcance declarado).
- No aplica una estrategia de test automatizado para el contenido
  narrativo de `docs/tecnica/adopcion-proyecto-existente.md` ni
  `docs/usuario/adopcion-proyecto-existente.md` (AC-1, AC-2, AC-6): son
  verificación manual reproducible por lectura directa del archivo
  contra los criterios de aceptación (presencia de las 7+4 secciones,
  no vacío, ejemplos con nombres reales de archivo).
