# -*- coding: utf-8 -*-
"""
校园失物招领小程序 —— 原型图生成脚本
输出：prototype/svg/*.svg （375 x 812，微信小程序标准尺寸）

用途：生成的 SVG 可直接拖入「即时设计 / Figma」，
      每个文字和矩形都会成为独立可编辑图层，便于后续加交互、生成分享链接。
"""
import os

W, H = 375, 812
FONT = "'PingFang SC','Microsoft YaHei','Helvetica Neue',Arial,sans-serif"

C = dict(
    green="#07C160", greenL="#E8F8EF", greenD="#06AD56",
    orange="#FF8F1F", orangeL="#FFF3E6",
    red="#FA5151",
    t1="#1A1A1A", t2="#666666", t3="#999999", t4="#C4C4C4", t5="#E5E7EB",
    line="#EFEFEF", bg="#F5F6F8", white="#FFFFFF",
    field="#F7F8FA", seg="#F2F3F5", ph="#EDEFF2", phIcon="#C8CDD4",
)

# ---------------------------------------------------------------- 基础图元


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def txt(x, y, s, size=14, fill=None, weight="400", anchor="start", ls=0, op=None):
    fill = fill or C["t1"]
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    w = f' font-weight="{weight}"' if weight != "400" else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    o = f' opacity="{op}"' if op is not None else ""
    return (f'<text x="{r(x)}" y="{r(y)}" font-size="{size}" fill="{fill}"'
            f'{w}{a}{l}{o}>{esc(s)}</text>')


def rect(x, y, w, h, rx=0, fill="none", stroke=None, sw=1, op=None, dash=None):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    o = f' opacity="{op}"' if op is not None else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{r(x)}" y="{r(y)}" width="{r(w)}" height="{r(h)}" '
            f'rx="{r(rx)}" fill="{fill}"{s}{d}{o}/>')


def circle(cx, cy, rr, fill="none", stroke=None, sw=1, op=None):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    o = f' opacity="{op}"' if op is not None else ""
    return f'<circle cx="{r(cx)}" cy="{r(cy)}" r="{r(rr)}" fill="{fill}"{s}{o}/>'


def line(x1, y1, x2, y2, stroke=None, sw=1, cap="round", op=None):
    stroke = stroke or C["line"]
    c = f' stroke-linecap="{cap}"' if cap else ""
    o = f' opacity="{op}"' if op is not None else ""
    return (f'<line x1="{r(x1)}" y1="{r(y1)}" x2="{r(x2)}" y2="{r(y2)}" '
            f'stroke="{stroke}" stroke-width="{sw}"{c}{o}/>')


def path(d, fill="none", stroke=None, sw=1, cap="round", join="round", op=None):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    o = f' opacity="{op}"' if op is not None else ""
    return (f'<path d="{d}" fill="{fill}"{s} stroke-linecap="{cap}" '
            f'stroke-linejoin="{join}"{o}/>')


def r(v):
    """数字取整避免 1.0000000000000002 这类脏数据"""
    f = round(float(v), 2)
    return int(f) if f == int(f) else f


def blof(top, h, size):
    """在高度为 h 的盒子内垂直居中时，文字基线的 y 值"""
    return round(top + h / 2.0 + size * 0.35, 1)


def tw(s, size):
    """粗估文本宽度：中文按 1em，英文数字按 0.55em"""
    n = 0.0
    for ch in s:
        n += 1.0 if ord(ch) > 0x2000 else 0.55
    return n * size


def pill(x, y, h, s, size=11, fg=None, bg=None, pad=8, rx=None, stroke=None):
    """自适应宽度的标签胶囊"""
    fg = fg or C["green"]
    bg = bg or C["greenL"]
    w = tw(s, size) + pad * 2
    rx = h / 2.0 if rx is None else rx
    out = rect(x, y, w, h, rx, bg, stroke)
    out += txt(x + w / 2.0, blof(y, h, size), s, size, fg, "500", "middle")
    return out, w


