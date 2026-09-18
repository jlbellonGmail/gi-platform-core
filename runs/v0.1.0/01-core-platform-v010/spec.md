# Spec — Core Platform v0.1.0

## Objetivo

Entregar un núcleo común y neutral consumible por productos/verticales, con
tenancy, identidad base, autorización contextual, aislamiento, auditoría y
contratos públicos.

## Criterios de aceptación

- AC-1: Organization admite múltiples Sites y Site no puede pertenecer a otra Organization.
- AC-2: UserProfile admite múltiples OrganizationMembership.
- AC-3: autorización exige membership activa, role y permission compatibles.
- AC-4: el contexto Site exige pertenencia y acceso explícito.
- AC-5: ninguna decisión permite acceso cruzado entre Organizations.
- AC-6: mutaciones y decisiones generan AuditEvent estructurado.
- AC-7: CoreApi expone contratos versionados `0.1.0` sin tablas privadas.
- AC-8: no se importa ni implementa lógica de Dental u otra vertical.
- AC-9: `docs/tecnica/core-platform-v010.md`, `docs/usuario/core-platform-v010.md` e índices quedan actualizados.
- AC-10: la evidencia queda en `runs/v0.1.0/01-core-platform-v010/`.

## Fuera de alcance

UI, HTTP concreto, base de datos concreta, Dental, CRM, finanzas, pacientes,
profesionales, chatbot, Voice y canales de presentación.
