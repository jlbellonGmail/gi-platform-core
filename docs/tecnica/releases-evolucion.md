# Releases y evolución determinísticos

`scripts/release-readiness.ps1` es la ruta canónica y read-only para evaluar un
candidato SemVer. El alcance de cada release se declara en
`runs/<version>/release-readiness/manifest.json`; así el gate valida los items
reales del ROADMAP de este repositorio y no fases históricas de la Template.
El gate exige ejecutarse sobre `develop` limpio, comprueba que el commit
local/remoto coincide, que los items declarados están cerrados, que CI está
verde sobre ese SHA, que la integridad pasa, que `main` es ancestro (si existe),
que el tag candidato no existe y que `v1.1.0` conserva su objeto y commit
histórico. `-DryRun` hace explícito que no se crean PR, tag, release ni cambios
remotos.

El flujo posterior es `develop` validado → PR contra `main` → gates → merge
humano → comprobación del commit final → tag anotado `vX.Y.Z` → release breve.
La primera release puede crear `main`; las siguientes sólo llegan por PR. Un
hotfix usa una rama desde el tag estable, pasa el mismo gate y se reincorpora
a `develop`; no se introduce GitFlow adicional. El run se ubica bajo
`runs/<version>/`, por lo que el mecanismo es reutilizable para `v2.1.0` y
`v3.0.0`.
