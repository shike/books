#!/usr/bin/env python3
"""
生成 ai-coding 53 张配图(SVG)。
每张图基于章节上下文设计具体内容,不止是占位框。
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from svg_renderer import render_figure, save

OUT_DIR = "/Users/shike/Desktop/code/books/ai-coding/figures"

# ===== ch00-01 (1+4 = 5 张) =====
FIGS = {}

FIGS["ai_coding_book_sec00_roadmap"] = {
    "layout": "timeline",
    "content": {
        "title": "本书阅读路线图",
        "steps": [
            {"name": "① 牌桌重排", "detail": "从选模型到选工作方式"},
            {"name": "② 复刻网站", "detail": "一次真实委托的四段式复刻"},
            {"name": "③ 登录 SaaS", "detail": "登录态 + 凭据保护"},
            {"name": "④ Demo 对齐", "detail": "介导的需求澄清"},
            {"name": "⑤ 周报自动化", "detail": "口径即代码"},
            {"name": "⑥ 飞书 Agent", "detail": "常驻 + 隔离子"},
            {"name": "⑦ 行业调研", "detail": "三件套分工"},
            {"name": "⑧ 经验蒸馏", "detail": "三层沉淀结构"},
        ]
    }
}

FIGS["ai_coding_book_sec01_fig01"] = {
    "layout": "quadrant",
    "content": {
        "title": "AI 编程生态四象限(模型 × 软件 × 套餐 × 开放度)",
        "items": [
            ("高开放度", "Anthropic / OpenAI|全栈闭环 + 生态友好|模型档位最完整"),
            ("垂直闭环", "国产三家(智谱 Kimi MiniMax)|模型 + 软件 + 套餐绑定|迁移成本差异显著"),
            ("海外旗舰", "Fable 5 / Opus 5 档位|能力第一档 · 价格第一档|复杂任务首选"),
            ("国产入门", "¥49 / 月档普及|迁移路径清晰 · 集成快|纯量任务成本最低"),
        ]
    }
}

FIGS["ai_coding_book_sec01_fig02"] = {
    "layout": "compare",
    "content": {
        "title": "上下文窗口:标称值 vs 有效值 vs 计费触发点",
        "left": {
            "title": "标称 vs 有效",
            "items": [
                "标称 1M 上下文:理论值",
                "有效 200K:实际可用(订阅)",
                "超出 200K 自动压缩摘要",
                "细节随压缩丢失"
            ],
            "color": "#0F4C81"
        },
        "right": {
            "title": "计费触发点",
            "items": [
                "输入 Token 计费起点",
                "缓存命中不计费(Kimi 优势)",
                "输出按 5× 价计",
                "5h 滚动 + 周上限双池"
            ],
            "color": "#16A085"
        }
    }
}

FIGS["ai_coding_book_sec01_fig03"] = {
    "layout": "compare",
    "content": {
        "title": "五家垂直闭环结构对比",
        "left": {
            "title": "海外两家",
            "items": [
                "Anthropic:Claude Code + 4 档模型",
                "OpenAI:Codex 4 形态 + GPT-5.6",
                "全栈闭环 · 生态最广",
                "支付 + 网络门槛"
            ],
            "color": "#0F4C81"
        },
        "right": {
            "title": "国产三家",
            "items": [
                "智谱:迁移成本最低(接口兼容 20+)",
                "Kimi:长任务成本最优(缓存免费)",
                "MiniMax:跑量任务默认后端",
                "¥49 入门 · 人民币计价"
            ],
            "color": "#16A085"
        }
    }
}

FIGS["ai_coding_book_sec01_fig04"] = {
    "layout": "tree",
    "content": {
        "title": "国内编程套餐选型决策树",
        "root": {
            "name": "你的核心场景",
            "children": [
                {
                    "name": "重度长任务(数小时+重复读)",
                    "children": [
                        {"name": "Kimi K3 档"},
                        {"name": "缓存命中免费"},
                        {"name": "白名单风险"},
                    ]
                },
                {
                    "name": "跑量任务(批量短请求)",
                    "children": [
                        {"name": "MiniMax Token Plan"},
                        {"name": "¥49/119/469"},
                        {"name": "复杂任务能力有限"},
                    ]
                },
                {
                    "name": "频繁迁移 / 多工具混用",
                    "children": [
                        {"name": "智谱 Z Code"},
                        {"name": "接口兼容 20+"},
                        {"name": "高峰限速"},
                    ]
                },
            ]
        }
    }
}

# ===== ch02 (4 张) =====

FIGS["ai_coding_book_sec02_four_stage"] = {
    "layout": "flow_h",
    "content": {
        "title": "复刻网站四段式工作流全貌",
        "steps": [
            {"name": "① 需求受理", "detail": "30 分钟诊断报告"},
            {"name": "② 难点识别", "detail": "技术 / 业务 / 过程"},
            {"name": "③ 四阶段执行", "detail": "骨架 → 仿真 → 对齐 → 验收"},
            {"name": "④ 验收交付", "detail": "量化检查项"},
        ]
    }
}

FIGS["ai_coding_book_sec02_timeline"] = {
    "layout": "timeline",
    "content": {
        "title": "复刻网站四阶段时间线",
        "steps": [
            {"name": "D1-2 骨架", "detail": "页面结构 + 路由"},
            {"name": "D3-5 仿真", "detail": "视觉 / 交互 / 数据"},
            {"name": "D6-7 对齐", "detail": "Demo + 客户反馈"},
            {"name": "D8+ 验收", "detail": "量化检查 + 交付"},
        ]
    }
}

FIGS["ai_coding_book_sec02_hallucination"] = {
    "layout": "grid",
    "content": {
        "title": "AI 幻觉模式图:三类典型撒谎",
        "items": [
            {"name": "虚构引用", "content": "捏造论文 / URL / 标准号|AI 自信编出" + "|看起来像真实文献"},
            {"name": "拼凑事实", "content": "把 A 项目的细节|嫁接到 B 项目|时间地点张冠李戴"},
            {"name": "推理短路", "content": "跳过中间步骤|直接给结论|逻辑链不可追溯"},
            {"name": "时序幻觉", "content": "把未来事件说成已发生|把旧版本说成新|时间锚点错位"},
        ],
        "cols": 2,
    }
}

FIGS["ai_coding_book_sec02_diff"] = {
    "layout": "compare",
    "content": {
        "title": "视觉差异比对:截图 vs 实际渲染",
        "left": {
            "title": "原始截图",
            "items": [
                "1080p 截图",
                "字体系统默认",
                "颜色取色器采得",
                "间距肉眼测量",
                "动效无法捕获"
            ],
            "color": "#0F4C81"
        },
        "right": {
            "title": "复刻渲染",
            "items": [
                "Flex/Grid 布局推算",
                "字体替代(Fallback)",
                "色值有 ±3 偏差",
                "间距用规范值",
                "动效用 CSS 估算"
            ],
            "color": "#D2691E"
        }
    }
}

# ===== ch03 (4 张) =====

FIGS["sec03_workflow"] = {
    "layout": "flow_h",
    "content": {
        "title": "复刻 SaaS 整体工作流",
        "steps": [
            {"name": "登录态获取", "detail": "Cookie / Token / Session"},
            {"name": "登录态保活", "detail": "定期心跳 + 过期前刷新"},
            {"name": "80% 固化", "detail": "登录 / 凭据 / 审计"},
            {"name": "20% AI 接管", "detail": "操作流程 + 业务判断"},
        ]
    }
}

FIGS["sec03_session_lifecycle"] = {
    "layout": "timeline",
    "content": {
        "title": "登录态生命周期",
        "steps": [
            {"name": "登录请求", "detail": "账号密码 / 扫码"},
            {"name": "Token 颁发", "detail": "短期(2h)+ 长期(7d)"},
            {"name": "使用中", "detail": "每次请求带 Token"},
            {"name": "过期前", "detail": "用 refresh 换新"},
            {"name": "失效", "detail": "需重新登录"},
        ]
    }
}

FIGS["sec03_8020_architecture"] = {
    "layout": "grid",
    "content": {
        "title": "80/20 混合架构:核心安全 vs AI 灵活",
        "items": [
            {"name": "80% 固化代码", "content": "登录认证 / 凭据加密|权限校验 / 操作审计|—— 不交给 AI"},
            {"name": "20% AI 接管", "content": "业务流程编排|数据处理逻辑|异常分支判断"},
            {"name": "边界:什么不归 AI", "content": "支付链路 · 权限变更|数据导出 · 关键操作|—— 必须人工确认"},
            {"name": "可审计:什么归 AI", "content": "内容生成 · 信息汇总|格式转换 · 推荐排序|—— 全程留痕"},
        ],
        "cols": 2,
    }
}

FIGS["sec03_five_shields"] = {
    "layout": "grid",
    "content": {
        "title": "五件套防护:SaaS 复刻的最小安全集",
        "items": [
            {"name": "① 凭据隔离", "content": "Token 不写代码|独立环境变量"},
            {"name": "② 操作审计", "content": "每次写操作留痕|可回滚可追溯"},
            {"name": "③ 权限边界", "content": "AI 仅访问必要资源|目录级围栏"},
            {"name": "④ 异常告警", "content": "异常操作触发@人|30s 内人工介入"},
            {"name": "⑤ 数据脱敏", "content": "日志中敏感字段|打码 / 加密"},
            {"name": "备份:回滚机制", "content": "变更前快照|一键回滚"},
        ],
        "cols": 3,
    }
}

# ===== ch04 (3 张) =====

FIGS["ai_coding_book_sec04_intent_debt_funnel"] = {
    "layout": "funnel",
    "content": {
        "title": "意图债的来源分布:100 → 30 → 5",
        "stages": [
            {"name": "客户原始表达", "detail": "模糊 1 句话"},
            {"name": "AI 解读", "detail": "3-5 个候选解读"},
            {"name": "Demo 介导对齐", "detail": "明确 1 个目标"},
            {"name": "可执行需求", "detail": "验收标准清晰"},
        ]
    }
}

FIGS["ai_coding_book_sec04_doc_vs_demo"] = {
    "layout": "compare",
    "content": {
        "title": "文档式对齐 vs Demo 对齐",
        "left": {
            "title": "文档式",
            "items": [
                "客户写 PRD / 需求清单",
                "AI 按文字执行",
                "交付后才发现'不是这意思'",
                "改 3 轮后交付"
            ],
            "color": "#D2691E"
        },
        "right": {
            "title": "Demo 介导",
            "items": [
                "AI 出可点击原型",
                "客户在原型上指指点点",
                "第 1 天就澄清歧义",
                "改 1 轮后交付"
            ],
            "color": "#16A085"
        }
    }
}

FIGS["ai_coding_book_sec04_demo_flow"] = {
    "layout": "flow_h",
    "content": {
        "title": "Demo 介导的需求对齐流程",
        "steps": [
            {"name": "客户一句话", "detail": "模糊诉求"},
            {"name": "AI 出原型", "detail": "30 分钟"},
            {"name": "客户指认", "detail": "对 / 错 / 不够"},
            {"name": "迭代原型", "detail": "直到对"},
            {"name": "可执行需求", "detail": "验收清单"},
        ]
    }
}

# ===== ch05 (3 张) =====

FIGS["ai_coding_book_sec05_cost"] = {
    "layout": "compare",
    "content": {
        "title": "口径即代码:成本表(真实 vs 模糊)",
        "left": {
            "title": "口径模糊",
            "items": [
                "'上上周销售额'",
                "未说明是否含退款",
                "未说明是否含线下",
                "未说明是否含未付款",
                "每周差 1-2 万"
            ],
            "color": "#D2691E"
        },
        "right": {
            "title": "口径固化",
            "items": [
                "'已完成 + 真实客户 + 上周'",
                "Git 版本管理",
                "AI 按口径脚本执行",
                "数字 100% 可复现",
                "审计日志可追溯"
            ],
            "color": "#16A085"
        }
    }
}

FIGS["ai_coding_book_sec05_pipeline"] = {
    "layout": "flow_h",
    "content": {
        "title": "数据管道四段式架构",
        "steps": [
            {"name": "取数", "detail": "凌晨 2 点定时 · SQL"},
            {"name": "清洗", "detail": "异常值 · 缺失 · 重复"},
            {"name": "分析", "detail": "维度 · 指标 · 对比"},
            {"name": "呈现", "detail": "图表 · 文字解读"},
        ]
    }
}

FIGS["ai_coding_book_sec05_dirty"] = {
    "layout": "grid",
    "content": {
        "title": "数据脏污示例与脱敏规则",
        "items": [
            {"name": "缺失字段", "content": "customer_id IS NULL|补默认 · 标 unknown"},
            {"name": "重复订单", "content": "order_id 重复|按 (时间,金额) 去重"},
            {"name": "测试订单", "content": "金额 = 0.01|过滤 · 不入账"},
            {"name": "敏感字段", "content": "手机号 / 身份证|日志中打码 · 入库加密"},
        ],
        "cols": 2,
    }
}

# ===== ch06 (4 张) =====

FIGS["sec06_cron_heartbeat"] = {
    "layout": "flow_v",
    "content": {
        "title": "定时心跳与异常处理流程",
        "steps": [
            {"name": "每日 9:00 触发", "detail": "cron 定时"},
            {"name": "拉取 14 项指标", "detail": "DAU / GMV / 转化 …"},
            {"name": "对比阈值", "detail": "±20% 异常"},
            {"name": "正常 → 出报告", "detail": "推飞书群"},
            {"name": "异常 → @ 责任人", "detail": "30s 内响应"},
        ]
    }
}

FIGS["sec06_unattended_day"] = {
    "layout": "timeline",
    "content": {
        "title": "AI 全天定时任务时间线",
        "steps": [
            {"name": "00:00", "detail": "数据归档"},
            {"name": "02:00", "detail": "取数 + 清洗"},
            {"name": "09:00", "detail": "每日巡检报告"},
            {"name": "14:00", "detail": "活动数据检查"},
            {"name": "周一 09:00", "detail": "周经营简报"},
            {"name": "异常随时", "detail": "@ 责任人"},
        ]
    }
}

FIGS["sec06_gateway_arch"] = {
    "layout": "grid",
    "content": {
        "title": "该框架 + 飞书对接架构",
        "items": [
            {"name": "飞书 IM", "content": "@ Agent / 接收通知|消息总线"},
            {"name": "该框架", "content": "常驻 Agent|7×24 在线"},
            {"name": "隔离子 Agent", "content": "每个任务独立会话|任务互不干扰"},
            {"name": "业务系统", "content": "数据库 / API|取数 + 操作"},
            {"name": "审计日志", "content": "每次操作留痕|合规可追溯"},
            {"name": "异常告警", "content": "30s 内 @ 责任人|人工兜底"},
        ],
        "cols": 3,
    }
}

FIGS["sec06_70_30_split"] = {
    "layout": "compare",
    "content": {
        "title": "常驻会话与隔离开子 Agent 比例",
        "left": {
            "title": "70% 常驻会话",
            "items": [
                "群聊 / IM 主入口",
                "维护对话上下文",
                "处理日常对话",
                "调度子任务"
            ],
            "color": "#0F4C81"
        },
        "right": {
            "title": "30% 隔离子 Agent",
            "items": [
                "执行具体任务",
                "独立会话隔离",
                "Token 不互相串扰",
                "失败不影响主会话"
            ],
            "color": "#16A085"
        }
    }
}

# ===== ch07 (3 张) =====

FIGS["sec07_afternoon_pipeline"] = {
    "layout": "flow_h",
    "content": {
        "title": "调研三件套调用顺序",
        "steps": [
            {"name": "① 爬虫建库", "detail": "权威资料入库"},
            {"name": "② RAG 主分析", "detail": "已入库资料做分析"},
            {"name": "③ 搜索补缺", "detail": "补 RAG 缺的信息"},
            {"name": "④ AI 整合", "detail": "多源差异摆台"},
        ]
    }
}

FIGS["sec07_data_source_decision"] = {
    "layout": "flow_v",
    "content": {
        "title": "数据源决策流程:何时用哪种",
        "steps": [
            {"name": "权威资料?", "detail": "IDC / Gartner / 财报"},
            {"name": "是 → 爬虫入库", "detail": "→ RAG 知识库"},
            {"name": "否 → 已知领域?", "detail": "已在知识库"},
            {"name": "是 → RAG 回答", "detail": "基于已有资料"},
            {"name": "否 → 搜索补缺", "detail": "补全后再分析"},
        ]
    }
}

FIGS["sec07_source_pyramid"] = {
    "layout": "pyramid",
    "content": {
        "title": "三类数据源的金字塔结构",
        "layers": [
            {"name": "权威报告", "items": "IDC · Gartner · 财报 | 数字唯一可信"},
            {"name": "专业媒体", "items": "36Kr · 虎嗅 · 极客公园 | 趋势与解读"},
            {"name": "公开资料", "items": "官方博客 · GitHub | 上下文与示例"},
            {"name": "网络讨论", "items": "论坛 · 知乎 · 推特 | 仅作线索 · 不作结论"},
        ]
    }
}

# ===== ch08 (3 张) =====

FIGS["ai_coding_book_sec08_three_layers"] = {
    "layout": "pyramid",
    "content": {
        "title": "知识的三层沉淀结构",
        "layers": [
            {"name": "Prompt 模板", "items": "人类直接复用 | 标准化最高"},
            {"name": "Skill", "items": "AI 自动调用 | 写给 AI 的操作规程"},
            {"name": "知识库", "items": "可被检索 | 五项结构 (场景/现象/原因/解法/效果)"},
            {"name": "个人记忆", "items": "散落各处 · 易流失 | 蒸馏起点"},
        ]
    }
}

FIGS["ai_coding_book_sec08_distill_flow"] = {
    "layout": "flow_h",
    "content": {
        "title": "自我蒸馏全流程",
        "steps": [
            {"name": "采集", "detail": "飞书发言 / 文档 / 笔记"},
            {"name": "识别", "detail": "AI 识别可结构化经验"},
            {"name": "分类", "detail": "按主题 + 上下文标签"},
            {"name": "沉淀", "detail": "知识库 / Skill / Prompt"},
            {"name": "复用", "detail": "新员工直接调用"},
        ]
    }
}

FIGS["ai_coding_book_sec08_four_steps"] = {
    "layout": "flow_h",
    "content": {
        "title": "经验采集四步流程",
        "steps": [
            {"name": "① 全量抓取", "detail": "3 年发言 + 文档"},
            {"name": "② AI 识别", "detail": "可结构化的经验段"},
            {"name": "③ 当事人确认", "detail": "是否记错 / 漏掉"},
            {"name": "④ 标签入库", "detail": "主题 + 上下文"},
        ]
    }
}

# ===== ch09 (3 张) =====

FIGS["sec09_dual_memory"] = {
    "layout": "compare",
    "content": {
        "title": "双记忆机制:显式 vs 隐式",
        "left": {
            "title": "显式记忆",
            "items": [
                "AI 主动写下的笔记",
                "结构化 · 可检索",
                "Token 成本高",
                "长期保留"
            ],
            "color": "#0F4C81"
        },
        "right": {
            "title": "隐式记忆",
            "items": [
                "上下文窗口内的对话",
                "临时 · 会话结束丢失",
                "Token 成本低",
                "短期参考"
            ],
            "color": "#16A085"
        }
    }
}

FIGS["sec09_feedback_loop"] = {
    "layout": "flow_v",
    "content": {
        "title": "反馈回路示意:数据 → AI → 人工 → 数据",
        "steps": [
            {"name": "AI 出结果", "detail": "基于历史数据"},
            {"name": "人工判断", "detail": "对 / 错 / 不够"},
            {"name": "反馈入库", "detail": "正确答案写入知识库"},
            {"name": "下次更准", "detail": "RAG 检索 + 蒸馏"},
        ]
    }
}

FIGS["sec09_context_cost"] = {
    "layout": "grid",
    "content": {
        "title": "上下文成本曲线:Token 用量 vs 任务质量",
        "items": [
            {"name": "0-20K", "content": "简单对话|质量线性增长|成本可接受"},
            {"name": "20K-100K", "content": "中等任务|质量缓增|开始出现边际递减"},
            {"name": "100K-500K", "content": "复杂任务|质量峰值区间|成本陡增"},
            {"name": ">500K", "content": "超出有效值|质量不稳定|细节压缩丢失"},
        ],
        "cols": 2,
    }
}

# ===== ch10 (4 张) =====

FIGS["sec10_vertical_slice"] = {
    "layout": "grid",
    "content": {
        "title": "MVP 垂直切片:核心路径完整 + 其余留空",
        "items": [
            {"name": "核心路径", "content": "用户从进入到付费|每个环节打通 · 不闪退"},
            {"name": "辅助功能", "content": "次要功能暂留占位|用 '即将上线' 标识"},
            {"name": "管理后台", "content": "仅核心查询 + 改|其余用 SQL 临时操作"},
            {"name": "边界条件", "content": "异常 / 边界用最简文案|后续补全"},
        ],
        "cols": 2,
    }
}

FIGS["sec10_gantt"] = {
    "layout": "timeline",
    "content": {
        "title": "7 天 MVP 时间盒甘特图",
        "steps": [
            {"name": "D1 骨架", "detail": "页面 + 路由"},
            {"name": "D2 数据库", "detail": "建表 + API"},
            {"name": "D3 核心功能", "detail": "登录 / 主流程"},
            {"name": "D4 支付", "detail": "接入支付链路"},
            {"name": "D5 测试", "detail": "Demo + Bug 修复"},
            {"name": "D6 上线", "detail": "部署 + 监控"},
            {"name": "D7 复盘", "detail": "数据 + 用户反馈"},
        ]
    }
}

FIGS["sec10_payment_decision"] = {
    "layout": "tree",
    "content": {
        "title": "收款链路决策树",
        "root": {
            "name": "收款需求",
            "children": [
                {
                    "name": "国内个人 / 小团队",
                    "children": [
                        {"name": "微信 / 支付宝"},
                        {"name": "二维码收款"},
                        {"name": "0 费率"},
                    ]
                },
                {
                    "name": "国内企业",
                    "children": [
                        {"name": "微信支付商户号"},
                        {"name": "需营业执照"},
                        {"name": "0.6% 费率"},
                    ]
                },
                {
                    "name": "海外用户",
                    "children": [
                        {"name": "Stripe"},
                        {"name": "支持国际卡"},
                        {"name": "2.9% + $0.3"},
                    ]
                },
            ]
        }
    }
}

FIGS["sec10_coldstart_channels"] = {
    "layout": "grid",
    "content": {
        "title": "冷启动渠道选择",
        "items": [
            {"name": "社区首发", "content": "V2EX · 知乎 · 即刻|种子用户 · 反馈快"},
            {"name": "创始人发声", "content": "创始人朋友圈 · 知乎|信任感强 · 触达窄"},
            {"name": "行业 KOL", "content": "垂类博主 · 公众号|精准 · 成本高"},
            {"name": "付费投放", "content": "信息流 · 搜索词|规模大 · 转化待测"},
        ],
        "cols": 2,
    }
}

# ===== ch11 (4 张) =====

FIGS["sec11_safety_net"] = {
    "layout": "grid",
    "content": {
        "title": "沙盒测试与回滚机制",
        "items": [
            {"name": "沙盒环境", "content": "生产数据副本|改动先在沙盒跑"},
            {"name": "蓝绿部署", "content": "新版本并行|蓝绿切换"},
            {"name": "自动回滚", "content": "异常 5min 内|自动切回旧版"},
            {"name": "变更前快照", "content": "数据库 + 配置|变更前自动备份"},
        ],
        "cols": 2,
    }
}

FIGS["sec11_three_phases"] = {
    "layout": "timeline",
    "content": {
        "title": "三阶段时间线:接养 → 稳态 → 进化",
        "steps": [
            {"name": "接养期", "detail": "接手 + 摸清边界"},
            {"name": "稳态期", "detail": "异常处理 + 监控"},
            {"name": "进化期", "detail": "模型迭代 + 业务优化"},
        ]
    }
}

FIGS["sec11_strangler_fig"] = {
    "layout": "flow_h",
    "content": {
        "title": "遗留系统 strangler 模式:逐层替换",
        "steps": [
            {"name": "旧系统", "detail": "整体运行"},
            {"name": "新接口", "detail": "代理层拦截"},
            {"name": "路由", "detail": "新功能走新系统"},
            {"name": "迁移", "detail": "老功能逐步替换"},
            {"name": "退役", "detail": "旧系统完全下线"},
        ]
    }
}

FIGS["sec11_archaeology_funnel"] = {
    "layout": "funnel",
    "content": {
        "title": "考古学式探索漏斗:从表层到根因",
        "stages": [
            {"name": "症状", "detail": "用户报告异常"},
            {"name": "现象", "detail": "时间 / 范围 / 模式"},
            {"name": "复现", "detail": "能稳定复现"},
            {"name": "根因", "detail": "代码 / 配置 / 数据"},
            {"name": "解法", "detail": "最小变更修复"},
        ]
    }
}

# ===== ch12 (3 张) =====

FIGS["sec12_pipeline"] = {
    "layout": "flow_v",
    "content": {
        "title": "三层管道架构:采集 → 处理 → 决策",
        "steps": [
            {"name": "采集层", "detail": "数据库 + API + 文件"},
            {"name": "处理层", "detail": "清洗 + 分析 + 蒸馏"},
            {"name": "决策层", "detail": "报告 + 告警 + 推荐"},
        ]
    }
}

FIGS["sec12_funnel"] = {
    "layout": "funnel",
    "content": {
        "title": "30 → 5 → 4 漏斗:从需求到交付的收敛",
        "stages": [
            {"name": "30 条需求", "detail": "客户原始诉求"},
            {"name": "5 个目标", "detail": "Demo 介导收敛"},
            {"name": "4 周交付", "detail": "MVP + 迭代"},
            {"name": "1 个上线", "detail": "完整可验收"},
        ]
    }
}

FIGS["sec12_cost"] = {
    "layout": "compare",
    "content": {
        "title": "三种买法成本对比",
        "left": {
            "title": "API 按量",
            "items": [
                "$5/$25 每百万 Token",
                "适合:服务用户上线后",
                "按用量 · 无额度限制",
                "需自建调度"
            ],
            "color": "#0F4C81"
        },
        "right": {
            "title": "订阅包月",
            "items": [
                "$20-$200/月 三档",
                "适合:个人天天使用",
                "定额池 · 5h+周双池",
                "额度耗尽即停"
            ],
            "color": "#16A085"
        }
    }
}

# ===== ch13 (4 张) =====

FIGS["sec13_context_triage"] = {
    "layout": "grid",
    "content": {
        "title": "上下文失效三类型判别",
        "items": [
            {"name": "溢出型", "content": "超出有效窗口|压缩摘要丢失细节|—— 拆任务"},
            {"name": "干扰型", "content": "无关上下文|挤掉关键信息|—— 清理"},
            {"name": "陈旧型", "content": "旧版本上下文|AI 给出过时答案|—— 重新喂入"},
        ],
        "cols": 3,
    }
}

FIGS["sec13_triple_debt"] = {
    "layout": "grid",
    "content": {
        "title": "三重债务模型:技术债 / 意图债 / 上下文债",
        "items": [
            {"name": "技术债", "content": "代码质量 / 架构|—— 长期不治会拖垮"},
            {"name": "意图债", "content": "客户原始诉求 vs 实现|—— 改版无底洞"},
            {"name": "上下文债", "content": "AI 错过关键信息|—— 决策失准"},
        ],
        "cols": 3,
    }
}

FIGS["sec13_ladder"] = {
    "layout": "pyramid",
    "content": {
        "title": "治理组合分阶段实施阶梯",
        "layers": [
            {"name": "L4: 自动化"},
            {"name": "L3: 监控 + 告警"},
            {"name": "L2: 流程规范"},
            {"name": "L1: 工具链"},
            {"name": "L0: 共识"},
        ]
    }
}

FIGS["sec13_four_diseases"] = {
    "layout": "grid",
    "content": {
        "title": "四类问题全景对照",
        "items": [
            {"name": "性能病", "content": "慢 · 卡顿|—— 优化算法 + 缓存"},
            {"name": "质量病", "content": "输出不准|—— 评估 + 蒸馏"},
            {"name": "成本病", "content": "费用高|—— 缓存 + 模型选择"},
            {"name": "体验病", "content": "用户不会用|—— 重设计交互"},
        ],
        "cols": 2,
    }
}

# ===== ch14 (3 张) =====

FIGS["sec14_decision_tree"] = {
    "layout": "tree",
    "content": {
        "title": "三类数据源决策树",
        "root": {
            "name": "数据需求",
            "children": [
                {
                    "name": "已知结构化",
                    "children": [
                        {"name": "数据库直查"},
                        {"name": "SQL 即可"},
                    ]
                },
                {
                    "name": "未知领域",
                    "children": [
                        {"name": "先用搜索探路"},
                        {"name": "再爬虫建库"},
                        {"name": "最后 RAG 分析"},
                    ]
                },
                {
                    "name": "实时监控",
                    "children": [
                        {"name": "订阅源 + 定时任务"},
                        {"name": "差异告警"},
                    ]
                },
            ]
        }
    }
}

FIGS["sec14_compliance_check"] = {
    "layout": "flow_v",
    "content": {
        "title": "抓取前实操自检流程",
        "steps": [
            {"name": "目标网站 robots.txt", "detail": "是否允许爬虫"},
            {"name": "版权声明 / ToS", "detail": "是否允许商业使用"},
            {"name": "数据规模评估", "detail": "是否触发风控"},
            {"name": "请求频率控制", "detail": "≤ 1 req/sec"},
            {"name": "数据脱敏", "detail": "敏感字段处理"},
            {"name": "留存期限", "detail": "原始数据 ≤ 90 天"},
        ]
    }
}

FIGS["sec14_walled_garden"] = {
    "layout": "timeline",
    "content": {
        "title": "抓取环境围墙化十年",
        "steps": [
            {"name": "2014", "detail": "开放 API"},
            {"name": "2017", "detail": "JS 渲染反爬"},
            {"name": "2020", "detail": "登录态必须"},
            {"name": "2023", "detail": "行为风控"},
            {"name": "2026", "detail": "设备指纹 + 关联账户"},
        ]
    }
}

# ===== ch15 (3 张) =====

FIGS["sec15_sdd_vs_superpowers"] = {
    "layout": "compare",
    "content": {
        "title": "SDD 规范层与执行习惯框架的分层",
        "left": {
            "title": "SDD 规范层",
            "items": [
                "Spec → Driven Development",
                "先写规范 · AI 按规范执行",
                "—— 适合:复杂业务"
            ],
            "color": "#0F4C81"
        },
        "right": {
            "title": "执行习惯框架",
            "items": [
                "技能 · 工作流 · 流程",
                "AI 复用既有经验",
                "—— 适合:重复任务"
            ],
            "color": "#16A085"
        }
    }
}

FIGS["sec15_subagent_token_flow"] = {
    "layout": "flow_h",
    "content": {
        "title": "子 Agent Token 流:主会话调度 + 子任务隔离",
        "steps": [
            {"name": "主会话", "detail": "接收任务 + 拆解"},
            {"name": "子 Agent A", "detail": "任务 1 + 独立 Token"},
            {"name": "子 Agent B", "detail": "任务 2 + 独立 Token"},
            {"name": "结果汇总", "detail": "回传主会话"},
        ]
    }
}

FIGS["sec15_four_levers"] = {
    "layout": "grid",
    "content": {
        "title": "四杠杆框架:质量 / 成本 / 速度 / 风险",
        "items": [
            {"name": "质量", "content": "评估集 + 蒸馏|高 = 慢"},
            {"name": "成本", "content": "缓存 + 模型选择|低 = 慢 / 质量"},
            {"name": "速度", "content": "模型升级 + 并行|快 = 贵"},
            {"name": "风险", "content": "沙盒 + 回滚 + 审计|低 = 慢"},
        ],
        "cols": 2,
    }
}

# ===== 生成所有图 =====
def main():
    print(f"Total figures: {len(FIGS)}")
    for name, spec in FIGS.items():
        try:
            svg = render_figure(name, spec["layout"], spec["content"])
            path = save(OUT_DIR, name, svg)
            print(f"  ✓ {name} → {path}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
            raise

if __name__ == "__main__":
    main()