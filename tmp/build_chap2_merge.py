#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chap2_merge.tex 的表格融合后处理脚本（幂等）。

背景
----
``body/chap2_merge.tex`` 的**章节结构与正文**由人工维护（见 handoff.md），
本脚本只负责其中**机械、可验证**的部分：

1. 把 UPA 原稿中已删除的三张独立表的关键基线行，按原数值并入
   SfMamba 的三张主表（按骨干网络分类的 CNN 分组）；
2. 把 VisDA-C 逐类别表中独有的方法，其 Average 结果并入表 2-1 的 VisDA-C 列；
3. 重算三张主表的「并列最优加粗 / 次优下划线」标注。

**不做**任何重新计算或数值杜撰：所有数值一律照抄 ``body/chap2.tex``。
非溯源项仅允许是 ``--`` 占位符（该方法在对应基准上无报告数据）。

结构重构（UPA 独立方法节 → SfMamba 章内 APS 子节、删除 CACL、
新增 Filter×SCS 正交消融实验）已在 ``body/chap2_merge.tex`` 中**手工完成**，
本脚本不参与，故不覆盖它们。

用法
----
    python3 tmp/build_chap2_merge.py            # 就地融合（幂等）
    python3 tmp/build_chap2_merge.py --check    # 只校验数值溯源，不写文件
