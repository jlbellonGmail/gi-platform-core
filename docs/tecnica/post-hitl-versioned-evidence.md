# Evidencia Post-HITL versionada

El workflow deriva `version` y `slug` desde la rama `feature/vX.Y.Z-NN-slug`.
Las tres rutas consumidas por `complete-approved-pr.ps1` se construyen como
`runs/<version>/<slug>/<evidencia>.md`. Esto mantiene alineada la evidencia
con la identidad de la work unit y evita depender de la versión del Template.

El cambio es de gobernanza: no modifica la lógica del Core ni datos externos.

