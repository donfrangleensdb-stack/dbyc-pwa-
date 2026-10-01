with open('app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Add minutes render
c = c.replace('rules:renderRulesPage,\n    reports:', 'rules:renderRulesPage,\n    minutes:renderMinutes,\n    reports:', 1)

# Add minutes to noHeader
old_noh = "const noHeader=['profile','members','attendance','qr','scanner','idcard','certificates','points','events','birthdays','news','notifications','reports','account','rules'];"
new_noh = "const noHeader=['profile','members','attendance','qr','scanner','idcard','certificates','points','events','birthdays','news','notifications','reports','account','rules','minutes'];"
c = c.replace(old_noh, new_noh, 1)

# Also add filterNews function
filter_fn = '''
function filterNews(btn, cat){
  document.querySelectorAll('.filter-chip').forEach(b=>b.classList.remove('filter-active'));
  btn.classList.add('filter-active');
  const d=getData(), u=getUser();
  const el=document.getElementById('newsList'); if(!el) return;
  let news=[...(d.news||[])].reverse();
  let anns=d.announcements.filter(a=>a.group==='All'||a.group===u?.group).reverse();
  if(cat!=='all'){
    news=news.filter(n=>n.category===cat);
    anns=cat==='Announcement'?anns:[];
  }
  let html='';
  news.forEach(n=>{html+=newsItemHtml(n,d,u);});
  if(anns.length>0){
    html+='<div style="font-size:0.72rem;font-weight:800;color:#1a237e;letter-spacing:1px;margin:10px 0 6px">ANNOUNCEMENTS</div>';
    anns.forEach(a=>{html+=`<div style="padding:10px 0;border-bottom:1px solid #eee"><div style="font-weight:700;color:#1a237e;font-size:0.85rem">${a.title}</div><div style="font-size:0.8rem;color:#333;margin:3px 0">${a.message}</div><div style="font-size:0.65rem;color:var(--dbyc-muted)">${a.group} • ${fmtDate(a.date)} • ${a.author}</div></div>`;});
  }
  el.innerHTML=html||'<div class="empty-msg">No news in this category</div>';
}
'''
# Insert after renderNews function closing
c = c.replace('function updateTickerFromData()', filter_fn + '\nfunction updateTickerFromData()', 1)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(c)

print('Done!')
print('minutes render:', 'minutes:renderMinutes' in c)
print('noHeader minutes:', "'minutes'" in c)
print('filterNews:', 'filterNews' in c)
