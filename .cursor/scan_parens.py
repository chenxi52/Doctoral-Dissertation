#!/usr/bin/env python3
"""
按段落扫描 body/ + back/ 的括号密度，列清单。
阈值：≥ 1 括号 / 50 字（按 reduce-parens.mdc）。
"""
import re
from pathlib import Path

ROOT = Path('/Users/xichen/Documents/hithesis-master')

# 剥离数学/LaTeX 命令，避免误算
def strip_math_and_commands(text):
    # 行内 / 显示数学
    text = re.sub(r'\$\$[^$]*\$\$', '', text)
    text = re.sub(r'\$[^$]*\$', '', text)
    text = re.sub(r'\\\[.*?\\\]', '', text)
    # 命令
    for cmd in ('cite', 'ref', 'eqref', 'label', 'bicaption', 'caption',
                'section', 'subsection', 'subsubsection', 'paragraph',
                'subparagraph', 'item', 'begin', 'end', 'includegraphics',
                'centering', 'textbf', 'emph', 'hline', 'cline', 'toprule',
                'midrule', 'bottomrule'):
        text = re.sub(r'\\' + cmd + r'(?:\[[^\]]*\])?(?:\{[^}]*\})*', '', text)
    # 通用 \cmd{...} 和 \cmd[...]{...}{...}
    text = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^\]]*\])?\{[^}]*\}', '', text)
    # 环境体 \begin{...}...\end{...}
    text = re.sub(r'\\begin\{[^}]+\}.*?\\end\{[^}]+\}', '', text, flags=re.DOTALL)
    # 表格对齐 &
    text = text.replace('&', ' ')
    # 多余空白
    text = re.sub(r'\s+', ' ', text)
    return text


def total_density(text):
    t = strip_math_and_commands(text)
    parens = len(re.findall(r'[（()）]', t))
    chars = len(t.replace(' ', ''))
    return parens, chars, parens / max(chars, 1) * 50


def paragraph_density(text):
    t = strip_math_and_commands(text)
    paras = re.split(r'\n\s*\n', t)
    results = []
    for p in paras:
        p = p.strip()
        if len(p) < 40:
            continue
        parens = len(re.findall(r'[（()）]', p))
        chars = len(p.replace(' ', ''))
        density = parens / max(chars, 1) * 50
        if density >= 0.8:  # 略低于 1.0，让清单更宽
            # 找括号内的内容作提示
            snippets = re.findall(r'[（(]([^）)]+)[）)]', p)
            results.append((density, parens, chars, p[:150], snippets))
    return results


# 模式识别
def identify_patterns(text):
    patterns = []
    # 模式 3：列举括号（含 X、Y、Z）
    for m in re.finditer(r'（含[^）]*、[^）]*）', text):
        patterns.append(('列举', m.group(0)))
    for m in re.finditer(r'（包括[^）]*、[^）]*）', text):
        patterns.append(('列举', m.group(0)))
    # 模式 1/2：缩写/英文术语括号
    for m in re.finditer(r'（([A-Z][A-Za-z0-9\-]*(?:\s+[A-Z][A-Za-z0-9\-]*)*)）', text):
        inside = m.group(1).strip()
        # 全大写 / 缩写 / 混合 → 模式 2
        if re.match(r'^[A-Z][A-Za-z]*[\s\-][A-Z][A-Za-z]*[\s\-][A-Z][A-Za-z]*[,，]?\s*[A-Z]+$', inside) or \
           re.match(r'^[A-Z]+$', inside.split()[-1] if inside.split() else '') or \
           re.match(r'^[A-Z][A-Za-z\-]+\s+[A-Z][A-Za-z\-]+\s+[A-Z]+$', inside):
            patterns.append(('缩写首次展开', m.group(0)))
        else:
            patterns.append(('英文术语', m.group(0)))
    # 模式 4：数据/单位注解
    for m in re.finditer(r'（约?\s*\d+[^）]*）', text):
        patterns.append(('数据注解', m.group(0)))
    return patterns


files = sorted(list((ROOT / 'body').glob('*.tex')) + list((ROOT / 'back').glob('*.tex')))

print('=' * 80)
print(' 全库"冗余括号"密度扫描（按段落，阈值 ≥ 0.8 / 50字）')
print('=' * 80)

grand_total_paras = 0
grand_4cat_paras = 0
for f in files:
    text = f.read_text(encoding='utf-8')
    parens, chars, density = total_density(text)
    paras = paragraph_density(text)
    patterns = identify_patterns(text)

    flag = '🔴' if density > 1.0 else '⚠️ ' if density > 0.5 else '✅'
    print(f'\n{flag} {f.name}: 全文密度 {density:.2f} / 50字 ({parens}括号 / {chars}字, 高密度段 {len(paras)})')
    print(f'   4 类可去模式识别: {len(patterns)} 处')
    # 按模式分组
    from collections import Counter
    pat_counter = Counter(p[0] for p in patterns)
    for k, v in pat_counter.items():
        print(f'     - {k}: {v}')

    for d, p, c, snippet, snippets in paras:
        mark = '🔴' if d >= 1.0 else '⚠️'
        print(f'   {mark} 段密度 {d:.2f} ({p}括号/{c}字) 括号内: {snippets[:3]}')
        print(f'      段首: {snippet}...')
        grand_total_paras += 1

print('\n' + '=' * 80)
print(f' 共 {grand_total_paras} 个高密度段（≥ 0.8 / 50字）')
print('=' * 80)
