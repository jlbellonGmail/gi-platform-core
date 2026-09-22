"""Domain entities and invariants for the neutral Core."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import FrozenSet
from uuid import uuid4

from .errors import ValidationError


def new_id() -> str:
    return str(uuid4())


def required(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{label} is required")
    return value.strip()


@dataclass(frozen=True)
class Tenant:
    name: str
    id: str = field(default_factory=new_id)
    active: bool = True

    def __post_init__(self) -> None:
        required(self.name, "tenant.name")

    @property
    def organization_id(self) -> str:
        """Legacy identity alias; the canonical tenant identifier is ``id``."""
        return self.id


@dataclass(frozen=True)
class Location:
    tenant_id: str
    name: str
    id: str = field(default_factory=new_id)
    active: bool = True

    def __post_init__(self) -> None:
        required(self.tenant_id, "location.tenant_id")
        required(self.name, "location.name")

    @property
    def organization_id(self) -> str:
        return self.tenant_id


@dataclass(frozen=True)
class UserProfile:
    external_subject: str
    display_name: str
    id: str = field(default_factory=new_id)
    active: bool = True

    def __post_init__(self) -> None:
        required(self.external_subject, "user.external_subject")
        required(self.display_name, "user.display_name")


@dataclass(frozen=True)
class Permission:
    code: str
    description: str
    id: str = field(default_factory=new_id)
    active: bool = True

    def __post_init__(self) -> None:
        code = required(self.code, "permission.code")
        if any(ch.isspace() for ch in code) or ":" not in code:
            raise ValidationError("permission.code must use a namespaced value such as organization:read")
        required(self.description, "permission.description")


@dataclass(frozen=True)
class Role:
    tenant_id: str
    name: str
    permission_codes: FrozenSet[str]
    id: str = field(default_factory=new_id)
    active: bool = True

    def __post_init__(self) -> None:
        required(self.tenant_id, "role.tenant_id")
        required(self.name, "role.name")
        if not self.permission_codes:
            raise ValidationError("role.permission_codes must not be empty")

    @property
    def organization_id(self) -> str:
        return self.tenant_id


@dataclass(frozen=True)
class OrganizationMembership:
    user_id: str
    tenant_id: str
    active: bool = True
    location_ids: FrozenSet[str] = frozenset()
    id: str = field(default_factory=new_id)

    @property
    def organization_id(self) -> str:
        return self.tenant_id


@dataclass(frozen=True)
class IdentityLink:
    """Opaque vertical Person reference linked to a Core access identity."""

    tenant_id: str
    person_id: str
    user_id: str
    id: str = field(default_factory=new_id)
    active: bool = True

    def __post_init__(self) -> None:
        required(self.tenant_id, "identity_link.tenant_id")
        required(self.person_id, "identity_link.person_id")
        required(self.user_id, "identity_link.user_id")

    @property
    def organization_id(self) -> str:
        return self.tenant_id


@dataclass(frozen=True)
class MembershipRole:
    membership_id: str
    role_id: str
    id: str = field(default_factory=new_id)


@dataclass(frozen=True)
class AuditEvent:
    action: str
    actor_user_id: str | None
    tenant_id: str | None
    location_id: str | None
    outcome: str
    metadata: dict[str, str] = field(default_factory=dict)
    id: str = field(default_factory=new_id)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def organization_id(self) -> str | None:
        return self.tenant_id


# Temporary source compatibility for consumers released before CORE03.
Organization = Tenant
TenantMembership = OrganizationMembership
