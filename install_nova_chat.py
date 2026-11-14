from pathlib import Path

p = Path('app.js')
if not p.exists():
    raise SystemExit('Run from FieldShift repository root (app.js not found).')
s = p.read_text()
if 'function novaChatPage()' in s:
    raise SystemExit('Nova Chat is already installed; no changes made.')

navneedle = "['community','♧','Nova Connect']"
if navneedle not in s:
    navneedle = "['community','♧','Farmer Community']"
assert navneedle in s, 'Could not locate farmer community navigation'
s=s.replace(navneedle,navneedle+",['messages','✉','Nova Chat']",1)

rneedle = 'community,rotation,climate,explorer,research'
assert rneedle in s, 'Render router differs; no edits saved'
s=s.replace(rneedle,'community,messages:novaChatPage,rotation,climate,explorer,research',1)

# Add realtime to existing Supabase subscription (RLS restricts payload to participants)
rtneedle = ".on('postgres_changes',{event:'INSERT',schema:'public',table:'farm_notifications',filter:'user_id=eq.'+state.auth.id},async()=>{await loadPersonalData();if(state.page==='notifications')render()}).subscribe();"
assert rtneedle in s, 'Realtime hook not found; no edits saved'
s=s.replace(rtneedle, ".on('postgres_changes',{event:'INSERT',schema:'public',table:'nova_chat_messages',filter:'recipient_id=eq.'+state.auth.id},async()=>{if(state.page==='messages')await loadNovaMessages()})\n "+rtneedle,1)

