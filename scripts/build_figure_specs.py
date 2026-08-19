#!/usr/bin/env python3
"""
books/scripts/build_figure_specs.py

从 workbuddy/fde/ai-coding 的章节,提取所有被引用的图名,
推断图类型(title/subtitle/items),生成 spec JSON 列表。

推断规则(基于图名+章节标题):
- 含 'time-allocation' / 'percent' / 'proportion' → pie
- 含 'comparison' / 'compare' / 'vs' / '对比' → bar
- 含 'flow' / 'process' / 'step' / 'loop' / 'workflow' → flow
- 含 'compare' / 'before-after' → compare
- 含 'quadrant' / 'matrix' / 'four' / '三象限' → grid
- 含 'funnel' / 'debt' / 'pyramid' → funnel
- 含 'matrix' / 'criteria' / 'score' → matrix
- 含 'screen' / 'ui' / 'interface' / 'login' / 'main' / 'workspace' / 'install' → screen
- 含 'radar' / 'capability' → grid
- 默认 → blank
"""
import os
import re
import json
from pathlib import Path
from collections import defaultdict

BOOKS_DIR = Path(__file__).resolve().parent.parent
WORKBUDDY = BOOKS_DIR / 'workbuddy'
FDE = BOOKS_DIR / 'fde'
AI = BOOKS_DIR / 'ai-coding'

# ----- 推断规则 -----

TYPE_RULES = [
    (r'time-allocation|percent|proportion|distribution|分布|占比', 'pie'),
    (r'comparison|compare|vs-|vs\.|对比|差异|区别', 'bar'),
    (r'flow|process|step|loop|workflow|pipeline|cycle|path|流程|步骤|循环|路径', 'flow'),
    (r'before-after|before_after|left-right|对比图|两栏|左右', 'compare'),
    (r'quadrant|matrix|four|五象限|三象限|四象限|网格|矩阵', 'grid'),
    (r'funnel|pyramid|leak|漏斗|金字塔', 'funnel'),
    (r'criteria|score|评级|评分|评估表', 'matrix'),
    (r'screen|ui-|main-|login|workspace|install|installer|ui-三栏|界面', 'screen'),
    (r'radar|capability|边界|能力', 'grid'),
]

# ----- 内容模板(根据图名关键词) -----

