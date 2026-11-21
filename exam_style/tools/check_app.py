"""Headless-Edge checks for the assembled app: maths renders, no script errors, quiz flows (single, multi-select, mock), defaults.
Usage: python check_app.py <SP>"""
import html, json, os, re, subprocess, sys

SP = sys.argv[1]
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
src = open(SP + '/out/COMP9417_Exam_Drill.html', encoding='utf8').read()
probe = r'''
(function(){
  const out={flows:[],err:[],jsErrors:window.__errs||[]};
  const box=document.createElement('div'); document.body.appendChild(box);
  const scan=(label,h)=>{ box.innerHTML=h; typeset(box); box.querySelectorAll('.katex-error').forEach(e=>out.err.push([label,e.getAttribute('title')||'',e.textContent.slice(0,80)])); };
  D.qs.filter(q=>q.u==='EX').forEach(q=>{ scan(q.id+' stem',q.q); if(q.e) scan(q.id+' explain',q.e); q.o.forEach((o,i)=>{ scan(q.id+' opt'+i,o.t); scan(q.id+' why'+i,o.w) }) });
  const ex=D.units.find(u=>u.id==='EX'); if(ex) scan('EX notes',ex.html);
  box.remove();
  const step=(n,f)=>{ try{ f(); out.flows.push(n+': ok') }catch(e){ out.flows.push(n+': FAIL '+e.message) } };
  const nEX=D.qs.filter(q=>q.u==='EX').length, nMulti=D.qs.filter(q=>q.u==='EX'&&isMulti(q)).length;
  out.counts={ex:nEX,multi:nMulti,total:D.qs.length,kinds:{}};
  D.qs.filter(q=>q.u==='EX').forEach(q=>out.counts.kinds[q.k]=(out.counts.kinds[q.k]||0)+1);
  step('defaults hide code and derivation',()=>{ if(F.kinds.join()!=='concept,calc') throw new Error(F.kinds.join()); startSmart(); const bad=session.ids.filter(id=>!kindOk(id)); if(bad.length) throw new Error('hidden kinds present') });
  ['home','practice','mock','notes','stats'].forEach(v=>step('view '+v,()=>go(v)));
  step('EX notes reader',()=>{ go('reader',{u:'EX'}); if(!document.querySelector('#prose')) throw new Error('no prose') });
  step('exam-style practice, answer everything',()=>{
    newSession('practice',pick(unitIds('EX').filter(kindOk),Math.min(40,nEX)),'t'); const s=session; let multiSeen=0, rightAll=0;
    for(let i=0;i<s.ids.length;i++){ const id=s.ids[s.idx], q=Q.get(id);
      if(isMulti(q)){ multiSeen++; q.o.forEach((o,k)=>{ if(o.ok) choose(k) }); if(!document.querySelector('[data-act=check-multi]:not([disabled])')) throw new Error('no check button'); checkMulti(); }
      else { choose(q.o.findIndex(o=>o.ok)) }
      if(!document.querySelector('.why')) throw new Error('no reveal for '+id);
      if(!isRight(s,id)) throw new Error('correct choice marked wrong '+id); rightAll++;
      move(1) }
    if(view.name!=='results') throw new Error('not at results: '+view.name);
    out.multiAnswered=multiSeen; out.practiceRight=rightAll+'/'+s.ids.length });
  step('multi-select: partial answer is wrong, exact set is right',()=>{
    const q=D.qs.find(q=>q.u==='EX'&&isMulti(q)); if(!q) return; newSession('practice',[q.id],'t'); const s=session;
    const okIdx=q.o.map((o,i)=>o.ok?i:-1).filter(i=>i>=0); choose(okIdx[0]); checkMulti(); if(isRight(s,q.id)) throw new Error('partial counted right');
    newSession('practice',[q.id],'t'); const s2=session; okIdx.forEach(i=>choose(i)); const wrongIdx=q.o.findIndex(o=>!o.ok); choose(wrongIdx); choose(wrongIdx); checkMulti(); if(!isRight(s2,q.id)) throw new Error('exact set after toggle counted wrong') });
  step('exam-style mock',()=>{
    startExamMock(); const s=session; if(!s||s.mode!=='mock') throw new Error('no mock'); if(s.limitSec!==78*60) throw new Error('limit '+s.limitSec);
    s.ids.slice(0,6).forEach(id=>{ s.idx=s.ids.indexOf(id); const q=Q.get(id); if(isMulti(q)){ q.o.forEach((o,k)=>{ if(o.ok) choose(k) }) } else choose(q.o.findIndex(o=>o.ok)) });
    if(document.querySelector('.why')) throw new Error('mock leaked explanations'); finish(); if(view.name!=='results') throw new Error('no results'); out.mockRight=s.ids.filter(id=>isRight(s,id)).length });
  step('all-topics mock',()=>{ startMock(20); finish() });
  step('review view of a multi question',()=>{ const q=D.qs.find(q=>q.u==='EX'&&isMulti(q)); if(!q) return; newSession('practice',[q.id],'t'); q.o.forEach((o,k)=>{ if(o.ok) choose(k) }); checkMulti(); finish(); session.idx=0; go('quiz'); if(!document.querySelector('.opt.multi')) throw new Error('no multi class') });
  step('kind toggles',()=>{ document.body.dataset.t=1; go('home'); document.querySelector('[data-act=kind-toggle][data-k=code]').click(); if(!F.kinds.includes('code')) throw new Error('code not on'); document.querySelector('[data-act=kind-toggle][data-k=code]').click() });
  step('home after',()=>go('home'));
  document.documentElement.innerHTML='<body><pre id="result">'+JSON.stringify(out).replace(/</g,'&lt;')+'</pre></body>';
})();'''
pre = '<script>window.__errs=[];window.addEventListener("error",e=>window.__errs.push(e.message));</script>'
test = src.replace('<body style="margin:0">', '<body style="margin:0">' + pre, 1).replace('</body></html>', '<script>' + probe + '</script></body></html>')
tp = SP + '/out/_test.html'
open(tp, 'w', encoding='utf8').write(test)
r = subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run', f'--user-data-dir={SP}/edge', '--virtual-time-budget=90000', '--dump-dom', 'file:///' + tp.replace('\\', '/')], capture_output=True, text=True, encoding='utf8', errors='replace', timeout=290)
os.remove(tp)
m = re.search(r'<pre id="result">(.*?)</pre>', r.stdout, re.S)
if not m:
    print('no result', r.stdout[:400], r.stderr[:300]); sys.exit(1)
res = json.loads(html.unescape(m.group(1)))
for f in res['flows']:
    print('  ', f)
print('counts:', res['counts'], '| multi answered', res.get('multiAnswered'), '| practice right', res.get('practiceRight'), '| mock right', res.get('mockRight'))
print('js errors:', res['jsErrors'])
print('maths problems:', len(res['err']))
for e in res['err'][:20]:
    print('  ', e)
