import os, re

# Read app.js
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace Data Layer with safe storage engine
old_data_layer_marker = '// ══════════════════════════════════════════════════════\n// DATA LAYER\n// ══════════════════════════════════════════════════════'
new_data_layer = '''// ══════════════════════════════════════════════════════
// DATA LAYER (Robust storage with fallback)
// ══════════════════════════════════════════════════════
const _memStore = {};
function safeStorageGet(k) {
  try {
    if (typeof localStorage !== 'undefined') {
      const v = localStorage.getItem(k);
      if (v !== null) return v;
    }
  } catch(e) {}
  try {
    if (typeof sessionStorage !== 'undefined') {
      const v = sessionStorage.getItem(k);
      if (v !== null) return v;
    }
  } catch(e) {}
  return _memStore[k] !== undefined ? _memStore[k] : null;
}
function safeStorageSet(k, v) {
  _memStore[k] = v;
  try { if (typeof localStorage !== 'undefined') localStorage.setItem(k, v); } catch(e) {}
  try { if (typeof sessionStorage !== 'undefined') sessionStorage.setItem(k, v); } catch(e) {}
}
function safeStorageRemove(k) {
  delete _memStore[k];
  try { if (typeof localStorage !== 'undefined') localStorage.removeItem(k); } catch(e) {}
  try { if (typeof sessionStorage !== 'undefined') sessionStorage.removeItem(k); } catch(e) {}
}
function save(d) {
  try { safeStorageSet(SK, JSON.stringify(d)); } catch(e) { console.warn('save error:', e); }
}
function seed() {
  const d = {
    members:[], attendance:[], announcements:[], events:[], pts_log:[], nid:1,
    minutes:[], news:[], notifications:[], readNotifs:[],
    tickers:['Welcome to Don Bosco Youth Centre! 🙏 May God bless all our members!',
             'DBYC – Building Young Lives through Faith, Hope and Love.',
             '"Give me souls, take away the rest." – St. John Bosco']
  };
  addMember(d, {
    name:'Director DBYC', dob:'1980-01-01', mobile:'9000000001',
    email:'director@dbyc.org', address:'Don Bosco Youth Centre',
    group:'Elder', role:'Director', password:'admin123', photo:''
  });
  d.announcements.push({id:Date.now(),title:'Welcome to DBYC!',message:'God bless you! Welcome to Don Bosco Youth Centre.',group:'All',date:today(),author:'Director'});
  d.news.push({id:Date.now()+1, title:'DBYC App Launched!', content:'Our new member management app is now live. Download it on your phone!', category:'General', date:today(), author:'Director', pinned:true});
  d.minutes.push({id:Date.now()+2, title:'First Meeting – September 2026', date:today(), group:'All', agenda:'1. Welcome new members\\n2. Group activities planning\\n3. Attendance policy review', decisions:'All members must attend minimum 75% meetings. New activities planned for October.', attendees:1, author:'Director'});
  d.notifications.push({id:Date.now()+3, type:'system', title:'Welcome to DBYC!', body:'Your account has been created. God bless you!', date:today(), icon:'🙏', read:false});
  save(d); return d;
}
function migrateData(d) {
  if(!d) return seed();
  if(!d.members) d.members=[];
  if(!d.attendance) d.attendance=[];
  if(!d.announcements) d.announcements=[];
  if(!d.events) d.events=[];
  if(!d.pts_log) d.pts_log=[];
  if(!d.minutes) d.minutes=[];
  if(!d.news) d.news=[];
  if(!d.notifications) d.notifications=[];
  if(!d.readNotifs) d.readNotifs=[];
  if(!d.tickers) d.tickers=[];
  return d;
}
function getData() {
  try {
    const raw = safeStorageGet(SK);
    if(!raw) return seed();
    return migrateData(JSON.parse(raw));
  } catch(e) {
    console.warn('getData fallback:', e);
    return seed();
  }
}
function today() { return new Date().toISOString().split('T')[0]; }
function getUser() {
  try {
    const id = safeStorageGet(UK);
    if(!id) return null;
    return getData().members.find(m => m.id.toUpperCase() === id.toUpperCase()) || null;
  } catch(e) { return null; }
}
function setUser(m) {
  try {
    if(m && m.id) safeStorageSet(UK, m.id);
    else safeStorageRemove(UK);
  } catch(e) {}
}'''

# Replace from DATA LAYER to function addMember
pos_dl = js.find(old_data_layer_marker)
pos_am = js.find('function addMember(d, info)')

if pos_dl != -1 and pos_am != -1:
    js = js[:pos_dl] + new_data_layer + '\n' + js[pos_am:]
    print('Data layer replaced successfully')
else:
    print('Warning: could not locate data layer markers', pos_dl, pos_am)

# Replace doLogin
old_do_login = '''function doLogin(){
  const u=$('loginUser').value.trim(), p=$('loginPass').value;
  if(!u||!p){toast('⚠️ Enter ID and password');return;}
  const d=getData();
  const m=d.members.find(x=>(x.id===u||x.mobile===u||x.email===u)&&x.password===p&&x.active);
  if(!m){toast('❌ Invalid credentials');return;}
  setUser(m); launchApp();
}'''

