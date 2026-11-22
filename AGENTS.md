# AGENTS.md

给所有在此仓库工作的 AI agent（Cursor / Claude Code / Codex / subagent）阅读的硬性约束 + 工作流入口。

最后更新：2026-10-08

---

## 你（Agent）每次进来先读什么

1. **本文件（AGENTS.md）** — 红线 + 正本位置 + 章节地图 + 几条速记
2. **[handoff.md](handoff.md)** — 上一窗口做到哪了、下一步是什么
3. **正文（按需）** — 当前章节对应的 `body/chap<N>.tex`
4. **参考稿（按需）** — `papers/<X>/main_re.tex`，**只读**

**工作流不预读。** 需要时按下面"去 THESIS_WORKFLOW.md 找"的映射，按章节读对应位置即可；不要一开始就把整个 370 行读完。上下文很贵。

---

## 红线：写作中禁止滥用 `\textbf{}`

**正文段落（叙述、定义、说明、过渡、结论等纯文字段落）中禁止使用 `\textbf{...}` 做行内视觉强调。** 完整规则见 [.cursor/rules/no-bold-text.mdc](.cursor/rules/no-bold-text.mdc)。

执行要点：

- 用句法重排替代粗体强调（见规则文件「替代方案」）。
- 不适用范围：章节标题、`\caption{}`、表头、固定术语引导词；公式 `\mathbf{}` 不受限。
- 在 body/back/front/thesis.tex 中遇到正文 `\textbf{某段叙述}` → 立即改写，不保留。
- 用户显式要求保留某些 `\textbf{}` 时，视为一次性显式批准，并在汇报里单独标注。

---

## 红线：引言章节末段必须做「本章工作归纳」

**章节首节（`\section{引言}` / `\section{绪论}`）末段必须有「本章工作归纳」段（itemize / enumerate，**恰好 3 项**，**列点内禁止 `\textbf{}`**）；同时禁止只罗列小节标题的章节导览段。** 完整规则见 [.cursor/rules/no-section-roadmap.mdc](.cursor/rules/no-section-roadmap.mdc)。

执行要点：

- **项数**：归纳列点**必须恰好 3 项**。少于 3 项要拆分合并，多于 3 项要合并到 3 项。例外仅在用户显式批准时允许，并在汇报里标注。
- **粗体**：列点内**禁止使用 `\textbf{}`**——这条**覆盖** `no-bold-text.mdc` 第 5 条"列点首词 / 首次出现方法名允许加粗"的豁免条款。需要强调方法名时改用 `XXX` 代码体或 `\emph{XXX}` 斜体。
- **句法**：每项首词点名方法名 / 模块名（不加粗）+ 英文冒号 `:` + 续接一句"做了什么"。
- **正向**：引言末段必须用 itemize / enumerate 列出本章实际做了什么工作。
- **反向**：禁止「本章其余部分组织如下：§X.Y 介绍……」「本节结构如下：…、…、…」「本章共分 N 节：……」这类只复述目录的导览段。
- 判断口诀：段中只出现小节标题 + "介绍/给出/讨论" → 禁止；段中出现"本章工作 + 具体方法名 + 做了什么" → 必须保留。
- 摘要末段如要交代各章贡献，改写为一句话概括（第 X 章研究 ……，第 Y 章研究 ……）。
- 章末小结（`\section{本章小结}`）的归纳段与引言末段的归纳互补，位置不同，两者都要有。
- 现行违例扫描范围：body/、back/ 全部 `.tex`。

**当前仓库扫描结果**（2026-09-29 立规时）：6 个章节的引言节末段均无归纳列表，chap1 是绪论（不一定需要「本章工作归纳」）、chap6 是骨架（无内容可归纳），待补的具体章节为 chap2 / chap3 / chap4 / chap5。

---

| 需要什么 | 去 THESIS_WORKFLOW.md |
|---|---|
| 完整十阶段流水线定义 | §2 |
| 每章 8 步 SOP | §3 |
| 章节地图 + 详细状态描述 | §4 |
| 编译命令 / 错误速查 / PDF 截屏 | §1 / §6 |
| 参考文献工作流 / BibTeX style | §5 |
| 写作质量门禁 / 术语表 | §7 |
| 与 AI 协作格式 / 汇报模板 / subagent 边界 | §8 |
| 终稿 checklist / 变更日志 | §9 / §10 |

`papers/` 内一切**只读**，连 `\input{}` 都不被允许。

