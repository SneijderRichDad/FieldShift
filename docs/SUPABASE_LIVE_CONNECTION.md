# FieldShift AI — Supabase live connection and authentication

## Actual project (created 11 Nov 2026)

- Project: **FieldShift AI**
- Organization: **SneijderRichDad's Org**
- Region: `eu-central-1` (Frankfurt)
- Project ID: `rrsubgyvjpiedbhlfwza`
- Public API base URL: `https://rrsubgyvjpiedbhlfwza.supabase.co`
- Dashboard: https://supabase.com/dashboard/project/rrsubgyvjpiedbhlfwza
- Database: **14 public tables**, all with row-level security; **two private storage buckets**.
- Existing migrations are **already applied to this live project**. **Do not run the SQL files again.** The SQL sources are retained in this package for reference and fresh projects.

## Connect the website

1. On Cloudflare Pages (or in local Codespaces), set the **build-time** environment variables `VITE_SUPABASE_URL=https://rrsubgyvjpiedbhlfwza.supabase.co` and `VITE_SUPABASE_ANON_KEY=<publishable key from Supabase Dashboard → Settings → API Keys>`.
2. Rebuild the website (`npm run build`). The public publishable key is intended for browser-side use, but **never** use a Supabase `service_role` key there.
3. Enable **Google** at Supabase Dashboard → Authentication → Providers, supplying a Google Cloud OAuth Web client ID and secret in Supabase only. Use the precise Supabase callback URL in Google Cloud's redirect allowlist.
4. Add the published `https://YOUR-SITE.pages.dev` URL to Supabase Authentication → URL Configuration. Enable only controlled domains and origins. Add localhost during development.
5. Test with two distinct farmer accounts and verify cross-account access controls and real-time comments.
6. To make the first admin, have the admin sign in once, identify their `auth.users.id` in the Supabase dashboard, then grant membership using a privileged SQL editor only; do not let users self-assign roles.
7. NVIDIA NIM API key and models belong in **Cloudflare runtime secrets**, not browser variables or GitHub.

## What is configured now

`farmer_profiles`, `farms`, `crop_seasons`, `rotation_plans`, `community_posts`, `community_comments`, `market_listings`, `community_reports`, `farm_notifications`, `farm_activity`, `farmer_stories`, `published_stories_data`, `story_admins`, and `user_restrictions`.

Supabase Realtime publication contains `community_posts`, `community_comments`, and `farm_notifications`. Media buckets `farm-images` and `farmer-story-media` are private. The public story view reads an approved snapshot, not private drafts.

**Not yet live-tested:** Google OAuth provider, an actual Google sign-in, farmer-owned inserts under a live session, Cloudflare deployment, NVIDIA NIM calls, and end-to-end media uploads. The code and database are prepared; connecting the login provider and deployment are required before demonstrating actual authenticated operations.

## Existing security warning

Four authenticated-callable `SECURITY DEFINER` admin functions remain flagged by Supabase Security Advisor. Those functions do internal admin checks; review them further before inviting external farmer accounts. The security advisor flagged no elevated-permission public view after hardening.

### Browser defaults included in this release

The application now includes the new project's **public Supabase URL and browser publishable key** as defaults, so a normally built frontend contacts the correct FieldShift backend without copying private credentials. These are explicitly public browser identifiers, **not** database passwords or service-role keys. You can override both using `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` at build time. Google OAuth must still be enabled and the deployed origin allowed in Supabase before sign-in succeeds.