new_do_login = '''function doLogin(){
  const uIn = $('loginUser'), pIn = $('loginPass');
  if(!uIn || !pIn) return;
  const u = uIn.value.trim(), p = pIn.value;
  if(!u || !p){ toast('⚠️ Enter ID and password'); return; }
  const d = getData();
  const m = d.members.find(x => 
    (x.id.toUpperCase() === u.toUpperCase() || 
     (x.mobile && x.mobile.trim() === u) || 
     (x.email && x.email.toLowerCase() === u.toLowerCase())) &&
    x.password === p && x.active !== false
  );
  if(!m){ toast('❌ Invalid ID or Password (Default: DBYC0001 / admin123)'); return; }
  setUser(m);
  toast(`✅ Welcome, ${m.name}!`);
  launchApp();
}'''

js = js.replace(old_do_login, new_do_login)

# Replace launchApp, updateHeader, initSlideshow, and end init
old_launch_marker = '// ══════════════════════════════════════════════════════\n// APP LAUNCH\n// ══════════════════════════════════════════════════════'
pos_launch = js.find(old_launch_marker)
pos_nav = js.find('// ══════════════════════════════════════════════════════\n// NAVIGATION')

new_launch_block = '''// ══════════════════════════════════════════════════════
// APP LAUNCH
// ══════════════════════════════════════════════════════
function launchApp(){
  try {
    const auth = $('auth-screen');
    if(auth) auth.style.display='none';
    const app = $('app');
    if(app) app.classList.add('show');
    try { allMemberSelects(); } catch(e){ console.warn(e); }
    try { updateHeader(); } catch(e){ console.warn(e); }
    try { renderHome(); } catch(e){ console.warn(e); }
    try { initTicker(); } catch(e){ console.warn(e); }
    try { initSlideshow(); } catch(e){ console.warn(e); }
    try { goPage('home'); } catch(e){ console.warn(e); }
  } catch(err) {
    console.error('launchApp error:', err);
  }
}
function updateHeader(){
  const u=getUser(); if(!u) return;
  const dAvatar=$('drawerAvatar');
  if(dAvatar) {
    dAvatar.innerHTML = u.photo
      ? `<img src="${u.photo}" class="drawer-avatar" alt="">`
      : `<div class="drawer-avatar-ph">${GI[u.group]||'👤'}</div>`;
  }
  if($('drawerName')) $('drawerName').textContent=u.name;
  if($('drawerRole')) $('drawerRole').textContent=`${u.role} • ${u.group}`;
  if($('drawerId')) $('drawerId').textContent=u.id;
  if(isAdmin()){
    if($('drawerAdminSection')) $('drawerAdminSection').style.display='';
    if($('drawerAdminItem')) $('drawerAdminItem').style.display='';
  }
  if($('adminTile')) $('adminTile').style.display=isAdmin()?'':'none';
  if($('addMemberBtn')) $('addMemberBtn').style.display=isSuperAdmin()?'':'none';
  if($('addEventBtn')) $('addEventBtn').style.display=isAdmin()?'':'none';
}
function initTicker(){
  try {
    const d=getData();
    const anns=(d.announcements||[]).slice(-5).map(a=>a.title+' – '+a.message);
    const ticks=[...(d.tickers||[]),...anns];
    const el=$('tickerText');
    if(el) el.textContent=ticks.join('   •   ');
  } catch(e){}
}
function initSlideshow(){
  try {
    const slides=document.querySelectorAll('.bg-slide');
    if(!slides || slides.length === 0) return;
    let i=0;
    setInterval(()=>{
      try {
        if(slides[i]) slides[i].classList.remove('on');
        i=(i+1)%slides.length;
        if(slides[i]) slides[i].classList.add('on');
      } catch(e){}
    },6000);
  } catch(e){}
}
'''

if pos_launch != -1 and pos_nav != -1:
    js = js[:pos_launch] + new_launch_block + '\n' + js[pos_nav:]
    print('Launch block replaced successfully')

# Replace End Init Block
old_init_marker = '// ══════════════════════════════════════════════════════\n// APP INIT\n// ══════════════════════════════════════════════════════'
pos_init = js.find(old_init_marker)

new_init_block = '''// ══════════════════════════════════════════════════════
// APP INIT (Fast & Safe Boot)
// ══════════════════════════════════════════════════════
let splashDismissed = false;
function dismissSplash(){
  if(splashDismissed) return;
  splashDismissed = true;
  const s = $('splash');
  if(s){
    s.classList.add('hide');
    setTimeout(()=>{
      s.style.display='none';
      setupInitialView();
    }, 350);
  } else {
    setupInitialView();
  }
}
function setupInitialView(){
  try {
    const u = getUser();
    if(u){
      launchApp();
    } else {
      const auth = $('auth-screen');
      if(auth) auth.style.display='flex';
      const app = $('app');
      if(app) app.classList.remove('show');
      showPanel('login');
    }
  } catch(err) {
    console.error('setupInitialView error:', err);
    const auth = $('auth-screen');
    if(auth) auth.style.display='flex';
    showPanel('login');
  }
}
function bootApp(){
  try {
    if('serviceWorker' in navigator && location.protocol.startsWith('http')) {
      navigator.serviceWorker.register('sw.js').catch(()=>{});
    }
  } catch(e){}
  initSlideshow();
  setTimeout(dismissSplash, 1200);
}

if(document.readyState === 'complete' || document.readyState === 'interactive'){
  bootApp();
} else {
  document.addEventListener('DOMContentLoaded', bootApp);
  window.addEventListener('load', bootApp);
}
// Absolute safety net: dismiss after 2.5s no matter what
setTimeout(dismissSplash, 2500);
'''

if pos_init != -1:
    js = js[:pos_init] + new_init_block
    print('Init block replaced successfully')

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print('app.js written!')
