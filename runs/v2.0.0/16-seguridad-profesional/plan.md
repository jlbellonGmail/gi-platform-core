# Plan — F11 Seguridad profesional

1. Mantener la política declarativa en `.agentic/` y agregar schema mínimo.
2. Exponer lectura de perfiles y validación de autorización scoped en un script
   común, sin credenciales ni lógica por proveedor.
3. Reducir permisos explícitos de CI y desactivar persistencia de credenciales
   en jobs de sólo lectura.
4. Añadir documentación técnica/usuario, índices y tests negativos.
5. Validar adaptadores, contrato, pytest, diff y CI antes de PR/merge.

Los gates existentes para aprobación stale, PR contra develop, guard-develop,
close-feature y reconciliador permanecen la fuente de verdad; F11 no los
duplica ni los relaja.
