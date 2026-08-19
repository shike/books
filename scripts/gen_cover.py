#!/usr/bin/env python3
"""
books/scripts/gen_cover.py

为 fde 和 workbuddy 生成竖向 1200x1800 cover.png mockup。
- fde: 暗红 + 故事叙事派风格
- workbuddy: 蓝白 + 实用操作派风格
ai-coding 已有专业 cover.png,不动。
"""
import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BOOKS_DIR = Path(__file__).resolve().parent.parent
FONT = '/System/Library/Fonts/STHeiti Medium.ttc'
FONT_BOLD = '/System/Library/Fonts/STHeiti Medium.ttc'  # STHeiti 没有 weight 区分


def get_font(size):
    return ImageFont.truetype(FONT, size)


def get_color(rgb):
    return rgb


def draw_cover_fde():
    """fde 封面:暗红 + 大字 + 故事感"""
    W, H = 1200, 1800
    img = Image.new('RGB', (W, H), (35, 18, 28))  # 深酒红
    draw = ImageDraw.Draw(img)

    # 顶部装饰条
    draw.rectangle([(0, 0), (W, 12)], fill=(220, 70, 90))
    # 底部装饰条
    draw.rectangle([(0, H - 12), (W, H)], fill=(220, 70, 90))

    # 网格底纹(浅)
    for i in range(0, W, 60):
        draw.line([(i, 0), (i, H)], fill=(60, 35, 45), width=1)
    for i in range(0, H, 60):
        draw.line([(0, i), (W, i)], fill=(60, 35, 45), width=1)

    # 顶部标签:"前线部署工程师"
    f_label = get_font(36)
    label = '前线部署工程师 · FDE'
    bbox = draw.textbbox((0, 0), label, font=f_label)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, 200), label, fill=(220, 70, 90), font=f_label)

    # 主标题 FDE(大字)
    f_title = get_font(280)
    title = 'FDE'
    bbox = draw.textbbox((0, 0), title, font=f_title)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, 350), title, fill=(245, 240, 230), font=f_title)

    # 副标题:"AI 竞赛不在于模型"
    f_sub = get_font(58)
    sub = 'AI 竞赛不在于模型'
    bbox = draw.textbbox((0, 0), sub, font=f_sub)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, 720), sub, fill=(245, 240, 230), font=f_sub)

    # 装饰线
    draw.line([(W / 2 - 200, 830), (W / 2 + 200, 830)], fill=(220, 70, 90), width=3)

    # 描述:"一本写给 AI 项目一线人员的书"
    f_desc = get_font(36)
    desc = '一本写给 AI 项目一线人员的书'
    bbox = draw.textbbox((0, 0), desc, font=f_desc)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, 880), desc, fill=(180, 170, 160), font=f_desc)

    # 中部 26 章引用块
    f_quote = get_font(34)
    quote_lines = [
        '"FDE 不是部署工程师,',
        '是 AI 项目从实验室',
        '推到生产环境的 全场唯一 。"',
    ]
    f_quote_b = get_font(50)
    f_author = get_font(28)
    y = 1080
    for line in quote_lines:
        bbox = draw.textbbox((0, 0), line, font=f_quote_b)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) / 2, y), line, fill=(220, 70, 90), font=f_quote_b)
        y += 60
    # 作者
    author = '— 来自一线项目的方法论'
    bbox = draw.textbbox((0, 0), author, font=f_author)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, y + 20), author, fill=(140, 130, 120), font=f_author)

    # 底部信息:"26 章 · 3 篇深度案例 · 6 大行业战场"
    f_info = get_font(32)
    info = '26 章  ·  3 篇深度案例  ·  6 大行业战场'
    bbox = draw.textbbox((0, 0), info, font=f_info)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, 1500), info, fill=(160, 150, 140), font=f_info)

    # 作者
    f_author = get_font(30)
    author = '施可 著'
    bbox = draw.textbbox((0, 0), author, font=f_author)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, 1620), author, fill=(220, 70, 90), font=f_author)

    out = BOOKS_DIR / 'fde' / 'promotion' / 'cover.png'
    img.save(out, 'PNG', optimize=True)
    return out


