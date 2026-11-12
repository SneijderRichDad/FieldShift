/** Optional NVIDIA multimodal vision service. Auth verified with Supabase; never return a confirmed crop disease diagnosis. */
export default async function handler(req,res){
 res.setHeader('Cache-Control','no-store');
 if(req.method!=='POST')return res.status(405).json({error:'Method not allowed'});
 const url=process.env.VITE_SUPABASE_URL,key=process.env.VITE_SUPABASE_ANON_KEY,token=String(req.headers.authorization||'').replace(/^Bearer\s+/i,'');
 if(!url||!key||!process.env.NVIDIA_API_KEY||!process.env.NVIDIA_VISION_MODEL)return res.status(503).json({error:'Vision analysis is not configured'});
 if(!token)return res.status(401).json({error:'Sign in first'});
 const img=req.body?.image;
 if(typeof img!=='string'||img.length>3_000_000||!/^data:image\/(jpeg|png|webp);base64,[a-zA-Z0-9+/=]+$/.test(img))return res.status(400).json({error:'Upload JPEG, PNG or WebP below 2MB'});
 try{
  const user=await fetch(`${url.replace(/\/$/,'')}/auth/v1/user`,{headers:{apikey:key,Authorization:`Bearer ${token}`},signal:AbortSignal.timeout(8000)});if(!user.ok)return res.status(401).json({error:'Invalid session'});
  const result=await fetch('https://integrate.api.nvidia.com/v1/chat/completions',{method:'POST',headers:{'Content-Type':'application/json',Authorization:`Bearer ${process.env.NVIDIA_API_KEY}`},body:JSON.stringify({model:process.env.NVIDIA_VISION_MODEL,max_tokens:350,temperature:0.2,messages:[{role:'system',content:'Provide an educational crop-photo observation, not a definitive diagnosis. Describe visible symptoms if detectable, list multiple possible explanations with uncertainty, suggest which information to gather, recommend consulting a local agronomist. Never invent tests or prescribe chemicals.'},{role:'user',content:[{type:'text',text:`Review this crop image for visible concerns. Farm crop context: ${String(req.body.crop||'unspecified').slice(0,120)}.`},{type:'image_url',image_url:{url:img}}]}]}),signal:AbortSignal.timeout(25000)});
  if(!result.ok)throw Error('Vision model rejected request');const payload=await result.json();const answer=payload.choices?.[0]?.message?.content;if(typeof answer!=='string')throw Error('No vision output');return res.status(200).json({answer,provisional:true});
 }catch(err){return res.status(502).json({error:'Vision provider is unavailable; consult an agricultural expert'})}
}
