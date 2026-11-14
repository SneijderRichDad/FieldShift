# FieldShift Marketplace — authentic farmer supply and buyer demand

FieldShift AI, Supabase project `rrsubgyvjpiedbhlfwza`.

## What is real
- Signed-in users can post **seller offers** or **buyer requests**. Both are stored in public.market_listings under the submitting user's auth ID.
- Only `available` entries can be viewed by other signed-in users; owners can access their own entries under RLS.
- Market filters show genuine signed-in user listings only, without seeded fake buyers.
- Market inquiries use public.market_inquiries; only the sender and the listing owner can read messages. Never include private credentials in an inquiry.
- Rwanda provides all **30 districts** in UI selectors; the full map list is grounded in Government of Rwanda local government directory (https://www.gov.rw/government/directory/local-government).
- The country switcher supports Rwanda, Uganda, Kenya, Tanzania, Burundi and DR Congo as marketplace browsing/posting contexts. **It does not provide verified regional soil or climate support for these other countries**.
- Three external marketplaces are linked for optional discovery: eHaho, Agrimobile and eHingiriSoko. Their listings are independent and are *not* automatically included in the FieldShift matching results.

## Before demonstrating
1. Confirm Google OAuth works on the deployed domain.
2. Sign in with two different accounts; create a seller offer and buyer request in the same district/country.
3. Verify both appear in Marketplace and show the correct listing type.
4. Send an inquiry and read it from the listing-owner inbox.
5. Sign out: no personal account data or inquiry messages should remain visible.
6. Verify the business RLS policies, market moderation and contact safety before inviting real users.

## Database setup
Migration is already applied to live project. Keep SQL file in repository for recovery or new environments. Do not rerun blindly.

## Important honesty
No buyer records were invented or scraped; listings depend on actual registrations. Public marketplace listings are not transaction, quality or identity guarantees. External third-party listings belong to their providers.
