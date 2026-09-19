# Estado operativo

Proyecto nuevo: GI-PLATFORM-CORE.

## Procedencia

- Template base: v2.0.0
- Template SHA: `f5d4b6cc029c34c0d0c05831bfd28134276fa167`

## Estado

- `AGENTS.md` corregido y reducido a contrato operativo; referencia verificada
  contra `D:\proyectos\template\AGENTS.md` de Template v2.0.1.
- En progreso: empaquetado instalable, contrato de consumo, CI real del Core y
  ejemplo reproducible para hosts externos.
- Contrato público v0.1.0 formalizado en `contracts/`, exportado por el paquete
  y validado como JSON; ejemplo de consumo ejecutado correctamente.
- Rama estable/local: `develop`.
- Trabajo activo: persistencia Supabase del Core e integración de contratos;
  corregido el almacenamiento normalizado de `location_access`.
- Validación local: pytest completo `280 passed` tras corregir el launcher de
  PowerShell 7 usado por los tests en Windows.
- Validación posterior: PostgreSQL efímero con roles Supabase simulados pasó
  DDL, 9 tablas, 9 policies, RLS en 9 tablas y aislamiento efectivo.
- Validación externa read-only: endpoint Supabase configurado respondió HTTP 200
  y no expuso filas anónimas; falta validar JWT/autorización real.
- Validador reproducible agregado en `scripts/validate_supabase_core.py`; su
  prueba local y la comprobación pública actual pasan.
- La migración Core tiene cobertura estática de sus 9 tablas, RLS, grants y
  clave compuesta de `location_access` (`3 passed` en las pruebas nuevas).
- La lectura pública `list_organizations` quedó scoped por usuario y membership
  activa para evitar enumeración cross-tenant; contrato y tests actualizados.
- Consumo externo verificado en un entorno virtual limpio: el wheel
  `gi_platform_core-0.1.0` se instaló sin el checkout y `CoreApi` respondió con
  contrato/version `0.1.0`.
- Mecanismo de publicación agregado en
  `.github/workflows/publish-core-package.yml`: un tag SemVer humano publica el
  wheel como artefacto de la release.
- Documentación histórica del template sobre `product-tests` marcada como tal;
  la CI vigente del Core quedó referenciada como fuente ejecutable.
- ROADMAP funcional: `01-core-platform-v010` en READY_FOR_PR.
- Work units activas: ninguna.
- Runs de producto: ninguno.
- Skills: cero, estado válido hasta demostrar una necesidad especializada.
- MCP reales: cero; catálogo declarativo vacío.
- Modelos/proveedores: cero configurados; routing declarativo preparado.

## Próximo paso exacto

La construcción local de `gi-platform-core==0.1.0` ya fue verificada. El paso
siguiente es validar JWT/RLS contra el proyecto Supabase real y aplicar las
migraciones sólo con credenciales server-side autorizadas. Después ejecutar la
validación completa y crear la PR. No se hizo push ni se crearon tags; no hay
remoto configurado.

## Bloqueo externo actual

El checkout no tiene `origin` y no se encontró un repositorio GitHub inequívoco
para este proyecto bajo la cuenta autenticada. `.env` tampoco contiene
`SUPABASE_ACCESS_TOKEN` ni una credencial server-side. Para reanudar el cierre
se necesita configurar el remoto correcto y proporcionar, de forma segura, un
JWT de usuario de prueba; no se requieren cambios adicionales de código para
esas dos validaciones.

<!-- STATUS:AUTO:BEGIN -->

## Estado verificado automáticamente

- Actualizado: 2026-09-19T17:23:43Z
- Versión: v0.1.0
- Rama: feature/v0.1.0-02-supabase-gi-dev-validation
- HEAD: 5a2658734b39e4652fadbe530e6d61a4b7a554ab
- Remoto: https://github.com/jlbellonGmail/gi-platform-core.git
- Working tree: dirty
- Worktrees: 2
- Worktrees Git: 2
- Unidades activas: = [feature/v0.1.0-02-supabase-gi-dev-validation]
- PR activa: UNKNOWN / sin PR abierta
- CI: UNKNOWN / sin CI verificable
- CI vigente: UNKNOWN / sin CI verificable
- Última release: UNKNOWN / no disponible

<!-- STATUS:AUTO:END -->
