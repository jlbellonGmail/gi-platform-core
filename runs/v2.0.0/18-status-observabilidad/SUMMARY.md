# F13 — STATUS observabilidad y reentrada

Implementación: `scripts/update-status.ps1` y `scripts/check-status.ps1`.

Resultado: STATUS humano derivado, snapshot JSON opt-in, unidades activas desde worktrees Git, señales PR/CI/release y diagnósticos STALE/INCONSISTENTE/TEMPORAL/ERROR_REAL. Se preserva la incidencia histórica de derivación desde ramas `maintenance` para F14/F15 y no se corrige dentro de F13.

Tests: `pytest -q tests/test_status_scripts.py` PASS. Reconciliación F15: `2e8b39f` (`origin/develop` `333ea8d`). Autorización scoped F13 registrada y habilitada para fase 13. Merge: pendiente.
