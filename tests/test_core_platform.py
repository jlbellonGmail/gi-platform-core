import pytest

from gi_platform_core import CoreApi, CoreService, InMemoryCoreStore
from gi_platform_core.authorization import TenantContext
from gi_platform_core.errors import AuthorizationError, IsolationError


@pytest.fixture
def core():
    store = InMemoryCoreStore()
    service = CoreService(store)
    for code in {"organization:read", "site:read", "organization:admin"}:
        service.create_permission(code, code)
    return service, store


def setup_org(service, name, user_subject):
    org = service.create_organization(name)
    site_a = service.create_site(org.id, f"{name} A")
    user = service.create_user(user_subject, user_subject)
    membership = service.add_membership(user.id, org.id)
    role = service.create_role(org.id, "administrator", {"organization:read", "site:read", "organization:admin"})
    service.assign_role(membership.id, role.id)
    service.grant_site_access(membership.id, site_a.id)
    return org, site_a, user, membership


def test_organization_has_multiple_sites_and_public_api_is_consumable(core):
    service, _ = core
    org = service.create_organization("Acme")
    first = service.create_site(org.id, "North")
    second = service.create_site(org.id, "South")
    assert {site.id for site in service.store.sites.values() if site.organization_id == org.id} == {first.id, second.id}
    api = CoreApi(service)
    assert api.create_organization("Another")["contract_version"] == "0.1.0"


def test_user_can_belong_to_multiple_organizations(core):
    service, _ = core
    first, _, user, _, = setup_org(service, "First", "same-user")
    second = service.create_organization("Second")
    membership = service.add_membership(user.id, second.id)
    assert {m.organization_id for m in service.store.memberships.values() if m.user_id == user.id} == {first.id, second.id}
    assert membership.organization_id == second.id


def test_authorization_requires_membership_role_and_site_context(core):
    service, _ = core
    org, site, user, _ = setup_org(service, "Tenant", "authorized")
    assert service.authorize(TenantContext(user.id, org.id), "organization:read").allowed
    assert service.authorize(TenantContext(user.id, org.id, site.id), "site:read").allowed
    assert not service.authorize(TenantContext(user.id, org.id, site.id), "unknown:action").allowed


def test_no_cross_organization_access(core):
    service, _ = core
    first, site, user, first_membership = setup_org(service, "First", "user-a")
    second, _, _, _ = setup_org(service, "Second", "user-b")
    decision = service.authorize(TenantContext(user.id, second.id), "organization:read")
    assert not decision.allowed
    with pytest.raises(IsolationError):
        service.grant_site_access(first_membership.id, next(site_id for site_id, value in service.store.sites.items() if value.organization_id == second.id))


def test_site_access_is_scoped_and_does_not_leak_to_other_site(core):
    service, _ = core
    org = service.create_organization("Scoped")
    allowed_site = service.create_site(org.id, "Allowed")
    denied_site = service.create_site(org.id, "Denied")
    user = service.create_user("scoped", "Scoped")
    membership = service.add_membership(user.id, org.id)
    role = service.create_role(org.id, "reader", {"site:read"})
    service.assign_role(membership.id, role.id)
    service.grant_site_access(membership.id, allowed_site.id)
    assert service.authorize(TenantContext(user.id, org.id, allowed_site.id), "site:read").allowed
    assert not service.authorize(TenantContext(user.id, org.id, denied_site.id), "site:read").allowed
    assert [site.id for site in service.list_sites(TenantContext(user.id, org.id))] == [allowed_site.id]


def test_relevant_operations_are_audited_and_inactive_membership_denied(core):
    service, store = core
    org, site, user, membership = setup_org(service, "Audited", "audited")
    store.memberships[membership.id] = membership.__class__(membership.user_id, membership.organization_id, False, membership.site_ids, membership.id)
    assert not service.authorize(TenantContext(user.id, org.id, site.id), "site:read").allowed
    actions = {event.action for event in store.audit_events}
    assert {"organization.created", "site.created", "membership.created", "authorization.checked"} <= actions


def test_api_contract_contains_context_without_exposing_store_details(core):
    service, _ = core
    org = service.create_organization("API")
    user = service.create_user("api-user", "API User")
    response = CoreApi(service).authorize(user.id, org.id, "site:read")
    assert response["contract_version"] == "0.1.0"
    assert response["allowed"] is False
    assert "permissions" not in response


def test_public_contract_covers_membership_roles_and_site_operations(core):
    service, _ = core
    api = CoreApi(service)
    organization = api.create_organization('Contract')
    site = api.create_site(organization['id'], 'Main')
    user = api.create_user('contract-user', 'Contract User')
    membership = api.add_membership(user['id'], organization['id'])
    role = api.create_role(organization['id'], 'reader', {'site:read'})
    api.assign_role(membership['id'], role['id'])
    api.grant_site_access(membership['id'], site['id'])
    sites = api.list_sites(user['id'], organization['id'], site['id'])
    assert sites[0]['id'] == site['id']
    assert api.list_memberships(user['id'])[0]['organization_id'] == organization['id']
