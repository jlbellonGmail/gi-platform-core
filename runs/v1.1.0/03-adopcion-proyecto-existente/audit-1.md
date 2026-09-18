```yaml
status: approved
attempt: 1
feedback:
  - "No bloqueante: ni AC-3/AC-4/AC-5 ni el plan (sección 'scripts/check-adoption-conflicts.ps1') ni los casos borde de spec.md contemplan qué hace el script si `$TargetPath` existe pero no es accesible (permiso denegado, unidad de red desconectada, etc.). `Test-Path` en PowerShell típicamente devuelve `$false` ante un acceso denegado en vez de lanzar excepción, lo que podría reportar 'sin colisiones' de forma engañosa en vez de 'no se pudo inspeccionar'. Sugiero que builder-agent lo considere al implementar T-03, pero no amerita rechazar esta spec: el resto de los casos borde (ruta inexistente, colisión de nombre, adopción parcial, hosting no-GitHub, `runs/` genérico, `AGENTS.md` con contenido propio) están cubiertos con precisión y accionabilidad."
  - "No bloqueante: confirmar en la implementación real que el criterio de AC-1 'un ejemplo con nombres reales de archivo' para cada uno de los 7 elementos efectivamente nombra un archivo real distinto por elemento (la tabla de referencia de plan.md ya lo hace para todos, así que alcanza con que builder-agent no la resuma de forma genérica al redactar prosa)."
```

## Auditoría: 03-adopcion-proyecto-existente (intento 1)

### Identificación y modo
- `spec.md` declara Work unit `03-adopcion-proyecto-existente`, Modo `FEATURE`. Verificado: no existe `runs/milestone-*/work-unit.json` en el worktree, por lo tanto el modo declarado es consistente con lo que realmente se audita (no hay manifest de Milestone).

### Criterios de aceptación (verificabilidad)
- AC-1 a AC-10 son concretos y verificables: enumeran archivos exactos, exit codes exactos, secciones exactas, y en varios casos ejemplos de verificación reproducible (`pytest tests/test_check_adoption_conflicts.py -v`, `git diff --stat develop...HEAD`). No encontré criterios vagos tipo "documentación adecuada" sin más — cada AC dice qué contenido concreto debe existir.
- AC-1 y AC-6 en particular fijan contenido mínimo verificable (nombres reales de archivo del template, límites explícitos del script) que evita que la doc quede genérica.

### Límites de alcance
- La sección "Alcance" tiene un bloque "Explícitamente NO incluye" extenso y específico (no migración real, no automatiza merge, no diff de contenido/historial git, no otros hostings, no toca `docs/producto/contexto-producto.md` como elemento del checklist, no reestructura `ci.yml` — delegado a `04-ci-wiring-product-tests`). Los límites son claros y no dejan ambigüedad sobre qué se construye.

### Casos borde
- Cubren lo esperable para este tipo de cambio: nombre genérico de carpeta (`runs/`), `AGENTS.md` preexistente con contenido de proyecto real, CI/docs.yml con generador o pipeline propio del destino, colisión de nombre sin relación semántica en workflows, ausencia de rama `develop`, hosting no-GitHub, ruta destino inválida, colisión de nombre en `scripts/`, adopción parcial previa. Cubre bien "errores" y "datos inválidos" (ruta inexistente). No aplica responsive/accesibilidad (no hay UI) ni concurrencia real (script de una sola invocación local, síncrono). El único hueco es el de permisos de filesystem, señalado arriba como no bloqueante.

### Supuestos
- Los cuatro supuestos declarados (hosting GitHub ya asumido, PowerShell/pwsh ya requerido, detección limitada a existencia de rutas por delegación explícita del pedido humano, acoplamiento manual de la lista de rutas del script con el checklist) son técnicos e inferibles de `AGENTS.md` y del patrón de scripts ya existente, o están explícitamente delegados por el pedido humano original según el contexto de esta auditoría. Ninguno es una decisión de negocio/UX/seguridad/privacidad disfrazada de supuesto técnico.

### Exigencias no negociables del circuito
- `docs/tecnica/adopcion-proyecto-existente.md` (AC-1) y `docs/usuario/adopcion-proyecto-existente.md` (AC-2): exigidos explícitamente.
- `runs/v1.1.0/03-adopcion-proyecto-existente/decision.md` (AC-10) y enlaces exactos en `docs/tecnica/index.md`/`docs/usuario/index.md` vía `scripts/update-doc-indexes.ps1` (AC-9): exigidos explícitamente.
- No se asume stack, backend, base de datos ni dependencia de build no documentada: el único artefacto nuevo (`scripts/check-adoption-conflicts.ps1`) usa PowerShell, ya establecido como herramienta requerida en `AGENTS.md`; no se agrega entrada nueva a `docs/tecnica/arquitectura.md` porque no corresponde (correcto, según plan.md sección 4).
- No inventa contenido de negocio: los "ejemplos con nombres reales" citados (`ready-for-pr.ps1`, `workunit-lib.ps1`, los 11 scripts, `tests/test_agentic_sync_scripts.py`, `docs/tecnica/circuito-agentico.md`, marcadores `FEATURE_LINKS_START/END`) fueron verificados contra el repo real y existen tal como se describen.

### Contexto y fuentes / contexto de producto
- La sección "Contexto y fuentes" enumera 7 fuentes consultadas en el orden de precedencia de `AGENTS.md` y qué aportó cada una, de forma trazable. Verifiqué `docs/producto/contexto-producto.md`: todas sus secciones están efectivamente "Por definir", por lo que el spec no lo contradice ni necesita declarar un cambio de decisión de producto.
- No hay contradicción arbitraria entre fuentes: la única decisión con más de una respuesta razonable (incluir o no el script) fue delegada explícitamente por el pedido humano, no resuelta arbitrariamente por el analyst entre fuentes en conflicto.

### Decisiones pendientes bloqueantes
- Sección vacía ("Ninguna"). No hay motivo de rechazo automático por este punto.

### Coherencia spec↔plan y trazabilidad AC→plan→tasks
- `plan.md` no amplía el alcance de `spec.md`: sección 1 replica exactamente los archivos tocados/no tocados declarados en "Alcance", y sección 3 reafirma el límite de AC-8 (`check-adoption-conflicts.ps1` no participa del contrato del circuito).
- Trazabilidad verificada en ambas direcciones:
  - AC-1 → plan (sección `docs/tecnica/...`) → T-01
  - AC-2 → plan (sección `docs/usuario/...`) → T-02
  - AC-3, AC-4, AC-5 → plan (contrato del script) → T-03
  - AC-6 → plan (tabla de colisión/estrategia + límites) → T-01
  - AC-7 → plan (contrato de tests) → T-04, T-08
  - AC-8 → plan (secciones 3 y 6) → T-07, T-08
  - AC-9 → plan (sección "Índices de documentación") → T-05
  - AC-10 → plan (sección `decision.md`) → T-06
  - No hay tareas en `tasks.md` que invoquen un `AC-N` inexistente ni que introduzcan alcance no respaldado por `spec.md`.

### Conclusión
El paquete spec+plan+tasks es internamente consistente, verificable, respeta los límites de alcance declarados, no inventa stack ni contenido de negocio, no deja decisiones pendientes bloqueantes, y tiene trazabilidad completa AC↔plan↔tasks en ambas direcciones. Apruebo con dos observaciones no bloqueantes para que `builder-agent` las tenga en cuenta al implementar.
