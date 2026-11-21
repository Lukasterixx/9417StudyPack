"""Assemble the app: base data + EX notes and questions, with the multi-select / exam-style app changes.
Usage: python assemble.py <SP>    writes SP/out/index.html (page body for the Artifact tool) and SP/out/COMP9417_Exam_Drill.html (standalone)."""
import glob, html, json, os, re, sys

SP = sys.argv[1]
OLD_LIB = SP + '/lib'
sys.path.insert(0, SP + '/tools')
sys.path.append(OLD_LIB)
import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer
from qbank import parse, qid

TOKEN = re.compile(r'(```.*?```|`[^`\n]+`|\$\$.+?\$\$|(?<![\\$])\$(?!\s)(?:[^$\n]|\\\$)+?(?<![\s\\])\$(?!\d))', re.S)
PH = 'XMATHPLACEHOLDERX{}X'


def protect(src):
    math = []

    def sub(m):
        t = m.group(0)
        if t.startswith('`'):
            return t
        disp = t.startswith('$$')
        math.append((disp, (t[2:-2] if disp else t[1:-1]).strip()))
        return PH.format(len(math) - 1)

    return TOKEN.sub(sub, src), math


def restore(out, math):
    def sub(m):
        disp, tex = math[int(m.group(1))]
        return f'<span class="{"md" if disp else "m"}">{html.escape(tex, quote=False)}</span>'

    out = re.sub(r'XMATHPLACEHOLDERX(\d+)X', sub, out)
    out = out.replace('\\$', '<span>$</span>')
    return out.replace('<table>', '<div class="tw"><table>').replace('</table>', '</table></div>')


def md(src, inline=False, extra=()):
    s, math = protect(src)
    eng = markdown.Markdown(extensions=['tables', 'fenced_code', 'sane_lists', 'codehilite', *extra],
                            extension_configs={'codehilite': {'guess_lang': False, 'css_class': 'hl'}})
    out = eng.convert(s)
    if inline and out.startswith('<p>') and out.endswith('</p>') and out.count('<p>') == 1:
        out = out[3:-4]
    return restore(out, math), eng


def code_html(code):
    return highlight(code, PythonLexer(), HtmlFormatter(nowrap=False, cssclass='hl')).strip()


# ---------------------------------------------------------------- data
D = json.load(open(SP + '/base/data_v1.json', encoding='utf8'))
D['units'] = [u for u in D['units'] if u['id'] != 'EX']
D['qs'] = [q for q in D['qs'] if q['u'] != 'EX']

ex_notes = SP + '/work/notes/EX.md'
if os.path.exists(ex_notes):
    src = open(ex_notes, encoding='utf8').read()
    h, eng = md(src, extra=('toc',))
    toc = [{'id': t['id'], 't': html.unescape(t['name'])} for top in eng.toc_tokens for t in (top['children'] or [top])]
    D['units'].insert(0, {'id': 'EX', 'code': 'EX', 'short': 'Exam-style', 'title': 'Exam toolkit and exam-style practice', 'html': h, 'toc': toc,
                          'mins': max(1, round(len(src.split()) / 200)), 'gloss': None, 'noq': 0})
nq = 0
for f in sorted(glob.glob(SP + '/work/questions/EX*.txt')):
    parsed, errs = parse(f)
    if errs:
        print(os.path.basename(f), 'parse errors', errs[:3])
    for q in parsed:
        D['qs'].append({
            'id': qid('EX', q), 'u': 'EX', 't': q['topic'], 'k': q['kind'], 'd': int(q['diff']), 's': q['source'],
            'm': 1 if (q.get('multi') == 'yes' or sum(o['ok'] for o in q['options']) > 1) else 0,
            'q': md(q['stem'])[0], 'c': code_html(q['code']) if q['code'] else '',
            'e': md(q['explain'])[0] if q['explain'] else '',
            'o': [{'t': md(o['text'], inline=True)[0], 'w': md(o['why'])[0], 'ok': 1 if o['ok'] else 0} for o in q['options']],
        })
        nq += 1
