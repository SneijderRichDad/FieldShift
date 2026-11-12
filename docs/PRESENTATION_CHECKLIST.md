# Presentation readiness — IhingaLink AI

## Required external configuration

- [ ] Firebase project created by your team.
- [ ] Google sign-in provider enabled in Firebase Console.
- [ ] Vercel production domain added to Firebase Authentication **Authorized domains** (exact hostname, no scheme).
- [ ] All `VITE_FIREBASE_*` web app config values added to Vercel and deployment rebuilt.
- [ ] Cloud Firestore database created and `firestore.rules` applied.
- [ ] Test real Google login from a browser, and verify the signed-in account email and sign-out.
- [ ] Test second Google account and check sector posts show up across two devices.
- [ ] Verify the NASA POWER call using a deployed Vercel URL (local static serving does not execute the `/api/nasa-power` function).

## Demo script

1. Open the Vercel production URL and show the farmer overview.
2. Open My Farm Profile, select the real **Continue with Google** option, and choose a Google account.
3. Save the farm's district/sector/crops and refresh; verify persistence.
4. In a second logged-in browser account, make a sector community post; confirm the post is visible to the other account after refresh.
5. In Rotation Studio, change a farmer priority and explain the three illustrative strategies and their limitations.
6. Open NASA Climate, fetch historical data, and show the date/source. Do not claim predictions or field-level precision.
7. Open NASA Research and Market pages, highlighting sources and demo-only listings.

## Known limitations / not ready as production claims

- The crop-scoring demonstration has **not** been validated by agronomists.
- Market listings, initial posts and rule-based advisor are demonstration features; market records do not establish a real buyer network.
- Firebase remains external: no team-owned project configuration was supplied to this build session, so real OAuth login could **not** be executed or verified here.
- Browser testing in the task environment was blocked from accessing a local server. JS syntax checks and scoring unit tests passed, but cross-browser end-to-end flows remain unverified.
- Further Firestore real-time sync, comments, moderation and authentication security testing is required before deploying for real farmers.

**Never describe the platform as production-ready or the Google login as tested without completing the checkboxes above.**
