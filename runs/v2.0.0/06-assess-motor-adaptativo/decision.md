# Decisión de implementación

Se adopta una primera implementación determinista basada en rutas cambiadas.
La política es deliberadamente conservadora: seguridad/datos y automatización
suben a `HIGH/FULL`; los demás cambios reciben señales proporcionales. La
salida es evidencia y recomendación, no activación de pipeline.

Se mantiene el contrato v1 completo y no se agregan modelos, dependencias,
MCP, adaptadores ni estados nuevos. La evolución semántica, fixtures y gates
proporcionales quedan fuera de esta fase y no se anticipan.
