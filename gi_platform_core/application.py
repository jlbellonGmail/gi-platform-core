"""Server-side use cases. No UI, framework or database is imported here."""

from dataclasses import replace

from .authorization import AuthorizationDecision, TenantContext
from .domain import AuditEvent, MembershipRole, Organization, OrganizationMembership, Permission, Role, Site, UserProfile
from .errors import IsolationError, NotFoundError, ValidationError
from .ports import CoreStore


class CoreService:
    def __init__(self, store: CoreStore) -> None:
        self.store = store

    def _audit(self, action: str, actor: str | None, organization: str | None, site: str | None, outcome: str, **metadata: str) -> None:
        self.store.record_audit(AuditEvent(action, actor, organization, site, outcome, metadata))

    def create_organization(self, name: str, actor_user_id: str | None = None) -> Organization:
        entity = Organization(name)
        self.store.save_organization(entity)
        self._audit("organization.created", actor_user_id, entity.id, None, "success")
        return entity

    def create_site(self, organization_id: str, name: str, actor_user_id: str | None = None) -> Site:
        self._organization(organization_id)
        entity = Site(organization_id, name)
        self.store.save_site(entity)
        self._audit("site.created", actor_user_id, organization_id, entity.id, "success")
        return entity

    def list_organizations(self) -> list[Organization]:
        return list(self.store.organizations.values())

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

    def grant_site_access(self, membership_id: str, site_id: str) -> OrganizationMembership:
        membership = self._membership(membership_id)
        site = self._site(site_id)
        if site.organization_id != membership.organization_id:
            raise IsolationError("site belongs to another organization")
        updated = replace(membership, site_ids=frozenset((*membership.site_ids, site_id)))
        self.store.save_membership(updated)
        self._audit("membership.site_access_granted", membership.user_id, membership.organization_id, site_id, "success")
        return updated

    def authorize(self, context: TenantContext, permission_code: str) -> AuthorizationDecision:
        try:
            membership = next(m for m in self.store.all_memberships() if m.user_id == context.user_id and m.organization_id == context.organization_id)
        except StopIteration:
            return self._denied(context, "active membership required")
        if not membership.active:
            return self._denied(context, "membership is inactive")
        if context.site_id is not None:
            site = self.store.get_site(context.site_id)
            if site is None or site.organization_id != context.organization_id:
                return self._denied(context, "site is outside organization")
            if context.site_id not in membership.site_ids:
                return self._denied(context, "site access is not granted")
        roles = [self.store.get_role(link.role_id) for link in self.store.all_membership_roles() if link.membership_id == membership.id and self.store.get_role(link.role_id) is not None]
        if any(role.organization_id == context.organization_id and permission_code in role.permission_codes for role in roles):
            self._audit("authorization.checked", context.user_id, context.organization_id, context.site_id, "allowed", permission=permission_code)
            return AuthorizationDecision(True, "permission granted", context)
        return self._denied(context, "permission denied")

    def list_sites(self, context: TenantContext) -> list[Site]:
        self.authorize(context, "site:read").require()
        membership = next(
            membership for membership in self.store.all_memberships()
            if membership.user_id == context.user_id
            and membership.organization_id == context.organization_id
            and membership.active
        )
        allowed = set(membership.site_ids)
        return [
            site for site in self.store.all_sites()
            if site.organization_id == context.organization_id
            and site.id in allowed
            and (context.site_id is None or site.id == context.site_id)
        ]

    def _denied(self, context: TenantContext, reason: str) -> AuthorizationDecision:
        self._audit("authorization.checked", context.user_id, context.organization_id, context.site_id, "denied", reason=reason)
        return AuthorizationDecision(False, reason, context)

    def _organization(self, entity_id: str) -> Organization:
        if self.store.get_organization(entity_id) is None:
            raise NotFoundError("organization not found")
        return self.store.get_organization(entity_id)

    def _site(self, entity_id: str) -> Site:
        if self.store.get_site(entity_id) is None:
            raise NotFoundError("site not found")
        return self.store.get_site(entity_id)

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