CONTENT_TEMPLATES = {
    # 第一卷:管理者 AI
    '1.1-website-hero': {
        'title': 'WorkBuddy 官网首页',
        'subtitle': '顶部"下载 WorkBuddy"按钮,一键获取客户端',
        'type': 'screen',
        'items': ['工作台 · 专家中心 · 技能市场 · 自动化', '个人版 · 团队版 · 企业版', '免费下载,集成多模型'],
        'screen_text': 'WorkBuddy · 桌面 AI 客户端',
    },
    '1.1.1-manager-time-allocation': {
        'title': '中层管理者一周时间分布',
        'subtitle': '会议与邮件合计占 63%,纯思考时间仅 10%',
        'type': 'pie',
        'items': [['邮件消息', 25], ['会议', 20], ['文档撰写', 20], ['数据处理', 10], ['决策', 15], ['其他', 10]],
    },
    '1.1.2-decision-density-roles': {
        'title': '不同岗位决策密度对比',
        'subtitle': '管理者约为一线员工的 3-5 倍',
        'type': 'bar',
        'items': [['一线员工', 2], ['基层管理', 4], ['中层管理', 8], ['高层管理', 12]],
    },
    '1.1.3-manager-info-three-sources': {
        'title': '管理者信息流三类来源',
        'subtitle': '文档、人、对话三类信息大多在本机',
        'type': 'compare',
        'items': [['文档资料', ['80% 在本机硬盘', 'OA/共享盘/邮件附件', '会议纪要/周报/月报']], ['人与对话', ['微信/飞书/邮件历史', '1:1 沟通记录', '客户外部消息']], ['系统数据', ['ERP/CRM/BI 导出', 'Excel/CSV 中间表', '日志与操作记录']]],
    },
    '1.1.4-agent-workflow': {
        'title': '桌面 AI 代理人工作流',
        'subtitle': '管理者只需要派活,执行由 AI 完成',
        'type': 'flow',
        'items': ['管理者派活', 'AI 拆解任务', '调用本地文件', '生成成品草稿', '管理者审阅签发'],
    },
    '1.1.5-workbuddy-capability-radar': {
        'title': 'WorkBuddy 能力边界示意图',
        'subtitle': '能做与不能做的清晰区分',
        'type': 'grid',
        'items': [
            ['文档处理 强', ['周报/汇报/邮件', '数据透视/PPT', '中译英/纪要']],
            ['知识检索 强', ['本地文件检索', '团队知识库', '专家经验调用']],
            ['自动化 中', ['定时任务', '事件触发', '工作流编排']],
            ['创新创造 弱', ['原创策略', '战略决策', '人际沟通']],
        ],
    },
    '1.1.6-manager-decision-attributes': {
        'title': '管理者决策的三个独特属性',
        'subtitle': '上下文、可审计、可复制',
        'type': 'flow',
        'items': ['决策需要完整上下文', '决策要可审计与追溯', '决策要可复制到他人'],
    },
    '1.2-windows-installer': {
        'title': 'Windows 安装包下载',
        'subtitle': 'WorkBuddySetup.exe 文件,资源管理器中显示',
        'type': 'screen',
        'items': ['WorkBuddySetup.exe · 286 MB', '双击开始安装', '安装包已通过数字签名验证'],
        'screen_text': 'WorkBuddySetup.exe',
    },
    '1.3-macos-drag-install': {
        'title': 'macOS 拖拽安装界面',
        'subtitle': '左侧 Applications 目标文件夹',
        'type': 'screen',
        'items': ['WorkBuddy.app', '拖入 Applications', '安装完成,Launchpad 启动'],
        'screen_text': '安装 WorkBuddy',
    },
    '1.3.1-main-ui-three-columns': {
        'title': 'WorkBuddy 主界面三栏布局',
        'subtitle': '左栏导航 · 中栏对话 · 右栏工具面板',
        'type': 'screen',
        'items': ['左栏:新建任务 / 助理 / 专家 / 技能 / 连接器 / 自动化', '中栏:对话流,顶部任务标题,底部输入框', '右栏:Skill / 模型 / 积分 / 日志 四个标签页'],
        'screen_text': 'WorkBuddy 主界面',
    },
    '1.3.2-skill-marketplace': {
        'title': 'WorkBuddy 技能市场浏览页',
        'subtitle': '列表展示多个 Skill,支持分类筛选与关键词搜索',
        'type': 'screen',
        'items': ['分类:全部/办公/财务/营销/技术/法律/教育', 'Skill 列表:周报助手/PPT 大纲/Excel 汇总', '关键词搜索:支持中文/英文'],
        'screen_text': '技能市场',
    },
    '1.3.3-middle-column-chat': {
        'title': '中栏对话区特写',
        'subtitle': '顶部任务标题 · 中部对话流 · 底部输入框',
        'type': 'screen',
        'items': ['任务标题:本周周报整理', '对话流:用户提问 + AI 回答', '输入框:支持附件拖拽'],
        'screen_text': '对话区',
    },
    '1.3.4-right-column-tools': {
        'title': '右栏工具面板',
        'subtitle': 'Skill / 模型 / 积分 / 日志 四个标签页',
        'type': 'screen',
        'items': ['Skill 标签:已绑定 5 个', '模型标签:DeepSeek/Kimi/豆包', '积分标签:本月剩余 23.5', '日志标签:最近 7 天操作'],
        'screen_text': '工具面板',
    },
    '1.3.5-credits-detail': {
        'title': '积分消耗明细',
        'subtitle': '分任务、对话、本月三个维度展示',
        'type': 'screen',
        'items': ['本月消耗:42.6 积分', '任务维度:周报 8.2 / PPT 6.5 / 邮件 3.4', '对话维度:7 次任务共 28.5 积分', '本周峰值:周二 12.4 积分'],
        'screen_text': '积分明细',
    },
    '1.4-login-page': {
        'title': 'WorkBuddy 登录界面',
        'subtitle': '三个登录选项并排',
        'type': 'screen',
        'items': ['手机号登录', '微信扫码登录', '企业 SSO 登录'],
        'screen_text': '登录 WorkBuddy',
    },
    '1.4.1-weekly-input': {
        'title': '周报整理输入态',
        'subtitle': '本周素材粘贴至对话窗口',
        'type': 'screen',
        'items': ['输入框:本周 5 项工作记录', '附件:邮件截图 2 张', '指令:"按项目分类整理成周报草稿"'],
        'screen_text': '周报整理 - 输入',
    },
    '1.4.2-weekly-output': {
        'title': '周报整理输出态',
        'subtitle': 'WorkBuddy 输出结构化周报',
        'type': 'screen',
        'items': ['项目 A:完成 X / 推进 Y / 待办 Z', '项目 B:客户拜访 3 次 / 合同签订 1 份', '下周计划:5 项工作重点', '可直接复制到 OA 系统'],
        'screen_text': '周报整理 - 输出',
    },
    '1.4.3-report-input': {
        'title': '汇报材料生成输入态',
        'subtitle': 'Q3 数据 + 重点项目进展',
        'type': 'screen',
        'items': ['Q3 营收数据 5 行', '重点项目 3 个', '指令:"生成 20 页汇报材料,带图表"'],
        'screen_text': '汇报材料 - 输入',
    },
    '1.4.4-report-output': {
        'title': '汇报材料生成输出态',
        'subtitle': '完整 PPT 大纲 + 12 张图表',
        'type': 'screen',
        'items': ['封面:2026 Q3 经营汇报', '第一部分:业绩总览 5 页', '第二部分:重点项目 8 页', '第三部分:风险与对策 5 页', '附录:数据明细 2 页'],
        'screen_text': '汇报材料 - 输出',
    },
    '1.4.5-translate-input': {
        'title': '中译英邮件输入态',
        'subtitle': '中文邮件正文粘贴',
        'type': 'screen',
        'items': ['邮件主题:关于 X 项目交付时间调整', '邮件正文 4 段', '指令:"翻译成商务英文,语气正式"'],
        'screen_text': '邮件翻译 - 输入',
    },
    '1.4.6-translate-output': {
        'title': '中译英邮件输出态',
        'subtitle': 'WorkBuddy 输出英文邮件',
        'type': 'screen',
        'items': ['主题:Schedule Adjustment for Project X', '正文 4 段,商务语气', '可一键复制 / 发送 / 存草稿'],
        'screen_text': '邮件翻译 - 输出',
    },
    '1.4.7-ppt-input': {
        'title': 'PPT 大纲生成输入态',
        'subtitle': '主题与受众信息输入',
        'type': 'screen',
        'items': ['主题:AI 在企业落地的 5 个坑', '受众:500 强 CIO 沙龙', '时长:30 分钟', '指令:"生成 12 页 PPT 大纲"'],
        'screen_text': 'PPT 大纲 - 输入',
    },
    '1.4.8-ppt-output': {
        'title': 'PPT 大纲生成输出态',
        'subtitle': 'WorkBuddy 输出 12 页大纲',
        'type': 'screen',
        'items': ['第 1 页:封面', '第 2-3 页:5 个坑的导览', '第 4-10 页:每坑一页', '第 11 页:行动建议', '第 12 页:Q&A'],
        'screen_text': 'PPT 大纲 - 输出',
    },
    '1.4.9-meeting-input': {
        'title': '会议纪要转结构化输入态',
        'subtitle': '会议录音转写文本',
        'type': 'screen',
        'items': ['会议时长:90 分钟', '参会人:8 人', '转写文本:12000 字', '指令:"按议题分类,提取决策与待办"'],
        'screen_text': '会议纪要 - 输入',
    },
    '1.4.10-meeting-output': {
        'title': '会议纪要转结构化输出态',
        'subtitle': '议题/决策/待办三栏分类',
        'type': 'screen',
        'items': ['议题 1:产品方向 - 决策:聚焦 ToB SaaS', '议题 2:Q4 预算 - 决策:缩减 15%', '议题 3:招聘 - 待办:HR 启动 3 个岗位', '纪要可一键发邮件给参会人'],
        'screen_text': '会议纪要 - 输出',
    },
    '1.5-folder-permission': {
        'title': '文件夹授权对话框',
        'subtitle': '请选择 WorkBuddy 可以访问的文件夹',
        'type': 'screen',
        'items': ['D:\\WorkBuddy_workspace', 'E:\\公司共享盘', '桌面 / 文档 / 下载', '权限:仅读取,不修改原文件'],
        'screen_text': '授权文件夹',
    },
    '1.5.1-prompting-types': {
        'title': '提问型 vs 派活型对话对比',
        'subtitle': '左侧多轮模糊对话,右侧一次清晰交付',
        'type': 'compare',
        'items': [['提问型', ['"AI 是什么?"', '对话 5-6 轮', '输出是知识讲解']], ['派活型', ['"按这个数据生成周报"', '一次完成', '输出是可发出去的成品']]],
    },
    '1.5.2-three-piece-template': {
        'title': '三件套填空模板',
        'subtitle': '目标、约束、输出三块填空区',
        'type': 'flow',
        'items': ['目标:要做什么', '约束:不能做什么', '输出:什么样的成品'],
    },
    '1.5.3-prompt-iteration-quadrants': {
        'title': '提示词迭代四象限',
        'subtitle': '横轴偏差大小,纵轴修正难度',
        'type': 'grid',
        'items': [
            ['小偏差 · 易修正', ['措辞调整', '示例补充', '格式修正']],
            ['大偏差 · 易修正', ['目标重写', '输出规范重定', '数据源切换']],
            ['小偏差 · 难修正', ['风格调优', '语气调整', '细节微调']],
            ['大偏差 · 难修正', ['任务重构', '全新设计', '拆分子任务']],
        ],
    },
    '1.5.4-prompt-evolution': {
        'title': '标准提示词 v1 到 v4 演化路径',
        'subtitle': '从 v1 提问型到 v4 派活型的逐步沉淀',
        'type': 'flow',
        'items': ['v1:帮我写个周报', 'v2:基于本周 5 个项目输出周报', 'v3:基于附件数据按模板输出', 'v4:基于本机文件 + 历史风格输出'],
    },
    '1.5.5-prompt-can-cannot': {
        'title': '提示词能写与不能写的事',
        'subtitle': '左侧可被验证的任务,右侧依赖判断的决策',
        'type': 'compare',
        'items': [['提示词能做', ['文档生成', '数据整理', '格式转换', '初稿撰写']], ['提示词难做', ['战略决策', '人际沟通', '原创策略', '价值判断']]],
    },
    '1.6-workspace-settings': {
        'title': '设置工作目录 UI',
        'subtitle': '用户正在选择 D:\\WorkBuddy_workspace',
        'type': 'screen',
        'items': ['主目录:D:\\WorkBuddy_workspace', '子目录:周报 / 月报 / 客户 / 项目', '权限:读写', '实时同步:开启'],
        'screen_text': '工作目录',
    },
    '1.6.1-prompt-to-skill': {
        'title': '提示词到 Skill 的演进路径',
        'subtitle': '四次迭代:从一次性对话到可复用工具',
        'type': 'flow',
        'items': ['一次对话', '常用提示词', '带变量模板', '完整 Skill'],
    },
    '1.6.2-skill-three-parts': {
        'title': 'Skill 三大构成',
        'subtitle': '触发条件、执行逻辑、输出规范,缺一不可',
        'type': 'flow',
        'items': ['触发条件:什么场景用', '执行逻辑:具体步骤', '输出规范:产物长什么样'],
    },
    '1.6.3-skill-marketplace': {
        'title': 'WorkBuddy 技能市场浏览界面',
        'subtitle': '左侧分类 · 中间 Skill 列表 · 右侧详情',
        'type': 'screen',
        'items': ['分类:办公/财务/营销/技术', 'Skill:周报助手 / 合同审核 / 数据透视', '详情:作者/版本/评价', '一键安装到我的 Skill 库'],
        'screen_text': '技能市场',
    },
    '1.6.4-prompt-to-skill-flow': {
        'title': '提示词到 Skill 转化标准流程',
        'subtitle': '5 步走',
        'type': 'flow',
        'items': ['收集常用提示词', '抽象成变量模板', '补充触发场景', '补充输出规范', '发布为团队 Skill'],
    },
    '1.6.5-skill-team-reuse': {
        'title': 'Skill 跨人复用模型',
        'subtitle': '老师傅经验 → Skill 化 → 全员复用',
        'type': 'flow',
        'items': ['老师傅个人经验', '整理为可执行步骤', '封装为 Skill', '团队全员调用'],
    },
    '1.7-macos-blocked': {
        'title': 'macOS 系统设置 → 隐私与安全性',
        'subtitle': 'WorkBuddy 被阻止的提示和"仍要打开"按钮位置',
        'type': 'screen',
        'items': ['"WorkBuddy 已被阻止"', '"仍要打开" 按钮位置', '系统偏好设置 → 隐私 → 完全磁盘访问'],
        'screen_text': '允许 WorkBuddy',
    },
    '1.8-defender-prompt': {
        'title': 'Windows Defender 弹窗',
        'subtitle': '询问是否允许 WorkBuddy 对设备进行更改',
        'type': 'screen',
        'items': ['"你想允许此应用对设备进行更改吗?"', '发布者:WorkBuddy Inc.', '文件源:此电脑上的硬盘', '按钮:是 / 否'],
        'screen_text': '用户账户控制',
    },
    '1.9-main-interface': {
        'title': 'WorkBuddy 主界面全景',
        'subtitle': '展示三栏布局',
        'type': 'screen',
        'items': ['顶部:用户头像 / 设置 / 帮助', '左栏:导航 6 项', '中栏:对话区', '右栏:工具面板'],
        'screen_text': 'WorkBuddy 主界面',
    },
    '1.10-credits-page': {
        'title': '账户设置页 - 积分余额',
        'subtitle': '显示当前积分、有效期、消耗明细',
        'type': 'screen',
        'items': ['当前积分:128.5', '有效期:2026-12-31', '本月消耗:42.6', '充值:微信 / 支付宝 / 对公转账'],
        'screen_text': '积分管理',
    },
    '2.1-task-start': {
        'title': 'WorkBuddy 主界面 - 准备新建任务',
        'subtitle': '点击"新建任务"开始',
        'type': 'screen',
        'items': ['左栏:点击"新建任务"', '中栏:弹出对话框', '任务类型:周报 / PPT / 邮件 / 自定义', '右侧:任务历史记录'],
        'screen_text': '新建任务',
    },
    '2.2-weekly-input': {
        'title': '周报整理输入态',
        'subtitle': '本周素材粘贴至对话窗口',
        'type': 'screen',
        'items': ['粘贴 5 项工作记录', '上传 2 个附件', '指令:"整理成周报"'],
        'screen_text': '周报 - 输入',
    },
    '2.3-weekly-output': {
        'title': '周报整理输出态',
        'subtitle': '结构化周报草稿',
        'type': 'screen',
        'items': ['本周完成:A 项目里程碑 / B 客户签约', '进行中:3 项工作', '下周计划:5 项重点', '一键复制 / 发邮件 / 存草稿'],
        'screen_text': '周报 - 输出',
    },
    '2.4-excel-input': {
        'title': 'Excel 汇总输入态',
        'subtitle': '多张 Excel 文件拖入工作区',
        'type': 'screen',
        'items': ['拖入 3 个 Excel 文件', '每个 5-10 列', '指令:"按客户合并,生成总表"'],
        'screen_text': 'Excel 汇总 - 输入',
    },
    '2.5-excel-output': {
        'title': 'Excel 汇总输出态',
        'subtitle': 'WorkBuddy 输出合并后的 Excel',
        'type': 'screen',
        'items': ['合并后总表:120 行 × 12 列', '按客户分组', '新增"合并说明"列', '可一键下载 / 存入指定目录'],
        'screen_text': 'Excel 汇总 - 输出',
    },
    '2.6-ppt-input': {
        'title': 'PPT 大纲输入态',
        'subtitle': '主题与受众信息',
        'type': 'screen',
        'items': ['主题:Q4 战略复盘', '受众:董事会 5 人', '时长:20 分钟', '指令:"生成 10 页大纲"'],
        'screen_text': 'PPT - 输入',
    },
    '2.7-ppt-output': {
        'title': 'PPT 大纲输出态',
        'subtitle': 'WorkBuddy 输出 10 页大纲',
        'type': 'screen',
        'items': ['第 1 页:封面', '第 2 页:目录', '第 3-7 页:5 项复盘', '第 8-9 页:行动方案', '第 10 页:Q&A'],
        'screen_text': 'PPT - 输出',
    },
    '2.8-translate-input': {
        'title': '邮件翻译输入态',
        'subtitle': '中文邮件正文',
        'type': 'screen',
        'items': ['粘贴中文邮件 4 段', '指令:"翻译成英文"'],
        'screen_text': '邮件翻译 - 输入',
    },
    '2.9-translate-output': {
        'title': '邮件翻译输出态',
        'subtitle': 'WorkBuddy 输出英文邮件',
        'type': 'screen',
        'items': ['英文邮件 4 段', '商务语气', '一键复制'],
        'screen_text': '邮件翻译 - 输出',
    },
    '2.10-chart-output': {
        'title': '图表生成输出态',
        'subtitle': 'WorkBuddy 生成的柱状图',
        'type': 'screen',
        'items': ['数据:各产品线 Q3 营收', '图表类型:柱状图 + 折线', '配色:莫兰迪蓝绿', '可下载 PNG / 嵌入 PPT'],
        'screen_text': '图表输出',
    },
    '2.x-credits-detail': {
        'title': '积分消耗明细',
        'subtitle': '按任务类型分布',
        'type': 'pie',
        'items': [['周报', 30], ['PPT', 25], ['邮件', 15], ['Excel', 20], ['其他', 10]],
    },
    '2.x-decision-density': {
        'title': '管理决策密度时间分布',
        'subtitle': '管理者每日决策密度',
        'type': 'bar',
        'items': [['9 时', 8], ['10 时', 15], ['11 时', 20], ['14 时', 12], ['15 时', 18], ['16 时', 22], ['17 时', 10]],
    },
    '2.x-funnel': {
        'title': '任务处理漏斗',
        'subtitle': '从需求到交付的转化',
        'type': 'funnel',
        'items': [['需求提出', 100], ['任务派发', 85], ['AI 处理', 75], ['人工审阅', 60], ['交付完成', 50]],
    },
    '2.x-three-sources': {
        'title': '信息源三类分布',
        'subtitle': '管理者每天接收信息的来源',
        'type': 'pie',
        'items': [['邮件消息', 40], ['会议讨论', 30], ['文档报告', 20], ['系统数据', 10]],
    },
    '2.x-flow-overview': {
        'title': 'AI 辅助决策流程',
        'subtitle': '从问题到决策的五步走',
        'type': 'flow',
        'items': ['问题识别', '信息收集', '方案生成', '方案评估', '决策执行'],
    },
}


