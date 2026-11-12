# FieldShift AI — Cloudflare Pages deployment

1. Upload the repository contents to `SneijderRichDad/FieldShift` (the source ZIP contains the complete project).
2. In Supabase, create a project. Run `supabase/schema.sql`, then `supabase/stories.sql`, then `supabase/admin_and_activity.sql` in SQL Editor, in order. Review policies. Create a Google OAuth credential in Google Cloud and enable Supabase Auth → Providers → Google. Configure Supabase Auth → URL Configuration for the deployed `https://*.pages.dev` URL.
3. In Cloudflare dashboard → Workers & Pages → Create → Pages → Connect to Git, choose `SneijderRichDad/FieldShift`. Build command `npm run build`, output `dist`, root `/`.
4. Set **build-time** variables `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` (Supabase publishable/anon client key, not service role).
5. Set **runtime** Page Function variables `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` and **secret** values `NVIDIA_API_KEY`, `NVIDIA_MODEL`, and optionally `NVIDIA_VISION_MODEL`. These are stored in Cloudflare Pages Settings → Variables and Secrets; never commit secrets to GitHub. Deploy again after configuring.
6. Run manual tests using two Google accounts and one dedicated admin: OAuth redirect and logout; farm profile sync; one user creates post and second user sees it; reply realtime refresh; user notifications; admin lists accounts, temporarily restricts a test account and then restores it; farmer uploads a consented story and admin reviews it; NVIDIA assistant responds; NASA POWER data loads; mobile and screen-reader review.
7. Promote an administrator only through the Supabase SQL Editor after the admin's Google account first logs in: `insert into public.story_admins(user_id) values ('USER_UUID') on conflict do nothing;`. Never publish admin credentials or `service_role` keys. Recheck RLS policies before allowing real farmer data.

**Important:** Supabase data, NVIDIA AI, Cloudflare Pages deployment, Google OAuth and admin role assignment are NOT live until these user-authorized external setup steps are completed and tested. Code cannot create those accounts or secrets automatically.

Cloudflare Pages Functions auto-routes files under `functions/`; `functions/api/[[endpoint]].js` implements `/api/nasa-power`, `/api/market-news`, `/api/advisor`, and `/api/crop-scan` in the Workers environment. `/_redirects` adds SPA fallback. No Lovable dependency.

Never use fabricated farmers, real-time market prices, disease diagnoses, disaster predictions, or verified success claims during presentations. Use seeded content only when visibly marked `Demo`.

## Status update — 11 November 2026
The Supabase project **FieldShift AI** (`rrsubgyvjpiedbhlfwza`, Frankfurt) already exists, with the SQL migrations applied. **Do not repeat the SQL migration steps above on this project.** The new `My Farms` frontend includes public project connection defaults. Build variables remain recommended for explicit deployment control, but this release does not require them just to identify the public project. Google OAuth provider setup, NVIDIA runtime secrets, repository upload, and a Cloudflare Pages deployment are still pending. See `docs/SUPABASE_LIVE_CONNECTION.md`.
