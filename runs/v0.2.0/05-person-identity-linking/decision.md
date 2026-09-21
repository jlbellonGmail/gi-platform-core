# Decision: 05-person-identity-linking - Person Identity Linking

## Estado

Estado tecnico: ready_for_pr.

La aprobacion de merge es exclusivamente del HITL en GitHub sobre la PR.
Este documento no otorga ni implica esa aprobacion.

## Evidencias revisadas

- `runs/v0.2.0/05-person-identity-linking/spec.md`
- `runs/v0.2.0/05-person-identity-linking/plan.md`
- `runs/v0.2.0/05-person-identity-linking/tasks.md`
- `runs/v0.2.0/05-person-identity-linking/audit-1.md`
- `runs/v0.2.0/05-person-identity-linking/test-report-1.md`
- `runs/v0.2.0/05-person-identity-linking/code-review-1.md`

## Decisiones demostrables

- CoreApi v0.1.0 permanece compatible y las operaciones nuevas se versionan como v0.2.0.
- La autenticación HTTP se delega al host mediante callable inyectado; Core no inventa credenciales ni parsea JWT.
- La atomicidad se garantiza por puerto: RLock en memoria y RPC con advisory lock en Supabase; no se promete transacción distribuida de auditoría.

## Resultado

La feature queda apta para integrarse/cerrarse cuando GitHub confirme merge contra `develop` y el cierre automatico marque `ROADMAP.md`.
