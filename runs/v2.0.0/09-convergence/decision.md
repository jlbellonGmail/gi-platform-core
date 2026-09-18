# Decisión F04

Se adopta un único script determinístico con estado JSON mínimo. La política
por defecto es LIGHT=2, STANDARD=4 y FULL=6, configurable por parámetro; el
fingerprint de findings abiertos evita repetir ciclos sin cambio material.
Planner sólo reingresa ante una decisión material indicada por Reviewer.
