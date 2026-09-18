# Decision F16

Se conserva el diseno existente: F16 es una validacion, no una nueva capa de
orquestacion. La unica correccion de codigo es hacer tolerante el test de
recoleccion al formato de salida de pytest 8.3+, porque el harness exigia el
texto `tests collected` aunque pytest emitiera un conteo por archivo.

La suite del reconciliador Windows pasa localmente en este host, por lo que
la incidencia de F14 se clasifica como limitacion/interferencia historica del
entorno, no como bug reproducido del circuito. Python 3.14 local no coincide
con CI 3.12 y produce warnings de decodificacion CP1252 en subprocesses; se
registran como riesgo residual y no se ocultan.

No se publica `v2.0.0`, no se crea tag y F17 no se inicia.
