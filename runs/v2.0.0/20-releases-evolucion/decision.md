# Decisión F15

Se adopta `release-readiness.ps1` como única ruta de preparación y dry-run.
Es read-only para impedir que F15 publique o cree tags; la publicación estable
queda deliberadamente en el flujo PR develop→main y en F17. Se parametriza la
versión y se generaliza sólo el hardcode real de `check-integrity.ps1`.

Estado: implementado; v2.0.0 no publicada.
