import io

def load(p):
    return io.open(p, encoding='utf-8').read()

def save(p, s):
    io.open(p, 'w', encoding='utf-8').write(s)

B = chr(92)

p = 'body/chap2.tex'
s = load(p)
print('=== chap2 ===')

rules = [
    # ---------- 1. 数据集符号统一为 mathcal{S} / mathcal{T} ----------
    ('给定带标签源域数据 $\\mathcal{D}_s = \\{(x_i^s, y_i^s)\\}_{i=1}^{n_s}$ 与无标签目标域数据 $\\mathcal{D}_t = \\{x_i^t\\}_{i=1}^{n_t}$',
     '给定带标签源域数据 $\\mathcal{S} = \\{(x_i^s, y_i^s)\\}_{i=1}^{n_s}$ 与无标签目标域数据 $\\mathcal{T} = \\{x_i^t\\}_{i=1}^{n_t}$'),
    ('源域与目标域的边缘分布存在差异，即 $P_s(x) \\neq P_t(x)$，但条件分布保持一致：$P_s(y \\mid x) = P_t(y \\mid x)$',
     '源域与目标域的边缘分布存在差异，即 $Q(x) \\neq P(x)$，但条件分布保持一致：$Q(y \\mid x) = P(y \\mid x)$'),
    ('源域模型 $\\theta_s = f \\circ g$ 在源域数据 $\\mathcal{D}_s$ 上完成预训练',
     '源域模型 $\\theta_s = f \\circ g$ 在源域数据 $\\mathcal{S}$ 上完成预训练'),
    ('目标域适应阶段，源域数据 $\\mathcal{D}_s$ 不可访问',
     '目标域适应阶段，源域数据 $\\mathcal{S}$ 不可访问'),
    ('\\boldsymbol{\\mu}^{(k)}_c = \\frac{\\sum_{x^t \\in \\mathcal{D}_t} \\mathbf{1}(\\hat{y}^{(k)}_t = c) \\, g(x^t)}{\\sum_{x^t \\in \\mathcal{D}_t} \\mathbf{1}(\\hat{y}^{(k)}_t = c)}, \\qquad',
     '\\boldsymbol{\\mu}^{(k)}_c = \\frac{\\sum_{x^t \\in \\mathcal{T}} \\mathbf{1}(\\hat{y}^{(k)}_t = c) \\, g(x^t)}{\\sum_{x^t \\in \\mathcal{T}} \\mathbf{1}(\\hat{y}^{(k)}_t = c)}, \\qquad'),
    ('\\mathcal{L}_{\\text{KL}} = \\mathbb{E}_{x^t \\sim \\mathcal{D}_t} D_{\\text{KL}}',
     '\\mathcal{L}_{\\text{KL}} = \\mathbb{E}_{x^t \\sim \\mathcal{T}} D_{\\text{KL}}'),
    ('\\KwIn{无标签目标样本 $\\mathcal{D}_t$，',
     '\\KwIn{无标签目标样本 $\\mathcal{T}$，'),
    ('从 $\\mathcal{D}_t$ 中采样小批量样本',
     '从 $\\mathcal{T}$ 中采样小批量样本'),

    # ---------- 2. 模型符号 phi -> theta_t ----------
    ('预训练源域模型 $\\phi$；训练轮数 $\\hat{T}$，每轮迭代数 $e_T$，批次大小 $B$；超参数 $\\gamma, \\tau, K, \\beta$}',
     '预训练源域模型 $\\theta_s$；训练轮数 $\\hat{T}$，每轮迭代数 $e_T$，批次大小 $B_{\\text{batch}}$；超参数 $\\gamma_{\\text{sel}}, \\tau, K, \\beta_{\\text{CE}}$}'),
    ('\\KwOut{适应后的目标域模型 $\\phi$}', '\\KwOut{适应后的目标域模型 $\\theta_t$}'),
    ('$\\phi \\leftarrow \\phi - \\eta \\nabla (\\mathcal{L}_{\\text{CL}} + \\beta \\mathcal{L}_{\\text{CE}} + \\mathcal{L}_{\\text{IM}})$；',
     '$\\theta_t \\leftarrow \\theta_t - \\eta \\nabla (\\mathcal{L}_{\\text{CL}} + \\beta_{\\text{CE}} \\mathcal{L}_{\\text{CE}} + \\mathcal{L}_{\\text{IM}})$；'),
    ('\\Return $\\phi$', '\\Return $\\theta_t$'),
    ('在大小为 $B$ 的 mini-batch 中，我们定义$i\\in I=\\{1,\\cdots,2B\\}$',
     '在大小为 $B_{\\text{batch}}$ 的 mini-batch 中，我们定义$i\\in \\mathcal{I}=\\{1,\\cdots,2B_{\\text{batch}}\\}$'),
    ('从 $\\mathcal{T}$ 中采样小批量样本 $\\{x_b\\}_{b=1}^B$\\;',
     '从 $\\mathcal{T}$ 中采样小批量样本 $\\{x_b\\}_{b=1}^{B_{\\text{batch}}}$\\;'),

    # ---------- 3. 损失权重 beta -> beta_CE ----------
    ('最终总体损失为 $\\mathcal{L} = \\mathcal{L}_{\\text{CL}} + \\beta \\mathcal{L}_{\\text{CE}} + \\mathcal{L}_{\\text{IM}}$',
     '最终总体损失为 $\\mathcal{L} = \\mathcal{L}_{\\text{CL}} + \\beta_{\\text{CE}} \\mathcal{L}_{\\text{CE}} + \\mathcal{L}_{\\text{IM}}$'),
    ('超参数设置为：损失权重 $\\beta = 0.3$，对比温度 $\\tau = 0.1$，近邻数 $K = 4$，各类数据集的置信样本筛选比例 $\\gamma$ 在',
     '超参数设置为：损失权重 $\\beta_{\\text{CE}} = 0.3$，对比温度 $\\tau = 0.1$，近邻数 $K = 4$，各类数据集的置信样本筛选比例 $\\gamma_{\\text{sel}}$ 在'),
    ('UPA 对四个核心超参数——置信样本筛选比例 $\\gamma$、对比温度 $\\tau$、K 近邻数 $K$ 与损失权重 $\\beta$——',
     'UPA 对四个核心超参数——置信样本筛选比例 $\\gamma_{\\text{sel}}$、对比温度 $\\tau$、K 近邻数 $K$ 与损失权重 $\\beta_{\\text{CE}}$——'),
    ('具体而言：$\\gamma$ 在 0.5–0.9 范围内变化时',
     '具体而言：$\\gamma_{\\text{sel}}$ 在 0.5–0.9 范围内变化时'),
    ('尽管 VisDA-C 数据集因域偏移更严重而对 $\\gamma$ 的选择更为敏感',
     '尽管 VisDA-C 数据集因域偏移更严重而对 $\\gamma_{\\text{sel}}$ 的选择更为敏感'),

    # ---------- 4. 干净集 mathcal{H} -> mathcal{T}_c ----------
    ('将目标域样本划分为干净集 $\\mathcal{H}$ 与噪声集',
     '将目标域样本划分为干净集 $\\mathcal{T}_c$ 与噪声集'),
    ('选取每个类别中得分最高的前 $\\gamma\\%$ 的样本，组成干净伪标签样本集 $\\mathcal{H}$',
     '选取每个类别中得分最高的前 $\\gamma_{\\text{sel}}\\%$ 的样本，组成干净伪标签样本集 $\\mathcal{T}_c$'),
    ('CACL策略，在干净伪标签样本集 $\\mathcal{H}$ 上利用类别级对比学习',
     'CACL策略，在干净伪标签样本集 $\\mathcal{T}_c$ 上利用类别级对比学习'),
    ('若两个样本 $(x_i, y_i)$ 和 $(x_j, y_j)$ 均属于 $\\mathcal{H}$ 且 $y_i = y_j$',
     '若两个样本 $(x_i, y_i)$ 和 $(x_j, y_j)$ 均属于 $\\mathcal{T}_c$ 且 $y_i = y_j$'),
    ('\\mathcal{O}(i) = \\left\\{ o_{ij} \\mid y_i = y_j;\\ (x_i, y_i), (x_j, y_j) \\in \\mathcal{H} \\right\\},',
     '\\mathcal{O}(i) = \\left\\{ o_{ij} \\mid y_i = y_j;\\ (x_i, y_i), (x_j, y_j) \\in \\mathcal{T}_c \\right\\},'),
    ('\\mathcal{L}_{\\text{CE}} = -\\mathbb{E}_{(x_t, \\hat{y}_t) \\in \\mathcal{H}} \\sum_{c=1}^{C}',
     '\\mathcal{L}_{\\text{CE}} = -\\mathbb{E}_{(x_t, \\hat{y}_t) \\in \\mathcal{T}_c} \\sum_{c=1}^{C}'),
    ('计算置信度评分并选取 top $\\gamma\\%$ 样本构成 $\\mathcal{H}$\\;',
     '计算置信度评分并选取 top $\\gamma_{\\text{sel}}\\%$ 样本构成 $\\mathcal{T}_c$\\;'),
    ('APS 所选高置信子集 $\\mathcal{H}$ 上的伪标签精度',
     'APS 所选高置信子集 $\\mathcal{T}_c$ 上的伪标签精度'),

    # ---------- 5. 相似度矩阵 S -> mathbf{S}_t ----------
    ('计算两两余弦相似度构成相似度矩阵 $S \\in \\mathbb{R}^{n_t \\times n_t}$',
     '计算两两余弦相似度构成相似度矩阵 $\\mathbf{S}_t \\in \\mathbb{R}^{n_t \\times n_t}$'),

    # ---------- 6. SCS 序列 I / tilde{I} -> U / tilde{U} ----------
    ('\\tilde{P}_k = P_{\\Pi(k)}, \\quad \\tilde{I} = \\text{Replace}(I, \\{\\tilde{P}_k\\}),',
     '\\tilde{P}_k = P_{\\Pi(k)}, \\quad \\tilde{U} = \\text{Replace}(U, \\{\\tilde{P}_k\\}),'),
    ('得到扰动序列 $\\tilde{I}$。', '得到扰动序列 $\\tilde{U}$。'),
    ('D_{\\text{KL}}\\!\\left(\\theta_t(I) \\,\\|\\, \\theta_t(\\tilde{I})\\right),',
     'D_{\\text{KL}}\\!\\left(\\theta_t(U) \\,\\|\\, \\theta_t(\\tilde{U})\\right),'),
    ('D_{\\text{KL}}\\!\\left(\\theta_t(I) \\,\\|\\, \\theta_t(\\tilde{I})\\right).',
     'D_{\\text{KL}}\\!\\left(\\theta_t(U) \\,\\|\\, \\theta_t(\\tilde{U})\\right).'),

    # ---------- 7. patch token 数 N -> N_p，背景比例 gamma -> gamma_bg ----------
    ('共产生 $N = (H/p) \\times (W/p)$ 个 patch token',
     '共产生 $N_p = (H/p) \\times (W/p)$ 个 patch token'),
    ('识别相对于伪标签 $\\hat{y}$ 激活值最低的 $\\gamma\\%$ 的 patch 作为背景 patch 集合 $\\{P_k\\}_{k=1}^N$',
     '识别相对于伪标签 $\\hat{y}$ 激活值最低的 $\\gamma_{\\text{bg}}\\%$ 的 patch 作为背景 patch 集合 $\\{P_k\\}_{k=1}^{N_p}$'),
    ('目标域适应阶段背景比例 $\\gamma = 20\\%$',
     '目标域适应阶段背景比例 $\\gamma_{\\text{bg}} = 20\\%$'),
    ('{Ch-VSS 模块数 $L$ 与背景打乱比例 $\\gamma$ 的消融}{Fig.}{Ablation on the number of Ch-VSS blocks $L$ and the background shuffle ratio $\\gamma$}',
     '{Ch-VSS 模块数 $L_{\\text{vss}}$ 与背景打乱比例 $\\gamma_{\\text{bg}}$ 的消融}{Fig.}{Ablation on the number of Ch-VSS blocks $L_{\\text{vss}}$ and the background shuffle ratio $\\gamma_{\\text{bg}}$}'),
    ('本节考察两个关键超参数：Ch-VSS 块数 $L$ 与 SCS 的背景 patch 比例 $\\gamma$。',
     '本节考察两个关键超参数：Ch-VSS 块数 $L_{\\text{vss}}$ 与 SCS 的背景 patch 比例 $\\gamma_{\\text{bg}}$。'),
    ('图~\\ref{fig:sfmamba_l_ablation_right} 进一步展示了背景比例 $\\gamma$ 对目标精度的影响：当 $\\gamma=20$ 时取得最高精度，性能在小 $\\gamma$ 值下保持稳定，但 $\\gamma$ 过大时显著下降',
     '图~\\ref{fig:sfmamba_l_ablation_right} 进一步展示了背景比例 $\\gamma_{\\text{bg}}$ 对目标精度的影响：当 $\\gamma_{\\text{bg}}=20$ 时取得最高精度，性能在小 $\\gamma_{\\text{bg}}$ 值下保持稳定，但 $\\gamma_{\\text{bg}}$ 过大时显著下降'),
    ('  \\subfigure[置信样本筛选比例 $\\gamma$]{%', '  \\subfigure[置信样本筛选比例 $\\gamma_{\\text{sel}}$]{%'),

    # ---------- 8. SfMamba 筛选比例 beta -> gamma_sel，高质量子集统一 ----------
    ('按类别内排序选取前 $\\beta\\%$ 样本构成高质量子集 $\\mathcal{X}_t^{\\text{sel}}$',
     '按类别内排序选取前 $\\gamma_{\\text{sel}}\\%$ 样本构成高质量子集 $\\mathcal{T}_c$'),
    ('\\mathcal{L}_{\\text{CE}} = -\\mathbb{E}_{x^t \\in \\mathcal{X}_t^{\\text{sel}}} \\sum_{c=1}^{C} \\hat{y}_c \\log p_c(x^t), \\quad',
     '\\mathcal{L}_{\\text{CE}} = -\\mathbb{E}_{x^t \\in \\mathcal{T}_c} \\sum_{c=1}^{C} \\hat{y}_c \\log p_c(x^t), \\quad'),
    ('\\mathcal{L}_{\\text{KL}} = \\mathbb{E}_{x^t \\in \\mathcal{X}_t^{\\text{sel}}} D_{\\text{KL}}',
     '\\mathcal{L}_{\\text{KL}} = \\mathbb{E}_{x^t \\in \\mathcal{T}_c} D_{\\text{KL}}'),
]

for old, new in rules:
    n = s.count(old)
    print('  %-60s %d' % (old[:58], n))
    s = s.replace(old, new)

save(p, s)
print('saved', p)
