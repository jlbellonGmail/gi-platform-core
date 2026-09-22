"""Supabase REST adapter for the CoreStore port.

The host application supplies the URL and key.  The domain/application layers
never import this module, so Supabase remains an infrastructure adapter.
"""

from __future__ import annotations

import json
from dataclasses import asdict, replace
from datetime import datetime
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .domain import AuditEvent, IdentityLink, MembershipRole, Organization, OrganizationMembership, Permission, Role, Location, UserProfile, Tenant
from .errors import ConflictError, CoreError


class SupabaseError(CoreError):
    """A persistence or transport error returned by Supabase."""


class SupabaseCoreStore:
    """CoreStore implementation using the Supabase PostgREST API."""

    _tables = {
        "tenants": Tenant,
        "locations": Location,
        "user_profiles": UserProfile,
        "memberships": OrganizationMembership,
        "roles": Role,
        "permissions": Permission,
        "membership_roles": MembershipRole,
        "identity_links": IdentityLink,
    }

    def __init__(self, url: str, key: str, *, timeout: float = 10.0) -> None:
        if not url or not key:
            raise ValueError("SupabaseCoreStore requires url and key from the host application")
        self.url = url.rstrip("/")
        self.key = key
        self.timeout = timeout
        self.organizations: dict[str, Organization] = {}
        self.locations: dict[str, Location] = {}
        self.users: dict[str, UserProfile] = {}
        self.memberships: dict[str, OrganizationMembership] = {}
        self.permissions: dict[str, Permission] = {}
        self.roles: dict[str, Role] = {}
        self.membership_roles: dict[str, MembershipRole] = {}
        self.identity_links: dict[str, IdentityLink] = {}
        self._refresh()

    @property
    def tenants(self):
        return self.organizations

    def _request(self, table: str, method: str = "GET", *, query: str = "", body: Any = None, prefer: str = "return=representation") -> list[dict[str, Any]]:
        headers = {"apikey": self.key, "Authorization": f"Bearer {self.key}", "Content-Type": "application/json", "Accept-Profile": "core", "Content-Profile": "core", "Prefer": prefer}
        data = None if body is None else json.dumps(body, default=str).encode()
        request = Request(f"{self.url}/rest/v1/{table}{query}", data=data, headers=headers, method=method)
        try:
            with urlopen(request, timeout=self.timeout) as response:
                payload = response.read().decode()
        except Exception as exc:  # urllib errors intentionally stay provider-neutral to callers
            raise SupabaseError(f"Supabase request failed for core.{table}: {exc}") from exc
        if not payload:
            return []
        try:
            decoded = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise SupabaseError(f"invalid Supabase response for core.{table}") from exc
        if isinstance(decoded, dict) and decoded.get("code"):
            raise SupabaseError(decoded.get("message", "Supabase error"))
        return decoded if isinstance(decoded, list) else []

    def _refresh(self) -> None:
        for table, cls in self._tables.items():
            rows = self._request(table)
            for row in rows:
                entity = self._from_row(cls, row)
                if isinstance(entity, Permission): self.permissions[entity.code] = entity
                elif isinstance(entity, Organization): self.organizations[entity.id] = entity
                elif isinstance(entity, Location): self.locations[entity.id] = entity
                elif isinstance(entity, UserProfile): self.users[entity.id] = entity
                elif isinstance(entity, OrganizationMembership): self.memberships[entity.id] = entity
                elif isinstance(entity, Role): self.roles[entity.id] = entity
                elif isinstance(entity, MembershipRole): self.membership_roles[entity.id] = entity
                elif isinstance(entity, IdentityLink): self.identity_links[entity.id] = entity
        for row in self._request("location_access"):
            membership = self.memberships.get(row.get("membership_id"))
            if membership and row.get("active", True):
                self.memberships[membership.id] = replace(
                    membership,
                    location_ids=frozenset((*membership.location_ids, row["location_id"])),
                )

    @staticmethod
    def _from_row(cls, row: dict[str, Any]):
        row = dict(row)
        if "tenant_id" not in row and "organization_id" in row:
            row["tenant_id"] = row["organization_id"]
        values = {key: value for key, value in row.items() if key in cls.__dataclass_fields__}
        if cls is Role: values["permission_codes"] = frozenset(values.pop("permission_codes", []))
        if cls is OrganizationMembership: values["location_ids"] = frozenset(values.pop("location_ids", []))
        for field in ("created_at", "updated_at", "occurred_at"):
            if field in values and isinstance(values[field], str): values[field] = datetime.fromisoformat(values[field].replace("Z", "+00:00"))
        return cls(**values)

    @staticmethod
    def _row(entity: Any, table: str | None = None) -> dict[str, Any]:
        row = asdict(entity)
        if isinstance(entity, Role): row["permission_codes"] = sorted(row["permission_codes"])
        if isinstance(entity, OrganizationMembership):
            if table == "memberships": row.pop("location_ids", None)
            else: row["location_ids"] = sorted(row["location_ids"])
        row.pop("created_at", None); row.pop("updated_at", None); row.pop("occurred_at", None)
        return row

    def _save(self, table: str, entity: Any, key: str = "id") -> None:
        self._request(table, "POST", query=f"?on_conflict={key}", body=self._row(entity, table), prefer="resolution=merge-duplicates,return=representation")

    def save_organization(self, entity): self.organizations[entity.id] = entity; self._save("tenants", entity)
    def save_location(self, entity): self.locations[entity.id] = entity; self._save("locations", entity)
    def save_user(self, entity): self.users[entity.id] = entity; self._save("user_profiles", entity)
    def save_membership(self, entity):
        self.memberships[entity.id] = entity
        self._save("memberships", entity)
        for location_id in entity.location_ids:
            self._save_location_access(entity.id, location_id)
    def save_permission(self, entity): self.permissions[entity.code] = entity; self._save("permissions", entity, "code")
    def save_role(self, entity): self.roles[entity.id] = entity; self._save("roles", entity)
    def save_membership_role(self, entity): self.membership_roles[entity.id] = entity; self._save("membership_roles", entity)
    def save_identity_link(self, entity): self.identity_links[entity.id] = entity; self._save("identity_links", entity, "tenant_id,person_id")

    def link_identity_atomic(self, entity):
        rows = self._request("rpc/link_identity", "POST", body={
            "p_tenant_id": entity.tenant_id, "p_person_id": entity.person_id,
            "p_user_id": entity.user_id,
        })
        row = rows[0] if isinstance(rows, list) and rows else None
        if row:
            result = self._from_row(IdentityLink, row)
            if result.user_id != entity.user_id:
                raise ConflictError("person is already linked to another identity")
            self.identity_links[result.id] = result
            return result
        return entity

    def unlink_identity_atomic(self, organization_id, person_id):
        rows = self._request("rpc/unlink_identity", "POST", body={
            "p_tenant_id": organization_id, "p_person_id": person_id,
        })
        row = rows[0] if isinstance(rows, list) and rows else None
        if not row:
            return None
        result = self._from_row(IdentityLink, row)
        self.identity_links.pop(result.id, None)
        return result

    def _save_location_access(self, membership_id: str, location_id: str) -> None:
        self._request(
            "location_access",
            "POST",
            query="?on_conflict=membership_id,location_id",
            body={"membership_id": membership_id, "location_id": location_id, "active": True},
            prefer="resolution=merge-duplicates,return=minimal",
        )

    def record_audit(self, event: AuditEvent) -> None:
        self._request("audit_events", "POST", body=self._row(event, "audit_events"), prefer="return=minimal")

    def get_organization(self, entity_id): return self.organizations.get(entity_id)
    def get_location(self, entity_id): return self.locations.get(entity_id)
    def get_user(self, entity_id): return self.users.get(entity_id)
    def get_membership(self, entity_id): return self.memberships.get(entity_id)
    def get_role(self, entity_id): return self.roles.get(entity_id)
    def get_identity_link(self, entity_id): return self.identity_links.get(entity_id)
    def all_locations(self): return self.locations.values()
    def all_memberships(self): return self.memberships.values()
    def all_roles(self): return self.roles.values()
    def all_membership_roles(self): return self.membership_roles.values()
    def all_identity_links(self): return self.identity_links.values()
    def all_permissions(self): return self.permissions.values()
