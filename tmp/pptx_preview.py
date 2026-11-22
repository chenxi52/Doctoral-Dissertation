#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the generated slide1.xml to HTML (absolute positions, real geometry)
so it can be screenshotted for visual verification."""
import zipfile, re, html, sys, os

PPTX = sys.argv[1] if len(sys.argv) > 1 else "/Users/xichen/Documents/hithesis-master/outputs/AER-Bench_问题设定.pptx"
OUTH = sys.argv[2] if len(sys.argv) > 2 else "/tmp/aerrender/slide.html"
W, H = 12192000, 6858000
SCALE = 1600 / W  # px per EMU

with zipfile.ZipFile(PPTX) as z:
    s = z.read("ppt/slides/slide1.xml").decode("utf-8")

body = s.split("<p:spTree>")[1].split("</p:spTree>")[0]
parts = re.findall(r"<p:(sp|pic)>.*?</p:\1>", body, re.S)

out = [f"""<!doctype html><meta charset="utf-8"><style>
body{{margin:0;background:#888;font-family:'PingFang SC','Microsoft YaHei',sans-serif}}
.slide{{position:relative;width:{W*SCALE:.0f}px;height:{H*SCALE:.0f}px;background:#fff;overflow:hidden}}
.sh{{position:absolute}}
.tx{{white-space:pre-wrap;word-break:break-word}}
</style><div class="slide">"""]

for sp in parts:
    m = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/><a:ext cx="(\d+)" cy="(\d+)"', sp)
    if not m:
        continue
    x, y, cx, cy = [int(v) for v in m.groups()]
    fill = re.search(r'<a:solidFill><a:srgbClr val="([0-9A-Fa-f]{6})"/></a:solidFill>', sp)
    stroke = re.search(r'<a:ln w="\d+"><a:solidFill><a:srgbClr val="([0-9A-Fa-f]{6})"', sp)
    geom = re.search(r'<a:prstGeom prst="(\w+)"', sp)
    g = geom.group(1) if geom else "rect"
    rad = "12px" if g == "roundRect" else "0"
    style = (f"left:{x*SCALE:.1f}px;top:{y*SCALE:.1f}px;width:{cx*SCALE:.1f}px;"
             f"height:{cy*SCALE:.1f}px;")
    if fill:
        style += f"background:#{fill.group(1)};"
    else:
        style += "background:transparent;"
    if stroke:
        style += f"box-shadow:inset 0 0 0 1px #{stroke.group(1)};"
    style += f"border-radius:{rad};"

    # paragraphs
    paras = re.findall(r"<a:p>(.*?)</a:p>", sp, re.S)
    inner = []
    for p in paras:
        runs = re.findall(r"<a:rPr([^>]*)>(.*?)</a:rPr><a:t>(.*?)</a:t>", p, re.S)
        if not runs:
            continue
        algn = re.search(r'algn="(\w+)"', p)
        align = {"l": "left", "ctr": "center", "r": "right"}.get(algn.group(1) if algn else "l", "left")
        lspc = re.search(r'<a:spcPct val="(\d+)"/>', p)
        lh = int(lspc.group(1)) / 100000 if lspc else 1.2
        txt = ""
        for attrs, body_, t in runs:
            sz = re.search(r'sz="(\d+)"', attrs)
            b = re.search(r'b="(\d)"', attrs)
            col = re.search(r'srgbClr val="([0-9A-Fa-f]{6})"', body_)
            size = int(sz.group(1)) / 100 if sz else 18
            weight = "bold" if (b and b.group(1) == "1") else "normal"
            c = f"#{col.group(1)}" if col else "#000"
            txt += (f'<span style="font-size:{size/72*96*SCALE/ (96/72) :.1f}px;'
                    f'font-weight:{weight};color:{c}">{html.escape(t)}</span>')
        if txt:
            inner.append(f'<div class="tx" style="text-align:{align};line-height:{lh}">{txt}</div>')
    out.append(f'<div class="sh" style="{style}">{"".join(inner)}</div>')

out.append("</div>")
os.makedirs(os.path.dirname(OUTH), exist_ok=True)
open(OUTH, "w", encoding="utf-8").write("".join(out))
print("wrote", OUTH, "shapes:", len(parts))
