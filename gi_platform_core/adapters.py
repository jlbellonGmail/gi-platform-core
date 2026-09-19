"""Minimal infrastructure adapters; replaceable without changing use cases."""

from .domain import AuditEvent, MembershipRole, Organization, OrganizationMembership, Permission, Role, Location, UserProfile


class InMemoryCoreStore:
    """Deterministic adapter for local development and automated tests."""

    def __init__(self) -> None:
        self.organizations: dict[str, Organization] = {}
        self.locations: dict[str, Location] = {}
        self.users: dict[str, UserProfile] = {}
        self.memberships: dict[str, OrganizationMembership] = {}
        self.permissions: dict[str, Permission] = {}
        self.roles: dict[str, Role] = {}
        self.membership_roles: dict[str, MembershipRole] = {}
        self.audit_events: list[AuditEvent] = []

    def record_audit(self, event: AuditEvent) -> None:
        self.audit_events.append(event)

    def save_organization(self, entity: Organization) -> None:
        self.organizations[entity.id] = entity

    def save_location(self, entity: Location) -> None:
        self.locations[entity.id] = entity

    def save_user(self, entity: UserProfile) -> None:
        self.users[entity.id] = entity

    def save_membership(self, entity: OrganizationMembership) -> None:
        self.memberships[entity.id] = entity

    def save_permission(self, entity: Permission) -> None:
        self.permissions[entity.code] = entity

    def save_role(self, entity: Role) -> None:
        self.roles[entity.id] = entity

    def save_membership_role(self, entity: MembershipRole) -> None:
        self.membership_roles[entity.id] = entity

    def get_organization(self, entity_id: str): return self.organizations.get(entity_id)
    def get_location(self, entity_id: str): return self.locations.get(entity_id)
    def get_user(self, entity_id: str): return self.users.get(entity_id)
    def get_membership(self, entity_id: str): return self.memberships.get(entity_id)
    def get_role(self, entity_id: str): return self.roles.get(entity_id)
    def all_locations(self): return self.locations.values()
    def all_memberships(self): return self.memberships.values()
    def all_roles(self): return self.roles.values()
    def all_membership_roles(self): return self.membership_roles.values()
    def all_permissions(self): return self.permissions.values()
