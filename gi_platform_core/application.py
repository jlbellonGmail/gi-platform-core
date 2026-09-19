"""Server-side use cases. No UI, framework or database is imported here."""

from dataclasses import replace

from .authorization import AuthorizationDecision, TenantContext
from .domain import AuditEvent, MembershipRole, Organization, OrganizationMembership, Permission, Role, Location, UserProfile
from .errors import IsolationError, NotFoundError, ValidationError
from .ports import CoreStore


class CoreService:
    def __init__(self, store: CoreStore) -> None:
        self.store = store

    def _audit(self, action: str, actor: str | None, organization: str | None, location: str | None, outcome: str, **metadata: str) -> None:
        self.store.record_audit(AuditEvent(action, actor, organization, location, outcome, metadata))

    def create_organization(self, name: str, actor_user_id: str | None = None) -> Organization:
        entity = Organization(name)
        self.store.save_organization(entity)
        self._audit("organization.created", actor_user_id, entity.id, None, "success")
        return entity

    def create_location(self, organization_id: str, name: str, actor_user_id: str | None = None) -> Location:
        self._organization(organization_id)
        entity = Location(organization_id, name)
        self.store.save_location(entity)
        self._audit("location.created", actor_user_id, organization_id, entity.id, "success")
        return entity

    def list_organizations(self, user_id: str) -> list[Organization]:
        """List only active organizations visible through active memberships."""
        self._user(user_id)
        organization_ids = {
            membership.organization_id
            for membership in self.store.all_memberships()
            if membership.user_id == user_id and membership.active
        }
        return [
            organization
            for organization in self.store.organizations.values()
            if organization.active and organization.id in organization_ids
        ]

    def list_memberships(self, user_id: str) -> list[OrganizationMembership]:
        self._user(user_id)
        return [m for m in self.store.all_memberships() if m.user_id == user_id]

    def create_user(self, external_subject: str, display_name: str) -> UserProfile:
        entity = UserProfile(external_subject, display_name)
        self.store.save_user(entity)
        self._audit("user.created", entity.id, None, None, "success")
        return entity

    def create_permission(self, code: str, description: str) -> Permission:
        entity = Permission(code, description)
        if entity.code in self.store.permissions:
            raise ValidationError(f"permission already exists: {entity.code}")
        self.store.save_permission(entity)
        self._audit("permission.created", None, None, None, "success", code=entity.code)
        return entity

    def create_role(self, organization_id: str, name: str, permission_codes: set[str]) -> Role:
        self._organization(organization_id)
        missing = permission_codes - self.store.permissions.keys()
        if missing:
            raise ValidationError(f"unknown permissions: {sorted(missing)}")
        entity = Role(organization_id, name, frozenset(permission_codes))
        self.store.save_role(entity)
        self._audit("role.created", None, organization_id, None, "success", role_id=entity.id)
        return entity

    def add_membership(self, user_id: str, organization_id: str) -> OrganizationMembership:
        self._user(user_id)
        self._organization(organization_id)
        if any(m.user_id == user_id and m.organization_id == organization_id for m in self.store.memberships.values()):
            raise ValidationError("membership already exists")
        entity = OrganizationMembership(user_id, organization_id)
        self.store.save_membership(entity)
        self._audit("membership.created", user_id, organization_id, None, "success", membership_id=entity.id)
        return entity

    def assign_role(self, membership_id: str, role_id: str) -> MembershipRole:
        membership = self._membership(membership_id)
        role = self._role(role_id)
        if role.organization_id != membership.organization_id:
            raise IsolationError("role belongs to another organization")
        entity = MembershipRole(membership_id, role_id)
        self.store.save_membership_role(entity)
        self._audit("membership.role_assigned", membership.user_id, membership.organization_id, None, "success", role_id=role_id)
        return entity

    def grant_location_access(self, membership_id: str, location_id: str) -> OrganizationMembership:
        membership = self._membership(membership_id)
        location = self._location(location_id)
        if location.organization_id != membership.organization_id:
            raise IsolationError("location belongs to another organization")
        updated = replace(membership, location_ids=frozenset((*membership.location_ids, location_id)))
        self.store.save_membership(updated)
        self._audit("membership.location_access_granted", membership.user_id, membership.organization_id, location_id, "success")
        return updated

    def authorize(self, context: TenantContext, permission_code: str) -> AuthorizationDecision:
        try:
            membership = next(m for m in self.store.all_memberships() if m.user_id == context.user_id and m.organization_id == context.organization_id)
        except StopIteration:
            return self._denied(context, "active membership required")
        if not membership.active:
            return self._denied(context, "membership is inactive")
        if context.location_id is not None:
            location = self.store.get_location(context.location_id)
            if location is None or location.organization_id != context.organization_id:
                return self._denied(context, "location is outside organization")
            if context.location_id not in membership.location_ids:
                return self._denied(context, "location access is not granted")
        roles = [self.store.get_role(link.role_id) for link in self.store.all_membership_roles() if link.membership_id == membership.id and self.store.get_role(link.role_id) is not None]
        if any(role.organization_id == context.organization_id and permission_code in role.permission_codes for role in roles):
            self._audit("authorization.checked", context.user_id, context.organization_id, context.location_id, "allowed", permission=permission_code)
            return AuthorizationDecision(True, "permission granted", context)
        return self._denied(context, "permission denied")

    def list_locations(self, context: TenantContext) -> list[Location]:
        self.authorize(context, "location:read").require()
        membership = next(
            membership for membership in self.store.all_memberships()
            if membership.user_id == context.user_id
            and membership.organization_id == context.organization_id
            and membership.active
        )
        allowed = set(membership.location_ids)
        return [
            location for location in self.store.all_locations()
            if location.organization_id == context.organization_id
            and location.id in allowed
            and (context.location_id is None or location.id == context.location_id)
        ]

    def _denied(self, context: TenantContext, reason: str) -> AuthorizationDecision:
        self._audit("authorization.checked", context.user_id, context.organization_id, context.location_id, "denied", reason=reason)
        return AuthorizationDecision(False, reason, context)

    def _organization(self, entity_id: str) -> Organization:
        if self.store.get_organization(entity_id) is None:
            raise NotFoundError("organization not found")
        return self.store.get_organization(entity_id)

    def _location(self, entity_id: str) -> Location:
        if self.store.get_location(entity_id) is None:
            raise NotFoundError("location not found")
        return self.store.get_location(entity_id)

    def _user(self, entity_id: str) -> UserProfile:
        if self.store.get_user(entity_id) is None:
            raise NotFoundError("user not found")
        return self.store.get_user(entity_id)

    def _membership(self, entity_id: str) -> OrganizationMembership:
        if self.store.get_membership(entity_id) is None:
            raise NotFoundError("membership not found")
        return self.store.get_membership(entity_id)

    def _role(self, entity_id: str) -> Role:
        if self.store.get_role(entity_id) is None:
            raise NotFoundError("role not found")
        return self.store.get_role(entity_id)
