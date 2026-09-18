# Decisión F08

Se mantiene `resolve-agentic-model.ps1` como punto único de resolución y se
agrega un catálogo declarativo pequeño dentro de `.agentic/models.json`.
La selección puntúa calidad, costo y latencia según LIGHT/STANDARD/FULL,
después de exigir capacidades, contexto, disponibilidad y security profile.
El empate se resuelve por alias ordenado, por lo que la decisión es
determinística. F07 sólo aporta su `passRate` como evidencia relativa
trazable; no se convierte en benchmark absoluto ni se inventan métricas.
Los aliases históricos siguen siendo de migración y Builder/Reviewer siguen
siendo roles lógicos independientes.
