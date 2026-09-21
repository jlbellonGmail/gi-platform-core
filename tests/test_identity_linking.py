import io
import json
from dataclasses import replace
from concurrent.futures import ThreadPoolExecutor
from wsgiref.util import setup_testing_defaults

import pytest

from gi_platform_core import CoreApi, CoreService, InMemoryCoreStore, create_app
from gi_platform_core.authorization import TenantContext
from gi_platform_core.errors import AuthorizationError, ConflictError, NotFoundError
from gi_platform_core.http import AuthenticatedActor


@pytest.fixture
def fixture():
    store = InMemoryCoreStore()
    service = CoreService(store)
    for code in {"organization:identity_link", "organization:identity_unlink"}:
        service.create_permission(code, code)
    org = service.create_organization("Tenant")
    actor = service.create_user("actor-sub", "Actor")
    target = service.create_user("target-sub", "Target")
    actor_membership = service.add_membership(actor.id, org.id)
    service.add_membership(target.id, org.id)
    role = service.create_role(org.id, "identity-admin", {"organization:identity_link", "organization:identity_unlink"})
    service.assign_role(actor_membership.id, role.id)
    return service, store, org, actor, target


def test_resolution_requires_exact_subject_and_active_membership(fixture):
    service, store, org, actor, target = fixture
    resolved = service.resolve_identity(org.id, target.id, "target-sub")
    assert resolved.id == target.id
    with pytest.raises(NotFoundError):
        service.resolve_identity(org.id, target.id, "wrong-sub")
    membership = next(m for m in store.memberships.values() if m.user_id == target.id)
    store.memberships[membership.id] = membership.__class__(membership.user_id, membership.organization_id, False, membership.location_ids, membership.id)
    with pytest.raises(NotFoundError):
        service.resolve_identity(org.id, target.id, "target-sub")


def test_link_does_not_create_membership_and_is_idempotent(fixture):
    service, store, org, actor, target = fixture
    before = len(store.memberships)
    first = service.link_identity(TenantContext(actor.id, org.id), "person-1", target.id, "target-sub")
    second = service.link_identity(TenantContext(actor.id, org.id), "person-1", target.id, "target-sub")
    assert first.id == second.id
    assert len(store.memberships) == before
    assert [item.action for item in store.audit_events if item.action.startswith("identity.")] == ["identity.resolved", "identity.linked", "identity.resolved", "identity.linked"]


def test_unlink_is_authorized_and_idempotent(fixture):
    service, _, org, actor, target = fixture
    service.link_identity(TenantContext(actor.id, org.id), "person-remove", target.id, "target-sub")
    assert service.unlink_identity(TenantContext(actor.id, org.id), "person-remove") is not None
    assert service.unlink_identity(TenantContext(actor.id, org.id), "person-remove") is None


def test_inactive_actor_organization_role_and_permission_are_denied(fixture):
    service, store, org, actor, target = fixture
    actor_record = store.users[actor.id]
    store.users[actor.id] = actor_record.__class__(actor_record.external_subject, actor_record.display_name, actor_record.id, False)
    with pytest.raises(AuthorizationError):
        service.link_identity(TenantContext(actor.id, org.id), "person-inactive", target.id, "target-sub")
    store.users[actor.id] = actor
    role = next(item for item in store.roles.values())
    store.roles[role.id] = replace(role, active=False)
    with pytest.raises(AuthorizationError):
        service.link_identity(TenantContext(actor.id, org.id), "person-inactive", target.id, "target-sub")
    store.roles[role.id] = role
    permission = store.permissions["organization:identity_link"]
    store.permissions[permission.code] = replace(permission, active=False)
    with pytest.raises(AuthorizationError):
        service.link_identity(TenantContext(actor.id, org.id), "person-inactive", target.id, "target-sub")
    store.permissions[permission.code] = permission
    store.organizations[org.id] = replace(org, active=False)
    with pytest.raises(AuthorizationError):
        service.link_identity(TenantContext(actor.id, org.id), "person-inactive", target.id, "target-sub")


def test_conflicting_target_and_cross_tenant_are_denied(fixture):
    service, store, org, actor, target = fixture
    same_org_user = service.create_user("same-org-sub", "Same Org")
    service.add_membership(same_org_user.id, org.id)
    other = service.create_organization("Other")
    other_user = service.create_user("other-sub", "Other")
    other_membership = service.add_membership(other_user.id, other.id)
    service.link_identity(TenantContext(actor.id, org.id), "person-1", target.id, "target-sub")
    with pytest.raises(ConflictError):
        service.link_identity(TenantContext(actor.id, org.id), "person-1", same_org_user.id, "same-org-sub")
    with pytest.raises(NotFoundError):
        service.resolve_identity(org.id, other_user.id, "other-sub")


def test_concurrent_same_link_has_one_identity(fixture):
    service, store, org, actor, target = fixture
    def link():
        return service.link_identity(TenantContext(actor.id, org.id), "person-concurrent", target.id, "target-sub").id
    with ThreadPoolExecutor(max_workers=8) as pool:
        ids = list(pool.map(lambda _: link(), range(8)))
    assert len(set(ids)) == 1
    assert len([item for item in store.identity_links.values() if item.person_id == "person-concurrent"]) == 1


def _request(app, method, path, payload=None, actor=None):
    body = json.dumps(payload or {}).encode()
    environ = {"REQUEST_METHOD": method, "PATH_INFO": path, "CONTENT_LENGTH": str(len(body)), "wsgi.input": io.BytesIO(body), "HTTP_AUTHORIZATION": "Bearer test"}
    setup_testing_defaults(environ)
    statuses = []
    response = b"".join(app(environ, lambda status, headers: statuses.append(status)))
    return int(statuses[0].split()[0]), json.loads(response)


def test_http_auth_authorization_errors_and_tenant_isolation(fixture):
    service, store, org, actor, target = fixture
    app = create_app(CoreApi(service), lambda headers: AuthenticatedActor(actor.id, org.id))
    status, _ = _request(app, "POST", f"/v1/organizations/{org.id}/identity-validation", {"user_id": target.id, "external_subject": "target-sub"})
    assert status == 200
    status, body = _request(app, "POST", f"/v1/organizations/{org.id}/identity-links", {"person_id": "person-http", "user_id": target.id, "external_subject": "target-sub"})
    assert status == 201 and body["contract_version"] == "0.2.0"
    other = service.create_organization("Other")
    status, body = _request(app, "POST", f"/v1/organizations/{other.id}/identity-validation", {"user_id": target.id, "external_subject": "target-sub"})
    assert status == 404 and body["error"]["code"] == "not_found"


def test_http_requires_authentication(fixture):
    service, _, org, _, _ = fixture
    app = create_app(CoreApi(service), lambda _: None)
    status, body = _request(app, "POST", f"/v1/organizations/{org.id}/identity-validation", {})
    assert status == 401 and body["error"]["code"] == "authentication_required"


def test_http_health_does_not_require_auth(fixture):
    service, _, _, _, _ = fixture
    app = create_app(CoreApi(service), lambda _: None)
    status, body = _request(app, "GET", "/healthz")
    assert status == 200 and body["status"] == "ok"
