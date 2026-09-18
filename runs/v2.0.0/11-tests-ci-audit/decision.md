# Decisión F06

- Se conserva la pirámide existente y se agrega sólo una batería pequeña de
  invariantes de `.audit`, porque la suite ya cubre los contratos F01–F05.
- `.audit` sigue siendo una evaluación global independiente: pytest valida la
  estructura mínima, pero no reemplaza una auditoría ni Reviewer.
- CI mantiene tres jobs: circuito, wiring de producto y reconciliador Windows.
- El launcher evita `EncodedCommand`; en hosts locales que terminan
  descendientes se conserva el diagnóstico como limitación ambiental y CI
  Windows sigue siendo la fuente de verificación del comportamiento real.
- F07 queda pendiente; F09 y F11 pueden planificarse en paralelo cuando sus
  prerrequisitos propios estén disponibles. F08 espera evidencia de F07.
