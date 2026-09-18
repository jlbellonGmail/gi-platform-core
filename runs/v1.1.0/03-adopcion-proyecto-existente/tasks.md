# Tasks: Adopción del circuito en un proyecto existente

- **T-01** — Escribir `docs/tecnica/adopcion-proyecto-existente.md` con
  una sección por cada uno de los 7 elementos del checklist (incluidas
  las 4 subsecciones de workflows), cada una con "Colisión probable" y
  "Estrategia de merge" concretas, siguiendo la tabla de referencia de
  `plan.md` sección 2.
  Verificación: el archivo existe, no está vacío, y contiene un
  encabezado identificable por cada uno de `.agentic/`, `scripts/`,
  `runs/`, `docs/tecnica/`, `docs/usuario/`, `AGENTS.md`, `ci.yml`,
  `docs.yml`, `post-hitl-merge-gate.yml`,
  `post-merge-close-feature.yml`, cada uno con contenido no genérico y
  al menos un nombre de archivo real del template mencionado
  explícitamente. Incluye también la sección de límites del script
  descripta en AC-6.
  Traza: AC-1, AC-6.

- **T-02** — Escribir `docs/usuario/adopcion-proyecto-existente.md`
  explicando propósito, cuándo usar la guía, cómo recorrer el checklist
  y cómo correr opcionalmente el script.
  Verificación: el archivo existe, no está vacío, y describe en
  lenguaje operativo (no de diseño) el propósito y el uso.
  Traza: AC-2.

- **T-03** — Implementar `scripts/check-adoption-conflicts.ps1` según el
  contrato de `plan.md` sección 2 (parámetro `-TargetPath`, validación
  de ruta, tabla interna de rutas conocidas por elemento, reporte
  agrupado, código de salida 0/1, sin escritura).
  Verificación manual: ejecutar el script contra un directorio temporal
  vacío (código de salida `0`, sin colisiones) y contra un directorio
  temporal con al menos un path conocido de cada categoría pre-creado
  (código de salida distinto de cero, colisiones listadas
  correctamente); confirmar que el directorio destino no cambia antes/
  después en ambos casos.
  Traza: AC-3, AC-4, AC-5.
  Depende de: T-01 (la tabla de rutas conocidas debe alinearse con el
  checklist redactado ahí).

- **T-04** — Escribir `tests/test_check_adoption_conflicts.py` cubriendo
  los casos de AC-7 (destino vacío, destino con colisiones, ruta
  inexistente, estado del destino sin cambios), siguiendo el patrón de
  `tests/test_agentic_sync_scripts.py`.
  Verificación: `pytest tests/test_check_adoption_conflicts.py -v`
  pasa en verde.
  Traza: AC-7.
  Depende de: T-03.

- **T-05** — Ejecutar `scripts/update-doc-indexes.ps1
  03-adopcion-proyecto-existente "Adopción de proyecto existente"` y
  confirmar los enlaces agregados.
  Verificación: `docs/tecnica/index.md` y `docs/usuario/index.md`
  contienen, dentro de `FEATURE_LINKS_START`/`FEATURE_LINKS_END`, un
  enlace exacto y único a `adopcion-proyecto-existente.md`.
  Traza: AC-9.
  Depende de: T-01, T-02.

- **T-06** — Escribir `runs/v1.1.0/03-adopcion-proyecto-existente/decision.md`
  con decisiones demostrables desde spec/plan/tasks/auditoría/
  implementación, incluida explícitamente la justificación de incluir
  el script en el alcance.
  Verificación: el archivo existe, no está vacío, y referencia
  decisiones concretas trazables a `spec.md`/`plan.md`.
  Traza: AC-10.

- **T-07** — Revisar el diff final de la rama contra `develop` para
  confirmar que no toca ningún archivo preexistente de `.agentic/`,
  `scripts/*.ps1` (fuera del nuevo script), `AGENTS.md` ni
  `.github/workflows/*.yml`.
  Verificación: `git diff --stat develop...HEAD` (o equivalente) lista
  únicamente archivos nuevos en `docs/tecnica/`, `docs/usuario/`,
  `scripts/check-adoption-conflicts.ps1`,
  `tests/test_check_adoption_conflicts.py`,
  `runs/v1.1.0/03-adopcion-proyecto-existente/`, más las ediciones acotadas de
  `docs/tecnica/index.md`/`docs/usuario/index.md`.
  Traza: AC-8.
  Depende de: T-01 a T-06.

- **T-08** — Correr la suite completa de tests del circuito.
  Verificación: `pytest -v` pasa en verde, sin regresiones en tests
  preexistentes.
  Traza: AC-7 (cobertura propia) y AC-8 (regresión: ningún test
  existente se ve afectado por archivos fuera de alcance).
  Depende de: T-04.
