```yaml
status: approved
attempt: 2
feedback:
```

# QA F17 — intento 2

Se revalidó el contrato completo y el diff del wait. El comando ahora consulta
todos los checks de la PR, compatible con la limitación 403 de protección
nativa, y finaliza con error o timeout sin simular PASS. La suite integral y
los gates oficiales quedan sujetos a confirmación del CI remoto del HEAD.
