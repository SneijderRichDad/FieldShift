-- Run using Supabase SQL Editor. Real accounts require configuring Google OAuth in Authentication settings.
create extension if not exists pgcrypto;
create table if not exists public.farmer_profiles (
 user_id uuid primary key references auth.users(id) on delete cascade,
 display_name text not null check(char_length(display_name) between 1 and 70),
 district text not null check(char_length(district)<80),
 sector text not null check(char_length(sector)<80),
 crops text not null default '',
 priority text not null default 'Soil health',
 updated_at timestamptz not null default now()
);
create table if not exists public.community_posts (
 id uuid primary key default gen_random_uuid(),
 author_id uuid not null references auth.users(id) on delete cascade,
 author_name text not null check(char_length(author_name) between 1 and 70),
 district text not null check(char_length(district)<80),
 sector text not null check(char_length(sector)<80),
 topic text not null default 'Community',
 body text not null check(char_length(body) between 4 and 2500),
 created_at timestamptz not null default now()
);
create table if not exists public.community_comments (
 id uuid primary key default gen_random_uuid(),
 post_id uuid not null references public.community_posts(id) on delete cascade,
 author_id uuid not null references auth.users(id) on delete cascade,
 author_name text not null check(char_length(author_name) between 1 and 70),
 body text not null check(char_length(body) between 1 and 800),
 created_at timestamptz not null default now()
);
create index if not exists community_posts_place_time on public.community_posts(district,sector,created_at desc);
create index if not exists community_comments_post on public.community_comments(post_id,created_at);
alter table public.farmer_profiles enable row level security;
alter table public.community_posts enable row level security;
alter table public.community_comments enable row level security;
create policy "Profiles owner read" on public.farmer_profiles for select to authenticated using (auth.uid()=user_id);
create policy "Profiles owner insert" on public.farmer_profiles for insert to authenticated with check (auth.uid()=user_id);
create policy "Profiles owner update" on public.farmer_profiles for update to authenticated using (auth.uid()=user_id) with check (auth.uid()=user_id);
create policy "Posts signed-in read" on public.community_posts for select to authenticated using (true);
create policy "Posts owner insert" on public.community_posts for insert to authenticated with check (auth.uid()=author_id);
create policy "Posts owner delete" on public.community_posts for delete to authenticated using (auth.uid()=author_id);
create policy "Comments signed-in read" on public.community_comments for select to authenticated using (true);
create policy "Comments owner insert" on public.community_comments for insert to authenticated with check (auth.uid()=author_id);
create policy "Comments owner delete" on public.community_comments for delete to authenticated using (auth.uid()=author_id);
-- For production: add rate limiting, reporting/moderation tables, abuse controls and verify displayed names using trusted profile records.