---

## 红线：papers/ 只读

`papers/` 目录（含 `papers/DAMF/`、`papers/UPA/`、所有子目录）下的所有文件——`.tex`、`.pdf`、`.bib`、图片、辅助文件——**均为只读参考资料**，禁止修改。

- 这些文件是**已发表的论文稿件**，作为本论文（正本在 `body/`、`back/`、根目录 `thesis.tex`）的写作参考与图源存在。
- 论文图可以被 `\includegraphics{papers/DAMF/...pdf}` 引用，但 `.tex` 源不应被改写。
- 如果用户明确要求改 `papers/` 内文件，必须在汇报里单独标注此次为"用户授权的参考稿修改"。
- 误操作恢复：`git checkout -- papers/` 或重新拷贝原文。

**触发告警的三种情形**（看到就停下反问）：

1. 用户要求修改 `papers/DAMF/main_re.tex` 等 LaTeX 源。
2. 在 `papers/` 内跑 `latexmk` / `make` / `git commit`。
3. 把 `papers/X/main_re.tex` 复制到 `papers/` 内做"小改"（应输出到 `body/`）。

---

## 正本在哪

- 论文正文：`body/chap1.tex` … `body/chap5.tex`
- 论文前后：`back/conclusion.tex`、`back/acknowledgements.tex`、`back/resume.tex`、`back/publications.tex`
- 主文件：根目录 `thesis.tex`
- 参考文献：根目录 `reference.bib`
- 编译配置：根目录 `.latexmkrc`（xelatex，`$max_repeat=2`）+ `Makefile`

> **当前论文主题**：面向多泛化场景的模型迁移研究（对应三条核心开放性约束维度：数据域泛化 → 词表域泛化 → 情感域泛化）

完整工作流在 [THESIS_WORKFLOW.md](THESIS_WORKFLOW.md) —— 本文件不再重复其内容。

---

## 看到图片/公式需求时

需要复用 `papers/**/main_re.tex` 等里的图或公式结构 → 在 `body/` 下重写，不要改 `papers/`。

图源优先级、PDF 截屏到 `figures/<chap>/`、公式编号规则：见 `THESIS_WORKFLOW.md` §6.5 / §7.2。

---

## 红线：图表浮动选项必须用 `[!htbp]`

所有 `figure` / `figure*` / `table` / `table*` 的浮动参数**统一写为 `[!htbp]`**，含义：

- `h`（here）**优先**：第一选择放在正文当前位置。
- `t` / `b` / `p`：fallback 链——当前位置放不下时依次退到页面顶部 / 底部 / 独立页。
- `!`：放宽 LaTeX 内部美学约束（如「避免连续 figure 堆在同一页」），让 `h` 真正能被满足。

**禁止**：

- 只写 `[h]`、`[t]`、`[b]`、`[p]`、`[ht]`、`[hb]`、`[th]`、`[tb]`、`[htb]`、`[thb]`、`[hbt]`、`[bht]` 等任何不完全等于 `[!htbp]` 的写法。
- `[H]`（需 `float` 包，强制当前位置放不下就报错，不推荐）。
- 裸 `:any 图/表 环境不带方括号`（位置完全交给 LaTeX 启发式，不可控）。

**适用范围**：

- 单栏 `figure` / `table` 与双栏跨页 `figure*` / `table*` 一律使用 `[!htbp]`。
- 已被 `bicaption` 包裹的图表，沿用外层环境的参数即可。

`grep -hoE 'begin\{(figure\*?|table\*?)\}\[[^\]]*\]' body/*.tex back/*.tex | sort -u` 应只输出 `begin{figure}[!htbp]` / `begin{figure*}[!htbp]` / `begin{table}[!htbp]` / `begin{table*}[!htbp]` 四种。

---

## 红线：caption 内禁止加入原论文图表位置标注

在 `body/`、`back/`、`front/`、`thesis.tex` 等正本 `.tex` 文件的 `\caption{}` 与 `\bicaption{}{}{}{}{}` 等图表标题中，**禁止**加入诸如 `(paper Fig.~6)`、`(paper Table.~2)`、`（论文Fig.~5）`、`(paper Algorithm 1)` 等指示**原论文（`papers/` 参考稿）**中图表位置或章节编号的标注词。

**为什么**：

