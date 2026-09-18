# Plan — SDD adaptativo

1. Añadir un materializador PowerShell aislado que lea JSON/JSONL de ASSESS,
   valide su contrato y traduzca `depth` a un perfil SDD.
2. Mantener los scripts y contratos v1 sin modificar; el perfil es una
   capacidad opt-in para la planificación actual.
3. Cubrir LIGHT/STANDARD/FULL, consumo de la última observación JSONL y
   rechazo de entradas inválidas con pytest ejecutando PowerShell real.
4. Documentar contrato, límites y uso; actualizar índices con el script común.
5. Validar suite focal, suite completa, adaptadores, contrato, diff y CI.

No se agregan agentes, modos, dependencias, router, gates de producto ni
framework de Evals de Fase 07.
