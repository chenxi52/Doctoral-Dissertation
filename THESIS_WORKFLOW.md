# 博士论文书写工作流（THESIS_WORKFLOW）

> 本文件是本仓库博士论文的**完整工作流手册**。
> 目标：把"从打开 IDE → 写完一章 → 编译通过 → 终稿校对"的全过程拆成可重复执行的阶段、命令、质量门禁。
> 读者：作者本人 + 任何在此仓库工作的 AI agent（Cursor / Claude Code / Codex / subagent）。
>
> 一句话定位：**这是仓库的"操作手册 + 工序卡 + 红线图"**，不是论文正文的一部分，不要 `\input{}` 进 `thesis.tex`。

> **使用阶段划分：**
>
> | 阶段 | 模式 | 何时做 |
> | --- | --- | --- |
> | §1–§9（章节撰写、编译、参考文献、back/* 等） | **逐章迭代（per-chapter）** ——一次只动一章，章节内部自闭环即可 | 当前阶段。每次开新窗口默认在这里 |
> | §10 终稿校对（含整文一致性扫描） | **整文一次性** ——全章节 ✅ + 所有 back/* 写完之后再做 | **所有章节 ✅ 且 `back/*` 写完后才启动** |
>
> **不要混淆**：在逐章阶段如果看到其他章节有 warning / 引用不一致 / 编号不统一，**不动**——那是阶段 10 的事。判断标准：每章自己的 `compile exit 0` + 章节内 `comm -23` 为空 + 章节内 0 占位 = 本章节闭环。

---

## 0. 仓库契约（红线先看）

来自 `AGENTS.md`，所有 agent 必读、必守：

| 红线 | 含义 | 误操作恢复 |
| --- | --- | --- |
| `papers/**` 只读 | `.tex` / `.pdf` / `.bib` / 图片 / 辅助文件一律**不可写、不可删、不可改名** | `git checkout -- papers/` 或重新拷贝 |
| 正本位置 | 论文正文 `body/chap1.tex`…`chap5.tex`；前后 `back/*`；主文件 `thesis.tex`；参考文献 `reference.bib` | — |
| 图源引用 | `\includegraphics{papers/DAMF/...pdf}` 合法 | — |
| 公式/表格模板复用 | 从 `papers/**/main_re.tex` 借鉴结构 → **重写到 `body/`**，不要就地改 `papers/` | 拷贝到 `body/` 之前先备份原文 |
| 用户授权例外 | 如果用户显式说"改 `papers/...`"，执行时必须在汇报里单列"已修改只读参考区 `papers/...`" | 同上 |

**触发告警的三种情形**（agent 看到就要停下反问）：
1. 用户要求修改 `papers/DAMF/main_re.tex` 等 LaTeX 源。
2. `cp papers/X/main_re.tex body/` 之后又被要求就地微调 `papers/X/` 同名文件。
3. `latexmk` / `make` / `git commit` 等命令被建议在 `papers/` 内执行。

---

## 1. 工具链与编译环境

### 1.1 必须就绪

```bash
which xelatex latexmk bibtex splitindex makeindex
```

- 必须有：`xelatex`、`latexmk`；可选但强烈建议：`bibtex`、`splitindex`、`makeindex`。
- 字体：模板自带 `fontset=fandol`（哈工大 hithesis 默认），若改用 macOS 系统字体需在 `thesis.tex` 调整 `\documentclass` 选项。

### 1.2 仓库内已有的两套配置

| 文件 | 角色 | 备注 |
| --- | --- | --- |
| `.latexmkrc` | `latexmk` 默认入口；`$max_repeat=5`，xelatex，synctex | **优先用这一个**：`latexmk -xelatex thesis` |
| `latexmkrc`（根目录小写） | 老配置，`$pdf_mode=1`、用 `splitindex` 替代 `makeindex` | 用于显式 `latexmk -r latexmkrc` 时覆盖默认 |
| `Makefile` | `make thesis` / `make viewthesis` / `make clean` | 等价于手动调用 `latexmk -xelatex thesis` |

### 1.3 编译命令速记

```bash
# 全量编译（含 bibtex + splitindex + 索引）
latexmk -xelatex thesis

# 只跑一次（debug 阶段用，看错误不自动重跑）
latexmk -xelatex -interaction=nonstopmode thesis

# 清理中间产物
latexmk -c thesis

# 彻底清理（含 thesis.pdf）
make cleanall

