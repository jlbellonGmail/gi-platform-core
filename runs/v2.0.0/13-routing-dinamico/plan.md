# Plan F08

Extender el router existente, sin crear un segundo sistema: catálogo de
implementaciones en `.agentic/models.json`, pesos por profundidad y filtros
de capacidad/contexto/seguridad/disponibilidad en
`scripts/resolve-agentic-model.ps1`. Mantener la interfaz legacy cuando no
se envían señales dinámicas. Leer el resumen JSONL de F07 de forma offline y
registrar la fuente en la decisión de routing. Probar con fixtures y
`-AllowMissingCredentials`, sin red ni catálogo remoto.
