"""
基于 wb-v4-base.png 生成 1.9 和 2.1-2.10 所有变体
5 场景 × 2 张 (输入+输出) + 1.9 (空状态) = 11 张

设计原则:
- 顶部任务标题根据场景更新
- 用户消息气泡: 右上, 浅灰背景
- 助手回复: 中央, 白色背景, 列表/段落
- 思考/制品提示: 真实 UI 风格
"""
from PIL import Image, ImageDraw, ImageFont
import os

BASE = "/Users/shike/Desktop/code/workbuddy-books"
SRC = f"{BASE}/第一卷/figures/wb-v4-base.png"
DST_DIR = f"{BASE}/第一卷/figures"

FONT_REGULAR = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/Users/shike/Library/Fonts/AlibabaPuHuiTi-3-75-SemiBold.otf"
FONT_MONO = "/System/Library/Fonts/SFNSMono.ttf"

def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception as e:
        return ImageFont.load_default()

# 配色
COLOR_BG = (254, 254, 254)
COLOR_USER_BUBBLE = (243, 243, 245)      # 用户消息气泡背景
COLOR_AI_BG = (254, 254, 254)            # AI 回复背景
COLOR_TEXT = (28, 28, 28)
COLOR_SUBTLE = (140, 140, 140)
COLOR_HINT = (170, 170, 170)
COLOR_THINK = (160, 160, 160)
COLOR_LINK = (37, 99, 235)               # 蓝色链接
COLOR_BORDER = (228, 228, 230)

font_title = load_font(FONT_BOLD, 42)         # 任务标题
font_user_msg = load_font(FONT_REGULAR, 30)   # 用户消息
font_ai_msg = load_font(FONT_REGULAR, 28)     # AI 消息
font_ai_title = load_font(FONT_BOLD, 30)      # AI 段落标题
font_meta = load_font(FONT_REGULAR, 24)       # 思考/制品提示
font_artifact = load_font(FONT_REGULAR, 26)   # 制品路径

def make_variant(name, task_title, user_msg=None, ai_blocks=None, think_text=None, artifact=None):
    """
    name: 输出文件名 (如 2.3-weekly-output.png)
    task_title: 顶部任务标题
    user_msg: 用户消息 (None 表示空状态, 不画气泡)
    ai_blocks: AI 回复块, list of dict
       - {"type": "h2", "text": "已完成事项"}
       - {"type": "li", "text": "A 项目..."}
       - {"type": "p", "text": "..."}
    think_text: "思考 1次" 提示
    artifact: "(已打开 weekly_report.docx)" 制品路径
    """
    img = Image.open(SRC).convert("RGB")
    W, H = img.size
    draw = ImageDraw.Draw(img)

    # 1. 顶部任务标题 (y=40-180) - 整块覆盖, x 范围到 2200 (保留进度面板)
    draw.rectangle([(460, 40), (2200, 180)], fill=COLOR_BG)
    draw.text((480, 60), task_title, fill=COLOR_TEXT, font=font_title)
    draw.text((480 + len(task_title)*42 + 30, 70), "▾", fill=COLOR_SUBTLE, font=font_title)

    # 2. 中央对话区 - 整块覆盖 (y=180-1450)
    draw.rectangle([(460, 180), (2400, 1450)], fill=COLOR_BG)

    y = 220

    # 3. 思考提示 (如果有)
    if think_text:
        draw.text((500, y), think_text, fill=COLOR_THINK, font=font_meta)
        y += 50

    # 4. 用户消息气泡 (右上,圆角矩形)
    if user_msg:
        # 测量文本宽度
        bbox = draw.textbbox((0, 0), user_msg, font=font_user_msg)
        text_w = bbox[2] - bbox[0]
        text_h = 50
        bubble_w = text_w + 60
        bubble_h = text_h + 30
        bubble_x = 2400 - bubble_w - 20
        bubble_y = y
        # 圆角矩形
        draw.rounded_rectangle(
            [(bubble_x, bubble_y), (bubble_x + bubble_w, bubble_y + bubble_h)],
            radius=14, fill=COLOR_USER_BUBBLE
        )
        draw.text((bubble_x + 30, bubble_y + 15), user_msg, fill=COLOR_TEXT, font=font_user_msg)
        y = bubble_y + bubble_h + 30

    # 5. AI 回复 (左对齐)
    if ai_blocks:
        for block in ai_blocks:
            btype = block["type"]
            text = block["text"]
            if btype == "h2":
                draw.text((500, y), text, fill=COLOR_TEXT, font=font_ai_title)
                y += 45
            elif btype == "li":
                # 列表项: • 缩进
                draw.text((510, y), "•", fill=COLOR_TEXT, font=font_ai_msg)
                draw.text((540, y), text, fill=COLOR_TEXT, font=font_ai_msg)
                y += 42
            elif btype == "p":
                draw.text((500, y), text, fill=COLOR_TEXT, font=font_ai_msg)
                y += 42
            elif btype == "h3":
                # 制品标题
                draw.text((500, y), text, fill=COLOR_TEXT, font=font_ai_title)
                y += 45

    # 6. 制品路径 (底部蓝色)
    if artifact:
        draw.text((500, 1370), artifact, fill=COLOR_LINK, font=font_artifact)

    # 7. 进度面板区域 (右侧,保留)
    # 不动

    out = f"{DST_DIR}/{name}"
    img.save(out, "PNG", optimize=True)
    size_kb = os.path.getsize(out) / 1024
    print(f"  {name}  {size_kb:.0f}KB")