def img_ph(x, y, w, h, rx=8, bg=None, ic=None, label=None):
    """图片占位图：灰底 + 山 + 太阳。图标按 min(w,h) 等比缩放，不会被拉伸"""
    bg = bg or C["ph"]
    ic = ic or C["phIcon"]
    cx, cy = x + w / 2.0, y + h / 2.0
    m = min(w * 0.5, h * 0.8)          # 山脉宽度
    mw, mh = m, m * 0.55
    base = cy + mh * 0.5
    left, right = cx - mw * 0.5, cx + mw * 0.5
    p1 = (cx - mw * 0.20, base - mh * 0.95)
    v = (cx + mw * 0.02, base - mh * 0.45)
    p2 = (cx + mw * 0.16, base - mh * 0.68)
    out = rect(x, y, w, h, rx, bg)
    out += path(f"M{r(left)} {r(base)} L{r(p1[0])} {r(p1[1])} L{r(v[0])} {r(v[1])} "
                f"L{r(p2[0])} {r(p2[1])} L{r(right)} {r(base)} Z", ic)
    out += circle(p1[0] - mw * 0.14, p1[1] - mw * 0.06, mw * 0.10, ic)
    if label:
        out += txt(cx, base + m * 0.30, label, 13, C["t4"], anchor="middle")
    return out


# ---------------------------------------------------------------- 页面骨架

def status_bar():
    s = [txt(28, 30, "9:41", 14, C["t1"], "600")]
    for bx, bh in [(0, 5), (5, 8), (10, 11), (15, 14)]:
        s.append(rect(300 + bx, 29 - bh, 3, bh, 1, C["t1"]))
    s.append(path("M321 25.5 a9 9 0 0 1 13 0", stroke=C["t1"], sw=1.8))
    s.append(path("M324.3 29 a5 5 0 0 1 6.4 0", stroke=C["t1"], sw=1.8))
    s.append(circle(327.5, 32.6, 1.5, C["t1"]))
    s.append(rect(339, 17, 21, 11, 3.5, "none", C["t4"], 1))
    s.append(rect(340.6, 18.6, 18, 7.8, 2, C["t1"]))
    s.append(rect(361, 20.5, 1.8, 4, 0.9, C["t4"]))
    return "".join(s)


def capsule():
    """微信小程序右上角胶囊按钮"""
    s = [rect(267, 48, 92, 32, 16, C["white"], "#E8E8E8", 1)]
    for dx in (-7, 0, 7):
        s.append(circle(290 + dx, 64, 1.8, C["t1"]))
    s.append(line(313, 56, 313, 72, "#E8E8E8", 1, cap=None))
    s.append(circle(336, 64, 6.5, "none", C["t1"], 1.5))
    s.append(circle(336, 64, 1.6, C["t1"]))
    return "".join(s)


def navbar(title, back=False, show_capsule=True, bg=None):
    s = [rect(0, 44, W, 44, 0, bg or C["white"])]
    if back:
        s.append(path("M29 58 L21 66 L29 74", stroke=C["t1"], sw=2))
        s.append(line(21.5, 66, 36, 66, C["t1"], 2))
    s.append(txt(W / 2.0, 72, title, 17, C["t1"], "600", "middle"))
    if show_capsule:
        s.append(capsule())
    s.append(line(0, 88, W, 88, C["line"], 1, cap=None))
    return "".join(s)


def tabbar(active="home"):
    """底部导航：首页 / 发布 / 我的"""
    s = [rect(0, 732, W, 80, 0, C["white"])]
    s.append(line(0, 732, W, 732, C["line"], 1, cap=None))
    items = [("home", "首页", 62.5), ("publish", "发布", 187.5), ("me", "我的", 312.5)]
    for key, label, cx in items:
        on = (key == active)
        col = C["green"] if on else C["t3"]
        if key == "home":
            s.append(path(f"M{cx-10} 752 L{cx} 743 L{cx+10} 752 L{cx+10} 766 "
                          f"L{cx-10} 766 Z", stroke=col, sw=1.9))
        elif key == "publish":
            # 发布是全局主操作，始终保持品牌绿（与主流小程序一致）
            s.append(circle(cx, 754, 12.5, C["green"] if on else "#8FE0B4"))
            s.append(rect(cx - 6, 752.7, 12, 2.6, 1.3, C["white"]))
            s.append(rect(cx - 1.3, 747.4, 2.6, 12, 1.3, C["white"]))
        else:
            s.append(circle(cx, 749.5, 5.2, "none", col, 1.9))
            s.append(path(f"M{cx-8.5} 766.5 a8.5 8.5 0 0 1 17 0", stroke=col, sw=1.9))
        s.append(txt(cx, 780, label, 10, col, "500", "middle"))
    s.append(rect(132, 794, 111, 4.5, 2.25, "#E0E0E0"))
    return "".join(s)


