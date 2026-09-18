"""GI-PLATFORM-CORE public package for v0.1.0."""

from .adapters import InMemoryCoreStore
from .application import CoreService
from .authorization import AuthorizationDecision, TenantContext
from .contracts import CoreApi, CONTRACT_VERSION

__all__ = [
    "AuthorizationDecision",
    "CONTRACT_VERSION",
    "CoreApi",
    "CoreService",
    "InMemoryCoreStore",
    "TenantContext",
]