ids = [q['id'] for q in D['qs']]
assert len(ids) == len(set(ids)), 'duplicate question ids'
if not any(u['id'] == 'EX' for u in D['units']) and nq:
    print('questions exist but no EX notes yet: the EX unit will be missing')

# ---------------------------------------------------------------- app patches
head = open(SP + '/base/template_head.html', encoding='utf8').read()
tail = open(SP + '/base/template_tail.html', encoding='utf8').read()


def rep(s, old, new, label):
    assert old in s, 'patch anchor missing: ' + label
    return s.replace(old, new, 1)


def rrep(s, pat, new, label):
    out, n = re.subn(pat, lambda m: new, s, count=1, flags=re.S)
    assert n == 1, 'patch pattern missing: ' + label
    return out


tail = rep(tail, "kinds: ['concept', 'derivation', 'code']", "kinds: ['concept', 'calc']", 'defaults')
tail = rep(tail, "if (F.v !== 2) { F.kinds = defaults.kinds.slice(); F.v = 2 }", "if (F.v !== 3) { F.kinds = defaults.kinds.slice(); F.v = 3 }", 'migration')
tail = rep(tail, "session = {mode, ids, order, idx: 0, ans: {}, title,", "session = {mode, ids, order, idx: 0, ans: {}, chk: {}, title,", 'session')
tail = rrep(tail, r"function choose\(i\) \{.*?\n\}\nfunction move\(delta\)", r"""function choose(i) {
  const s = session, id = s.ids[s.idx], q = Q.get(id);
  if (s.done) return;
  if (isMulti(q)) {
    if (s.mode !== 'mock' && s.chk && s.chk[id]) return;
    const a = Array.isArray(s.ans[id]) ? s.ans[id].slice() : [], k = a.indexOf(i);
    if (k >= 0) a.splice(k, 1); else a.push(i);
    s.ans[id] = a; saveSession(); render(); return;
  }
  if (s.mode === 'mock') { s.ans[id] = i; saveSession(); render(); return }
  if (s.ans[id] !== undefined) return;
  s.ans[id] = i; record(id, q.o[i].ok === 1); save(); saveSession(); render();
}
function checkMulti() {
  const s = session, id = s.ids[s.idx];
  if (s.done || s.mode === 'mock' || !Array.isArray(s.ans[id]) || !s.ans[id].length || (s.chk && s.chk[id])) return;
  s.chk = s.chk || {}; s.chk[id] = 1;
  record(id, isRight(s, id)); save(); saveSession(); render();
}
function startExamMock() {
  const picked = shuffle(unitIds('EX')).slice(0, 26);
  if (!picked.length) return;
  newSession('mock', picked, `Exam-style mock, ${picked.length} questions`, 78 * 60);
}
function move(delta)""", 'choose')
tail = rep(tail, "s.ids.forEach((id, i) => { if (s.ans[id] !== undefined) record(id, Q.get(id).o[s.ans[id]].ok === 1, now + i) });",
           "s.ids.forEach((id, i) => { if (hasAns(s, id)) record(id, isRight(s, id), now + i) });", 'finish')
