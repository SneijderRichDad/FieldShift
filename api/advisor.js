/** Authenticated Vercel function proxying NVIDIA NIM; the NVIDIA key never reaches browsers. */
export default async function handler(req,res){
  res.setHeader('Cache-Control','no-store');
  if(req.method!=='POST')return res.status(405).json({error:'Method not allowed'});
  const url=process.env.VITE_SUPABASE_URL,key=process.env.VITE_SUPABASE_ANON_KEY,token=String(req.headers.authorization||'').replace(/^Bearer\s+/i,'');
  if(!url||!key||!process.env.NVIDIA_API_KEY||!process.env.NVIDIA_MODEL)return res.status(503).json({error:'Supabase or NVIDIA is not configured'});
  if(!token)return res.status(401).json({error:'Sign in to use live AI'});
  const q=req.body||{};
  if(typeof q.question!=='string'||q.question.length<2||q.question.length>500)return res.status(400).json({error:'Question must be 2-500 characters'});
  try{
    const user=await fetch(`${url.replace(/\/$/,'')}/auth/v1/user`,{headers:{apikey:key,Authorization:`Bearer ${token}`},signal:AbortSignal.timeout(8000)});
    if(!user.ok)return res.status(401).json({error:'Invalid or expired login'});
    const source=`You are IhingaLink's cautious crop-rotation educator. Ground reasoning in farmer-provided location and crops, but never invent measurements, forecast precision, disease diagnoses, buyers, or emergency warnings. Give a concise practical explanation, identify missing local soil and season data, and recommend consulting a local agronomist before field changes. Avoid prescribing specific pesticides. No direct access to NASA data is provided in this request.`;
    const response=await fetch('https://integrate.api.nvidia.com/v1/chat/completions',{method:'POST',headers:{'Content-Type':'application/json',Authorization:`Bearer ${process.env.NVIDIA_API_KEY}`},body:JSON.stringify({model:process.env.NVIDIA_MODEL,messages:[{role:'system',content:source},{role:'user',content:`District: ${String(q.location||'unspecified').slice(0,70)}; Sector: ${String(q.sector||'unspecified').slice(0,70)}; Crops: ${String(q.crops||'unspecified').slice(0,120)}. Question: ${q.question}`}],temperature:0.2,max_tokens:400}),signal:AbortSignal.timeout(22000)});
    if(!response.ok)throw Error('NVIDIA provider unavailable');const json=await response.json();const answer=json.choices?.[0]?.message?.content;
    if(typeof answer!=='string')throw Error('No assistant response');return res.status(200).json({answer,source:'NVIDIA NIM model, AI-generated; review with local experts'});
  }catch(err){return res.status(502).json({error:'AI provider temporarily unavailable; try again later'})}
}
