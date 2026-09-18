# Spec — ASSESS / motor adaptativo

## Intención

Materializar una primera capacidad determinista que use evidencia de rutas
cambiadas para recomendar riesgo y profundidad futura, sin activar todavía
SDD adaptativo ni alterar el pipeline v1.1.0.

## Hechos y supuestos

- Hecho: Fase 00 exige conservar el motor v1 hasta sustitución probada.
- Hecho: Fase 01 corresponde al ítem `06-assess-motor-adaptativo`.
- Supuesto explícito: la primera evidencia suficiente y portable es la lista
  de rutas cambiadas; el análisis semántico de diffs queda para fases futuras.
- No hay ambigüedad material de producto: la salida es recomendación auditable,
  no una decisión de autorización.

## Criterios de aceptación

- AC-1: existe un script PowerShell determinista que devuelve riesgo y una de
  las profundidades `LIGHT`, `STANDARD`, `FULL` a partir de rutas explícitas.
- AC-2: las señales sensibles/automatización son conservadoras y explicables;
  documentación/test aislado puede clasificarse `LOW/LIGHT`.
- AC-3: la falta de rutas falla cerradamente y no produce recomendación.
- AC-4: la salida incluye evidencia JSONL interoperable y no invoca IA,
  proveedores, MCP, orquestación ni modifica contratos v1.
- AC-5: hay tests automatizados para clasificación, evidencia y fallo cerrado.
- AC-6: se crean `docs/tecnica/assess-motor-adaptativo.md`,
  `docs/usuario/assess-motor-adaptativo.md`,
  `runs/v2.0.0/06-assess-motor-adaptativo/decision.md` y enlaces exactos en ambos
  índices.
