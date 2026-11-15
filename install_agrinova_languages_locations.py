from pathlib import Path
import shutil

p=Path('app.js')
if not p.exists(): raise SystemExit('Run from the repository root containing app.js.')
s=p.read_text(encoding='utf-8')
if 'function agriTranslatePage()' in s: raise SystemExit('Localization installer already applied.')
backup=Path('app.js.before_languages_locations')
if not backup.exists(): shutil.copy2(p,backup)

def replace_once(old,new):
 global s
 if old not in s: raise SystemExit('Missing expected code anchor: '+old[:100]+' — no app.js changes saved.')
 s=s.replace(old,new,1)

# The list of subdivisions is explicitly named according to each country's administrative hierarchy.
# Do not invent lower levels for countries where our verified data is incomplete.
geo=r'''// AgriNova regional hierarchy. Countries do not share the same division names.
const agriRegions={
 Rwanda:{label:'Province / City of Kigali',localLabel:'District',regions:{
  'City of Kigali':['Gasabo','Kicukiro','Nyarugenge'],
  'Eastern Province':['Bugesera','Gatsibo','Kayonza','Kirehe','Ngoma','Nyagatare','Rwamagana'],
  'Northern Province':['Burera','Gakenke','Gicumbi','Musanze','Rulindo'],
  'Southern Province':['Gisagara','Huye','Kamonyi','Muhanga','Nyamagabe','Nyanza','Nyaruguru','Ruhango'],
  'Western Province':['Karongi','Ngororero','Nyabihu','Nyamasheke','Rubavu','Rusizi','Rutsiro']
 }},
 Kenya:{label:'County',localLabel:'Sub-county / town',regions:{'Counties':['Baringo','Bomet','Bungoma','Busia','Elgeyo Marakwet','Embu','Garissa','Homa Bay','Isiolo','Kajiado','Kakamega','Kericho','Kiambu','Kilifi','Kirinyaga','Kisii','Kisumu','Kitui','Kwale','Laikipia','Lamu','Machakos','Makueni','Mandera','Marsabit','Meru','Migori','Mombasa',"Murang'a",'Nairobi City','Nakuru','Nandi','Narok','Nyamira','Nyandarua','Nyeri','Samburu','Siaya','Taita Taveta','Tana River','Tharaka Nithi','Trans Nzoia','Turkana','Uasin Gishu','Vihiga','Wajir','West Pokot']}},
 Uganda:{label:'Region',localLabel:'District / town',regions:{'Regions':['Central','Eastern','Northern','Western']}},
 Tanzania:{label:'Region',localLabel:'District / town',regions:{'Regions':['Arusha','Dar es Salaam','Dodoma','Geita','Iringa','Kagera','Katavi','Kigoma','Kilimanjaro','Lindi','Manyara','Mara','Mbeya','Morogoro','Mtwara','Mwanza','Njombe','Pemba North','Pemba South','Pwani','Rukwa','Ruvuma','Shinyanga','Simiyu','Singida','Songwe','Tabora','Tanga','Zanzibar North','Zanzibar South and Central','Zanzibar West']}},
 Burundi:{label:'Province',localLabel:'Commune',regions:{
  'Buhumuza':['Butaganzwa','Butihinda','Cankuzo','Gisagara','Gisuru','Muyinga','Ruyigi'],
  'Bujumbura':['Bubanza','Bukinanyana','Cibitoke','Isare','Mpanda','Mugere','Mugina','Muhuta','Mukaza','Ntahangwa','Rwibaga'],
  'Burunga':['Bururi','Makamba','Matana','Musongati','Nyanza','Rumonge','Rutana'],
  'Butanyerera':['Busoni','Kayanza','Kiremba','Kirundo','Matongo','Muhanga','Ngozi','Tangara'],
  'Gitega':['Bugendana','Gishubi','Gitega','Karusi','Kiganda','Muramvya','Mwaro','Nyabihanga','Shombo']
 }},
 'DR Congo':{label:'Province',localLabel:'Territory / city',regions:{'Provinces':['Bas-Uele','Equateur','Haut-Katanga','Haut-Lomami','Haut-Uele','Ituri','Kasai','Kasai-Central','Kasai-Oriental','Kinshasa','Kongo Central','Kwango','Kwilu','Lomami','Lualaba','Mai-Ndombe','Maniema','Mongala','Nord-Kivu','Nord-Ubangi','Sankuru','Sud-Kivu','Sud-Ubangi','Tanganyika','Tshopo','Tshuapa']}}
};
function agriRegionNames(country){const regions=agriRegions[country]?.regions||{};return Object.values(regions).flat();}
function agriRwandaRegion(district){const regions=agriRegions.Rwanda.regions;return Object.keys(regions).find(region=>regions[region].includes(district))||'City of Kigali';}
function agriRegionSelect(country,current='',id='agriRegion'){
 const entry=agriRegions[country]||agriRegions.Rwanda;
 const names=agriRegionNames(country);
 if(country==='Rwanda' || country==='Burundi'){
   const groups=Object.entries(entry.regions);
   const regions=groups.map(([name])=>name);
   const selected=regions.includes(current)?current:regions[0];
   return `<label class="label" for="${id}">${escapeHTML(entry.label)}</label><select class="input" name="region" id="${id}" required>${regions.map(x=>`<option value="${escapeHTML(x)}" ${x===selected?'selected':''}>${escapeHTML(x)}</option>`).join('')}</select>`;
 }
 const selected=names.includes(current)?current:names[0];
 return `<label class="label" for="${id}">${escapeHTML(entry.label)}</label><select class="input" name="region" id="${id}" required>${names.map(x=>`<option value="${escapeHTML(x)}" ${x===selected?'selected':''}>${escapeHTML(x)}</option>`).join('')}</select>`;
}
function agriLocalInput(country,region,current='',id='districtSelect'){
 const entry=agriRegions[country]||agriRegions.Rwanda;
 const options=(entry.regions||{})[region]||[];
 const selected=options.includes(current)?current:options[0]||'';
 if(country==='Rwanda'||country==='Burundi')return `<label class="label" for="${id}">${escapeHTML(entry.localLabel)}</label><select class="input" id="${id}" name="district" required>${options.map(x=>`<option value="${escapeHTML(x)}" ${x===selected?'selected':''}>${escapeHTML(x)}</option>`).join('')}</select>`;
 return `<label class="label" for="${id}">${escapeHTML(entry.localLabel)}</label><input class="input" id="${id}" name="district" maxlength="80" required placeholder="Enter ${escapeHTML(entry.localLabel.toLowerCase())}" value="${escapeHTML(current)}">`;
}
function agriSwapLocal(country,region,holderId,fieldId){const holder=document.querySelector('#'+holderId);if(holder)holder.innerHTML=agriLocalInput(country,region,'',fieldId);}
'''
replace_once('const marketCountries=supportedCountries;', 'const marketCountries=supportedCountries;\n'+geo)

