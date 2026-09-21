# Release readiness

Crear `runs/<version>/release-readiness/manifest.json` con esta forma mínima:

```json
{
  "schemaVersion": 1,
  "roadmapItems": ["05-person-identity-linking"]
}
```

Luego ejecutar:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\release-readiness.ps1 `
  -Version v0.2.1 -DryRun
```

El comando sólo valida; no crea ni publica recursos.
