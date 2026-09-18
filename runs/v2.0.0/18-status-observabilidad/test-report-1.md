# Test report 1

Verdict: approved

```yaml
status: approved
attempt: 1
```

- `pytest -q tests/test_status_scripts.py`: PASS (7 tests).
- Se verificó salida JSON de `update-status.ps1 -Json` sin escritura implícita.
- Se verificó `check-status.ps1 -Json` y clasificación de snapshot stale.
- `check-integrity.ps1`: PASS esperado según gate existente; cualquier warning de STATUS stale se regenera antes del cierre.

## Revalidación 2

```yaml
status: approved
attempt: 2
```

- `pytest -q tests/test_status_scripts.py`: 7 passed.
- Corrección verificada en Linux: `check-status.ps1` ya no incurre en recursión por el nombre de la función Git.

## Revalidación 3 — reconciliación F15

```yaml
status: approved
attempt: 3
```

- Merge de `origin/develop` (`333ea8d`) integrado en `2e8b39f`.
- `pytest -q tests/test_status_scripts.py`: 7 passed.
- `check-status.ps1 -Json`: ejecutable; reporta sólo snapshot regenerable y GitHub temporalmente no verificable.
- `check-integrity.ps1`: la ejecución aislada del host no finalizó; se conserva la incidencia conocida sin debilitar el gate.

## Revalidación 4

```yaml
status: approved
attempt: 4
```

Se corrigió la whitelist de autorización scoped para aceptar fase 13; los
tests focalizados y el CI previo al cambio permanecen verdes. El nuevo CI
queda requerido por el cambio de script.
