-- CORE03: rename the technical tenancy vocabulary without changing UUIDs or data.
-- This migration is additive to the published history and is safe to re-run.
do $$
begin
  if to_regclass('core.organizations') is not null
     and to_regclass('core.tenants') is null then
    alter table core.organizations rename to tenants;
  end if;
  if to_regclass('core.organization_memberships') is not null
     and to_regclass('core.memberships') is null then
    alter table core.organization_memberships rename to memberships;
  end if;
end $$;

-- Defensive bootstrap for installations where the v0.2 identity migration was
-- skipped. The normal order still applies 20260920000000 first.
create table if not exists core.identity_links (
  id uuid primary key default gen_random_uuid(),
  tenant_id uuid not null references core.tenants(id) on delete cascade,
  person_id text not null check (length(btrim(person_id)) > 0),
  user_id uuid not null references core.user_profiles(id) on delete cascade,
  active boolean not null default true,
  created_at timestamptz not null default now(),
  unique (tenant_id, person_id)
);
alter table core.identity_links enable row level security;
grant select, insert, update, delete on core.identity_links to service_role;

do $$
declare
  item record;
begin
  for item in select table_name from (values
    ('locations'), ('memberships'), ('roles'), ('audit_events'), ('identity_links')
  ) tables(table_name)
  loop
    if to_regclass('core.' || item.table_name) is not null
       and exists (select 1 from information_schema.columns
                   where table_schema = 'core' and table_name = item.table_name
                     and column_name = 'organization_id') then
      execute format('alter table core.%I rename column organization_id to tenant_id', item.table_name);
    end if;
  end loop;
end $$;

alter index if exists core.locations_organization_idx rename to locations_tenant_idx;
alter index if exists core.memberships_user_org_idx rename to memberships_user_tenant_idx;
alter index if exists core.roles_organization_idx rename to roles_tenant_idx;
alter index if exists core.audit_org_location_time_idx rename to audit_tenant_location_time_idx;
alter index if exists core.identity_links_user_org_idx rename to identity_links_user_tenant_idx;
create index if not exists identity_links_user_tenant_idx
  on core.identity_links(user_id, tenant_id);

-- Read-only aliases let older database readers transition without duplicating data.
create or replace view core.organizations as select * from core.tenants;
create or replace view core.organization_memberships as select * from core.memberships;

alter table core.tenants enable row level security;
alter table core.memberships enable row level security;
drop policy if exists organizations_member_read on core.tenants;
create policy tenants_member_read on core.tenants for select to authenticated using (
  exists (select 1 from core.memberships m join core.user_profiles u on u.id = m.user_id
          where m.tenant_id = tenants.id and m.active
            and u.external_subject = auth.uid()::text and u.active)
);
drop policy if exists memberships_self_read on core.memberships;
create policy memberships_self_read on core.memberships for select to authenticated using (
  exists (select 1 from core.user_profiles u
          where u.id = memberships.user_id and u.external_subject = auth.uid()::text)
);

-- Keep the atomic identity-link boundary tenant-scoped after the rename.
drop function if exists core.link_identity(uuid, text, uuid);
drop function if exists core.unlink_identity(uuid, text);
create or replace function core.link_identity(p_tenant_id uuid, p_person_id text, p_user_id uuid)
returns setof core.identity_links language plpgsql security definer set search_path = core, public as $$
begin
  perform pg_advisory_xact_lock(hashtextextended(p_tenant_id::text || ':' || p_person_id, 0));
  insert into core.identity_links(tenant_id, person_id, user_id)
  values (p_tenant_id, btrim(p_person_id), p_user_id)
  on conflict (tenant_id, person_id) do nothing;
  return query select * from core.identity_links
    where tenant_id = p_tenant_id and person_id = btrim(p_person_id) and active;
end $$;

create or replace function core.unlink_identity(p_tenant_id uuid, p_person_id text)
returns setof core.identity_links language sql security definer set search_path = core, public as $$
  delete from core.identity_links
   where tenant_id = p_tenant_id and person_id = btrim(p_person_id) returning *;
$$;
revoke all on function core.link_identity(uuid, text, uuid) from public, anon, authenticated;
revoke all on function core.unlink_identity(uuid, text) from public, anon, authenticated;
grant execute on function core.link_identity(uuid, text, uuid) to service_role;
grant execute on function core.unlink_identity(uuid, text) to service_role;
