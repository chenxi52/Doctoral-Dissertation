#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析 UPA 四张表 vs SfMamba 三张表的方法集合差异，
为融合决策提供依据：哪些行已在 SfMamba 表中、哪些需要补入。
"""
import io, re

TXT = io.open('body/chap2.tex', encoding='utf-8').read().split('\n')

def name_of(line):
    """从数据行提取方法名（去掉 cite 与 bold）"""
    s = line.strip()
    if not s or s.startswith('%') or s.startswith('\\multicolumn'):
        return None
    if '&' not in s:
        return None
    first = s.split('&')[0].strip()
    first = re.sub(r'\\cite\{[^}]*\}', '', first)
    first = re.sub(r'\\textbf\{([^}]*)\}', r'\1', first)
    first = re.sub(r'\$[^$]*\$', '', first).strip()
    first = first.replace('~', '').replace('\\dagger', '').strip()
    return first

def collect(a, b, groups=()):
    """收集区间内的 (组名, 方法名)"""
    cur = None
    out = []
    for i in range(a-1, b):
        s = TXT[i].strip()
        if s.startswith('\\multicolumn') and 'textit' in s:
            m = re.search(r'\\textit\{([^}]*)\}', s)
            cur = m.group(1) if m else cur
            continue
        n = name_of(s)
        if n:
            out.append((cur, n, i+1))
    return out

print('#### UPA Office-Home (215-239) ####')
upa_oh = collect(215, 239)
for g,n,l in upa_oh: print(f'  {l:4d} [{g}] {n}')

print('\n#### SfMamba OH+VisDA (565-613) ####')
sf_oh = collect(565, 613)
for g,n,l in sf_oh: print(f'  {l:4d} [{g}] {n}')

upa_oh_names = {n for _,n,_ in upa_oh}
sf_oh_names  = {n for _,n,_ in sf_oh}
print('\n>>> UPA-OH 有、SF-OH 无（可补入）:', sorted(upa_oh_names - sf_oh_names))
print('>>> SF-OH 有、UPA-OH 无（保留）      :', sorted(sf_oh_names - upa_oh_names))

print('\n#### UPA Office (248-276) ####')
upa_off = collect(248, 276)
for g,n,l in upa_off: print(f'  {l:4d} [{g}] {n}')
print('\n#### SfMamba Office (624-669) ####')
sf_off = collect(624, 669)
for g,n,l in sf_off: print(f'  {l:4d} [{g}] {n}')
upa_off_names={n for _,n,_ in upa_off}; sf_off_names={n for _,n,_ in sf_off}
print('\n>>> UPA-Office 有、SF 无:', sorted(upa_off_names - sf_off_names))
print('>>> SF 有、UPA-Office 无:', sorted(sf_off_names - upa_off_names))

print('\n#### UPA DomainNet-126 (287-300) ####')
upa_dn = collect(287, 300)
for g,n,l in upa_dn: print(f'  {l:4d} [{g}] {n}')
print('\n#### SfMamba DN-126 (675-713) ####')
sf_dn = collect(675, 713)
for g,n,l in sf_dn: print(f'  {l:4d} [{g}] {n}')
upa_dn_names={n for _,n,_ in upa_dn}; sf_dn_names={n for _,n,_ in sf_dn}
print('\n>>> UPA-DN 有、SF 无:', sorted(upa_dn_names - sf_dn_names))
print('>>> SF 有、UPA-DN 无:', sorted(sf_dn_names - upa_dn_names))
