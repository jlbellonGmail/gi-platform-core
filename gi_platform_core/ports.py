"""Ports consumed by the application layer and implemented by adapters."""

from typing import Protocol

from .domain import (
    AuditEvent,
    MembershipRole,
    Organization,
    OrganizationMembership,
    Permission,
    Role,
    Site,
    UserProfile,
)


class CoreStore(Protocol):
    organizations: dict[str, Organization]
    sites: dict[str, Site]
    users: dict[str, UserProfile]
    memberships: dict[str, OrganizationMembership]
    permissions: dict[str, Permission]
    roles: dict[str, Role]
    membership_roles: dict[str, MembershipRole]

    def record_audit(self, event: AuditEvent) -> None: ...


class AuditSink(Protocol):
    def record_audit(self, event: AuditEvent) -> None: ...