def home_indicator():
    return rect(132, 794, 111, 4.5, 2.25, "#E0E0E0")


def svg_doc(title, body):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" font-family="{FONT}">\n'
            f'<title>{esc(title)}</title>\n{body}\n</svg>\n')


# ---------------------------------------------------------------- 复用组件

def search_bar(x, y, w, h, placeholder, size=13):
    s = [rect(x, y, w, h, h / 2.0, C["seg"])]
    cy = y + h / 2.0
    s.append(circle(x + 24, cy, 6.2, "none", C["t3"], 1.6))
    s.append(line(x + 28.4, cy + 4.4, x + 32, cy + 8, C["t3"], 1.6))
    s.append(txt(x + 40, blof(y, h, size), placeholder, size, C["t3"]))
    return "".join(s)


def info_card(x, y, w, h, kind, title, meta1, meta2, thumb_w=80, kw=None):
    """首页/搜索结果的信息卡片。kind: 招领 / 寻物"""
    is_find = (kind == "招领")           # 招领=绿，寻物=橙
    fg = C["green"] if is_find else C["orange"]
    bg = C["greenL"] if is_find else C["orangeL"]
    s = [rect(x, y, w, h, 12, C["white"], C["line"], 1)]
    th = h - 24
    s.append(img_ph(x + 12, y + 12, thumb_w, th, 8))
    cx = x + 12 + thumb_w + 12
    p, _ = pill(cx, y + 12, 20, kind, 11, fg, bg, 7, 4)
    s.append(p)
    if kw:
        # 关键词高亮：把标题按关键词切成多段
        i = title.find(kw)
        if i >= 0:
            pre, mid, suf = title[:i], title[i:i + len(kw)], title[i + len(kw):]
            x0 = cx
            s.append(txt(x0, y + 54, pre, 15, C["t1"], "500"))
            x0 += tw(pre, 15)
            s.append(txt(x0, y + 54, mid, 15, C["green"], "600"))
            x0 += tw(mid, 15)
            s.append(txt(x0, y + 54, suf, 15, C["t1"], "500"))
        else:
            s.append(txt(cx, y + 54, title, 15, C["t1"], "500"))
    else:
        s.append(txt(cx, y + 54, title, 15, C["t1"], "500"))
    s.append(txt(cx, y + 78, meta1, 12, C["t3"]))
    s.append(txt(cx, y + 98, meta2, 12, C["t4"]))
    return "".join(s)


def filter_row(y, pills, active_idx, right=None):
    """分类筛选胶囊行"""
    s = []
    x = 16
    for i, (label, w) in enumerate(pills):
        on = (i == active_idx)
        s.append(rect(x, y, w, 32, 16, C["green"] if on else C["white"],
                      None if on else C["line"], 1))
        s.append(txt(x + w / 2.0, blof(y, 32, 13), label, 13,
                     C["white"] if on else C["t2"], "500" if on else "400", "middle"))
        x += w + 8
    if right:
        s.append(txt(359, blof(y, 32, 12), right, 12, C["t2"], anchor="end"))
    return "".join(s)


def segmented(x, y, w, h, labels, active, size=13, inner_pad=2, rx=10):
    """分段控件"""
    s = [rect(x, y, w, h, rx, C["seg"])]
    n = len(labels)
    iw = (w - inner_pad * 2) / float(n)
    for i, lab in enumerate(labels):
        ix = x + inner_pad + i * iw
        if i == active:
            cx, cy, cw, ch = ix, y + inner_pad, iw, h - inner_pad * 2
            s.append(rect(cx, cy, cw, ch, rx - 3, C["white"]))
        s.append(txt(ix + iw / 2.0, blof(y, h, size), lab, size,
                     C["green"] if i == active else C["t2"],
                     "600" if i == active else "400", "middle"))
    return "".join(s)


def field_label(x, top, s):
    return txt(x, blof(top, 20, 14), s, 14, C["t1"], "600")


def input_box(x, y, w, h, placeholder, size=14, value=None):
    s = [rect(x, y, w, h, 8, C["field"])]
    s.append(txt(x + 14, blof(y, h, size), value or placeholder, size,
                 C["t1"] if value else "#B0B0B0"))
    return "".join(s)


