# Plan F06

1. Auditar la suite y conservar pruebas de alto valor por contrato, regresión,
   integración, lifecycle, CI y schemas.
2. Añadir una prueba pequeña de invariantes del framework `.audit` sin
   mezclarla con Reviewer ni ejecutar un auditor durante pytest.
3. Corregir el launcher Windows para pasar argumentos como `-File` y dejar
   diagnóstico claro cuando el host no permite procesos persistentes.
4. Mantener CI con jobs separados y product-tests como wiring desacoplado.
5. Ejecutar pytest, sync de adaptadores, contrato de la work unit y checks de
   status; registrar resultados y code review del diff final.
