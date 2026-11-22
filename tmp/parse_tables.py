#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析 chap2 各表的数据行，供融合建表使用。"""
import io, re

TXT = io.open('body/chap2.tex', encoding='utf-8').read().split('\n')

def rows(a, b):
    """列出 [a,b] 行中的表格数据行（以 & 结尾的行）"""
    out = []
    for i in range(a-1, b):
        s = TXT[i]
        st = s.strip()
        if not st: continue
        if st.startswith('%'): continue
        if st.startswith('\\multicolumn') or st.startswith('\\midrule') or \
           st.startswith('\\toprule') or st.startswith('\\bottomrule') or \
           st.startswith('\\hline'):
            out.append((i+1, 'GROUP', st))
        elif '&' in st and st.endswith('\\\\'):
            out.append((i+1, 'ROW', st))
    return out

def show(name, a, b):
    print('\n' + '='*20, name, f'(lines {a}-{b})', '='*20)
    for ln, kind, s in rows(a, b):
        tag = 'GRP' if kind=='GROUP' else '   '
        print(f'{ln:4d} {tag} {s[:150]}')

show('UPA Office-Home', 215, 239)
show('UPA Office', 248, 276)
show('UPA DomainNet-126', 287, 300)
show('UPA VisDA-C', 176, 203)
