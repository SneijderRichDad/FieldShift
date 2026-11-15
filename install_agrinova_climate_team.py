from pathlib import Path
import shutil

app = Path('app.js')
if not app.exists():
    raise SystemExit('Run this from your FieldShift repository root (app.js missing).')
s = app.read_text(encoding='utf-8')
if 'function simulation(){' not in s or 'function greenhouse(){' not in s or 'async function fetchClimate(){' not in s:
    raise SystemExit('Expected AgriNova code differs. No changes made.')
if 'NASA POWER live historical baseline' in s:
    raise SystemExit('The climate simulator update is already installed.')
shutil.copyfile(app, 'app.js.before_climate_team')

start=s.index('function simulation(){')
end=s.index('function greenhouse(){',start)
new_sim=r'''function simulation(){
 const district=state.simDistrict||state.profile.district||'Musanze';
 const rain=Number(storage.get('scenarioRain',0));
 const heat=Number(storage.get('scenarioHeat',0));
 const live=state.climateStatus==='live'&&Array.isArray(state.climate)&&state.climate.length>0;
 const days=live?state.climate:[];
 const meanTemp=live?days.reduce((a,x)=>a+x.temp,0)/days.length:null;
 const meanRain=live?days.reduce((a,x)=>a+x.rain,0)/days.length:null;
 const adjustedTemp=live?meanTemp+heat:null;
 const adjustedRain=live?meanRain*(1+rain/100):null;
 const fmt=n=>Number(n).toFixed(1);
 const note='NASA POWER live historical baseline';
 layout(`<section class="card"><div class="row" style="flex-wrap:wrap;align-items:flex-end;gap:16px"><div><h3 style="margin-top:0">Nova Climate Simulator</h3><p class="muted">Explore the latest available NASA POWER historical daily data, then try hypothetical climate changes. This is not a weather forecast or field measurement.</p></div><button id="simLoadNASA" class="btn" ${state.climateStatus==='loading'?'disabled':''}>${state.climateStatus==='loading'?'Loading NASA data…':'↻ Load NASA climate history'}</button></div><div class="field" style="max-width:400px;margin-top:16px"><label class="label" for="simDistrict">Choose Rwandan district</label><select class="input" id="simDistrict">${Object.keys(districts).map(d=>`<option value="${escapeHTML(d)}" ${d===district?'selected':''}>${escapeHTML(d)}</option>`).join('')}</select></div>${state.country!=='Rwanda'?'<p class="notice warn">Climate analysis here is configured for Rwanda only. Switch the location to Rwanda.</p>':''}${state.climateStatus==='error'?`<p class="notice warn" role="alert">NASA request failed: ${escapeHTML(state.climateError||'Request failed')}. No observations have been invented.</p>`:''}<div class="grid two" style="margin-top:17px"><div class="card"><h3>🌡 Temperature</h3><p class="muted">Observed historical daily mean</p><div class="metric"><div class="num">${live?fmt(meanTemp)+'°C':'—'}</div><p class="muted">Hypothetical adjusted mean: <b>${live?fmt(adjustedTemp)+'°C':'Load data first'}</b></p></div><label class="label" for="simHeat">Temperature change: +${heat}°C</label><input id="simHeat" type="range" min="0" max="4" step="0.5" value="${heat}" style="width:100%"/></div><div class="card"><h3>🌧 Rainfall</h3><p class="muted">Observed historical daily average</p><div class="metric"><div class="num">${live?fmt(meanRain)+' mm/day':'—'}</div><p class="muted">Hypothetical adjusted daily mean: <b>${live?fmt(adjustedRain)+' mm/day':'Load data first'}</b></p></div><label class="label" for="simRain">Rainfall change: ${rain>0?'+':''}${rain}%</label><input id="simRain" type="range" min="-50" max="50" step="5" value="${rain}" style="width:100%"/></div></div><p class="muted" style="margin:14px 0">${live?`✓ ${note} · ${escapeHTML(district)} · ${days.length} valid daily values · ${escapeHTML(days[0].date)} through ${escapeHTML(days[days.length-1].date)}. Source: NASA POWER T2M and PRECTOTCORR.`:'No observed baseline loaded. Press “Load NASA climate history” to fetch recent historical observations.'}</p><div class="grid three" style="margin-top:16px"><div class="card"><h3>🌿 Soil cover</h3><p class="muted">${rain>20?'Consider drainage, erosion protection and cover crops.':'Maintain soil cover and evaluate erosion exposure.'}</p></div><div class="card"><h3>💧 Water planning</h3><p class="muted">${rain<-15?'Explore water storage and drought-tolerant rotations.':'Compare crop water requirements with local supplies.'}</p></div><div class="card"><h3>☀ Heat exposure</h3><p class="muted">${heat>=2?'Evaluate heat-sensitive crops and seasonal timing.':'Consider crop tolerance and planting windows.'}</p></div></div><p class="notice" style="margin-top:16px"><b>Interpretation:</b> Values labeled historical are derived from NASA POWER gridded estimates, not real-time weather stations. Scenario adjustments are mathematical what-if exercises, not forecasts, calibrated crop yields, or field-specific advice. Consult local agronomists and official weather services before decisions.</p></section>`);
 const sel=$('#simDistrict');if(sel)sel.onchange=()=>{state.simDistrict=sel.value;state.climate=null;state.climateStatus='not-requested';simulation()};
 const btn=$('#simLoadNASA');if(btn)btn.onclick=()=>{if(state.country!=='Rwanda'){alert('Select Rwanda in the location menu first.');return;}void fetchClimate()};
 ['simRain','simHeat'].forEach(id=>{const el=$('#'+id);if(el)el.onchange=()=>{storage.set(id==='simRain'?'scenarioRain':'scenarioHeat',Number(el.value));simulation()}});
}
'''
s=s[:start]+new_sim+s[end:]

