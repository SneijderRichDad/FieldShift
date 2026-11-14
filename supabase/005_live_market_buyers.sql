-- Applied to FieldShift AI production database on 2026-11-14.
-- Buyer demand and farmer offers use the same authenticated RLS-protected table.
alter table public.market_listings
  add column if not exists listing_type text not null default 'seller'
  check (listing_type in ('seller','buyer')),
  add column if not exists country text not null default 'Rwanda'
  check (country in ('Rwanda','Uganda','Kenya','Tanzania','Burundi','DR Congo')),
  add column if not exists currency text not null default 'RWF'
  check (currency in ('RWF','UGX','KES','TZS','BIF','CDF','USD'));
alter table public.market_listings add column if not exists price_amount numeric(14,2) check(price_amount>=0);
update public.market_listings set price_amount=asking_price_rwf where price_amount is null and asking_price_rwf is not null;
create index if not exists market_listings_discovery_idx on public.market_listings(country,listing_type,status,created_at desc);
create table if not exists public.market_inquiries (
 id uuid primary key default gen_random_uuid(),
 listing_id uuid not null references public.market_listings(id) on delete cascade,
 sender_id uuid not null references auth.users(id) on delete cascade,
 message text not null check(length(trim(message)) between 10 and 800),
 created_at timestamptz not null default now(),
 unique(listing_id,sender_id,message)
);
create index if not exists market_inquiries_listing_idx on public.market_inquiries(listing_id,created_at desc);
create index if not exists market_inquiries_sender_idx on public.market_inquiries(sender_id);
alter table public.market_inquiries enable row level security;
create policy "inquiries_participant_read" on public.market_inquiries for select to authenticated
using (sender_id=(select auth.uid()) or exists
 (select 1 from public.market_listings m where m.id=listing_id and m.user_id=(select auth.uid())));
create policy "inquiries_sender_insert" on public.market_inquiries for insert to authenticated
with check (sender_id=(select auth.uid()) and exists
 (select 1 from public.market_listings m where m.id=listing_id and m.status='available' and m.user_id<>(select auth.uid())));
grant select,insert on public.market_inquiries to authenticated;
