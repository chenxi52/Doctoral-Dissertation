import io

def load(p):
    return io.open(p, encoding='utf-8').read()

def save(p, s):
    io.open(p, 'w', encoding='utf-8').write(s)

B = chr(92)

p = 'body/chap4.tex'
s = load(p)
print('=== chap4 ===')

# --- 1. 掩码族 M -> mathcal{M}（避让第3章损失上界 M）---
# 公式与正文中的掩码记号
mask_rules = [
    # eq:query_injector
    ('x^l = E_p(\\mathrm{pool}_{M^l} F_{\\mathrm{sam}}).',
     'x^l = E_p(\\mathrm{pool}_{\\mathcal{M}^l} F_{\\mathrm{sam}}).'),
    # eq:mask_pred
    ('M^l = E_m(X^l) \\cdot F_{\\mathrm{clip},e},',
     '\\mathcal{M}^l = E_m(X^l) \\cdot F_{\\mathrm{clip},e},'),
    # 正文"第$l$层新生成的掩码$M^l$"
    ('给定Transformer解码器第$l$层新生成的掩码$M^l$',
     '给定Transformer解码器第$l$层新生成的掩码$\\mathcal{M}^l$'),
    # 正文"其中$M^l$为连续掩码值，最终层输出记为$M=\{m_i\}_{i=1}^N$"
    ('其中$M^l$为连续掩码值，最终层输出记为$M=\\{m_i\\}_{i=1}^N$',
     '其中$\\mathcal{M}^l$为连续掩码值，最终层输出记为$\\mathcal{M}=\\{m_i\\}_{i=1}^{N_q}$'),
    # eq:class_pred 中的 pool_M
    ('E_c(X^l + E_p(\\mathrm{pool}_M F_{\\mathrm{clip},e}))',
     'E_c(X^l + E_{aux}(\\mathrm{pool}_{\\mathcal{M}} F_{\\mathrm{clip},e}))'),
    # eq:mask_attn
    ('M^{l-1}_{[x,y]} = \\begin{cases} 0, & M^{l-1}_{[x,y]} > 0, \\\\ -\\infty, & \\text{otherwise}, \\end{cases}',
     '\\mathcal{M}^{l-1}_{[x,y]} = \\begin{cases} 0, & \\mathcal{M}^{l-1}_{[x,y]} > 0, \\\\ -\\infty, & \\text{otherwise}, \\end{cases}'),
    # eq:mask_ensemble 中的 r
    ('r = \\sum_{i=1}^N p_i(c) \\cdot m_{i,[x,y]}',
     'r = \\sum_{i=1}^{N_q} p_i(c) \\cdot m_{i,[x,y]}'),
    # 类别集成
    ('P_d=\\{p_{i,d}\\}_{i=1}^N', 'P_d=\\{p_{i,d}\\}_{i=1}^{N_q}'),
    ('P_{\\mathrm{cl}}=\\{p_{i,\\mathrm{cl}}\\}_{i=1}^N',
     'P_{\\mathrm{cl}}=\\{p_{i,\\mathrm{cl}}\\}_{i=1}^{N_q}'),
    # SAM 掩码族
    ('生成类别无关掩码$M_{\\mathrm{sam}}$', '生成类别无关掩码$\\mathcal{M}_{\\mathrm{sam}}$'),
    ('首先对$M_{\\mathrm{sam}}$应用AttnPool', '首先对$\\mathcal{M}_{\\mathrm{sam}}$应用AttnPool'),
    ('得到选中的概率-掩码对$(M\'_{\\mathrm{sam}}, P\'_{\\mathrm{sam}})$',
     '得到选中的概率-掩码对$(\\mathcal{M}\'_{\\mathrm{sam}}, P\'_{\\mathrm{sam}})$'),
    # 解码层数 L -> L_dec
    ('$\\{F_{\\text{clip},l}\\}_{l=1}^L$', '$\\{F_{\\text{clip},l}\\}_{l=1}^{L_{\\text{dec}}}$'),
    ('整个Transformer解码器由$L=9$层组成', '整个Transformer解码器由$L_{\\text{dec}}=9$层组成'),
    ('Transformer解码器层数$L=9$', 'Transformer解码器层数$L_{\\text{dec}}=9$'),
    # 查询数 N -> N_q
    ('$P_d = \\mathrm{Softmax}', '$P_d = \\mathrm{Softmax}'),
    # 注入层编号中的 l 与 L 无关，无需改
    # E_p 两义 -> E_aux（掩码辅助投影）
    ('（2）$E_p$将池化后的掩码特征投影为预测辅助嵌入',
     '（2）$E_{aux}$将池化后的掩码特征投影为预测辅助嵌入'),
    # 集成系数
    ('其中$\\alpha=0.4$，$\\beta=0.8$为平衡系数',
     '其中$\\alpha_{\\text{ens}}=0.4$，$\\beta_{\\text{ens}}=0.8$为平衡系数'),
    ('OpenSeg Ensemble默认参数$\\alpha=0.4$、$\\beta=0.8$、$\\epsilon=0.2$',
     'OpenSeg Ensemble默认参数$\\alpha_{\\text{ens}}=0.4$、$\\beta_{\\text{ens}}=0.8$、$\\epsilon_{\\text{fuse}}=0.2$'),
    ('其中$\\epsilon=0.2$控制SAM零样本掩码在未见类别上的融合权重',
     '其中$\\epsilon_{\\text{fuse}}=0.2$控制SAM零样本掩码在未见类别上的融合权重'),
    # 融合公式中的 alpha/beta/epsilon
    ('p_i(j) = \\begin{cases} (p_{i,d}(j))^{1-\\alpha} \\cdot (p_{i,\\mathrm{cl}}(j))^\\alpha, & j \\in \\mathcal{C}_{\\text{train}}, \\\\ (p_{i,d}(j))^{1-\\beta} \\cdot (p_{i,\\mathrm{cl}}(j))^\\beta, & \\text{otherwise}, \\end{cases}',
     'p_i(j) = \\begin{cases} (p_{i,d}(j))^{1-\\alpha_{\\text{ens}}} \\cdot (p_{i,\\mathrm{cl}}(j))^{\\alpha_{\\text{ens}}}, & j \\in \\mathcal{C}_{\\text{train}}, \\\\ (p_{i,d}(j))^{1-\\beta_{\\text{ens}}} \\cdot (p_{i,\\mathrm{cl}}(j))^{\\beta_{\\text{ens}}}, & \\text{otherwise}, \\end{cases}'),
    ('\\hat{r}_{[x,y]}(j) = \\begin{cases} r_{[x,y]}(j), & j \\in \\mathcal{C}_{\\text{train}}, \\\\ (1-\\epsilon) r_{[x,y]}(j) + \\epsilon r\'_{[x,y]}(j), & \\text{otherwise}, \\end{cases}',
     '\\hat{r}_{[x,y]}(j) = \\begin{cases} r_{[x,y]}(j), & j \\in \\mathcal{C}_{\\text{train}}, \\\\ (1-\\epsilon_{\\text{fuse}}) r_{[x,y]}(j) + \\epsilon_{\\text{fuse}} r\'_{[x,y]}(j), & \\text{otherwise}, \\end{cases}'),
    # 阈值 xi 保持；温度 tau 保持
]

for old, new in mask_rules:
    n = s.count(old)
    print('  %-60s %d' % (old[:58], n))
    s = s.replace(old, new)

save(p, s)
print('saved', p)
