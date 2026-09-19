"""Versioned, JSON-safe public contracts independent from persistence entities."""

from dataclasses import asdict
from datetime import date, datetime
from typing import Any

from .application import CoreService
from .authorization import TenantContext

CONTRACT_VERSION = "0.1.0"


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


def _public(entity: object) -> dict:
    value = asdict(entity)
    value.pop("occurred_at", None)
    value = _json_value(value)
    value["contract_version"] = CONTRACT_VERSION
    return value


class CoreApi:
    """Small transport-neutral facade suitable for HTTP, events or RPC."""

    def __init__(self, service: CoreService) -> None:
        self.service = service

    def create_organization(self, name: str) -> dict:
        return _public(self.service.create_organization(name))

    def create_location(self, organization_id: str, name: str) -> dict:
        return _public(self.service.create_location(organization_id, name))

    def list_organizations(self, user_id: str) -> list[dict]:
        return [_public(item) for item in self.service.list_organizations(user_id)]

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
