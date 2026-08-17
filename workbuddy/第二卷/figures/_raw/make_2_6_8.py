"""
2.6.8 占位图: 专家中心与自动化的关系
- 左侧: 专家中心 (工具箱 - Skill 列表)
- 右侧: 自动化引擎 (使用说明书 - 触发器 + 定时 + 日程)
- 中间: 双向箭头 + "调用 / 反馈"
- 风格贴近 2.6.1-trigger-types.png (三级递进图)
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = "/Users/shike/Desktop/code/workbuddy-books/第二卷/figures/2.6.8-expert-center-automation-relation.png"

W, H = 2400, 1200  # 2x, 最大宽度 1600px -> 原图 2400x1200

# 配色 (贴近 2.6.1: 青绿 + 浅蓝)
TEAL = (38, 166, 154)
TEAL_DARK = (20, 130, 120)
BG_CARD = (245, 250, 252)
BORDER = (38, 166, 154)
TEXT_DARK = (28, 28, 28)
TEXT_GRAY = (110, 110, 110)
WATERMARK = (190, 190, 190)

FONT_REGULAR = "/System/Library/Fonts/STHeiti Light.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"

def font(path, size):
    try:
        return ImageFont.truetype(path, size, index=0)
    except Exception:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            return ImageFont.load_default()

f_title = font(FONT_BOLD, 56)
f_h1 = font(FONT_BOLD, 60)
f_h2 = font(FONT_BOLD, 44)
f_body = font(FONT_REGULAR, 36)
f_meta = font(FONT_REGULAR, 30)
f_wm = font(FONT_REGULAR, 24)

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

# 标题
d.text((W // 2 - 360, 60), "专家中心 与 自动化 的关系", fill=TEXT_DARK, font=f_title)

# 左侧卡片: 专家中心 (工具箱)
LX, LY, LW, LH = 180, 240, 880, 720
d.rounded_rectangle([LX, LY, LX + LW, LY + LH], radius=20, fill=BG_CARD, outline=BORDER, width=4)

# 左卡片标题
d.text((LX + 40, LY + 40), "专家中心", fill=TEAL_DARK, font=f_h1)
d.text((LX + 40, LY + 120), "Center of Excellence", fill=TEXT_GRAY, font=f_meta)
d.text((LX + 40, LY + 175), "工具箱 (静态能力)", fill=TEXT_GRAY, font=f_meta)

# 4 个 Skill 项
skills = [
    ("周报", "weekly-report-skill"),
    ("月报", "monthly-report-skill"),
    ("客户回访", "customer-followup-skill"),
    ("合同审阅", "contract-review-skill"),
]
y = LY + 260
for name, sid in skills:
    # 圆点
    d.ellipse([LX + 50, y + 18, LX + 80, y + 48], fill=TEAL)
    # 名称
    d.text((LX + 110, y), name, fill=TEXT_DARK, font=f_h2)
    # ID (灰)
    d.text((LX + 110, y + 60), sid, fill=TEXT_GRAY, font=f_body)
    y += 110

# 右侧卡片: 自动化引擎
RX, RY, RW, RH = 1340, 240, 880, 720
d.rounded_rectangle([RX, RY, RX + RW, RY + RH], radius=20, fill=BG_CARD, outline=BORDER, width=4)

d.text((RX + 40, RY + 40), "自动化", fill=TEAL_DARK, font=f_h1)
d.text((RX + 40, RY + 120), "Automation", fill=TEXT_GRAY, font=f_meta)
d.text((RX + 40, RY + 175), "使用说明书 (动态调用)", fill=TEXT_GRAY, font=f_meta)

# 4 个自动化场景
autos = [
    ("周报自动生成", "每周五 17:30"),
    ("月度数据汇总", "每月 1 日 09:00"),
    ("客户回访提醒", "每天 09:00 检查"),
    ("合同审阅分发", "新建 PDF 时触发"),
]
y = RY + 260
for name, when in autos:
    d.ellipse([RX + 50, y + 18, RX + 80, y + 48], fill=TEAL)
    d.text((RX + 110, y), name, fill=TEXT_DARK, font=f_h2)
    d.text((RX + 110, y + 60), when, fill=TEXT_GRAY, font=f_body)
    y += 110

# 中间: 双向箭头
# 上箭头 (左→右, 能力调用)
arrow_y_top = 500
arrow_y_bot = 700
mid_x = (LX + LW + RX) // 2

# 上行: 能力调用 (左 → 右)
d.line([(LX + LW + 20, arrow_y_top), (RX - 20, arrow_y_top)], fill=TEAL, width=8)
# 箭头头部
d.polygon([
    (RX - 20, arrow_y_top - 20),
    (RX - 20, arrow_y_top + 20),
    (RX + 20, arrow_y_top),
], fill=TEAL)
# 上方标签
d.text((mid_x - 180, arrow_y_top - 70), "能力调用", fill=TEAL_DARK, font=f_h2)
d.text((mid_x - 240, arrow_y_top + 18), "Skill → 执行动作", fill=TEXT_GRAY, font=f_body)

# 下行: 反馈迭代 (右 → 左)
d.line([(RX - 20, arrow_y_bot), (LX + LW + 20, arrow_y_bot)], fill=TEAL, width=8)
d.polygon([
    (LX + LW + 20, arrow_y_bot - 20),
    (LX + LW + 20, arrow_y_bot + 20),
    (LX + LW - 20, arrow_y_bot),
], fill=TEAL)
d.text((mid_x - 180, arrow_y_bot - 70), "反馈迭代", fill=TEAL_DARK, font=f_h2)
d.text((mid_x - 200, arrow_y_bot + 18), "调用结果 → Skill 改进", fill=TEXT_GRAY, font=f_body)

# 底部一句话总结
d.text((W // 2 - 540, 1020),
       "Skill 是工具, 自动化是「什么时候用什么工具」",
       fill=TEXT_DARK, font=f_h1)

# 水印 (右下角)
d.text((W - 380, H - 60), "WorkBuddy 三部曲 · 第二卷", fill=WATERMARK, font=f_wm)

img.save(OUT, "PNG", optimize=True)
print(f"OK: {OUT}  {W}x{H}")
