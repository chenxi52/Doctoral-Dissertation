import io

def load(p):
    return io.open(p, encoding='utf-8').read()

def save(p, s):
    io.open(p, 'w', encoding='utf-8').write(s)

B = chr(92)

# ---------------- chap1 ----------------
p = 'body/chap1.tex'
s = load(p)
print('=== chap1 ===')
r1 = [
    ('提出基于特征聚合的不确定性感知伪标签去噪方法 UPA，',
     '提出基于特征聚合的不确定性感知伪标签去噪方法（Uncertainty-aware Pseudo-label-filtering Adaptation, UPA），'),
    ('提出基于选择性扫描的不确定性感知迁移方法 SfMamba，',
     '提出基于选择性扫描的不确定性感知迁移方法（SfMamba），'),
    ('提出跨模型先验融合的开放词汇分割方法 CMPF，',
     '提出跨模型先验融合的开放词汇分割方法（Cross-Model Prior Fusion, CMPF），'),
    ('提出基于多模态基础模型引导的双主动域适应方法 DAMF，',
     '提出基于多模态基础模型引导的双主动域适应方法（Dual Active Multi-modal adaptation Framework, DAMF），'),
]
for old, new in r1:
    print('  %-56s %d' % (old[:54], s.count(old)))
    s = s.replace(old, new)
save(p, s)

# ---------------- chap2 ----------------
p = 'body/chap2.tex'
s = load(p)
print('=== chap2 ===')
r2 = [
    ('本章提出基于特征聚合的不确定性感知伪标签去噪方法UPA，',
     '本章提出基于特征聚合的不确定性感知伪标签去噪方法（Uncertainty-aware Pseudo-label-filtering Adaptation, UPA），'),
    ('本章在判别层去噪机制的基础上进一步提出基于选择性扫描的不确定性感知迁移方法 SfMamba，',
     '本章在判别层去噪机制的基础上进一步提出基于选择性扫描的不确定性感知迁移方法（SfMamba），'),
    ('我们提出了一种新颖的伪标签去噪机制 APS，该机制通过近邻样本来迭代评估样本的不确定性：',
     '我们提出了一种新颖的伪标签去噪机制（Adaptive Pseudo-label Selection, APS），该机制通过近邻样本来迭代评估样本的不确定性：'),
    ('为此，本文提出类感知对比学习CACL策略，',
     '为此，本文提出类感知对比学习（Class-Aware Contrastive Learning, CACL）策略，'),
    ('本文提出了语义一致性打乱 SCS 策略。',
     '本文提出了语义一致性打乱（Semantic-Consistent Shuffle, SCS）策略。'),
    ('通道级视觉状态空间模块抑制表征层不确定性；',
     '通道级视觉状态空间模块（Channel-wise Visual State-Space, Ch-VSS）抑制表征层不确定性；'),
]
for old, new in r2:
    print('  %-56s %d' % (old[:54], s.count(old)))
    s = s.replace(old, new)
save(p, s)

# ---------------- chap3 ----------------
p = 'body/chap3.tex'
s = load(p)
print('=== chap3 ===')
r3 = [
    ('    \\item DAMF 双主动学习框架：首次将视觉—语言模型引入稀缺标注条件下的模型迁移框架，',
     '    \\item DAMF（Dual Active Multi-modal adaptation Framework）双主动学习框架：首次将视觉—语言模型引入稀缺标注条件下的模型迁移框架，'),
    ('本节提出双聚焦主动样本选择器 DFSelector，',
     '本节提出双聚焦主动样本选择器（Dual-Focused active sample Selector, DFSelector），'),
    ('（3）跨模型对齐损失 $L(h(x),g_V(x))$。本方法通过 DFSelector、APT 和 ADL 三个模块分别',
     '（3）跨模型对齐损失 $L(h(x),g_V(x))$。本方法通过 DFSelector、APT（Adaptive Prompt Tuning）和 ADL（Alternating Distillation）三个模块分别'),
]
for old, new in r3:
    print('  %-56s %d' % (old[:54], s.count(old)))
    s = s.replace(old, new)
save(p, s)

# ---------------- chap4 ----------------
p = 'body/chap4.tex'
s = load(p)
print('=== chap4 ===')
r4 = [
    ('为突破上述瓶颈，本章提出基于跨模型先验融合的开放词汇分割方法 CMPF。',
     '为突破上述瓶颈，本章提出基于跨模型先验融合的开放词汇分割方法（Cross-Model Prior Fusion, CMPF）。'),
]
for old, new in r4:
    print('  %-56s %d' % (old[:54], s.count(old)))
    s = s.replace(old, new)
save(p, s)

print('done')
