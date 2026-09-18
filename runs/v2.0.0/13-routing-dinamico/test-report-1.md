# QA F08

Veredicto: **approved**

- Router legacy y schemas: 24 passed.
- LIGHT con capacidades: `balanced`/eficiente.
- FULL complejo: `quality` por mayor calidad.
- Fallback y ausencia de candidatos: comportamiento trazable y fail-safe.
- F07: `eval-results.jsonl` es leído como evidencia relativa.
- Seguridad: candidatos fuera del `securityProfiles` se descartan.
- Configuración inválida: falla sin seleccionar silenciosamente.
- `git diff --check`: sin errores.

```yaml
status: approved
attempt: 1
tests: 241
feedback:
  - Suite completa y contrato adaptativo ejecutados con resultado verde tras reconciliar develop con F10.
```
