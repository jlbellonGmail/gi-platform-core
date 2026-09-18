# Tasks: Arquitectura de roles por capacidades

- **T-01** — Definir Planner, Builder y Reviewer con capacidades y contratos.
  Verificación: `agents.json` contiene exactamente esos tres roles.
  Traza: AC-01, AC-02, AC-03.
- **T-02** — Mantener aliases históricos y routing desacoplado.
  Verificación: resolver aliases y modelos canónicos sin lock-in.
  Traza: AC-02, AC-05.
- **T-03** — Regenerar adaptadores y corregir mensaje versionado.
  Verificación: sync `-Check` y test de start pasan.
  Traza: AC-05, AC-06.
- **T-04** — Documentar arquitectura, uso, decisión e índices.
  Verificación: contrato de feature y SUMMARY pasan.
  Traza: AC-07.
- **T-05** — Ejecutar revisión independiente y regresión completa.
  Verificación: pytest y checks determinísticos verdes, sin F04.
  Traza: AC-03, AC-04, AC-08.
