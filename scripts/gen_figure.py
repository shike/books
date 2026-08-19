#!/usr/bin/env python3
"""
books/scripts/gen_figure.py

根据 图名 → 推断图类型 → 生成占位/概念图。
支持 7 种图型:
  - pie       饼图(占比/分布)
  - bar       柱图(对比/数量)
  - flow      流程图(步骤/路径)
  - compare   对比图(左右/上下)
  - grid      网格/象限
  - funnel    漏斗
  - matrix    矩阵
  - screen    界面/UI 截图占位
  - blank     通用空白(只标题+描述)
"""
import os
import sys
import json
import re
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# 中文字体
FONT_PATH = '/System/Library/Fonts/STHeiti Medium.ttc'
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 32
FONT_SIZE_SMALL = 24
FONT_SIZE_TINY = 18

# 配色(8 种莫兰迪)
COLORS = [
    (107, 144, 148),  # 蓝绿
    (199, 144, 158),  # 粉
    (217, 178, 116),  # 黄
    (124, 156, 132),  # 绿
    (98, 110, 134),   # 蓝灰
    (196, 134, 96),   # 橙
    (160, 132, 168),  # 紫
    (180, 160, 130),  # 沙
]

BG_COLOR = (245, 243, 238)  # 米白底
TEXT_COLOR = (50, 50, 55)
SUB_COLOR = (110, 110, 120)
LINE_COLOR = (180, 175, 165)

def get_font(size):
    return ImageFont.truetype(FONT_PATH, size)

def wrap_text(text, max_chars, font):
    """简单按字符数换行"""
    lines = []
    current = ''
    for ch in text:
        current += ch
        if len(current) >= max_chars:
            lines.append(current)
            current = ''
    if current:
        lines.append(current)
    return lines

def draw_title(draw, title, w):
    font = get_font(FONT_SIZE_LARGE)
    lines = wrap_text(title, 18, font)
    y = 50
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((w - tw) / 2, y), line, fill=TEXT_COLOR, font=font)
        y += 60

def draw_subtitle(draw, subtitle, w, y_start):
    font = get_font(FONT_SIZE_SMALL)
    lines = wrap_text(subtitle, 30, font)
    y = y_start
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((w - tw) / 2, y), line, fill=SUB_COLOR, font=font)
        y += 35
    return y

def draw_footnote(draw, text, w, h):
    font = get_font(FONT_SIZE_TINY)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, h - 40), text, fill=SUB_COLOR, font=font)

