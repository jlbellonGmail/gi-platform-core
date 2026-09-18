# Decision — Core Platform v0.1.0

- **Stack:** Python estándar, porque no existía stack de producto declarado y
  el alcance requiere un núcleo transport-neutral.
- **Persistencia:** port `CoreStore` y adaptador en memoria; no se fija una
  base de datos antes de que exista una necesidad de despliegue.
- **Autorización:** membership activa + role + permission + Organization y
  Site cuando corresponda; deny-by-default.
- **Contratos:** fachada `CoreApi` con `contract_version: 0.1.0`.
- **Verticales:** ninguna dependencia; `GI-CLINICADENTAL` solo queda como
  primera consumidora prevista en el contexto de producto.
