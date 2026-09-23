# -*- coding: utf-8 -*-
"""生成基本使用流程图 SVG（输出到 docs/images/）"""
import os

W, H = 900, 662
FONT = "'PingFang SC','Microsoft YaHei','Helvetica Neue',Arial,sans-serif"
GREEN, GREEN_L, TEXT, SUB, LINE = "#07C160", "#E8F8EF", "#1A1A1A", "#8A9099", "#DDE1E6"

BW, BH, GAP, X0 = 168, 58, 38, 46


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def box(x, y, label, idx=None, solid=False):
    fill = GREEN if solid else "#FFFFFF"
    fg = "#FFFFFF" if solid else TEXT
    stroke = GREEN if solid else LINE
    out = (f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="10" '
           f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    out += (f'<text x="{x + BW / 2}" y="{y + BH / 2 + 5}" font-size="15" '
            f'fill="{fg}" font-weight="500" text-anchor="middle">{esc(label)}</text>')
    if idx:
        out += (f'<circle cx="{x + BW - 15}" cy="{y + 13}" r="9" fill="{GREEN_L}"/>'
                f'<text x="{x + BW - 15}" y="{y + 17}" font-size="10" fill="{GREEN}" '
                f'font-weight="600" text-anchor="middle">{idx}</text>')
    return out


def arrow(x1, y, x2):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2 - 9}" y2="{y}" stroke="{GREEN}" '
            f'stroke-width="1.8" stroke-linecap="round"/>'
            f'<path d="M{x2 - 9} {y - 5} L{x2} {y} L{x2 - 9} {y + 5} Z" fill="{GREEN}"/>')


ROWS = [
    ("流程一：浏览信息 → 查看详情", ["进入首页", "浏览或搜索信息", "查看物品详情", "联系发布者"], True),
    ("流程二：发布信息 → 发布成功", ["点击「发布」", "填写物品信息", "点击「立即发布」", "发布成功"], False),
    ("流程三：搜索物品 → 查看结果", ["输入物品关键词", "查看搜索结果", "查看物品详情", "联系发布者"], False),
    ("信息状态流转（发布者可修改）", ["发布信息", "招领中 / 寻物中", "标记为「已解决」", "自动下架，不再展示"], False),
]


def main():
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="{FONT}">',
         f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>']
    s.append(f'<text x="{X0}" y="46" font-size="22" font-weight="600" fill="{TEXT}">'
             f'校园失物招领小程序 · 基本使用流程</text>')
    s.append(f'<text x="{X0}" y="72" font-size="13" fill="{SUB}">'
             f'共三条主干流程与一条状态流转，覆盖本次作业要求演示的全部场景</text>')

    y = 118
    for label, items, solid in ROWS:
        s.append(f'<text x="{X0}" y="{y - 12}" font-size="13" font-weight="600" '
                 f'fill="{GREEN}">{esc(label)}</text>')
        for i, name in enumerate(items):
            x = X0 + i * (BW + GAP)
            s.append(box(x, y, name, i + 1, solid and i == 0))
            if i < len(items) - 1:
                s.append(arrow(x + BW, y + BH / 2, x + BW + GAP))
        y += 152
    s.append('</svg>')

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(base, "docs", "images")
    if not os.path.isdir(out):
        os.makedirs(out)
    p = os.path.join(out, "流程图-基本使用流程.svg")
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(s))
    print("generated:", p)


if __name__ == "__main__":
    main()
