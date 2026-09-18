# Plan F15

1. Implementar un único gate PowerShell read-only parametrizado por versión.
2. Generalizar el root de `check-integrity.ps1` para runs versionados,
   conservando el default compatible v2.0.0.
3. Añadir documentación técnica/usuario, evidencia SDD y pruebas de positivos
   y negativos.
4. Ejecutar suite, integridad, supply-chain, convergencia y revisión final.

La publicación real queda fuera del cambio y requiere PR, decisión humana y
gates sobre `main`.
