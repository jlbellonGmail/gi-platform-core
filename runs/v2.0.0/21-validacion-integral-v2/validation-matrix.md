# Matriz integral F16

| Componente | Escenario | Resultado | Evidencia | Riesgo residual |
| --- | --- | --- | --- | --- |
| Fuentes canonicas | AGENTS/ROADMAP/STATUS/SUMMARY/docs coherentes | PASS | inspeccion + SUMMARY | STATUS requiere regeneracion final |
| Integrity | ROADMAP/runs/SUMMARY/Git | PASS | check-integrity.ps1 | warning snapshot stale antes de actualizar |
| Status | rama, HEAD, staleness | PASS | check-status.ps1 tras update | PR/CI temporal |
| Pytest | suite integral local | PASS | test-report-1.md | warnings CP1252; Python 3.14 local; PATH alternativo sin pytest |
| Reconciliacion | Windows local | PASS | 7/7 tests | CI Windows sigue siendo autoridad remota |
| Adaptive SDD | LIGHT/STANDARD/FULL | PASS | tests adaptive/materialize/contract | sin telemetria costo |
| Evals | normal y perfiles | PASS | agentic-evals 10/10 | determinista, no modelo real |
| Roles/convergence | Builder/Reviewer, loops, escalamiento | PASS | tests_convergence/agents/evals | ejecucion cognitiva no simulada |
| Routing | capacidades y aliases | PASS | tests_model_router | costo/latencia no medidos |
| Governance | single/multi, stale auth/review/CI | PASS | tests complete-approved/security | GitHub protection nativa limitada |
| Paralelizacion | oleadas A+B+C y reconcile | PASS | tests_parallel_units_f14 | simulacion de remoto |
| Conflictos | auto, semantic, blocked | PASS | unit-lifecycle tests | integracion manual no aplicable |
| Maintenance/close | normal, correctiva, historica | PASS | canonical/close tests | remoto real posterior |
| Cleanup | limpio/residual/registered/retry | PASS | cleanup/local reconciler tests | residual depende de Windows/EDR |
| Seguridad/MCP | deny-by-default, cero MCP | PASS | security-policy/mcp-tools | servidores reales no instalados |
| Supply chain/CI | pinning, permisos, jobs | PASS | validate-supply-chain + ci.yml | CI remoto del HEAD pendiente |
| Release | dry-run, SemVer, no publish | PASS | release-readiness rechazado hasta F16/F17 | F17 debe auditar release |
| v1.1.0 | tag e historia intactos | PASS | git tag/cat-file/log | sin riesgo observado |
| Skills | criterio profesional | NOT_APPLICABLE | `.agents/skills` vacio | activar solo procedimiento probado |
| Product tests | template sin stack | NOT_APPLICABLE | ci.yml placeholder | proyecto real debe reemplazar placeholder |