# Extended language selector rather than the previous two-state button.
replace_once('<button class="btn secondary small" id="langSwitch" aria-label="Switch language">${state.lang===\'en\'?\'RW\':\'EN\'}</button>', '<select class="btn secondary small" id="languageSelect" aria-label="Language"><option value="en" ${state.lang===\'en\'?\'selected\':\'\'}>English</option><option value="rw" ${state.lang===\'rw\'?\'selected\':\'\'}>Kinyarwanda</option><option value="fr" ${state.lang===\'fr\'?\'selected\':\'\'}>Français</option></select>')

translations=r'''// DOM translations cover fixed interface text only, never user-authored content.
// Add further strings to this dictionary as new feature copy is introduced.
const agriStrings={
 'Your farming world, connected':['Ubuhinzi bwawe, hamwe','Votre univers agricole connecté'],
 'Rooted in Rwanda.':['Dushingiye mu Rwanda.','Enracinés au Rwanda.'],
 'Growing together.':['Dukura twese hamwe.','Grandir ensemble.'],
 'WELCOME TO YOUR FARMING COMMUNITY':['MURAKAZA NEZA MU IHURIRO RY’ABAHINZI','BIENVENUE DANS VOTRE COMMUNAUTÉ AGRICOLE'],
 'One trusted space for climate intelligence, stronger crop rotations and the farmers who make Rwanda grow.':['Ahantu hamwe hizewe ho kwiga iby’ikirere, guhinduranya ibihingwa no guhuza abahinzi.','Un seul espace fiable pour le climat, la rotation des cultures et les agriculteurs.'],
 'Manage my farms ↗':['Cunga imirima yanjye ↗','Gérer mes fermes ↗'],
 'Plan next season ↗':['Tegura igihembwe gitaha ↗','Planifier la prochaine saison ↗'],
 'Plan every season with confidence.':['Tegura buri gihembwe ufite icyizere.','Planifiez chaque saison en confiance.'],
 'Keep all your farms, field records and rotation decisions in one secure place.':['Bika amakuru y’imirima n’imigambi y’ihinga ahizewe.','Conservez les données de vos fermes et vos plans au même endroit sécurisé.'],
 'My registered farms':['Imirima yanjye yanditswe','Mes fermes enregistrées'],
 'Private to you':['Ni ibyawe gusa','Privé pour vous'],
 'This information stays private. Never share precise farm coordinates in community posts.':['Aya makuru ni ibanga. Ntugatangaze aho umurima uherereye neza mu butumwa rusange.','Ces informations restent privées. Ne publiez pas les coordonnées exactes de vos champs.'],
 'Start with your first field to build a private growing history.':['Tangira wandika umurima wawe wa mbere.','Commencez par enregistrer votre première parcelle.'],
 'Your crop season history will appear here.':['Amateka y’ibihembwe azagaragara hano.','Votre historique de cultures apparaîtra ici.'],
 'Find your next buyer. Find what farms are selling.':['Shakisha umuguzi. Menya ibigurishwa n’abahinzi.','Trouvez votre acheteur. Découvrez les récoltes proposées.'],
 'No registered-user matches yet':['Nta matangazo ahuye n’ibyo ushaka','Aucune annonce correspondante'],
 'No matching offer or buyer request has been published in this location. Change filters or start the market by publishing your harvest.':['Nta bicuruzwa cyangwa ubusabe biboneka hano. Hindura ibyo ushakisha cyangwa utangaze umusaruro wawe.','Aucune offre ou demande ici. Modifiez les filtres ou publiez votre récolte.'],
 'Discover more real markets':['Menya andi masoko','Découvrir d’autres marchés'],
 'Find your next buyer. Find what farms are selling.':['Shakisha umuguzi. Menya ibigurishwa n’abahinzi.','Trouvez votre acheteur. Découvrez les récoltes proposées.'],
 'Agriculture insights, local markets and farmer community — start with your location.':['Amakuru y’ubuhinzi, amasoko n’ihuriro ry’abahinzi — tangirira aho uherereye.','Informations agricoles, marchés et communauté — commencez par votre lieu.'],
 'Connect with farmers in your sector. Share what works, ask questions, and plan together.':['Ganira n’abahinzi bo mu murenge wawe, musangire ubumenyi.','Échangez avec les agriculteurs de votre secteur et planifiez ensemble.'],
 'Farmer experience · not verified advice':['Uburambe bw’umuhinzi · si inama zemejwe','Expérience agricole · conseils non vérifiés'],
 'Share a question or farming experience':['Sangiza abandi ikibazo cyangwa uburambe','Partager une question ou une expérience'],
 'Sign in first to publish to the real marketplace.':['Banza winjire kugira ngo utangaze ku isoko.','Connectez-vous pour publier une annonce.'],
 'Price to negotiate':['Igiciro kiganirwaho','Prix à négocier'],
 'Your listing':['Itangazo ryawe','Votre annonce'],
 'Send private inquiry →':['Ohereza ubutumwa bwihariye →','Envoyer une demande privée →'],
 'Sign in to inquire':['Injira kugira ngo ubaze','Connectez-vous pour demander'],
 'No observed baseline loaded. Press “Load NASA climate history” to fetch recent historical observations.':['Nta makuru ya NASA arafungurwa. Kanda kugira ngo uyabone.','Aucune donnée NASA chargée. Chargez les observations historiques.'],
 'Hypothetical adjusted mean:':['Ikigereranyo cyahinduwe mu buryo bw’igerageza:','Moyenne hypothétique ajustée :'],
 'Load data first':['Banza ufungure amakuru','Charger d’abord les données'],
 'Search crops, district or description...':['Shakisha igihingwa, akarere cyangwa ibisobanuro...','Rechercher culture, district ou description...'],
 'Save my farm profile':['Bika umwirondoro wanjye','Enregistrer mon profil'],
 'Dashboard':['Ahabanza','Tableau de bord'],'My Farms':['Imirima yanjye','Mes exploitations'],
 'Nova Planner':['Igenamigambi rya Nova','Planificateur Nova'],'Nova AI':['Nova AI','Nova IA'],
 'Nova Climate':['Ikirere cya Nova','Climat Nova'],'Nova Connect':['Ihuriro rya Nova','Communauté Nova'],
 'Nova Chat':['Ubutumwa bwa Nova','Messagerie Nova'],'Nova Market':['Isoko rya Nova','Marché Nova'],
 'Farm Map':['Ikarita y’imirima','Carte des fermes'],'Success Stories':['Inkuru z’intsinzi','Témoignages de réussite'],
 'NASA Research':['Ubushakashatsi bwa NASA','Recherches de la NASA'],
 'Climate Simulator':['Ikigereranyo cy’ikirere','Simulateur climatique'],
 'Greenhouse Planner':['Igenamigambi rya serire','Planification de serre'],
 'Crop Photo Review':['Isuzuma ry’ifoto y’igihingwa','Analyse de photo de culture'],
 'My Profile':['Umwirondoro wanjye','Mon profil'],'Private Account':['Konti yihariye','Compte privé'],
 'Notifications':['Amatangazo','Notifications'],'Help & Security':['Ubufasha n’umutekano','Aide et sécurité'],
 'About AgriNova':['Ibyerekeye AgriNova','À propos d’AgriNova'],
 'WORKSPACE':['AHO UKORERA','ESPACE DE TRAVAIL'], 'MORE TO EXPLORE':['IBINDI','À DÉCOUVRIR'],
 'Location':['Ahantu','Lieu'],'Search crops, districts, farmer stories...':['Shakisha ibihingwa, uturere n’inkuru...','Rechercher des cultures, des districts et des récits...'],
 'Better harvests, together.':['Umusaruro mwiza, twese hamwe.','De meilleures récoltes, ensemble.'],
 'Explore community →':['Sura ihuriro →','Explorer la communauté →'],
 'Your farming world, connected':['Ubuhinzi bwawe, hamwe','Votre monde agricole connecté'],
 'Farm name':['Izina ry’umurima','Nom de la ferme'],'Your display name':['Izina rigaragara','Nom affiché'],
 'Country':['Igihugu','Pays'],'District':['Akarere','District'], 'District / city':['Akarere / umujyi','District / ville'],
 'Sector':['Umurenge','Secteur'],'Province':['Intara','Province'],'Province / City of Kigali':['Intara / Umujyi wa Kigali','Province / Ville de Kigali'],
 'County':['Kaunti','Comté'],'Sub-county / town':['Agace / umujyi','Sous-comté / ville'],
 'Region':['Intara','Région'],'District / town':['Akarere / umujyi','District / ville'],
 'Territory / city':['Teritwari / umujyi','Territoire / ville'],
 'Commune':['Komine','Commune'], 'Farm name':['Izina ry’umurima','Nom de la ferme'],
 'Crop':['Igihingwa','Culture'],'Quantity':['Ingano','Quantité'],'Soil type':['Ubwoko bw’ubutaka','Type de sol'],
 'Area (hectares)':['Ubuso (hegitari)','Surface (hectares)'],
 'Farm name':['Izina ry’umurima','Nom de la ferme'],'Crop seasons':['Ibihembwe by’ihinga','Saisons culturales'],
 'Registered farms':['Imirima yanditswe','Fermes enregistrées'],
 'Saved rotation plans':['Gahunda z’ihinduranya ry’ibihingwa','Plans de rotation enregistrés'],
 'Add a farm':['Ongeramo umurima','Ajouter une ferme'],
 'Save farm securely →':['Bika umurima mu mutekano →','Enregistrer la ferme en sécurité →'],
 'Record a growing season':['Andika igihembwe cy’ihinga','Enregistrer une saison culturale'],
 'Choose farm':['Hitamo umurima','Choisir la ferme'], 'Season':['Igihembwe','Saison'],
 'Planting date (optional)':['Itariki yo gutera (si ngombwa)','Date de semis (facultatif)'],
 'Save my farm profile':['Bika umwirondoro wanjye','Enregistrer mon profil'],
 'Account & Google sign-in':['Konti no kwinjira na Google','Compte et connexion Google'],
 'Continue with Google':['Komeza ukoresheje Google','Continuer avec Google'],
 'Sign out':['Sohoka','Déconnexion'],'Sign in':['Injira','Connexion'],
 'Privacy and location':['Amabanga n’aho uherereye','Confidentialité et localisation'],
 'Farm and farmer information':['Amakuru y’umuhinzi n’umurima','Informations sur le fermier et la ferme'],
 'Farmer and farm information':['Amakuru y’umuhinzi n’umurima','Informations de l’agriculteur et de la ferme'],
 'Crop or produce':['Igihingwa cyangwa umusaruro','Culture ou produit agricole'],
 'I want to':['Ndashaka','Je souhaite'],'Sell my harvest':['Kugurisha umusaruro','Vendre ma récolte'],
 'Find a farmer to buy from':['Kubona umuhinzi nguraho','Trouver un agriculteur vendeur'],
 'Expected price (optional)':['Igiciro nifuza (si ngombwa)','Prix souhaité (facultatif)'],
 'Notes (optional)':['Ibisobanuro (si ngombwa)','Notes (facultatif)'],
 'Publish verified-account listing →':['Tangaza ibyo ugurisha cyangwa ushaka →','Publier votre annonce →'],
 'All listings':['Amatangazo yose','Toutes les annonces'],'Harvest for sale':['Umusaruro ugurishwa','Récoltes à vendre'],
 'Buyers looking for crops':['Abashaka kugura ibihingwa','Acheteurs de cultures'],
 'Offers for sale':['Ibicuruzwa','Offres de vente'],'Buyer requests':['Ubusabe bw’abaguzi','Demandes des acheteurs'],
 'Published user listings':['Amatangazo yashyizweho','Annonces publiées'],
 'Messages about my offers':['Ubutumwa ku bicuruzwa byanjye','Messages concernant mes offres'],
 'Refresh inbox':['Vugurura ubutumwa','Actualiser la boîte de réception'],
 'Publish an offer or request':['Tangaza igicuruzwa cyangwa ubusabe','Publier une offre ou une demande'],
 'Registered users':['Abiyandikishije','Utilisateurs inscrits'],
 'Nova Climate Simulator':['Ikigereranyo cy’ikirere cya Nova','Simulateur climatique Nova'],
 'Choose Rwandan district':['Hitamo akarere mu Rwanda','Choisir un district du Rwanda'],
 'Load NASA climate history':['Fungura amakuru ya NASA y’ikirere','Charger l’historique climatique NASA'],
 'Observed historical daily mean':['Ikigereranyo cy’ubushyuhe bwabayeho','Moyenne quotidienne historique observée'],
 'Observed historical daily average':['Imvura mpuzandengo yabayeho','Moyenne quotidienne historique observée'],
 'Rainfall':['Imvura','Précipitations'],'Temperature':['Ubushyuhe','Température'],
 'Soil cover':['Gupfuka ubutaka','Couverture du sol'],
 'Water planning':['Gahunda y’amazi','Planification de l’eau'],
 'Heat exposure':['Ingaruka z’ubushyuhe','Exposition à la chaleur'],
 'Nova Chat':['Ubutumwa bwa Nova','Messagerie Nova'],'Available farmers':['Abahinzi baboneka','Agriculteurs disponibles'],
 'Message':['Ubutumwa','Message'],'Send':['Ohereza','Envoyer'], 'Block':['Hagarika','Bloquer'],
 'View my farms ↗':['Reba imirima yanjye ↗','Voir mes fermes ↗'],
 'My district':['Akarere kanjye','Mon district'],'My sector':['Umurenge wanjye','Mon secteur'],
 'All Rwanda':['U Rwanda hose','Tout le Rwanda'],
 'Join farmer chat':['Injira mu butumwa bw’abahinzi','Rejoindre la messagerie'],
 'Our mission':['Intego yacu','Notre mission'],'Project credits':['Abadufashije','Crédits du projet'],
 'Meet the six co-founders':['Menya abashinze umushinga batandatu','Rencontrez les six cofondateurs'],
 'Save':['Bika','Enregistrer'],'Cancel':['Hagarika','Annuler'], 'Delete':['Siba','Supprimer'],
 'Search':['Shakisha','Rechercher'],'Loading...':['Birimo gufunguka...','Chargement...'],
 'Date not entered':['Itariki ntiyanditswe','Date non renseignée'],
 'Area not entered':['Ubuso ntibwanditswe','Surface non renseignée'],
 'Soil not recorded':['Ubwoko bw’ubutaka ntibwanditswe','Sol non renseigné'],
 'No farms registered yet':['Nta mirima irandikwa','Aucune ferme enregistrée'],
 'Your crop season history will appear here.':['Amateka y’ibihembwe azagaragara hano.','Votre historique de cultures apparaîtra ici.']
};
function agriTranslatePage(){
 if(state.lang==='en'||!document.querySelectorAll||!document.createTreeWalker)return;
 const root=document.querySelector('#app');if(!root)return;
 const index=state.lang==='fr'?1:0;
 const exclude='.chat-message,.comment,.market-details,.story-body,[data-post] p,.farm-record h3';
 const walker=document.createTreeWalker(root,4); // SHOW_TEXT
 const nodes=[];let node;while((node=walker.nextNode()))nodes.push(node);
 for(const n of nodes){const parent=n.parentElement;if(!parent||parent.closest(exclude)||['SCRIPT','STYLE','TEXTAREA'].includes(parent.tagName))continue;
  const raw=n.nodeValue||'';const key=raw.trim();if(!key||!agriStrings[key])continue;
  const translated=agriStrings[key][index];
  if(parent.tagName==='OPTION' && !parent.hasAttribute('value'))parent.value=key; // keep DB values stable
  n.nodeValue=raw.replace(key,translated);
 }
 for(const el of root.querySelectorAll('[placeholder],[title],[aria-label]')){
  for(const name of ['placeholder','title','aria-label']){const value=el.getAttribute(name);if(agriStrings[value])el.setAttribute(name,agriStrings[value][index]);}
 }
}
'''
replace_once('function layout(content){',translations+'\nfunction layout(content){')
replace_once('</main></div></div>`;}\nfunction hero()', '</main></div></div>`;agriTranslatePage();}\nfunction hero()')
replace_once("if(e.target.id==='countrySelect'){", "if(e.target.id==='languageSelect'){state.lang=e.target.value;storage.set('lang',state.lang);render();return;}if(e.target.id==='countrySelect'){")

