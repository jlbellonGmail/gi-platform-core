# Uso: identidad de acceso para Person

Con Python 3.12+, usar `CoreService` con `InMemoryCoreStore` o
`SupabaseCoreStore`, envolverlo con `CoreApi` y llamar a
`validate_identity`, `link_identity` y `unlink_identity`. La autenticación y
el `TenantContext` los aporta el host; los consumidores no acceden a stores
privados.

Para HTTP, configurar el autenticador del host y ejecutar:

```powershell
$env:CORE_AUTH_MODULE = "mi_host.auth:authenticate"
python -m gi_platform_core.http_server
```

También pueden configurarse `CORE_HTTP_HOST` y `CORE_HTTP_PORT`. El host debe
terminar TLS y validar su mecanismo de sesión/JWT existente. Las respuestas de
error son JSON-safe y versionadas. Aplicar
`supabase/migrations/20260920000000_identity_links.sql`; las claves
server-side y `service_role` nunca se entregan a un vertical, navegador o
cliente.
