# Nota: flakiness de pytest local (Windows) vs. CI oficial

Se ejecutó `pytest -v tests/` tres veces contra el mismo estado limpio
del commit `9e18063` (working tree limpio, sin cambios entre corridas):

- Corrida 1 (suite completa): 194 passed, 3 failed —
  `test_close_feature_script.py::test_already_closed_feature_is_idempotent_and_does_not_create_empty_commit`,
  `test_feature_contract_scripts.py::test_contract_rejects_link_outside_managed_zone`,
  `test_local_reconciler_scripts.py::test_reconciler_never_removes_dirty_worktree`.
  Duración: 1737.40s.
- Corrida 2 (solo esos 3 tests, aislados): 3 passed. Duración: 31.78s.
- Corrida 3 (suite completa de nuevo): 195 passed, 2 failed — un
  conjunto **distinto** al de la corrida 1:
  `test_feature_contract_scripts.py::test_ready_for_pr_blocks_real_gh_error`,
  `test_local_reconciler_scripts.py::test_start_reconciler_returns_quickly`.
  Duración: 1566.11s.

Causa raíz observada directamente en la corrida 3 (traceback real):

```
Cloning into bare repository '...\pytest-36\test_start_reconciler_returns_0\origin.git'...
error: could not write config file ...origin.git/config: Permission denied
fatal: could not set 'core.ignorecase' to 'true'
```

`Permission denied` al escribir un archivo de configuración Git dentro de
un directorio temporal de Windows, en un test que dispara procesos
`git`/`pwsh` reales de forma intensiva. Esto es exactamente el patrón que
`docs/tecnica/circuito-agentico.md` documenta como "EDR/antivirus
agresivo bloquea el reconciliador local (Windows)" — no un fallo
determinista ligado al contenido del commit auditado.

Evidencia que corrobora que es ruido ambiental del entorno del auditor,
no una regresión real:

1. Los 3 tests que fallaron en la corrida 1 pasan de forma aislada y
   determinista en la corrida 2.
2. El conjunto de tests que falla cambia entre corridas (3 tests
   distintos en la corrida 1, 2 tests totalmente distintos en la
   corrida 3) — no reproducible de forma consistente, característica de
   contención de recursos/EDR, no de un bug determinista del código.
3. `.pytest_cache` también mostró warnings de Windows
   (`[WinError 183] No se puede crear un archivo que ya existe`) en
   ambas corridas, reforzando que el entorno local tiene fricción de
   filesystem/permitting ajena al proyecto.
4. El mecanismo OFICIAL de verificación (`.github/workflows/ci.yml`,
   jobs `circuit-tests` en `ubuntu-latest` y `local-reconciler-tests`
   en `windows-latest`) se consultó en vivo contra el commit exacto
   `9e18063` vía `gh api repos/{owner}/{repo}/commits/9e18063.../check-runs`
   (ver `check-runs-audited-commit-9e18063.json`): los 4 checks
   (`circuit-tests`, `product-tests`, `local-reconciler-tests`,
   `guard-develop`) reportan `success`. `windows-latest` en GitHub
   Actions es, por diseño documentado del propio proyecto, el entorno
   Windows limpio sin EDR agresivo que sustituye la necesidad de
   confiar en una corrida local — ver AGENTS.md, sección CI/CD,
   `local-reconciler-tests`.

Clasificación (AUDIT_RULES.md §15/§16/§19 Caso B): la corrida CI oficial
es `VERIFICACIÓN OFICIAL DEL PROYECTO` = VERIFICADA (PASS). Las corridas
locales del auditor son `VERIFICACIÓN COMPLEMENTARIA DEL AUDITOR`, y su
flakiness se registra como `NO VERIFICADO — LIMITACIÓN DEL ENTORNO`
(entorno del auditor, no defecto del proyecto), sin penalizar Q5.3.
