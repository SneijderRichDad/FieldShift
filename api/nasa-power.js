/** Vercel Node.js function. Public NASA data only; bounds prevent abuse and excessive API requests. */
export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'public, s-maxage=3600, stale-while-revalidate=86400');
  if (req.method !== 'GET') return res.status(405).json({error:'Method not allowed'});
  const q = req.query || {};
  const lat = Number(q.latitude), lon = Number(q.longitude);
  const date = /^\d{8}$/;
  if (!Number.isFinite(lat) || !Number.isFinite(lon) || lat < -2.95 || lat > -1.0 || lon < 28.7 || lon > 30.95 ||
      !date.test(String(q.start||'')) || !date.test(String(q.end||'')) || q.start>q.end ||
      String(q.parameters||'')!=='T2M,PRECTOTCORR') {
    return res.status(400).json({error:'Invalid Rwanda location, dates, or parameter list'});
  }
  const start = Date.UTC(+String(q.start).slice(0,4),+String(q.start).slice(4,6)-1,+String(q.start).slice(6));
  const end = Date.UTC(+String(q.end).slice(0,4),+String(q.end).slice(4,6)-1,+String(q.end).slice(6));
  if (end-start>92*86400000 || end>Date.now()) return res.status(400).json({error:'Date interval out of range'});
  const url = new URL('https://power.larc.nasa.gov/api/temporal/daily/point');
  Object.entries({parameters:'T2M,PRECTOTCORR',community:'AG',longitude:lon,latitude:lat,start:q.start,end:q.end,format:'JSON','time-standard':'UTC'}).forEach(([k,v])=>url.searchParams.set(k,String(v)));
  try {
    const response = await fetch(url,{signal:AbortSignal.timeout(15000)});
    if(!response.ok) throw new Error(`NASA HTTP ${response.status}`);
    const json = await response.json();
    if(!json?.properties?.parameter?.T2M || !json?.properties?.parameter?.PRECTOTCORR) throw new Error('Missing NASA parameters');
    return res.status(200).json(json);
  } catch (err) {
    return res.status(502).json({error:'NASA POWER is temporarily unavailable. No substitute data generated.'});
  }
}