def make_figure(spec):
    """根据 spec 生成一张图。spec 包含:
    - output: 输出路径
    - title: 主标题
    - subtitle: 副标题(可选)
    - type: 图型
    - items: 内容项(根据 type 不同含义不同)
    - width, height: 尺寸(默认 1280x800)
    """
    output = spec['output']
    title = spec.get('title', '示意图')
    subtitle = spec.get('subtitle', '')
    fig_type = spec.get('type', 'blank')
    items = spec.get('items', [])
    w = spec.get('width', 1280)
    h = spec.get('height', 800)
    
    os.makedirs(os.path.dirname(output), exist_ok=True)
    img = Image.new('RGB', (w, h), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 顶部装饰条
    draw.rectangle([(0, 0), (w, 8)], fill=COLORS[0])
    
    # 标题
    draw_title(draw, title, w)
    
    # 副标题
    content_y = 180
    if subtitle:
        content_y = draw_subtitle(draw, subtitle, w, content_y) + 20
    
    # 内容区
    content_h = h - content_y - 60
    content_area = (40, content_y, w - 40, content_y + content_h)
    
    # 根据类型画内容
    if fig_type == 'pie':
        draw_pie(draw, content_area, items)
    elif fig_type == 'bar':
        draw_bar(draw, content_area, items)
    elif fig_type == 'flow':
        draw_flow(draw, content_area, items)
    elif fig_type == 'compare':
        draw_compare(draw, content_area, items)
    elif fig_type == 'grid':
        draw_grid(draw, content_area, items)
    elif fig_type == 'funnel':
        draw_funnel(draw, content_area, items)
    elif fig_type == 'matrix':
        draw_matrix(draw, content_area, items)
    elif fig_type == 'screen':
        draw_screen(draw, content_area, items, spec.get('screen_text', ''))
    else:
        draw_blank(draw, content_area, items)
    
    # 脚注
    draw_footnote(draw, f'WorkBuddy 内部培训示意图 · {fig_type}', w, h)
    
    img.save(output, 'PNG', optimize=True)
    return output

# ---------- 7 种图型实现 ----------

def draw_pie(draw, area, items):
    """items: [(label, percent), ...]"""
    import math
    x1, y1, x2, y2 = area
    cx, cy = (x1 + x2) / 2 - 200, (y1 + y2) / 2
    r = min(y2 - y1, x2 - x1) * 0.35
    
    total = sum(p for _, p in items) or 1
    start = -math.pi / 2
    font = get_font(FONT_SIZE_SMALL)
    
    legend_x = x1 + (x2 - x1) * 0.65
    legend_y = y1 + 20
    
    for i, (label, pct) in enumerate(items):
        angle = (pct / total) * 2 * math.pi
        end = start + angle
        color = COLORS[i % len(COLORS)]
        draw.pieslice([(cx - r, cy - r), (cx + r, cy + r)], 
                      start * 180 / math.pi, end * 180 / math.pi, fill=color)
        
        # 图例
        draw.rectangle([(legend_x, legend_y), (legend_x + 18, legend_y + 18)], fill=color)
        text = f'{label}  {pct}%'
        draw.text((legend_x + 26, legend_y - 2), text, fill=TEXT_COLOR, font=font)
        legend_y += 32
        
        start = end

def draw_bar(draw, area, items):
    """items: [(label, value), ...]"""
    x1, y1, x2, y2 = area
    n = len(items)
    if n == 0:
        return
    max_val = max(v for _, v in items) or 1
    bar_w = (x2 - x1) * 0.7 / n
    gap = (x2 - x1) * 0.3 / (n + 1)
    base_y = y2 - 60
    chart_h = y2 - y1 - 100
    
    font = get_font(FONT_SIZE_SMALL)
    font_label = get_font(FONT_SIZE_TINY)
    
    for i, (label, val) in enumerate(items):
        bx = x1 + gap + i * (bar_w + gap)
        h = (val / max_val) * chart_h
        draw.rectangle([(bx, base_y - h), (bx + bar_w, base_y)], 
                      fill=COLORS[i % len(COLORS)])
        # 数值
        text = str(val)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        draw.text((bx + (bar_w - tw) / 2, base_y - h - 35), text, fill=TEXT_COLOR, font=font)
        # 标签
        bbox = draw.textbbox((0, 0), label, font=font_label)
        tw = bbox[2] - bbox[0]
        draw.text((bx + (bar_w - tw) / 2, base_y + 10), label, fill=SUB_COLOR, font=font_label)

def draw_flow(draw, area, items):
    """items: [step1, step2, ...]"""
    x1, y1, x2, y2 = area
    n = len(items)
    if n == 0:
        return
    box_w = min(220, (x2 - x1) / n - 20)
    box_h = 100
    total_w = n * box_w + (n - 1) * 40
    start_x = (x1 + x2 - total_w) / 2
    cy = (y1 + y2) / 2 - 20
    
    font = get_font(FONT_SIZE_SMALL)
    
    for i, step in enumerate(items):
        x = start_x + i * (box_w + 40)
        color = COLORS[i % len(COLORS)]
        # 圆角矩形
        draw.rounded_rectangle([(x, cy - box_h/2), (x + box_w, cy + box_h/2)], 
                              radius=12, fill=color)
        # 文字
        lines = wrap_text(step, 10, font)
        text_y = cy - box_h/2 + 15
        for line in lines[:3]:
            bbox = draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
            draw.text((x + (box_w - tw) / 2, text_y), line, fill=(255, 255, 255), font=font)
            text_y += 32
        
        # 箭头
        if i < n - 1:
            arrow_x = x + box_w + 5
            arrow_x2 = x + box_w + 35
            draw.line([(arrow_x, cy), (arrow_x2, cy)], fill=LINE_COLOR, width=3)
            draw.polygon([(arrow_x2, cy - 8), (arrow_x2, cy + 8), (arrow_x2 + 8, cy)], fill=LINE_COLOR)

def draw_compare(draw, area, items):
    """items: [(side, [points])]  如 [("A 方案", ["快", "便宜"]), ("B 方案", ["稳", "全"])]"""
    x1, y1, x2, y2 = area
    sides = items if isinstance(items[0], tuple) else [("A", items)]
    n = len(sides)
    col_w = (x2 - x1) / n - 20
    
    font = get_font(FONT_SIZE_MEDIUM)
    font_pt = get_font(FONT_SIZE_SMALL)
    
    for i, (title, points) in enumerate(sides):
        x = x1 + i * (col_w + 20)
        color = COLORS[i % len(COLORS)]
        # 头部
        draw.rectangle([(x, y1), (x + col_w, y1 + 60)], fill=color)
        bbox = draw.textbbox((0, 0), title, font=font)
        tw = bbox[2] - bbox[0]
        draw.text((x + (col_w - tw) / 2, y1 + 10), title, fill=(255, 255, 255), font=font)
        # 内容
        py = y1 + 90
        for pt in points:
            # 圆点
            draw.ellipse([(x + 20, py + 10), (x + 35, py + 25)], fill=color)
            lines = wrap_text(pt, 14, font_pt)
            for line in lines:
                draw.text((x + 50, py), line, fill=TEXT_COLOR, font=font_pt)
                py += 30
            py += 10

def draw_grid(draw, area, items):
    """items: [(quadrant_name, [points])] 四象限"""
    x1, y1, x2, y2 = area
    midx = (x1 + x2) / 2
    midy = (y1 + y2) / 2
    
    # 坐标轴
    draw.line([(x1, midy), (x2, midy)], fill=LINE_COLOR, width=2)
    draw.line([(midx, y1), (midx, y2)], fill=LINE_COLOR, width=2)
    
    font = get_font(FONT_SIZE_TINY)
    
    # 4 个象限标签
    for i, (qname, points) in enumerate(items[:4]):
        col = i % 2
        row = i // 2
        qx = x1 + col * (x2 - x1) / 2 + 10
        qy = y1 + row * (y2 - y1) / 2 + 10
        draw.text((qx, qy), qname, fill=COLORS[i % len(COLORS)], font=font)
        for j, pt in enumerate(points[:5]):
            draw.text((qx, qy + 25 + j * 22), f'• {pt}', fill=TEXT_COLOR, font=font)

def draw_funnel(draw, area, items):
    """items: [(stage, value), ...]"""
    x1, y1, x2, y2 = area
    n = len(items)
    if n == 0:
        return
    max_val = max(v for _, v in items) or 1
    stage_h = (y2 - y1) / n
    cy_start = y1 + 20
    
    font = get_font(FONT_SIZE_MEDIUM)
    
    for i, (label, val) in enumerate(items):
        w = (val / max_val) * (x2 - x1) * 0.85
        x_start = (x1 + x2 - w) / 2
        x_end = x_start + w
        cy = cy_start + i * stage_h
        
        color = COLORS[i % len(COLORS)]
        if i < n - 1:
            next_w = (items[i+1][1] / max_val) * (x2 - x1) * 0.85
            next_x_start = (x1 + x2 - next_w) / 2
            draw.polygon([
                (x_start, cy), (x_end, cy),
                (next_x_start + next_w, cy + stage_h - 4), (next_x_start, cy + stage_h - 4)
            ], fill=color)
        else:
            draw.rectangle([(x_start, cy), (x_end, cy + stage_h - 4)], fill=color)
        
        # 文字
        bbox = draw.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((x1 + x2 - tw) / 2, cy + 8), label, fill=(255, 255, 255), font=font)

