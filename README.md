> **Release status (14 November 2026):** New farmer marketplace features are built into the attached source and the Supabase production schema has been upgraded. This archive has passed 26 Node automated tests and JavaScript syntax checks. A fresh local Vite build was unavailable here because npm dependencies were not installed; run `npm install && npm run build && npm test` in GitHub Codespaces before deploying. The **live Cloudflare site is still on the earlier version until you deploy this release**.

# IhingaLink AI — Better harvests, together 🇷🇼

Rwanda-first agricultural collaboration and crop-rotation planning **prototype** prepared for NASA Space Apps Challenge: **Field Shift — Adapting Farms with NASA Data**.

## Quick start

1. Place the extracted files in your GitHub repository (`SneijderRichDad/FieldShift` if you are using the existing project).
2. In GitHub Codespaces or a local Node.js environment, run `npm install` then `npm run dev`.
3. Use port 5173 for local development; run `npm run build` for a Cloudflare Pages deployment.
4. Copy `.env.example` to `.env.local` and configure services as detailed below.
5. On Cloudflare Pages: import GitHub `SneijderRichDad/FieldShift`, build command `npm run build`, output directory `dist`. See `docs/CLOUDFLARE_DEPLOYMENT.md`.

## Prototype pages

- Overview: refreshed Rwanda-first homepage, crop metrics and farmer discussions.
- My Farms: real Supabase-backed private farm registration, crop season records, and saved rotation plans for authenticated farmers.
- Farmer Community: by district/sector with posts, replies, likes, search, local examples and optional Supabase cloud storage.
- Rotation Studio: compares three illustrative rotations by water, soil and diversity weights (not scientifically calibrated).
- Climate Intelligence: request NASA POWER historical temperature and rainfall data; source dates labeled; failure never fills invented readings.
- Farm Explorer: interactive OpenStreetMap location context for **all 30** Rwanda districts (approximate reference markers), not measured field polygons/NDVI.
- NASA Research: curated dated science/research links.
- Local Marketplace: authenticated real seller offers and buyer requests in Supabase; country, district, crop and type filters; private inquiry inbox; links to independent local marketplaces, optional latest public Google News RSS headlines (not verified commodity prices).
- AI Farm Advisor: rule-based fallback and optional authenticated NVIDIA NIM server API.
- Climate Simulator: what-if rainfall/temperature sliders (scenarios are **not forecasts**).
- Greenhouse Planner: season, crop, water considerations (not calibrated agronomic schedules).
- Crop Photo Review: local preview; optional authenticated NVIDIA vision review (may suggest possibilities, **not diagnosis**).
- Help & Security: real Supabase password reset when configured, privacy/security guidance.
- About IhingaLink: localized identity, mission; cofounder bios not invented.
- My Farm & Account: editable farm profile and real Google OAuth when Supabase is configured.
- English/Kinyarwanda: language-switch scaffold, Kinyarwanda overview wording and voice recognition attempt (full translation remains incomplete).

## Real Google authentication (Supabase recommended)

