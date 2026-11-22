import re, glob

files = sorted(glob.glob('body/*.tex') + glob.glob('back/*.tex') + glob.glob('front/*.tex') + glob.glob('thesis.tex'))

print("=== 公式衔接检查（逗号+空行 / 句号+不空行）===")
viol = 0
for f in files:
    lines = open(f, encoding='utf-8').readlines()
    for ln, line in enumerate(lines):
        if not re.match(r'^\s*\\end\{(equation|align\*?|eqnarray\*?)\}', line):
            continue
        # find last content line of the env
        j = ln - 1
        while j >= 0 and (not lines[j].strip() or lines[j].strip().startswith('%')):
            j -= 1
        if j < 0:
            continue
        last = lines[j].rstrip()
        if not last or last.strip().startswith('%'):
            continue
        ends_comma = last.rstrip().endswith((',', '，'))
        ends_period = last.rstrip().endswith(('.', '。'))
        # is there a blank line after env end?
        k = ln + 1
        blank = False
        while k < len(lines) and lines[k].strip().startswith('%'):
            k += 1
        if k < len(lines) and not lines[k].strip():
            blank = True
        if ends_comma and blank:
            print(f'  {f}:{ln+1} 公式末逗号 + 空行  -> {last.strip()[-40:]}')
            viol += 1
        if ends_period and not blank:
            print(f'  {f}:{ln+1} 公式末句号 + 无空行 -> {last.strip()[-40:]}')
            viol += 1
print(f'公式衔接违例: {viol}')

print()
print("=== 括号密度（正文叙述段）===")
for f in sorted(glob.glob('body/*.tex') + glob.glob('back/*.tex') + glob.glob('front/*.tex')):
    s = open(f, encoding='utf-8').read()
    p = s.count('（') + s.count('(') + s.count('）') + s.count(')')
    c = len(s)
    d = p / c * 50 if c else 0
    flag = '  <-- 需排查' if d > 1.0 else ('  (抽查)' if d > 0.5 else '')
    print(f'  {f}: {p} 处, 密度 {d:.3f}/50字{flag}')
