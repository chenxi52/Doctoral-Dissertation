#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重建 body/chap2.tex —— 双方法结构正本。

来源：
  body/chap2.tex.bak        原稿（未改动的双方法版）：§2.2 UPA(含 CACL) + §2.3 SfMamba
  body/chap2_merge.tex.bak  合并稿：已融合的 3 张主表 + 已整理的 SfMamba 实验段

产出：
  body/chap2.tex             双方法结构 + 统一实验节 + 跨骨干 APS 统一消融表
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(ROOT, 'body', 'chap2.tex.bak')
MERGE = os.path.join(ROOT, 'body', 'chap2_merge.tex.bak')
OUT = os.path.join(ROOT, 'body', 'chap2.tex')


def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read().split('\n')


def find(lines, needle, start=0, what=''):
    for i in range(start, len(lines)):
        if needle in lines[i]:
            return i
    raise SystemExit(f'NOT FOUND: {needle!r} {what}')


def sl(lines, a, b):
    """1-indexed inclusive."""
    return lines[a - 1:b]


O = read(ORIG)
M = read(MERGE)

# ============================== 定位锚点 ==============================
o_intro_end   = find(O, '\\end{enumerate}') + 1
o_upa_start   = find(O, '\\section{基于特征聚合的不确定性感知伪标签去噪方法}')
o_upa_meth    = find(O, '\\subsection{实验结果与分析}', o_upa_start) - 1
o_upa_abl     = find(O, '\\noindent\\textbf{(3) 消融实验分析}')
o_upa_vis     = find(O, '\\noindent\\textbf{(4) 可视化分析}')
o_upa_tsne_end= find(O, '\\end{figure}', find(O, '\\bicaption[fig:upa_tsne]')) + 1
# ---- 3. §2.3 SfMamba 方法节（原稿原文） ----
#      原稿 §2.3.2 末尾已含 CE/KL 联合损失与总损失；合并稿另有「总体训练流程」小节含
#      同样公式 → 两者重复。策略：保留原稿 §2.3.2 的损失公式（先出现），
#      在重建时把原稿该段替换为「总体训练流程」小节的一次性版本。
o_sfm_start   = find(O, '\\section{基于选择性扫描的不确定性感知的迁移方法}')
o_sfm_meth    = find(O, '\\subsection{实验结果与分析}', o_sfm_start) - 1
o_summary     = find(O, '\\section{本章小结}')

m_setup  = find(M, '\\noindent\\textbf{(1) 数据集与实验设置}')
m_main   = find(M, '\\noindent\\textbf{(2) 主实验结果}')
m_abl    = find(M, '\\noindent\\textbf{(3) 消融实验分析}')
m_sfmabl = find(M, '\\noindent\\textbf{SfMamba 模块消融}')
m_filter = find(M, '\\bicaption[tab:abl_filter]')
m_filter_end = find(M, '\\end{table}', m_filter) + 1
m_ablattn= find(M, '为评估 Ch-VSS 中双向通道扫描设计的有效性')
m_vis    = find(M, '\\noindent\\textbf{(4) 可视化分析}')
m_gradcam= find(M, 'Grad-CAM 可视化（图~\\ref{fig:sfmamba_gradcam}）')
m_hyper  = find(M, '\\noindent\\textbf{SfMamba 的超参数分析}')
m_eff    = find(M, '\\noindent\\textbf{(5) 计算效率}')
m_sum    = find(M, '\\section{本章小结}')
m_train  = find(M, '\\noindent\\textbf{总体训练流程}')
m_train_end = find(M, '\\section{实验结果与分析}', m_train)

print('[锚点] 定位完成')

# ============================== 组装 ==============================
out = []

# ---- 1. 引言（原稿，归纳列表已匹配双方法结构，保留） ----
out += sl(O, 1, o_intro_end)

# ---- 2. §2.2 UPA 方法节（原稿原文，含 CACL / alg:upa） ----
out += ['']
out += sl(O, o_upa_start, o_upa_meth)

# ---- 3. §2.3 SfMamba 方法节（原稿原文） ----
#      原稿 §2.3.2 末尾已含 CE/KL 联合损失与总损失，与合并稿「总体训练流程」小节重复。
#      策略：只保留「总体训练流程」小节版本（合并稿），把原稿 §2.3.2 中的重复公式段删除。
sfm_body = sl(O, o_sfm_start, o_sfm_meth)
# 删除原稿中「为缓解伪标签噪声 ... \eqref{eq:chap2_im}。」这一整段（含两个公式）
_dup_start = None
for i, l in enumerate(sfm_body):
    if l.startswith('为缓解伪标签噪声对'):
        _dup_start = i
        break
