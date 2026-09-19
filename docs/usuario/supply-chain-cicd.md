# Supply chain y CI/CD

> **Nota de vigencia:** GI-PLATFORM-CORE ya declara un paquete Python y
> pruebas reales del Core. Las referencias históricas al placeholder de
> `product-tests` describen la baseline del template, no el estado actual.

El repositorio verifica automáticamente Actions fijadas, permisos explícitos,
dependencias reproducibles y pruebas del paquete Core.

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-supply-chain.ps1
pytest -q tests/test_supply_chain_policy.py
```

No hay release automático en F12; las releases pertenecen a F15.