# 预览
make viewthesis        # macOS：open thesis.pdf
```

`$max_repeat=5` 保证冷启动（xelatex → bibtex → xelatex → xelatex + splitindex）能收敛；如果你看到"未定义引用 / 索引"重复出现，先 `make cleanall` 再 `latexmk -xelatex thesis`。

---

## 2. 全局流水线（十阶段）

每个阶段都有"输入 → 动作 → 产物 → 退出条件"四要素。任何阶段未达退出条件不要跳到下一阶段。

| # | 阶段 | 关键产物 | 退出条件 |
| --- | --- | --- | --- |
| 1 | 总体计划 & 章节地图 | 本文件第 4 节的章节状态表 | 每章状态打勾、负责人（你自己）确认 |
| 2 | 阅读 & 资料抽取 | `body/<chap>.tex` 的草稿 outline | outline 与论文章节小标题一一对应 |
| 3 | 章节正文撰写 | 填满 outline 的完整段落 | 每个 `\section` 都有 ≥ 3 段中文论述 |
| 4 | 图 / 表 / 公式 | `\includegraphics` + `\bicaption` + 编号 | LaTeX 编译后图、公式、表交叉引用全部生成 |
| 5 | 参考文献 | `reference.bib` + 正文 `\cite{}` | `Citation 'X' undefined` 警告消失 |
| 6 | 编译 & 错误修复 | `thesis.pdf` 无错误 | `latexmk` 退出码为 0、`thesis.log` 无 `!` 行 |
| 7 | 交叉引用一致性 | 所有 `\ref{fig:...}` `\ref{tab:...}` `\ref{eq:...}` 生效 | `LaTeX Warning: There were undefined references` 为 0 |
| 8 | 前置 / 后置内容 | 摘要、目录、`back/conclusion.tex`、`back/acknowledgements.tex`、`back/resume.tex` | 中文 / 英文摘要齐；致谢、简历、结论均过稿 |
| 9 | 排版 & 排印检查 | 字号、间距、章节对齐 | 抽样 5 页无 overfull / underfull warning |
| 10 | 终稿校对 | 提交版 PDF | 答辩决议、授权页排好；`thesis.pdf` < 50 MB；图清晰 |

> **不要跳阶段**。第五章 AER-Bench 的草稿（`body/chap5.tex`）当前还是骨架，按本流程从阶段 2 进入。

---

## 3. 每章工作流模板（通用 SOP）

无论哪一章，下面这套 8 步动作都适用：

1. **读材料**
   - 从 `papers/<对应论文>/main_re.tex`（或 `clean_manuscript.tex` 等正文源）读章节。
   - 读 `papers/<对应论文>/main_re.bbl` 提取本论文的参考文献条目。
   - 注意：`papers/` 内一切**只读**（红线见 §0）。

2. **抽骨架**
   - 在脑中列出 4~6 个 `\subsection` 标题，对应论文的 § 几。几。
   - 与 `body/<chap>.tex` 当前大纲对比，缺口标红。

3. **填正文**
   - 一节一节写；每节先写**中文论述**，再放公式 / 表格 / 图。
   - 数学符号、缩写第一次出现时给中文 + 英文（`源域（Source Domain, SD）`），后续可只用中文或缩写。

4. **插图**
   - 优先级：\1) 仓库 `figures/<chap>/*.pdf`；\2) `papers/<对应论文>/xx.pdf` 直接引用；\3) 从 `papers/<...>.pdf` 截屏落到 `figures/<chap>/`（脚本工具见 §6.5）。
   - 统一用 `\bicaption[fig:key]{}{中文标题}{Fig.}{English title}`（hithesis 提供的双语 caption 宏）。

5. **加表 / 公式**
   - 表：统一 `\bicaption[tab:key]{}{中文}{Table}{English}` + `\label{tab:key}`。
   - 公式：`\begin{equation} \label{eq:key} ... \end{equation}`，不要在行内用 `\label`。

6. **加引用**
   - 论文里出现的所有方法 / 数据集 / 关键结论都要有 `\cite{}`，key 与 `reference.bib` 对齐。
   - 缺条目 → 按 §5 流程添加。

7. **章节内自检**
   - `latexmk -xelatex -interaction=nonstopmode thesis`：零 `!` 错误，章节 `aux` 文件生成。
   - `grep -n "TODO\|FIXME\|XXX\|占位\|待核验" body/<chap>.tex`：必须为 0 行（终稿前）。

8. **章节收尾**
   - 在章节末尾写一段"本章小结"（chap1 除外），1~3 段，承接下一章。

---

## 4. 章节地图（chapter-by-chapter）

仓库现状按行数（`wc -l body/*.tex back/*.tex`）盘点如下；状态在"状态"列。

| 章节 | 文件 | 行数 | 状态 | 主要参考稿 | 关键产出 |
| --- | --- | --- | --- | --- | --- |
| 绪论 | `body/chap1.tex` | 211 | ✅ 已写完，需与各章对齐小节编号 / 引用 | 无（综述） | 研究背景 / 现状 / 创新点 / 论文结构 |
| 基于 CNN 和选择性扫描机制的无源域适应方法（UPA / SfMamba） | `body/chap2.tex` | — | ✅ 主体完，需补消融表与可视化 | `papers/UPA/clean_manuscript.tex` + `papers/Sfmamba/main_re.tex` | APS + CACL / Ch-VSS + SCS；VisDA-C / Office-Home / DomainNet |
| 多模态基础模型引导的主动无源域适应方法（DAM / DAMF） | `body/chap3.tex` | — | ✅ 主体完，需补风险上界附录 | `papers/DAMF/main_re.tex` | DFSelector + APT + ADL；闭 / 开集 |
| 跨模型先验融合驱动的开放词汇分割方法（CMPF） | `body/chap4.tex` | — | ⚠️ 骨架偏薄（仅引言+框架），方法与实验段需扩写 | `papers/` 内对应手稿 | Query / Feature Injector + OpenSeg Ensemble |
| 面向艺术情感推理的多层级视觉语义评测基准（AER-Bench） | `body/chap5.tex` | — | 🔴 **当前为骨架，必须从阶段 2 进入本工作流撰写** | `papers/AER-Bench.pdf` | perception / emotion&VAD / reasoning / description 四层 + 14 个 MLLM 评测 |
| 结论 | `back/conclusion.tex` | 8 | 🔴 仅有模板说明，需写正文 | 无 | 三部分：成果 / 创新点 / 展望 |
| 答辩决议 | 模板宏 `\resolution` | — | ✅ 用电子版宏即可 | — | — |
| 索引 | `back/ceindex.tex` | 4 | ✅ 模板骨架 | — | — |
| 发表论文 | `back/publications.tex` | 24 | ⚠️ 需对照实际发表列表核对 | — | — |
| 致谢 | `back/acknowledgements.tex` | 9 | 🔴 待写 | 无 | — |
| 简历 | `back/resume.tex` | 16 | 🔴 待写 | 无 | — |
| 摘要 | `front/*.tex` | — | ⚠️ 摘要模板由 hithesis 类生成，必要时单独维护 | — | 中英摘要 ≥ 300 字 |

> 状态图标：✅ 完成 / ⚠️ 需补 / 🔴 缺主体。

### 4.1 chap5（AER-Bench）执行路径（接续你上一轮的提问）

1. **读论文**：`papers/AER-Bench.pdf`（13 MB，IEEE TPAMI 风格）。提取：
   - § 几。数据集统计（2,058 件 / 24,792 单图 / 9,999 配对）；
   - § 几。四层级（perception / emotion&VAD / reasoning / description）；
   - § 几。模板化题生成 + 评测协议；
   - § 几。14 个 MLLM 评测表与四个核心 finding。

2. **当前骨架**（`body/chap5.tex`）已留好 `\section{AER-Bench 设计} / {任务构造与评测协议} / {数据分析} / {实验结果与发现} / {本章小结}`，按 §3 SOP 逐节填实。

3. **图源**：`\includegraphics{papers/AER-Bench/figures/...pdf}`（如该子目录无拆图，用 `papers/AER-Bench.pdf` 的对应页截屏落到 `figures/chap5/`，命名 `fig_aerbench_<n>.pdf`）。

4. **引用**：正文涉及"情感心理学 / Arnheim / Berlyne / Warriner VAD / WikiArt"等需在 `reference.bib` 补齐条目，key 建议 `<作者首字母><年><关键词>` 形式。

---

## 5. 参考文献工作流

### 5.1 `reference.bib` 现状

- 1588 行，已积累 UPA / SfMamba / DAM / DAMF / CMPF 的核心条目；
- 仍可能缺：AER-Bench（自引）、Arnheim 1954、Berlyne、Warriner 2013 等艺术与情感心理学经典条目。

### 5.2 添加新条目

```bash
# 1) 编辑 reference.bib，按 BibTeX 规范
# 2) 在 body/<chap>.tex 用 \cite{key}
# 3) 重新编译（自动跑 bibtex）
latexmk -xelatex thesis
```

### 5.3 引用核验

```bash
# 找出正文中所有 \cite{...} 引用的 key
grep -hoE '\\cite\{[^}]+\}' body/*.tex back/*.tex | \
  sed -E 's/\\cite\{([^}]+)\}/\1/g' | tr ',' '\n' | sort -u > /tmp/cited_keys.txt

# 找出 reference.bib 中所有 entry key
grep -E '^@' reference.bib | sed -E 's/@[a-zA-Z]+\{([^,]+),/\1/' | sort -u > /tmp/bib_keys.txt

# 差集 = 缺失或多余
comm -23 /tmp/cited_keys.txt /tmp/bib_keys.txt   # 正文用但 bib 缺 → 必补
comm -13 /tmp/cited_keys.txt /tmp/bib_keys.txt   # bib 多余 → 可清理
```

每次写完一章跑一次，把 diff 清零再进入下一章。

### 5.4 BibTeX style

模板自带 `gbt7714-numerical-quanjiao.bst`（GB/T 7714 全角数字编号）和 `hithesis.bst`；`thesis.tex` 当前用的是后者（`\bibliographystyle{hithesis}`）。换 style 会改变正文排版，**不要中途切换**。

---

## 6. 编译错误速查

### 6.1 缺字体（`xeCJK` 警告）

```text
! LaTeX Error: File `xxx.sty' not found.
```

- 解决：`tlmgr install xxx`（TeX Live）或装 `texlive-xetex` + `texlive-fonts-extra`。
- macOS 备选：`brew install --cask mactex`。

### 6.2 未定义引用 / 引用

```text
LaTeX Warning: Citation 'chen2024upa' undefined.
LaTeX Warning: There were undefined references.
```

- 先跑一次 `latexmk -xelatex thesis` 让 aux 文件生成；再跑 bibtex；再跑两次 xelatex。
- 仍存在 → 检查 `reference.bib` 的 key 是否与 `\cite{}` 完全一致（区分大小写）。

### 6.3 `splitindex` / `makeindex` 索引未生成

```text
! I can't find file `thesis_english.ind'.
```

- 老配置 `latexmkrc` 已经把 makeindex 替换为 splitindex；显式用 `latexmk -r latexmkrc thesis`。
- 或者：`make thesis`（走 Makefile 内置的 splitindex 链）。

### 6.4 图找不到

```text
! LaTeX Error: File `figures/foo.png' not found.
```

- 仓库 `\graphicspath{{figures/}}`（在 `thesis.tex`），所以路径写 `figures/<chap>/foo.png` 或 `<chap>/foo.png`。
- 直接引用 `papers/<...>/xx.pdf` 也可以，但**只在 papers/ 只读的前提下**。

### 6.5 图从 PDF 截屏 / 抽取

```bash
# 用 macOS 自带的 sips / Quartz 抽取单页
sips -s format png papers/AER-Bench.pdf --out /tmp/aer_page.png
# 仅抽取第 6 页
sips -s format pdf papers/AER-Bench.pdf --out /tmp/aer_p6.pdf
```

或者安装 `pdftoppm`（`brew install poppler`，需要 sudo 改 Homebrew 所有权时换 conda 装 poppler），落到 `figures/chap6/fig_aerbench_<n>.pdf`。

### 6.6 overfull / underfull 警告

- `Overfull \hbox ...`：行宽超界，常因 `verbatim`、长 URL、长公式；可用 `\sloppy`、断行或换字体。
- `Underfull \hbox ...`：可忽略（LaTeX 排版常见）。
- `Overfull \vbox ...`：通常是图片太大；用 `\includegraphics[width=...]{...}` 控制比例。

---

## 7. 写作质量门禁

### 7.1 引用规范

- 正文 `\cite{a, b}` → 用逗号 + 空格：`\cite{a, b}`，不要 `\cite{a,b}`。
- 同一处引用 3 个以上 → 用 `\cite{a,b,c}`。
- 不出现的 bib 条目 → 删除（`comm -13` 阶段 §5.3）。

### 7.2 图 / 表 / 公式编号

- 编号交给 LaTeX：永远不要手写"图 3.1"。
- 章节内用 `\bicaption[fig:chapN_key]{}{中文}{Fig.}{English}` + `\label{fig:chapN_key}`。
- 公式用 `\begin{equation} \label{eq:chapN_key} ... \end{equation}`。

### 7.3 用词一致性（建立术语表）

仓库当前一致使用的术语（请勿在新增章节里改写）：

| 中文 | 英文 / 缩写 | 出处章节 |
| --- | --- | --- |
| 源域 / 目标域 | Source Domain / Target Domain | chap2–4 |
| 无源域适应 | Source-Free Domain Adaptation, SFDA | chap2–4 |
| 自适应伪标签选择 | Adaptive Pseudo-label Selection, APS | chap2 |
| 类感知对比学习 | Class-Aware Contrastive Learning, CACL | chap2 |
| 通道级视觉状态空间 | Channel-wise Visual State-Space, Ch-VSS | chap2 |
| 语义一致性打乱 | Semantic-Consistent Shuffle, SCS | chap2 |
| 双聚焦主动样本选择器 | DFSelector | chap3 |
| 自适应提示微调 | Adaptive Prompt Tuning, APT | chap3 |
| 交替蒸馏 | Alternating Distillation, ADL | chap3 |
| 查询注入器 / 特征注入器 | Query / Feature Injector | chap4 |
| 开放集合集成 | OpenSeg Ensemble | chap4 |
| 感知维度 / 情感与 VAD / 推理 / 描述 | perception / emotion&VAD / reasoning / description | chap5 |

新增术语请同步在本表登记，保持中英对照。

### 7.4 一句话长度 / 段落结构

- 中文段落 4~8 句；段首给主题句，段尾给衔接句。
- 章节首段必须以一句话概括"本章要解决什么问题 / 怎么解决"。
- 章节末段必须以一句话给出"承上启下"。

---

## 8. 与 AI 协作的约定

### 8.1 让 agent 写一段时的输入格式

```text
请基于 papers/<X>/main_re.tex §<n> 在 body/chap<N>.tex 第 §<m> 节追加正文。
要求：
- 不修改 papers/ 内任何文件；
- 仅写入 body/chap<N>.tex；
- 中英术语第一次出现时给中英对照；
- 涉及图表的引用请使用 \includegraphics{papers/<X>/figures/<f>.pdf}；
- 不要在 body/chap<N>.tex 里留 TODO/FIXME/占位字样。
```

### 8.2 agent 汇报模板（每完成一章让 agent 用这个）

```markdown
## 完成报告：chap<N>

- 改了什么：<具体行号 / 段落>
- 没改什么：papers/ 下任何文件（红线已遵守）/ 其他章节
- 编译：`latexmk -xelatex thesis` 退出码 0 / 还有 N 个 warning
- 引用：新增 N 个 bib 条目，键值 `[xxx]`；`comm -23` 差集为空
- 待你 review 的地方：<具体段落>
- 风险：<任何潜在语义错误 / 引用错位>
```

### 8.3 subagent 边界（与根规则呼应）

- subagent 默认无写 `papers/` 权限；用 prompt 显式重申 §0 的红线。
- 写 `body/` 时必须用绝对路径。
- 用 `Task` 工具时，prompt 末尾加一句："完成后请按 §8.2 汇报模板输出。"

---

## 9. 终稿 checklist

提交前 24 小时逐项核对：

- [ ] `latexmk -xelatex thesis` 退出码 0，零 `!` 错误
- [ ] `grep -n "TODO\|FIXME\|占位\|待核验" body/*.tex back/*.tex` 为空
- [ ] 所有 `\cite{}` 在 `reference.bib` 中存在（§5.3 diff = 0）
- [ ] 所有 `\ref{}` 都能正确解析（`thesis.log` 无 undefined reference）
- [ ] 中英文摘要完整（hithesis 类自动生成，需要 `front/` 下维护）
- [ ] `back/conclusion.tex` 含"主要成果 / 创新点 / 展望"三部分
- [ ] `back/acknowledgements.tex` 已写（导师 / 实验室 / 家人）
- [ ] `back/resume.tex` 已写（教育背景 / 研究方向）
- [ ] `back/publications.tex` 与实际发表 / 在投列表一致
- [ ] 论文 PDF 大小 < 50 MB（hithesis 要求）
- [ ] 抽样 10 页：无 overfull / underfull 关键警告
- [ ] 章节地图（§4）中所有状态从 🔴 / ⚠️ 变成 ✅
- [ ] 答辩决议、授权页正常排版（`\resolution` / `\authorization`）
- [ ] 索引（`back/ceindex.tex`）跑 splitindex 后不报缺文件

---

## 10. 变更日志

| 日期 | 变更 | 作者 |
| --- | --- | --- |
| 2026-09-21 | 初版：建立工作流 + 章节地图 | Cursor (Claude Sonnet 5) |