def chip(x, y, h, s, size=13, on=False):
    w = tw(s, size) + 24
    fg = C["white"] if on else C["t2"]
    bg = C["green"] if on else C["white"]
    st = None if on else C["t5"]
    out = rect(x, y, w, h, h / 2.0, bg, st, 1)
    out += txt(x + w / 2.0, blof(y, h, size), s, size, fg, "500" if on else "400", "middle")
    return out, w


def star_icon(cx, cy, col, filled=False):
    d = (f"M{cx} {cy-9} l2.7 5.5 6.1 0.9 -4.4 4.3 1 6.0 -5.4 -2.9 "
         f"-5.4 2.9 1 -6.0 -4.4 -4.3 6.1 -0.9 Z")
    return path(d, col if filled else "none", col, 1.6)


def share_icon(cx, cy, col):
    s = [circle(cx - 6, cy + 1, 3, "none", col, 1.6),
         circle(cx + 6, cy - 6, 3, "none", col, 1.6),
         circle(cx + 6, cy + 8, 3, "none", col, 1.6)]
    s.append(line(cx - 3.3, cy - 0.3, cx + 3.3, cy - 4.6, col, 1.6))
    s.append(line(cx - 3.3, cy + 2.3, cx + 3.3, cy + 6.6, col, 1.6))
    return "".join(s)


# ---------------------------------------------------------------- 页面 01 首页

HOME_CARDS = [
    ("招领", "捡到一张校园卡", "三教 201 门口 · 今天 09:30", "李同学 · 计算机学院", None),
    ("寻物", "丢失一串宿舍钥匙", "一食堂二楼 · 昨天 18:20", "王同学 · 外国语学院", None),
    ("招领", "捡到一把黑色雨伞", "图书馆三楼 · 昨天 16:05", "张同学 · 数学学院", None),
    ("寻物", "丢失一只白色蓝牙耳机", "体育馆羽毛球场 · 09-21 20:10", "刘同学 · 体育学院", None),
]


def page_home():
    s = [rect(0, 0, W, H, 0, C["white"])]
    s.append(rect(0, 88, W, H - 88, 0, C["bg"]))
    s.append(status_bar())
    s.append(navbar("校园失物招领"))
    s.append(rect(0, 88, W, 56, 0, C["white"]))
    s.append(search_bar(16, 99, 343, 38, "搜索物品名称，如 校园卡、钥匙"))
    s.append(filter_row(162, [("全部", 56), ("寻物", 56), ("招领", 56)], 0, "最新发布 ▾"))
    y = 206
    for k, t, m1, m2, kw in HOME_CARDS:
        s.append(info_card(16, y, 343, 104, k, t, m1, m2))
        y += 114
    s.append(tabbar("home"))
    return svg_doc("01 首页", "".join(s))


# ---------------------------------------------------------------- 页面 02 发布信息

def publish_form_body():
    """发布信息页的正文（发布成功页会复用作为背景）"""
    s = []
    s.append(segmented(16, 100, 343, 40, ["寻物", "招领"], 1))
    # 物品照片
    s.append(field_label(16, 160, "物品照片"))
    s.append(rect(16, 186, 88, 88, 10, C["white"], C["t5"], 1, dash="5 4"))
    s.append(rect(52, 220.7, 16, 3, 1.5, C["t4"]))
    s.append(rect(58.5, 214.2, 3, 16, 1.5, C["t4"]))
    s.append(txt(60, 254, "添加照片", 10, C["t3"], anchor="middle"))
    # 物品名称
    s.append(field_label(16, 294, "物品名称"))
    s.append(input_box(16, 318, 343, 44, "如：校园卡、宿舍钥匙"))
    # 物品分类
    s.append(field_label(16, 378, "物品分类"))
    x = 16
    for i, c in enumerate(["证件卡类", "钥匙", "雨伞", "水杯", "耳机", "图书"]):
        out, w = chip(x, 402, 36, c, on=(i == 0))
        s.append(out)
        x += w + 8
    # 地点与时间
    s.append(field_label(16, 454, "地点与时间"))
    s.append(input_box(16, 478, 167, 44, "如：三教 201", 13))
    s.append(input_box(192, 478, 167, 44, "09-23 09:30", 13))
    # 详细描述
    s.append(field_label(16, 538, "详细描述"))
    s.append(rect(16, 562, 343, 84, 8, C["field"]))
    s.append(txt(30, 588, "补充物品特征，如颜色、品牌、有无挂件…", 14, "#B0B0B0"))
    s.append(txt(345, 632, "0/100", 12, C["t4"], anchor="end"))
    # 联系方式
    s.append(field_label(16, 658, "联系方式"))
    s.append(input_box(16, 682, 343, 44, "微信号 / 手机号（仅详情页可见）", 13))
    return "".join(s)


