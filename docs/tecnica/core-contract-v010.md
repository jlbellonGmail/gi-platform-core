# Contrato público del Core v0.1.0

El contrato público se implementa en `gi_platform_core.contracts.CoreApi` y se
describe máquina-legiblemente en
`contracts/core-api-v0.1.0.manifest.json`. La versión del paquete y el campo
`contract_version` son `0.1.0`.

## Regla de consumo

El consumidor sólo debe depender de `CoreApi`, de los valores JSON que devuelve
y de las excepciones públicas de `gi_platform_core.errors`. No debe importar
entidades privadas, acceder a diccionarios de un store ni leer tablas Supabase.

Todas las respuestas son JSON-safe: conjuntos del dominio se exponen como
listas ordenadas y las fechas, cuando existan en una respuesta pública, como
ISO-8601. Cada respuesta incluye `contract_version`.

Las operaciones de lectura que enumeran organizaciones requieren `user_id` y
se limitan a organizaciones con membership activa; el consumidor no puede
listar el store completo.

## Compatibilidad

- Cambios compatibles dentro de `0.1.x` conservan nombres, campos existentes y
  significado de las decisiones.
- Un cambio incompatible incrementa el minor durante `0.x` y publica un nuevo
  manifiesto de contrato.
- El consumidor debe rechazar o registrar una versión que no soporte.
- Las reglas de Dental no forman parte de este contrato.

La lista completa de operaciones y sus invariantes está en el manifiesto JSON.
