# Log de corrección metodológica post-emisión

Commit auditado (sin cambios): `34773af3b03d0bd84b0c88f621353a7dfd6a83ed`

## Motivo

Seis observaciones metodológicas recibidas sobre el borrador inicial del
informe. Ninguna requirió re-inspeccionar código/documentación/config del
repositorio auditado; solo corregir interpretación del framework y
ejecutar una verificación pendiente que era razonable y segura.

## Cambios aplicados

1. Q6.5 reclasificado de N/A a aplicable y puntuado (perfil TEMPLATE
   incluye "documentación compilada" explícitamente). Se ejecutó
   `pip install mkdocs-material && mkdocs build --strict` — exit 0.
   Nuevo hallazgo F-007 (Q6.5, MINOR, -0.50): el build funciona, pero el
   pipeline completo (build+deploy) nunca se ejecutó de punta a punta
   porque `main` no existe en el remoto.
2. Recalculo completo: puntos aplicables 98 -> 100 (ya no hay N/A);
   puntos obtenidos 90.25 -> 92.25; score bruto 92.09 -> 92.25; score
   final sin cambio (79, mismo Gate G2 dominante en ambos casos).
3. Sección Q reescrita: F-004 activa el Gate G2 (por eso el score final
   es 79), pero closing solo F-004 sube el score a 94.50, no a 100 --
   F-001/F-002/F-003/F-005/F-007 también deben cerrarse.
4. Corrección de F-004 endurecida: una notificación post-hoc sin
   prevención/reversión real recupera como máximo la mitad de los
   puntos de Q6.2 (DÉBIL 25% -> PARCIAL 50%), no el criterio completo.
   Solo branch protection real o un control que efectivamente prevenga
   o revierta recuperan el criterio a COMPLETO.
5. F-006 (pinning de Actions a SHA) reclasificado de MINOR puntuable a
   SUGGESTION: sin evidencia de riesgo objetivo no cubierto por otro
   mecanismo (Actions oficiales, repo privado de un solo mantenedor,
   sin contribuciones externas no confiables, pull_request_target ya
   usa el patrón seguro de checkout de rama confiable). Movido a
   "Mejoras opcionales" (sección K). +0.50 dejó de restar puntos en
   Q7.3, que vuelve a COMPLETO.
6. Validación de consistencia repetida con los números corregidos:
   puntos obtenidos (92.25) + puntos recuperables obligatorios (7.75)
   = puntos aplicables (100.00). Igualdad exacta. Resultado:
   CONSISTENCIA METODOLÓGICA = PASS.

## Resultado

Score bruto: 92.25/100 (antes 92.09/100 sobre 98 aplicables)
Score final: 79/100 (sin cambio)
Consistencia metodológica: PASS
Registrado como BASELINE oficial (no se degrada a provisional ni a
inconsistente, porque la validación de consistencia con los números
corregidos se cumple de forma exacta).

---

## Segunda ronda de corrección (Q6.5 / F-007)

Commit auditado (sin cambios): `34773af3b03d0bd84b0c88f621353a7dfd6a83ed`

### Motivo

Observación: F-007 penalizaba Q6.5 por la ausencia de ejecución
histórica de `docs.yml` sobre `main`, pese a que ya existía evidencia
directa (`mkdocs build --strict` -> exit 0) de que el build de
documentación es reproducible. Q6.5 se llama "Build y artefactos
reproducibles" -- evalua reproducibilidad del build, no ejecucion
historica de despliegue. Ademas, main/release sigue declarado como
capacidad futura/prospectiva (mismo criterio ya aplicado a Q6.4):
AUDIT_RULES S45 y QUALITY_SCORE prohiben penalizar automaticamente una
capacidad prospectiva por no haber sido ejercida todavia.

### Revision

No se encontro ningun otro defecto objetivo de reproducibilidad del
build (ejecucion limpia, deterministica, exit 0, sin advertencias
promovidas a error por --strict, usando el comando oficial exacto de
docs.yml).

### Cambios aplicados

1. F-007 retirado como hallazgo puntuable (queda documentado como
   "retirado" en la seccion H para trazabilidad, no borrado en
   silencio).
2. Q6.5 = COMPLETO = 2.00/2.00.
3. La ausencia de ejecucion historica de docs.yml pasa a ser
   NO VERIFICADO CONTEXTUAL (seccion L): sin impacto en puntuacion.
4. Recalculo completo del informe.

### Resultado matematico

Puntos aplicables: 100.00
Puntos obtenidos: 92.75 (antes 92.25)
Score bruto: 92.75/100 (antes 92.25/100)
Puntos recuperables obligatorios: 7.25 (antes 7.75)
Validacion: 92.75 + 7.25 = 100.00 -- exacta
Score final: 79/100 (sin cambio, Gate G2 por F-004 sigue siendo mas
restrictivo que el bruto en todos los calculos: 92.09 -> 92.25 -> 92.75,
los tres > 79)
Consistencia metodologica: PASS

Registrada como BASELINE oficial (no provisional, no inconsistente).