def page_publish():
    s = [rect(0, 0, W, H, 0, C["white"])]
    s.append(status_bar())
    s.append(navbar("发布信息", back=True))
    s.append(publish_form_body())
    s.append(rect(16, 740, 343, 48, 24, C["green"]))
    s.append(txt(187.5, blof(740, 48, 16), "立即发布", 16, C["white"], "600", "middle"))
    s.append(home_indicator())
    return svg_doc("02 发布信息", "".join(s))


# ---------------------------------------------------------------- 页面 03 发布成功

def page_publish_ok():
    s = [rect(0, 0, W, H, 0, C["white"])]
    s.append(status_bar())
    s.append(navbar("发布信息", back=True))
    s.append(publish_form_body())
    s.append(rect(16, 740, 343, 48, 24, C["green"]))
    s.append(txt(187.5, blof(740, 48, 16), "立即发布", 16, C["white"], "600", "middle"))
    s.append(rect(0, 0, W, H, 0, "#000000", op=0.45))
    s.append(rect(56, 288, 263, 252, 16, C["white"]))
    s.append(circle(187.5, 340, 27, C["greenL"]))
    s.append(path("M174.5 340 l8.8 8.8 17.2 -19", stroke=C["green"], sw=4))
    s.append(txt(187.5, 400, "发布成功", 17, C["t1"], "600", "middle"))
    s.append(txt(187.5, 426, "你的信息已发布成功", 13, C["t3"], anchor="middle"))
    s.append(txt(187.5, 446, "可在「我的发布」中查看和管理", 13, C["t3"], anchor="middle"))
    s.append(rect(80, 462, 215, 42, 21, C["green"]))
    s.append(txt(187.5, blof(462, 42, 15), "查看我的发布", 15, C["white"], "600", "middle"))
    s.append(txt(187.5, 528, "返回首页", 14, C["t2"], anchor="middle"))
    return svg_doc("03 发布成功", "".join(s))


# ---------------------------------------------------------------- 页面 04 搜索页

def search_navbar(kw):
    s = [rect(0, 44, W, 44, 0, C["white"])]
    s.append(path("M29 58 L21 66 L29 74", stroke=C["t1"], sw=2))
    s.append(line(21.5, 66, 36, 66, C["t1"], 2))
    s.append(search_bar(48, 48, 265, 36, kw, 14))
    s.append(txt(359, blof(48, 36, 14), "取消", 14, C["t2"], anchor="end"))
    s.append(line(0, 88, W, 88, C["line"], 1, cap=None))
    return "".join(s)


def page_search():
    s = [rect(0, 0, W, H, 0, C["white"])]
    s.append(status_bar())
    s.append(search_navbar("校园卡"))
    # 搜索历史
    s.append(txt(16, 130, "搜索历史", 14, C["t1"], "600"))
    s.append(txt(359, 130, "清空", 12, C["t3"], anchor="end"))
    x, y = 16, 146
    for c in ["校园卡", "宿舍钥匙", "雨伞", "蓝牙耳机"]:
        out, w = chip(x, y, 36, c, 13)
        s.append(out)
        x += w + 8
    x, y = 16, 190
    for c in ["学生证", "三教", "一卡通"]:
        out, w = chip(x, y, 36, c, 13)
        s.append(out)
        x += w + 8
    # 热门搜索
    s.append(line(16, 254, 359, 254, C["line"], 1, cap=None))
    s.append(txt(16, 288, "热门搜索", 14, C["t1"], "600"))
    rank_col = ["#FE2C55", "#FF8F1F", "#FFC300", C["t3"], C["t3"]]
    y = 304
    for i, name in enumerate(["校园卡", "宿舍钥匙", "雨伞", "蓝牙耳机", "水杯"]):
        s.append(txt(18, blof(y, 40, 15), str(i + 1), 15, rank_col[i], "700", "middle"))
        s.append(txt(48, blof(y, 40, 14), name, 14, C["t1"]))
        if i < 2:
            p, _ = pill(66 + tw(name, 14), blof(y, 40, 10) - 8, 18, "热", 10,
                        C["red"], "#FFECEE", 5, 4)
            s.append(p)
        s.append(txt(359, blof(y, 40, 14), "搜索", 12, C["t3"], anchor="end"))
        if i < 4:
            s.append(line(16, y + 40, 359, y + 40, C["line"], 1, cap=None))
        y += 40
    s.append(home_indicator())
    return svg_doc("04 搜索页", "".join(s))


