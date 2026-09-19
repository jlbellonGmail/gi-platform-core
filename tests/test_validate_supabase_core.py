import json

from scripts.validate_supabase_core import read_table


class Response:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self):
        return json.dumps([]).encode()


def test_location_access_validation_uses_composite_key(monkeypatch):
    requests = []

    def fake_urlopen(request, timeout):
        requests.append(request)
        return Response()

    monkeypatch.setattr("scripts.validate_supabase_core.urlopen", fake_urlopen)

    status, count, error = read_table("https://example.supabase.co", "key", "", "location_access")

    assert status == 200
    assert count == 0
    assert error is None
    assert "membership_id%2Clocation_id" in requests[0].full_url
    assert requests[0].get_header("Accept-profile") == "core"
