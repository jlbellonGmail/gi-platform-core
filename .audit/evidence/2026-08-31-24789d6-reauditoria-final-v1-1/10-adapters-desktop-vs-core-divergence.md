# Divergencia sync-agentic-adapters.ps1 entre PowerShell Desktop y Core

## Comando y resultado (Windows PowerShell 5.1 Desktop, `powershell.exe`)

```
$PSVersionTable.PSVersion = 5.1.26100.9278 / PSEdition = Desktop

powershell -NoProfile -ExecutionPolicy Bypass -File ./scripts/sync-agentic-adapters.ps1 -Check
-> Adaptador desactualizado o divergente: .mcp.json
-> Adaptador desactualizado o divergente: opencode.json
-> exit 1
```

## Mismo comando bajo PowerShell 7 Core (`pwsh`), mismos archivos, mismo commit

```
$PSVersionTable.PSVersion = 7.6.4 / PSEdition = Core

pwsh -NoProfile -File ./scripts/sync-agentic-adapters.ps1 -Check
-> Adaptadores agenticos sincronizados.
-> exit 0
```

## Diff real generado por -AutoFix bajo Desktop edition (en worktree aislado, no aplicado al repo real)

Ver `git diff` capturado manualmente durante la auditoria (no persistido como
archivo binario aqui por brevedad): la unica diferencia es el formato de
serializacion de objetos/hashtables vacios de `ConvertTo-Json` entre
PSEdition Desktop y Core (indentacion y saltos de linea distintos para
`"mcpServers": {}` y para todo `opencode.json`), no una diferencia de
contenido semantico.

## Confirmacion: CI usa `pwsh`, no `powershell.exe`

`.github/workflows/ci.yml` linea 29:
`run: pwsh -NoProfile -ExecutionPolicy Bypass -File ./scripts/sync-agentic-adapters.ps1 -Check`

## Confirmacion: AGENTS.md instruye `powershell`, README.md instruye `pwsh`

AGENTS.md, seccion "Configuracion de modelos": todos los ejemplos de
`sync-agentic-adapters.ps1`, `ready-for-pr.ps1`, `wait-pr-ci.ps1`,
`complete-approved-pr.ps1` usan literalmente `powershell -NoProfile
-ExecutionPolicy Bypass -File ...`.
AGENTS.md, seccion "Herramientas locales requeridas": "Windows PowerShell
(`powershell.exe`) para los scripts de automatizacion en `scripts/*.ps1`."

README.md lineas 22 y 28: los mismos comandos usan literalmente `pwsh
-NoProfile -ExecutionPolicy Bypass -File ...`.

## Relevancia

Un usuario que siga literalmente AGENTS.md (el documento que el propio
proyecto define como fuente normativa/autoritativa, ver
`.audit/profiles/TEMPLATE.md` seccion 15) en una maquina Windows estandar
(PowerShell 5.1 preinstalado, sin instalar PowerShell 7 aparte) obtiene un
`FAIL` falso positivo al ejecutar exactamente el comando documentado
inmediatamente despues de editar `.agentic/`, sobre los archivos ya
commiteados en el commit auditado.
