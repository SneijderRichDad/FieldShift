-- Reproducible reference for the active FieldShift AI project.
-- This schema was already applied to rrsubgyvjpiedbhlfwza on 2026-11-11.
-- DO NOT rerun on the current project; this file is for a new project or review.
create table public.farms (
 id uuid primary key default gen_random_uuid(),
 user_id uuid not null references auth.users(id) on delete cascade,
 farm_name text not null check(length(trim(farm_name)) between 2 and 100),
 district text not null check(length(district) between 1 and 80),
 sector text not null check(length(sector) between 1 and 80),
 area_hectares numeric(10,3) check(area_hectares > 0 and area_hectares < 100000),
 soil_type text, irrigation_type text,water_availability text,
 latitude double precision check(latitude between -90 and 90),
 longitude double precision check(longitude between -180 and 180),
 created_at timestamptz not null default now(),
 updated_at timestamptz not null default now(), unique(id,user_id)
);
create index farms_user_idx on public.farms(user_id);
alter table public.farms enable row level security;
create policy "farms_owner_select" on public.farms for select to authenticated using(user_id=(select auth.uid()));
create policy "farms_owner_insert" on public.farms for insert to authenticated with check(user_id=(select auth.uid()));
create policy "farms_owner_update" on public.farms for update to authenticated using(user_id=(select auth.uid())) with check(user_id=(select auth.uid()));
create policy "farms_owner_delete" on public.farms for delete to authenticated using(user_id=(select auth.uid()));
create table public.crop_seasons (
 id uuid primary key default gen_random_uuid(),farm_id uuid not null,
 user_id uuid not null references auth.users(id) on delete cascade,
 crop_name text not null check(length(trim(crop_name)) between 2 and 100),
 season_label text not null check(length(trim(season_label)) between 1 and 60),
 planting_date date,estimated_harvest_date date,actual_harvest_date date,
 field_notes text check(length(field_notes) <= 3000),
 area_hectares numeric(10,3) check(area_hectares > 0 and area_hectares < 100000),
 created_at timestamptz not null default now(),
 foreign key(farm_id,user_id) references public.farms(id,user_id) on delete cascade,
 check(estimated_harvest_date is null or planting_date is null or estimated_harvest_date >= planting_date)
);
create index seasons_farm_date_idx on public.crop_seasons(farm_id,planting_date desc);
create index seasons_user_idx on public.crop_seasons(user_id);
alter table public.crop_seasons enable row level security;
create policy "seasons_owner_select" on public.crop_seasons for select to authenticated using(user_id=(select auth.uid()));
create policy "seasons_owner_insert" on public.crop_seasons for insert to authenticated with check(user_id=(select auth.uid()));
create policy "seasons_owner_update" on public.crop_seasons for update to authenticated using(user_id=(select auth.uid())) with check(user_id=(select auth.uid()));
create policy "seasons_owner_delete" on public.crop_seasons for delete to authenticated using(user_id=(select auth.uid()));
create table public.rotation_plans (
 id uuid primary key default gen_random_uuid(),farm_id uuid not null,
 user_id uuid not null references auth.users(id) on delete cascade,
 plan_name text not null check(length(trim(plan_name)) between 2 and 100),
 planned_crops jsonb not null default '[]'::jsonb check(jsonb_typeof(planned_crops)='array'),
 farmer_priority text,evidence_summary text,is_shared boolean not null default false,
 created_at timestamptz not null default now(),
 foreign key(farm_id,user_id) references public.farms(id,user_id) on delete cascade
);
create index rotation_plans_farm_idx on public.rotation_plans(farm_id,created_at desc);
alter table public.rotation_plans enable row level security;
create policy "rotation_owner_or_shared_read" on public.rotation_plans for select to authenticated using(user_id=(select auth.uid()) or is_shared);
create policy "rotation_owner_insert" on public.rotation_plans for insert to authenticated with check(user_id=(select auth.uid()));
create policy "rotation_owner_update" on public.rotation_plans for update to authenticated using(user_id=(select auth.uid())) with check(user_id=(select auth.uid()));
create policy "rotation_owner_delete" on public.rotation_plans for delete to authenticated using(user_id=(select auth.uid()));
create table public.market_listings (
 id uuid primary key default gen_random_uuid(),user_id uuid not null references auth.users(id) on delete cascade,
 crop_name text not null check(length(trim(crop_name)) between 2 and 100),
 quantity numeric(12,2) check(quantity>0),unit text check(length(unit)<=30),
 asking_price_rwf numeric(14,2) check(asking_price_rwf>=0),
 district text not null check(length(district) between 1 and 80),
 sector text not null check(length(sector) between 1 and 80),
 details text check(length(details)<=1500),status text not null default 'available'
 check(status in('available','reserved','sold','closed')),
 created_at timestamptz not null default now(),updated_at timestamptz not null default now()
);
create index market_listings_location_idx on public.market_listings(district,sector,status,created_at desc);
create index market_listings_owner_idx on public.market_listings(user_id);
alter table public.market_listings enable row level security;
create policy "market_read_available_or_owned" on public.market_listings for select to authenticated using(status='available' or user_id=(select auth.uid()));
create policy "market_insert_owned" on public.market_listings for insert to authenticated with check(user_id=(select auth.uid()));
create policy "market_update_owned" on public.market_listings for update to authenticated using(user_id=(select auth.uid())) with check(user_id=(select auth.uid()));
create policy "market_delete_owned" on public.market_listings for delete to authenticated using(user_id=(select auth.uid()));
create table public.community_reports (
 id uuid primary key default gen_random_uuid(),post_id uuid not null references public.community_posts(id) on delete cascade,
 reporter_id uuid not null references auth.users(id) on delete cascade,
 reason text not null check(length(reason) between 5 and 500),
 created_at timestamptz not null default now(),unique(post_id,reporter_id)
);
create index reports_created_idx on public.community_reports(created_at desc);
alter table public.community_reports enable row level security;
create policy "reporter_insert" on public.community_reports for insert to authenticated with check(reporter_id=(select auth.uid()));
create policy "reporter_or_admin_read" on public.community_reports for select to authenticated using(reporter_id=(select auth.uid()) or public.is_story_admin());
insert into storage.buckets(id,name,public,file_size_limit,allowed_mime_types)
values('farm-images','farm-images',false,10485760,array['image/jpeg','image/png','image/webp'])
on conflict(id) do update set public=false,file_size_limit=10485760,allowed_mime_types=excluded.allowed_mime_types;
create policy "Farm image owner upload" on storage.objects for insert to authenticated
 with check(bucket_id='farm-images' and (storage.foldername(name))[1]=(select auth.uid())::text);
create policy "Farm image owner read" on storage.objects for select to authenticated
 using(bucket_id='farm-images' and (storage.foldername(name))[1]=(select auth.uid())::text);
create policy "Farm image owner remove" on storage.objects for delete to authenticated
 using(bucket_id='farm-images' and (storage.foldername(name))[1]=(select auth.uid())::text);
grant usage on schema public to authenticated;
grant select,insert,update,delete on public.farms,public.crop_seasons,public.rotation_plans,public.market_listings to authenticated;
grant select,insert on public.community_reports to authenticated;
