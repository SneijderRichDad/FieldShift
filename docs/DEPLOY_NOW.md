# Deploy FieldShift AI on Cloudflare Pages — handoff

## 0. Verified state

- Source: this package, not Lovable.
- Supabase: `rrsubgyvjpiedbhlfwza` (Frankfurt), real database with 14 secured public tables.
- GitHub: `https://github.com/SneijderRichDad/FieldShift` exists. ChatGPT's GitHub connector cannot write to it (GitHub API 403). The app files MUST be uploaded by the account owner or the connector permissions repaired.
- Tests: `npm test` passed 23/23 in the packaging environment. `node --check app.js` and `node --check functions/api/[[endpoint]].js` passed.
- `npm install` timed out in the packaging environment; **production compilation is not independently verified**.
- Public site, OAuth, NVIDIA API and two-person farmer workflow have **not** been verified.

## 1. Upload source to the existing GitHub repository

1. Extract the ZIP on your computer. Open `https://github.com/SneijderRichDad/FieldShift`.
2. From the `main` branch choose **Add file > Upload files**.
3. Upload all extracted project files/folders (including `functions/`, `public/`, `api/`, `supabase/`, `docs/`, `.env.example`, `app.js`, `index.html`, `styles.css`, `package.json`, `wrangler.toml`). Do not upload real `.env.local` files or API keys.
4. Commit with message `Deploy FieldShift AI web app with Supabase integration`.
5. Check repository Code tab now contains `package.json`, `app.js`, `index.html` and `functions/api/[[endpoint]].js`, in addition to your existing `LICENSE`.

You may alternatively create a new repository named `fieldshift-ai` but must still upload the files to it. The connected ChatGPT GitHub tool cannot create repositories or commit with its current authorization.

## 2. Connect Cloudflare Pages to GitHub

1. In Cloudflare go to **Workers & Pages > Create > Pages > Connect to Git**.
2. Authorize Cloudflare's GitHub app for `SneijderRichDad/FieldShift` and select branch `main`.
3. Use **Vite**. Root directory `/` (repository root); build command `npm run build`; output directory `dist`.
4. In project **Settings > Variables and Secrets**, define in **production and preview** environments:
   - `VITE_SUPABASE_URL` = `https://rrsubgyvjpiedbhlfwza.supabase.co`
   - `VITE_SUPABASE_ANON_KEY` = the publishable key from Supabase > Project Settings > API Keys (public client key, **not** `service_role`).
   - `NVIDIA_API_KEY` = secret from NVIDIA Build (server only). Do not prefix it with `VITE_`.
   - `NVIDIA_MODEL` = an actual NVIDIA model identifier supported by your account (server only).
   - Optionally `NVIDIA_VISION_MODEL` for crop photo review (server only).
5. Deploy. Open the exact `https://<your-generated-project-name>.pages.dev` URL shown by Cloudflare. The Pages Functions API routes are under `/api/`.

If the Cloudflare build fails, open **Deployments > Build log**, copy the first error, and fix it before announcing the app as live. Do not add the URL to Google OAuth until it exists.

## 3. Enable real Google login

1. Open `https://supabase.com/dashboard/project/rrsubgyvjpiedbhlfwza/auth/providers` > **Google**.
2. In Google Cloud Console, create an OAuth client of type **Web application** (configure consent screen first if needed).
3. Add **Authorized redirect URI** (this is the Google → Supabase callback, not the Pages URL):
   `https://rrsubgyvjpiedbhlfwza.supabase.co/auth/v1/callback`
4. Enter the Google OAuth Client ID and Client Secret into Supabase's Google provider settings. Never put the secret in the frontend or GitHub.
5. Open `https://supabase.com/dashboard/project/rrsubgyvjpiedbhlfwza/auth/url-configuration`, set **Site URL** to your actual Cloudflare Pages production URL and add that URL under **Redirect URLs**.
6. Go to the deployed Pages site, select **Continue with Google**, log in with a test Google account, confirm redirect to the app, sign out, and sign in again.

## 4. Live farmer workflow tests

Use TWO test Google accounts that you control.

1. Farmer A signs in, creates a farm and growing season, refreshes, and confirms data persists.
2. Farmer A saves a crop-rotation plan. Farmer B does NOT see private farm details.
3. Farmer A posts in a selected sector. Farmer B signs in, views the discussion, posts a reply. Confirm Farmer A sees the new reply (Realtime).
4. Farmer A creates a market listing. Farmer B views the available listing.
5. Test an anonymous visitor cannot view personal notifications or admin controls.
6. Upload test image / story. Grant an admin account using project owner's secure SQL editor **after their first sign-in**, then review the story; verify it is public only after approval.
7. Ask the NVIDIA advisor a question and confirm a real model reply. If 503, confirm NVIDIA credentials/model and Pages runtime variables.
8. Test the app on mobile. Review Cloudflare Functions invocation errors and Supabase Auth logs if needed.

## Important

The SQL scripts in `supabase/` are for reference. Do NOT reapply them to this existing project: the migrations were already executed. Never publish actual farmer data or claim disease detection/market prices are verified without external validation.
