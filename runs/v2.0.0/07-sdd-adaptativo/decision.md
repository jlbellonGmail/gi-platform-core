# Decisión de implementación

Se adopta `scripts/materialize-sdd.ps1` como capacidad opt-in y determinista.
ASSESS conserva autoridad exclusiva sobre la profundidad; el materializador
solo traduce su salida a pasos, artefactos y gates proporcionales.

La compatibilidad v1 se preserva: no se modifica el contrato Feature/Milestone
ni se eliminan artefactos universales. La autorización previa de esta ejecución
se registra en `human-authorization.md` y tiene un camino explícito en el gate;
la exigencia de aprobación GitHub sigue siendo el comportamiento por defecto.

Estado técnico: ready_for_pr, pendiente de PR, CI y cierre remoto.
