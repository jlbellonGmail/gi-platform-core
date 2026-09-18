# Plan — F17

1. Actualizar STATUS automáticamente y capturar estado Git/GitHub.
2. Ejecutar pytest con Python canónico, reconciliador aislado, evals y todos
   los gates oficiales.
3. Auditar .audit con TEMPLATE, revisar incidencias, portabilidad, seguridad,
   supply-chain, lifecycle, mantenimiento y release readiness.
4. Corregir únicamente el wait infinito de CI con timeout explícito.
5. Generar docs, decisión, reporte de auditoría, QA y code review.
6. Validar contrato, marcar READY_FOR_PR, crear PR, esperar CI y mergear F17.
7. Verificar cierre en develop y ejecutar dry-run/publicación F15, tag y release.

Compatibilidad: no se cambian roles, proveedores, formatos históricos ni
dependencias. El cambio de wait sólo limita una espera externa y conserva el
veredicto de gh pr checks.