def extract_referenced_figs(chapter_md):
    """从章节 md 中提取所有 figures/ 引用,返回 [(fig_path, alt_text), ...]"""
    refs = []
    pattern = re.compile(r'!\[([^\]]*)\]\(figures/([^)]+)\)')
    for m in pattern.finditer(chapter_md):
        alt, path = m.group(1), m.group(2)
        refs.append((path, alt))
    return refs


def collect_all_refs():
    """收集所有书的图引用"""
    all_refs = []
    
    # workbuddy 三卷
    for vol in ['第一卷', '第二卷', '第三卷']:
        ch_dir = WORKBUDDY / vol / 'chapters'
        if ch_dir.exists():
            for f in sorted(ch_dir.glob('*.md')):
                if f.name.startswith('_'):
                    continue
                refs = extract_referenced_figs(f.read_text(encoding='utf-8'))
                for path, alt in refs:
                    all_refs.append({
                        'book': 'workbuddy',
                        'vol': vol,
                        'chapter': f.name,
                        'fig_name': path,
                        'alt': alt,
                    })
        ap_dir = WORKBUDDY / vol / 'appendices'
        if ap_dir.exists():
            for f in sorted(ap_dir.glob('*.md')):
                if f.name.startswith('_'):
                    continue
                refs = extract_referenced_figs(f.read_text(encoding='utf-8'))
                for path, alt in refs:
                    all_refs.append({
                        'book': 'workbuddy',
                        'vol': vol,
                        'chapter': f'appendices/{f.name}',
                        'fig_name': path,
                        'alt': alt,
                    })
    
    # ai-coding
    for sub in ['chapters', 'appendices', 'assets']:
        d = AI / sub
        if d.exists():
            for f in sorted(d.rglob('*.md')):
                if '_archive' in str(f):
                    continue
                refs = extract_referenced_figs(f.read_text(encoding='utf-8'))
                for path, alt in refs:
                    all_refs.append({
                        'book': 'ai-coding',
                        'vol': '',
                        'chapter': f'{sub}/{f.relative_to(d)}',
                        'fig_name': path,
                        'alt': alt,
                    })
    
    return all_refs


