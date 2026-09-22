"""GI-PLATFORM-CORE public package v0.2.1."""

__version__ = "0.2.1"

from .adapters import InMemoryCoreStore
from .application import CoreService
from .authorization import AuthorizationDecision, TenantContext
from .contracts import CoreApi, CONTRACT_VERSION, IDENTITY_CONTRACT_VERSION, TENANT_CONTRACT_VERSION
from .http import AuthenticatedActor, create_app
from .supabase_adapter import SupabaseCoreStore
from .domain import Tenant, TenantMembership

__all__ = [
    "AuthenticatedActor", "AuthorizationDecision", "CONTRACT_VERSION", "CoreApi",
    "CoreService", "IDENTITY_CONTRACT_VERSION", "TENANT_CONTRACT_VERSION", "InMemoryCoreStore", "SupabaseCoreStore", "Tenant", "TenantMembership",
    "TenantContext", "__version__", "create_app",
]
