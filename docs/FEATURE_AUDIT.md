# IhingaLink AI feature audit — 10 Nov 2026

**Definitions:** Built = source code exists and syntax/logic checks passed; Demo = local or illustrative data; Config needed = requires external account and credentials; Missing = no true production implementation. Full deployed-browser verification is NOT complete.

| Requested feature | Current implementation | Status / gap |
|---|---|---|
| Rwanda-focused homepage | Hero and localized farming community overview | Built; design not user-tested |
| Farmer account / farm management | District/sector/crops/priority editable, browser storage; Supabase profile table | Built, cloud requires setup; multi-farm management missing |
| Google login and password help | Supabase OAuth sign-in and sign-out, reset email | Config needed + real deployed sign-in test |
| Farmer community communication | Same-sector/district feed, posts, replies, sample content; Supabase persistence scaffold | Built; proper production moderation, privacy, real-time updates missing |
| Crop rotation AI | 3 explainable pre-defined rotations with adjustable heuristic weights | Demo, not agronomic AI optimization or locally validated recommendations |
| NASA climate dashboard | NASA POWER historical data fetching via Vercel function | Built code; live API and page validation not confirmed here |
| Interactive farm map | OpenStreetMap location embed for six selected districts | Limited demo; field boundary/NDVI overlays missing |
| Climate simulation laboratory | Rain and heat scenario sliders | Built qualitative demo, not a calibrated climate or yield model |
| AI assistant (NVIDIA) | Authenticated server-side NVIDIA NIM chat endpoint; local fallback | Config needed; no full expert validation |
| Crop image scanner | Preview and optional NVIDIA vision analysis | Config needed; no trained/validated disease diagnostic model |
| Greenhouse planning | Crops, season and water-choice guidance | Built educational demo, not validated greenhouse scheduling |
| Marketplace | Filtered demo buyer/seller postings, external Rwanda market link | Demo; no real enrollment/verified live prices |
| Google News / market headlines | Public Google News RSS server endpoint on demand | Built code; fetch not proven in this environment |
| Search districts and crops | Search community and marketplace text | Built basic filter; full geosearch not implemented |
| Kinyarwanda / English | Language toggle, limited translated headline + voice language selection | Partial; full site translation missing |
| Voice recognition | Web Speech API for advisor query, where browser supports it | Built best-effort; Kinyarwanda browser support unverified |
| NASA latest news / evidence | Dated NASA and NASA Harvest sources | Curated references; not a live NASA alert channel |
| About us / founders | Mission page, placeholder for unconfirmed names | Built page; biographies require approved names |
| Help/security | OAuth/error guidance, password email flow and privacy notes | Built page; no support ticket backend |
| Hosting / Codespaces | Vite package, devcontainer, Vercel routes and serverless APIs | Source ready; deployment not completed |
| GitHub repository / commit | Repo name planned: `ihingalink-ai` | NOT created; account connector currently shows no accessible repositories |
| Google Drive delivery | Local source ZIP generated | NOT uploaded to requested account; connected Drive has a different email |

## Important comparisons

**OneSoil:** strong NDVI field monitoring and crop-rotation workflows. **Plantix:** established crop-photo diagnosis + expert community. **eHingiriSoko:** Rwanda-based digital market and agricultural services. IhingaLink's *proposed* positioning: smallholder farmer groups by local Rwandan sector, paired with NASA-evidence-supported crop-rotation scenarios and peer discussion in one accessible interface. This is differentiation in product focus, not proof of superiority or unique features.

Sources: https://onesoil.ai/en/platform , https://www.plantix.net/en/ , https://ehingirisoko.digital/ , https://www.nasaharvest.org/news , https://www.nasa.gov/news-release/nasa-usda-sign-agreement-advancing-earth-science-agriculture/
