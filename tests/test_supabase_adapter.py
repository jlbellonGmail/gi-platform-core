import json
from types import SimpleNamespace
from unittest.mock import patch

from gi_platform_core import CoreService, SupabaseCoreStore


class FakeResponse:
    def __init__(self, payload=None):
        self.payload = json.dumps(payload or []).encode()

    def __enter__(self): return self
    def __exit__(self, *_): return False
    def read(self): return self.payload


def test_supabase_store_uses_host_configuration_and_core_profile_headers():
    requests = []

    def fake_urlopen(request, timeout):
        requests.append((request, timeout))
        return FakeResponse([])

    with patch('gi_platform_core.supabase_adapter.urlopen', fake_urlopen):
        store = SupabaseCoreStore('https://example.supabase.co/', 'server-key')
        CoreService(store).create_organization('Acme')

    assert len(requests) == 10  # 7 entity refreshes + site access refresh + organization + audit
    assert all(request.headers['Accept-profile'] == 'core' for request, _ in requests)
    assert all(request.headers['Authorization'] == 'Bearer server-key' for request, _ in requests)
    assert requests[-2][0].method == 'POST'
    assert requests[-2][0].full_url.endswith('/rest/v1/organizations?on_conflict=id')


def test_supabase_adapter_decodes_role_and_site_access_shapes():
    from gi_platform_core.domain import OrganizationMembership, Role

    role = SupabaseCoreStore._from_row(Role, {
        'id': 'r', 'organization_id': 'o', 'name': 'reader',
        'permission_codes': ['location:read'], 'active': True,
    })
    membership = SupabaseCoreStore._from_row(OrganizationMembership, {
        'id': 'm', 'user_id': 'u', 'organization_id': 'o',
        'active': True, 'location_ids': ['s'],
    })
    assert role.permission_codes == frozenset({'location:read'})
    assert membership.location_ids == frozenset({'s'})


def test_supabase_store_persists_site_access_in_its_own_table():
    requests = []

    def fake_urlopen(request, timeout):
        requests.append(request)
        return FakeResponse([])

    with patch('gi_platform_core.supabase_adapter.urlopen', fake_urlopen):
        store = SupabaseCoreStore('https://example.supabase.co', 'server-key')
        service = CoreService(store)
        organization = service.create_organization('Acme')
        site = service.create_location(organization.id, 'North')
        user = service.create_user('subject', 'User')
        membership = service.add_membership(user.id, organization.id)
        service.grant_location_access(membership.id, site.id)

    location_access_posts = [request for request in requests if '/rest/v1/location_access?' in request.full_url]
    assert len(location_access_posts) == 1
    body = json.loads(location_access_posts[0].data.decode())
    assert body == {'membership_id': membership.id, 'location_id': site.id, 'active': True}
    membership_posts = [request for request in requests if '/rest/v1/organization_memberships?' in request.full_url]
    assert 'location_ids' not in json.loads(membership_posts[-1].data.decode())
