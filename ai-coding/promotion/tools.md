# 工具清单

> 本表收录全书提到的工具,按"模型 / IDE 与脚手架 / 数据获取 / 运营与协作"四类分组。"首次出现章节"标注该工具在原书首次被讨论的位置,便于读者回溯上下文。价格、版本、能力描述均以 2026 年 7 月 31 日数据截止为基准;后续版本变化不在本表覆盖范围。

## 一、模型

| 工具名 | 类别 | 用途 | 首次出现章节 |
|--------|------|------|--------------|
| Claude Opus 5 | 模型 | Anthropic 旗舰模型,$5/$25,1M 上下文,Claude Code 默认模型 | 第 1 章 |
| Claude Sonnet 5 | 模型 | Anthropic 中档模型,$3/$15,承担主力日常任务 | 第 1 章 |
| Claude Haiku 4.5 | 模型 | Anthropic 入门档,$1/$5,高频轻量后台任务 | 第 1 章 |
| Claude Fable 5 | 模型 | Anthropic 顶级档,$10/$50,2026-06 被出口管制暂停,7-01 恢复 | 第 1 章 |
| GPT-5.6 Sol | 模型 | OpenAI 旗舰档,$5/$30,对标 Claude Opus 5 | 第 1 章 |
| GPT-5.6 Terra | 模型 | OpenAI 中档,$2.50/$15,对标 Claude Sonnet 5 | 第 1 章 |
| GPT-5.6 Luna | 模型 | OpenAI 入门档,$1/$6,对标 Claude Haiku 4.5 | 第 1 章 |
| Codex(GPT-5.6 配套) | 模型/Agent | OpenAI 编程 Agent,命令行/编辑器/网页/桌面四种用法 | 第 1 章 |
| GLM-5.2(智谱) | 模型 | 智谱主力,模型开源,API 价约 Opus 5 的 1/5.7 | 第 1 章 |
| K3(Kimi) | 模型 | 月之暗面 2.8T 总参数开源模型,1M 上下文,按 Token 计量+缓存命中不计额度 | 第 1 章 |
| M3(MiniMax) | 模型 | 428B/23B 激活开源模型,1M 保底 512K,全模态额度池 | 第 1 章 |
| DeepSeek V4-Flash | 模型 | 成本地板,$0.14/$0.28,1M 上下文,作为后台批量任务默认后端 | 第 1 章 |
| DeepSeek V4-Pro | 模型 | 1.6T 总参数预览版,2026-04-24 发布,旧 API 名 07-24 退役 | 第 1 章 |
| Gemini 3.1 Pro | 模型 | 1M 上下文窗口,超大代码库通读场景的常用路由 | 第 15 章 |
| Qwen / Llama | 模型 | Chroma Context Rot 研究的覆盖系列,18 模型无一幸免退化 | 第 13 章 |

## 二、IDE 与脚手架

