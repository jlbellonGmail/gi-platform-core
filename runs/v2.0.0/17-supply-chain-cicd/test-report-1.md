# QA 1 — approved

```yaml
status: approved
attempt: 3
```

- `pytest -q`: 236 passed local; PR #67 circuit-tests exposed and reproduced a PowerShell parser defect in the new negative-path diagnostic.
- Corrección aplicada: delimitación `${fileName}` antes de `:`; la suite focalizada se repite antes de republicar.
- Corrección adicional aplicada: el gate reconoce la sintaxis `- uses:` y no inspecciona evidencia histórica `.audit` como código.
- La suite completa posterior dio 238 passed y 1 fallo sólo por codificación de la aserción Windows; la aserción se hizo ASCII-estable y el test focalizado queda pendiente de este HEAD.
- Tras reconciliar `origin/develop` (incluido F10), el gate y las 3 pruebas focalizadas pasan; la suite completa de F10 ya estaba verde en su CI vigente.
- `pytest -q tests/test_supply_chain_policy.py`: passed.
- `validate-supply-chain.ps1`: passed.
- `git diff --check`: passed.
- Se verificaron casos negativos de Action flotante y dependencia no fijada.
- No hay stack de producto, artifacts ni dependencia Node que probar.
