import re, glob

files = sorted(glob.glob('body/*.tex') + glob.glob('back/*.tex') + glob.glob('front/*.tex'))
print("=== 正文叙述段中的 \\textbf（排除：段首提纲/列表项/表格单元格/伪代码）===")
viol = 0
for f in files:
    lines = open(f, encoding='utf-8').readlines()
    in_list = False
    in_table = False
    in_alg = False
    for ln, line in enumerate(lines, 1):
        st = line.strip()
        if st.startswith('%'):
            continue
        for env in ('itemize', 'enumerate', 'description', 'publist'):
            if '\\begin{%s}' % env in st:
                in_list = True
            if '\\end{%s}' % env in st:
                in_list = False
        if '\\begin{table' in st or '\\begin{tabular' in st or '\\begin{longtable' in st:
            in_table = True
        if '\\end{table' in st or '\\end{tabular}' in st or '\\end{longtable}' in st:
            in_table = False
        if '\\begin{algorithm}' in st:
            in_alg = True
        if '\\end{algorithm}' in st:
            in_alg = False
        if in_list or in_table or in_alg:
            continue
        if '\\textbf{' not in line:
            continue
        if re.match(r'^\s*(\\noindent\s*)?\\textbf\{', line):
            continue
        if '\\For{' in line or '\\If{' in line or '\\ForEach{' in line:
            continue
        print('  %s:%d %s' % (f, ln, st[:140]))
        viol += 1
print('正文 \\textbf 违例: %d' % viol)