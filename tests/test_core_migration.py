from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "supabase" / "migrations" / "20260918000000_core_schema.sql"

TABLES = {
    "organizations",
    "locations",
    "user_profiles",
    "organization_memberships",
    "permissions",
    "roles",
    "membership_roles",
    "location_access",
    "audit_events",
}


def test_core_migration_declares_all_tables_with_rls_and_read_policies():
    sql = MIGRATION.read_text(encoding="utf-8")

    for table in TABLES:
        assert f"create table if not exists core.{table}" in sql
        assert f"alter table core.{table} enable row level security" in sql
    assert "grant usage on schema core to anon, authenticated, service_role" in sql
    assert "grant select on all tables in schema core to anon" in sql
    assert "grant select on all tables in schema core to authenticated" in sql
    assert "grant all on all tables in schema core to service_role" in sql


def test_core_migration_keeps_location_access_normalized():
    sql = MIGRATION.read_text(encoding="utf-8")

    assert "create table if not exists core.location_access" in sql
    assert "primary key (membership_id, location_id)" in sql
    assert "location_ids" not in sql
