# Farmer Success Stories: trust, evidence, and moderation

## What the new feature does
- A signed-in farmer writes their starting point, approach, observed progress, and results. Photos before/after and a video (including optional camera recording) can be submitted.
- Media is stored in a private Supabase bucket; only the author/admins can retrieve pending media. Published media can be served with short-lived signed URLs.
- All submissions start `pending`. Admins (manually granted in Supabase, never self-assigned from browser UI) review them and may `published`, `verified`, or `rejected`.
- `published` means a real farmer account shared a story which was screened; **it does not mean the result was independently verified**.
- `verified` should be applied ONLY after the administrator checks the claimed evidence and permission to display it. This process is manual; NVIDIA must never automatically verify user-provided farm results.
- Names, media, and public contact details require informed consent. Contacts are optional and default to hidden. Do not expose precise farm coordinates, private addresses, or contacts of minors.

## Before using in a live presentation
1. Configure Supabase Google OAuth, deployed redirect URL, database tables and storage via `supabase/schema.sql` and `supabase/stories.sql`.
2. Add a trusted administrator's auth user UUID to `public.story_admins` **in Supabase SQL editor only**.
3. Test with two test user accounts and a separate admin. Confirm a farmer cannot self-approve or view pending submissions from someone else; confirm admin can review; confirm approved media opens using signed URLs.
4. Test file upload (JPEG and MP4/WebM); reject unsupported files, oversize files, and missing consent. Check microphone/camera access in HTTPS.
5. Ask volunteers for written consent before using videos and contacts in judges' demo. Do not fabricate farmer experiences or label prototypes as successful real farming deployments.
6. Add a clear consent withdrawal and removal process before a public launch. Ensure review coverage and data deletion requests.

## Evaluation criteria for real-world impact
- Farmer-reported outcomes should include a baseline and dates/seasons.
- Make claims bounded: farmer experiences don't prove that NASA data alone caused improvements.
- Record adverse outcomes and limitations, not just positive testimonials.
- Independent agricultural experts should review any agronomy claims.

## Trust principles
Differentiate **first-hand farmer report**, **admin-published report**, and **evidence-reviewed story**. Publication alone is not proof of crop suitability or guaranteed yield. The platform is not an official NASA service.
