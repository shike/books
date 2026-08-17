"""
v8 base: 基于 v7 base 加补丁
补丁:
1. 侧栏底部 (y=900-1400): 加 "已归档" + "提示词库" 分组, 解决 700px 大空白
2. 1.9 中央 (y=720-820): 加 4 个常用场景 chip, 解决中央太单薄
"""
from PIL import Image, ImageDraw, ImageFont
import os

BASE = "/Users/shike/Desktop/code/workbuddy-books"
SRC = f"{BASE}/第一卷/figures/wb-v7-base.png"
DST = f"{BASE}/第一卷/figures/wb-v8-base.png"

img = Image.open(SRC).convert("RGB")
W, H = img.size
print(f"源: {SRC}  {W}x{H}")

# 字体
FONT_REGULAR = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/Users/shike/Library/Fonts/AlibabaPuHuiTi-3-75-SemiBold.otf"

def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception as e:
        print(f"字体失败: {e}")
        return ImageFont.load_default()

# 配色
COLOR_SIDEBAR = (252, 252, 252)
COLOR_BG = (255, 255, 255)
COLOR_TEXT = (28, 28, 28)
COLOR_SUBTLE = (140, 140, 140)
COLOR_HINT = (190, 190, 190)
COLOR_LINK = (37, 99, 235)
COLOR_CHIP_BG = (245, 245, 247)
COLOR_CHIP_BORDER = (230, 230, 232)
COLOR_CHIP_ICON = (100, 116, 139)
COLOR_STATUS = (160, 160, 160)

font_section = load_font(FONT_REGULAR, 24)
font_tip = load_font(FONT_REGULAR, 22)
font_chip = load_font(FONT_REGULAR, 26)
font_chip_icon = load_font(FONT_BOLD, 28)
font_archived = load_font(FONT_REGULAR, 22)
font_prompt = load_font(FONT_REGULAR, 26)
font_prompt_meta = load_font(FONT_REGULAR, 20)
font_status = load_font(FONT_REGULAR, 22)

draw = ImageDraw.Draw(img)

# ============================================================
# 1. 侧栏底部补丁: y=900-1400
# ============================================================
# 1.1 "已归档" 分组 (y=900-960)
draw.text((40, 880), "已归档", fill=COLOR_SUBTLE, font=font_section)
draw.text((70, 925), "(0 项)", fill=COLOR_HINT, font=font_archived)

# 1.2 "提示词库" 分组 (y=990-1340)
draw.text((40, 990), "提示词库", fill=COLOR_SUBTLE, font=font_section)

# 3 个示例提示词
prompts = [
    ("周报模板", "本周完成 5 项工作, 跟进 3 项..."),
    ("会议纪要", "把刚才的会议整理成结构化纪要..."),
    ("客户邮件", "起草一封给 X 客户的回信..."),
]

y_p = 1030
for name, snippet in prompts:
    # 项目名 (深色)
    draw.text((70, y_p), name, fill=COLOR_TEXT, font=font_prompt)
    # 缩略预览 (浅灰)
    draw.text((70, y_p + 32), snippet, fill=COLOR_HINT, font=font_prompt_meta)
    y_p += 90

# ============================================================
# 2. 1.9 中央加常用场景 chip (4 个) (y=720-820)
# ============================================================
# 提示: "或者试试这些场景"
hint_above = "或者试试这些场景"
hint_font = load_font(FONT_REGULAR, 24)
bbox_h = draw.textbbox((0, 0), hint_above, font=hint_font)
text_w_h = bbox_h[2] - bbox_h[0]

# 4 个 chip
chip_data = [
    ("✎", "整理周报"),
    ("✉", "起草邮件"),
    ("▤", "分析数据"),
    ("◐", "翻译文档"),
]
chip_w = 230
chip_h = 64
chip_gap = 28
n = len(chip_data)
total_w = n * chip_w + (n - 1) * chip_gap
chip_x_start = (W - total_w) // 2  # 居中
chip_y = 800

# 在 chip 上方写提示
hint_x = (W - text_w_h) // 2
draw.text((hint_x, chip_y - 50), hint_above, fill=COLOR_SUBTLE, font=hint_font)

for i, (icon, text) in enumerate(chip_data):
    x = chip_x_start + i * (chip_w + chip_gap)
    # 圆角矩形背景
    draw.rounded_rectangle(
        [(x, chip_y), (x + chip_w, chip_y + chip_h)],
        radius=14, fill=COLOR_CHIP_BG, outline=COLOR_CHIP_BORDER, width=1
    )
    # icon (左侧)
    draw.text((x + 24, chip_y + 16), icon, fill=COLOR_CHIP_ICON, font=font_chip_icon)
    # 文字 (居中偏右)
    bbox = draw.textbbox((0, 0), text, font=font_chip)
    text_w = bbox[2] - bbox[0]
    text_x = x + 56 + (chip_w - 56 - text_w) // 2
    draw.text((text_x, chip_y + 18), text, fill=COLOR_TEXT, font=font_chip)

img.save(DST, "PNG", optimize=True)
size_kb = os.path.getsize(DST) / 1024
print(f"输出: {DST}  {W}x{H}  {size_kb:.0f}KB")
