"""
v8 变体: 基于 wb-v8-base.png (2400x1600) 真实 WorkBuddy v5.3.12
生成 1.9 + 2.1-2.10 共 11 张

改进点 (相对 v7):
- 1.9 现在带 4 个常用场景 chip (在 base 里有)
- 2.10 等输出图加 think_text (已有, 补全)
- 所有变体侧栏底部自动带 "已归档" + "提示词库" 补丁

UI 元素 (2400x1600 坐标):
- 左侧 (0-540):
  - y=120 WorkBuddy v5.3.12 logo
  - y=180-560 7 个 nav
  - y=640 任务分组
  - y=760 空间分组
  - y=900 已归档分组 (v8 新增)
  - y=1020 提示词库分组 (v8 新增, 含 3 示例)
  - y=1530 用户头像
- 顶部 (540-2400, y=0-130):
  - "本地助理" + "已连接:微信小程序" + 设置
- 中央对话 (540-2400, y=130-1400)
- 底部输入框 (540-2400, y=1400-1600)
"""
from PIL import Image, ImageDraw, ImageFont
import os
import shutil

BASE = "/Users/shike/Desktop/code/workbuddy-books"
SRC = f"{BASE}/第一卷/figures/wb-v8-base.png"
DST_DIR = f"{BASE}/第一卷/figures"

FONT_REGULAR = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/Users/shike/Library/Fonts/AlibabaPuHuiTi-3-75-SemiBold.otf"

def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception as e:
        return ImageFont.load_default()

# 配色
COLOR_BG = (255, 255, 255)
COLOR_USER_BUBBLE = (243, 243, 245)
COLOR_TEXT = (28, 28, 28)
COLOR_SUBTLE = (140, 140, 140)
COLOR_HINT = (170, 170, 170)
COLOR_THINK = (160, 160, 160)
COLOR_LINK = (37, 99, 235)

font_user_msg = load_font(FONT_REGULAR, 32)
font_ai_msg = load_font(FONT_REGULAR, 30)
font_ai_title = load_font(FONT_BOLD, 32)
font_meta = load_font(FONT_REGULAR, 26)
font_artifact = load_font(FONT_REGULAR, 28)
font_task_title = load_font(FONT_BOLD, 30)
font_status = load_font(FONT_REGULAR, 22)

def make_variant(name, user_msg=None, ai_blocks=None, think_text=None, artifact=None, task_title=None):
    """
    name: 输出文件名
    task_title: 顶部任务标题(可选,None 时用空状态)
    """
    img = Image.open(SRC).convert("RGB")
    W, H = img.size
    draw = ImageDraw.Draw(img)

    # 1. 顶部 - 保留"本地助理"标题
    # (不做特殊处理, 保留 v8 base 顶部)

    # 2. 中央对话区 - 整块覆盖 (y=130-1400)
    draw.rectangle([(540, 130), (2400, 1400)], fill=COLOR_BG)

    y = 200

    # 3. 思考提示 (如果有)
    if think_text:
        draw.text((600, y), think_text, fill=COLOR_THINK, font=font_meta)
        y += 60

    # 4. 用户消息气泡 (右上,圆角矩形)
    if user_msg:
        bbox = draw.textbbox((0, 0), user_msg, font=font_user_msg)
        text_w = bbox[2] - bbox[0]
        bubble_w = text_w + 80
        bubble_h = 70
        bubble_x = 2400 - bubble_w - 40
        bubble_y = y
        draw.rounded_rectangle(
            [(bubble_x, bubble_y), (bubble_x + bubble_w, bubble_y + bubble_h)],
            radius=18, fill=COLOR_USER_BUBBLE
        )
        draw.text((bubble_x + 40, bubble_y + 20), user_msg, fill=COLOR_TEXT, font=font_user_msg)
        y = bubble_y + bubble_h + 30

    # 5. AI 回复 (左对齐)
    if ai_blocks:
        for block in ai_blocks:
            btype = block["type"]
            text = block["text"]
            if btype == "h2":
                draw.text((600, y), text, fill=COLOR_TEXT, font=font_ai_title)
                y += 50
            elif btype == "li":
                draw.text((610, y), "•", fill=COLOR_TEXT, font=font_ai_msg)
                draw.text((650, y), text, fill=COLOR_TEXT, font=font_ai_msg)
                y += 48
            elif btype == "p":
                draw.text((600, y), text, fill=COLOR_TEXT, font=font_ai_msg)
                y += 48
            elif btype == "h3":
                draw.text((600, y), text, fill=COLOR_TEXT, font=font_ai_title)
                y += 50

    # 6. 状态信息 (在 AI 回复结束 + 制品之前, 突出"已完成 Ns")
    # 默认 status: "已完成 22s"
    if ai_blocks and not think_text:
        # 输出图: 在 AI 回复后, 制品前, 加 status
        status_text = f"✓ 已完成 22s"
        draw.text((600, y + 20), status_text, fill=COLOR_SUBTLE, font=font_status)

    # 7. 制品路径
    if artifact:
        draw.text((600, 1300), artifact, fill=COLOR_LINK, font=font_artifact)

    out = f"{DST_DIR}/{name}"
    img.save(out, "PNG", optimize=True)
    size_kb = os.path.getsize(out) / 1024
    print(f"  {name}  {size_kb:.0f}KB")