assert _dup_start is not None, '未找到原稿 SfMamba 重复损失段'
_dup_end = _dup_start
for i in range(_dup_start, len(sfm_body)):
    if '参见式~\\eqref{eq:chap2_im}' in sfm_body[i]:
        _dup_end = i
        break
# 连同其后的注释行一起删
while _dup_end + 1 < len(sfm_body) and sfm_body[_dup_end + 1].startswith('%'):
    _dup_end += 1
sfm_body = sfm_body[:_dup_start] + sfm_body[_dup_end + 1:]

out += ['']
out += sfm_body

# ---- 4. 总体训练流程 + alg:sfmamba（取自合并稿，引用改指 UPA 的 APS 小节） ----
train = '\n'.join(sl(M, m_train, m_train_end - 1))
train = train.replace('\\ref{sec:chap2_aps}', '\\ref{sec:chap2_upa_denoising}')
train = train.replace('三条抑制路径在同一次参数更新中协同作用',
                      '判别层去噪与骨干级序列增强在同一次参数更新中协同作用')
# 合并稿里该标题是 \noindent\textbf{}（行内强调形式），改为正式的 \subsection
train = train.replace('\\noindent\\textbf{总体训练流程}',
                      '\\subsection{总体训练流程}')
out += ['']
out += train.split('\n')

# ============================== §2.4 实验结果与分析 ==============================
exp = []
exp.append('\\section{实验结果与分析}')
exp.append('')
exp.append('\\label{sec:chap2_experiments}')
exp.append('')
exp.append('本章两条方法在统一的实验协议下评估，覆盖 Office、Office-Home、VisDA-C 与 DomainNet-126 四个跨域基准。'
           '主表按骨干网络分类组织，使同一骨干下的方法可在公平条件下比较；消融实验则按抑制机制归类，'
           '在卷积骨干与状态空间骨干上分别考察各机制的独立贡献及其互补性。以下先给出数据集与实现细节，'
           '再报告主实验结果，最后给出消融实验、可视化分析与计算效率分析。')
exp.append('')

# ---- (1) 数据集与实验设置（两条方法的实现细节合并） ----
exp.append('\\noindent\\textbf{(1) 数据集与实验设置}')
exp.append('')
exp.append('本节在 Office~\\cite{saenko2010adapting}、Office-Home~\\cite{venkateswara2017deep}、VisDA-C~\\cite{peng2017visda} '
           '与 DomainNet-126~\\cite{peng2019moment} 四个基准数据集上评估所提的两条方法。具体而言：Office 数据集包含 '
           'Amazon（A）、Dslr（D）与 Webcam（W）三个域，域间共享 31 个类别；Office-Home 数据集包含 Art（A）、Clipart（C）、'
           'Product（P）与 Real World（R）四个域，每个域共享 65 个类别；VisDA-C 数据集包含合成域 Synthetic（S）与真实域 '
           'Real（R）的跨域分割任务；DomainNet-126 包含 126 个类别，来自 Real（R）、Painting（P）、Clipart（C）与 '
           'Sketch（S）四个域。')
exp.append('')
exp.append('UPA 在卷积骨干上评估：Office、Office-Home 与 DomainNet-126 使用 ResNet-50，VisDA-C 使用 ResNet-101，'
           '源域模型采用 SHOT 的预训练设置。适应阶段采用 SGD 优化器，设置动量 0.9、权重衰减 $10^{-3}$、batch size 64，'
           '学习率策略为先线性预热一个 epoch 后余弦退火衰减；Office、Office-Home 与 DomainNet-126 的初始学习率设为 '
           '$10^{-2}$，VisDA-C 的初始学习率设为 $10^{-3}$，瓶颈层学习率设置为骨干网络的 10 倍。损失权重 '
           '$\\beta_{\\text{CE}} = 0.3$，对比温度 $\\tau = 0.1$，近邻数 $K = 4$，置信样本筛选比例 $\\gamma_{\\text{sel}}$ '
           '在 Office / Office-Home / DomainNet-126 设为 0.6，在 VisDA-C 设为 0.8。')
exp.append('')
exp.append('SfMamba 在状态空间骨干上评估：采用 VMamba-T（Tiny）与 VMamba-S（Small）两种规模的 SSM 骨干，'
           '并以 SHOT~\\cite{liang2021source} 自训练框架为基础，冻结分类器。训练阶段采用 AdamW 优化器，'
           '权重衰减率为 $5 \\times 10^{-2}$，并用余弦退火策略，批次大小为 32，在单卡 NVIDIA RTX A100 GPU 进行实验。'
           '源域预训练 Office / Office-Home / VisDA-C / DomainNet-126 分别为 100 / 50 / 10 / 30 个 epoch，'
           '目标域适应阶段背景比例 $\\gamma_{\\text{bg}} = 20\\%$，近邻数 $K = 4$，置信样本筛选比例 '
           '$\\gamma_{\\text{sel}}$ 在 Office-Home 与 DomainNet-126 设为 0.6，在 VisDA-C 设为 0.8。'
           '所有结果报告三次随机种子 $\\{0, 1, 2\\}$ 的平均值。')