# ============================================================
# 1.9-main-interface.png (空状态, 就是 base 本身)
# ============================================================
# 直接复制 v4-base.png
import shutil
shutil.copy(SRC, f"{DST_DIR}/1.9-main-interface.png")
print(f"  1.9-main-interface.png  (复制自 v4-base)")

# ============================================================
# 2.1 task-start.png (用户输入第一条消息,助手开始思考)
# ============================================================
make_variant(
    "2.1-task-start.png",
    task_title="周报整理",
    user_msg="帮我整理本周的工作周报",
    think_text="思考 1次",
)

# ============================================================
# 2.2 weekly-input.png (周报输入)
# ============================================================
make_variant(
    "2.2-weekly-input.png",
    task_title="周报整理",
    user_msg="帮我把本周完成的工作整理成周报",
    think_text="思考 1次",
)

# ============================================================
# 2.3 weekly-output.png (周报输出)
# ============================================================
make_variant(
    "2.3-weekly-output.png",
    task_title="周报整理",
    user_msg="帮我把本周完成的工作整理成周报",
    ai_blocks=[
        {"type": "h2", "text": "已生成周报草稿"},
        {"type": "p", "text": "本周共完成 8 项工作, 跟进 3 项, 下周计划 4 项。"},
        {"type": "h2", "text": "已完成事项"},
        {"type": "li", "text": "A 项目需求调研, 输出 12 页报告"},
        {"type": "li", "text": "B 客户合同确认, 排期周三签约"},
        {"type": "li", "text": "主持内部周会, 输出 6 项行动项"},
        {"type": "h2", "text": "进行中事项"},
        {"type": "li", "text": "C 客户方案修订 (v2 版本)"},
        {"type": "li", "text": "新员工入职培训推进"},
        {"type": "h2", "text": "下周计划"},
        {"type": "li", "text": "完成 A 项目交付, 启动 D 项目立项"},
    ],
    artifact="已生成周报草稿文件: weekly_report_2026-08.docx (artifacts)",
)

# ============================================================
# 2.4 excel-input.png
# ============================================================
make_variant(
    "2.4-excel-input.png",
    task_title="销售数据整理",
    user_msg="把销售明细按区域汇总, 生成 Excel 报告",
    think_text="思考 1次",
)

# ============================================================
# 2.5 excel-output.png
# ============================================================
make_variant(
    "2.5-excel-output.png",
    task_title="销售数据整理",
    user_msg="把销售明细按区域汇总, 生成 Excel 报告",
    ai_blocks=[
        {"type": "h2", "text": "分析报告已生成"},
        {"type": "p", "text": "报告包含 4 个工作表:"},
        {"type": "li", "text": "整体 KPI 卡片 (总销售额、销售量、退货率、退货率) + 月度汇总表"},
        {"type": "li", "text": "渠道分析 渠道 × 品类销售额透视表 + 月度渠道明细 (含环比增长)"},
        {"type": "li", "text": "品类分析 品类综合统计 (含退货率、占比) + 月度品类明细"},
        {"type": "li", "text": "原始明细 完整原始数据 (含退货序列) + 月度销售量 vs 退货量折线图"},
        {"type": "h2", "text": "基于数据的几个核心发现:"},
        {"type": "li", "text": "京东自营销售额最高, 是各渠道中的主力"},
        {"type": "li", "text": "数码配件是销售额最大的品类"},
        {"type": "li", "text": "3 月环比 2 月有明显增长, 整体呈上升趋势"},
        {"type": "li", "text": "微信小程序渠道体量较小, 有增长潜力"},
    ],
    artifact="已打开 销售分析报告.xlsx (artifacts)",
)