def build_spec(ref, template_overrides=None):
    """根据引用信息生成 spec dict"""
    fig_name = ref['fig_name']
    stem = fig_name.replace('.png', '').replace('.jpg', '').replace('.svg', '')
    
    # 优先用模板
    if template_overrides and stem in template_overrides:
        spec = dict(template_overrides[stem])
    elif stem in CONTENT_TEMPLATES:
        spec = dict(CONTENT_TEMPLATES[stem])
    else:
        # 用 alt 文字作为标题
        title = ref.get('alt', stem).strip()
        if not title:
            title = stem
        # 推断类型
        fig_type = 'blank'
        for pat, t in TYPE_RULES:
            if re.search(pat, stem, re.IGNORECASE):
                fig_type = t
                break
        spec = {
            'title': title,
            'subtitle': '',
            'type': fig_type,
            'items': [],
        }
    
    # 输出路径
    if ref['book'] == 'workbuddy':
        out = WORKBUDDY / ref['vol'] / 'figures' / fig_name
    else:
        # ai-coding 用 ../figures/xxx
        out = AI / 'figures' / fig_name
    
    spec['output'] = str(out)
    return spec


def main():
    refs = collect_all_refs()
    print(f'共 {len(refs)} 条图引用')
    
    # 去重(按 fig_name)
    seen = set()
    unique = []
    for r in refs:
        if r['fig_name'] not in seen:
            seen.add(r['fig_name'])
            unique.append(r)
    print(f'去重后 {len(unique)} 张图')
    
    # 生成 spec
    specs = []
    missing_template = []
    for r in unique:
        try:
            spec = build_spec(r)
            specs.append(spec)
        except Exception as e:
            print(f'  ERR {r["fig_name"]}: {e}')
    
    # 写 json
    out_path = BOOKS_DIR / 'scripts' / 'figure_specs.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(specs, f, ensure_ascii=False, indent=2)
    print(f'已生成 {len(specs)} 个 spec → {out_path.relative_to(BOOKS_DIR)}')
    
    # 统计各类型
    from collections import Counter
    type_count = Counter(s.get('type', 'blank') for s in specs)
    print('图型分布:')
    for t, n in type_count.most_common():
        print(f'  {t:10s} {n}')


if __name__ == '__main__':
    main()