exp.append('')

# ---- (2) 主实验结果（合并稿：3 张融合表 + 分析） ----
exp += sl(M, m_main, m_abl - 1)

# ---- (3) 消融实验分析 ----
exp.append('\\noindent\\textbf{(3) 消融实验分析}')
exp.append('')
exp.append('本节对 UPA 的判别层去噪机制（APS 与 CACL）与 SfMamba 的骨干级增强机制（Ch-VSS 与 SCS）开展消融验证，'
           '以考察各抑制机制对迁移不确定性的独立贡献及其互补性。')
exp.append('')

# 3.1 UPA 侧消融（原稿：ablation_loss 三行含 CACL / uncertainty / iter）
exp.append('\\noindent\\textbf{UPA 的判别层去噪消融}')
exp.append('')
exp += sl(O, o_upa_abl + 2, o_upa_vis - 1)

# 3.2 跨骨干 APS 统一消融表（新建）
exp.append('\\noindent\\textbf{APS 筛选机制的跨骨干消融}')
exp.append('')
exp.append('上述 UPA 侧的消融实验在卷积骨干上开展，而 SfMamba 侧在状态空间骨干上同样引入了 APS 作为样本筛选子组件，'
           '两者的实验条件与结论无法直接互相印证。为在同一表格内呈现 APS 在不同骨干上的作用边界，'
           '表~\\ref{tab:abl_aps} 将卷积骨干与状态空间骨干上的 APS 消融结果合并列示。')
exp.append('')
exp.append('\\begin{table}[!htbp]')
exp.append('    \\bicaption[tab:abl_aps]{}{APS 筛选机制在卷积骨干与状态空间骨干上的消融实验}{Table}{Ablation of the APS filtering mechanism on the CNN and the Mamba backbones}')
exp.append('    \\vspace{0.5em}\\centering\\wuhao')
exp.append('    \\begin{tabular}{llccccc}')
exp.append('    \\toprule')
exp.append('    Method & Backbone & APS & CACL & Office & Office-Home & VisDA-C \\\\')
exp.append('    \\midrule')
exp.append('    \\multicolumn{7}{c}{\\textit{基于卷积骨干的方法}} \\\\')
exp.append('    \\midrule')
exp.append('    SHOT~\\cite{liang2021source} & ResNet-50/101 & -- & -- & 88.6 & 71.8 & 82.9 \\\\')
exp.append('    w/ APS              & ResNet-50/101 & \\Checkmark & -- & \\textbf{89.5} & \\textbf{72.7} & \\textbf{84.2} \\\\')
exp.append('    w/ APS + CACL       & ResNet-50/101 & \\Checkmark & \\Checkmark & \\textbf{89.9} & \\textbf{73.0} & \\textbf{88.7} \\\\')
exp.append('    \\midrule')
exp.append('    \\multicolumn{7}{c}{\\textit{基于状态空间骨干的方法}} \\\\')
exp.append('    \\midrule')
exp.append('    SHOT~\\cite{liang2021source} & VMamba-S & -- & -- & -- & 80.3 & 79.9 \\\\')
exp.append('    w/ APS              & VMamba-S & \\Checkmark & -- & -- & 81.2 & 85.4 \\\\')
exp.append('    \\bottomrule')
exp.append('    \\end{tabular}')
exp.append('\\end{table}')
exp.append('')
exp.append('表~\\ref{tab:abl_aps}表明，APS 筛选在两类骨干上均带来正增益，但其作用强度与收益结构存在显著差异。'
           '在卷积骨干上，APS 在 Office、Office-Home 与 VisDA-C 上分别带来 +0.9\\%、+0.9\\% 与 +1.3\\% 的提升，'
           '且在此基础上引入 CACL 可在 VisDA-C 上进一步获得 +4.5\\% 的增益——说明在卷积骨干上，'
           '判别层的伪标签噪声是适应性能的主要瓶颈，对干净集继续施加表征级正则仍有明显收益。'
           '在状态空间骨干上，APS 在 Office-Home 与 VisDA-C 上分别带来 +0.9\\% 与 +5.5\\% 的提升，'
           '但在 VisDA-C 上这一增益远低于同基准下 SCS 单独引入所带来的 +9.4\\%（详见表~\\ref{tab:abl_filter}）。'
           '这一对照说明，APS 所解决的监督信号可靠性问题与 SCS 所解决的序列层空间共现记忆问题作用于不同的失效模式，'
           '在状态空间骨干上二者的收益无法相互替代，须联合使用方能取得最优性能。')
