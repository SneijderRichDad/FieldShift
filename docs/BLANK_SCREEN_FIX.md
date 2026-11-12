# White screen: fixed offline preview

The earlier `FieldShift_AI_Offline_Preview.html` placed `export function scoreRotation` inside a classic inline `<script>`. The browser stops parsing the script with `SyntaxError: Unexpected token export`, leaving the app root empty.

The corrected `OFFLINE_DEMO.html` removes `export` for its self-contained inline script. It also does not attempt Supabase/Firebase initialization while running locally. This file is an offline **demonstration only**. Login, live community updates, NVIDIA and API calls require normal hosting plus credentials.

For the full application, deploy the Vite project (not the offline HTML). Cloudflare Pages: build `npm run build`, output `dist`, with the required environment variables and Supabase configuration.

Validated locally using `node --check`, a VM render smoke test, and `npm test` (23/23 passing). Automated Chromium file browsing is restricted in this runtime, so an actual Microsoft Edge click-through still needs verification.
