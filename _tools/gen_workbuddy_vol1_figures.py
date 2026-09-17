#!/usr/bin/env python3
"""
生成 workbuddy 第一卷 53 张配图(SVG)。
每章分配:ch01-06 各 7 张,ch07 5 张,ch08 6 张 = 53
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from svg_renderer import render_figure, save

OUT_DIR = "/Users/shike/Desktop/code/books/workbuddy/第一卷/figures"

FIGS = {}

# ===== ch01: 管理者为什么需要桌面 AI (7 张) =====

FIGS["1.1.1-manager-workload-pie"] = {
    "layout": "grid",
    "content": {
        "title": "中层管理者每周 50 小时工作负荷分布",
        "items": [
            {"name": "邮件 / 消息", "content": "25% · 12.5h"},
            {"name": "会议", "content": "20% · 10h"},
            {"name": "文档撰写", "content": "20% · 10h"},
            {"name": "数据处理", "content": "10% · 5h"},
            {"name": "决策判断", "content": "15% · 7.5h"},
            {"name": "其他", "content": "10% · 5h"},
        ],
        "cols": 3,
    }
}

FIGS["1.1.2-mechanical-vs-judgment"] = {
    "layout": "compare",
    "content": {
        "title": "32-37 小时被机械劳动吃掉 vs 12.5-17.5 小时真正决策",
        "left": {
            "title": "机械劳动(32-37h)",
            "items": ["读邮件 · 判断已读不回", "文档打字 / 改格式", "导数据 · 清洗 · 画图", "流程跑腿 · 信息搬运"],
            "color": "#D2691E"
        },
        "right": {
            "title": "判断决策(12.5-17.5h)",
            "items": ["战略方向 · 风险评估", "团队指导 · 1:1", "跨部门协调", "复盘 · 学习"],
            "color": "#0F4C81"
        }
    }
}

FIGS["1.2.1-cloud-ai-pain-points"] = {
    "layout": "grid",
    "content": {
        "title": "云端 AI 解决不了管理者的核心痛点",
        "items": [
            {"name": "周报场景", "content": "需读本周邮件 / 聊天|云端 AI 需手动复制粘贴"},
            {"name": "PPT 场景", "content": "需读本周报告 / 数据|复制粘贴比直接做更累"},
            {"name": "纪要场景", "content": "需读录音转写 + 行动项|云端无法读本地文件"},
            {"name": "数据透视", "content": "需读本地 Excel|云端无法访问本地"},
        ],
        "cols": 2,
    }
}

FIGS["1.2.2-five-scenarios-cloud-ai-fail"] = {
    "layout": "compare",
    "content": {
        "title": "云端 AI 在 5 个场景的真实体验",
        "left": {
            "title": "云端 AI 的回答",
            "items": [
                "通用模板 · 千篇一律",
                "不知道你电脑上的真实文件",
                "需手动复制粘贴材料",
                "每周重复 · 累"
            ],
            "color": "#D2691E"
        },
        "right": {
            "title": "桌面 AI 应该做的",
            "items": [
                "基于本地真实数据",
                "无需复制粘贴 · 直接读",
                "每周自动 · 一次性配置",
                "省心 · 准"
            ],
            "color": "#16A085"
        }
    }
}

FIGS["1.3.1-desktop-ai-three-features"] = {
    "layout": "grid",
    "content": {
        "title": "桌面 AI 客户端的差异化价值",
        "items": [
            {"name": "本地访问", "content": "授权文件夹后|AI 可读你电脑文件"},
            {"name": "多模型路由", "content": "通用入口 + 多模型|按任务自动选"},
            {"name": "持久记忆", "content": "团队历史 / 个人偏好|AI 越来越懂你"},
        ],
        "cols": 3,
    }
}

FIGS["1.3.2-who-fits-workbuddy"] = {
    "layout": "tree",
    "content": {
        "title": "你适合用 WorkBuddy 吗?决策树",
        "root": {
            "name": "你是中层管理者?",
            "children": [
                {
                    "name": "每周 ≥ 5 小时处理文档/邮件",
                    "children": [
                        {"name": "适合 WorkBuddy"},
                        {"name": "省 5-10h/周"},
                    ]
                },
                {
                    "name": "需要跨部门协调",
                    "children": [
                        {"name": "适合"},
                        {"name": "AI 整理沟通记录"},
                    ]
                },
                {
                    "name": "是工程师 / 个人贡献者",
                    "children": [
                        {"name": "用 Cursor / Claude Code"},
                        {"name": "WorkBuddy 不专为编码"},
                    ]
                },
            ]
        }
    }
}

FIGS["1.4.1-book-value-matrix"] = {
    "layout": "grid",
    "content": {
        "title": "读完这本书你能得到什么",
        "items": [
            {"name": "个人效率", "content": "省 5-10 小时/周"},
            {"name": "5 个场景", "content": "周报 / 邮件 / PPT / 纪要 / 数据"},
            {"name": "提示词能力", "content": "五段式 · 复制可用"},
            {"name": "成本意识", "content": "积分 / 模型路由"},
            {"name": "团队准备", "content": "第二卷衔接"},
        ],
        "cols": 3,
    }
}

# ===== ch02: 装上 WorkBuddy (7 张) =====

FIGS["2.1.1-download-steps"] = {
    "layout": "flow_h",
    "content": {
        "title": "下载 WorkBuddy:4 步",
        "steps": [
            {"name": "① 访问官网", "detail": "workbuddy.cn/download"},
            {"name": "② 系统识别", "detail": "Windows / macOS"},
            {"name": "③ 选择包", "detail": "在线 / 离线 / Beta"},
            {"name": "④ 下载", "detail": "8-480 MB"},
        ]
    }
}

FIGS["2.1.2-windows-vs-macos"] = {
    "layout": "compare",
    "content": {
        "title": "Windows vs macOS 安装包对比",
        "left": {
            "title": "Windows",
            "items": ["WorkBuddySetup.exe", "约 8 MB", "在线安装 · 自动更新"],
            "color": "#0F4C81"
        },
        "right": {
            "title": "macOS",
            "items": ["WorkBuddy-x.x.x.dmg", "约 480 MB", "完整客户端打包"],
            "color": "#16A085"
        }
    }
}

FIGS["2.2.1-install-windows-steps"] = {
    "layout": "flow_v",
    "content": {
        "title": "Windows 安装 6 步",
        "steps": [
            {"name": "双击 .exe"},
            {"name": "同意许可"},
            {"name": "选择安装目录"},
            {"name": "等待复制文件"},
            {"name": "桌面生成快捷方式"},
            {"name": "首次启动"},
        ]
    }
}

FIGS["2.2.2-install-macos-steps"] = {
    "layout": "flow_v",
    "content": {
        "title": "macOS 安装 5 步",
        "steps": [
            {"name": "双击 .dmg"},
            {"name": "拖到 Applications"},
            {"name": "首次启动授权"},
            {"name": "同意 Gatekeeper"},
            {"name": "完成"},
        ]
    }
}

FIGS["2.3.1-folder-authorization"] = {
    "layout": "grid",
    "content": {
        "title": "文件夹授权机制:为什么 WorkBuddy 跟云端不同",
        "items": [
            {"name": "授权范围", "content": "WorkBuddy 仅访问|你授权的目录"},
            {"name": "数据流向", "content": "本地处理 · 不上传云端"},
            {"name": "权限回收", "content": "随时取消授权|WorkBuddy 立即停止访问"},
            {"name": "云端对比", "content": "云端 AI 需手动|复制粘贴文件"},
        ],
        "cols": 2,
    }
}

FIGS["2.3.2-three-login-methods"] = {
    "layout": "compare",
    "content": {
        "title": "三种登录方式对比",
        "left": {
            "title": "手机号登录",
            "items": ["国内用户首选", "验证码", "30 秒完成"],
            "color": "#0F4C81"
        },
        "right": {
            "title": "微信 / 企业微信",
            "items": ["免密码", "团队统一身份", "适合公司配"],
            "color": "#16A085"
        }
    }
}

FIGS["2.4.1-first-task-walkthrough"] = {
    "layout": "flow_h",
    "content": {
        "title": "首次任务跑通:6 步确认安装成功",
        "steps": [
            {"name": "新建任务", "detail": "左栏 + 按钮"},
            {"name": "输入提示词", "detail": "中栏底部"},
            {"name": "选择模型", "detail": "自动 / 指定"},
            {"name": "提交", "detail": "Enter / 点击"},
            {"name": "查看结果", "detail": "中栏滚动"},
            {"name": "保存到收藏", "detail": "右栏 ☆"},
        ]
    }
}

# ===== ch03: 主界面与三栏布局 (7 张) =====

FIGS["3.1.1-three-column-layout"] = {
    "layout": "grid",
    "content": {
        "title": "三栏布局:总览",
        "items": [
            {"name": "左栏 · 导航", "content": "200px|历史 · 收藏 · 技能市场"},
            {"name": "中栏 · 主体", "content": "600px|对话 · AI 回复 · 输出"},
            {"name": "右栏 · 上下文", "content": "300px|文件 · 模型状态 · 资料"},
            {"name": "顶部条", "content": "全局菜单 · 任务状态 · 模型路由"},
            {"name": "底部条", "content": "积分余额 · 提示词输入"},
        ],
        "cols": 3,
    }
}

FIGS["3.1.2-three-column-rationale"] = {
    "layout": "compare",
    "content": {
        "title": "为什么是三栏不是两栏或四栏",
        "left": {
            "title": "两栏的缺点",
            "items": ["工具/上下文无位置", "挤在主体里(乱)", "藏到二级菜单(找不到)"],
            "color": "#D2691E"
        },
        "right": {
            "title": "三栏的优势",
            "items": ["屏幕宽度 vs 信息密度最佳折中", "1280×800 笔记本刚好", "左 200 + 中 600 + 右 300"],
            "color": "#16A085"
        }
    }
}

FIGS["3.2.1-left-column-four-zones"] = {
    "layout": "pyramid",
    "content": {
        "title": "左栏 4 区(从上到下)",
        "layers": [
            {"name": "新建任务 + 搜索"},
            {"name": "历史任务(按时间倒序)"},
            {"name": "收藏(常用提示词)"},
            {"name": "技能市场(团队共享)"},
        ]
    }
}

FIGS["3.2.2-middle-column-elements"] = {
    "layout": "grid",
    "content": {
        "title": "中栏元素全览",
        "items": [
            {"name": "任务标题", "content": "可编辑 · 自动保存"},
            {"name": "对话气泡", "content": "用户左 · AI 右"},
            {"name": "Markdown 渲染", "content": "代码高亮 · 表格"},
            {"name": "附件区", "content": "已上传文件预览"},
            {"name": "操作按钮", "content": "复制 · 重生成 · 反馈"},
            {"name": "输入框", "content": "提示词 + 文件拖入"},
        ],
        "cols": 3,
    }
}

FIGS["3.3.1-right-column-context"] = {
    "layout": "grid",
    "content": {
        "title": "右栏 4 个标签(默认)",
        "items": [
            {"name": "文件", "content": "当前任务关联文件|可拖入新增"},
            {"name": "模型", "content": "路由状态 · 当前调用|可手动切换"},
            {"name": "日志", "content": "本次任务操作记录"},
            {"name": "工具", "content": "插件 · 函数调用状态"},
        ],
        "cols": 2,
    }
}

FIGS["3.4.1-top-bar-elements"] = {
    "layout": "flow_h",
    "content": {
        "title": "顶部条 5 元素",
        "steps": [
            {"name": "≡ 菜单", "detail": "主菜单 · 设置"},
            {"name": "WorkBuddy", "detail": "logo · 状态"},
            {"name": "任务标题", "detail": "可编辑"},
            {"name": "模型路由", "detail": "自动/指定"},
            {"name": "用户头像", "detail": "积分 · 设置"},
        ]
    }
}

FIGS["3.5.1-shortcut-keys"] = {
    "layout": "grid",
    "content": {
        "title": "10 个最常用快捷键",
        "items": [
            {"name": "⌘ N", "content": "新建任务"},
            {"name": "⌘ K", "content": "命令面板"},
            {"name": "⌘ /", "content": "搜索"},
            {"name": "⌘ ⇧ F", "content": "格式化"},
            {"name": "⌘ ⏎", "content": "提交"},
            {"name": "⌘ S", "content": "保存到收藏"},
            {"name": "⌘ R", "content": "重生成"},
            {"name": "⌘ Z", "content": "撤销"},
            {"name": "⌘ 1/2/3", "content": "切换左中右栏"},
            {"name": "⌘ ,", "content": "偏好设置"},
        ],
        "cols": 5,
    }
}

# ===== ch04: 5 个管理者高频场景 (7 张) =====

FIGS["4.0.1-five-scenes-trader"] = {
    "layout": "grid",
    "content": {
        "title": "管理者每周 5 个 AI 高价值场景",
        "items": [
            {"name": "周报生成", "content": "AI 读邮件 + 写 1500 字"},
            {"name": "邮件润色", "content": "大白话 → 专业邮件"},
            {"name": "PPT 大纲", "content": "AI 读报告 + 出 15 页框架"},
            {"name": "会议纪要", "content": "录音转写 → 决策与行动项"},
            {"name": "数据透视", "content": "Excel → AI 出洞察"},
        ],
        "cols": 3,
    }
}

FIGS["4.1.1-weekly-report-flow"] = {
    "layout": "flow_h",
    "content": {
        "title": "周报生成:4 步流程",
        "steps": [
            {"name": "准备目录", "detail": "本周邮件/聊天/文档"},
            {"name": "新建任务", "detail": "用模板"},
            {"name": "AI 读 + 写", "detail": "30 秒"},
            {"name": "审阅修改", "detail": "10 分钟"},
        ]
    }
}

FIGS["4.1.2-weekly-report-prompt-template"] = {
    "layout": "grid",
    "content": {
        "title": "周报提示词模板(五段式)",
        "items": [
            {"name": "角色", "content": "你是 10 年经验的部门负责人"},
            {"name": "任务", "content": "基于本周文件生成周报"},
            {"name": "约束", "content": "1200-1500 字 · 三段式"},
            {"name": "素材", "content": "~/Documents/工作周报/W37/"},
            {"name": "输出", "content": "完成项 + 进度项 + 下周计划"},
        ],
        "cols": 3,
    }
}

FIGS["4.2.1-email-polish-3-mistakes"] = {
    "layout": "grid",
    "content": {
        "title": "邮件润色:3 个常见坑",
        "items": [
            {"name": "坑 1:太正式", "content": "AI 改得不像你写的|—— 加'保持本人语气'约束"},
            {"name": "坑 2:没上下文", "content": "AI 不知道写给谁|—— 写明收件人"},
            {"name": "坑 3:过长", "content": "AI 改得啰嗦|—— 给字数上限"},
        ],
        "cols": 3,
    }
}

FIGS["4.3.1-ppt-outline-7-pages"] = {
    "layout": "flow_h",
    "content": {
        "title": "PPT 大纲生成:7 步",
        "steps": [
            {"name": "准备素材", "detail": "报告 / 数据"},
            {"name": "新建任务", "detail": "PPT 大纲模板"},
            {"name": "指定页数", "detail": "15 页"},
            {"name": "AI 出大纲", "detail": "每页标题 + 要点"},
            {"name": "审阅调整", "detail": "结构是否合理"},
            {"name": "导出大纲", "detail": "Markdown / Word"},
            {"name": "填入 PPT 工具", "detail": "二次加工"},
        ]
    }
}

FIGS["4.4.1-meeting-minutes-template"] = {
    "layout": "grid",
    "content": {
        "title": "会议纪要 6 段式模板",
        "items": [
            {"name": "基本信息", "content": "时间 · 参会人"},
            {"name": "讨论要点", "content": "议题 + 各方观点"},
            {"name": "决策项", "content": "拍板的结论"},
            {"name": "行动项", "content": "谁 · 做什么 · 截止"},
            {"name": "下次议题", "content": "后续跟进"},
            {"name": "风险点", "content": "未解决的问题"},
        ],
        "cols": 3,
    }
}

FIGS["4.5.1-data-analysis-flow"] = {
    "layout": "flow_h",
    "content": {
        "title": "数据透视:5 步",
        "steps": [
            {"name": "上传 Excel", "detail": "右栏文件"},
            {"name": "说明维度", "content": "想看什么角度"},
            {"name": "AI 跑分析", "detail": "30 秒"},
            {"name": "生成图表", "detail": "PDF / PNG"},
            {"name": "写洞察", "detail": "3-5 段文字"},
        ]
    }
}

# ===== ch05: 多模型路由 (7 张) =====

FIGS["5.1.1-six-models-comparison"] = {
    "layout": "grid",
    "content": {
        "title": "6 款国产大模型能力对比",
        "items": [
            {"name": "DeepSeek", "content": "数据逻辑最强|价格最低"},
            {"name": "Kimi", "content": "200K 长文本|读 PDF 最强"},
            {"name": "智谱 GLM", "content": "中文写作|企业级强"},
            {"name": "通义千问", "content": "结构化输出|API 强"},
            {"name": "豆包", "content": "日常对话|自然"},
            {"name": "文心一言", "content": "稳定|中庸"},
        ],
        "cols": 3,
    }
}

FIGS["5.1.2-model-sweet-spots"] = {
    "layout": "compare",
    "content": {
        "title": "每款模型的甜点区",
        "left": {
            "title": "按任务选",
            "items": ["写中文正式邮件 → 智谱", "读 50 页 PDF → Kimi", "数据逻辑 → DeepSeek", "调工具 API → 通义千问"],
            "color": "#0F4C81"
        },
        "right": {
            "title": "按风格选",
            "items": ["头脑风暴 → 豆包", "日常查询 → 文心一言", "价格敏感 → DeepSeek"],
            "color": "#16A085"
        }
    }
}

FIGS["5.2.1-single-model-vs-routing"] = {
    "layout": "compare",
    "content": {
        "title": "单模型 AI vs 多模型路由",
        "left": {
            "title": "单模型(网页版)",
            "items": ["所有任务跑同一个模型", "DeepSeek 强项不在中文写作", "周报可能不佳", "你自己挑模型"],
            "color": "#D2691E"
        },
        "right": {
            "title": "多模型路由",
            "items": ["按任务自动选", "周报 → 智谱", "PDF 摘要 → Kimi", "你只提需求"],
            "color": "#16A085"
        }
    }
}

FIGS["5.2.2-routing-flow"] = {
    "layout": "flow_v",
    "content": {
        "title": "多模型路由的工作流",
        "steps": [
            {"name": "你提需求", "detail": "中文邮件润色"},
            {"name": "路由判断", "detail": "任务特征:中文写作"},
            {"name": "选最优模型", "detail": "智谱 GLM"},
            {"name": "调用 + 返回", "detail": "10 秒"},
            {"name": "展示结果", "detail": "你看到结果"},
        ]
    }
}

FIGS["5.3.1-four-dimensions-routing"] = {
    "layout": "grid",
    "content": {
        "title": "四维评分机制:任务路由",
        "items": [
            {"name": "任务类型", "content": "写作 / 阅读 / 逻辑 / 结构化"},
            {"name": "上下文长度", "content": "< 10K / 10K-100K / > 100K"},
            {"name": "质量要求", "content": "日常 / 正式 / 关键"},
            {"name": "成本预算", "content": "免费档 / 标准 / 重度"},
        ],
        "cols": 2,
    }
}

FIGS["5.4.1-manual-override"] = {
    "layout": "flow_h",
    "content": {
        "title": "手动覆盖路由:何时用",
        "steps": [
            {"name": "AI 路由结果不满意", "detail": "打开右栏'模型'"},
            {"name": "手动选另一个", "detail": "从下拉列表"},
            {"name": "重新生成", "detail": "⌘ R"},
            {"name": "对比选择", "detail": "保存满意版本"},
        ]
    }
}

FIGS["5.5.1-routing-preference"] = {
    "layout": "grid",
    "content": {
        "title": "路由偏好设置",
        "items": [
            {"name": "默认模型", "content": "日常任务默认谁"},
            {"name": "成本优先", "content": "同等质量选最便宜的"},
            {"name": "质量优先", "content": "不在意钱 · 要最好"},
            {"name": "速度优先", "content": "毫秒级响应"},
        ],
        "cols": 2,
    }
}

# ===== ch06: 提示词 (7 张) =====

FIGS["6.1.1-qa-vs-task-mindset"] = {
    "layout": "compare",
    "content": {
        "title": "从'问问题'到'派活'的思维转变",
        "left": {
            "title": "'问'的方式(60 分)",
            "items": ["'帮我写封邮件'", "'总结下这个 PDF'", "AI 不知道你要干嘛", "输出质量上限 60 分"],
            "color": "#D2691E"
        },
        "right": {
            "title": "'派活'的方式(90 分)",
            "items": ["角色 · 任务 · 约束 · 素材 · 输出", "5 个要素齐全", "AI 输出质量 90+ 分", "可复用 · 可量化"],
            "color": "#16A085"
        }
    }
}

FIGS["6.1.2-five-elements-prompt"] = {
    "layout": "grid",
    "content": {
        "title": "五段式提示词 5 要素",
        "items": [
            {"name": "角色", "content": "你是谁 · 什么身份"},
            {"name": "任务", "content": "动词开头 · 具体做什么"},
            {"name": "约束", "content": "长度 · 语气 · 风格"},
            {"name": "素材", "content": "哪些文件 · 哪些背景"},
            {"name": "输出", "content": "最终格式"},
        ],
        "cols": 5,
    }
}

FIGS["6.2.1-role-when-skip"] = {
    "layout": "compare",
    "content": {
        "title": "角色:何时写 / 何时省",
        "left": {
            "title": "推荐写",
            "items": ["复杂任务", "需要特定语气", "希望激活特定风格库"],
            "color": "#16A085"
        },
        "right": {
            "title": "可以省",
            "items": ["翻译等简单任务", "要中立输出", "不想 AI 偏向某种视角"],
            "color": "#D2691E"
        }
    }
}

FIGS["6.2.2-task-verb-table"] = {
    "layout": "grid",
    "content": {
        "title": "任务动词清单(动词开头)",
        "items": [
            {"name": "整理", "content": "把...组织为..."},
            {"name": "分析", "content": "从...中识别..."},
            {"name": "写", "content": "产出...文体"},
            {"name": "改", "content": "把 A 改成 B"},
            {"name": "对比", "content": "对比 X 和 Y"},
            {"name": "总结", "content": "提炼核心 3 点"},
        ],
        "cols": 3,
    }
}

FIGS["6.3.1-three-types-constraints"] = {
    "layout": "grid",
    "content": {
        "title": "约束的 3 类",
        "items": [
            {"name": "长度", "content": "字数 · 页数 · 行数"},
            {"name": "语气", "content": "正式 / 轻松 / 委婉"},
            {"name": "风格", "content": "参考谁 · 避免什么"},
        ],
        "cols": 3,
    }
}

FIGS["6.4.1-materials-providing"] = {
    "layout": "compare",
    "content": {
        "title": "素材:给 AI 多少背景",
        "left": {
            "title": "给得太多",
            "items": ["复制整篇文档", "AI 跑得慢", "Token 成本翻倍"],
            "color": "#D2691E"
        },
        "right": {
            "title": "给得刚好",
            "items": ["只给关键段落", "AI 抓得准", "成本最低"],
            "color": "#16A085"
        }
    }
}

FIGS["6.5.1-output-format-5-types"] = {
    "layout": "grid",
    "content": {
        "title": "输出格式 5 类(让 AI 知道你要什么)",
        "items": [
            {"name": "Markdown", "content": "标准结构化"},
            {"name": "表格", "content": "对比型"},
            {"name": "JSON", "content": "程序可读"},
            {"name": "代码块", "content": "技术内容"},
            {"name": "列表", "content": "要点型"},
        ],
        "cols": 3,
    }
}

# ===== ch07: Credits 与成本 (5 张) =====

FIGS["7.1.1-pricing-model"] = {
    "layout": "compare",
    "content": {
        "title": "订阅费 + 积分双重计费",
        "left": {
            "title": "订阅费",
            "items": ["固定月费", "给'使用权'", "4 档可选", "类比:月租"],
            "color": "#0F4C81"
        },
        "right": {
            "title": "积分(Credit)",
            "items": ["按使用量消耗", "给'算力'", "1 Credit ≈ 1 token", "类比:流量"],
            "color": "#16A085"
        }
    }
}

FIGS["7.1.2-four-tiers"] = {
    "layout": "grid",
    "content": {
        "title": "4 档订阅对比",
        "items": [
            {"name": "个人版", "content": "免费 · 5 万 积分/月"},
            {"name": "Pro 版", "content": "中层管理者 · 50 万 积分/月"},
            {"name": "Ultra 版", "content": "重度用户 · 200 万 积分/月"},
            {"name": "团队版", "content": "5-7 人共享 · 350 万 积分/月"},
            {"name": "企业版", "content": "议价 · 50+ 人 · SSO"},
        ],
        "cols": 3,
    }
}

FIGS["7.2.1-credits-consumption-vars"] = {
    "layout": "grid",
    "content": {
        "title": "积分消耗的 4 个变量",
        "items": [
            {"name": "输入长度", "content": "AI 读的文件越多 · 越多"},
            {"name": "输出长度", "content": "AI 写的内容越多 · 越多"},
            {"name": "模型档位", "content": "旗舰档(贵) vs 入门档(便宜)"},
            {"name": "是否缓存命中", "content": "重复读免费(Kimi)"},
        ],
        "cols": 2,
    }
}

FIGS["7.3.1-five-saving-tips"] = {
    "layout": "grid",
    "content": {
        "title": "5 个省积分的技巧",
        "items": [
            {"name": "① 选对模型", "content": "日常用便宜档"},
            {"name": "② 缓存复用", "content": "重复读命中免费"},
            {"name": "③ 提示词精简", "content": "少废话 · 命中要点"},
            {"name": "④ 限速提交", "content": "避免重生成 5 次"},
            {"name": "⑤ 任务合并", "content": "1 个长任务 vs 5 个短"},
        ],
        "cols": 3,
    }
}

FIGS["7.4.1-dashboard-layout"] = {
    "layout": "grid",
    "content": {
        "title": "积分消耗仪表盘 4 个视图",
        "items": [
            {"name": "顶部条", "content": "实时余额(绿/黄/红)"},
            {"name": "左栏底部", "content": "详细余额 + 趋势"},
            {"name": "中栏顶部", "content": "当前任务消耗"},
            {"name": "右栏'工具'", "content": "本月消耗进度"},
        ],
        "cols": 2,
    }
}

# ===== ch08: 从个人到团队 (6 张) =====

FIGS["8.1.1-personal-vs-team"] = {
    "layout": "compare",
    "content": {
        "title": "个人用好 vs 团队用好的根本差异",
        "left": {
            "title": "个人用好(本卷目标)",
            "items": ["独立完成周报/邮件/PPT", "省 5-10h/周", "仍是个人贡献"],
            "color": "#0F4C81"
        },
        "right": {
            "title": "团队用好(第二卷)",
            "items": ["5-10 人集体放大", "省 50-100h/周", "沉淀团队资产"],
            "color": "#16A085"
        }
    }
}

FIGS["8.2.1-four-things-team-intro"] = {
    "layout": "grid",
    "content": {
        "title": "团队引入 WorkBuddy 的 4 件事",
        "items": [
            {"name": "① 示范", "content": "领导公开使用|展示真实场景"},
            {"name": "② 培训", "content": "8 章内容压缩为 2 天|让团队会用且用得专业"},
            {"name": "③ 流程", "content": "把 AI 使用嵌入|日常工作流"},
            {"name": "④ 文化", "content": "允许尝试 · 容忍失败|不是命令而是示范"},
        ],
        "cols": 2,
    }
}

FIGS["8.3.1-three-resistance-types"] = {
    "layout": "grid",
    "content": {
        "title": "团队可能遇到的 3 类典型阻力",
        "items": [
            {"name": "技术阻力", "content": "不会用 · 学不动|—— 一对一辅导"},
            {"name": "心理阻力", "content": "怕被替代 · 怕显笨|—— 强调'AI 帮你不替你'"},
            {"name": "流程阻力", "content": "原有流程冲突|—— 重设计而非叠加"},
        ],
        "cols": 3,
    }
}

FIGS["8.3.2-resistance-strategies"] = {
    "layout": "compare",
    "content": {
        "title": "应对阻力的策略",
        "left": {
            "title": "硬推(失败)",
            "items": ["领导命令式推广", "团队表面服从实际不用", "3 个月后回到原点"],
            "color": "#D2691E"
        },
        "right": {
            "title": "软推(成功)",
            "items": ["示范 + 培训 + 流程", "团队看到真实价值", "自发传播"],
            "color": "#16A085"
        }
    }
}

FIGS["8.4.1-vol2-preview"] = {
    "layout": "grid",
    "content": {
        "title": "第二卷预告(团队到组织)",
        "items": [
            {"name": "团队落地三阶段", "content": "试点 · 推广 · 沉淀"},
            {"name": "企业微信集成", "content": "飞书 · 钉钉 · 协作"},
            {"name": "团队工作目录", "content": "公共区 · 个人区 · 项目区"},
            {"name": "技能市场", "content": "选现成的 Skill"},
            {"name": "专家中心", "content": "沉淀团队最佳实践"},
            {"name": "30 天培训", "content": "从 0 到全员"},
            {"name": "成本与权限", "content": "积分 怎么分"},
        ],
        "cols": 3,
    }
}

FIGS["8.4.2-checklist-trigger-readiness"] = {
    "layout": "timeline",
    "content": {
        "title": "读第二卷前的准备清单",
        "steps": [
            {"name": "D1", "detail": "个人用满 2 周"},
            {"name": "D2", "detail": "整理 5 个真实场景"},
            {"name": "D3", "detail": "识别 3 个阻力点"},
            {"name": "D4", "detail": "准备团队预算"},
            {"name": "D5", "detail": "开始第二卷"},
        ]
    }
}


def main():
    print(f"Total figures: {len(FIGS)}")
    for name, spec in FIGS.items():
        try:
            svg = render_figure(name, spec["layout"], spec["content"])
            path = save(OUT_DIR, name, svg)
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
            raise

if __name__ == "__main__":
    main()