#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
表格融合工具：
  1) 解析表格（支持 \multicolumn 分组、注释行）
  2) 按 backbone 分组合并 UPA 表的行
  3) 重算每列的 \textbf（全局最优）/ \underline（次优）
  4) 输出新的 tabular 行序列
"""
import io, re


def _clean(c):
    """去掉强调标记，得到裸数值文本"""
    c = c.strip()
    prev = None
    while prev != c:
        prev = c
        c = re.sub(r'\\textbf\{([^}]*)\}', r'\1', c)
        c = re.sub(r'\\underline\{([^}]*)\}', r'\1', c)
    return c


def _num(c):
    c = _clean(c)
    c = c.replace('\\', '').replace(' ', '')
    try:
        return float(c)
    except ValueError:
        return None


class Row:
    __slots__ = ('group', 'name', 'cells', 'kind')

    def __init__(self, group, name, cells, kind='data'):
        self.group = group
        self.name = name
        self.cells = cells      # list[str]，不含方法名与 SF 标记
        self.kind = kind        # 'data' | 'group' | 'rule'


def parse_table(lines, a, b):
    """解析 [a,b] 行（1-indexed 闭区间）内的表格数据"""
    rows = []
    cur_group = None
    for i in range(a - 1, b):
        raw = lines[i]
        s = raw.strip()
        commented = s.startswith('%')
        if commented:
            s = s.lstrip('%').strip()
        if not s:
            continue
        # 分组标题
        m = re.search(r'\\multicolumn\{[^}]*\}\{c\}\{\\textit\{([^}]*)\}\}', s)
        if m:
            cur_group = m.group(1)
            rows.append(Row(cur_group, None, [], 'group'))
            continue
        if s.startswith('\\toprule') or s.startswith('\\midrule') or s.startswith('\\bottomrule'):
            rows.append(Row(cur_group, None, [], 'rule'))
            continue
        if '&' not in s:
            continue
        body = s.rstrip()
        if body.endswith('\\\\'):
            body = body[:-2]
        elif body.endswith('\\'):
            body = body[:-1]
        cells = [c.strip() for c in body.split('&')]
        if len(cells) < 2:
            continue
        name = re.sub(r'\\cite\{[^}]*\}', '', cells[0])
        name = re.sub(r'\\textbf\{([^}]*)\}', r'\1', name)
        name = name.replace('~', '').replace('\\dagger', '').replace('$', '').strip()
        name = name.replace('\\checkmark', '').replace('\\ding{55}', '').strip()
        if name in ('Method', '方法', ''):
            continue
        vals = cells[2:]     # 跳过方法名与 SF 标记
        rows.append(Row(cur_group, name, vals, 'data'))
    return rows


def row_with_sf(orig_line):
    """从原始行文本重建 'name & sf & vals' 的完整形式（保留 \checkmark/\ding）"""
    s = orig_line.strip()
    body = s.rstrip()
    if body.endswith('\\\\'):
        body = body[:-2]
    elif body.endswith('\\'):
        body = body[:-1]
    return body


def recompute_marks(rows, name_col=0):
    """按「全局最优 = \\textbf，次优 = \\underline」重算每列标记。
    只处理数值列，SF 列与 '-' 跳过。"""
    data = [r for r in rows if r.kind == 'data']
    ncol = max(len(r.cells) for r in data)
    for ci in range(ncol):
        col = []
        for r in data:
            if ci < len(r.cells):
                v = _num(r.cells[ci])
                if v is not None:
                    col.append((v, r))
        if not col:
            continue
        mx = max(v for v, _ in col)
        best = [r for v, r in col if v == mx]
        rest = [(v, r) for v, r in col if v < mx]
        s2 = max(v for v, _ in rest) if rest else None
        second = [r for v, r in rest if v == s2] if s2 is not None else []
        # 先清除该列所有标记
        for r in data:
            if ci < len(r.cells):
                r.cells[ci] = re.sub(r'\\textbf\{([^}]*)\}', r'\1', r.cells[ci])
                r.cells[ci] = re.sub(r'\\underline\{([^}]*)\}', r'\1', r.cells[ci])
        for r in best:
            c = _clean(r.cells[ci])
            if c.replace('\\', '') != '-':
                r.cells[ci] = '\\textbf{%s}' % c
        for r in second:
            if r in best:
                continue
            c = _clean(r.cells[ci])
            if c.replace('\\', '') != '-':
                r.cells[ci] = '\\underline{%s}' % c
    return rows
