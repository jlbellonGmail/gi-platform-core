# F05 — Contrato adaptativo de evidencias

## Objetivo
Reducir artefactos humanos obligatorios sin perder trazabilidad, validación ni reentrada. La profundidad proviene de ASSESS/SDD.

## Criterios de aceptación
- AC-1: contrato único para LEGACY y ADAPTIVE, con requisitos distintos LIGHT/STANDARD/FULL.
- AC-2: todo run adaptativo exige SUMMARY estructurado y enlaces sólo existentes.
- AC-3: LIGHT puede omitir spec/plan/tasks/audit/test-report/decision cuando no son necesarios y no acepta placeholders.
- AC-4: STANDARD exige intención, plan, QA, review y documentación; FULL agrega tasks, decisión y auditoría.
- AC-5: ready-for-pr valida antes de mutar ROADMAP y enumera sólo evidencia existente.
- AC-6: runs históricos sin sdd.json no se reescriben.
- AC-7: convergencia JSON se consume como evidencia máquina, sin Markdown por iteración; proveedor/modelo no afectan el contrato.
- AC-8: hay pruebas para niveles, faltantes, placeholders, SUMMARY y convergencia.
- AC-9: se crean docs técnica/usuario, enlaces exactos y decision.md.

## Clarificaciones realizadas
La autorización humana fija que F05 no inicia F06 ni fases posteriores y que SUMMARY permanece obligatorio. No quedan decisiones bloqueantes.
