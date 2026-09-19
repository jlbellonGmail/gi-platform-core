-- Rename the generic tenancy scope to the product term locations.
alter table if exists core.sites rename to locations;
alter table if exists core.site_access rename to location_access;
alter table if exists core.location_access rename column site_id to location_id;
alter table if exists core.audit_events rename column site_id to location_id;

alter index if exists core.sites_organization_idx rename to locations_organization_idx;
alter index if exists core.site_access_site_idx rename to location_access_location_idx;
alter index if exists core.audit_org_site_time_idx rename to audit_org_location_time_idx;

drop policy if exists sites_member_read on core.locations;
drop policy if exists locations_member_read on core.locations;
create policy locations_member_read on core.locations for select to authenticated using (
  exists (select 1 from core.location_access a
          join core.organization_memberships m on m.id = a.membership_id
          join core.user_profiles u on u.id = m.user_id
          where a.location_id = locations.id and a.active and m.active
            and u.external_subject = auth.uid()::text and u.active)
);

drop policy if exists site_access_member_read on core.location_access;
drop policy if exists location_access_member_read on core.location_access;
create policy location_access_member_read on core.location_access for select to authenticated using (
  exists (select 1 from core.organization_memberships m
          join core.user_profiles u on u.id = m.user_id
          where m.id = location_access.membership_id and m.active
            and u.external_subject = auth.uid()::text)
);
