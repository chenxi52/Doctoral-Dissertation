#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate a one-page PPTX: 第五章 AER-Bench 问题设定（如何诊断艺术情感推理是否可信）.
Reuses theme/master/layout from the existing reference deck so the visual style matches.
"""
import os, re, shutil, zipfile

ROOT = "/Users/xichen/Documents/hithesis-master"
REF = os.path.join(ROOT, "outputs", "强化学习到世界模型_组会前沿.pptx")
OUT = os.path.join(ROOT, "outputs", "AER-Bench_问题设定.pptx")
BUILD = "/tmp/aer_ppt_build"

# ---- palette (from reference deck) ----
INK      = "111111"   # near-black
GREY     = "5B5B5B"
LGREY    = "B7B7B2"
BLUE     = "2C6EAA"
GREEN    = "2F7D68"
PURPLE   = "6656A8"
ORANGE   = "F05A28"
LBLUE    = "EAF2F9"
LGREEN   = "EAF4F0"
LPURPLE  = "F0EDFA"
LORANGE  = "FFF0E8"
PAPER    = "FFFFFF"
BAND     = "F1F1EF"

NS = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"')

_ids = iter(range(10, 100000))


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def run(text, sz=1000, b=0, color=INK, spc=None, i=0):
    a = f' spc="{spc}"' if spc is not None else ""
    return (f'<a:r><a:rPr lang="zh-CN" altLang="en-US" sz="{sz}" b="{b}" i="{i}"'
            f'{a} dirty="0"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'<a:latin typeface="+mn-lt"/><a:ea typeface="+mn-ea"/><a:cs typeface="+mn-cs"/>'
            f'</a:rPr><a:t>{esc(text)}</a:t></a:r>')


def para(runs, algn="l", line=105000, before=0, after=0):
    return (f'<a:p><a:pPr algn="{algn}">'
            f'<a:lnSpc><a:spcPct val="{line}"/></a:lnSpc>'
            f'<a:spcBef><a:spcPts val="{before}"/></a:spcBef>'
            f'<a:spcAft><a:spcPts val="{after}"/></a:spcAft>'
            f'<a:buNone/></a:pPr>' + "".join(runs) + '</a:p>')


def shape(x, y, cx, cy, geom="rect", fill=None, line=None, lw=12700, adj=None,
          name="shape", paras=None, anchor="t", ins=(91440, 68580, 91440, 68580),
          wrap=True, rot=None):
    """paras: list of <a:p> xml strings"""
    i = next(_ids)
    av = f'<a:avLst>{adj}</a:avLst>' if adj else '<a:avLst/>'
    if fill:
        fl = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'
    else:
        fl = '<a:noFill/>'
    if line:
        ln = f'<a:ln w="{lw}"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill><a:prstDash val="solid"/></a:ln>'
    else:
        ln = '<a:ln w="0"><a:noFill/><a:prstDash val="solid"/></a:ln>'
    rotx = f' rot="{rot}"' if rot is not None else ""
    l, t, r, b = ins
    body = "".join(paras) if paras else '<a:p><a:endParaRPr lang="zh-CN" altLang="en-US"/></a:p>'
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="{esc(name)} {i}"/>'
            f'<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm{rotx}><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="{geom}">{av}</a:prstGeom>{fl}{ln}</p:spPr>'
            f'<p:txBody><a:bodyPr anchor="{anchor}" lIns="{l}" tIns="{t}" rIns="{r}" bIns="{b}" '
            f'wrap="{"square" if wrap else "none"}"><a:normAutofit/></a:bodyPr><a:lstStyle/>'
            f'{body}</p:txBody></p:sp>')


def pic(x, y, cx, cy, rid, name="pic"):
    i = next(_ids)
    return (f'<p:pic><p:nvPicPr><p:cNvPr id="{i}" name="{esc(name)} {i}"/>'
            f'<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
            f'<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')


# ============================ slide content ============================
S = []

# --- header ---
S.append(shape(400050, 266700, 6000000, 209550, fill=None,
               name="eyebrow",
               paras=[para([run("第五章 · AER-Bench · 问题设定", 1050, 1, ORANGE)])]))
S.append(shape(400050, 500000, 11391900, 620000, fill=None, anchor="ctr",
               name="title",
               paras=[para([run("如何诊断艺术情感推理是否可信", 2600, 1, INK)])]))
S.append(shape(400050, 1150000, 11391900, 260000, fill=None, anchor="ctr",
               name="subtitle",
               paras=[para([run("核心问题：模型的情感输出“听起来合理”，是否等于它真的“看懂了”作品？",
                               1150, 0, GREY)])]))
S.append(shape(400050, 1440000, 11391900, 12700, fill=LGREY, name="rule"))

# --- LEFT panel: 问题设定 ---
LX, LW = 400050, 4150000
S.append(shape(LX, 1600000, LW, 300000, fill=None, name="lefthead",
               paras=[para([run("问题设定：语义推理为何难以诊断", 1350, 1, INK)])]))

items = [
    ("01", "度量失效",
     "情感类内容受主观性、抽象性与文化语境三重影响，“事实正确”与“语言流畅”都无法作为可靠性依据；"
     "模型给出的情感标签即便命中，也可能与作品的视觉依据无关。", ORANGE, LORANGE),
    ("02", "监督稀缺",
     "高阶语义所需的细粒度证据化标注（如“左上方冷色笔触营造孤寂氛围”）在预训练语料中极为稀缺，"
     "导致模型缺乏从局部视觉元素到整体情感语义的可追溯推理路径。", BLUE, LBLUE),
    ("03", "伪流畅",
     "模型能够生成语气贴切、表述流畅的情感论述，却未必有视觉证据支撑——"
     "这使得单一情感指标上的高分不足以证明其艺术情感理解“可信”。", PURPLE, LPURPLE),
]
iy = 2010000
for num, title, body, col, bg in items:
    S.append(shape(LX, iy, LW, 1020000, geom="roundRect", fill=bg, line=None,
                   adj='<a:gd name="adj" fmla="val 4000"/>', name="itembg"))
    S.append(shape(LX + 130000, iy + 150000, 620000, 300000, fill=None, anchor="ctr",
                   name="num",
                   paras=[para([run(num, 1500, 1, col)])]))
    S.append(shape(LX + 830000, iy + 150000, LW - 990000, 300000, fill=None, anchor="ctr",
                   name="ittl",
                   paras=[para([run(title, 1250, 1, INK)])]))
    S.append(shape(LX + 130000, iy + 480000, LW - 260000, 480000, fill=None,
                   name="itbody",
                   paras=[para([run(body, 950, 0, GREY)], line=112000)]))
    iy += 1100000

# --- RIGHT panel: 诊断协议 ---
RX, RW = 4800000, 6991950
S.append(shape(RX, 1600000, RW, 300000, fill=None, name="righthead",
               paras=[para([run("诊断协议：从感知线索到证据化解释的逐层追溯", 1350, 1, INK)])]))

levels = [
    ("L1", "感知维度层", "视觉张力 · 动态性 · 空间开放性\n材质印象 · 光照时间性", BLUE, LBLUE),
    ("L2", "情感与 VAD 层", "12 类离散情感标签\n效价—唤醒度—支配度三维评分", GREEN, LGREEN),
    ("L3", "推理层（证据锚定）", "情感映射 · 语境 · 多义性\n隐性表达", ORANGE, LORANGE),
    ("L4", "描述层", "表现性 · 完整性 · 忠实性", PURPLE, LPURPLE),
]
BW, GAP = 1520000, 304000
by = 2020000
for idx, (tag, name, body, col, bg) in enumerate(levels):
    x = RX + idx * (BW + GAP)
    S.append(shape(x, by, BW, 1240000, geom="roundRect", fill=bg, line=col, lw=9525,
                   adj='<a:gd name="adj" fmla="val 6000"/>', name="lv"))
    S.append(shape(x, by, BW, 200000, fill=None, anchor="ctr", ins=(0, 0, 0, 0),
                   name="lvtag", paras=[para([run(tag, 900, 1, col)])]))
    S.append(shape(x + 90000, by + 240000, BW - 180000, 300000, fill=None, anchor="ctr",
                   ins=(0, 0, 0, 0), name="lvname",
                   paras=[para([run(name, 1150, 1, INK)], algn="ctr")]))
    paras = [para([run(body.split("\n")[0], 900, 0, GREY)], algn="ctr", line=112000)]
    if "\n" in body:
        paras.append(para([run(body.split("\n")[1], 900, 0, GREY)], algn="ctr", line=112000))
    S.append(shape(x + 90000, by + 570000, BW - 180000, 600000, fill=None,
                   ins=(0, 0, 0, 0), name="lvbody", paras=paras))
    if idx < 3:
        S.append(shape(x + BW, by + 480000, GAP, 300000, fill=None, anchor="ctr",
                       ins=(0, 0, 0, 0), name="arrow",
                       paras=[para([run("›", 2000, 1, LGREY)], algn="ctr")]))

# callout under the ladder
S.append(shape(RX, 3400000, RW, 780000, geom="roundRect", fill=PAPER, line=ORANGE, lw=12700,
               adj='<a:gd name="adj" fmla="val 4000"/>', name="callout"))
S.append(shape(RX + 180000, 3480000, RW - 360000, 240000, fill=None, anchor="ctr",
               name="coh",
               paras=[para([run("诊断的关键在 L3：能否说明“哪一个感知维度 → 支撑哪一个情感判断”",
                                1100, 1, INK)])]))
S.append(shape(RX + 180000, 3740000, RW - 360000, 380000, fill=None,
               name="cob",
               paras=[para([run("要求模型输出可追溯的证据链，而非仅给出正确标签；"
                                "单图检验图像内推理，双图检验作品间关系推理，两类设置互为补充。",
                                950, 0, GREY)], line=112000)]))

# task types strip
S.append(shape(RX, 4300000, RW, 260000, fill=None, name="taskhead",
               paras=[para([run("同一框架下的任务形式", 1050, 1, GREY)])]))
tasks = [("感知单选", "精确匹配", BLUE), ("情感排序", "Hit@3 + NDCG@3", GREEN),
         ("VAD 评分", "方向敏感得分", PURPLE), ("配对推理", "左右单选", BLUE),
         ("开放式推理/描述", "rubric 语义评判", ORANGE)]
tx = RX
for nm, mt, col in tasks:
    tw = 1330000
    S.append(shape(tx, 4610000, tw, 520000, geom="roundRect", fill=BAND, line=None,
                   adj='<a:gd name="adj" fmla="val 12000"/>', name="tk"))
    S.append(shape(tx + 60000, 4680000, tw - 120000, 220000, fill=None, anchor="ctr",
                   ins=(0, 0, 0, 0), name="tkn",
                   paras=[para([run(nm, 950, 1, INK)], algn="ctr")]))
    S.append(shape(tx + 60000, 4900000, tw - 120000, 220000, fill=None, anchor="ctr",
                   ins=(0, 0, 0, 0), name="tkm",
                   paras=[para([run(mt, 850, 0, GREY)], algn="ctr")]))
    tx += tw + 90000

# --- BOTTOM band ---
BY, BH = 5320000, 1120000
S.append(shape(400050, BY, 11391900, BH, geom="roundRect", fill=INK, line=None,
               adj='<a:gd name="adj" fmla="val 3000"/>', name="band"))
S.append(shape(600000, BY + 140000, 2500000, 260000, fill=None, anchor="ctr",
               name="b1h", paras=[para([run("评测规模", 1000, 1, ORANGE)])]))
S.append(shape(600000, BY + 430000, 2600000, 520000, fill=None,
               name="b1b",
               paras=[para([run("2,058 ", 1150, 1, PAPER),
                            run("件作品　", 900, 0, LGREY),
                            run("24,792 ", 1150, 1, PAPER),
                            run("单图任务　", 900, 0, LGREY),
                            run("9,999 ", 1150, 1, PAPER),
                            run("配对任务　", 900, 0, LGREY),
                            run("14 ", 1150, 1, PAPER),
                            run("个 MLLM", 900, 0, LGREY)], line=125000)]))
S.append(shape(3320000, BY + 200000, 12700, BH - 400000, fill=LGREY, name="div"))
S.append(shape(3520000, BY + 140000, 2400000, 260000, fill=None, anchor="ctr",
               name="b2h", paras=[para([run("核心诊断发现", 1000, 1, ORANGE)])]))
S.append(shape(3520000, BY + 430000, 7650000, 520000, fill=None,
               name="b2b",
               paras=[para([run("情感识别强", 1000, 1, PAPER),
                            run("、", 1000, 0, GREY),
                            run("感知机制弱", 1000, 1, PAPER),
                            run("、", 1000, 0, GREY),
                            run("流畅描述强", 1000, 1, PAPER),
                            run("、", 1000, 0, GREY),
                            run("证据推理弱", 1000, 1, PAPER),
                            run("　——　主要瓶颈：模型能流畅地“谈论”情感，却难以把情感主张锚定到精确的视觉与上下文证据之上。",
                                950, 0, LGREY)], line=125000)]))

# page number
S.append(shape(11239500, 6480000, 552450, 190500, fill=None, anchor="t",
               name="pn",
               paras=[para([run("第五章 · 问题设定", 900, 0, LGREY)], algn="r")]))

slide_xml = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
             f'<p:sld {NS}><p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>'
             f'<a:effectLst/></p:bgPr></p:bg><p:spTree>'
             f'<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
             f'<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
             f'<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
             + "".join(S) +
             f'</p:spTree></p:cSld><p:clrMapOvr><a:overrideClrMapping bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/></p:clrMapOvr></p:sld>')

# ============================ build package ============================
if os.path.exists(BUILD):
    shutil.rmtree(BUILD)
os.makedirs(BUILD)

# extract theme/master/layout from reference deck
with zipfile.ZipFile(REF) as z:
    for name in ["ppt/theme/theme1.xml", "ppt/slideMasters/slideMaster1.xml",
                 "ppt/slideMasters/_rels/slideMaster1.xml.rels",
                 "ppt/slideLayouts/slideLayout1.xml",
                 "ppt/slideLayouts/_rels/slideLayout1.xml.rels",
                 "docProps/core.xml"]:
        try:
            data = z.read(name)
        except KeyError:
            continue
        dst = os.path.join(BUILD, name)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "wb").write(data)

def w(p, s):
    full = os.path.join(BUILD, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(s)

w("ppt/slides/slide1.xml", slide_xml)
w("ppt/slides/_rels/slide1.xml.rels",
  '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
  '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
  '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
  '</Relationships>')

w("ppt/presentation.xml",
  '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
  f'<p:presentation {NS}><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
  '<p:sldIdLst><p:sldId id="256" r:id="rId2"/></p:sldIdLst>'
  '<p:sldSz cx="12192000" cy="6858000"/><p:notesSz cx="6858000" cy="9144000"/>'
  '<p:defaultTextStyle><a:defPPr><a:defRPr lang="en-US"/></a:defPPr>'
  '<a:lvl1pPr marL="0" indent="0" algn="l" defTabSz="914400"><a:defRPr sz="1800" kern="1200">'
  '<a:solidFill><a:schemeClr val="tx1"/></a:solidFill><a:latin typeface="+mn-lt"/><a:ea typeface="+mn-ea"/><a:cs typeface="+mn-cs"/>'
  '</a:defRPr></a:lvl1pPr></p:defaultTextStyle></p:presentation>')

w("ppt/_rels/presentation.xml.rels",
  '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
  '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
  '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>'
  '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/>'
  '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/presProps" Target="presProps.xml"/>'
  '<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>'
  '</Relationships>')

w("ppt/presProps.xml",
  '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
  '<p:presentationPr xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
  'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
  'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>')

w("_rels/.rels",
  '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
  '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
  '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>'
  '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
  '</Relationships>')

w("[Content_Types].xml",
  '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
  '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
  '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
  '<Default Extension="xml" ContentType="application/xml"/>'
  '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
  '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
  '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
  '<Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
  '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
  '<Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>'
  '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
  '</Types>')

# core.xml — rewrite with our title
core = os.path.join(BUILD, "docProps/core.xml")
if os.path.exists(core):
    c = open(core, encoding="utf-8").read()
    c = re.sub(r"<dc:title>.*?</dc:title>",
               "<dc:title>如何诊断艺术情感推理是否可信</dc:title>", c, flags=re.S)
    open(core, "w", encoding="utf-8").write(c)

# zip
if os.path.exists(OUT):
    os.remove(OUT)
zf = zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED)
for root, _, files in os.walk(BUILD):
    for f in files:
        full = os.path.join(root, f)
        arc = os.path.relpath(full, BUILD)
        if arc == "[Content_Types].xml":
            zf.write(full, arc)
        else:
            zf.write(full, arc)
zf.close()
print("written:", OUT, os.path.getsize(OUT), "bytes")