def draw_cover_workbuddy():
    """workbuddy 封面:蓝白 + 步骤清单感(实用派)"""
    W, H = 1200, 1800
    img = Image.new('RGB', (W, H), (245, 247, 250))  # 浅灰白底
    draw = ImageDraw.Draw(img)

    # 顶部蓝色色块
    draw.rectangle([(0, 0), (W, 360)], fill=(70, 110, 165))
    # 蓝色色块底部斜切
    draw.polygon([(0, 360), (W, 360), (W, 380), (0, 410)], fill=(70, 110, 165))

    # 顶部副标题:"从个人到组织"
    f_sub = get_font(46)
    sub = '从个人到组织'
    bbox = draw.textbbox((0, 0), sub, font=f_sub)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, 110), sub, fill=(255, 255, 255), font=f_sub)

    # 主标题 WorkBuddy
    f_title = get_font(140)
    title = 'WorkBuddy'
    bbox = draw.textbbox((0, 0), title, font=f_title)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, 190), title, fill=(255, 255, 255), font=f_title)

    # 中部步骤框(3 个)
    step_y = 540
    step_w = 320
    step_h = 280
    step_gap = 40
    steps_x_start = (W - 3 * step_w - 2 * step_gap) / 2

    steps = [
        ('第一卷', '个人用好', '8 章'),
        ('第二卷', '团队用好', '8 章'),
        ('第三卷', '组织用好', '8 章'),
    ]
    for i, (vol, name, count) in enumerate(steps):
        x = steps_x_start + i * (step_w + step_gap)
        # 卡片
        draw.rounded_rectangle([(x, step_y), (x + step_w, step_y + step_h)], 
                              radius=20, fill=(255, 255, 255), outline=(220, 226, 235), width=2)
        # 序号圆
        draw.ellipse([(x + step_w / 2 - 30, step_y + 30), 
                      (x + step_w / 2 + 30, step_y + 90)], 
                     fill=(70, 110, 165))
        f_n = get_font(40)
        n_text = f'{i + 1}'
        bbox = draw.textbbox((0, 0), n_text, font=f_n)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((x + step_w / 2 - tw / 2, step_y + 35 + th / 2 - 15), 
                 n_text, fill=(255, 255, 255), font=f_n)
        # 卷名
        f_v = get_font(30)
        bbox = draw.textbbox((0, 0), vol, font=f_v)
        tw = bbox[2] - bbox[0]
        draw.text((x + (step_w - tw) / 2, step_y + 110), vol, fill=(120, 120, 130), font=f_v)
        # 副标题
        f_t = get_font(50)
        bbox = draw.textbbox((0, 0), name, font=f_t)
        tw = bbox[2] - bbox[0]
        draw.text((x + (step_w - tw) / 2, step_y + 155), name, fill=(50, 60, 80), font=f_t)
        # 章节数
        f_c = get_font(28)
        bbox = draw.textbbox((0, 0), count, font=f_c)
        tw = bbox[2] - bbox[0]
        draw.text((x + (step_w - tw) / 2, step_y + 220), count, fill=(140, 140, 150), font=f_c)

    # 副标题:"管理者用好桌面 AI 的三步进阶"
    f_sub2 = get_font(40)
    sub2 = '管理者用好桌面 AI 的三步进阶'
    bbox = draw.textbbox((0, 0), sub2, font=f_sub2)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, 920), sub2, fill=(80, 90, 110), font=f_sub2)

    # 中部引言区(白底,蓝色引用)
    draw.rectangle([(80, 1020), (W - 80, 1180)], fill=(255, 255, 255), outline=(220, 226, 235), width=2)
    f_quote = get_font(38)
    quote = '"派活,比学会 AI 更重要。"'
    bbox = draw.textbbox((0, 0), quote, font=f_quote)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, 1080), quote, fill=(70, 110, 165), font=f_quote)
    f_quote_e = get_font(28)
    en = '"Dispatch beats prompting."'
    bbox = draw.textbbox((0, 0), en, font=f_quote_e)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, 1130), en, fill=(140, 140, 150), font=f_quote_e)

    # 底部信息
    f_info = get_font(32)
    info = '24 章 + 18 附录 + 6 序/目录'
    bbox = draw.textbbox((0, 0), info, font=f_info)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, 1340), info, fill=(120, 120, 130), font=f_info)

    f_info2 = get_font(28)
    info2 = '60+ 真实操作场景 + 6 工具箱 + 1 套培训认证体系'
    bbox = draw.textbbox((0, 0), info2, font=f_info2)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, 1400), info2, fill=(140, 140, 150), font=f_info2)

    # 培训定位标签
    f_tag = get_font(28)
    tag = '企业培训 / 咨询交付件'
    bbox = draw.textbbox((0, 0), tag, font=f_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, 1480), tag, fill=(70, 110, 165), font=f_tag)

    # 作者
    f_author = get_font(34)
    author = '施可 著'
    bbox = draw.textbbox((0, 0), author, font=f_author)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, 1620), author, fill=(80, 90, 110), font=f_author)

    # 底部装饰线
    draw.rectangle([(0, H - 12), (W, H)], fill=(70, 110, 165))

    out = BOOKS_DIR / 'workbuddy' / 'promotion' / 'cover.png'
    img.save(out, 'PNG', optimize=True)
    return out


def main():
    print('=== 生成 fde cover ===')
    fde_out = draw_cover_fde()
    print(f'  OK  {fde_out.relative_to(BOOKS_DIR)}  {fde_out.stat().st_size/1024:.1f} KB')

    print('=== 生成 workbuddy cover ===')
    wb_out = draw_cover_workbuddy()
    print(f'  OK  {wb_out.relative_to(BOOKS_DIR)}  {wb_out.stat().st_size/1024:.1f} KB')

    print('=== ai-coding cover (已有) ===')
    ai_out = BOOKS_DIR / 'ai-coding' / 'promotion' / 'cover.png'
    print(f'  --  {ai_out.relative_to(BOOKS_DIR)}  {ai_out.stat().st_size/1024/1024:.1f} MB')


if __name__ == '__main__':
    main()