tail = rep(tail, "const isRight = (s, id) => s.ans[id] !== undefined && Q.get(id).o[s.ans[id]].ok === 1;",
           """const isMulti = q => q.m === 1 || q.o.filter(o => o.ok).length > 1;
const hasAns = (s, id) => Array.isArray(s.ans[id]) ? s.ans[id].length > 0 : s.ans[id] !== undefined;
const isRight = (s, id) => {
  const q = Q.get(id), a = s.ans[id];
  if (a === undefined) return false;
  if (isMulti(q)) return Array.isArray(a) && q.o.every((o, i) => (o.ok === 1) === a.includes(i));
  return q.o[a].ok === 1;
};""", 'isRight')
# quiz view
tail = rep(tail, "ord = s.order[id], ch = s.ans[id];", "ord = s.order[id], ch = s.ans[id], multi = isMulti(q), sel = multi && Array.isArray(ch) ? ch : [];", 'vQuiz vars')
tail = rep(tail, "const reveal = review || (!mock && ch !== undefined);", "const reveal = review || (!mock && (multi ? !!(s.chk && s.chk[id]) : ch !== undefined));", 'vQuiz reveal')
tail = rep(tail, "const answered = Object.keys(s.ans).length;", "const answered = s.ids.filter(x => hasAns(s, x)).length;", 'vQuiz answered')
tail = rep(tail, "const o = q.o[oi], chosen = ch === oi;", "const o = q.o[oi], chosen = multi ? sel.includes(oi) : ch === oi;", 'vQuiz chosen')
tail = rep(tail, "const tag = o.ok ? (chosen ? 'Correct, your answer' : 'Correct answer') : (chosen ? 'Your answer, incorrect' : 'Why not this one');",
           "const tag = o.ok ? (chosen ? (multi ? 'Correct, you selected it' : 'Correct, your answer') : (multi ? 'Correct, but you missed it' : 'Correct answer')) : (chosen ? 'Your answer, incorrect' : (multi ? 'Rightly left out' : 'Why not this one'));", 'vQuiz tag')
tail = rep(tail, 'return `<button class="${cls}" data-act="choose" data-i="${oi}" aria-pressed="${chosen}">', 'return `<button class="${cls}${multi ? \' multi\' : \'\'}" data-act="choose" data-i="${oi}" aria-pressed="${chosen}">', 'vQuiz button')
tail = rep(tail, '<div class="opts">${opts}</div>${solution}',
           """${multi && !reveal ? '<p class="small muted" style="margin:0">Select one or more, then check.</p>' : ''}<div class="opts">${opts}</div>${multi && !reveal && !mock ? `<div class="row end"><button class="btn primary" data-act="check-multi" ${sel.length ? '' : 'disabled'}>Check answer</button></div>` : ''}${solution}""", 'vQuiz opts')
tail = rep(tail, "s.ans[x] !== undefined ? 'done' : ''", "hasAns(s, x) ? 'done' : ''", 'palette')
tail = rep(tail, "tried = s.ids.filter(id => s.ans[id] !== undefined).length;", "tried = s.ids.filter(id => hasAns(s, id)).length;", 'results')
tail = rep(tail, "if (s.done || s.mode === 'mock' || s.ans[id] !== undefined) move(1);",
           "if (s.done || s.mode === 'mock' || (isMulti(Q.get(id)) ? !!(s.chk && s.chk[id]) : s.ans[id] !== undefined)) move(1); else if (isMulti(Q.get(id))) checkMulti();", 'keydown')
tail = rep(tail, "case 'choose': choose(+d.i); break;",
           """case 'choose': choose(+d.i); break;
    case 'check-multi': checkMulti(); break;
    case 'kind-toggle': { const i = F.kinds.indexOf(d.k); if (i >= 0) F.kinds.splice(i, 1); else F.kinds.push(d.k); LS.set('filter', F); render(); break }
    case 'ex-practice': newSession('practice', pick(unitIds('EX').filter(kindOk), 20), 'Exam-style practice'); break;
    case 'ex-mock': startExamMock(); break;""", 'click cases')
tail = rep(tail, "if (Object.keys(session.ans).length < session.ids.length)", "if (session.ids.filter(x => hasAns(session, x)).length < session.ids.length)", 'submit')
# home
tail = rrep(tail, r'<div class="actions">.*?(?=\n  \$\{lossCurve\(\)\})', """<div class="actions">
    <button class="act primary" data-act="ex-practice"><b>Exam-style practice</b><span>20 questions in the style of the practice exam</span></button>
    <button class="act" data-act="tab" data-v="mock"><b>Mock exam</b><span>Exam-style or all topics, timed</span></button>
    <button class="act" data-act="smart"><b>Smart practice</b><span>20 questions from every topic, mistakes first</span></button>
    <button class="act" data-act="set-wrong" ${wrong.length ? '' : 'disabled'}><b>Fix mistakes</b><span>${wrong.length} wrong on latest try</span></button>
    <button class="act" data-act="unit" data-u="EX"><b>Exam toolkit</b><span>Calculator recipes for each question type</span></button>
    <button class="act" data-act="set-flag" ${fl.length ? '' : 'disabled'}><b>Flagged</b><span>${fl.length} saved for later</span></button>
  </div>
  <button class="act" data-act="unit" data-u="MAP"><b>Course map</b><span>How every topic and method connects</span></button>
  <div class="row"><button class="chip" data-act="kind-toggle" data-k="derivation" aria-pressed="${F.kinds.includes('derivation')}">Include derivations</button><button class="chip" data-act="kind-toggle" data-k="code" aria-pressed="${F.kinds.includes('code')}">Include code questions</button></div>
  <p class="small muted" style="margin:0">The exam is calculation and theory with no coding, so derivation and code questions stay hidden from quizzes unless you switch them on.</p>""", 'home')
