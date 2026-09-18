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

    assert len(requests) == 9  # 7 deterministic refreshes + organization + audit
    assert all(request.headers['Accept-profile'] == 'core' for request, _ in requests)
    assert all(request.headers['Authorization'] == 'Bearer server-key' for request, _ in requests)
    assert requests[-2][0].method == 'POST'
    assert requests[-2][0].full_url.endswith('/rest/v1/organizations?on_conflict=id')


def test_supabase_adapter_decodes_role_and_site_access_shapes():
    from gi_platform_core.domain import OrganizationMembership, Role

    role = SupabaseCoreStore._from_row(Role, {
        'id': 'r', 'organization_id': 'o', 'name': 'reader',
        'permission_codes': ['site:read'], 'active': True,
    })
    membership = SupabaseCoreStore._from_row(OrganizationMembership, {
        'id': 'm', 'user_id': 'u', 'organization_id': 'o',
        'active': True, 'site_ids': ['s'],
    })
    assert role.permission_codes == frozenset({'site:read'})
    assert membership.site_ids == frozenset({'s'})