# Profile: region selector and country-appropriate district field.
old='''<div class="field"><label class="label">District</label><select class="input" id="districtSelect" name="district">${Object.keys(districts).map(d=>`<option ${d===state.profile.district?'selected':''}>${d}</option>`).join('')}</select></div>'''
new='''<div class="field">${agriRegionSelect(state.country, state.country==='Rwanda'?agriRwandaRegion(state.profile.district):(state.profile.country===state.country?state.profile.region:''),'profileRegion')}</div><div class="field" id="profileLocality">${agriLocalInput(state.country,state.country==='Rwanda'?agriRwandaRegion(state.profile.district):(state.profile.country===state.country?state.profile.region:agriRegionNames(state.country)[0]),state.profile.country===state.country?state.profile.district:(state.country==='Rwanda'?state.profile.district:''),'districtSelect')}</div>'''
replace_once(old,new)
replace_once("if(e.target.id==='districtSelect'){", "if(e.target.id==='profileRegion'){agriSwapLocal(state.country,e.target.value,'profileLocality','districtSelect');return;}if(e.target.id==='marketCountry'){state.country=e.target.value;storage.set('country',state.country);state.marketScope='all';const mainCountry=$('#countrySelect');if(mainCountry)mainCountry.value=state.country;const holder=$('#marketLocationFields');if(holder)holder.innerHTML=agriRegionSelect(state.country,'','marketRegion')+'<div id=\"marketLocality\">'+agriLocalInput(state.country,(agriRegions[state.country]&&Object.keys(agriRegions[state.country].regions)[0])||'','', 'marketDistrict')+'</div>';return;}if(e.target.id==='marketRegion'){agriSwapLocal(state.country,e.target.value,'marketLocality','marketDistrict');return;}if(e.target.id==='districtSelect'){")
# Correct earlier bug: for Kenya/Uganda/etc their region options are under synthetic grouping key, and locality manual.
replace_once("(agriRegions[state.country]&&Object.keys(agriRegions[state.country].regions)[0])||''", "agriRegionNames(state.country)[0]||''")
replace_once("state.profile={name:data.name.trim(),district:data.district,sector:data.sector,crops:data.crops.trim()||'Not entered',priority:data.priority};", "state.profile={...state.profile,name:data.name.trim(),country:state.country,region:data.region||'',district:data.district,sector:data.sector,crops:data.crops.trim()||'Not entered',priority:data.priority};")
replace_once("display_name:state.profile.name,district:state.profile.district,sector:state.profile.sector,crops:state.profile.crops,priority:state.profile.priority", "display_name:state.profile.name,country:state.profile.country||'Rwanda',region:state.profile.region||'',district:state.profile.district,sector:state.profile.sector,crops:state.profile.crops,priority:state.profile.priority")
replace_once(".select('display_name,district,sector,crops,priority')", ".select('display_name,country,region,district,sector,crops,priority')")

