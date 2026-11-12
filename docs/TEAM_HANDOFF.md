# FieldShift / IhingaLink AI — Team handoff

## What is included

- Rwanda-focused agriculture website: home, local sector community feed, illustrative rotation comparison, climate explorer, farmer profiles, marketplace demo, story submissions, greenhouse planning, and photo-review interface.
- Supabase integration for Google OAuth, profile records, community posts/comments and realtime updates, private notifications, activity history and consented story media storage.
- Administrator dashboard guarded by a database role: overview of accounts, restrict/unrestrict posting, remove abusive posts, review farmer success evidence. Administrator grants themselves require secure Supabase owner action, never browser self-promotion.
- Cloudflare Pages server API handlers using server-side NVIDIA keys, authenticated assistant, optional vision review, and public NASA POWER data. These integrations are coded, not yet activated.

## Not yet proven live

No Supabase/NVIDIA/Cloudflare credentials are connected; no real OAuth or cloud upload has been completed; no public site has been deployed. The GitHub connector returned 403 on commits. The app's demo records and crop rotation scores are illustrative, not expert-approved farm prescriptions.

## Team workflow

1. Repository owner: authorize GitHub connector Contents: read/write access to `SneijderRichDad/FieldShift` OR upload the source archive in GitHub's web interface.
2. Database lead: create a team-owned Supabase project, apply SQL migrations in order, enable Google OAuth and confirm RLS restrictions with two test accounts.
3. Infrastructure lead: configure Cloudflare Pages from the GitHub repo and set build variables and runtime secrets, test `/api/nasa-power`.
4. AI lead: create NVIDIA NIM API credentials and identify a supported text model and optionally a vision model. Store secrets only in Cloudflare, never in GitHub.
5. Quality lead: run `npm test` and `npm run build`, then test flows on the deployed HTTPS URL, including accessibility and mobile views.
6. Content lead: review farming guidance with agronomists and obtain farmer consent before stories and videos are public.

## Security notes

- `VITE_SUPABASE_ANON_KEY` is a publishable client identifier, not a privileged service-role key. Never place the Supabase service role, NVIDIA key or Google OAuth client secret in `VITE_` variables or JavaScript.
- Private farmer coordinates and unpublished contact/media stay private, and no fake success stories are added.
- Farmer account restrictions disable posting and stories; they are not global authentication bans. Full account deletion and permission grants require a trusted project owner using the Supabase Dashboard.
- Do not present Google News headlines as verified real-time harvest prices. NASA POWER is historical gridded data and should not be described as an individual field sensor or emergency warning system.

## Presentation requirements

Have at least two test farmer accounts, one admin account, dated NASA POWER data, real posted discussion visible between accounts, one consented story moved through admin review, one NVIDIA response (with evidence), and verified browser access before stating the platform is fully operational.