1. A [Supabase](https://supabase.com/) project is already active in SneijderRichDad's organization. See `docs/SUPABASE_LIVE_CONNECTION.md`. Never paste secrets into a chat or commit them to GitHub.
2. In Supabase **Authentication → Providers → Google**, enable Google and configure a Google Cloud web OAuth Client ID and Client Secret. Set the authorized redirect URI to the callback URL displayed by Supabase.
3. In Supabase **Authentication → URL Configuration**, set the Site URL to your final Cloudflare Pages hostname and add approved preview/localhost redirect URLs.
4. The SQL migrations were already applied in the live project. Do not execute them again. Review policies with your team before opening access to farmers.
5. Set `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` (public anon key, **never service role key**) in Cloudflare Pages build environment variables, and redeploy.
6. Test sign-in and sign-out in the deployed browser using a real Google account. Confirm page refresh preserves the session, one user cannot modify another user's records, and community posts appear for a second user.
7. Enable Auth email password flow separately in Supabase if you want password reset to apply to email accounts. For Google-only users password management stays with Google.

**No secret credentials are included.** Browser publishable keys are set at build-time; server secrets are not included. Firebase compatibility code is retained from the earlier prototype but Supabase is the intended backend when configured.

## NVIDIA AI assistant and optional crop-photo review

Set `NVIDIA_API_KEY` and `NVIDIA_MODEL` as **server-only** Cloudflare Pages Function secret values; never expose the API key with a `VITE_` prefix. `api/advisor.js` verifies the user's Supabase access token before calling NVIDIA NIM. For photo review, configure an appropriate NVIDIA vision-capable chat model as `NVIDIA_VISION_MODEL`, then review model/image support and pricing. Both endpoints return clear errors if unavailable. There is no claim of training, validation, or expert-level crop diagnosis.

## Market and NASA science integrity

NASA POWER observations are historical **gridded estimates**, not field measurements or current emergency warnings. NASA research articles are not alerts. Public news headlines are not market prices. A verified commodity-price API or authorized data-sharing agreement is necessary for real price figures. The simulator is qualitative; it does not provide calibrated crop yields.

## Testing and limitations

Run `npm test`; source syntax checks: `node --check app.js`, `node --check api/*.js` individually. The initial tests target the rotation scoring helper. A production build / browser walkthrough requires installed dependencies and a reachable browser-based development environment. See `docs/FEATURE_AUDIT.md` and `docs/PRESENTATION_GATES.md` for what remains unverified.

## Security and privacy

- No secret/service role keys in the repository or browser.
- Supabase RLS policies restrict profile updates and posts to their owners; all authenticated users can see shared community posts. Do not post exact field addresses publicly.
- Field notes and social content are user-generated, not agronomist-certified.
- Before serving real farmers, add moderation/reporting, abuse prevention, accessibility/translation reviews, terms/privacy policy, and local agricultural validation.

## Third-party sources

NASA POWER API: https://power.larc.nasa.gov/docs/services/api/temporal/daily/  
NASA Harvest: https://www.nasaharvest.org/news  
Supabase Auth: https://supabase.com/docs/guides/auth/social-sign-in/auth-google  
NVIDIA API: https://docs.api.nvidia.com/nim/reference/llm-apis  
Rwandan market service: https://ehingirisoko.digital/


## Trust-building Farmer Success Stories (new)

The **Farmer Success Stories** page now allows signed-in farmers to submit actual experiences, a starting situation, seasonal progress, observed results and optional JPEG/PNG/WebP photos or MP4/WebM/MOV videos. There is also a short in-browser video recording tool when supported by the browser and HTTPS permissions. Submissions are **pending** by default and will not be displayed as successes until an admin reviews them.

**Supabase setup:** run `supabase/schema.sql` and `supabase/stories.sql` in the SQL editor (in that order). Stories use private `farmer-story-media` Storage (25 MB limit) and RLS policies; media is delivered with short-lived signed URLs. Google OAuth needs its provider and deployment redirect URL configured. An admin role must be added **manually** in the Supabase SQL editor for a known `auth.users.id` with:

```
insert into public.story_admins(user_id) values ('VERIFIED_AUTH_USER_UUID');
```

Only those users will see **Story Review Admin**, where they may publish (unverified farmer report), mark evidence reviewed (only after external checking), or reject. Ordinary accounts cannot add themselves as admin. Only consented contact details are shown publicly. No invented farmer outcomes or fabricated media are supplied. Reviews do not imply guaranteed agricultural results. Written media permissions, moderation, user deletion requests, and privacy impact review are required before public launch. Do not include minors' contact details without appropriate guardian consent.

**NVIDIA:** existing `/api/advisor` and `/api/crop-scan` proxy a supported NVIDIA NIM model. Add `NVIDIA_API_KEY` and relevant model names to Vercel's **server-only** environment; this is not a code-generation or automatic quality-assurance service. The first live API request cannot be tested until credentials are provisioned. Reference: https://docs.api.nvidia.com/nim/reference/llm-apis

**Known limitation:** This release provides UI workflows and access-policy SQL but does not claim to have verified the hosted Supabase database, OAuth login, real media upload, NVIDIA inference, or full production deployment. Run browser tests with configured services before presenting them as live.


## Additional functionality (Cloudflare release)

- Cloudflare Pages Function handlers in `functions/api/[[endpoint]].js` serve NVIDIA AI, NVIDIA vision, NASA climate, and public market news.
- Authenticated farmer account activity and notifications have RLS-protected tables; admins see an access-controlled overview and can restrict posting or remove abusive community posts.
- Live Supabase PostgreSQL subscriptions for community posts, comments, and private notifications when Realtime is configured.
- Install database migrations in order: `supabase/schema.sql`, `supabase/stories.sql`, `supabase/admin_and_activity.sql`. These are not auto-installed.
- Source code does **not** include Supabase project credentials, NVIDIA API keys, or a fake Google login.
- `npm test` runs offline unit and simulated routing checks. `npm run build` requires installed node dependencies.

## Live database integration update — 11 Nov 2026

The working Supabase backend now exists. See `docs/SUPABASE_LIVE_CONNECTION.md` for its project URL, configuration, applied migrations, remaining Google OAuth steps, and testing gates. The refreshed dashboard and **My Farms** page are included in the standalone HTML preview, but the preview itself is intentionally offline (no fake auth).

### Connected-design release
The default **public** Supabase URL and publishable key are now included in `app.js` so Vite builds can use the active project immediately. **Never** commit a service-role key. This does not activate Google OAuth, which still needs a provider credential and allowed hosting domain in Supabase Authentication.

## Marketplace upgrade — 14 Nov 2026

- Complete official Rwanda district list (30 districts). Sector names remain user-entered rather than pretending incomplete static lists are exhaustive.
- Country selector: Rwanda, Uganda, Kenya, Tanzania, Burundi and DR Congo. This extends marketplace browsing and publishing context; it **does not** certify farm-climate support outside Rwanda.
- Real authenticated buyer requests and farmer seller offers are held in Supabase. No scraped or invented buyers.
- Private inquiry messaging between logged-in users; only participants can view each message by RLS.
- Independent real marketplaces linked: eHaho, Agrimobile and eHingiriSoko; their content is not integrated as a live FieldShift feed.

### Deploy from Codespaces

```bash
# Upload this release ZIP to the root of your Codespace and then:
unzip -o FieldShift_AI_Marketplace_30_Districts_Release.zip
npm install
npm run build
npm test
git add app.js styles.css README.md tests/marketplace.test.js supabase/005_live_market_buyers.sql docs/MARKETPLACE_LIVE_2026_11_14.md
git commit -m "Add Rwanda districts, country switcher and live buyer marketplace"
git push origin main
npx wrangler pages deploy dist --project-name=fieldshift-pages --branch=main
```

**Already applied:** live Supabase schema modifications for `listing_type`, `country`, `currency`, `price_amount` and `market_inquiries`. Do not blindly rerun migration files on production.

**IMPORTANT:** The public site needs a fresh deployment of this source. Google OAuth and live tests using actual registered farmer accounts remain to be verified.
