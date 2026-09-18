# Plan F16

1. Inspeccionar fuentes canonicas, roadmap, runs, adaptadores, CI y tag v1.1.0.
2. Ejecutar pytest, reconciliador Windows, integrity, status, evals y gates especializados.
3. Reproducir la incidencia local F14 con timeout, identificar causa y corregir solo bugs acotados.
4. Registrar matriz integral con PASS/PARTIAL/NOT_APPLICABLE y riesgos residuales.
5. Revisar independientemente el diff final, preparar PR hacia develop y cerrar solo tras merge real.

La evidencia remota de CI es complementaria y no sustituye fallos o warnings
locales. No se ejecuta release ni se crea tag.
