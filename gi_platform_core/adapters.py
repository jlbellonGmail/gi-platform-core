"""Minimal infrastructure adapters; replaceable without changing use cases."""

from threading import RLock
from .domain import AuditEvent, IdentityLink, MembershipRole, Organization, OrganizationMembership, Permission, Role, Location, UserProfile
from .errors import ConflictError


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
        self.identity_links: dict[str, IdentityLink] = {}
        self.audit_events: list[AuditEvent] = []
        self._identity_lock = RLock()

    @property
    def tenants(self):
        return self.organizations

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

    def save_identity_link(self, entity: IdentityLink) -> None:
        self.identity_links[entity.id] = entity

    def get_identity_link(self, entity_id: str): return self.identity_links.get(entity_id)
    def all_identity_links(self): return self.identity_links.values()

    def link_identity_atomic(self, entity: IdentityLink) -> IdentityLink:
        with self._identity_lock:
            existing = next((item for item in self.identity_links.values()
                             if item.active and item.organization_id == entity.organization_id
                             and item.person_id == entity.person_id), None)
            if existing and existing.user_id != entity.user_id:
                raise ConflictError("person is already linked to another identity")
            if existing:
                return existing
            self.save_identity_link(entity)
            return entity

    def unlink_identity_atomic(self, organization_id: str, person_id: str):
        with self._identity_lock:
            existing = next((item for item in self.identity_links.values()
                             if item.active and item.organization_id == organization_id
                             and item.person_id == person_id), None)
            if existing:
                self.identity_links.pop(existing.id, None)
            return existing

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
