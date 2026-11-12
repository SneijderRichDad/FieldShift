-- Apply AFTER schema.sql and stories.sql. Run in Supabase SQL editor as project owner.
-- The app never receives a service-role key or privileged auth.users grants.
create table if not exists public.user_restrictions (
 user_id uuid primary key references auth.users(id) on delete cascade,
 restricted boolean not null default false,
 reason text not null default '',
 updated_at timestamptz not null default now(),
 updated_by uuid references auth.users(id)
);
alter table public.user_restrictions enable row level security;
create policy "Users see own restriction" on public.user_restrictions for select to authenticated using (user_id=auth.uid());
-- No client writes to restrictions; RPC exclusively.

create table if not exists public.farm_activity (
 id bigint generated always as identity primary key,
 user_id uuid not null references auth.users(id) on delete cascade,
 event_type text not null check (length(event_type) between 2 and 50),
 summary text not null check (length(summary) between 1 and 180),
 created_at timestamptz not null default now()
);
alter table public.farm_activity enable row level security;
create policy "Farmers read own activity" on public.farm_activity for select to authenticated using(user_id=auth.uid());
create policy "Farmers write own activity" on public.farm_activity for insert to authenticated with check(user_id=auth.uid() and not exists(select 1 from public.user_restrictions r where r.user_id=auth.uid() and r.restricted));
create index if not exists farm_activity_user_time on public.farm_activity(user_id,created_at desc);

create table if not exists public.farm_notifications (
 id uuid primary key default gen_random_uuid(),
 user_id uuid not null references auth.users(id) on delete cascade,
 title text not null check(length(title) between 1 and 110),
 body text not null check(length(body) between 1 and 500),
 is_read boolean not null default false,
 created_at timestamptz not null default now()
);
alter table public.farm_notifications enable row level security;
create policy "Farmers see own notifications" on public.farm_notifications for select to authenticated using(user_id=auth.uid());
create policy "Farmers mark own read" on public.farm_notifications for update to authenticated using(user_id=auth.uid()) with check(user_id=auth.uid());
create index if not exists farm_notifications_user_time on public.farm_notifications(user_id,created_at desc);

-- Owner grants admin role explicitly in SQL Editor, NEVER from an unauthenticated browser:
-- insert into public.story_admins(user_id) values ('TRUSTED_AUTH_USER_UUID') on conflict do nothing;
-- Privileged administrator overview; admins must pass server-checked role.
create or replace function public.admin_user_overview()
returns table(user_id uuid, email text, joined_at timestamptz, last_sign_in timestamptz, display_name text, district text, sector text, is_admin boolean, is_restricted boolean, posts bigint)
language plpgsql security definer set search_path = '' as $$
begin
 if not public.is_story_admin() then raise exception 'Not authorized' using errcode='42501'; end if;
 return query
 select u.id,u.email::text,u.created_at,u.last_sign_in_at,
 p.display_name,p.district,p.sector,(a.user_id is not null),coalesce(r.restricted,false),
 (select count(*) from public.community_posts x where x.author_id=u.id)
 from auth.users u left join public.farmer_profiles p on p.user_id=u.id
 left join public.story_admins a on a.user_id=u.id
 left join public.user_restrictions r on r.user_id=u.id
 order by u.created_at desc limit 250;
end $$;
revoke all on function public.admin_user_overview() from public,anon;
grant execute on function public.admin_user_overview() to authenticated;

create or replace function public.admin_set_restriction(target_user uuid, should_restrict boolean, explanation text default '')
returns boolean language plpgsql security definer set search_path = '' as $$
begin
 if not public.is_story_admin() then raise exception 'Not authorized' using errcode='42501'; end if;
 if target_user=auth.uid() then raise exception 'Cannot restrict your own administrator account'; end if;
 if exists(select 1 from public.story_admins where user_id=target_user) then raise exception 'Remove admin role through secure project owner process first'; end if;
 if not exists(select 1 from auth.users where id=target_user) then raise exception 'Unknown account'; end if;
 insert into public.user_restrictions(user_id,restricted,reason,updated_at,updated_by)
 values(target_user,should_restrict,left(coalesce(explanation,''),300),now(),auth.uid())
 on conflict (user_id) do update set restricted=excluded.restricted,reason=excluded.reason,updated_at=now(),updated_by=auth.uid();
 return true;
end $$;
revoke all on function public.admin_set_restriction(uuid,boolean,text) from public,anon;
grant execute on function public.admin_set_restriction(uuid,boolean,text) to authenticated;

create or replace function public.admin_remove_community_post(target_post uuid)
returns boolean language plpgsql security definer set search_path = '' as $$
begin
 if not public.is_story_admin() then raise exception 'Not authorized' using errcode='42501'; end if;
 delete from public.community_posts where id=target_post;
 return found;
end $$;
revoke all on function public.admin_remove_community_post(uuid) from public,anon;
grant execute on function public.admin_remove_community_post(uuid) to authenticated;

-- These checks are database-enforced even if a restricted client bypasses UI controls.
alter policy "Posts owner insert" on public.community_posts
 with check(auth.uid()=author_id and not exists(select 1 from public.user_restrictions r where r.user_id=auth.uid() and r.restricted));
alter policy "Comments owner insert" on public.community_comments
 with check(auth.uid()=author_id and not exists(select 1 from public.user_restrictions r where r.user_id=auth.uid() and r.restricted));
alter policy "Signed-in farmers may submit pending stories" on public.farmer_stories
 with check(author_id=auth.uid() and review_status='pending' and reviewer_id is null and reviewed_at is null and review_note is null
 and not exists(select 1 from public.user_restrictions r where r.user_id=auth.uid() and r.restricted)
 and ((contact_type='none' and contact_value is null and not contact_consent) or (contact_type<>'none' and contact_value is not null and contact_consent))
 and (media_path is null or media_path like auth.uid()::text || '/%')
 and (before_media_path is null or before_media_path like auth.uid()::text || '/%')
 and (after_media_path is null or after_media_path like auth.uid()::text || '/%'));

-- Supabase Realtime database subscriptions: add required tables to publication once.
do $$ begin
 alter publication supabase_realtime add table public.community_posts,public.community_comments,public.farm_notifications;
exception when duplicate_object then null;
end $$;