# mock screen
tail = rep(tail, '<h1 style="font-size:28px;font-weight:800">Mock exam</h1>',
           """<h1 style="font-size:28px;font-weight:800">Mock exam</h1>
  <button class="act primary" data-act="ex-mock" style="text-align:left;width:100%;white-space:normal"><b>Exam-style mock</b><span>26 questions in 78 minutes, like the practice exam. The length and time are my estimate from the screenshots.</span></button>
  <p class="small muted" style="margin:0">Or build a longer mock from every topic:</p>""", 'mock heading')
tail = rrep(tail, r'<div class="row"><button class="chip" data-act="calc-toggle" aria-pressed="\$\{F\.kinds\.includes\(\'calc\'\)\}">Include calculation questions</button></div>\n  <fieldset>',
            """<div class="row"><button class="chip" data-act="kind-toggle" data-k="derivation" aria-pressed="${F.kinds.includes('derivation')}">Include derivations</button><button class="chip" data-act="kind-toggle" data-k="code" aria-pressed="${F.kinds.includes('code')}">Include code questions</button></div>
  <fieldset>""", 'mock chips')
tail = rrep(tail, r'function vNotes\(\) \{.*?\n\}\nfunction vReader\(\)', r"""function vNotes() {
  const row = u => `<button class="unit" data-act="unit" data-u="${u.id}"><span class="code">${esc(u.code)}</span><span class="name">${esc(u.title)}</span><span class="cnt">${u.mins} min read</span></button>`;
  const start = D.units.filter(u => u.id === 'EX' || u.id === 'MAP'), weeks = D.units.filter(u => u.id !== 'EX' && u.id !== 'MAP');
  return `<div class="wrap"><h1 style="font-size:28px;font-weight:800">Study notes</h1>
  <section style="display:grid;gap:6px"><h2 class="sec-title">Start here</h2>
  <p class="muted small" style="margin:0">The exam is calculation and theory with no coding. The toolkit is the short guide built around its question types, and the course map shows how the topics connect.</p>
  <div class="units">${start.map(row).join('')}</div></section>
  <section style="display:grid;gap:6px"><h2 class="sec-title">Full notes by week</h2>
  <p class="muted small" style="margin:0">The complete reference, in lecture order, with every formula. Page references such as W4 p.37 are PDF page numbers in that week's slides.</p>
  <div class="units">${weeks.map(row).join('')}</div></section></div>`;
}
function vReader()""", 'notes screen')
head = rep(head, '</style>\n<nav id="tabs"', '.opt.multi .l { border-radius: 6px }\n</style>\n<nav id="tabs"', 'css')

data = json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
page = head + '<script id="data" type="application/json">' + data + '</script>' + tail
os.makedirs(SP + '/out', exist_ok=True)
open(SP + '/out/COMP9417_Exam_Drill.html', 'w', encoding='utf8').write(page)
body = page.split('<body style="margin:0">', 1)[1].rsplit('</body></html>', 1)[0]
open(SP + '/out/index.html', 'w', encoding='utf8').write(body)
print(len(D['units']), 'units', len(D['qs']), 'questions', nq, 'exam-style', f'{len(page) / 1e6:.2f} MB')
