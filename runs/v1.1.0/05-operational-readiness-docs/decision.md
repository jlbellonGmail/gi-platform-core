# Decision: 05-operational-readiness-docs - Operational Readiness Docs

## Estado

Estado tecnico: ready_for_pr (implementacion completa, pendiente de QA y
del circuito posterior).

La aprobacion de merge es exclusivamente del HITL en GitHub sobre la PR.
Este documento no otorga ni implica esa aprobacion.

## Evidencias revisadas

Estos son los artefactos esperados del circuito para esta feature; no
implica que todos ya existieran ni hubieran sido leidos en el momento
exacto en que se escribio esta lista (p. ej. `test-report-1.md` y
`code-review-1.md` se producen en pasos posteriores del circuito):

- `runs/v1.1.0/05-operational-readiness-docs/spec.md` (version 2, aprobada en
  `audit-2.md`)
- `runs/v1.1.0/05-operational-readiness-docs/plan.md`
- `runs/v1.1.0/05-operational-readiness-docs/tasks.md`
- `runs/v1.1.0/05-operational-readiness-docs/audit-1.md` (rejected)
- `runs/v1.1.0/05-operational-readiness-docs/audit-2.md` (approved)

## Fase CLARIFY resuelta: `enforce_admins`

El intento 1 de `spec.md` dejaba `enforce_admins: false` como "supuesto
conservador" en la seccion "Supuestos". `audit-1.md` lo rechazo: es una
decision de seguridad/permisos que admite dos respuestas validas
distintas, no un detalle tecnico inferible de evidencia existente, y
estaba en tension directa con la regla dura ya documentada en
`AGENTS.md` seccion "Git" ("Nunca commitear directo a `develop`... ni
nunca directo a `main`") — con `false`, un admin si podria pushear
directo a `develop` saltandose PR/aprobacion/CI.

- **Pregunta**: ¿`enforce_admins` debe ser `true` o `false` en el payload
  de branch protection documentado, dado que el item de `ROADMAP.md` no
  lo especifica y esto determina si los administradores del repositorio
  pueden bypassear esa misma proteccion?
- **Respuesta del humano**: `true`. Los administradores tambien deben
  quedar sujetos a la proteccion — consistente con la regla dura ya
  existente en `AGENTS.md` ("Nunca commitear directo a `develop`... ni
  nunca directo a `main`"), sin excepcion, aceptando que en un incidente
  operativo excepcional no haya bypass automatico disponible para
  admins.
- **Valor final**: `enforce_admins: true`, propagado de forma consistente
  en `spec.md` (AC-2, AC-6, "Clarificaciones realizadas"), `plan.md`
  (seccion 2.1), `AGENTS.md` (bullet "Branch protection de GitHub") y
  `docs/tecnica/operational-readiness-docs.md`.

`audit-2.md` verifico explicitamente esta resolucion y aprobo la spec sin
feedback pendiente.

## Decisiones demostrables

- Se agrego el bullet "Branch protection de GitHub" en `AGENTS.md`,
  seccion "Setup manual (una sola vez, no automatizable)", con los 4
  requisitos sobre `develop` (PR obligatoria, status check `test` en
  verde, al menos 1 aprobacion, dismiss stale approvals),
  `enforce_admins: true`, el comando `gh api --method PUT` completo con
  el payload JSON exacto de `plan.md`, el paso de validacion local
  `$branchProtection | ConvertFrom-Json | Out-Null`, el comando `GET` de
  verificacion de solo lectura, la advertencia explicita de que el `PUT`
  reemplaza (no fusiona) la configuracion existente, la nota de
  dependencia con la feature `04-ci-wiring-product-tests` sobre el
  nombre del status check, y la alternativa manual de UI (incluyendo
  "Include administrators" como equivalente clasico de
  `enforce_admins: true`, con nota de que en Rulesets modernos la
  etiqueta equivalente es "Do not allow bypassing the above settings" —
  ver nota no bloqueante de `audit-2.md`).
- Se agrego la seccion "Troubleshooting: EDR/antivirus agresivo bloquea
  el reconciliador local (Windows)" al final de
  `docs/tecnica/circuito-agentico.md` (despues de "Gate post-HITL"), con
  sintoma, causa, alcance (exclusivamente local, no afecta git remoto,
  CI ni merge) y la solucion exacta (`git worktree remove --force` +
  `git worktree add`), con advertencia sobre descarte de cambios sin
  commitear y nota de que el lock file del reconciliador vive fuera del
  worktree.
- Se escribio `docs/tecnica/operational-readiness-docs.md` con las
  decisiones de diseno de ambos puntos y los casos borde cubiertos.
- Se escribio `docs/usuario/operational-readiness-docs.md` con el
  proposito de la feature y como usar ambos checklists.
- Se ejecuto
  `scripts/update-doc-indexes.ps1 05-operational-readiness-docs "Operational Readiness Docs"`,
  agregando un enlace nuevo en `docs/tecnica/index.md` y
  `docs/usuario/index.md`.
- No se toco `.github/workflows/ci.yml`, ningun script de `scripts/*.ps1`
  ni ninguna configuracion real de GitHub: el comando `gh api` queda
  documentado, no ejecutado, consistente con el alcance explicito de
  `spec.md` ("Explicitamente NO incluye").
- No se agrego ninguna dependencia de build/backend/base de
  datos/integracion externa.

## Resultado

La feature queda apta para integrarse/cerrarse cuando GitHub confirme
merge contra `develop` y el cierre automatico marque `ROADMAP.md`.
