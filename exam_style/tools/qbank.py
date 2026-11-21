"""Parser + linter for the COMP9417 question-bank text format (multi-select aware).
Usage: python qbank.py lint <file.txt>"""
import re, sys, hashlib, collections

KINDS = {'concept', 'calc', 'code', 'derivation'}
BANNED = re.compile(r"\b(all|none) of the (above|others|these|options)\b|\bboth (of the )?(above|[A-E]\b)|\b(option|answer|choice) [A-E]\b|\b[A-E] and [A-E]\b", re.I)


def parse(path):
    text = open(path, encoding='utf8').read().replace('\r\n', '\n')
    blocks = re.split(r'^=== Q[ \t]*$', text, flags=re.M)
    qs, errs = [], []
    if blocks[0].strip():
        errs.append('text before first "=== Q"')
    for n, b in enumerate(blocks[1:], 1):
        q = {'n': n, 'options': [], 'code': None, 'explain': None, 'stem': None}
        parts = re.split(r'^--- ?([A-Ea-z]+\*?)[ \t]*$', b, flags=re.M)
        for line in parts[0].strip().split('\n'):
            m = re.match(r'(topic|kind|diff|source|multi):\s*(.+)', line.strip())
            if m:
                q[m.group(1)] = m.group(2).strip()
            elif line.strip():
                errs.append(f'Q{n}: bad header line {line!r}')
        for tag, body in zip(parts[1::2], parts[2::2]):
            body = body.strip('\n')
            t = tag.rstrip('*')
            if t in ('stem', 'code', 'explain'):
                q[t] = body.rstrip() if t == 'code' else body.strip()
            elif re.fullmatch(r'[A-E]', t):
                sp = re.split(r'^>>[ \t]?', body, maxsplit=1, flags=re.M)
                q['options'].append({'text': sp[0].strip(), 'why': sp[1].strip() if len(sp) > 1 else '', 'ok': tag.endswith('*')})
            else:
                errs.append(f'Q{n}: unknown section --- {tag}')
        qs.append(q)
    return qs, errs


def qid(unit, q):
    return unit + '-' + hashlib.sha1((q.get('stem') or '').encode()).hexdigest()[:7]


def lint(path):
    qs, errs = parse(path)
    longest = 0
    seen = {}
    for q in qs:
        n = q['n']
        for k in ('topic', 'kind', 'diff', 'source', 'stem'):
            if not q.get(k):
                errs.append(f'Q{n}: missing {k}')
        if q.get('kind') not in KINDS:
            errs.append(f'Q{n}: kind must be one of {sorted(KINDS)}')
        if q.get('diff') not in ('1', '2', '3'):
            errs.append(f'Q{n}: diff must be 1/2/3')
        o = q['options']
        if not 4 <= len(o) <= 5:
            errs.append(f'Q{n}: needs 4-5 options, has {len(o)}')
        nok = sum(x['ok'] for x in o)
        if nok < 1:
            errs.append(f'Q{n}: must have at least one correct option (marked *)')
        elif nok > 1:
            if not re.search(r'one or more|more than one|all that apply|all (of )?the (correct|true)', q.get('stem') or '', re.I):
                errs.append(f'Q{n}: has {nok} correct options but the stem does not say "Select one or more"')
            if nok == len(o):
                errs.append(f'Q{n}: every option is correct, which is too easy to guess')
        elif re.search(r'one or more|more than one|all that apply', q.get('stem') or '', re.I) and q.get('multi') != 'yes':
            errs.append(f'Q{n}: stem says select one or more but only one option is marked correct (add the header "multi: yes" if the exam really shows checkboxes)')
        if q.get('multi') == 'yes' and not re.search(r'one or more|more than one|all that apply', q.get('stem') or '', re.I):
            errs.append(f'Q{n}: multi: yes needs the stem to say "Select one or more"')
        if len({x['text'] for x in o}) != len(o):
            errs.append(f'Q{n}: duplicate option text')
        for x in o:
            if len(x['why']) < 25:
                errs.append(f'Q{n}: option {x["text"][:30]!r} needs a real ">> why" explanation')
            if not x['text']:
                errs.append(f'Q{n}: empty option text')
            if BANNED.search(x['text']) or BANNED.search(x['why']):
                errs.append(f'Q{n}: option/why refers to other options by position or uses all/none-of-the-above (options are shuffled): {x["text"][:40]!r}')
        if q.get('kind') in ('calc', 'derivation', 'code') and not q.get('explain'):
            errs.append(f'Q{n}: {q.get("kind")} question needs --- explain with worked solution')
        fields = [('stem', q.get('stem')), ('explain', q.get('explain'))]
        fields += [('option', x['text']) for x in o] + [('why', x['why']) for x in o]
        for f, s in fields:
            if s and s.replace('\\$', '').replace('$$', '').count('$') % 2:
                errs.append(f'Q{n}: unbalanced $ in {f}')
            if s and re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', s):
                errs.append(f'Q{n}: control character in {f} (a backslash was damaged)')
        s = q.get('stem') or ''
        if s in seen:
            errs.append(f'Q{n}: duplicate stem of Q{seen[s]}')
        seen[s] = n
        if o and nok == 1 and max(o, key=lambda x: len(x['text']))['ok']:
            longest += 1
    return qs, errs, longest


if __name__ == '__main__':
    qs, errs, longest = lint(sys.argv[2])
    nm = sum(1 for q in qs if sum(x['ok'] for x in q['options']) > 1)
    print(f'{len(qs)} questions, {nm} select-one-or-more')
    print('kinds:', dict(collections.Counter(q.get('kind') for q in qs)))
    print('difficulty:', dict(sorted(collections.Counter(str(q.get('diff')) for q in qs).items())))
    print('topics:', dict(collections.Counter(q.get('topic') for q in qs)))
    single = sum(1 for q in qs if sum(x['ok'] for x in q['options']) == 1)
    if single:
        print(f'correct option is the longest in {100*longest/single:.0f}% of single-answer questions (aim for under 40%)')
    print(f'{len(errs)} problems')
    for e in errs:
        print('  ', e)
    sys.exit(1 if errs else 0)