| 工具名 | 类别 | 用途 | 首次出现章节 |
|--------|------|------|--------------|
| Claude Code | IDE / Agent | Anthropic 命令行 Agent,hooks/skills/子代理最全的工程结构 | 第 1 章 |
| Cursor | IDE | 主流 AI IDE,Composer 2 基于 Kimi K2.5 RL 训练 | 第 1 章 |
| Codex CLI | IDE / Agent | OpenAI 的命令行编程 Agent,Apache-2.0 开源 | 第 1 章 |
| Z Code 3.0(智谱) | IDE | 智谱编程 IDE,改用自家核心模块,Claude Code 改两行配置可接入 | 第 1 章 |
| Kimi Code | IDE | 月之暗面编程 IDE,Apache-2.0 开源 | 第 1 章 |
| MiniMax Code | IDE | MiniMax 编程 IDE,Agent Team 多智能体,可接入微信/飞书/Telegram | 第 1 章 |
| GitHub Copilot | IDE | AI 代码补全,GitClear 报告研究对象之一 | 第 13 章 |
| OpenClaw | IDE / Agent | 38.4 万 stars 的开源 Agent 接入框架,Gateway–Node–Host 三层架构 | 第 6 章 |
| Kimi Claw Beta | IDE / Agent | 月之暗面提供的 OpenClaw 云托管产品,2026-02-16 上线 | 第 6 章 |
| OpenSpec(Fission-AI) | 脚手架 | 轻量 SDD 工具,/opsx 命令驱动 proposal/specs/design/tasks 四件套 | 第 15 章 |
| superpowers(obra) | 脚手架 | 14 个 Markdown skill + 加载器,强制 TDD/调试/评审工作流,25 万+ stars | 第 15 章 |
| github/spec-kit | 脚手架 | GitHub 官方 SDD 工具包,刚性阶段门的重流水线 | 第 15 章 |
| AWS Kiro | 脚手架 | AWS agentic IDE,SDD 固化为默认工作流,EARS 记法 | 第 15 章 |
| AGENTS.md | 脚手架 | Linux 基金会托管的开放标准,6 万+ 仓库采用,记录项目背景与约束 | 第 15 章 |
| CLAUDE.md | 脚手架 | Claude Code 项目级记忆文件,与 Auto Memory 构成双记忆 | 第 8 章 |
| FastMCP(jlowin) | 脚手架 | Python 社区事实标准 MCP 服务端框架,装饰器注册工具 | 第 14 章 |
| Playwright | 脚手架 | 浏览器自动化,Stagehand 底层驱动,登录态 .auth/state 序列化 | 第 3 章 |
| Stagehand | 脚手架 | 浏览器自动化,act/extract/observe/agent 四原语,v3 提速 44% | 第 3 章 |
| Browser Use | 脚手架 | AI 浏览器 Agent,WebVoyager 89.1% SOTA,sensitive_data 占位符 | 第 3 章 |
| Open-AutoGLM(zai-org) | 脚手架 | 开源侧"请求人工接管(登录/验证码等)"动作设计 | 第 3 章 |
| Dify / Coze / RAGflow | 脚手架 | 数据流横评对象,n8n 400+ 集成,fair-code 商用注意事项 | 第 6 章 |
| n8n | 脚手架 | 400+ 集成的可自托管自动化平台 | 第 6 章 |
| 飞书 aily | 脚手架 | 飞书原生 Agent 办公平台,云端持续工作与三方 Agent 接入 | 第 6 章 |

## 三、数据获取

| 工具名 | 类别 | 用途 | 首次出现章节 |
|--------|------|------|--------------|
| Firecrawl | 数据 | 托管 API 型爬虫,1 页 1 credit,stealth 5 倍价,Map 先行省钱 | 第 2 章 |
| Crawl4AI | 数据 | 开源 Python 爬虫库,零密钥,CLI/Docker 部署,50,000+ stars | 第 14 章 |
| Jina Reader | 数据 | 极简前缀型,`r.jina.ai/网址`返回 Markdown,约 $0.05/1M Token | 第 14 章 |
| Bright Data | 数据 | 企业反爬型,3M+ 解锁域名,MCP 月 5,000 次免费,Markdown 默认输出 | 第 14 章 |
| Apify | 数据 | 无代码市场型,7,000+ Actor 预置抓取小程序,$5 免费额度起 | 第 14 章 |
| Scrapy | 数据 | 稳定 HTML 站点高产量生产首选,BSD-3-Clause | 第 14 章 |
| ScrapeGraphAI | 数据 | MIT 许可,28.2k stars,自然语言描述抓取,底层 Playwright | 第 14 章 |
| Spider.cloud | 数据 | 利益相关方的竞品基准测试,RAG recall@5 91.5% 自我宣称 | 第 14 章 |
| Tavily | 数据 | Agent 优化搜索+提取一体,$7.5—8/1k,免费 1,000 次/月,2026-02 被 Nebius 收购 | 第 7 章 |
| Exa | 数据 | 神经语义搜索,$7/1k,免费 20,000 次/月,偏深度内容 | 第 7 章 |
| Brave Search API | 数据 | Bing API 关停后唯一大型独立索引,2026-02 取消免费计划改送 $5 额度 | 第 7 章 |
| Perplexity Sonar | 数据 | 检索+生成+引用打包进 token 价,一口价 $1/$1 起 | 第 7 章 |
| SingleFile | 数据 | 浏览器扩展,把整个网页存成单个 HTML,作证据级快照存档 | 第 2 章 |
| Wappalyzer | 数据 | 技术栈指纹识别,HTTP 响应头/JS 全局变量/DOM 特征 | 第 2 章 |
| Visualping | 数据 | 轻量网页变更监控,Business 档 $100/月起含 20,000 次检查/200 页 | 第 12 章 |
| Distill.io / Wachete / Hexowatch | 数据 | 轻量网页监控工具,云端付费 $4.9—$29/月起 | 第 12 章 |
| Chroma | 数据 | Context Rot 研究的主体,18 模型无一幸免退化,有效上下文≈标称 25—30% | 第 13 章 |
| gitclear | 数据 | Coding on Copilot 系列报告,2.11 亿行变更代码分析 | 第 13 章 |
| Mem0 | 数据 | Claude API 价格指南的整理方,Web search $10/1,000 次独立计费 | 第 14 章 |
| Cloudflare AI Labyrinth | 数据 | 2025—2026 默认拦截 AI 爬虫,假页面迷宫污染抓取结果 | 第 2 章 |

