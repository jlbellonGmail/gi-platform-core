# Plan — ASSESS / motor adaptativo

1. Añadir un script aislado con entradas explícitas, señales deterministas,
   clasificación conservadora y salida JSON/JSONL.
2. Añadir tests pytest que ejecuten PowerShell y cubran HIGH/FULL,
   MEDIUM/STANDARD, LOW/LIGHT, evidencia y ausencia de entrada.
3. Documentar contrato, límites, compatibilidad y uso; actualizar índices
   mediante el script común.
4. Verificar suite completa, contrato Feature, adaptadores, diff y CI.

No se modifican scripts maduros, roles, router, workflows ni adaptadores.
