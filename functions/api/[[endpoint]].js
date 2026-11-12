/** Cloudflare Pages Functions: secrets live exclusively in context.env. */
const json=(body,status=200,cache='no-store')=>new Response(JSON.stringify(body),{status,headers:{'Content-Type':'application/json; charset=utf-8','Cache-Control':cache,'X-Content-Type-Options':'nosniff'}});
const timeout=(ms)=>AbortSignal.timeout(ms);
async function authenticate(request,env){
 const token=(request.headers.get('Authorization')||'').replace(/^Bearer\s+/i,'');
 if(!token)return false;
 const url=env.VITE_SUPABASE_URL,apikey=env.VITE_SUPABASE_ANON_KEY;
 if(!url||!apikey)return false;
 const result=await fetch(`${url.replace(/\/$/,'')}/auth/v1/user`,{headers:{apikey,Authorization:`Bearer ${token}`},signal:timeout(8000)});
 return result.ok;
}
function safeText(v,max=120){return typeof v==='string'?v.slice(0,max):''}
async function advisor(request,env){
 if(!env.NVIDIA_API_KEY||!env.NVIDIA_MODEL||!env.VITE_SUPABASE_URL||!env.VITE_SUPABASE_ANON_KEY)return json({error:'Supabase or NVIDIA is not configured'},503);
 if(!await authenticate(request,env))return json({error:'Sign in to use live AI'},401);
 let input;try{input=await request.json()}catch{return json({error:'Invalid JSON'},400)}
 if(typeof input.question!=='string'||input.question.trim().length<2||input.question.length>500)return json({error:'Question must have 2-500 characters'},400);
 const system='You are a cautious Rwanda-focused agricultural learning assistant. Explain crop-rotation tradeoffs; do not invent NASA readings, buyer prices, crop diagnoses, verified yields or emergency warnings. Distinguish observation from prediction, state uncertainty and advise consultation with local agronomists.';
 const prompt=`District: ${safeText(input.location,70)}. Sector: ${safeText(input.sector,70)}. Crops: ${safeText(input.crops,120)}. Question: ${input.question}`;
 const n=await fetch('https://integrate.api.nvidia.com/v1/chat/completions',{method:'POST',headers:{Authorization:`Bearer ${env.NVIDIA_API_KEY}`,'Content-Type':'application/json'},body:JSON.stringify({model:env.NVIDIA_MODEL,messages:[{role:'system',content:system},{role:'user',content:prompt}],temperature:0.2,max_tokens:500}),signal:timeout(24000)});
 if(!n.ok)return json({error:'NVIDIA inference temporarily unavailable'},502);
 const value=await n.json(),answer=value.choices?.[0]?.message?.content;
 return typeof answer==='string'?json({answer,source:'NVIDIA NIM; AI-generated, verify with a local agricultural expert'}):json({error:'No NVIDIA answer returned'},502);
}
async function scan(request,env){
 if(!env.NVIDIA_API_KEY||!env.NVIDIA_VISION_MODEL||!env.VITE_SUPABASE_URL||!env.VITE_SUPABASE_ANON_KEY)return json({error:'Crop photo review is not configured'},503);
 if(!await authenticate(request,env))return json({error:'Sign in first'},401);
 let q;try{q=await request.json()}catch{return json({error:'Invalid JSON'},400)}
 if(typeof q.image!=='string'||q.image.length>3_000_000||!/^data:image\/(jpeg|png|webp);base64,[a-zA-Z0-9+/=]+$/.test(q.image))return json({error:'Use a JPEG, PNG, or WebP image under 2 MB'},400);
 const content=[{type:'text',text:`Look at the ${safeText(q.crop,100)} crop photo. Describe visible signs only, several plausible explanations, and safe non-chemical next steps. Never assert a confirmed disease diagnosis. Mention when to consult an agricultural extension officer.`},{type:'image_url',image_url:{url:q.image}}];
 const n=await fetch('https://integrate.api.nvidia.com/v1/chat/completions',{method:'POST',headers:{Authorization:`Bearer ${env.NVIDIA_API_KEY}`,'Content-Type':'application/json'},body:JSON.stringify({model:env.NVIDIA_VISION_MODEL,messages:[{role:'user',content}],temperature:0.1,max_tokens:440}),signal:timeout(24000)});
 if(!n.ok)return json({error:'NVIDIA vision service temporarily unavailable'},502);
 const value=await n.json(),answer=value.choices?.[0]?.message?.content;
 return typeof answer==='string'?json({answer,source:'AI image interpretation, not a medical or crop diagnosis'}):json({error:'No image interpretation returned'},502);
}
async function nasa(request){
 const q=new URL(request.url).searchParams;
 const latitude=Number(q.get('latitude')),longitude=Number(q.get('longitude')),start=q.get('start')||'',end=q.get('end')||'';
 if(!Number.isFinite(latitude)||!Number.isFinite(longitude)||latitude < -2.95||latitude > -1||longitude <28.7||longitude>30.95||!/^[0-9]{8}$/.test(start)||!/^[0-9]{8}$/.test(end)||start>end||q.get('parameters')!=='T2M,PRECTOTCORR'||(Date.UTC(+end.slice(0,4),+end.slice(4,6)-1,+end.slice(6))-Date.UTC(+start.slice(0,4),+start.slice(4,6)-1,+start.slice(6)))>92*86400000)return json({error:'Invalid location or date range'},400);
 const u=new URL('https://power.larc.nasa.gov/api/temporal/daily/point');u.search=new URLSearchParams({parameters:'T2M,PRECTOTCORR',community:'AG',longitude:String(longitude),latitude:String(latitude),start,end,format:'JSON'});
 const response=await fetch(u,{signal:timeout(12000)});if(!response.ok)return json({error:'NASA POWER temporarily unavailable'},502);
 const body=await response.json();if(!body?.properties?.parameter?.T2M||!body?.properties?.parameter?.PRECTOTCORR)return json({error:'NASA POWER did not return the requested observations'},502);return json(body,200,'public, s-maxage=3600');
}
const decode=s=>s.replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g,'$1').replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"');
async function news(){const u='https://news.google.com/rss/search?q=Rwanda+agriculture+market+farmers&hl=en&gl=RW&ceid=RW:en';const r=await fetch(u,{signal:timeout(10000)});if(!r.ok)return json({error:'News unavailable'},502);const xml=(await r.text()).slice(0,350000);const items=(xml.match(/<item>[\s\S]*?<\/item>/g)||[]).slice(0,8).map(item=>{const tag=k=>decode((item.match(new RegExp(`<${k}>([\\s\\S]*?)<\\/${k}>`))||[])[1]||'');return {title:tag('title').slice(0,180),url:tag('link'),date:tag('pubDate')}}).filter(x=>/^https:\/\//.test(x.url));return json({items,disclaimer:'News headlines are not real-time crop prices'},200,'public, s-maxage=3600')}
export async function onRequest({request,env,params}){
 const endpoint=Array.isArray(params.endpoint)?params.endpoint.join('/'):params.endpoint;
 const isPost=endpoint==='advisor'||endpoint==='crop-scan';
 if(isPost&&request.method!=='POST'||!isPost&&request.method!=='GET')return json({error:'Method not allowed'},405);
 try{
  if(endpoint==='advisor')return await advisor(request,env);
  if(endpoint==='crop-scan')return await scan(request,env);
  if(endpoint==='nasa-power')return await nasa(request);
  if(endpoint==='market-news')return await news();
  return json({error:'Unknown endpoint'},404);
 }catch(e){return json({error:'Service is temporarily unavailable'},502)}
}