# The existing authenticated/public NASA climate data loader is shared across the
# climate explorer and the simulator. Make its location and render target aware.
a=s.index('async function fetchClimate(){')
b=s.index('\nasync function loadMarketInquiries()',a)
block=s[a:b]
block=block.replace('state.climateError=\'District climate data is currently configured for Rwanda only. Select Rwanda for the current district climate module or consult NASA POWER directly.\';climate();return;', "state.climateError='District climate data is currently configured for Rwanda only. Select Rwanda.';render();return;")
block=block.replace("state.climateStatus='loading';climate();", "state.climateStatus='loading';render();")
block=block.replace("districts[state.profile.district]||districts.Musanze", "districts[state.page==='simulation'?(state.simDistrict||state.profile.district):state.profile.district]||districts.Musanze")
# End-of-load render; preserve current page.
if not block.rstrip().endswith('climate()}'):
    raise SystemExit('The NASA loader end differs from expected. No changes saved.')
block=block.rstrip(); block=block[:-len('climate()}')]+'render()}'
s=s[:a]+block+s[b:]

# Add credits to the existing About page (roles are proposed responsibility areas).
start=s.index('function about(){')
end=s.index('\nfunction startSpeech(){',start)
new_about=r'''function about(){
 const founders=[
 ['MANZI Snejder Arsenal','Product vision & team coordination'],
 ['GISUBIZO Moise','Web application & frontend development'],
 ['UMUTONIWASE Kenitha','UX, accessibility & farmer onboarding'],
 ['MUKUNZI Ally Muhadjir','Backend, data privacy & testing'],
 ['KUNDWA KEZA Dalcia','Markets & farmer partnerships'],
 ['ISARO Sasha Salmah','Climate research & agronomy evidence']
 ];
 layout(`<div class="hero"><div><span class="eyebrow" style="color:white">AGRINOVA · NOVAX LAB · RWANDA</span><h2>Smarter Farming. Stronger Communities.</h2><p>Accessible farming decisions supported by NASA historical climate observations and farmer experience.</p><button class="btn white" data-page="simulation">Explore climate scenarios →</button></div><div class="hero-art">🌱</div></div><div class="grid two" style="margin-top:18px"><div class="card"><h3>Our mission</h3><p>Help farmers understand historical climate, compare crop-rotation options, document farms, and connect with agricultural communities.</p><p class="muted">AgriNova is an educational prototype, not an official NASA service, certified agronomy tool or weather-forecast service.</p></div><div class="card"><h3>Project credits</h3><p><b>Team:</b> NovaX Lab · Rwanda · NASA Space Apps Field Shift challenge</p><p><b>NASA data:</b> NASA POWER historical T2M and PRECTOTCORR. <a href="https://power.larc.nasa.gov/" target="_blank" rel="noopener noreferrer">NASA POWER ↗</a></p><p><b>Technology:</b> JavaScript, Vite, Supabase, Cloudflare Pages, GitHub, OpenStreetMap.</p><p class="muted">AI-assisted code and presentation materials are disclosed in submission documentation. Third-party imagery and resources must retain their applicable attribution.</p></div></div><div class="section-head"><h3>Meet the six co-founders</h3></div><p class="muted">Responsibilities below are proposed work areas for the team to confirm internally.</p><div class="grid three">${founders.map(([name,role])=>`<div class="card"><div style="font-size:27px;margin-bottom:10px">🌿</div><h3 style="font-size:16px;margin-bottom:8px">${escapeHTML(name)}</h3><p class="muted">Co-founder · ${escapeHTML(role)}</p></div>`).join('')}</div>`);
}
'''
s=s[:start]+new_about+s[end:]

app.write_text(s,encoding='utf-8')
print('Installed NASA-connected Climate Simulator and About/team credits.')
print('Backup: app.js.before_climate_team')
print('Next: npm run build && npm test')