# ============================================================
# 1.9-main-interface.png (空状态, 就是 base 本身, 但要重新生成因为 v8 base 已加 chip)
# ============================================================
shutil.copy(SRC, f"{DST_DIR}/1.9-main-interface.png")
print(f"  1.9-main-interface.png  (复制自 v8-base, 已带 4 chip)")

# ============================================================
# 2.1 task-start.png
# ============================================================
make_variant(
    "2.1-task-start.png",
    user_msg="帮我整理本周的工作周报",
    think_text="已完成 22s",
)

# ============================================================
# 2.2 weekly-input.png
# ============================================================
make_variant(
    "2.2-weekly-input.png",
    user_msg="帮我把本周完成的工作整理成周报",
    think_text="已完成 22s",
)

# ============================================================
# 2.3 weekly-output.png
# ============================================================
make_variant(
    "2.3-weekly-output.png",
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
    artifact="已生成周报草稿文件: weekly_report_2026-08.docx",
)

# ============================================================
# 2.4 excel-input.png
# ============================================================
make_variant(
    "2.4-excel-input.png",
    user_msg="把销售明细按区域汇总, 生成 Excel 报告",
    think_text="已完成 35s",
)

# ============================================================
# 2.5 excel-output.png
# ============================================================
make_variant(
    "2.5-excel-output.png",
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
    artifact="已打开 销售分析报告.xlsx",
)

# ============================================================
# 2.6 ppt-input.png
# ============================================================
make_variant(
    "2.6-ppt-input.png",
    user_msg="帮我做一个季度复盘 PPT 的大纲, 12 页",
    think_text="已完成 41s",
)

# ============================================================
# 2.7 ppt-output.png
# ============================================================
make_variant(
    "2.7-ppt-output.png",
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
    user_msg="把这份英文产品介绍翻译成中文",
    think_text="已完成 18s",
)

# ============================================================
# 2.9 translate-output.png
# ============================================================
make_variant(
    "2.9-translate-output.png",
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
    user_msg="把销售数据生成 4 张图表",
    ai_blocks=[
        {"type": "h2", "text": "已生成 4 张图表"},
        {"type": "li", "text": "各渠道销售额对比 (柱状图)"},
        {"type": "li", "text": "月度销售趋势 (折线图)"},
        {"type": "li", "text": "品类销售占比 (饼图)"},
        {"type": "li", "text": "退货率热力图"},
        {"type": "h2", "text": "图表已整合到 销售图表包.zip"},
    ],
    artifact="已打开 销售图表包.zip",
)

print("\n全部生成完成")
