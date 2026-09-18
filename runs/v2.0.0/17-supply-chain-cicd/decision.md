# Decisión F12

Se adopta pinning SHA para las Actions existentes y versiones exactas para
las dependencias del tooling. Se agrega un gate pequeño y portable porque
reduce riesgo verificable sin incorporar una plataforma externa.

No se agregan SBOM/provenance ni artifacts: el template no genera un build de
producto y hacerlo ahora sería ceremonia sin evidencia de valor. F15 decidirá
la implementación de releases con commit/tag y evidencia de validación.
