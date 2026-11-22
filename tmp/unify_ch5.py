import io

def load(p):
    return io.open(p, encoding='utf-8').read()

def save(p, s):
    io.open(p, 'w', encoding='utf-8').write(s)

B = chr(92)

# ============ chap5 ============
p = 'body/chap5.tex'
s = load(p)
print('=== chap5 ===')

rules5 = [
    # 情感类别数 K -> K_emo
    ('类别数 $K=12$，检验统计量 $H$、效应量 $\\epsilon^2$ 与渐近 $p$ 值',
     '情感类别数 $K_{\\text{emo}}=12$，检验统计量 $H_{\\text{KW}}$、效应量 $\\epsilon^2$ 与渐近 $p$ 值'),
    # 表头
    ('维度 & $H$ & $\\epsilon^2$ & $p$ \\\\',
     '维度 & $H_{\\text{KW}}$ & $\\epsilon^2$ & $p$ \\\\'),
    # Top-3 排序加权系数 alpha -> alpha_top3（Krippendorff's alpha 保留）
    ('最终的情感排序得分取两者的加权和（$\\alpha=0.5$）：',
     '最终的情感排序得分取两者的加权和（$\\alpha_{\\text{top3}}=0.5$）：'),
    ('S_{\\mathrm{Top3}}=\\alpha\\cdot\\mathrm{Hit@3}+(1-\\alpha)\\cdot\\mathrm{NDCG@3}.',
     'S_{\\text{Top3}}=\\alpha_{\\text{top3}}\\cdot\\mathrm{Hit@3}+(1-\\alpha_{\\text{top3}})\\cdot\\mathrm{NDCG@3}.'),
    ('S_{\\mathrm{VAD}}(\\hat{v},v)=', 'S_{\\text{VAD}}(\\hat{v},v)='),
    # VAD 惩罚系数 p -> p_pen
    ('其中 $p=15$ 当预测与参考落在中性点（值为 3）两侧，$p=5$ 当其一为中性而另一为非中性',
     '其中 $p_{\\text{pen}}=15$ 当预测与参考落在中性点（值为 3）两侧，$p_{\\text{pen}}=5$ 当其一为中性而另一为非中性'),
    # 标注对象 S/C/R/A -> mathcal O
    ('标注规则为：$S$ 为五维感知画像，$C$ 为与 $S$ 一致的情感标签与 VAD 取值，$A$ 为聚焦情感的表述，$R$ 为基于证据的简明推理；$A$ 与 $R$ 中的每一项关键论断都必须给出具体的视觉证据锚点。 \\\\',
     '标注规则为：$\\mathcal{O}_{\\text{per}}$ 为五维感知画像，$\\mathcal{O}_{\\text{emo}}$ 为与 $\\mathcal{O}_{\\text{per}}$ 一致的情感标签与 VAD 取值，$\\mathcal{O}_{\\text{des}}$ 为聚焦情感的表述，$\\mathcal{O}_{\\text{rea}}$ 为基于证据的简明推理；$\\mathcal{O}_{\\text{des}}$ 与 $\\mathcal{O}_{\\text{rea}}$ 中的每一项关键论断都必须给出具体的视觉证据锚点。 \\\\'),
    # Cramer's V 说明
    ("进一步使用 Cramer's V~\\cite{cramer1999mathematical} 列联系数",
     "进一步使用 Cramer's V（列联系数 $V$）~\\cite{cramer1999mathematical}"),
]

for old, new in rules5:
    n = s.count(old)
    print('  %-58s %d' % (old[:56], n))
    s = s.replace(old, new)

save(p, s)
print('saved', p)

# ============ appB ============
p = 'extras/optional-back/appB.tex'
s = load(p)
print('=== appB ===')

rulesB = [
    ('其中须包含五个感知字段（$S$）、情感归因（$C$）、推理字段（$R$）与描述字段（$A$），不允许出现额外字段；',
     '其中须包含五个感知字段（$\\mathcal{O}_{\\text{per}}$）、情感归因（$\\mathcal{O}_{\\text{emo}}$）、推理字段（$\\mathcal{O}_{\\text{rea}}$）与描述字段（$\\mathcal{O}_{\\text{des}}$），不允许出现额外字段；'),
    ('\\item $A$ 与 $R$ 中的每一项关键论断都必须落到具体视觉证据上',
     '\\item $\\mathcal{O}_{\\text{des}}$ 与 $\\mathcal{O}_{\\text{rea}}$ 中的每一项关键论断都必须落到具体视觉证据上'),
    ('    $S$ & 情感线索感知 &', '    $\\mathcal{O}_{\\text{per}}$ & 情感线索感知 &'),
    ('    $C$ & 情感归因 &', '    $\\mathcal{O}_{\\text{emo}}$ & 情感归因 &'),
    ('    $R$ & 解释性推理 &', '    $\\mathcal{O}_{\\text{rea}}$ & 解释性推理 &'),
    ('    $A$ & 情感描述 &', '    $\\mathcal{O}_{\\text{des}}$ & 情感描述 &'),
    ('\\multicolumn{3}{@{}l}{\\itshape \\textbf{情感线索感知（$S$）}} \\\\',
     '\\multicolumn{3}{@{}l}{\\itshape \\textbf{情感线索感知（$\\mathcal{O}_{\\text{per}}$）}} \\\\'),
    ('\\multicolumn{3}{@{}l}{\\itshape \\textbf{情感归因（$C$）}} \\\\',
     '\\multicolumn{3}{@{}l}{\\itshape \\textbf{情感归因（$\\mathcal{O}_{\\text{emo}}$）}} \\\\'),
    ('\\multicolumn{3}{@{}l}{\\itshape \\textbf{解释性推理（$R$）}} \\\\',
     '\\multicolumn{3}{@{}l}{\\itshape \\textbf{解释性推理（$\\mathcal{O}_{\\text{rea}}$）}} \\\\'),
    ('\\multicolumn{3}{@{}l}{\\itshape \\textbf{情感描述（$A$）}} \\\\',
     '\\multicolumn{3}{@{}l}{\\itshape \\textbf{情感描述（$\\mathcal{O}_{\\text{des}}$）}} \\\\'),
    ('作为补充，$C$ 对象中的三个情感标签', '作为补充，$\\mathcal{O}_{\\text{emo}}$ 对象中的三个情感标签'),
    ('$R$ 对象实例化的是正文定义的四种推理类型', '$\\mathcal{O}_{\\text{rea}}$ 对象实例化的是正文定义的四种推理类型'),
    ('一份 $S$ 引用列表', '一份 $\\mathcal{O}_{\\text{per}}$ 引用列表'),
]

for old, new in rulesB:
    n = s.count(old)
    print('  %-58s %d' % (old[:56], n))
    s = s.replace(old, new)

save(p, s)
print('saved', p)
