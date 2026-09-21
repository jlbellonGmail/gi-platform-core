# Releases y evolución determinísticos

`scripts/release-readiness.ps1` es la ruta canónica y read-only para evaluar
un candidato SemVer. Cada release declara en
`runs/<version>/release-readiness/manifest.json` los items reales del ROADMAP
y los tags históricos anotados que deben preservarse.

El gate comprueba árbol limpio, coincidencia local/remota del SHA, items
cerrados, CI verde, integridad, ancestro de `main` si existe, ausencia del tag
candidato y validez de los tags históricos declarados. `-DryRun` no crea PR,
tag, release ni cambios remotos.
