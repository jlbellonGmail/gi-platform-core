# Spec — Supabase gi-dev validation

## Alcance

Implementar un comando local que verifique el destino, autentique al usuario
de prueba, cree como máximo una organización sintética, un perfil y una
membership activa mediante los casos de uso existentes, y valide la visibilidad
RLS autenticada.

## Criterios de aceptación

- AC-1: el host debe coincidir exactamente con el project ref introducido para
  gi-dev antes de cualquier escritura.
- AC-2: password, JWT y clave server-side se leen ocultos y no se persisten.
- AC-3: el bootstrap es idempotente y aborta ante duplicados o datos no
  sintéticos equivalentes.
- AC-4: sólo se invocan `create_organization`, `create_user` y
  `add_membership`; la auditoría normal del Core permanece activa.
- AC-5: `validate_supabase_core.py --expect-visible organizations` pasa con el
  JWT del usuario de prueba.
- AC-6: las filas visibles autenticadas quedan acotadas por las relaciones
  permitidas por las policies vigentes.
- AC-7: no se modifican policies ni se ejecutan eliminaciones.
