# Decisión — F11 Seguridad profesional

Se adopta una matriz pequeña de capacidades con `deny` por defecto. Sólo las
acciones remotas, externas, destructivas, de merge o de secretos requieren
gate. Se preserva `complete-approved-pr.ps1` porque ya valida aprobación
humana y HEAD vigente; se evita duplicar esa lógica.

La política es consumible por F10 mediante JSON y no implementa MCP. No se
implementa F12: SBOM, signing, provenance y pinning integral quedan fuera.
