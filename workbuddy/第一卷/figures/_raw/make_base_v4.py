"""
v4 base: 基于 wb-real-main.png (2880x1800) 真实 v5.3.12 界面
精确坐标脱敏:
- 顶部任务标题 y=50-150
- 用户消息 y=110-200
- 助手内容 y=200-1450
- 左侧项目区 y=700-1500
"""
from PIL import Image, ImageDraw, ImageFont
import os

BASE = "/Users/shike/Desktop/code/workbuddy-books"
SRC = f"{BASE}/第一卷/figures/_raw/wb-real-main.png"
DST = f"{BASE}/第一卷/figures/wb-v4-base.png"

img = Image.open(SRC).convert("RGB")
W, H = img.size
print(f"源: {SRC}  {W}x{H}")

FONT_REGULAR = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/Users/shike/Library/Fonts/AlibabaPuHuiTi-3-75-SemiBold.otf"

def load_font(path, size, idx=0):
    try:
        return ImageFont.truetype(path, size, index=idx)
    except Exception as e:
        print(f"字体失败: {e}")
        return ImageFont.load_default()

# 真实 UI 配色 (采样自原图)
COLOR_BG = (254, 254, 254)       # 主背景
COLOR_PANEL = (255, 255, 255)    # 卡片
COLOR_SIDEBAR = (252, 252, 252)  # 侧边栏
COLOR_BORDER = (232, 232, 232)   # 分割线
COLOR_TEXT = (28, 28, 28)        # 主文字
COLOR_SUBTLE = (140, 140, 140)   # 次级
COLOR_HINT = (190, 190, 190)     # 占位
COLOR_HOVER = (235, 235, 240)    # 选中背景
COLOR_ACCENT = (37, 99, 235)     # 蓝色

font_title = load_font(FONT_BOLD, 42)
font_nav = load_font(FONT_REGULAR, 36)
font_section = load_font(FONT_REGULAR, 30)
font_placeholder = load_font(FONT_REGULAR, 30)
font_tip = load_font(FONT_REGULAR, 26)

draw = ImageDraw.Draw(img)

# ============================================================
# 1. 顶部任务标题 (y=40-180) - 整块覆盖, x 范围扩到 2400
# 原位置: "调研语音数字人系统" + 下拉箭头 (y=46-72)
# 用户消息气泡 "4. 先做MVP" (y=112-168, x=1900-2100)
# 进度面板"进度"标题 (y=86-115) - 不动
# ============================================================
draw.rectangle([(460, 40), (2200, 180)], fill=COLOR_BG)  # x 范围到 2200 保留进度面板
# 写新标题
draw.text((480, 60), "WorkBuddy", fill=COLOR_TEXT, font=font_title)
# 加下拉箭头
draw.text((780, 70), "▾", fill=COLOR_SUBTLE, font=font_title)

# ============================================================
# 2. 中央对话区 - 整块覆盖 (y=180-1450)
# 顶部标题区 y=40-180 已覆盖
# 用户消息"4. 先做MVP" y=112-168 也在顶部区被覆盖
# ============================================================
draw.rectangle([(460, 180), (2400, 1450)], fill=COLOR_BG)

# 写一个空状态提示: "开始你的第一个任务"
hint_font = load_font(FONT_REGULAR, 38)
hint_text = "开始你的第一个任务"
# 居中估算
bbox = draw.textbbox((0, 0), hint_text, font=hint_font)
text_w = bbox[2] - bbox[0]
draw.text(((460+2400-text_w)//2, 650), hint_text, fill=COLOR_HINT, font=hint_font)

# 下方小字提示
sub_font = load_font(FONT_REGULAR, 26)
sub_text = "在下方输入框直接说说你想做什么"
bbox2 = draw.textbbox((0, 0), sub_text, font=sub_font)
text_w2 = bbox2[2] - bbox2[0]
draw.text(((460+2400-text_w2)//2, 710), sub_text, fill=COLOR_HINT, font=sub_font)

# ============================================================
# 3. 左侧项目区 (y=700-1500) - 整块覆盖
# 包括 code/workbuddy-books/pre-sales-playb/dy-location 4 个项目及其子任务
# 保留: 顶部"定时任务"和"项目"分组标题 (y<700)
# 重画: "Agent 团队" / "已归档" (被覆盖了)
# ============================================================
# 先覆盖整块
draw.rectangle([(0, 700), (460, 1500)], fill=COLOR_SIDEBAR)

# 写"项目"分组标签 (在 y≈700 处)
# 原图"项目"标题在 y=638-663
# y=700-740 应该是项目文件夹"code"的位置
# 改成"暂无项目"占位
draw.text((60, 760), "（暂无项目）", fill=COLOR_HINT, font=font_tip)

# 写"Agent 团队" / "已归档" 在 y=1500-1600
draw.text((60, 1540), "Agent 团队", fill=COLOR_SUBTLE, font=font_section)
draw.text((60, 1610), "已归档", fill=COLOR_SUBTLE, font=font_section)

# ============================================================
# 4. 右侧进度面板 (x=2200-2880, y=80-260)
# 保留 — 这是真实 UI 元素
# 但里面的"跟踪较长任务的进度"是 placeholder,保留
# ============================================================

# ============================================================
# 5. 底部输入框 y=1476+ 保留
# 6. footer "内容由AI生成,重要信息请务必核查" 保留
# ============================================================

img.save(DST, "PNG", optimize=True)
size_kb = os.path.getsize(DST) / 1024
print(f"输出: {DST}  {W}x{H}  {size_kb:.0f}KB")
