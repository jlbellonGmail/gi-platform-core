# Decision — F17

Estado: BLOCKED

Se adopta una auditoría FULL por riesgo de release. Se corrige el wait
indefinido de CI con timeout controlado. Los riesgos residuales ambientales
(Python PATH sin pytest y locking temporal de Windows) se documentan y se
compensan con Python canónico, repro aislado y CI remoto. No se publica hasta
que audit, QA, code review, CI e integrity estén aprobados. Audit, QA, code review, integrity y CI técnico están aprobados; falta una aprobación GitHub humana independiente. No se fabrica self-review ni se fuerza el merge.
