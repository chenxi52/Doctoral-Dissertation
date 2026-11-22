#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
重算表格中每列的 \textbf（全局最优）与 \underline（次优）标记。

规则：
  * 只统计**实际渲染的行**（以 % 开头的注释行不参与，也不改写）。
  * \textbf → 该列全局最优值
  * \underline → 该列次优值（并列次优全部标注）
  * 值为 '-' / '-' 的列跳过
  * 非数值列（SF 标记列、方法名列）跳过

用法：python3 recompute_marks.py body/chap2_merge.tex
"""
import io, re, sys

PATH = sys.argv[1] if len(sys.argv) > 1 else 'body/chap2_merge.tex'

with io.open(PATH, encoding='utf-8') as f:
    lines = f.readlines()


def strip_mark(c):
    prev = None
    while prev != c:
        prev = c
        c = re.sub(r'\\textbf\{([^}]*)\}', r'\1', c)
        c = re.sub(r'\\underline\{([^}]*)\}', r'\1', c)
    return c


def to_num(c):
    c = strip_mark(c).replace('\\', '').replace(' ', '').strip()
    if c in ('-', '', '--'):
        return None
    try:
        return float(c)
    except ValueError:
        return None


def is_data_row(s):
    if s.startswith('%'):
        return False
    if '&' not in s:
        return False
    if s.startswith('\\midrule') or s.startswith('\\toprule') or s.startswith('\\bottomrule'):
        return False
    if 'multicolumn' in s:
        return False
    return True


def process_table(a, b, tname):
    """处理 [a,b] 行（1-indexed 闭区间）内的表格"""
    data = []          # (line_index, cells)
    for i in range(a - 1, min(b, len(lines))):
        s = lines[i].strip()
        if not is_data_row(s):
            continue
        body = s.rstrip()
        if body.endswith('\\\\'):
            body = body[:-2]
        elif body.endswith('\\'):
            body = body[:-1]
        cells = [c.strip() for c in body.split('&')]
        if len(cells) < 3:
            continue
        # 方法名行（表头）跳过
        nm = re.sub(r'\\cite\{[^}]*\}', '', cells[0])
        nm = re.sub(r'\\multirow\{[^}]*\}\{\*\}\{([^}]*)\}', r'\1', nm)
        nm = nm.replace('~', '').replace('\\dagger', '').replace('$', '').strip()
        if nm in ('Method', '方法', ''):
            continue
        data.append((i, cells))

    if not data:
        return 0

    ncol = max(len(c) for _, c in data)
    changed = 0
    for ci in range(2, ncol):     # 跳过方法名列(0)与 SF 列(1)
        col = []
        for i, cells in data:
            if ci < len(cells):
                v = to_num(cells[ci])
                if v is not None:
                    col.append((v, i))
        if not col:
            continue
        mx = max(v for v, _ in col)
        best_idx = {i for v, i in col if v == mx}
        rest = [(v, i) for v, i in col if v < mx]
        s2 = max(v for v, _ in rest) if rest else None
        second_idx = {i for v, i in rest if v == s2} if s2 is not None else set()

        for i, cells in data:
            if ci >= len(cells):
                continue
            old = cells[ci]
            new = re.sub(r'\\textbf\{([^}]*)\}', r'\1', old)
            new = re.sub(r'\\underline\{([^}]*)\}', r'\1', new)
            bare = strip_mark(new)
            # 并列最优全部加粗；次优（并列也全部）用下划线
            if i in best_idx:
                new = '\\textbf{%s}' % bare
            elif i in second_idx:
                new = '\\underline{%s}' % bare
            else:
                new = bare
            if new != old:
                cells[ci] = new
                changed += 1
                # 回写到原行
                body = ' & '.join(cells) + ' \\\\'
                lines[i] = '  ' + body + '\n'
    print(f'  {tname}: {len(data)} 行, 修改 {changed} 处标记')
    return changed


SKIP_LABELS = {'table:Visda-C'}   # 未改动行内容的表，保持原标注
# 仅重算「行内容被改动过」的融合主表；其余表保持原文件标注不动
ONLY_LABELS = {'tab:main_oh_visda', 'tab:main_office', 'tab:main_dn126'}


def find_tables():
    """找出所有 table 环境，返回 [(起始行, 结束行, caption_label)]"""
    tabs = []
    i = 0
    while i < len(lines):
        if re.match(r'\s*\\begin\{table\*?\}', lines[i]):
            start = i
            label = None
            j = i
            while j < len(lines):
                m = re.search(r'\\bicaption\[([^\]]+)\]', lines[j])
                if m:
                    label = m.group(1)
                    break
                j += 1
            k = i
            depth = 0
            while k < len(lines):
                if re.match(r'\s*\\begin\{table\*?\}', lines[k]):
                    depth += 1
                if re.match(r'\s*\\end\{table\*?\}', lines[k]):
                    depth -= 1
                    if depth == 0:
                        break
                k += 1
            tabs.append((start + 1, k + 1, label or '(无label)'))
            i = k
        i += 1
    return tabs


print(f'重算标记: {PATH}')
total = 0
for a, b, lab in find_tables():
    if lab in SKIP_LABELS:
        print(f'  {lab}: 跳过（未改动行内容）')
        continue
    if lab not in ONLY_LABELS:
        print(f'  {lab}: 跳过（非融合主表）')
        continue
    total += process_table(a, b, lab)

with io.open(PATH, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print(f'合计修改 {total} 处')
