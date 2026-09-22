# ROADMAP

## Estado inicial

GI-PLATFORM-CORE fue inicializado desde Template v2.0.0. Este archivo no
contiene funcionalidades inventadas ni conserva las fases de construcción
del Template.

- [x] 01-core-platform-v010 — Core neutral de tenancy, identidad,
  autorización contextual, aislamiento, auditoría y contratos públicos v0.1.0.
- [x] 05-person-identity-linking — Vinculación tenant-aware de Person con una
  identidad de acceso Core, CoreApi v0.2.0 y servicio HTTP.
- [x] 02-supabase-gi-dev-validation — Integración, bootstrap sintético y
  validación autenticada de RLS del Core contra Supabase gi-dev.
- [x] 03-post-hitl-versioned-evidence — Corrección del gate Post-HITL para
  resolver evidencias por versión y slug de work unit.
- [x] 04-post-merge-close-dispatch — Habilitar el cierre post-merge manual
  seguro cuando el evento automático queda suprimido por GITHUB_TOKEN.
- [x] 06-release-readiness-current-roadmap — Alinear el gate de readiness de
  releases con el ROADMAP vigente del repositorio y eliminar referencias
  históricas incompatibles.
- [x] 07-release-evidence — Materializar la evidencia versionada de la release
  para el gate de readiness posterior al merge.
- [x] 09-release-history-manifest — Eliminar la referencia rígida a un tag
  histórico inexistente y validar tags reales desde el manifiesto.

- [x] 10-package-version-consistency — Alinear la versión exportada por el paquete con la versión distribuida del wheel v0.2.1.

- [x] T01-release-governance-reconciliation — Reconciliar evidencia histórica,
  controles de release y estado operativo tras la auditoría v0.2.1.
- [x] 11-core03-tenant-readiness — Consolidar Tenant, contratos públicos,
  seguridad, documentación y readiness para módulos consumidores.

## Procedencia de la baseline

- Template: v2.0.0
- SHA: `f5d4b6cc029c34c0d0c05831bfd28134276fa167`

## Convenciones

- `[ ]`: pendiente.
- `[-]`: READY_FOR_PR.
- `[x]`: completado después del merge.

Las entradas funcionales deben ser líneas `NN-slug — descripción`. Los items
TNN documentan mantenimiento de gobernanza y siguen el mismo lifecycle.