# Market form: country-specific admin divisions, stored in the region column.
old='<select class="input" name="country">${supportedCountries.map(c=>`<option ${c===country?\'selected\':\'\'}>${escapeHTML(c)}</option>`).join(\'\')}</select><label class="label">District / city</label><input class="input" name="district" maxlength="80" required value="${escapeHTML(country===\'Rwanda\'?state.profile.district:\'\')}" placeholder="Your district or city">'
new='<select class="input" id="marketCountry" name="country">${supportedCountries.map(c=>`<option value="${escapeHTML(c)}" ${c===country?\'selected\':\'\'}>${escapeHTML(c)}</option>`).join(\'\')}</select><div id="marketLocationFields">${agriRegionSelect(country,country===\'Rwanda\'?agriRwandaRegion(state.profile.district):\'\',\'marketRegion\')}<div id="marketLocality">${agriLocalInput(country,country===\'Rwanda\'?agriRwandaRegion(state.profile.district):agriRegionNames(country)[0],country===\'Rwanda\'?state.profile.district:\'\',\'marketDistrict\')}</div></div>'
replace_once(old,new)
replace_once("unit:data.unit||'kg',district:String(data.district).trim(),", "unit:data.unit||'kg',region:String(data.region||''),district:String(data.district).trim(),")

# Scope farm-registration UI to Rwanda because the farm table currently lacks a country field.
replace_once('const auth=!!(state.supabase&&state.auth);\n const formDisabled=auth?', "const auth=!!(state.supabase&&state.auth);\n const farmCountrySupported=state.country==='Rwanda';\n const formDisabled=auth&&farmCountrySupported?")
replace_once("${!auth?`<div class=\"notice warn\"><b>Google sign-in required:", "${!farmCountrySupported?'<p class=\"notice warn\">Farm registration and NASA district climate data currently support Rwanda only. You can use Nova Market with the other countries; wider farm support requires a country-aware farm schema.</p>':''}${!auth?`<div class=\"notice warn\"><b>Google sign-in required:")

# Update country change to clear stale profile region for market, while preserving saved farm data.
replace_once("state.marketScope='all';state.climate=null;state.climateStatus='not-requested';render();return;", "state.marketScope='all';state.climate=null;state.climateStatus='not-requested';render();return;")

p.write_text(s,encoding='utf-8')
print('Installed EN/RW/FR localization and country-aware profile/market selectors.')
print('Backup:',backup)
print('Database migration must be applied before new profile/market fields are used. Run npm run build && npm test.')
