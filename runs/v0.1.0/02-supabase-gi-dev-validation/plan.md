# Plan — Supabase gi-dev validation

1. Preservar el desarrollo previo y crear esta Feature desde un checkout
   limpio según el contrato de work units.
2. Implementar el comando interactivo con preflight, autenticación, bootstrap
   idempotente y comprobaciones RLS.
3. Documentar el origen permitido de la clave server-side y el único comando.
4. Ejecutar tests unitarios, suite completa, validadores de migración y gates.
5. Ejecutar la validación externa sólo con credenciales introducidas en la
   terminal local y registrar evidencia sin secretos.
6. Generar revisión independiente, convergencia y dejar la rama lista para PR.