# ---------------------------------------------------------------- 页面 05 搜索结果

RESULT_CARDS = [
    ("招领", "捡到一张校园卡", "三教 201 门口 · 今天 09:30", "李同学 · 计算机学院"),
    ("寻物", "丢失一张校园卡，急！", "一食堂二楼 · 昨天 18:20", "王同学 · 外国语学院"),
    ("招领", "拾到校园卡一张（尾号 0421）", "图书馆三楼 · 09-21 16:05", "张同学 · 数学学院"),
    ("寻物", "校园卡丢失，卡面有贴纸", "体育馆 · 09-20 20:10", "刘同学 · 体育学院"),
]


def page_search_result():
    s = [rect(0, 0, W, H, 0, C["white"])]
    s.append(rect(0, 88, W, H - 88, 0, C["bg"]))
    s.append(status_bar())
    s.append(search_navbar("校园卡"))
    s.append(txt(16, 118, "找到 12 条相关信息", 13, C["t2"]))
    s.append(txt(359, 118, "综合排序 ▾", 12, C["t2"], anchor="end"))
    s.append(filter_row(134, [("全部", 56), ("寻物", 56), ("招领", 56)], 0, "地点 ▾"))
    y = 180
    for k, t, m1, m2 in RESULT_CARDS:
        s.append(info_card(16, y, 343, 104, k, t, m1, m2, kw="校园卡"))
        y += 114
    s.append(home_indicator())
    return svg_doc("05 搜索结果", "".join(s))


# ---------------------------------------------------------------- 页面 06 信息详情

def page_detail():
    s = [rect(0, 0, W, H, 0, C["white"])]
    s.append(status_bar())
    s.append(navbar("详情", back=True))
    # 大图
    s.append(img_ph(0, 88, W, 224, 0, label="校园卡照片"))
    # 内容区
    s.append(rect(0, 312, W, 400, 0, C["white"]))
    p, w1 = pill(16, 328, 24, "招领", 11, C["green"], C["greenL"], 8, 6)
    s.append(p)
    p, _ = pill(16 + w1 + 8, 328, 24, "证件卡类", 11, C["t2"], C["seg"], 8, 6)
    s.append(p)
    s.append(txt(16, 384, "捡到一张校园卡", 20, C["t1"], "600"))
    rows = [("地点", "三教 201 门口"),
            ("时间", "2026-09-23 09:30"),
            ("发布", "李同学 · 今天 09:35")]
    y = 410
    for k, v in rows:
        s.append(txt(16, blof(y, 30, 14), k, 14, C["t3"]))
        s.append(txt(84, blof(y, 30, 14), v, 14, C["t1"]))
        y += 30
    s.append(line(16, 506, 359, 506, C["line"], 1, cap=None))
    s.append(txt(16, 534, "物品描述", 14, C["t1"], "600"))
    s.append(txt(16, 562, "今天早上在三教 201 门口的桌子上捡到一张校园卡，", 14, C["t2"]))
    s.append(txt(16, 586, "卡面贴有一张卡通贴纸。请失主联系我核对姓名。", 14, C["t2"]))
    s.append(txt(16, 618, "温馨提示：请勿提前透露物品全部特征，以便核实失主身份。",
                 11, C["t4"]))
    # 发布者信息
    s.append(line(16, 646, 359, 646, C["line"], 1, cap=None))
    s.append(circle(44, 682, 18, C["greenL"]))
    s.append(txt(44, 689, "李", 15, C["green"], "600", "middle"))
    s.append(txt(76, 676, "李同学", 14, C["t1"], "600"))
    s.append(txt(76, 696, "计算机学院 · 发布于今天 09:35", 11, C["t3"]))
    s.append(txt(359, 682, "TA 的其他发布 ›", 12, C["t3"], anchor="end"))
    # 底部操作栏
    s.append(rect(0, 712, W, 100, 0, C["white"]))
    s.append(line(0, 712, W, 712, C["line"], 1, cap=None))
    s.append(star_icon(40, 750, C["t2"]))
    s.append(txt(40, 782, "收藏", 10, C["t2"], anchor="middle"))
    s.append(share_icon(104, 748, C["t2"]))
    s.append(txt(104, 782, "分享", 10, C["t2"], anchor="middle"))
    s.append(rect(150, 736, 209, 48, 24, C["green"]))
    s.append(txt(254.5, blof(736, 48, 16), "联系 TA", 16, C["white"], "600", "middle"))
    s.append(home_indicator())
    return svg_doc("06 信息详情", "".join(s))


