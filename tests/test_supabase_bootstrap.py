from scripts.bootstrap_validate_supabase import expected_host


def test_gi_dev_target_requires_exact_project_host():
    assert expected_host("https://abc123.supabase.co", "abc123")
    assert not expected_host("https://abc123.supabase.co", "other-project")
    assert not expected_host("http://abc123.supabase.co", "abc123")
    assert not expected_host("https://abc123.supabase.co.evil.example", "abc123")
