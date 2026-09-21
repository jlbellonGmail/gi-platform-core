-- CoreApi v0.2.0 identity links. person_id is opaque to Core.
create table if not exists core.identity_links (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references core.organizations(id) on delete cascade,
  person_id text not null check (length(btrim(person_id)) > 0),
  user_id uuid not null references core.user_profiles(id) on delete cascade,
  active boolean not null default true,
  created_at timestamptz not null default now(),
  unique (organization_id, person_id)
);
create index if not exists identity_links_user_org_idx on core.identity_links(user_id, organization_id);
alter table core.identity_links enable row level security;
grant select, insert, update, delete on core.identity_links to service_role;

-- These functions are the atomic port used by SupabaseCoreStore. They are
-- executable only by service_role; authorization and membership validation
-- remain in CoreService and the host authentication boundary.
create or replace function core.link_identity(p_organization_id uuid, p_person_id text, p_user_id uuid)
returns setof core.identity_links language plpgsql security definer set search_path = core, public as $$
begin
  perform pg_advisory_xact_lock(hashtextextended(p_organization_id::text || ':' || p_person_id, 0));
  insert into core.identity_links(organization_id, person_id, user_id)
  values (p_organization_id, btrim(p_person_id), p_user_id)
  on conflict (organization_id, person_id) do nothing;
  return query select * from core.identity_links where organization_id = p_organization_id and person_id = btrim(p_person_id) and active;
end $$;
create or replace function core.unlink_identity(p_organization_id uuid, p_person_id text)
returns setof core.identity_links language sql security definer set search_path = core, public as $$
  delete from core.identity_links where organization_id = p_organization_id and person_id = btrim(p_person_id) returning *;
$$;
revoke all on function core.link_identity(uuid, text, uuid) from public, anon, authenticated;
revoke all on function core.unlink_identity(uuid, text) from public, anon, authenticated;
grant execute on function core.link_identity(uuid, text, uuid) to service_role;
grant execute on function core.unlink_identity(uuid, text) to service_role;
