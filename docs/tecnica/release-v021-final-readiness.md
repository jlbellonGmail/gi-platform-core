# Readiness final de GI-PLATFORM-CORE v0.2.1

La release v0.2.1 distribuye el paquete Python `gi-platform-core` con versión de distribución y `gi_platform_core.__version__` alineadas en `0.2.1`.

El contrato público de CoreApi para identidad y vinculación permanece en `0.2.0`; la versión del paquete no modifica ese contrato ni las releases históricas.

La secuencia reproducible de validación es:

1. Ejecutar `scripts/release-readiness.ps1 -Version v0.2.1 -DryRun` sobre `develop` limpio y sincronizado.
2. Ejecutar `check-integrity.ps1` y `validate-supply-chain.ps1`.
3. Ejecutar la suite completa con Python 3.12.
4. Construir el wheel con `python -m build --wheel`.
5. Instalar el wheel en un entorno virtual externo al checkout e importar `CoreApi`, `InMemoryCoreStore` y `__version__`.
6. Crear el tag anotado y la release sólo después de que el candidato tenga CI verde.
7. Descargar el wheel asociado a la release y repetir la instalación externa.

La prueba externa debe ejecutarse desde un directorio fuera del checkout para evitar que el árbol fuente contamine `sys.path`.
