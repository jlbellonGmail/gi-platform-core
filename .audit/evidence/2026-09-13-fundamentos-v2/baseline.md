# Baseline verificada antes de modificar el contenido del proyecto

Fecha: 2026-09-13. Repositorio: `jlbellonGmail/template`.
Se ejecutó `git fetch origin --prune --tags` correctamente.

| Referencia | Valor observado |
| --- | --- |
| HEAD del checkout principal | `9acd2b8`, `chore/cierre-pipeline-secuencial` |
| origin/develop / base del worktree | `bc8b883d99dc0f6eff1b20d54ce80e814a2e7549` |
| origin/main / commit v1.1.0 | `d13ffcf34b6d982a7b3b89a364c17762f5efad70` |
| Objeto del tag anotado v1.1.0 local y remoto | `34964e132074d6d36133f04933a412ddcd199ba7` |
| Árbol v1.1.0 y origin/develop | `38b5aa817a7833507a73853cb98f84e2328f5e06` |

`git diff --stat v1.1.0 origin/develop` vacío. La diferencia entre los
commits corresponde a la integración de release; iniciar desde develop
preserva exactamente el contenido estable sin introducir main en la rama.
No se mueve, recrea ni publica ningún tag.

Checkout principal registrado por Git: `C:/Proyectos/template`, accesible
en esta sesión como `D:/Proyectos/template`. Único cambio local preexistente:
` M STATUS.md`; no se copia ni modifica. La rama local develop está detrás
de origin/develop y no se usa como base. El registro inicial no contenía
otros worktrees. La rama chore histórica ya estaba integrada por PR #28;
no se presenta como trabajo pendiente ni se elimina.

Hash Git del STATUS ajeno, comprobado antes y después de la suite inicial:
`c80e4a65090e12d4ecb440427751eab3b03b074a`.

Nuevo worktree: `D:/Proyectos/worktrees/fundamentos-v2` (Git muestra el alias
`C:/Proyectos/worktrees/fundamentos-v2`), rama `chore/fundamentos-v2`, desde
origin/develop. No hay implementación ni commits directos en ramas estables.

Inspeccionados: AGENTS, ROADMAP, STATUS, arquitectura, `.agentic/` y schemas,
roles y modelos, `.audit/` reglas/estándar/perfil TEMPLATE, scripts, tests,
workflows, `.agents/skills/README.md` y `.agentic/mcp.json`. Skills canónicas
sin implementaciones; MCP canónico con `servers: {}`. Las herramientas
disponibles en la sesión no son dependencias nuevas del Template.

GitHub: sin PR abiertas al inicio. CI de main en release #29 verde
(run `34732002942`), CI de develop tras #28 verde (`34731802916`). Son
evidencias históricas de baseline, no sustituyen CI de la nueva PR.

Validación inicial de adaptadores: `pwsh -NoProfile -ExecutionPolicy Bypass
-File scripts/sync-agentic-adapters.ps1 -Check`, exit 0.
`python` del PATH pertenece al runtime local de herramientas y no contiene
pytest. Se usa el intérprete ya instalado `py -3.14 -m pytest`; no se
agregan dependencias ni se modifica el entorno global. CI usa Python 3.12.
