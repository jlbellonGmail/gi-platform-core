# Manual operativo de GI-PLATFORM-CORE

Este archivo define cómo trabajar en este repositorio. Es un contrato de
operación, no el backlog, una spec ni una fotografía del estado de Git.
Para principios normativos consultar [CONSTITUTION.md](CONSTITUTION.md); para
trabajo planificado [ROADMAP.md](ROADMAP.md); para reentrada
[STATUS.md](STATUS.md); para decisiones técnicas `docs/tecnica/` y para el
contrato ejecutable `scripts/`.

GI-PLATFORM-CORE es un proyecto independiente inicializado desde Template
v2.0.0 (`f5d4b6cc029c34c0d0c05831bfd28134276fa167`). La procedencia no
implica sincronización posterior con el template ni importa su backlog,
roadmap o evidencias históricas.

## Reentrada operativa

Al comenzar una sesión leer `AGENTS.md`, `CONSTITUTION.md`, `ROADMAP.md`,
`STATUS.md` y el estado real de Git:

```powershell
git status --short --branch
git log -1 --oneline --decorate
git branch -vv
git worktree list
```

Si la tarea depende de GitHub, comprobar también el estado real de PR y CI:

```powershell
gh pr list --state all --limit 20
gh run list --limit 20
```

La evidencia de Git, GitHub, `runs/` y los scripts prevalece sobre un resumen
desactualizado en `STATUS.md`. Antes de devolver control, bloquearse o pedir
una decisión, actualizar el estado y ejecutar:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\update-status.ps1
pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\check-status.ps1
```

`update-status.ps1` sólo administra el bloque automático de `STATUS.md`.
El texto manual sigue siendo responsabilidad del agente. `STATUS.md` no
reemplaza artefactos, tests, PR, CI ni evidencia primaria.

## Autoridad y seguridad

La precedencia es: instrucción humana vigente; este contrato y las reglas
globales; ítems y referencias de `ROADMAP.md`; contexto de producto; decisiones
de arquitectura y ADR; código y tests; supuestos explícitos.

No inventar reglas de negocio, permisos, datos, seguridad, privacidad,
cumplimiento, resultados funcionales ni contenido legal. Una contradicción
material se registra y se escala antes de cerrar la intención.

Aplicar los principios de `CONSTITUTION.md`: SDD, determinismo, roles por
capacidad, complejidad proporcional, evidencia trazable, fail-safe,
reversibilidad, mínimo privilegio, portabilidad, evaluabilidad y observabilidad.
No habilitar fases o capacidades sólo porque estén descritas en documentación.

No modificar adaptadores generados manualmente. No hacer force-push, no
destruir trabajo ajeno y no marcar una unidad como completada sin la transición
real correspondiente.

## Roles

Los roles conceptuales son tres:

- **Planner** interpreta la intención, consume ASSESS y produce intención y plan.
- **Builder** modifica el worktree, implementa y genera evidencia; no se aprueba.
- **Reviewer** valida independientemente el estado vigente y el diff evaluado.

`analyst-agent`, `qa-agent` y `code-reviewer-agent` son aliases históricos de
migración, no roles arquitectónicos. Modelos, proveedores y herramientas son
adaptadores reemplazables. La fuente canónica está en `.agentic/` y sus
adaptadores se regeneran con `scripts/sync-agentic-adapters.ps1`.

La coordinación normal es Builder → validación determinística → Reviewer →
feedback estructurado → Builder. El Reviewer siempre valida el estado vigente.
Planner sólo reingresa por decisión material, ambigüedad, contradicción o
cambio de alcance. Un bloqueo externo o fallo técnico se conserva con evidencia
y termina de forma segura.

## Work units

Una Feature es un ítem de `ROADMAP.md`, una rama y un run. Se inicia desde el
checkout principal de `develop`:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-work-unit.ps1 `
  -Version v0.1.0 -Mode Feature -Slug 01-ejemplo
```

El script valida el estado, crea la rama `feature/v0.1.0-01-ejemplo`, el
worktree bajo `../worktrees/` y el run correspondiente. Omitir `-Version`
conserva la interfaz legacy. No iniciar una unidad desde otro worktree ni con
un checkout sucio.

Un Milestone sólo agrupa ítems realmente interdependientes:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-work-unit.ps1 `
  -Version v0.1.0 -Mode Milestone -Slug nombre -Items 01-uno,02-dos
