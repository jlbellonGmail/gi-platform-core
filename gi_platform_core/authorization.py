"""Tenant context and authorization value objects."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TenantContext:
    user_id: str
    tenant_id: str
    location_id: str | None = None

    @property
    def organization_id(self) -> str:
        """Legacy alias retained for pre-CORE03 consumers."""
        return self.tenant_id


@dataclass(frozen=True)
class AuthorizationDecision:
    allowed: bool
    reason: str
    context: TenantContext

    def require(self) -> None:
        if not self.allowed:
            from .errors import AuthorizationError

            raise AuthorizationError(self.reason)
