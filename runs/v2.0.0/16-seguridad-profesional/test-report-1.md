# QA — F11 Seguridad profesional

```yaml
status: approved
attempt: 1
```

## Resultado

- `pytest -q`: 232 passed in 609.25s.
- Batería focalizada seguridad/lifecycle/workflows: 54 passed in 21.72s.
- `security-policy.ps1`: política válida; autorización exacta acepta y scope
  ajeno/secreto rechaza.
- CI jobs de lectura: `contents: read` y `persist-credentials: false`.
- Limitación ambiental: PowerShell muestra advertencia XML del host en tests
  existentes; no produjo fallos ni expuso secretos.
