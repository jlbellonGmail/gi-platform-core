# Decisión T04

Se adopta un checker determinista separado porque `check-status.ps1` valida
únicamente el snapshot; ambos se conservan y no duplican lifecycle. `Txx`
usa el modo `Maintenance`, comparte cierre y no se convierte en fase Fxx.
