# NASA evidence register (checked 9 November 2026)

**API:** [NASA POWER daily API](https://power.larc.nasa.gov/docs/services/api/temporal/daily/). The MVP requests `T2M` mean near-surface air temperature and `PRECTOTCORR` precipitation for a **district-reference coordinate** over a past date window. POWER data are gridded estimates, not field instruments. [NASA POWER open-data description](https://data.nasa.gov/dataset/prediction-of-worldwide-energy-resources-power) notes that meteorological data may lag by 2–3 days. The app therefore requests dates ending one week back and checks response validity. It explicitly says when no data was obtained.

**Potential next satellite sources:** [GPM IMERG](https://gpm.nasa.gov/data/imerg) for satellite-based precipitation estimates, [SMAP](https://power.larc.nasa.gov/docs/methodology/data/sources_hydrology/) for coarse-scale soil moisture, Landsat for vegetation indices, and locally calibrated soil characteristics. None is yet integrated into the running MVP, so the app must not advertise those layers as active.

## Verified research articles included in-app
- **26 October 2026:** [NASA, USDA Sign Agreement Advancing Earth Science, Agriculture](https://www.nasa.gov/news-release/nasa-usda-sign-agreement-advancing-earth-science-agriculture/). Policy/research context, not local farmer alerts.
- **20 October 2026:** [The Human Fingerprint on Earth's Water Cycle](https://science.nasa.gov/earth/earth-observatory/the-human-fingerprint-on-earths-water-cycle/). GRACE/GRACE-FO terrestrial water storage over years, *not* a forecast for Rwanda farms.
- **29 May 2026:** [Painting the Growing Season in the Maize Triangle](https://science.nasa.gov/earth/earth-observatory/painting-the-growing-season-in-the-maize-triangle/). NISAR radar captures seasonal crop patterns in South Africa, illustrative of remote-sensing potential, not direct Rwanda observations.

Articles are manually curated. "NASA Research" is **not** a live news API or a disaster alert feed. This prevents stale headlines from being misrepresented as real-time agricultural conditions.
