# Dispatch manual de cierre post-merge

El workflow `post-merge-close-feature.yml` conserva el evento automático y
ofrece `workflow_dispatch` para el caso en que un merge realizado con
`GITHUB_TOKEN` no genere un nuevo evento de workflow. El dispatch exige
`pr_number`, `branch`, `version` y `slug`, y valida que la rama sea exactamente
`feature/<version>-<slug>`.

Después de esa validación, todas las comprobaciones y la escritura de
`ROADMAP.md` siguen en `scripts/close-feature.ps1`. Por tanto, un dispatch no
puede cerrar una PR no mergeada ni publicar un estado arbitrario.

