# 全文统一符号约定（一次性定稿，全篇各章不得偏离）

> 目的：正本 `body/chap2..5.tex` + `extras/optional-back/appA.tex` + `extras/optional-back/appB.tex`
> 共用同一套符号；全文符号表放在 `front/vocab.tex`（摘要之后、目录之前）。

## 0. 冲突清单（改动前的实际情况）

| 概念 | 第2章 | 第3章 | 第4章 | 第5章 | 冲突性质 |
|---|---|---|---|---|---|
| 源域数据 | `\mathcal{D}_s` | `\mathcal{S}` | — | — | 同概念两符号 |
| 目标域数据 | `\mathcal{D}_t` | `\mathcal{T}` | — | — | 同概念两符号 |
| 已标注数据集 | — | `\mathcal{L}` / `\mathscr{L}` | — | — | 与损失符号 `\mathcal{L}` 撞车 |
| 干净样本集 | `\mathcal{H}` | `\mathcal{H}`（=假设空间！） | — | — | 同符号两概念 |
| 损失函数 | `\mathcal{L}`（整体） | `L`（标量） | — | — | 三套损失记号 |
| 熵 / 多样性项 | `\mathcal{L}_{\text{ent}}` | `\mathcal{L}_{ent}` | — | — | 同概念两写法 |
| 交叉熵项 | `\mathcal{L}_{\text{CE}}` | `\mathcal{L}_{ce}` | — | — | 同概念两写法 |
| 知识保持项 | — | `\mathcal{L}_{kg}` / `\mathcal{L}_{\text{kg}}` | — | — | 同概念两写法 |
| 蒸馏损失 | — | `\mathcal{L}_{T\leftarrow V}^{dist}` / `\mathcal{L}_{dis}^{V\rightarrow T}` | — | — | 同概念两写法 |
| Rademacher 复杂度 | — | `\mathfrak{R}` / `\mathcal{R}` | — | — | 同概念两符号 |
| prompt 模板 | — | `V_k` / `\mathbb{V}_k` | — | — | 同概念两符号 |
| ViL 图像特征 | — | `I` / `\mathbf{I}` | — | — | 同概念两符号 |
| 文本嵌入 | — | `w_k` / `\mathbf{w}_k` | — | — | 同概念两符号 |
| ViL 假设 | — | `g`（=特征提取器） | — | — | 同符号两概念 |
| ViL 特征空间距离 | — | `d_Z` / `d_{\mathcal{Z}}` | — | — | 同概念两符号 |
| 模型（算法块） | `\phi` | `\theta_t`（`\phi`=编码器） | — | — | 同符号两概念 |
| 批大小 / 标注预算 | `B` | `B` | — | — | 同符号两概念 |
| 筛选比例 | `\gamma` | — | — | — | 第2章内部两义 |
| 类别内保留比例 | `\gamma` | — | — | — | 第2章内部两义 |
| 近邻数 / 类别数 | `K` | `N` | `N` | `K` | 跨章撞车 |
| 解码层数 / 块数 | `L` | — | `L` | — | 跨章撞车 |
| 损失上界 / 掩码 | — | `M` | `M` | — | 跨章撞车 |
| 类别数 / 情感标注对象 | — | `C` | — | `C` | 跨章撞车 |
| 标注对象 | — | — | — | `S`/`C`/`R`/`A` | 与 `\mathcal{S}`/`C` 撞车 |
| 统计量 / 假设空间 | — | `\mathcal{H}` | — | `H` | 撞车 |
| 概率 / p 值 / 惩罚 | — | — | — | `p`（两义） | 第5章内部两义 |
| 温度 | `\tau` | `\tau` | `\tau` | — | 一致 ✅ |
| 投影函数 | — | — | `E_p`（两义） | — | 第4章内部两义 |

## 1. 定稿约定

### 1.1 数据与域
- `\mathcal{S}` 源域数据集；`\mathcal{T}` 目标域数据集
- `\mathcal{T}_c` 干净伪标签样本集（第2章）
- `\mathcal{T}_q` 主动标注的目标样本子集（第3章）
- `\mathcal{T}_{CO}` / `\mathcal{T}_{MH}` Core-Set / MH 点集（第3章）
- `\mathcal{D}_l` 已标注数据集 = `\mathcal{S}\cup\mathcal{T}_q`（第3章）
- `P` 目标域分布，`Q` 源域分布（统一到第3章 / DA 理论惯例）
- `\hat{P}` / `\hat{Q}` / `\tilde{Q}` 经验分布

