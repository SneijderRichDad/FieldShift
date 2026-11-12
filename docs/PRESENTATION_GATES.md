# Presentation release gates

## Completed source-level checks
- JavaScript syntax passes for app.js and Vercel endpoints.
- Four crop-rotation scoring tests pass (`npm test`).
- Standalone interactive browser smoke test passed: all 10 inspected navigation pages, no uncaught page errors, community post, greenhouse form, rainfall slider, and safe disabled Google sign-in without credentials.
- Main navigation mapping contains the new modules.
- Sensitive NVIDIA key stays server side.
- Supabase SQL schema contains row-level security policies for profiles and community discussions.

## Not yet verified — required before a live demo
1. Create own Supabase project; run schema SQL; enable Google in OAuth providers.
2. Configure Supabase Google OAuth callback and Vercel Site URL / allowed redirects.
3. Deploy and test real OAuth with two distinct accounts, session persistence, sign-out, and reset for email-password users.
4. Test cloud posts/comments/profile update from two browsers; verify RLS rejects an unauthorized edit.
5. Set NVIDIA model/key securely in Vercel and test advisor responses, account access checks and error behavior.
6. Configure a compatible NVIDIA vision model and test actual sample crop photos; never call it a validated diagnosis.
7. Check NASA POWER API response and its dates, historical units, outage states, and district-center approximations.
8. Test Google News RSS fetch and ensure it is labeled news, not live verified market prices.
9. Run full Vite build and check desktop + smartphone navigation, search, all forms, photo file handling, accessibility.
10. Have Rwandan agricultural experts review the crop rotation assumptions and greenhouse advice.

**Execution limitation during this pass:** network package installation timed out and the local browser was blocked from localhost by the environment administrator. A standalone embedded browser smoke test succeeded, but the Vercel production build and end-to-end browser/OAuth checks are not claimed as completed.