```

Su manifest `work-unit.json` es la identidad y todos sus ítems se transicionan
de forma atómica. Si pueden publicarse como Features independientes, dividirlos.
Usar `scripts/workunit-lib.ps1` y `scripts/feature-contract.ps1`; no duplicar
parsers ni contratos en prompts.

## Circuito de trabajo

No existen checkpoints humanos intermedios. Cada etapa deja evidencia en
`runs/` y los retornos permitidos son Reviewer → Planner, QA → Builder,
code review → Builder y HITL NO MERGE → Builder.

1. **Planner/analyst** lee el ítem, referencias, contexto de producto si existe,
   reglas, arquitectura, código y tests. Produce la intención proporcional,
   plan y tareas trazables; aplica CLARIFY y no inventa decisiones materiales.
2. **Reviewer/reviewer-agent** valida coherencia, trazabilidad y profundidad.
   Un rechazo vuelve al Planner.
3. **Builder/builder-agent** implementa en su worktree, actualiza documentación
   e índices cuando corresponda y registra decisiones demostrables.
4. **QA/qa-agent** ejecuta tests del producto y del circuito, y valida
   `Assert-FeatureContract` o `Assert-WorkUnitContract`. Un fallo vuelve al Builder.
5. **Reviewer/code-reviewer-agent** revisa el diff final después de QA. Si
   rechaza, vuelve al Builder; todo cambio relevante repite QA.
6. Con review aprobada, ejecutar `ready-for-pr.ps1`. La unidad queda `[-]`
   `READY_FOR_PR`, nunca `[x]`.
7. Publicar la rama, crear PR contra `develop` y esperar CI con
   `wait-pr-ci.ps1`. La PR debe enlazar spec, plan, tareas, tests, riesgos y
   evidencia de revisión.
8. El único HITL es la decisión humana `MERGE` o `NO MERGE` sobre la PR real
   con CI verde. El agente nunca infiere esa decisión.
9. Con `MERGE`, `complete-approved-pr.ps1` puede esperar checks nuevamente y
   mergear. También es válido el merge directo humano desde GitHub tras revisar
   CI y evidencia.
10. Después del merge, `close-feature.ps1` confirma la PR hacia `develop`,
    cambia `[-]` a `[x]` y sincroniza el remoto. La limpieza local es posterior
    y separada, mediante `local-feature-reconcile.ps1`.

## ASSESS, SDD y evidencia

Para unidades v2, ejecutar ASSESS sobre las rutas evaluadas y conservar su
salida; luego materializar el SDD con `scripts/materialize-sdd.ps1`. ASSESS
clasifica `LIGHT`, `STANDARD` o `FULL`; ningún rol vuelve a clasificar a mano.

La fuente única del contrato es `scripts/feature-contract.ps1`. `SUMMARY.md`
es siempre la entrada humana. En v2, `sdd.json` determina qué evidencia se
exige; no crear placeholders para artefactos opcionales. En legacy, se conserva
el contrato histórico vigente.

Los veredictos de auditoría, QA y code review deben indicar `approved` o
`rejected`, el número de intento y feedback concreto. El intento numéricamente
mayor es el vigente; un aprobado viejo no cubre un rechazo nuevo.

La documentación técnica vive en `docs/tecnica/<slug>.md`, la de uso en
`docs/usuario/<slug>.md`, y los índices se actualizan con el script común cuando
el contrato de la unidad lo exige. `docs/producto/contexto-producto.md`, si
existe, es conocimiento transversal confirmado; su ausencia no bloquea.

CLARIFY sólo pregunta por decisiones materiales no deducibles de fuentes
autoritativas. Las respuestas se incorporan a la intención; decisiones
bloqueantes pendientes impiden aprobarla.

## ROADMAP y Git

Los estados son `[ ]` pendiente, `[-]` listo para PR y `[x]` sólo después del
merge confirmado a `develop`. Un milestone cambia todos sus ítems de forma
atómica. El cierre remoto no puede ejecutarse sobre una PR no mergeada.

`develop` es la integración diaria. Cada Feature/Milestone usa rama y worktree
propios; un agente no commitea directamente sobre `develop` ni `main`. Los
cierres automáticos y las transiciones explícitamente implementadas por los
scripts son las únicas excepciones documentadas.

`main` es estable y puede no existir todavía. Se crea sólo por decisión humana
al aprobar la primera release. Las releases usan tags SemVer anotados; los
agentes no crean, mueven, borran ni publican tags o releases.

## Stack y dependencias

El Core actual está implementado en Python y sus decisiones de arquitectura
están en `docs/tecnica/arquitectura.md`. Las migraciones y adaptadores de
persistencia sólo se consideran parte del producto cuando esa documentación y
la evidencia de la work unit los respaldan. No agregar frameworks, servicios,
integraciones, dependencias de build o endpoints reales sin decisión explícita,
alcance, datos y estrategia de pruebas documentados.

## CI y herramientas

Los workflows y scripts son la fuente ejecutable: no duplicar su lógica en
prompts. No usar `continue-on-error` para ocultar fallos. Antes de cerrar una
unidad comprobar tests del circuito y del producto si existen, contrato,
documentación, índices, Git y CI aplicable.

PowerShell 7, Git, `gh` autenticado, Python 3.12+ y `pytest` son las
herramientas locales esperadas. Las limitaciones reales de plataforma deben
quedar documentadas, no asumidas.

Después de modificar `.agentic/`, regenerar y comprobar adaptadores:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\sync-agentic-adapters.ps1
pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\sync-agentic-adapters.ps1 -Check
```

Este manual no sustituye `CONSTITUTION.md`, `ROADMAP.md`, `STATUS.md`, los
scripts, los contratos, la CI, la PR ni la decisión humana final. Si este texto
diverge de un contrato ejecutable, detenerse, registrar la contradicción y
corregir la fuente apropiada mediante una unidad trazable.
