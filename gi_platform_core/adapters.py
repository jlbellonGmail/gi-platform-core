"""Minimal infrastructure adapters; replaceable without changing use cases."""

from .domain import AuditEvent, MembershipRole, Organization, OrganizationMembership, Permission, Role, Site, UserProfile


class InMemoryCoreStore:
    """Deterministic adapter for local development and automated tests."""

    def __init__(self) -> None:
        self.organizations: dict[str, Organization] = {}
        self.sites: dict[str, Site] = {}
        self.users: dict[str, UserProfile] = {}
        self.memberships: dict[str, OrganizationMembership] = {}
        self.permissions: dict[str, Permission] = {}
        self.roles: dict[str, Role] = {}
        self.membership_roles: dict[str, MembershipRole] = {}
        self.audit_events: list[AuditEvent] = []

    def record_audit(self, event: AuditEvent) -> None:
        self.audit_events.append(event)