def draw_matrix(draw, area, items):
    """items: [(row_label, col_label, value), ...]"""
    x1, y1, x2, y2 = area
    rows = list(set(r for r, _, _ in items))
    cols = list(set(c for _, c, _ in items))
    rows.sort()
    cols.sort()
    
    if not rows or not cols:
        return
    
    cell_w = (x2 - x1 - 100) / len(cols)
    cell_h = (y2 - y1 - 80) / len(rows)
    
    font = get_font(FONT_SIZE_TINY)
    
    for r, row in enumerate(rows):
        for c, col in enumerate(cols):
            value = next((v for rr, cc, v in items if rr == row and cc == col), 0)
            cx = x1 + 80 + c * cell_w
            cy = y1 + 60 + r * cell_h
            color_val = min(255, 80 + value * 8)
            draw.rectangle([(cx + 2, cy + 2), (cx + cell_w - 2, cy + cell_h - 2)], 
                          fill=(255 - color_val + 80, 240, 240))
            text = str(value)
            bbox = draw.textbbox((0, 0), text, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            draw.text((cx + (cell_w - tw) / 2, cy + (cell_h - th) / 2 - 5), 
                     text, fill=TEXT_COLOR, font=font)
        # 行标签
        bbox = draw.textbbox((0, 0), row, font=font)
        draw.text((x1 + 5, y1 + 60 + r * cell_h + cell_h / 2 - 10), row, fill=TEXT_COLOR, font=font)
    # 列标签
    for c, col in enumerate(cols):
        bbox = draw.textbbox((0, 0), col, font=font)
        tw = bbox[2] - bbox[0]
        draw.text((x1 + 80 + c * cell_w + (cell_w - tw) / 2, y1 + 30), col, fill=TEXT_COLOR, font=font)

def draw_screen(draw, area, items, screen_text=''):
    """界面截图占位"""
    x1, y1, x2, y2 = area
    # 浏览器/应用窗口
    draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=8, outline=LINE_COLOR, width=2)
    # 标题栏
    draw.rectangle([(x1, y1), (x2, y1 + 50)], fill=(70, 80, 95))
    # 红黄绿圆点
    for i, color in enumerate([(220, 80, 80), (220, 180, 80), (90, 200, 110)]):
        draw.ellipse([(x1 + 15 + i * 25, y1 + 17), (x1 + 30 + i * 25, y1 + 32)], fill=color)
    # 标题文字
    font = get_font(FONT_SIZE_SMALL)
    if screen_text:
        bbox = draw.textbbox((0, 0), screen_text, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((x1 + x2 - tw) / 2, y1 + 12), screen_text, fill=(255, 255, 255), font=font)
    # 内容区
    py = y1 + 80
    for item in items:
        lines = wrap_text(item, 30, font)
        for line in lines:
            draw.text((x1 + 30, py), line, fill=TEXT_COLOR, font=font)
            py += 32
        py += 10

def draw_blank(draw, area, items):
    """通用空白(只画标题描述)"""
    x1, y1, x2, y2 = area
    font = get_font(FONT_SIZE_SMALL)
    py = y1 + 20
    for item in items:
        lines = wrap_text('• ' + item, 25, font)
        for line in lines:
            draw.text((x1 + 30, py), line, fill=TEXT_COLOR, font=font)
            py += 32
        py += 8

# ---------- 主入口 ----------

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法:')
        print('  gen_figure.py <spec.json>     # 单张')
        print('  gen_figure.py --batch <list.json>  # 批量')
        sys.exit(1)
    
    if sys.argv[1] == '--batch':
        with open(sys.argv[2], 'r', encoding='utf-8') as f:
            specs = json.load(f)
        for spec in specs:
            try:
                out = make_figure(spec)
                print(f'  OK  {os.path.basename(out)}')
            except Exception as e:
                print(f'  ERR {spec.get("output", "?")}: {e}')
    else:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            spec = json.load(f)
        out = make_figure(spec)
        print(f'OK  {out}')