- 论文正本应自含自洽，读者在阅读本论文时不需要知道"原论文第几号图"。
- 答辩 PPT、引用本论文的他人不会查阅 `papers/`，加入原论文位置标注对读者无价值。
- `papers/` 是只读参考资料区，本论文图表的编号（`fig:xxx`、`table:xxx`）即终态编号，与原论文无关。

**违例反模式**（删去即可）：

```latex
% ❌ 英文 caption
{Evolution of selected pseudo-label accuracy ... during training (paper Fig.~5).}
{Ablation on the number of Ch-VSS blocks $L$ (left, paper Fig.~6 left) and ... (right, paper Fig.~6 right)}

% ❌ 中文 caption
{Mamba 骨干上通道维度注意力机制对比示意（论文Fig.~4）}
{... 效果对比（论文Fig.~5）}
```

**允许**（不适用范围）：

1. **指向本论文自身的图表 / 公式 / 算法引用**：`图~\ref{fig:xxx}`、`表~\ref{table:xxx}`、`式 (3.2)`、`算法~\ref{alg:xxx}` 等指向本论文编号系统的引用，按需保留。
2. **章节内首次出现**的图表，`\label{}` 标签即为本论文统一编号。
3. **正文中叙述性引用**「如图 X.Y 所示」按本论文自身编号引用，不受本规则限制。

**适用范围**：`body/`、`back/`、`front/`、`thesis.tex` 等所有正本 `.tex` 文件的图表 caption。`papers/**/*.tex` 由 `papers-readonly.mdc` 单独约束，本规则不涉及。

**审计命令**：

```bash
grep -nE "paper Fig\.|paper Table\.|paper Eq\.|paper Algorithm|论文Fig\.|论文Table\.|论文式" body/*.tex back/*.tex front/*.tex thesis.tex 2>/dev/null
```

合规标准：所有正本 `.tex` 文件输出 0 行。

---

---

## 红线：禁止使用「」直角引号

正文叙述段中**禁止**使用「」（U+300C / U+300D）作为引号或强调符号。

需要标注术语、概念或强调短语时，按以下优先级选择：

1. **直接去掉引号**，让上下文承担语义（首选）
2. **句法重排**：用"是 X 的 Y" / "X 化" / "针对 X" 等结构替代引号强调
3. **代码体**：技术术语、专有概念用 `` `xxx` ``
4. **斜体**：通用术语或非技术概念用 `*xxx*`（即 `\emph{xxx}`）
5. **全角中文双引号** `“”`（U+201C / U+201D）：**仅在确实需要引号语义**（如引用他人原文、书名、专有名称）时使用

**违例反模式**（删掉即可）：

```latex
% ❌「掩码质量与类别语义识别之间的错配」问题
% ❌ 多停留于「先掩码后分类」的两阶段流程
% ❌ 在「图像中有什么」的事实判断上
```

**典型上下文判别**：

- 强调方法路径 / 概念名 → 直接去掉引号，让上下文承语义，例如「先掩码后分类的两阶段流程」
- 引用文献标题 / 他人原文 / 专有名称 → 可用 `“”`
- 技术术语首次出现 → 用 `` `xxx` `` 或 `*xxx*`

**适用范围**：`body/`、`back/`、`front/`、`thesis.tex` 等所有正本 `.tex` 文件。`papers/**/*.tex` 由 `papers-readonly.mdc` 单独约束，本规则不涉及。

**审计命令**：

```bash
# body/、back/、front/、thesis.tex 中的「」应输出 0
for f in body/*.tex back/*.tex front/*.tex thesis.tex; do
  [ -f "$f" ] || continue
  n=$(grep -oE "「|」" "$f" | wc -l | tr -d ' ')
  echo "$f: $n"
done
```

合规标准：所有文件「」计数 = 0。

---

## 红线：文中双引号统一用中文形式

正文段落中出现的成对引号**必须**使用中文双引号 `“”`（U+201C / U+201D），**禁止**用 ASCII `"`。

- ✅ `"先掩码后分类"的两阶段流程` `“先掩码后分类”的两阶段流程`
- ❌ `"先掩码后分类"的两阶段流程`（ASCII 直引号）

**不适用范围（保留 ASCII 或不替换）**：