exp.append('')

# 3.3 SfMamba 侧消融（合并稿：ablation_modules / abl_attn / abl_backbone / abl_scs），移除正交表
exp.append('\\noindent\\textbf{SfMamba 的骨干级增强消融}')
exp.append('')
# 合并稿此处有重复的「SfMamba 模块消融」行内标题，跳过它（m_sfmabl 指向该行）
exp += sl(M, m_sfmabl + 2, m_filter - 1)          # ablation_modules + 分析
exp += sl(M, m_ablattn, m_vis - 1)                # abl_attn / abl_backbone / abl_scs + 分析

# 正交表（原合并稿）—— 保留，用于说明 Filter 与 SCS 的交互
exp.append('为进一步辨析 APS 样本筛选与 SCS 在状态空间骨干上的作用边界，我们设计了两者的正交消融实验，'
           '如表~\\ref{tab:abl_filter}所示。该实验固定 Ch-VSS 模块为开启状态，在 Filter（APS 筛选）与 SCS 两个维度上'
           '作 2$\\times$2 交叉配置，从而在相同骨干能力下分离出判别层去噪与序列层抑制各自的独立贡献及其交互效应。')
exp.append('')
exp += sl(M, m_filter - 1, m_filter_end)
exp.append('')
exp.append('表~\\ref{tab:abl_filter}的结果表明，APS 样本筛选与 SCS 在两个基准上呈现出不同性质的作用。'
           '在 Office-Home 上，二者具有近似可加的互补效果：单独引入 Filter 带来 +0.9\\% 的增益'
           '（80.3\\% $\\rightarrow$ 81.2\\%），单独引入 SCS 带来 +0.6\\%（80.3\\% $\\rightarrow$ 80.9\\%），'
           '二者联合进一步提升至 81.7\\%，交互项为 -0.1\\%，即两者的收益基本可独立叠加。'
           'APS 所解决的伪标签监督信号可靠性问题与 SCS 所解决的序列层空间共现捷径问题，在中等规模偏移下作用于不同的失效模式，'
           '因此二者互不替代。')
exp.append('')
exp.append('而在 VisDA-C 上这一性质发生了显著改变：单独引入 Filter 带来 +5.5\\% 的增益'
           '（79.9\\% $\\rightarrow$ 85.4\\%），但单独引入 SCS 已带来 +9.4\\% 的增益'
           '（79.9\\% $\\rightarrow$ 89.3\\%），二者联合的结果 89.3\\% 与 SCS 单独使用完全持平，'
           '即 Filter 在该基准上未能提供任何超出 SCS 的额外收益。这一现象表明，'
           '在合成到真实的极端域偏移下，判别层的伪标签筛选虽能带来可观收益，却远不足以优化 Mamba 骨干的适应性能；'
           'Mamba 的适应瓶颈已不在伪标签噪声，而在序列层对背景 patch 空间共现的记忆。'
           'SCS 通过置换背景 patch 并施加一致性正则，直接切断了状态转移机制对虚假相关性的累积通路，'
           '因而提供了 Filter 所无法替代的增益。')
exp.append('')
exp.append('该结果从反面验证了本章的核心论点：迁移不确定性的分层抑制需要判别层去噪与骨干级序列增强的协同，'
           '缺少任一层次都将导致性能损失；反之，在 Mamba 骨干上，仅有判别层去噪而不引入序列层抑制机制，'
           '同样无法达到最优性能。')
exp.append('')

# ---- (4) 可视化分析：t-SNE（原稿）+ GradCAM/案例（合并稿） ----
exp.append('\\noindent\\textbf{(4) 可视化分析}')
exp.append('')
exp += sl(O, o_upa_vis + 2, o_upa_tsne_end)
exp.append('')
exp += sl(M, m_gradcam, m_hyper - 1)

# ---- SfMamba 超参数分析 ----
exp += ['']
exp += sl(M, m_hyper, m_eff - 1)

# ---- (5) 计算效率 ----
exp += ['']
exp += sl(M, m_eff, m_sum - 1)

out += exp

# ---- 本章小结（原稿，双方法结构） ----
out += ['']
out += sl(O, o_summary, len(O))

txt = '\n'.join(out)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(txt)
print(f'[写出] {OUT}  {len(txt.splitlines())} 行')
