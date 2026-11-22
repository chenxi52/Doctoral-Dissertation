import re, glob

ABB = ['SFDA', 'SFUDA', 'UDA', 'SFADA', 'OSDA', 'OSSFADA', 'OVS', 'OVD', 'OVR',
       'UPA', 'SfMamba', 'APS', 'CACL', 'SCS', 'Ch-VSS', 'DAMF', 'DFSelector',
       'APT', 'ADL', 'CMPF', 'AER-Bench', 'Mamba', 'CLIP', 'SAM', 'ViL', 'MLLM',
       'IM', 'PQ', 'HOS', 'VAD', 'NDCG', 'TSM', 'AP']

files = sorted(glob.glob('body/*.tex') + glob.glob('back/*.tex') + glob.glob('front/*.tex') +
               glob.glob('extras/optional-back/*.tex'))
alltext = ''
for f in files:
    alltext += open(f, encoding='utf-8').read()

print('=== 缩写展开检查（括号内以缩写结尾的形式）===')
for a in ABB:
    exp = len(re.findall(r'[（(][^（()）]{0,120}?\b%s\b[^（()）]{0,20}?[)）]' % re.escape(a), alltext))
    uses = len(re.findall(r'(?<![A-Za-z])%s(?![A-Za-z])' % re.escape(a), alltext))
    if uses == 0:
        print('  %-12s 未使用' % a)
        continue
    status = 'OK' if exp > 0 else '!! 未展开'
    print('  %-12s 出现 %3d 次, 展开 %d 处  %s' % (a, uses, exp, status))