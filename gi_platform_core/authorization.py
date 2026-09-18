"""Tenant context and authorization value objects."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TenantContext:
    user_id: str
    organization_id: str
    site_id: str | None = None


@dataclass(frozen=True)
class AuthorizationDecision:
    allowed: bool
    reason: str
    context: TenantContext

    def require(self) -> None:
        if not self.allowed:
            from .errors import AuthorizationError

            raise AuthorizationError(self.reason)
