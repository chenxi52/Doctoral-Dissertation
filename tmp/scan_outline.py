import re, glob
files = sorted(glob.glob('body/*.tex') + glob.glob('back/*.tex') + glob.glob('front/*.tex'))
total = 0
for f in files:
    lines = open(f, encoding='utf-8').readlines()
    for ln, line in enumerate(lines, 1):
        m = re.match(r'^\s*\\textbf\{((?:[^{}]|\{[^}]*\})+)\}', line)
        if not m:
            continue
        inner = m.group(1).strip()
        if not inner:
            continue
        if ln >= 2:
            prev = lines[ln-2].strip()
            is_start = (prev == '') or bool(re.match(r'\\(section|subsection|subsubsection|paragraph|caption)\b', prev))
        else:
            is_start = True
        if not is_start:
            continue
        last = inner[-1]
        if last in ('。', '.') and not (len(inner) >= 2 and inner[-2].isdigit()):
            print(f'{f}:{ln} \\textbf{{{inner}}}')
            total += 1
print(f'总计: {total} 处违例')
