#!/usr/bin/env python3
"""
扫描 body/ + back/ 下"公式末含逗号 + 公式后空行"的潜在违例。
仅检测，不修改。
"""
import re
from pathlib import Path

ROOT = Path('/Users/xichen/Documents/hithesis-master')

# 公式环境：equation / align / gather / multline / flalign / alignat + * 变体
ENV_NAMES = (
    'equation', 'equation*',
    'align', 'align*',
    'eqnarray', 'eqnarray*',
    'gather', 'gather*',
    'multline', 'multline*',
    'flalign', 'flalign*',
    'alignat', 'alignat*',
)
ENV_SET = set(ENV_NAMES)
BEGIN_RE = re.compile(r'\\begin\{(' + '|'.join(ENV_NAMES) + r')\}')
END_RE   = re.compile(r'\\end\{(' + '|'.join(ENV_NAMES) + r')\}')

# 衔接词（前 20 字内出现即视为衔接段）
CONNECTORS = ('其中', '上式中', '记 ', '记最终', '记第', '记为',
              '设 ', '设第', '设为', '令 ', '令第', '令为',
              '接下来', '下面', '随后', '进而', '此时', '此处',
              '该损失', '该方法', '该模块', '其定义', '其含义',
              '式 (', '式（', '式~\\ref', '式~\\eqref', '其中',
              '具体地', '具体而言', '一般地', '事实上', '进一步')

files = sorted(list((ROOT / 'body').glob('*.tex')) + list((ROOT / 'back').glob('*.tex')))

total_candidates = 0
total_strong = 0  # 末行真含逗号 + 后有空行 + 衔接段

print('=' * 70)
print(' 全库"公式末为逗号 + 公式后空行"潜在违例扫描')
print(' 扫描范围: body/*.tex + back/*.tex')
print('=' * 70)

for f in files:
    try:
        text = f.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    lines = text.split('\n')

    for i, line in enumerate(lines):
        m = BEGIN_RE.search(line)
        if not m:
            continue
        env = m.group(1)

        # 找对应 \end（同环境）
        j = i + 1
        depth = 1
        end_found = False
        while j < len(lines):
            if BEGIN_RE.search(lines[j]):
                depth += 1
            em = END_RE.search(lines[j])
            if em and em.group(1) == env:
                depth -= 1
                if depth == 0:
                    end_found = True
                    break
            j += 1
        if not end_found:
            continue

        # 公式末非空行（往前找）
        last = j - 1
        while last > i and lines[last].strip() == '':
            last -= 1
        last_text = lines[last].strip()
        # 末行是 \\ 行（多行公式换行符）→ 跳过
        if last_text == '\\\\' or last_text.endswith('\\\\'):
            continue
        # 末行只是 \label{} → 找 label 前一行
        if last_text.startswith('\\label{') and last > i:
            last2 = last - 1
            while last2 > i and lines[last2].strip() == '':
                last2 -= 1
            if last2 > i:
                last_text = lines[last2].strip()
                last = last2

        # 末标点判断
        has_comma = last_text.endswith(',') or last_text.endswith('，')
        has_period = last_text.endswith('.') or last_text.endswith('。') or last_text.endswith(')')

        # end 后是否空行
        after = j + 1
        has_blank_after = after < len(lines) and lines[after].strip() == ''

        if not has_comma or not has_blank_after:
            continue

        # 找衔接段（end 后第一个非空段）
        k = after + 1 if has_blank_after else after
        while k < len(lines) and lines[k].strip() == '':
            k += 1
        next_text = lines[k].strip()[:50] if k < len(lines) else ''

        is_connector = any(c in next_text for c in CONNECTORS)

        marker = '🔴' if is_connector else '⚠️ '
        total_candidates += 1
        if is_connector:
            total_strong += 1

        print(f'\n{marker} [{f.name}] 公式环境 \\begin{{{env}}} @ L{i+1}')
        print(f'   公式末行 L{last+1}: {last_text[:70]}')
        print(f'   end 行      L{j+1}: {lines[j].strip()[:60]}')
        print(f'   衔接段      L{k+1}: {next_text}{"..." if len(lines[k].strip()) > 50 else ""}')
        print(f'   判定: 末标点=逗号 ✓ | 后空行 ✓ | 衔接词={is_connector}')

print('\n' + '=' * 70)
print(f' 扫描完成: {len(files)} 个文件, {total_candidates} 处潜在违例, {total_strong} 处强违例（衔接词）')
print('=' * 70)
