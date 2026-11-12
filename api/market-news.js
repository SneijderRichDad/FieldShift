/** Public headlines only; never present Google News stories as verified market prices. */
const decode=s=>s.replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g,'$1').replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#39;/g,"'");
export default async function handler(req,res){
 res.setHeader('Cache-Control','public, s-maxage=3600, stale-while-revalidate=3600');
 if(req.method!=='GET')return res.status(405).json({error:'Method not allowed'});
 try{const u='https://news.google.com/rss/search?q=Rwanda+agriculture+market+farmers&hl=en&gl=RW&ceid=RW:en';const r=await fetch(u,{signal:AbortSignal.timeout(10000)});if(!r.ok)throw Error('RSS unavailable');const xml=(await r.text()).slice(0,350000);const raw=xml.match(/<item>[\s\S]*?<\/item>/g)||[];
 const items=raw.slice(0,5).map(item=>{const read=tag=>decode((item.match(new RegExp(`<${tag}>([\\s\\S]*?)<\\/${tag}>`))||[])[1]||'');const url=read('link');return {title:read('title').slice(0,200),url:url.startsWith('https://news.google.com/')?url:'',date:read('pubDate').slice(0,80)}}).filter(x=>x.title&&x.url);
 return res.status(200).json({items,notice:'News stories are not verified live commodity prices or trading offers'});
 }catch(e){return res.status(502).json({error:'Public news feed currently unavailable'})}
}
