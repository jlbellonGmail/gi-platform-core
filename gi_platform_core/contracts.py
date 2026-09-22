"""Versioned, JSON-safe public contracts independent from persistence entities."""

from dataclasses import asdict
from datetime import date, datetime
from typing import Any

from .application import CoreService
from .authorization import TenantContext

CONTRACT_VERSION = "0.1.0"
IDENTITY_CONTRACT_VERSION = "0.2.0"
TENANT_CONTRACT_VERSION = "0.3.0"


def _json_value(value: Any) -> Any:
    """Convert domain values to stable JSON-compatible primitives."""
    if isinstance(value, (set, frozenset)):
        return sorted(_json_value(item) for item in value)
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    return value


def _public(entity: object, version: str = CONTRACT_VERSION) -> dict:
    value = asdict(entity)
    value.pop("occurred_at", None)
    value = _json_value(value)
    if "tenant_id" in value:
        value["organization_id"] = value["tenant_id"]
    value["contract_version"] = version
    return value


class CoreApi:
    """Small transport-neutral facade suitable for HTTP, events or RPC."""

    def __init__(self, service: CoreService) -> None:
        self.service = service

    def create_organization(self, name: str) -> dict:
        return _public(self.service.create_organization(name))

    def create_tenant(self, name: str) -> dict:
        result = _public(self.service.create_tenant(name), TENANT_CONTRACT_VERSION)
        result["tenant_id"] = result["id"]
        return result

    def create_location(self, organization_id: str, name: str) -> dict:
        return _public(self.service.create_location(organization_id, name))

    def list_organizations(self, user_id: str) -> list[dict]:
        return [_public(item) for item in self.service.list_organizations(user_id)]

    def list_tenants(self, user_id: str) -> list[dict]:
        result = []
        for item in self.service.list_tenants(user_id):
            public = _public(item, TENANT_CONTRACT_VERSION)
            public["tenant_id"] = public["id"]
            result.append(public)
        return result

    def list_memberships(self, user_id: str) -> list[dict]:
        return [_public(item) for item in self.service.list_memberships(user_id)]

    def create_permission(self, code: str, description: str) -> dict:
        return _public(self.service.create_permission(code, description))

    def create_role(self, organization_id: str, name: str, permission_codes: set[str]) -> dict:
        return _public(self.service.create_role(organization_id, name, set(permission_codes)))

    def add_membership(self, user_id: str, organization_id: str) -> dict:
        return _public(self.service.add_membership(user_id, organization_id))

    def assign_role(self, membership_id: str, role_id: str) -> dict:
        return _public(self.service.assign_role(membership_id, role_id))

    def grant_location_access(self, membership_id: str, location_id: str) -> dict:
        return _public(self.service.grant_location_access(membership_id, location_id))

    def list_locations(self, user_id: str, organization_id: str, location_id: str | None = None) -> list[dict]:
        return [_public(item) for item in self.service.list_locations(TenantContext(user_id, organization_id, location_id))]

    def create_user(self, external_subject: str, display_name: str) -> dict:
        return _public(self.service.create_user(external_subject, display_name))

    def authorize(self, user_id: str, organization_id: str, permission: str, location_id: str | None = None) -> dict:
        decision = self.service.authorize(TenantContext(user_id, organization_id, location_id), permission)
        return {"contract_version": CONTRACT_VERSION, "allowed": decision.allowed, "reason": decision.reason, "context": _public(decision.context)}

    def validate_identity(self, organization_id: str, user_id: str, external_subject: str) -> dict:
        user = self.service.resolve_identity(organization_id, user_id, external_subject)
        return {"contract_version": IDENTITY_CONTRACT_VERSION, "organization_id": organization_id,
                "user": _public(user, IDENTITY_CONTRACT_VERSION), "valid": True}

    def link_identity(self, actor_user_id: str, organization_id: str, person_id: str,
                      user_id: str, external_subject: str) -> dict:
        link = self.service.link_identity(TenantContext(actor_user_id, organization_id), person_id, user_id, external_subject)
        return _public(link, IDENTITY_CONTRACT_VERSION)

    def unlink_identity(self, actor_user_id: str, organization_id: str, person_id: str) -> dict:
        link = self.service.unlink_identity(TenantContext(actor_user_id, organization_id), person_id)
        return {"contract_version": IDENTITY_CONTRACT_VERSION, "organization_id": organization_id,
                "person_id": person_id, "removed": link is not None}
