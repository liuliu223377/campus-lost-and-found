# -*- coding: utf-8 -*-
"""把 7 个页面拼成一张总览图（输出 docs/images/原型总览.svg），供 render_png.js 转 PNG"""
import os
import re

PW, PH = 375, 812
COLS, ROWS = 4, 2
GAP_X, GAP_Y = 30, 46
PAD_X, PAD_Y, HEADER = 40, 40, 142
FONT = "'PingFang SC','Microsoft YaHei','Helvetica Neue',Arial,sans-serif"

PAGES = [
    ("01-首页.svg", "首页"), ("02-发布信息.svg", "发布信息"),
    ("03-发布成功.svg", "发布成功"), ("04-搜索页.svg", "搜索页"),
    ("05-搜索结果.svg", "搜索结果"), ("06-信息详情.svg", "信息详情"),
    ("07-我的发布.svg", "我的发布"),
]


def strip_svg(text):
    """去掉 XML 声明和外层 <svg> 标签，只留内部图形"""
    text = re.sub(r'<\?xml[^>]*\?>', '', text)
    text = re.sub(r'<title>.*?</title>', '', text, flags=re.S)
    m = re.search(r'<svg[^>]*>(.*)</svg>', text, flags=re.S)
    return m.group(1) if m else text


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = os.path.join(base, "prototype", "svg")
    out = os.path.join(base, "docs", "images")
    if not os.path.isdir(out):
        os.makedirs(out)

    w = PAD_X * 2 + COLS * PW + (COLS - 1) * GAP_X
    h = HEADER + PAD_Y + ROWS * PH + (ROWS - 1) * GAP_Y + 56

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
         f'viewBox="0 0 {w} {h}" font-family="{FONT}">',
         f'<rect width="{w}" height="{h}" fill="#F5F6F8"/>',
         f'<text x="{PAD_X}" y="52" font-size="26" font-weight="600" fill="#1A1A1A">'
         f'校园失物招领小程序 · 原型总览</text>',
         f'<text x="{PAD_X}" y="78" font-size="14" fill="#8A9099">'
         f'共 7 个页面 · 375 × 812（微信小程序标准尺寸）· 可点击原型已部署至 Netlify</text>']

    for i, (fn, label) in enumerate(PAGES):
        col, row = i % COLS, i // COLS
        x = PAD_X + col * (PW + GAP_X)
        y = HEADER + row * (PH + GAP_Y)
        s.append(f'<text x="{x}" y="{y - 12}" font-size="15" font-weight="600" '
                 f'fill="#07C160">{esc(label)}</text>')
        s.append(f'<g transform="translate({x},{y})">'
                 f'<rect width="{PW}" height="{PH}" rx="14" fill="#FFFFFF" '
                 f'stroke="#E3E6EA" stroke-width="1"/></g>')
        body = strip_svg(open(os.path.join(src, fn), encoding="utf-8").read())
        s.append(f'<g transform="translate({x},{y})">{body}</g>')

    s.append('</svg>')
    p = os.path.join(out, "原型总览.svg")
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(s))
    print("generated:", p)
    print(f"画布尺寸: {w} x {h}")


if __name__ == "__main__":
    main()
