import re, glob, os

ABB = ['SFDA', 'SFUDA', 'UDA', 'SFADA', 'OSDA', 'OSSFADA', 'OVS', 'OVD', 'OVR',
       'UPA', 'SfMamba', 'APS', 'CACL', 'SCS', 'Ch-VSS', 'DAMF', 'DFSelector',
       'APT', 'ADL', 'CMPF', 'AER-Bench', 'Mamba', 'CLIP', 'SAM', 'ViL', 'MLLM',
       'IM', 'PQ', 'HOS', 'VAD', 'NDCG', 'Ap']

files = sorted(glob.glob('body/*.tex') + glob.glob('back/*.tex') + glob.glob('front/*.tex') +
               glob.glob('extras/optional-back/*.tex'))
alltext = ''
for f in files:
    alltext += open(f, encoding='utf-8').read()

print('=== 缩写展开检查（全称（缩写）形式）===')
for a in ABB:
    # 展开形式：全称（ABBR） 或 全称 (ABBR)
    exp = len(re.findall(r'[（(]\s*%s\s*[)）]' % re.escape(a), alltext))
    uses = len(re.findall(r'(?<![A-Za-z])%s(?![A-Za-z])' % re.escape(a), alltext))
    if uses == 0:
        print('  %-12s 未使用' % a)
        continue
    status = 'OK' if exp > 0 else '!! 未展开'
    print('  %-12s 出现 %3d 次, 展开 %d 处  %s' % (a, uses, exp, status))

print()
print('=== 本章工作归纳（引言节末段）===')
for f in sorted(glob.glob('body/*.tex')):
    s = open(f, encoding='utf-8').read()
    m = re.search(r'\\section\{引言\}', s)
    if not m:
        print('  %s: 无引言节' % f)
        continue
    seg = s[m.end():]
    # 找到引言节结束（下一个 \section）
    nxt = re.search(r'\\section\{', seg)
    intro = seg[:nxt.start()] if nxt else seg
    items = re.findall(r'\\item', intro)
    last_part = intro[-1500:]
    has_list = r'\begin{enumerate}' in last_part or r'\begin{itemize}' in last_part
    # 检查列表内是否有 \textbf
    tb = 0
    for mm in re.finditer(r'\\begin\{(enumerate|itemize)\}(.*?)\\end\{\1\}', last_part, re.S):
        tb += mm.group(2).count('\\textbf{')
    roadmap = re.search(r'(组织如下|安排如下|结构如下|内容如下|共分\s*\d+\s*节)', intro)
    print('  %-22s item数=%d, 末段有列表=%s, 列点内\\textbf=%d, 导览段=%s'
          % (f, len(items), has_list, tb, '有(!!)' if roadmap else '无'))