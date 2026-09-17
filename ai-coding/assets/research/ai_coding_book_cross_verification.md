# 《AI编程实战》调研 — 交叉验证报告（Phase 4）
验证日期：2026-07-31 ｜ 验证人：Orchestrator ｜ 输入：dim01–dim12 共 12 份维度报告（约 430 条证据）

## 一、置信度分级总览

### High Confidence（≥2 个独立信源 + 含一手来源，可直入正文）
| # | 事实 | 证据维度 |
|---|------|----------|
| H1 | OpenClaw 真实存在：Peter Steinberger 2025-11 发起（Clawdbot→Moltbot→OpenClaw），MIT 协议，GitHub 384.7k stars（2026-07-31 实测），Gateway–Node–Host 架构，飞书 channel 官方支持 | dim10（GitHub 一手 + 钛媒体 + arXiv） |
| H2 | Kimi Claw = 月之暗面基于 OpenClaw 的云托管产品（2026-02-16 上线）；腾讯 QClaw、智谱 AutoClaw、MiniMax MaxClaw、字节 ArkClaw 均为同类封装 | dim04、dim10 交叉 |
| H3 | OpenSpec = Fission-AI 的 SDD 框架（约 5.5 万 stars，2026-06）；superpowers = Jesse Vincent(obra) 的 agent 技能框架（2026-07 超 25 万 stars）；两者互补（计划工件 vs 执行习惯） | dim12（README 一手 + 多源时间线） |
| H4 | Kimi K3 已发布：2026-07-16 发布、07-27 开源，2.8T 参数/896 专家激活 16，1M 上下文 | dim04（官方博客 + IT之家 + 贝壳财经） |
| H5 | MiniMax M3 已发布：2026-06-01（开源 06-12），约 428B/23B 激活，1M 上下文（保底 512K） | dim05（官方 release notes + 百度百科 + 实测） |
| H6 | GLM-5.2：2026-06-13/16，753B MoE，1M 上下文，MIT 开源；GLM-5（02-12）全程昇腾 910B 训练 | dim03（官方 + 多源） |
| H7 | GPT-5.4（03-05）/ 5.5（04-23）/ 5.6（06-26 预览、07-09 GA，Sol/Terra/Luna 三档） | dim02（developers.openai.com 一手） |
| H8 | Claude 家族：Haiku 4.5 / Sonnet 5（06-30）/ Opus 5（07-24）/ Fable 5；Claude Code v2.1.220，Dynamic Workflows、30+ hooks、skills、嵌套 subagent | dim01（Anthropic 官方 + changelog） |
| H9 | 国内 Coding Plan 格局：智谱 GLM（客户端兼容最广 20+、4 个专属 MCP）、火山方舟（唯一原生 Anthropic 协议）、MiniMax、Kimi（Token 计量）、百炼（2026 改版后仅 Pro） | dim03、04、05、07 交叉 |
| H10 | 网站复刻四段式工作流（侦察→蒸馏→重建→量化验收）与 AI 分析代码幻觉铁律（marbles 案例） | dim08（GitHub skill 一手） |
| H11 | 登录态 SaaS 复刻：80/20 混合架构（Playwright 固化 + Browser Use 推理）、sensitive_data 凭据隔离、人工接管节点、写操作不可逆需幂等+审计 | dim09（官方文档 + 实战） |
| H12 | AI 爬虫工具分层：Firecrawl（托管）、Crawl4AI（开源自托管）、Jina Reader（前缀极简）、Bright Data（企业反爬）、Apify（无代码市场）；MCP 为标准接法 | dim11（官方文档 + 定价页） |

### Medium Confidence（单一权威来源或厂商自报，引用时必须带限定语）
- M1：各家 SWE-bench Pro/Verified 分数——**全部为厂商自报**（Opus 5 79.2%、Fable 5 80.0/80.3%、GLM-5.2 62.1、M3 59.0、GPT-5.6 Sol Terminal-Bench 88.8%）；正文引用必须标注"厂商自报+日期"。（dim01–07 一致警示）
- M2：Kimi K3 第三方锚点（Frontend Code Arena 1679 Elo、AA 指数 57）——第三方但单源。（dim04）
- M3：OpenClaw 月活 320 万、实例 50 万（2026-04，钛媒体单源报道）。（dim10）
- M4：Z Code 3.0（2026-06-13）切自研内核、放弃第三方 Agent 适配。（dim03，官方发布+单源解读）
- M5：Cursor Composer 2 基于 K2.5 RL 训练（"马斯克认证"属社区谈资，可作趣闻不作论断）。（dim04）
- M6：竞品发布的爬虫基准（Spider 91.5% > Firecrawl 89% > Crawl4AI 84.5%）——利益相关方发布，引用须注明。（dim11）

