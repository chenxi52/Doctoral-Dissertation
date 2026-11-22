# 博士论文 LaTeX 项目

主编译文件：

```bash
thesis.tex
```

常用命令：

```bash
latexmk -xelatex thesis.tex
latexmk -c thesis
make clean
```

目录说明：

- `front/`：封面、摘要等前置内容
- `body/`：正文各章
- `back/`：结论、发表论文、索引、致谢、简历等后置内容
- `figures/`：论文正文图片
- `papers/`：已发表论文 PDF
- `assets/`：作图素材，如 `pic.pptx`
- `extras/`：暂不参与主编译的模板备用文件

当前入口已从原模板示例目录整理到项目根目录，可直接在本目录编译。