# ============================================================
# 2.6 ppt-input.png
# ============================================================
make_variant(
    "2.6-ppt-input.png",
    task_title="PPT 大纲生成",
    user_msg="帮我做一个季度复盘 PPT 的大纲, 12 页",
    think_text="思考 1次",
)

# ============================================================
# 2.7 ppt-output.png
# ============================================================
make_variant(
    "2.7-ppt-output.png",
    task_title="PPT 大纲生成",
    user_msg="帮我做一个季度复盘 PPT 的大纲, 12 页",
    ai_blocks=[
        {"type": "h2", "text": "已生成 12 页大纲"},
        {"type": "li", "text": "第 1 页: 开场与议程 — 介绍复盘范围与流程 — 2 分钟"},
        {"type": "li", "text": "第 2 页: 项目背景与目标回顾 — 2 分钟"},
        {"type": "li", "text": "第 3 页: 关键成就概览 — 3 分钟"},
        {"type": "li", "text": "第 4 页: 业绩数据详述 (Part 1) — 5 分钟"},
        {"type": "li", "text": "第 5 页: 业绩数据详述 (Part 2) — 5 分钟"},
        {"type": "li", "text": "第 6 页: 新客获取与渠道分析 — 4 分钟"},
        {"type": "li", "text": "第 7 页: 关键问题识别 — 5 分钟"},
        {"type": "li", "text": "第 8 页: 改进措施与行动计划 — 4 分钟"},
        {"type": "li", "text": "第 9 页: 资源需求与风险 — 3 分钟"},
        {"type": "li", "text": "第 10 页: Q4 目标与重点 — 3 分钟"},
        {"type": "li", "text": "第 11 页: 问答与讨论 — 10 分钟"},
        {"type": "li", "text": "第 12 页: 总结与下一步 — 2 分钟"},
    ],
    artifact="已生成 PPT 大纲: ppt_outline.py",
)

# ============================================================
# 2.8 translate-input.png
# ============================================================
make_variant(
    "2.8-translate-input.png",
    task_title="产品文档翻译",
    user_msg="把这份英文产品介绍翻译成中文",
    think_text="思考 1次",
)

# ============================================================
# 2.9 translate-output.png
# ============================================================
make_variant(
    "2.9-translate-output.png",
    task_title="产品文档翻译",
    user_msg="把这份英文产品介绍翻译成中文",
    ai_blocks=[
        {"type": "h2", "text": "翻译完成"},
        {"type": "p", "text": "原文 1842 词, 译文 1612 字符。关键术语映射:"},
        {"type": "li", "text": "\"onboarding\" → \"引导\""},
        {"type": "li", "text": "\"engagement\" → \"互动率\""},
        {"type": "li", "text": "\"retention\" → \"留存\""},
        {"type": "li", "text": "\"churn\" → \"流失\""},
        {"type": "li", "text": "\"funnel\" → \"漏斗\""},
        {"type": "h2", "text": "已处理文件:"},
        {"type": "li", "text": "产品介绍_zh.md  (中英对照版)"},
        {"type": "li", "text": "产品介绍_纯中文.md  (仅中文)"},
    ],
    artifact="已翻译文件: 产品介绍_zh.md",
)

# ============================================================
# 2.10 chart-output.png
# ============================================================
make_variant(
    "2.10-chart-output.png",
    task_title="销售图表生成",
    user_msg="把销售数据生成 4 张图表",
    ai_blocks=[
        {"type": "h2", "text": "已生成 4 张图表"},
        {"type": "li", "text": "各渠道销售额对比 (柱状图)"},
        {"type": "li", "text": "月度销售趋势 (折线图)"},
        {"type": "li", "text": "品类销售占比 (饼图)"},
        {"type": "li", "text": "退货率热力图"},
        {"type": "h2", "text": "图表已整合到 销售图表包.zip"},
    ],
    artifact="已打开 销售图表包.zip (artifacts)",
)

print("\n全部生成完成")
