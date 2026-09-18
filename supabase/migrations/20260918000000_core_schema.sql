-- GI-PLATFORM-CORE v0.1.0.  This migration owns schema core only.
create schema if not exists core;

create table if not exists core.organizations (
  id uuid primary key default gen_random_uuid(),
  name text not null check (length(btrim(name)) > 0),
  active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create table if not exists core.sites (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references core.organizations(id) on delete cascade,
  name text not null check (length(btrim(name)) > 0),
  active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (organization_id, name)
);
create table if not exists core.user_profiles (
  id uuid primary key default gen_random_uuid(),
  external_subject text not null unique,
  display_name text not null check (length(btrim(display_name)) > 0),
  active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create table if not exists core.organization_memberships (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references core.user_profiles(id) on delete cascade,
  organization_id uuid not null references core.organizations(id) on delete cascade,
  active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (user_id, organization_id)
);
create table if not exists core.permissions (
  id uuid not null default gen_random_uuid(),
  code text primary key,
  description text not null,
  active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint permissions_code_format check (code ~ '^[^[:space:]:]+:[^[:space:]:]+$')
);
create table if not exists core.roles (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references core.organizations(id) on delete cascade,
  name text not null check (length(btrim(name)) > 0),
  permission_codes jsonb not null default '[]'::jsonb,
  active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (organization_id, name),
  check (jsonb_typeof(permission_codes) = 'array')
);
create table if not exists core.membership_roles (
  id uuid primary key default gen_random_uuid(),
  membership_id uuid not null references core.organization_memberships(id) on delete cascade,
  role_id uuid not null references core.roles(id) on delete cascade,
  created_at timestamptz not null default now(),
  unique (membership_id, role_id)
);
create table if not exists core.site_access (
  membership_id uuid not null references core.organization_memberships(id) on delete cascade,
  site_id uuid not null references core.sites(id) on delete cascade,
  active boolean not null default true,
  created_at timestamptz not null default now(),
  primary key (membership_id, site_id)
);
create table if not exists core.audit_events (
  id uuid primary key default gen_random_uuid(),
  action text not null check (length(btrim(action)) > 0),
  actor_user_id uuid references core.user_profiles(id) on delete set null,
  organization_id uuid references core.organizations(id) on delete set null,
  site_id uuid references core.sites(id) on delete set null,
  outcome text not null check (outcome in ('success', 'allowed', 'denied', 'failure')),
  metadata jsonb not null default '{}'::jsonb,
  occurred_at timestamptz not null default now()
);

create index if not exists sites_organization_idx on core.sites(organization_id);
create index if not exists memberships_user_org_idx on core.organization_memberships(user_id, organization_id);
create index if not exists roles_organization_idx on core.roles(organization_id);
create index if not exists membership_roles_membership_idx on core.membership_roles(membership_id);
create index if not exists site_access_site_idx on core.site_access(site_id);
create index if not exists audit_org_site_time_idx on core.audit_events(organization_id, site_id, occurred_at desc);

alter table core.organizations enable row level security;
alter table core.sites enable row level security;
alter table core.user_profiles enable row level security;
alter table core.organization_memberships enable row level security;
alter table core.roles enable row level security;
alter table core.permissions enable row level security;
alter table core.membership_roles enable row level security;
alter table core.site_access enable row level security;
alter table core.audit_events enable row level security;

drop policy if exists organizations_member_read on core.organizations;
create policy organizations_member_read on core.organizations for select to authenticated using (
  exists (select 1 from core.organization_memberships m join core.user_profiles u on u.id = m.user_id
          where m.organization_id = organizations.id and m.active and u.external_subject = auth.uid()::text and u.active)
);
drop policy if exists sites_member_read on core.sites;
create policy sites_member_read on core.sites for select to authenticated using (
  exists (select 1 from core.site_access a join core.organization_memberships m on m.id = a.membership_id
          join core.user_profiles u on u.id = m.user_id
          where a.site_id = sites.id and a.active and m.active and u.external_subject = auth.uid()::text and u.active)
);
drop policy if exists profiles_self_read on core.user_profiles;
create policy profiles_self_read on core.user_profiles for select to authenticated using (external_subject = auth.uid()::text);
drop policy if exists memberships_self_read on core.organization_memberships;
create policy memberships_self_read on core.organization_memberships for select to authenticated using (
  exists (select 1 from core.user_profiles u where u.id = organization_memberships.user_id and u.external_subject = auth.uid()::text)
);
drop policy if exists roles_member_read on core.roles;
create policy roles_member_read on core.roles for select to authenticated using (
  exists (select 1 from core.organization_memberships m join core.user_profiles u on u.id = m.user_id
          where m.organization_id = roles.organization_id and m.active and u.external_subject = auth.uid()::text)
);
drop policy if exists permissions_authenticated_read on core.permissions;
create policy permissions_authenticated_read on core.permissions for select to authenticated using (active);
drop policy if exists membership_roles_member_read on core.membership_roles;
create policy membership_roles_member_read on core.membership_roles for select to authenticated using (
  exists (select 1 from core.organization_memberships m join core.user_profiles u on u.id = m.user_id
          where m.id = membership_roles.membership_id and m.active and u.external_subject = auth.uid()::text)
);
drop policy if exists site_access_member_read on core.site_access;
create policy site_access_member_read on core.site_access for select to authenticated using (
  exists (select 1 from core.organization_memberships m join core.user_profiles u on u.id = m.user_id
          where m.id = site_access.membership_id and m.active and u.external_subject = auth.uid()::text)
);
drop policy if exists audit_actor_read on core.audit_events;
create policy audit_actor_read on core.audit_events for select to authenticated using (
  actor_user_id in (select u.id from core.user_profiles u where u.external_subject = auth.uid()::text)
);

grant usage on schema core to authenticated, service_role;
grant select on all tables in schema core to authenticated;
grant all on all tables in schema core to service_role;
