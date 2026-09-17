#!/usr/bin/env python3
"""
SVG 渲染基础库: 为三本书统一视觉风格。

视觉系统:
- 画布: 1200x800(适配电子书横向阅读)
- 暖纸底色: #FAF7F0
- 深炭文字: #2D2D2D
- 主色蓝: #0F4C81
- 强调青: #16A085
- 强调橙: #D2691E(警示/成本)
- 边框灰: #D8D2C5
- 次要灰: #8B8680

字体: system-ui, -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif
"""
from __future__ import annotations
import io
from typing import List, Dict, Any, Tuple, Optional

# ============ 视觉常量 ============
W, H = 1200, 800
BG = "#FAF7F0"
INK = "#2D2D2D"
BLUE = "#0F4C81"
TEAL = "#16A085"
ORANGE = "#D2691E"
RED = "#B73239"
GRAY = "#8B8680"
BORDER = "#D8D2C5"
SOFT = "#F0EBE0"
WHITE = "#FFFFFF"

FONT = 'system-ui, -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif'
MONO = 'ui-monospace, "SF Mono", Menlo, Consolas, monospace'


def escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ============ Primitives ============

def svg_open(w=W, h=H) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family='{FONT}'>
<rect width="{w}" height="{h}" fill="{BG}"/>
'''


def svg_close() -> str:
    return "</svg>\n"


def text(x, y, content, size=18, color=INK, anchor="start", weight="400",
        family=None, italic=False) -> str:
    fam = family or FONT
    weight_attr = f' font-weight="{weight}"' if weight != "400" else ""
    italic_attr = ' font-style="italic"' if italic else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}"{weight_attr}{italic_attr} '
            f'font-family=\'{fam}\'>{escape(content)}</text>\n')


def box(x, y, w, h, fill=WHITE, stroke=BORDER, rx=8, sw=1.5) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" rx="{rx}"/>\n'


def line(x1, y1, x2, y2, color=BORDER, sw=1.5, dash=None) -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{sw}"{dash_attr}/>\n')


def arrow(x1, y1, x2, y2, color=GRAY, sw=2) -> str:
    """带箭头的连线"""
    import math
    # 主线
    out = line(x1, y1, x2, y2, color, sw)
    # 箭头头部(三角)
    angle = math.atan2(y2 - y1, x2 - x1)
    ah = 10  # 箭头长度
    aw = 6   # 箭头半宽
    p1x, p1y = x2, y2
    p2x = x2 - ah * math.cos(angle) + aw * math.sin(angle)
    p2y = y2 - ah * math.sin(angle) - aw * math.cos(angle)
    p3x = x2 - ah * math.cos(angle) - aw * math.sin(angle)
    p3y = y2 - ah * math.sin(angle) + aw * math.cos(angle)
    out += (f'<polygon points="{p1x:.1f},{p1y:.1f} {p2x:.1f},{p2y:.1f} '
            f'{p3x:.1f},{p3y:.1f}" fill="{color}"/>\n')
    return out


def circle(cx, cy, r, fill=WHITE, stroke=BORDER, sw=1.5) -> str:
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'


def header(title: str, subtitle: str = "") -> str:
    """顶部标题区"""
    out = text(80, 70, title, size=32, color=BLUE, weight="600")
    if subtitle:
        out += text(80, 105, subtitle, size=16, color=GRAY, italic=True)
    out += line(80, 130, W - 80, 130, color=BORDER, sw=1)
    return out


def footer(source: str = "") -> str:
    """底部注脚"""
    out = line(80, H - 70, W - 80, H - 70, color=BORDER, sw=1)
    if source:
        out += text(80, H - 45, source, size=12, color=GRAY, italic=True)
    out += text(W - 80, H - 45, "施可 · 三本书", size=12, color=GRAY, anchor="end")
    return out


# ============ Compositions ============

def quadrant(items: List[Tuple[str, str]], title: str = "") -> str:
    """四象限图: items = [(label, description), ...] 4 个"""
    out = header(title) if title else ""
    cx, cy = W / 2, (130 + H - 70) / 2 + 10
    rx, ry = (W - 200) / 2, (H - 230) / 2
    axes = []
    axes.append(line(80, cy, W - 80, cy, color=INK, sw=2))
    axes.append(line(cx, 150, cx, H - 90, color=INK, sw=2))
    out += "".join(axes)

    positions = [
        (cx - rx, cy - ry, "start", "bottom"),    # 左上
        (cx + 20, cy - ry, "start", "bottom"),   # 右上
        (cx - rx, cy + 20, "start", "top"),      # 左下
        (cx + 20, cy + 20, "start", "top"),      # 右下
    ]
    colors = [BLUE, TEAL, ORANGE, GRAY]
    for (px, py, anchor, baseline), (label, desc), col in zip(positions, items, colors):
        out += text(px, py - 8 if baseline == "bottom" else py + 28, label,
                   size=22, color=col, weight="600", anchor=anchor)
        # 描述文字按行(简化:整段一行)
        for i, line_desc in enumerate(desc.split("|")):
            out += text(px, py + 14 + i * 22 if baseline == "bottom" else py + 50 + i * 22,
                       line_desc, size=14, color=INK, anchor=anchor)
    out += footer()
    return out


def timeline(steps: List[Dict[str, str]], title: str = "") -> str:
    """时间线: steps = [{name, detail?}, ...]"""
    out = header(title) if title else ""
    n = len(steps)
    y0 = H / 2
    margin = 120
    seg = (W - 2 * margin) / (n - 1) if n > 1 else 0
    # 主线
    out += line(margin, y0, W - margin, y0, color=INK, sw=3)
    for i, st in enumerate(steps):
        x = margin + i * seg if n > 1 else W / 2
        out += circle(x, y0, 16, fill=BLUE, stroke=BLUE)
        # 序号
        out += text(x, y0 + 5, str(i + 1), size=16, color=WHITE,
                   anchor="middle", weight="700")
        # 名称(上方)
        out += text(x, y0 - 40, st["name"], size=18, color=INK,
                   anchor="middle", weight="600")
        # 详情(下方)
        if "detail" in st:
            for j, line_t in enumerate(st["detail"].split("|")):
                out += text(x, y0 + 50 + j * 22, line_t,
                           size=14, color=GRAY, anchor="middle")
    out += footer()
    return out


def pyramid(layers: List[Dict[str, str]], title: str = "") -> str:
    """金字塔: layers = [{name, items?}, ...] 从顶到底"""
    out = header(title) if title else ""
    n = len(layers)
    top_y = 160
    bot_y = H - 110
    total_h = bot_y - top_y
    cx = W / 2
    max_w = W - 200
    out += ""
    for i, layer in enumerate(layers):
        w = max_w * (i + 1) / n
        h = total_h / n - 10
        y = top_y + i * (total_h / n)
        x = cx - w / 2
        out += box(x, y, w, h, fill=BLUE if i < 2 else (TEAL if i < n - 1 else ORANGE),
                  stroke=INK, rx=4)
        out += text(cx, y + h / 2 - 6, layer["name"], size=20, color=WHITE,
                   weight="600", anchor="middle")
        if "items" in layer:
            items = layer["items"].split("|")
            ix = cx - w / 2 + 20
            for it in items:
                out += text(ix, y + h / 2 + 16, "• " + it, size=13, color=WHITE, anchor="start")
    out += footer()
    return out


def funnel(stages: List[Dict[str, str]], title: str = "") -> str:
    """漏斗: stages = [{name, detail?}, ...] 从上到下"""
    out = header(title) if title else ""
    n = len(stages)
    top_y = 170
    bot_y = H - 130
    cx = W / 2
    top_w = W - 240
    bot_w = 120
    seg_h = (bot_y - top_y) / n
    for i, st in enumerate(stages):
        w_top = top_w - (top_w - bot_w) * (i / n)
        w_bot = top_w - (top_w - bot_w) * ((i + 1) / n)
        y = top_y + i * seg_h
        out += (f'<polygon points="{cx - w_top/2},{y} {cx + w_top/2},{y} '
                f'{cx + w_bot/2},{y + seg_h - 10} {cx - w_bot/2},{y + seg_h - 10}" '
                f'fill="{BLUE if i == 0 else (TEAL if i < n-1 else ORANGE)}" '
                f'stroke="{INK}" stroke-width="1.5"/>\n')
        # 文字
        out += text(cx, y + seg_h / 2 - 4, st["name"], size=20,
                   color=WHITE, weight="600", anchor="middle")
        if "detail" in st:
            out += text(cx, y + seg_h / 2 + 18, st["detail"],
                       size=14, color=WHITE, anchor="middle")
    out += footer()
    return out


def grid(items: List[Dict[str, str]], title: str = "", cols: int = 3) -> str:
    """网格: items = [{name, content?}, ...]"""
    out = header(title) if title else ""
    n = len(items)
    rows = (n + cols - 1) // cols
    margin = 100
    avail_w = W - 2 * margin
    avail_h = H - 230
    cell_w = (avail_w - (cols - 1) * 20) / cols
    cell_h = (avail_h - (rows - 1) * 20) / rows
    for i, item in enumerate(items):
        r, c = divmod(i, cols)
        x = margin + c * (cell_w + 20)
        y = 160 + r * (cell_h + 20)
        out += box(x, y, cell_w, cell_h, fill=WHITE, stroke=BLUE, rx=10, sw=1.5)
        # 标题条
        out += box(x, y, cell_w, 40, fill=BLUE, stroke=BLUE, rx=10, sw=0)
        # 底部补平(避免上面圆角下面直角)
        out += (f'<rect x="{x}" y="{y+30}" width="{cell_w}" height="10" '
                f'fill="{BLUE}"/>\n')
        out += text(x + 16, y + 26, item["name"], size=18, color=WHITE, weight="600")
        # 内容
        if "content" in item:
            for j, line_c in enumerate(item["content"].split("|")):
                out += text(x + 16, y + 60 + j * 22, "• " + line_c,
                           size=14, color=INK)
    out += footer()
    return out


def tree(root: Dict[str, Any], title: str = "") -> str:
    """树/决策图: root = {name, children: [{name, children?:[]}]}"""
    out = header(title) if title else ""

    def layout(node, x, y, level=0, max_depth=3):
        nonlocal out
        # 节点
        out += box(x - 70, y - 22, 140, 44, fill=BLUE if level == 0 else (TEAL if level == 1 else ORANGE),
                  stroke=INK, rx=8, sw=1.5)
        out += text(x, y + 5, node["name"], size=15, color=WHITE,
                   weight="600", anchor="middle")
        if "children" in node and level < max_depth:
            children = node["children"]
            n = len(children)
            spread = min(600, 80 * n)
            child_y = y + 130
            for i, ch in enumerate(children):
                if n == 1:
                    cx = x
                else:
                    cx = x - spread / 2 + spread * i / (n - 1)
                # 连线
                out += line(x, y + 22, cx, child_y - 22, color=GRAY, sw=1.5)
                layout(ch, cx, child_y, level + 1, max_depth)

    layout(root, W / 2, 200)
    out += footer()
    return out


def flow(steps: List[Dict[str, str]], title: str = "", horizontal: bool = True) -> str:
    """流程图: steps = [{name, detail?}],直式或横式"""
    out = header(title) if title else ""
    n = len(steps)
    if horizontal:
        margin = 100
        seg_w = (W - 2 * margin) / n
        for i, st in enumerate(steps):
            x = margin + i * seg_w + 20
            y = H / 2 - 50
            w = seg_w - 40
            out += box(x, y, w, 100, fill=BLUE, stroke=INK, rx=10, sw=1.5)
            out += text(x + w / 2, y + 35, st["name"], size=18, color=WHITE,
                       weight="600", anchor="middle")
            if "detail" in st:
                out += text(x + w / 2, y + 65, st["detail"], size=13,
                           color=WHITE, anchor="middle")
            if i < n - 1:
                ax1 = x + w + 5
                ax2 = x + seg_w - 5
                out += arrow(ax1, y + 50, ax2, y + 50, color=GRAY, sw=2)
    else:
        # 垂直
        margin = 120
        seg_h = (H - 280) / n
        for i, st in enumerate(steps):
            x = W / 2 - 120
            y = 160 + i * seg_h
            w = 240
            out += box(x, y, w, seg_h - 20, fill=BLUE, stroke=INK, rx=10, sw=1.5)
            out += text(x + w / 2, y + 30, st["name"], size=18, color=WHITE,
                       weight="600", anchor="middle")
            if "detail" in st:
                out += text(x + w / 2, y + 60, st["detail"], size=13,
                           color=WHITE, anchor="middle")
            if i < n - 1:
                ay1 = y + seg_h - 25
                ay2 = y + seg_h - 5
                out += arrow(W / 2, ay1, W / 2, ay2, color=GRAY, sw=2)
    out += footer()
    return out


def comparison(left: Dict[str, Any], right: Dict[str, Any], title: str = "") -> str:
    """对比图: {title: str, items: [str], color: BLUE/TEAL/ORANGE}"""
    out = header(title) if title else ""
    cx = W / 2
    margin = 100
    col_w = (W - 2 * margin - 40) / 2
    top_y = 170
    bot_y = H - 130
    # 左标题条
    out += box(margin, top_y, col_w, 60, fill=left.get("color", BLUE), stroke=INK, rx=10)
    out += text(margin + col_w / 2, top_y + 38, left["title"], size=24,
               color=WHITE, weight="600", anchor="middle")
    # 右标题条
    out += box(margin + col_w + 40, top_y, col_w, 60, fill=right.get("color", TEAL),
              stroke=INK, rx=10)
    out += text(margin + col_w + 40 + col_w / 2, top_y + 38, right["title"],
               size=24, color=WHITE, weight="600", anchor="middle")
    # 中间分隔
    out += f'<line x1="{cx}" y1="{top_y}" x2="{cx}" y2="{bot_y}" stroke="{BORDER}" stroke-width="2" stroke-dasharray="6 6"/>\n'
    # 各自条目
    items_per_col = max(len(left.get("items", [])), len(right.get("items", [])))
    item_h = (bot_y - top_y - 90) / max(items_per_col, 1)
    for i in range(items_per_col):
        y = top_y + 80 + i * item_h
        if i < len(left.get("items", [])):
            out += box(margin, y, col_w, item_h - 12, fill=WHITE, stroke=BORDER, rx=6)
            out += text(margin + 20, y + 28, "• " + left["items"][i],
                       size=15, color=INK)
        if i < len(right.get("items", [])):
            x = margin + col_w + 40
            out += box(x, y, col_w, item_h - 12, fill=WHITE, stroke=BORDER, rx=6)
            out += text(x + 20, y + 28, "• " + right["items"][i],
                       size=15, color=INK)
    out += footer()
    return out


def render_figure(name: str, layout: str, content: Dict[str, Any]) -> str:
    """统一入口"""
    title = content.get("title", name)
    if layout == "quadrant":
        return svg_open() + quadrant(content["items"], title) + svg_close()
    if layout == "timeline":
        return svg_open() + timeline(content["steps"], title) + svg_close()
    if layout == "pyramid":
        return svg_open() + pyramid(content["layers"], title) + svg_close()
    if layout == "funnel":
        return svg_open() + funnel(content["stages"], title) + svg_close()
    if layout == "grid":
        return svg_open() + grid(content["items"], title, content.get("cols", 3)) + svg_close()
    if layout == "tree":
        return svg_open() + tree(content["root"], title) + svg_close()
    if layout == "flow_h":
        return svg_open() + flow(content["steps"], title, horizontal=True) + svg_close()
    if layout == "flow_v":
        return svg_open() + flow(content["steps"], title, horizontal=False) + svg_close()
    if layout == "compare":
        return svg_open() + comparison(content["left"], content["right"], title) + svg_close()
    raise ValueError(f"unknown layout: {layout}")


def save(out_dir: str, name: str, svg: str):
    """保存 SVG 到 out_dir/name.svg"""
    import os
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{name}.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    return path


if __name__ == "__main__":
    # 自测
    svg = render_figure("test", "quadrant", {
        "title": "测试四象限",
        "items": [
            ("A 项", "高 / 重要"),
            ("B 项", "高 / 次要"),
            ("C 项", "低 / 重要"),
            ("D 项", "低 / 次要"),
        ]
    })
    save("/tmp", "test_quadrant", svg)
    print("Saved /tmp/test_quadrant.svg")