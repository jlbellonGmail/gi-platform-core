status: approved
scope: 04-post-merge-close-dispatch
head: HEAD
base: develop

Revisión independiente del estado publicado de la PR #4: el workflow conserva
pull_request_target: closed, añade workflow_dispatch con inputs obligatorios y
valida la correspondencia exacta entre versión, slug y rama Feature. El cierre
delegado sigue siendo close-feature.ps1, que verifica PR mergeada contra
develop. No se modificó guard-develop-branch.yml ni se habilitaron operaciones
destructivas. La implementación queda aprobada para HITL SingleMaintainer.
