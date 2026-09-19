# Uso del gate Post-HITL

Al crear una Feature versionada, sus evidencias de autorización, revisión e
integridad deben estar bajo `runs/<versión>/<slug>/`. El gate obtiene ambos
componentes de la rama de la PR y no requiere editar el workflow por versión.

La decisión humana MERGE sigue siendo independiente y no es generada por el
workflow ni por el agente.

