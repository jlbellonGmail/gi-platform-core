# Decision — Package version consistency

- La versión distribuida y `gi_platform_core.__version__` se alinean en
  `0.2.1`.
- CoreApi conserva los contratos públicos `0.1.0` y `0.2.0`; el patch no
  representa un cambio de contrato.
- La evidencia retrospectiva completa el expediente de la Feature 10 sin
  alterar el wheel ya publicado.