### Low Confidence（弱来源，仅作背景或弃用）
- L1："OpenClaw 是 Rust 无代码测试工具"——内容农场伪信息（含未渲染占位符），**已判定不采信**。（dim10）
- L2：部分中文合规文章的案号细节，出版前需裁判文书网复核。（dim11）

## 二、冲突区（Conflict Zone）与处置

| # | 冲突项 | 各方说法 | 处置结论 |
|---|--------|----------|----------|
| C1 | Claude Code 默认模型/版本时点 | 6 月资料：Opus 4.8 默认、SWE-bench Pro 69.2（厂商自报）；dim01：Opus 5（07-24 发布）接任默认、Pro 79.2 | **时间性冲突，非矛盾**。书中一律写"截至 2026 年 7 月底：Opus 5"，并注明此前为 4.8。第一章必须给全书一个"数据截止 2026-07-31"的声明。 |
| C2 | Fable 5 SWE-bench Pro | 80.0%（morphllm 转官方） vs 80.3%（dim02 引第三方榜单转述） | 数值口径差（四舍五入/榜单版本）。统一写"约 80%（厂商自报，2026-07）"。 |
| C3 | DeepSeek 估值 | 虎嗅（2026-04）：首轮融资洽谈、估值 100 亿美元；dim06：二轮投前 710 亿美元 | **不同轮次不同时点**，两个数字都可引用但必须各带日期。 |
| C4 | DeepSeek "幻觉率 94–96%" | dim06 列为坑点 | **存疑标记**：该数字大概率出自特定测试（特定模型版本/特定 QA 集），脱离语境引用会误导。书中若引用必须写清测试集、模型版本与日期；无法确认语境则降级为"幻觉控制是 DeepSeek 已知弱项（社区共识）"。写作阶段引用前需回查 dim06 原文条目。 |
| C5 | "Kimi 是唯一不限 5 小时窗口的 Coding Plan" | 1–4 月资料：成立；dim04：最迟 6 月起已引入 5 小时+周双层限额（官方帮助页 7-29） | **已过时**。以官方帮助页（2026-07-29）为准，Kimi 真差异是 Token 计量+缓存命中不计额度。 |
| C6 | MiniMax "¥29 Starter/每5小时40次" | 2–3 月资料：在售；dim05：6 月起停售、改 token 计费 | **已过时**。写作时用 Token Plan 现状，¥29 作为"价格战史"叙述。 |
| C7 | "GLM-5.2 击败 Claude" | 中文自媒体流传；dim03 纠偏：官方图 Opus 4.8（69.2）> GLM-5.2（62.1），GLM-5.2 赢的是 GPT-5.5 与 Gemini 3.1 Pro | **误传，书中主动纠偏**（可作"如何读厂商战报"的教学点）。 |
| C8 | Scale SEAL 榜首 61.5%（Muse Spark 1.1） | morphllm（2026-07-24）；dim07 未核到当期快照（6 月口径为 GPT-5.4 59.1%） | **未解决，低优先级**：出版前查 labs.scale.com 当期值；大纲与初稿中先写"SEAL 标准化榜首在 60 分上下（2026 年中）"。 |
| C9 | GLM-5.1 发布日期 | 官方 04-08 vs 媒体 04-09 | 以官方 04-08 为准。 |
| C10 | MiniMax M3 发布日期 | 官方 06-01 vs 部分媒体 05-31 | 以官方 06-01 为准。 |
| C11 | Claude Code 上下文窗口 | 部分横评写 200K；dim01：Opus 4.7 起支持 1M | **档位门控差异**：1M 为特定档/开关能力，默认 200K。书中写"标称 200K，可开 1M（>200K 触发压缩）"。 |

## 三、给写作阶段的硬性纪律（所有章节必须遵守）
1. **时效声明**：全书数据截止 2026-07-31；每个价格/版本号/跑分尽量带"截至 YYYY-MM"。
2. **跑分三层标注**：厂商自报（自建基准）/ 厂商自报（外部基准）/ 第三方独立 harness——正文优先用第三方。
3. **禁采清单**：内容农场伪信息（L1）、无语境的 DeepSeek 幻觉率数字（C4）、"GLM-5.2 击败 Claude"（C7）。
4. **法律内容**（复刻、爬虫、登录态）只引用 dim08/09/11 中的判例与法条，不发挥。