### 1.2 假设空间与理论
- `\mathcal{H}` / `\mathcal{G}`：源模型 / ViL 假设空间；`h` / `g_V`：其中的假设
- `L` 标量损失；`M` 损失上界；`\mathcal{L}_{\mathcal{D}}(h,h')` 经验风险
- `\mathcal{L}` / `\mathcal{L}_{\text{...}}`：可训练损失项（与标量 `L` 区分）
- `\eta_{\mathcal{H}}` / `\eta'_{\mathcal{H}}` / `\eta_{\mathcal{G}}` 理想最大误差；`\eta` 学习率
- `\mathfrak{R}_{n_t}` Rademacher 复杂度（统一 `\mathfrak{}`）

### 1.3 模型与多模态
- `\theta_s` / `\theta_t` / `\theta_v`：源 / 目标 / ViL 模型
- `g` / `f`：特征提取器 / 分类器（仅第2章）
- `\phi`：ViL 图像编码器；`\mathcal{Z}`：ViL 特征空间；`\mathbf{I}`：ViL 图像特征
- `V_k` / `c_k` / `\mathrm{Enc}_t` / `\mathbf{w}_k`：prompt 模板 / 类别名 / 文本编码器 / 文本嵌入
- `\tau`：温度参数（全文）

### 1.4 损失项（统一加 `\text{}`）
- `\mathcal{L}_{\text{ent}}` / `\mathcal{L}_{\text{div}}` / `\mathcal{L}_{\text{IM}}`
- `\mathcal{L}_{\text{CE}}` / `\mathcal{L}_{\text{CL}}` / `\mathcal{L}_{\text{KL}}` / `\mathcal{L}_{\text{kg}}`
- `\mathcal{L}_{T}` / `\mathcal{L}_{V}` / `\mathcal{L}_{C}`
- `\mathcal{L}_{T\leftarrow V}^{dist}` / `\mathcal{L}_{V\leftarrow T}^{dist}`

### 1.5 第2章专有
- `\hat{y}_t` / `\hat{p}_t` / `q_t`；`\mathcal{N}_t` / `K`；`z_i`
- `\mathcal{O}(i)` / `\mathcal{J}(i)` / `\mathcal{A}(i)` / `\mathcal{I}`
- `B_{\text{batch}}` / `\beta_{\text{CE}}` / `\gamma_{\text{sel}}`（筛选比例）/ `\gamma_{\text{bg}}`（背景比例）
- `N_p`（patch token 数）/ `L_{\text{vss}}`（Ch-VSS 块数）
- `U` / `\tilde{U}`（SCS 打乱前后序列）/ `P_k`（背景 patch）
- `d(\cdot,\cdot)` 余弦相似度；`\delta`→`\mathrm{softmax}`

### 1.6 第3章专有
- `\pi` / `B`（标注预算）/ `\rho` / `\alpha`（Core-Set 权重）
- `\mathcal{X}_{top}` / `N`（每类保留数）
- `m_{A\leftarrow B}` / `\Pi_{A\leftarrow B}` / `\beta_q` / `\beta` / `\lambda`

### 1.7 第4章专有
- `L_{\text{dec}}`（解码层数）/ `N_q`（查询数）
- `\mathcal{M}^l` / `\mathcal{M}` / `m_i`（掩码族，避让第3章 `M` 损失上界）
- `E_m` / `E_p` / `E_{aux}` / `E_c`（`E_p` 只表空间查询投影，掩码辅助投影改 `E_{aux}`）
- `P_d` / `P_{\text{cl}}` / `P_{\text{sam}}`
- `\alpha_{\text{ens}}` / `\beta_{\text{ens}}` / `\epsilon_{\text{fuse}}` / `\xi`

### 1.8 第5章专有
- `\mathcal{O}_{\text{per}}` / `\mathcal{O}_{\text{emo}}` / `\mathcal{O}_{\text{rea}}` / `\mathcal{O}_{\text{des}}`
  （对应标注 JSON 字段 `S` / `C` / `R` / `A`）
- `S_{\text{Top3}}` / `\alpha_{\text{top3}}` / `S_{\text{VAD}}` / `p_{\text{pen}}`
- `H_{\text{KW}}` / `K_{\text{emo}}` / `\epsilon^2` / `V`（Cramer's V）
- `\mathrm{Hit@3}` / `\mathrm{NDCG@3}`
- `\alpha`（Krippendorff 一致性系数）保留

### 1.9 全局
- `\mathcal{X}` 样本空间；`\mathcal{Y}` 标签空间；`\mathcal{C}` 类别集合；`C` 类别数
- `\epsilon` 误差容忍度；`\delta` 置信水平参数
- `$x$` / `$y$` 样本 / 标签；`n_s` / `n_t` 样本数

## 2. 符号表格式（front/vocab.tex）
- 位置：摘要之后、目录之前（`thesis.tex` 中 `\makecover` 之后）
- 载体：类内置 `denotation` 环境（自带目录项 + 表号重置为"表 1"），标题改为「符号说明表」
- 表格：`longtable` 三列「符号 | 含义 | 章节」，按主题分组，长表跨页自动重复表头
