"""Blind audit support (multi-select aware).
  python blind.py make <SP> <FILE_STEM>     e.g. EX_bayes -> writes SP/work/audit/EX_bayes.blind.md (no key, options reshuffled) and keys/
  python blind.py compare <SP> <FILE_STEM>  reads SP/work/audit/<STEM>.answers.txt, lines "n LETTER(S) [note]", prints disagreements
"""
import json, os, random, re, sys

SP, UNIT = sys.argv[2], sys.argv[3]
sys.path.insert(0, SP + '/tools')
from qbank import parse

adir = f'{SP}/work/audit'
kdir = adir + '/keys'
os.makedirs(kdir, exist_ok=True)
qpath = f'{SP}/work/questions/{UNIT}.txt'

if sys.argv[1] == 'make':
    qs, errs = parse(qpath)
    rng = random.Random(UNIT)
    key, out = {}, [f'# Blind paper for {UNIT}: {len(qs)} questions\n']
    for q in qs:
        o = q['options'][:]
        rng.shuffle(o)
        key[q['n']] = ''.join('ABCDE'[i] for i, x in enumerate(o) if x['ok'])
        out.append(f"\n## Question {q['n']}  (topic: {q['topic']})\n\n{q['stem']}\n")
        if q['code']:
            out.append(f"\n```python\n{q['code']}\n```\n")
        for i, x in enumerate(o):
            out.append(f"\n{'ABCDE'[i]}. {x['text']}\n")
    open(f'{adir}/{UNIT}.blind.md', 'w', encoding='utf8').write(''.join(out))
    json.dump({'key': key}, open(f'{kdir}/{UNIT}.key.json', 'w', encoding='utf8'))
    print(len(qs), 'questions blinded')
else:
    key = {int(k): v for k, v in json.load(open(f'{kdir}/{UNIT}.key.json', encoding='utf8'))['key'].items()}
    got = {}
    for line in open(f'{adir}/{UNIT}.answers.txt', encoding='utf8'):
        m = re.match(r'\s*(\d+)\s*[:.\-]?\s*([A-E][A-E, ]*?)(?:\s|$)', line)
        if m:
            got[int(m.group(1))] = ''.join(sorted(re.findall('[A-E]', m.group(2))))
    bad = [n for n in sorted(key) if got.get(n) != key[n]]
    print(f'{len(key)} questions, {len(got)} answered, {len(key) - len(bad)} agree')
    for n in bad:
        print(f'  Q{n}: you answered {got.get(n, "nothing")}, key says {key[n]}')