chat_js = r'''
// NOVA CHAT — authenticated, opt-in private farmer messaging.
const novaChat = {owner:null, ready:false, loading:false, busy:false, available:false, users:[], blocks:[], peer:null, messages:[], error:'', notice:''};
function novaReset(){novaChat.owner=state.auth?.id||null;novaChat.ready=false;novaChat.loading=false;novaChat.available=false;novaChat.users=[];novaChat.blocks=[];novaChat.peer=null;novaChat.messages=[];novaChat.error='';novaChat.notice='';}
const novaSafeId=id=>/^[0-9a-f-]{36}$/i.test(String(id||''));
async function novaLoadDirectory(){
 if(!state.auth||!state.supabase)return;
 if(novaChat.loading)return;
 novaChat.loading=true;
 try{
  const [own,peers,blocked]=await Promise.all([
   state.supabase.from('nova_chat_profiles').select('user_id,available').eq('user_id',state.auth.id).maybeSingle(),
   state.supabase.from('nova_chat_profiles').select('user_id,display_name,district').eq('available',true).order('display_name').limit(100),
   state.supabase.from('nova_chat_blocks').select('blocked_id').eq('blocker_id',state.auth.id)
  ]);
  if(own.error||peers.error||blocked.error)throw Error(own.error?.message||peers.error?.message||blocked.error?.message);
  novaChat.available=!!own.data?.available;
  novaChat.blocks=(blocked.data||[]).map(b=>b.blocked_id);
  novaChat.users=(peers.data||[]).filter(u=>u.user_id!==state.auth.id);
  novaChat.ready=true;novaChat.error='';
 }catch(e){novaChat.error=e.message||'Could not load chats';}
 finally{novaChat.loading=false;if(state.page==='messages')novaChatPage();}
}
async function loadNovaMessages(){
 if(!state.auth||!state.supabase||!novaSafeId(novaChat.peer))return;
 const me=state.auth.id,them=novaChat.peer;
 const {data,error}=await state.supabase.from('nova_chat_messages')
  .select('id,sender_id,recipient_id,body,created_at')
  .or(`and(sender_id.eq.${me},recipient_id.eq.${them}),and(sender_id.eq.${them},recipient_id.eq.${me})`)
  .order('created_at',{ascending:false}).limit(100);
 if(error)novaChat.error=error.message;
 else {novaChat.messages=(data||[]).reverse();novaChat.error='';}
 if(state.page==='messages')novaChatPage();
}
function novaChatPage(){
 const me=state.auth?.id||null;
 if(novaChat.owner!==me)novaReset();
 if(!state.auth||!state.supabase){
  layout('<section class="card"><h3>Nova Chat</h3><p>Sign in with Google to message farmers privately.</p><button class="btn" data-page="profile">Sign in to continue</button></section>');return;
 }
 if(!novaChat.ready&&!novaChat.loading&&!novaChat.error)void novaLoadDirectory();
 const selected=novaChat.users.find(u=>u.user_id===novaChat.peer);
 const contacts=novaChat.users.filter(u=>!novaChat.blocks.includes(u.user_id));
 layout(`<section class="nova-chat-shell">
  <div class="nova-chat-head"><div><h2>✉ Nova Chat</h2><p>Private conversations between farmers who choose to be available. No precise locations are shared.</p></div>
  <button type="button" class="btn ${novaChat.available?'secondary':''}" id="novaToggle">${novaChat.available?'Pause my availability':'Join farmer chat'}</button></div>
  ${novaChat.error?`<p class="notice warn" role="alert">${escapeHTML(novaChat.error)}</p>`:''}
  ${novaChat.notice?`<p class="nova-chat-notice" role="status">${escapeHTML(novaChat.notice)}</p>`:''}
  <div class="nova-chat-grid"><aside class="nova-chat-people"><div class="nova-chat-section">Available farmers <span>${contacts.length}</span></div>
  ${!novaChat.available?'<p class="nova-chat-empty">Select “Join farmer chat” to appear in the directory and send messages.</p>':''}
  ${contacts.map(u=>`<button type="button" class="nova-chat-person ${u.user_id===novaChat.peer?'selected':''}" data-nova-peer="${escapeHTML(u.user_id)}"><span class="nova-chat-avatar">${escapeHTML(u.display_name?.charAt(0)||'F')}</span><span><strong>${escapeHTML(u.display_name)}</strong><small>${escapeHTML(u.district||'Farmer')}</small></span></button>`).join('')||'<p class="nova-chat-empty">No other farmers available yet. Invite another registered farmer to join Nova Chat.</p>'}
  </aside><section class="nova-chat-conversation">${selected?`
   <div class="nova-chat-partner"><div><strong>${escapeHTML(selected.display_name)}</strong><small>${escapeHTML(selected.district||'Farmer')} · Private conversation</small></div><button type="button" class="btn secondary small" id="novaBlock">Block farmer</button></div>
   <div class="nova-chat-thread" role="log" aria-label="Conversation">${novaChat.messages.map(m=>`<div class="nova-chat-bubble ${m.sender_id===state.auth.id?'mine':'theirs'}"><p>${escapeHTML(m.body)}</p><small>${escapeHTML(new Date(m.created_at).toLocaleString())}</small></div>`).join('')||'<p class="nova-chat-empty">No messages yet. Start with a respectful greeting.</p>'}</div>
   <form id="novaMessageForm" class="nova-chat-compose"><label for="novaMessage" class="sr-only">Write a private message</label><textarea id="novaMessage" name="message" required maxlength="1500" rows="2" placeholder="Write a message..." ${!novaChat.available?'disabled':''}></textarea><button class="btn" type="submit" ${!novaChat.available?'disabled':''}>Send</button></form>
  `:'<div class="nova-chat-placeholder"><span>🌱</span><h3>Grow connections, one conversation at a time.</h3><p>Select an available farmer to start a private chat.</p></div>'}</section></div>
  <p class="nova-chat-privacy">Please avoid sharing passwords, precise home or farm locations, or sensitive personal information. You can block a farmer at any time.</p>
 </section>`);
 const thread=document.querySelector('.nova-chat-thread');if(thread)thread.scrollTop=thread.scrollHeight;
}
async function novaToggleAvailability(){
 if(!state.auth||!state.supabase||novaChat.busy)return;
 novaChat.busy=true;novaChat.error='';
 try{
  const available=!novaChat.available;
  const profileName=String(state.profile?.name||state.auth.user_metadata?.full_name||'Farmer').trim().slice(0,60)||'Farmer';
  const {error}=await state.supabase.from('nova_chat_profiles').upsert({user_id:state.auth.id,display_name:profileName,district:String(state.profile?.district||'').slice(0,80),available,updated_at:new Date().toISOString()},{onConflict:'user_id'});
  if(error)throw error;
  novaChat.available=available;novaChat.notice=available?'You are now visible to other available farmers.':'Your profile is hidden from the farmer directory.';
  await novaLoadDirectory();
 }catch(e){novaChat.error=e.message||'Could not change availability';}
 finally{novaChat.busy=false;if(state.page==='messages')novaChatPage();}
}
async function novaSend(message){
 if(!novaChat.available||!novaSafeId(novaChat.peer)||novaChat.busy||!state.auth)return;
 const body=String(message||'').trim();if(!body||body.length>1500)return;
 novaChat.busy=true;
 try{
  const {error}=await state.supabase.from('nova_chat_messages').insert({sender_id:state.auth.id,recipient_id:novaChat.peer,body});
  if(error)throw error;
  await loadNovaMessages();
 }catch(e){novaChat.error=e.message||'Message could not be sent';}
 finally{novaChat.busy=false;if(state.page==='messages')novaChatPage();}
}
async function novaBlockSelected(){
 if(!novaSafeId(novaChat.peer)||!state.auth||!confirm('Block this farmer? They will not be able to message you.'))return;
 const {error}=await state.supabase.from('nova_chat_blocks').insert({blocker_id:state.auth.id,blocked_id:novaChat.peer});
 if(error){novaChat.error=error.message;novaChatPage();return;}
 novaChat.peer=null;novaChat.messages=[];novaChat.notice='Farmer blocked.';await novaLoadDirectory();
}
document.addEventListener('click',async e=>{
 if(e.target.closest('#novaToggle')){await novaToggleAvailability();return;}
 if(e.target.closest('#novaBlock')){await novaBlockSelected();return;}
 const button=e.target.closest('[data-nova-peer]');if(!button)return;
 if(!novaChat.available){novaChat.notice='Join farmer chat before opening a conversation.';novaChatPage();return;}
 const id=button.dataset.novaPeer;
 if(!novaSafeId(id)||novaChat.blocks.includes(id))return;
 novaChat.peer=id;novaChat.messages=[];novaChatPage();await loadNovaMessages();
});
document.addEventListener('submit',async e=>{
 if(e.target.id!=='novaMessageForm')return;
 e.preventDefault();const field=e.target.querySelector('[name="message"]');if(field)await novaSend(field.value);
});
'''
s += '\n' + chat_js + '\n'
p.write_text(s)