# ---------------------------------------------------------------- 页面 07 我的发布

MY_CARDS = [
    ("招领", "捡到一张校园卡", "浏览 32 · 今天 09:35", "doing"),
    ("寻物", "丢失一串宿舍钥匙", "浏览 18 · 昨天 18:20", "doing"),
    ("招领", "捡到一把黑色雨伞", "浏览 47 · 已解决 · 昨天 16:05", "done"),
]


def page_mine():
    s = [rect(0, 0, W, H, 0, C["white"])]
    s.append(rect(0, 88, W, H - 88, 0, C["bg"]))
    s.append(status_bar())
    s.append(navbar("我的发布"))
    # 用户信息
    s.append(rect(0, 88, W, 180, 0, C["white"]))
    s.append(circle(52, 132, 28, C["greenL"]))
    s.append(txt(52, 143, "李", 22, C["green"], "600", "middle"))
    s.append(txt(94, 126, "李同学", 18, C["t1"], "600"))
    s.append(txt(94, 150, "2023xxxx · 计算机学院", 12, C["t3"]))
    for cx, num, lab in [(78, "3", "我发布的"), (187.5, "1", "已解决"), (297, "2", "我的收藏")]:
        s.append(txt(cx, 204, num, 18, C["t1"], "600", "middle"))
        s.append(txt(cx, 224, lab, 11, C["t3"], anchor="middle"))
    s.append(segmented(16, 284, 343, 36, ["全部", "寻物", "招领", "已解决"], 0, 12, 2, 8))
    y = 336
    for kind, title, meta, st in MY_CARDS:
        is_find = (kind == "招领")
        fg = C["green"] if is_find else C["orange"]
        bg = C["greenL"] if is_find else C["orangeL"]
        s.append(rect(16, y, 343, 112, 12, C["white"], C["line"], 1))
        s.append(img_ph(28, y + 12, 64, 64, 8))
        p, _ = pill(104, y + 12, 20, kind, 11, fg, bg, 7, 4)
        s.append(p)
        s.append(txt(104, y + 52, title, 15, C["t1"], "500"))
        s.append(txt(104, y + 74, meta, 12, C["t3"]))
        if st == "doing":
            s.append(txt(104, y + 98, "标记为已解决", 12, C["green"], "500"))
            s.append(txt(359, y + 98, "删除", 12, C["t3"], anchor="end"))
            s.append(txt(307, y + 98, "编辑", 12, C["t3"], anchor="end"))
        else:
            p, w = pill(359 - (tw("已解决", 11) + 16), y + 12, 20, "已解决", 11,
                        C["t2"], C["seg"], 8, 4)
            s.append(p)
            s.append(txt(359, y + 98, "删除", 12, C["t3"], anchor="end"))
            s.append(txt(307, y + 98, "编辑", 12, C["t3"], anchor="end"))
        y += 122
    s.append(tabbar("me"))
    return svg_doc("07 我的发布", "".join(s))


# ---------------------------------------------------------------- 入口

PAGES = [
    ("01-首页.svg", page_home, "01 首页"),
    ("02-发布信息.svg", page_publish, "02 发布信息"),
    ("03-发布成功.svg", page_publish_ok, "03 发布成功"),
    ("04-搜索页.svg", page_search, "04 搜索页"),
    ("05-搜索结果.svg", page_search_result, "05 搜索结果"),
    ("06-信息详情.svg", page_detail, "06 信息详情"),
    ("07-我的发布.svg", page_mine, "07 我的发布"),
]


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(base, "prototype", "svg")
    if not os.path.isdir(out):
        os.makedirs(out)
    for fn, builder, title in PAGES:
        with open(os.path.join(out, fn), "w", encoding="utf-8") as f:
            f.write(builder())
        print("generated:", fn)
    print("done ->", out)


if __name__ == "__main__":
    main()
