# Cierre post-merge reejecutable

Si el evento automático de cierre no aparece después de un merge, un
mantenedor puede ejecutar el workflow `Post-merge feature close` desde Actions
con el número de PR, rama, versión y slug exactos. El workflow vuelve a
verificar la PR y usa el procedimiento oficial; no se debe hacer un push
directo a `develop`.

