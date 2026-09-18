```yaml
status: rejected
attempt: 1
feedback:
  - "Supuesto principal indebido (bloqueante): la sección 'Supuestos' de spec.md resuelve como 'decisión operativa/técnica' que product-tests debe documentarse como igualmente obligatorio/bloqueante que circuit-tests en branch protection, pese a estar vacío. Esto NO es una decisión inferible de evidencia técnica existente (código, arquitectura, ADR, reglas globales, patrones): es una decisión de política/gobernanza sobre qué bloquea el merge (categoría 'permisos' explícita en la Política de fuentes de AGENTS.md como territorio que no se puede inventar). Hay al menos dos respuestas igualmente válidas con tradeoffs reales — (a) requerirlo ya para no tener que acordarse de cambiarlo después, vs (b) no requerirlo mientras esté vacío para evitar que un placeholder sin contenido real bloquee merges por una razón de infraestructura ajena al circuito — y la spec elige una unilateralmente. La propia sección 'Contexto y fuentes' confirma que el pedido humano NO zanjó esto: dice literalmente que el humano 'pide decidir explícitamente si debe ser requerido/bloqueante', es decir, delegó la pregunta sin responderla. Eso es exactamente la señal de una ambigüedad material que debía tratarse como Fase CLARIFY (con una pregunta puntual al humano, p.ej. '¿product-tests debe listarse como status check requerido en branch protection desde que es un placeholder vacío, o solo cuando tenga contenido real de stack?'), no resolverse como supuesto técnico. Agrava el problema que esta decisión sienta precedente para el checklist de branch protection de una feature separada (05-operational-readiness-docs) sin confirmación humana explícita — builder-agent estaría implementando de facto una política de gobernanza del repo basada en el razonamiento del propio analyst-agent, no en una decisión humana."
  - "Como consecuencia directa de lo anterior, AC-5 de spec.md ('Queda documentado explícitamente... que circuit-tests y product-tests deben tratarse como igualmente obligatorios/bloqueantes...') está construido sobre el mismo supuesto indebido: es un criterio de aceptación que fija una política de branch protection no confirmada por el humano. AC-5 debe reformularse (o eliminarse/posponerse) una vez resuelta la Fase CLARIFY, en vez de exigir que se documente como si fuera un hecho ya decidido."
  - "Gap de trazabilidad menor en tasks.md: T-06 (escribir docs/tecnica/ci-wiring-product-tests.md) incluye explícitamente en su descripción 'por qué product-tests queda documentado como requerido/bloqueante desde ya' — que es precisamente lo que exige AC-5 del lado de docs/tecnica — pero su campo 'Traza' solo lista AC-8, no AC-5. Si AC-5 se mantiene tras resolver el punto anterior, T-06 debe declarar también AC-5 en su traza para que la cobertura AC↔tasks quede completa en ambas direcciones (AC-5 hoy solo queda trazado a T-04, que cubre el lado de AGENTS.md pero no el de docs/tecnica)."
notes: |
  El resto de la spec/plan/tasks está bien construido y no presenta otros
  motivos de rechazo:
  - Identificación declara correctamente Modo: FEATURE, consistente con
    la ausencia de runs/milestone-*/work-unit.json en el worktree.
  - AC-1 a AC-4, AC-6 a AC-11 son verificables de forma objetiva (diff de
    YAML, presencia de jobs/steps, existencia y contenido de archivos,
    enlaces exactos en índices).
  - AC-8, AC-9, AC-11 exigen explícitamente docs/tecnica/<slug>.md,
    docs/usuario/<slug>.md y decision.md; AC-10 exige enlaces exactos en
    ambos índices. No falta ninguno de los artefactos obligatorios.
  - "Decisiones pendientes bloqueantes" está vacía, pero justamente por
    eso se rechaza: la ambigüedad material (branch protection de
    product-tests) existe y no debería haberse resuelto en silencio como
    supuesto — debería haber quedado ahí, o mejor, resuelta vía CLARIFY
    antes de cerrar la spec.
  - No se inventa stack, backend, dependencia de build ni contenido de
    negocio. El placeholder de product-tests se mantiene deliberadamente
    vacío y las fuentes consultadas están bien trazadas y con precedencia
    razonable.
  - Coherencia spec↔plan: plan.md no amplía el alcance declarado en
    spec.md; las exclusiones explícitas ('NO toca scripts/*.ps1,
    .agentic/, otros workflows, requirements-dev.txt,
    docs/tecnica/arquitectura.md') son idénticas en ambos documentos.
  - Trazabilidad AC→plan→tasks es completa y bidireccional salvo el gap
    puntual de T-06/AC-5 señalado arriba: cada AC-1..AC-11 aparece en al
    menos una sección de plan.md y al menos una tarea de tasks.md, y
    ninguna tarea inventa alcance sin AC-N real de respaldo.
  - No aplica Modo MILESTONE (no hay manifest), por lo que no corresponde
    el gate de tamaño/descomposición de grupos de items.

  Este rechazo es puntual y accionable: no requiere replantear la
  arquitectura del cambio (separar circuit-tests/product-tests en dos
  jobs top-level, con el placeholder vacío referenciando
  docs/tecnica/arquitectura.md, sigue siendo sólido), solo requiere que
  analyst-agent trate la pregunta de obligatoriedad en branch protection
  como una pregunta CLARIFY real hacia el humano antes de volver a cerrar
  spec.md, y ajuste AC-5 (y la traza de T-06) en consecuencia según la
  respuesta.
```
