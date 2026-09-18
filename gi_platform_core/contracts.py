"""Versioned public contracts independent from persistence entities."""

from dataclasses import asdict

from .application import CoreService
from .authorization import TenantContext

CONTRACT_VERSION = "0.1.0"


def _public(entity: object) -> dict:
    value = asdict(entity)
    value.pop("occurred_at", None)
    value["contract_version"] = CONTRACT_VERSION
    return value


class CoreApi:
    """Small transport-neutral facade suitable for HTTP, events or RPC."""

    def __init__(self, service: CoreService) -> None:
        self.service = service

    def create_organization(self, name: str) -> dict:
        return _public(self.service.create_organization(name))

    def create_site(self, organization_id: str, name: str) -> dict:
        return _public(self.service.create_site(organization_id, name))

    def list_organizations(self) -> list[dict]:
        return [_public(item) for item in self.service.list_organizations()]

    def list_memberships(self, user_id: str) -> list[dict]:
        return [_public(item) for item in self.service.list_memberships(user_id)]

    def create_permission(self, code: str, description: str) -> dict:
        return _public(self.service.create_permission(code, description))

    def create_role(self, organization_id: str, name: str, permission_codes: set[str]) -> dict:
        return _public(self.service.create_role(organization_id, name, permission_codes))

    def add_membership(self, user_id: str, organization_id: str) -> dict:
        return _public(self.service.add_membership(user_id, organization_id))

    def assign_role(self, membership_id: str, role_id: str) -> dict:
        return _public(self.service.assign_role(membership_id, role_id))

    def grant_site_access(self, membership_id: str, site_id: str) -> dict:
        return _public(self.service.grant_site_access(membership_id, site_id))

    def list_sites(self, user_id: str, organization_id: str, site_id: str | None = None) -> list[dict]:
        return [_public(item) for item in self.service.list_sites(TenantContext(user_id, organization_id, site_id))]

    def create_user(self, external_subject: str, display_name: str) -> dict:
        return _public(self.service.create_user(external_subject, display_name))

    def authorize(self, user_id: str, organization_id: str, permission: str, site_id: str | None = None) -> dict:
        decision = self.service.authorize(TenantContext(user_id, organization_id, site_id), permission)
        return {"contract_version": CONTRACT_VERSION, "allowed": decision.allowed, "reason": decision.reason, "context": _public(decision.context)}
