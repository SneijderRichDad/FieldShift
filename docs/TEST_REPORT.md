# Test report — 9 November 2026

- `node --check app.js`: PASS.
- `node --test tests/*.test.js`: PASS (4/4 crop scoring tests).
- Static review: pages include overview, community, rotation, climate, explorer, NASA research, market, advisor and profile.
- Google OAuth: Firebase SDK uses real `signInWithPopup` and `GoogleAuthProvider`; no mock Google identity. **Not end-to-end tested** because Firebase project identifiers and authorized domain have not been supplied.
- Browser automation: attempted Playwright/Chromium against local development server; browser was blocked by environment policy (`net::ERR_BLOCKED_BY_ADMINISTRATOR`). End-to-end navigation tests were therefore **inconclusive**, not passed.
- Vercel serverless NASA POWER API exists and validates dates/coordinates. Live API availability has not been independently verified from the app UI.
- Production build: `npm install` failed due to runtime network restrictions, so production Vite bundling remains unverified in this environment.

## Release blockers

1. Deploy to Vercel and test build, routing, NASA POWER and responsive UI.
2. Configure Firebase Authentication/Firestore, whitelist Vercel domain and test Google login with two accounts.
3. Audit Firestore rules and community posting/visibility before real-user onboarding.
4. Obtain written validation of crop rotation scores from a Rwandan agriculture expert.