"""
import io
import re
import sys

DST = 'body/chap2_merge.tex'
SRC = 'body/chap2.tex'

# ---------------------------------------------------------------- 表 2-1 / 2-2 / 2-3 注入行
# UPA 的 Office-Home 表提供、而 SfMamba 主表缺失的关键 SFDA 方法。
# MDD 在 UPA 原表中无 VisDA-C 记录 → 该列填 '--'（不能挪用其它方法的数值）。
OH_NEW = [
    '  CDAN~\\cite{CDAN} & \\ding{55} & 50.7 & 70.6 & 76.0 & 57.6 & 70.0 & 70.0 & 57.4 & 50.9 & 77.3 & 70.9 & 56.7 & 81.6 & 65.8 & 73.9 \\\\',
    '  MDD~\\cite{MDD} & \\ding{55} & 54.9 & 73.7 & 77.8 & 60.0 & 71.4 & 71.8 & 61.2 & 53.6 & 78.1 & 72.5 & 60.2 & 82.3 & 68.1 & -- \\\\',
    '  VDM-DA~\\cite{tian2022vdm} & \\Checkmark & 59.3 & 75.3 & 78.3 & 67.6 & 76.0 & 75.9 & 68.8 & 57.7 & 79.6 & 74.0 & 61.1 & 83.6 & 71.4 & 85.3 \\\\',
    '  D-MCD~\\cite{chu2022denoised} & \\Checkmark & 59.4 & 78.9 & 80.2 & 67.2 & 79.3 & 78.6 & 65.3 & 55.6 & 82.2 & 73.3 & 62.8 & 83.9 & 72.2 & 87.5 \\\\',
    '  DIPE~\\cite{DIPE} & \\Checkmark & 56.5 & 79.2 & 80.7 & 70.1 & 79.8 & 78.8 & 67.9 & 55.1 & 83.5 & 74.1 & 59.3 & 84.8 & 72.5 & 83.1 \\\\',
]
# 从 UPA 的 VisDA-C 逐类别表并入（只取 Average）。
# FixBi / U-SFAN 在 UPA 的 Office-Home 表中也有完整数据 → 整行并入；
# 其余方法仅有 VisDA-C 结果 → Office-Home 各列填 '--'（无记录）。
OH_VISDA_ONLY = [
    '  MCC~\\cite{MCC} & \\ding{55} & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & 78.8 \\\\',
    '  BCDM~\\cite{BCDM} & \\ding{55} & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & 83.4 \\\\',
    '  CAN~\\cite{CAN} & \\ding{55} & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & 87.2 \\\\',
    '  3C-GAN~\\cite{3C-GAN} & \\Checkmark & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & 81.6 \\\\',
    '  HCL~\\cite{HCL} & \\Checkmark & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & 83.5 \\\\',
    '  SSNLL~\\cite{chen2022self} & \\Checkmark & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & 86.0 \\\\',
    '  CDCL~\\cite{wang2022cross} & \\Checkmark & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & 87.5 \\\\',
    '  AdaContrast~\\cite{AdaContrast} & \\Checkmark & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & -- & 86.8 \\\\',
]
OH_FULL_ROWS = [
    '  FixBi~\\cite{FIxBi} & \\ding{55} & 58.1 & 77.3 & 80.4 & 67.7 & 79.5 & 78.1 & 65.8 & 57.9 & 81.7 & 76.4 & 62.9 & 86.7 & 72.7 & 87.2 \\\\',
    '  U-SFAN~\\cite{U-SFAN} & \\Checkmark & 57.8 & 77.8 & 81.6 & 67.9 & 77.3 & 79.2 & 67.2 & 54.7 & 81.2 & 73.3 & 60.3 & 83.9 & 71.9 & 82.7 \\\\',
]

OFF_NEW = [
    '  CDAN~\\cite{CDAN} & \\ding{55} & 92.9 & 94.1 & 71.0 & 98.6 & 69.3 & 100.0 & 87.7 \\\\',
    '  MDD~\\cite{MDD} & \\ding{55} & 93.5 & 94.5 & 74.6 & 98.4 & 72.2 & 100.0 & 88.9 \\\\',
    '  VDM-DA~\\cite{tian2022vdm} & \\Checkmark & 94.1 & 93.2 & 75.8 & 98.0 & 77.1 & 100.0 & 89.7 \\\\',
    '  3C-GAN~\\cite{3C-GAN} & \\Checkmark & 92.7 & 93.7 & 75.3 & 98.5 & 77.8 & 99.8 & 89.6 \\\\',
    '  D-MCD~\\cite{chu2022denoised} & \\Checkmark & 94.1 & 93.5 & 76.4 & 98.8 & 76.4 & 100.0 & 89.9 \\\\',
]

DN_NEW = [
    '  MCC~\\cite{MCC} & \\ding{55} & 44.8 & 65.7 & 41.9 & 34.9 & 47.3 & 35.3 & 72.4 & 48.9 \\\\',
]


# ---------------------------------------------------------------- 工具函数
def inject(lines, anchor, new_rows):
    """在 anchor 所在行之后插入 new_rows。

    幂等：以**方法名**判定是否已存在（而非整行字符串），因为同一方法在表中
    可能出现「脚本注入的无标记副本」与「原表的带标记正式行」两种形态
    （后者由 recompute_marks.py 重新加了粗体/下划线）。
    """
    def mname(row):
        n = re.sub(r'\\cite\{[^}]*\}', '', row.split('&')[0])
        n = re.sub(r'\\textbf\{([^}]*)\}', r'\1', n)
        n = n.replace('~', '').replace(' ', '').strip()
        return n

    existing = {mname(l) for l in lines if '&' in l and not l.strip().startswith('%')}
    todo = [r for r in new_rows if mname(r) not in existing]
    if not todo:
        return lines
    res, done = [], False
    for ln in lines:
        res.append(ln)
        if not done and anchor in ln:
            res.extend(r + '\n' for r in todo)
            done = True
    assert done, 'anchor not found: %r' % anchor
    return res


def uncomment(lines, prefixes):
    """把以给定前缀开头的注释行还原为正式行（幂等）。"""
    out = []
    for ln in lines:
        st = ln.strip()
        for p in prefixes:
            if st.startswith('% ' + p):
                ln = '  ' + st.lstrip('%').strip() + '\n'
                break
        out.append(ln)
    return out


def method_of(cell):
    """从表格首列提取方法名（去 cite / textbf / 下标 / 标记）。"""
    n = re.sub(r'\\cite\{[^}]*\}', '', cell)
    n = re.sub(r'\\textbf\{([^}]*)\}', r'\1', n)
    n = re.sub(r'\\underline\{([^}]*)\}', r'\1', n)
    n = re.sub(r'\\multirow\{[^}]*\}\{\*\}\{([^}]*)\}', r'\1', n)
    n = n.replace('~', '').replace('\\dagger', '').replace('$', '')
    n = n.replace('\\Checkmark', '').replace('\\ding{55}', '').strip()
    return n


def numeric_pairs(path):
    """抽取全文所有 (方法名, 数值) 对，用于溯源校验。"""
    out = set()
    for ln in io.open(path, encoding='utf-8'):
        s = ln.strip()
        if s.startswith('%') or '&' not in s:
            continue
        if 'multicolumn' in s or s.startswith('\\midrule') or s.startswith('\\cmidrule'):
            continue
        cells = [c.strip() for c in s.rstrip('\\').split('&')]
        if len(cells) < 3:
            continue
        name = method_of(cells[0])
        if name in ('', 'Method', '方法', 'APS', 'Filter', '--'):
            continue
        for x in cells[2:]:
            v = re.sub(r'\\textbf\{([^}]*)\}', r'\1', x)
            v = re.sub(r'\\underline\{([^}]*)\}', r'\1', v)
            v = v.replace('\\Checkmark', '').replace('\\ding{55}', '').strip()
            if v and v != '--':
                out.add((name, v))
    return out


# ---------------------------------------------------------------- 主流程
def main():
    check_only = '--check' in sys.argv
    text = io.open(DST, encoding='utf-8').read()

    if not check_only:
        # --- 表 2-1：注入 OH_NEW + 逐类别表独有方法 ---
        m = re.search(r'(\\bicaption\[tab:main_oh_visda\].*?\\end\{table\*?\})', text, re.S)
        assert m, 'tab:main_oh_visda not found'
        blk = m.group(1)
        lines = blk.splitlines(True)
        lines = inject(lines,
                       'SHOT~\\cite{liang2021source} & \\checkmark & 57.1',
                       OH_NEW + OH_VISDA_ONLY + OH_FULL_ROWS)
        lines = uncomment(lines, ['NRC~\\cite{yang2021neighbor}', 'CoWA-JMDS~\\cite{cowa}'])
        text = text[:m.start(1)] + ''.join(lines) + text[m.end(1):]

        # --- 表 2-2：注入 Office 基线 ---
        m = re.search(r'(\\bicaption\[tab:main_office\].*?\\end\{table\*?\})', text, re.S)
        assert m, 'tab:main_office not found'
        lines = m.group(1).splitlines(True)
        lines = inject(lines, 'SHOT~\\cite{liang2021source} & \\checkmark & 94.0', OFF_NEW)
        lines = uncomment(lines, ['DIPE~\\cite{DIPE}', 'CoWA-JMDS~\\cite{cowa}'])
        text = text[:m.start(1)] + ''.join(lines) + text[m.end(1):]

        # --- 表 2-3：注入 MCC + 统一方法名 ---
        m = re.search(r'(\\bicaption\[tab:main_dn126\].*?\\end\{table\*?\})', text, re.S)
        assert m, 'tab:main_dn126 not found'
        lines = m.group(1).splitlines(True)
        lines = inject(lines, 'SHOT~\\cite{liang2021source} & \\checkmark & 67.7', DN_NEW)
        lines = [l.replace('AdaCon~\\cite{AdaContrast}', 'AdaContrast~\\cite{AdaContrast}')
                  .replace('TENT~\\cite{tent}', 'Tent~\\cite{tent}') for l in lines]
        text = text[:m.start(1)] + ''.join(lines) + text[m.end(1):]

        io.open(DST, 'w', encoding='utf-8').write(text)
        print('fused -> %s' % DST)

    # --- 数值溯源校验 ---
    src = numeric_pairs(SRC)
    dst = numeric_pairs(DST)
    missing = sorted(p for p in dst if p not in src)
    # 允许的非溯源项：新增的 Filter×SCS 正交消融表（源自 papers/Sfmamba/suppl_abl_module.tex）
    ALLOWED = {('Baseline', '79.9'), ('Baseline', '80.3'),
               ('w/ Filter', '81.2'), ('w/ Filter', '85.4'),
               ('w/ SCS', '80.9'), ('w/ SCS', '89.3')}
    hard = [p for p in missing if p not in ALLOWED]
    print('溯源校验：合并版 %d 对，原稿 %d 对，非溯源 %d 项（允许 %d 项）'
          % (len(dst), len(src), len(missing), len(missing) - len(hard)))
    if hard:
        print('  ⚠️  非允许的非溯源项：')
        for n, v in hard[:40]:
            print('     %s = %s' % (n, v))
    else:
        print('  ✅ 全部数值可溯源（或属新增的 Filter×SCS 表）')


if __name__ == '__main__':
    main()
