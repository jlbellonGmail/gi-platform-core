# SUMMARY — Release history manifest

Versión: v0.2.1  
Estado: en implementación  
Tipo: Feature  
SDD: FULL  
PR: pendiente de crear hacia develop  
Merge: no autorizado; requiere decisión humana

## Objetivo

Retirar la dependencia rígida del gate respecto de `v1.1.0`, inexistente en
este repositorio, y usar tags históricos declarados por release.

## Resultado

El gate resuelve `historicalTags` desde el manifiesto y valida existencia y
tipo anotado.

## Cambios principales

Script, regresiones, manifiesto, documentación y evidencia de work unit.

## Validación

Se ejecutará readiness sobre el HEAD final con `v0.1.0` y `v0.2.0` reales.

## Decisiones

No se crean tags históricos ficticios ni se modifican releases publicadas.

## Incidencias

La ejecución inicial falló por la referencia rígida a `v1.1.0`.

## Detalle

El cambio es de gobernanza de release y no afecta APIs, datos o RLS.
