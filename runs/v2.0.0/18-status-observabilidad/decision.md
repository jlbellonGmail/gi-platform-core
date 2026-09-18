# Decision

Se elige snapshot derivado en memoria y JSON opt-in. Persistir un archivo automático por cada consulta haría dirty el checkout y crearía otra fuente de verdad. `STATUS.md` sólo se actualiza cuando se solicita explícitamente; el bloque AUTO es regenerable.
