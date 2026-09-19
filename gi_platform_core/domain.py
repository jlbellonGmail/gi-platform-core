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
class Organization:
    name: str
    id: str = field(default_factory=new_id)
    active: bool = True

    def __post_init__(self) -> None:
        required(self.name, "organization.name")


@dataclass(frozen=True)
class Location:
    organization_id: str
    name: str
    id: str = field(default_factory=new_id)
    active: bool = True

    def __post_init__(self) -> None:
        required(self.organization_id, "location.organization_id")
        required(self.name, "location.name")


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
    organization_id: str
    name: str
    permission_codes: FrozenSet[str]
    id: str = field(default_factory=new_id)
    active: bool = True

    def __post_init__(self) -> None:
        required(self.organization_id, "role.organization_id")
        required(self.name, "role.name")
        if not self.permission_codes:
            raise ValidationError("role.permission_codes must not be empty")


@dataclass(frozen=True)
class OrganizationMembership:
    user_id: str
    organization_id: str
    active: bool = True
    location_ids: FrozenSet[str] = frozenset()
    id: str = field(default_factory=new_id)


@dataclass(frozen=True)
class MembershipRole:
    membership_id: str
    role_id: str
    id: str = field(default_factory=new_id)


@dataclass(frozen=True)
class AuditEvent:
    action: str
    actor_user_id: str | None
    organization_id: str | None
    location_id: str | None
    outcome: str
    metadata: dict[str, str] = field(default_factory=dict)
    id: str = field(default_factory=new_id)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