1. 以 `%` 开头的**整行注释**（包括文件头 `% !Mode:: "TeX:UTF-8"`、`% TeX-master: "../thesis"` 等 LaTeX 编辑器指令行）。
2. 转义序列 `\"`（如德语变音 `ö`、LaTeX 命令参数内强制 ASCII 引号等场景）——按字符原样保留。
3. `\verb|"..."|`、`\verb|"..."=`、`\lstinline|"..."|` 等代码环境内部的 ASCII 引号——按字面保留。
4. bib 字段、`\url{...}`、`\path{...}` 内的 ASCII 引号。
5. 章节标题 `\section{...}`、图/表标题 `\caption{...}`、`\label{...}` 命令参数内——按内容需要任选 ASCII / 中文，但**论文正文叙述段内必须用中文**。

**审计命令**：

```bash
# 查找仍存在的 ASCII \" 双引号（注释行外）
for f in body/*.tex back/*.tex; do
  n=$(grep -v "^%" "$f" | grep -oE '"' | wc -l | tr -d ' ')
  echo "$f: $n"
done
```

合规标准：非注释行的 `"` 数 = 0（除转义 `\"` 与代码环境外）。

---

## 红线：段首提纲不加句号

每个节（`\section{...}`、`\subsection{...}`、`\subsubsection{...}`、`\paragraph{...}`）下首段的段首提纲 `\textbf{提纲}`，其 `\textbf{}` 括号内**末尾禁止**出现 `.` 或 `。`——若存在，去掉只留一个空格接到正文。完整规则见 [.cursor/rules/no-outline-period.mdc](.cursor/rules/no-outline-period.mdc)。

执行要点：

- **改写**：`\textbf{提纲。} 正文` → `\textbf{提纲} 正文`（删末尾 `.` / `。`，保留一个空格）。
- **段首判定**：紧跟 `\section{...}` / `\subsection{...}` / `\paragraph{...}` / `\caption{...}` 或紧邻空行之后的第一个 `\textbf{...}`。
- **不适用范围**：行内强调、表格 / 单元格、列表项内（itemize / enumerate）、数字 / 度量（`\textbf{0.6054}` 小数点不动）、章节标题内——均不在本规则限制内。
- **典型违例**：`\textbf{引理4.1（...）。}` 在段首位置 → 删除末尾 `。`；`\textbf{邻居纯度（Neighbor Purity, NP）。}` 在 `\item` 内 → 按列表项豁免保留。
- **扫描**：跑 `python3` one-liner（见 `.mdc` 文件末），对 body/、back/、front/、thesis.tex 全量检查；违例 = 0 才合规。

**当前仓库扫描结果**（2026-09-29 首次执行）：body/、back/ 全量扫描后发现 **1 处段首提纲违例**：`body/chap3.tex:50` 的 `\textbf{引理4.1（UDA设定下目标风险上界~\cite{mathelin2022discrepancy}）。}` 末尾的 `。` 需删除；2 处列表项内（`\textbf{邻居纯度（Neighbor Purity, NP）。}`、`\textbf{邻居亲和度（Neighbor Affinity, NA）。}`）按列表项豁免保留。**修复后扫描：0 处违例 ✅。**

---

## 红线：表格引用禁止放入括号

正文叙述段中**禁止**把表引用包在括号里——`（表~\ref{tab:xxx}）`、`（详见表~\ref{tab:xxx}）`、`（如表~\ref{tab:xxx}所示）` 等都属于冗余括号，去掉后语义不变。完整规则见 [.cursor/rules/reduce-parens.mdc](.cursor/rules/reduce-parens.mdc) 的"模式 5"。

执行要点：

- **改写**：`（表~\ref{tab:xxx}）` → `表~\ref{tab:xxx}`；`（详见表~\ref{tab:xxx}）` → `详见表~\ref{tab:xxx}`；`（如表~\ref{tab:xxx}所示）` → `如表~\ref{tab:xxx}所示`；按句法衔接，**不靠括号**。
- **典型违例**：
  - ❌ `我们对比了三种配置（表~\ref{tab:abl_scs}）：...`
  - ❌ `UPA 关键观察（表~\ref{tab:aba}）...`
  - ❌ `精度—参数量权衡上同样最优（表~\ref{tab:efficiency}）：...`
  - ✅ `我们对比了三种配置，如表~\ref{tab:abl_scs}所示：...`
  - ✅ `精度—参数量权衡上同样最优，详见表~\ref{tab:efficiency}：...`
- **不适用范围**：
  - LaTeX 命令本身（`\cite{...}` / `\ref{...}`）的语法括号不限制。
  - 图引用（`（图~\ref{fig:xxx}）`）目前未硬性限制，但**推荐**同样的简洁化改写。
  - 章节标题、`\caption{}`、表头本身不受本规则限制。
