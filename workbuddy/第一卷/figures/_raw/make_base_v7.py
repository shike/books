"""
v7 base: 基于 wb-window.png (2400x1600) 真实 WorkBuddy v5.3.12 界面

真实 UI 元素 (来自 wb-window.png):
- 左侧 (0-540):
  - WorkBuddy v5.3.12 logo (y=120)
  - 7 个 nav: 新建任务/助理/项目/专家·技能·连接器/自动化/资料库/更多 (y=180-560)
  - 任务(1) 分组: 西溪八方城瑞幸咖啡选址评... 1天前 (y=620-700)
  - 空间(1) 分组: 项目新手指引/生成项目功能介绍 51天前 (y=740-880)
  - 用户头像 + 施可 (y=1530)
- 顶部 (540-2400, y=0-130):
  - "本地助理" + "已连接:微信小程序" + 设置
  - 右侧: 搜索/分享/历史/布局
- 中央对话 (540-2400, y=130-1400):
  - 用户消息气泡 "这个功能是什么" (右上)
  - 助手回答 (左对齐)
- 底部输入框 (540-2400, y=1400-1600):
  - 占位符 + 默认权限 + Hy3 + 麦克风 + 发送
  - footer "内容由AI生成,请核实重要信息"

要清空:
- 任务历史 "西溪八方城瑞幸咖啡选址评..."
- 空间历史 "项目新手指引/生成项目功能介绍 51天前"
- 中央对话内容
"""
from PIL import Image, ImageDraw, ImageFont
import os

BASE = "/Users/shike/Desktop/code/workbuddy-books"
SRC = f"{BASE}/第一卷/figures/_raw/wb-window.png"
DST = f"{BASE}/第一卷/figures/wb-v7-base.png"

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

# 配色 (采样自 wb-window.png)
# 左侧栏背景: 浅灰白 (252, 252, 252)
# 主背景: 白 (255, 255, 255)
# 主文字: 深灰 (28, 28, 28)
# 次级文字: 浅灰 (140, 140, 140)
# 占位文字: 更浅 (190, 190, 190)
# 用户消息气泡: 浅灰 (243, 243, 245)

COLOR_BG = (255, 255, 255)            # 主背景
COLOR_SIDEBAR = (252, 252, 252)       # 侧边栏
COLOR_NAV_HOVER = (235, 235, 240)     # nav 选中
COLOR_TEXT = (28, 28, 28)
COLOR_SUBTLE = (140, 140, 140)
COLOR_HINT = (190, 190, 190)
COLOR_USER_BUBBLE = (243, 243, 245)
COLOR_LINK = (37, 99, 235)

font_title = load_font(FONT_BOLD, 38)        # 顶部 nav
font_nav = load_font(FONT_REGULAR, 32)        # 左侧 nav
font_section = load_font(FONT_REGULAR, 24)    # 分组标题
font_tip = load_font(FONT_REGULAR, 22)        # 提示
font_placeholder = load_font(FONT_REGULAR, 28)  # 占位

draw = ImageDraw.Draw(img)

# ============================================================
# 1. 左侧侧边栏 (y=620-1200) - 任务/空间历史清空
# 保留: WorkBuddy v5.3.12 logo + 7 个 nav 项 + 用户头像
# ============================================================
# 整块清空 y=620-1200 范围 (任务+空间历史)
draw.rectangle([(0, 620), (540, 1200)], fill=COLOR_SIDEBAR)
# 重画"任务"分组(无子项)
draw.text((40, 640), "任务", fill=COLOR_SUBTLE, font=font_section)
# 重画"空间"分组
draw.text((40, 760), "空间", fill=COLOR_SUBTLE, font=font_section)
draw.text((70, 810), "（暂无项目）", fill=COLOR_HINT, font=font_tip)

# ============================================================
# 2. 顶部区域 (y=0-130) - 保留 "本地助理 已连接:微信小程序"
# ============================================================
# 不动 - 保留

# ============================================================
# 3. 中央对话区 (540-2400, y=0-1400) - 整块覆盖
# 包括顶部"这个功能是什么"用户消息气泡 (y=100-160) + 助手回答
# 但要保留 y=0-130 顶部"本地助理 已连接:微信小程序"
# 实际策略: y=0-160 整块覆盖, 然后重画顶部"本地助理"
# ============================================================
# 整块覆盖 (包括顶部用户消息气泡 + 中央对话)
draw.rectangle([(540, 0), (2400, 1400)], fill=COLOR_BG)

# 重画顶部 (本地助理 已连接:微信小程序)
top_font = load_font(FONT_BOLD, 30)
draw.text((600, 50), "本地助理", fill=COLOR_TEXT, font=top_font)
# "已连接：微信小程序" 在 y=58
sub_top_font = load_font(FONT_REGULAR, 24)
draw.text((800, 55), "已连接：", fill=COLOR_SUBTLE, font=sub_top_font)
# 微信小程序绿色 chip (简化)
draw.text((900, 55), "● 微信小程序", fill=(50, 180, 100), font=sub_top_font)
# 设置图标
draw.text((1100, 55), "⚙", fill=COLOR_SUBTLE, font=sub_top_font)

# 写空状态提示 (中央)
hint_font = load_font(FONT_REGULAR, 36)
hint_text = "开始你的第一个任务"
bbox = draw.textbbox((0, 0), hint_text, font=hint_font)
text_w = bbox[2] - bbox[0]
draw.text(((540+2400-text_w)//2, 600), hint_text, fill=COLOR_HINT, font=hint_font)

# 下方小字
sub_font = load_font(FONT_REGULAR, 24)
sub_text = "在下方输入框直接说说你想做什么"
bbox2 = draw.textbbox((0, 0), sub_text, font=sub_font)
text_w2 = bbox2[2] - bbox2[0]
draw.text(((540+2400-text_w2)//2, 660), sub_text, fill=COLOR_HINT, font=sub_font)

# ============================================================
# 4. 底部输入框 (y=1400-1600) - 保留
# ============================================================
# 不动

# ============================================================
# 5. 底部 footer (y=1570) - 保留
# ============================================================
# 不动

img.save(DST, "PNG", optimize=True)
size_kb = os.path.getsize(DST) / 1024
print(f"输出: {DST}  {W}x{H}  {size_kb:.0f}KB")
