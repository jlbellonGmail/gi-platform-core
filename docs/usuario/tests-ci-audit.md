# Validación del template

> **Nota de vigencia:** el texto histórico sobre un `product-tests` placeholder
> ya no aplica a GI-PLATFORM-CORE. El CI actual ejecuta pruebas reales del Core;
> consultar `.github/workflows/ci.yml`.

Ejecuta `pytest -q` para los tests del circuito y del Core.

En CI, `circuit-tests`, `product-tests` y `local-reconciler-tests` aparecen
separados. El último requiere Windows y confirma la limpieza segura de
worktrees sólo después del cierre remoto.

`.audit` es una evaluación global independiente; no reemplaza la revisión de
una feature ni autoriza un merge por sí solo.