## 四、运营与协作

| 工具名 | 类别 | 用途 | 首次出现章节 |
|--------|------|------|--------------|
| 飞书(Lark) | 协作 | 国内 IM/审批/存储一体化,AI 锁屏触达率高于企微约 30% | 第 6 章 |
| 飞书多维表格(Bitable) | 协作 | tenant_access_token 鉴权,app_token/table_id 读记录接口 | 第 5 章 |
| 飞书 aily | 协作 | 飞书原生 Agent 办公平台 | 第 6 章 |
| 微信支付 | 运营 | 国内收款,小微商户 0.38%—0.6%,T+1 自动提现,仅 JSAPI/Native/付款码 | 第 10 章 |
| 支付宝 | 运营 | 国内收款,电脑网站支付 0.60%,企业/个体工商户可申请 | 第 10 章 |
| Stripe | 运营 | 国际收款,在线卡 2.9% + $0.30,国际卡 +1.5%,webhook 验签硬性要求 | 第 10 章 |
| Stripe Atlas | 运营 | 海外主体代办,$500 一次性注册特拉华 C-Corp/LLC,首年含注册代理 | 第 10 章 |
| Lemon Squeezy | 运营 | MoR 收款代理商,5% + 50¢,2024 年被 Stripe 收购,payout 约每月两次 | 第 10 章 |
| Paddle | 运营 | MoR 收款代理商,5% + 50¢ 全包,非本币结算另有货币费 | 第 10 章 |
| Clerk / Supabase Auth | 运营 | 托管登录选型,免费 50K MAU,Pro $25/月;2026-02 Clerk 由 10K 升至 50K | 第 10 章 |
| GitClear | 运营 | AI 时代代码质量系列报告,2.11 亿行变更分析 | 第 13 章 |
| Readhub | 运营 | 行业监管通报时间线追踪 | 第 6 章 |
| 新华社 CNCERT | 运营 | 提示词注入/误删数据/插件投毒/漏洞四类风险提示 | 第 6 章 |
| arXiv | 学术 | 本书 202+ 引用中的一手研究主要来源(论文 2605.23950、2603.28592、2603.22106 等) | 全文 |
| Vals AI | 数据 | SWE-bench Verified 榜单,第三方复测 Opus 5 97%、Sol 96.2% | 第 1 章 |
| Morph | 数据 | SWE-bench Pro 榜单,Scale SEAL 标准化 harness 榜首 GPT-5.4 59.1% | 第 1 章 |
| METR | 学术 | RCT 研究:慢 19% 自认快 20%,长程能力估值 11.3h—270h 不可采信 | 第 1 章 |

> 工具使用建议:选型时先回答"团队是否具备维护基础设施的人力"——有,选自托管;无,选托管 API;有受保护站点,选企业反爬;无工程团队,选无代码市场。任何选型都不是"找最优",而是"找在交付期内能稳的"。