css = Path('styles.css')
if not css.exists():
    raise SystemExit('styles.css not found')
cs=css.read_text()
cs += r'''
/* Nova Chat: private farmer messages */
.nova-chat-shell{background:var(--panel-bg,#fff);border:1px solid var(--line-color,#d9e6d9);color:var(--main-text,#163b32);border-radius:20px;padding:20px;box-shadow:0 10px 34px #123d2a0a}
.nova-chat-head{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:20px}
.nova-chat-head h2{margin:0;color:var(--main-text,#163b32)}
.nova-chat-head p,.nova-chat-privacy{font-size:12px;color:var(--sub-text,#5b7664)}
.nova-chat-grid{display:grid;grid-template-columns:minmax(205px,290px) minmax(0,1fr);border:1px solid var(--line-color,#dce8dd);border-radius:16px;overflow:hidden;min-height:460px}
.nova-chat-people{border-right:1px solid var(--line-color,#dce8dd);background:var(--input-bg,#f7faf6);padding:14px;min-width:0}
.nova-chat-section{display:flex;justify-content:space-between;font-size:13px;font-weight:800;padding:8px 6px 14px}
.nova-chat-person{display:flex;align-items:center;gap:10px;width:100%;padding:12px 8px;text-align:left;border:0;background:transparent;color:var(--main-text,#163b32);border-radius:12px}
.nova-chat-person:hover,.nova-chat-person.selected{background:rgba(91,173,108,.18)}
.nova-chat-person strong,.nova-chat-person small{display:block;overflow-wrap:anywhere}
.nova-chat-person small,.nova-chat-partner small{font-size:11px;opacity:.7;margin-top:3px}
.nova-chat-avatar{flex:0 0 36px;width:36px;height:36px;border-radius:50%;display:grid;place-items:center;background:#b9e4bf;color:#16442d;font-weight:800}
.nova-chat-conversation{display:flex;flex-direction:column;min-width:0;min-height:450px}
.nova-chat-partner{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:15px;border-bottom:1px solid var(--line-color,#dce8dd)}
.nova-chat-partner small{display:block}
.nova-chat-thread{flex:1;height:340px;overflow:auto;display:flex;flex-direction:column;gap:9px;padding:20px;background:var(--page-bg,#edf3e9)}
.nova-chat-bubble{max-width:82%;padding:12px 15px;border-radius:15px;background:var(--panel-bg,#fff);align-self:flex-start;overflow-wrap:anywhere}
.nova-chat-bubble.mine{background:#216c4b;color:#fff;align-self:flex-end}
.nova-chat-bubble p{margin:0 0 5px;white-space:pre-wrap;font-size:13px;line-height:1.5;color:inherit}
.nova-chat-bubble small{opacity:.65;font-size:10px}
.nova-chat-compose{display:flex;gap:10px;padding:13px;border-top:1px solid var(--line-color,#dce8dd)}
.nova-chat-compose textarea{flex:1;min-width:0;padding:10px;border:1px solid var(--line-color,#dce8dd);border-radius:12px;color:var(--main-text,#163b32);background:var(--input-bg,#fff);resize:vertical}
.nova-chat-empty{font-size:12px;color:var(--sub-text,#607a68);padding:8px;line-height:1.6}
.nova-chat-placeholder{margin:auto;text-align:center;max-width:330px;padding:32px;color:var(--sub-text,#5b7664)}
.nova-chat-placeholder span{font-size:40px}
.nova-chat-placeholder h3{color:var(--main-text,#163b32)}
.nova-chat-notice{padding:8px 12px;background:#e4f7e7;border-radius:10px;color:#155536;font-size:12px}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
@media(max-width:700px){.nova-chat-head{flex-wrap:wrap}.nova-chat-grid{grid-template-columns:1fr}.nova-chat-people{border-right:0;border-bottom:1px solid var(--line-color,#dce8dd);max-height:220px;overflow:auto}.nova-chat-thread{height:280px}.nova-chat-shell{padding:10px}}
'''
css.write_text(cs)
print('Nova Chat installed into app.js and styles.css')
