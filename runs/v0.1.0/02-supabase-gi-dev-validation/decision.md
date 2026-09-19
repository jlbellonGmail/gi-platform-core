# Decision — Supabase gi-dev validation

## Estado

Estado tecnico: en construcción; la aprobación de merge corresponde sólo al
HITL humano sobre una PR con CI verde.

## Decisiones demostrables

- Se conserva `SupabaseCoreStore` como adaptador y `CoreService` como capa de
  casos de uso.
- El project ref se compara con el hostname antes de instanciar el store con
  capacidad de escritura.
- El identificador sintético deriva del `sub` del JWT para permitir reintentos
  idempotentes sin nombres aleatorios.
- No se usa SQL administrativo ni se alteran políticas RLS.
