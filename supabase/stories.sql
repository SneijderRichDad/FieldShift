-- Run AFTER schema.sql in Supabase SQL Editor. Apply once; review policies before production.
-- All credentials and privileged operations remain server-side / in the Supabase console.
create table if not exists public.story_admins (
  user_id uuid primary key references auth.users(id) on delete cascade,
  created_at timestamptz not null default now()
);
alter table public.story_admins enable row level security;
create policy "Admins read own role" on public.story_admins for select to authenticated using (auth.uid() = user_id);
-- IMPORTANT: no client INSERT/UPDATE/DELETE policy for story_admins.
-- Workspace owner inserts admins manually in SQL Editor AFTER confirming the auth.users user ID:
-- insert into public.story_admins(user_id) values ('YOUR-TRUSTED-USER-UUID');
create or replace function public.is_story_admin()
returns boolean language sql stable security definer set search_path=public
as $$ select exists(select 1 from public.story_admins where user_id=auth.uid()) $$;
revoke all on function public.is_story_admin() from public;
grant execute on function public.is_story_admin() to authenticated, anon;

create table if not exists public.farmer_stories (
 id uuid primary key default gen_random_uuid(),
 author_id uuid not null references auth.users(id) on delete cascade,
 author_display text not null check(length(author_display) between 1 and 70),
 district text not null check(length(district) between 1 and 80),
 sector text not null check(length(sector) between 1 and 80),
 title text not null check(length(title) between 8 and 100),
 starting_point text not null check(length(starting_point) between 20 and 2000),
 progress text not null check(length(progress) between 20 and 2000),
 results text not null check(length(results) between 20 and 2000),
 media_path text,
 before_media_path text,
 after_media_path text,
 media_kind text not null default 'none' check(media_kind in ('none','image','video')),
 contact_type text not null default 'none' check(contact_type in ('none','email','phone')),
 contact_value text,
 contact_consent boolean not null default false,
 consent_at timestamptz not null,
 review_status text not null default 'pending' check(review_status in ('pending','published','verified','rejected')),
 reviewer_id uuid references auth.users(id),
 reviewed_at timestamptz,
 review_note text,
 created_at timestamptz not null default now()
);
create index if not exists farmer_stories_status_date on public.farmer_stories(review_status,created_at desc);
alter table public.farmer_stories enable row level security;
-- Database-level defense: approved public view only exposes data suitable for public sharing.
-- The interface uses this view, not the private moderation table, to avoid leaking review notes or unconsented contacts.
create or replace view public.published_farmer_stories with (security_invoker = true) as
select id,author_display,district,sector,title,starting_point,progress,results,
 media_path,before_media_path,after_media_path,media_kind,created_at,review_status, contact_consent,
 case when contact_consent then contact_type else 'none' end as contact_type,
 case when contact_consent then contact_value else null end as contact_value
from public.farmer_stories where review_status in ('published','verified');

grant select on public.published_farmer_stories to anon,authenticated;
create policy "Approved stories are public" on public.farmer_stories for select to anon, authenticated using (review_status in ('published','verified'));
create policy "Authors can see own submissions" on public.farmer_stories for select to authenticated using (author_id=auth.uid());
create policy "Admins can see all stories" on public.farmer_stories for select to authenticated using (public.is_story_admin());
create policy "Signed-in farmers may submit pending stories" on public.farmer_stories for insert to authenticated
 with check(author_id=auth.uid() and review_status='pending' and reviewer_id is null and reviewed_at is null and review_note is null
 and ((contact_type='none' and contact_value is null and not contact_consent) or (contact_type<>'none' and contact_value is not null and contact_consent))
 and (media_path is null or media_path like auth.uid()::text || '/%')
 and (before_media_path is null or before_media_path like auth.uid()::text || '/%')
 and (after_media_path is null or after_media_path like auth.uid()::text || '/%'));
-- No author UPDATE policy. Admin only may change moderation status. Auth cannot insert into admins.
create policy "Only admins can moderate" on public.farmer_stories for update to authenticated
 using(public.is_story_admin()) with check(public.is_story_admin());
-- Reviewer change should be limited to review columns via a separate RPC in production.

insert into storage.buckets(id,name,public,file_size_limit,allowed_mime_types)
values('farmer-story-media','farmer-story-media',false,26214400,
  array['image/jpeg','image/png','image/webp','video/mp4','video/webm','video/quicktime'])
on conflict (id) do update set public=false,file_size_limit=26214400,
allowed_mime_types=excluded.allowed_mime_types;
create policy "Authors upload to own story folder" on storage.objects for insert to authenticated
 with check(bucket_id='farmer-story-media' and (storage.foldername(name))[1]=auth.uid()::text);
create policy "Authors and admins access story uploads" on storage.objects for select to authenticated
 using(bucket_id='farmer-story-media' and ((storage.foldername(name))[1]=auth.uid()::text or public.is_story_admin()));
create policy "Published story media readable for signing" on storage.objects for select to anon,authenticated
 using(bucket_id='farmer-story-media' and exists (
 select 1 from public.farmer_stories s where (s.media_path=storage.objects.name or s.before_media_path=storage.objects.name or s.after_media_path=storage.objects.name)
 and s.review_status in ('published','verified')));
-- Keep deletion to privileged maintenance (do not add broad anonymous/public delete policies).