- **与 `reduce-parens.mdc` 的关系**：本规则是 `reduce-parens.mdc` 模式 3（"同位语 / 列举括号"）在表引用场景下的具体化——删除括号、改为逗号或句法衔接。
- **扫描**：

  ```bash
  grep -nE "（[^）]{0,30}表[^）]{0,30}\\?ref\\{tab:[^}]+\\}[^）]{0,30}）" body/*.tex back/*.tex front/*.tex thesis.tex
  ```

  合规标准：所有正本 `.tex` 文件输出 0 行（`%` 注释行内的违例也建议清理，但不影响渲染）。

**当前仓库扫描结果**（2026-10-08 立规时）：body/、back/ 全量扫描后发现 **3 处正文违例 + 1 处注释违例**（`body/chap2.tex:701` `（如表~\ref{tab:abl_attn}所示）`、`body/chap2.tex:727` `（详见表~\ref{tab:abl_backbone}）`、`body/chap2.tex:790` `（表~\ref{tab:abl_scs}）` 均为前两轮插入消融表时遗留的括号；`body/chap2.tex:672` 在 `%` 注释内）。**已全部修复为逗号 / "详见" / "如...所示" 衔接，扫描 0 违例 ✅。**

---

## 章节地图（速查）

| 章节 | 文件 | 行数 | 状态 |
|---|---|---|---|
| 绪论 | `body/chap1.tex` | 211 | ✅ 主体完，需与各章对齐小节编号 / 引用 |
| 基于 CNN 和选择性扫描机制的无源域适应方法（UPA / SfMamba） | `body/chap2.tex` | — | ✅ 主体完，需补消融表与可视化 |
| 多模态基础模型引导的主动无源域适应方法（DAM / DAMF） | `body/chap3.tex` | — | ✅ 主体完，需补风险上界附录 |
| 跨模型先验融合驱动的开放词汇分割方法（CMPF） | `body/chap4.tex` | — | ⚠️ 骨架偏薄，需扩写方法与实验段 |
| 面向艺术情感推理的多层级视觉语义评测基准（AER-Bench） | `body/chap5.tex` | — | 🔴 **当前为骨架，从阶段 2 进入** |
| 结论 | `back/conclusion.tex` | 8 | 🔴 待写 |
| 致谢 | `back/acknowledgements.tex` | 9 | 🔴 待写 |
| 简历 | `back/resume.tex` | 16 | 🔴 待写 |
| 发表论文 | `back/publications.tex` | 24 | ⚠️ 需对照实际列表 |

> **当前论文主题**：面向多泛化场景的模型迁移研究（对应三条核心开放性约束维度：数据域泛化 → 词表域泛化 → 情感域泛化）
>
> **研究主线**：沿三条核心开放性约束维度推进——第二条（无源域适应）沿 CNN 与 SSM 两条骨干路径协同抑制数据域迁移不确定性，第三章基于多模态引导的主动学习进一步扩展至稀缺标注设定，第四章通过跨模型先验融合解决词表域开放词汇分割，第五章通过多层级评测协议诊断情感域艺术情感推理能力缺口。

详细描述、执行路径（尤其是 chap5 = AER-Bench）：见 `THESIS_WORKFLOW.md` §4 / §4.1。

---

## 两条最常用命令（其余 → THESIS_WORKFLOW.md §1 / §6）

```bash
latexmk -xelatex thesis                          # 全量编译（走 .latexmkrc）
make cleanall && latexmk -xelatex thesis         # 冷启动
```

---

## 引用核验（每章收尾跑一次）

完整 one-liner + BibTeX style + diff 含义 → `THESIS_WORKFLOW.md` §5.3。极简版：

```bash
grep -hoE '\\cite\{[^}]+\}' body/*.tex back/*.tex | sed -E 's/\\cite\{([^}]+)\}/\1/g' | tr ',' '\n' | sort -u > /tmp/cited.txt
grep -E '^@' reference.bib | sed -E 's/@[a-zA-Z]+\{([^,]+),/\1/' | sort -u > /tmp/bib.txt
comm -23 /tmp/cited.txt /tmp/bib.txt   # 正文用但 bib 缺 → 必补
```

bib key 区分大小写；新增条目按 `<作者首字母><年><关键词>` 命名。
