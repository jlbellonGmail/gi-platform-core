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

    def create_user(self, external_subject: str, display_name: str) -> dict:
        return _public(self.service.create_user(external_subject, display_name))

    def authorize(self, user_id: str, organization_id: str, permission: str, site_id: str | None = None) -> dict:
        decision = self.service.authorize(TenantContext(user_id, organization_id, site_id), permission)
        return {"contract_version": CONTRACT_VERSION, "allowed": decision.allowed, "reason": decision.reason, "context": _public(decision.context)}
