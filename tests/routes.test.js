import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const app=fs.readFileSync(new URL('../app.js',import.meta.url),'utf8');
const validation=fs.readFileSync(new URL('../lib/story-validation.js',import.meta.url),'utf8');
const pure=app.replace("import {validateStoryInput,validateStoryFile,isSupportedStoryVideo} from './lib/story-validation.js';",validation.replace(/\bexport /g,''))
 .replace(/\bexport function /g,'function ')
 .replaceAll('import.meta.env?.','({})?.')
 .replace('render();initSupabase().then(ok=>{if(!ok)initFirebase()});','render();');
function appInstance(){
 const root={innerHTML:''};
 const fakeElement={scrollHeight:100,scrollTop:0,innerHTML:'',value:'',setAttribute(){},addEventListener(){}};
 const document={querySelector(sel){return sel==='#app'?root:fakeElement},addEventListener(){}};
 const memory=new Map();
 const context={innerWidth:1366,document,console,Date,Math,JSON,localStorage:{getItem:k=>memory.get(k),setItem:(k,v)=>memory.set(k,v)},URL,fetch:async()=>{throw Error('No network')},navigator:{},window:{},setTimeout,clearTimeout};
 vm.createContext(context);
 vm.runInContext(pure+';globalThis.__setPage=(id)=>{state.page=id;render();return document.querySelector("#app").innerHTML};',context);
 return {root,render:context.__setPage};
}
test('all 16 intended pages render content without uncaught exceptions in demo state',()=>{
 const a=appInstance();
 for(const page of ['dashboard','community','rotation','climate','explorer','research','market','advisor','profile','simulation','greenhouse','scanner','help','about','stories','account','notifications']){
  const html=a.render(page);
  assert.ok(html.includes('<main'),page+' should render main');
  assert.ok(html.length>800,page+' should have substantive UI');
 }
});
test('untrusted user cannot access review admin or see admin navigation',()=>{
 const a=appInstance();
 const view=a.render('admin');
 assert.match(view,/No reviewed farmer stories yet/);
 assert.doesNotMatch(view,/data-page="admin"/);
});
test('new stories page requests real sign-in and never invents a success case',()=>{
 const a=appInstance();
 const view=a.render('stories');
 assert.match(view,/No reviewed farmer stories yet/);
 assert.match(view,/Sign in with a configured Supabase Google account/);
});

test('private account and notifications require real authenticated Supabase session',()=>{const a=appInstance();assert.match(a.render('account'),/Sign in required/);assert.match(a.render('notifications'),/Sign in to see private notifications/)});
