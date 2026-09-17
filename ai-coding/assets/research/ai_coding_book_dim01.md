# 维度01 调研报告：Claude Code 与 Anthropic Claude 模型家族现状（截至 2026-07-31）

调研说明：本报告基于 30+ 次独立检索（中英混合 query），优先采用 Anthropic 官网/官方文档（anthropic.com、code.claude.com、GitHub anthropics/claude-code），辅以权威媒体（TechCrunch、Bloomberg、VentureBeat、Axios 的转述）、第三方基准站点（vals.ai、BenchLM、Artificial Analysis 转引）与开发者社区（Hacker News 讨论）。基准数字已标注"厂商自报（system card/发布页）"与"第三方 harness"的区别。检索时间：2026-07-31。

---

## 一、模型家族现状与发布时间线（2026 年）

### 1.1 Claude Opus 5 —— 当前旗舰主力（2026-07-24 发布）

Claim: Anthropic 于 2026 年 7 月 24 日发布 Claude Opus 5（API ID `claude-opus-5`），定价与 Opus 4.8 持平（$5/百万输入 token、$25/百万输出 token），1M token 上下文窗口（默认即最大），128K 最大输出（Batch API beta 下 300K），定位"接近 Fable 5 前沿智能、价格减半"，并成为 Claude Max 默认模型、Claude Pro 可用最强模型。[^1^][^2^][^3^]
Source: Anthropic 官方发布页《Introducing Claude Opus 5》
URL: https://www.anthropic.com/news/claude-opus-5
Date: 2026-07-24
Excerpt: "Claude Opus 5 is available today. It's a thoughtful and proactive model that comes close to the frontier intelligence of Claude Fable 5 at half the price. … It's the new default model on Claude Max, and the strongest model on Claude Pro."
Context: 官方一手来源。Opus 5 是 Anthropic 不到两个月内发布的第四款 Claude 5 系列模型（此前为 Mythos 5、Fable 5、Sonnet 5）。
Confidence: high

Claim: Opus 5 官方基准（system card）：SWE-bench Verified 96.0%、SWE-bench Pro 79.2%（Opus 4.8 为 69.2%，Fable 5 为 80.0%）、SWE-bench Multilingual 89.5%、SWE-bench Multimodal 59.4%、Frontier-Bench v0.1 43.3%（vs Fable 5 33.7%、GPT-5.6 Sol 34.4%）、ARC-AGI-3 30.2%、OSWorld 2.0 70.6%、GDPval-AA v2 Elo 1,861。2026 IMO 六道证明题全对 42/42（金牌线 29/42）。[^2^][^4^][^5^]
Source: tryfriday.ai（仅引用 Anthropic 官方 system card 与发布页数据）
URL: https://www.tryfriday.ai/blog/anthropic-launches-claude-opus-5
Date: 2026-07-24
Excerpt: "Per Anthropic's system card: 96.0% on SWE-bench Verified, 79.2% on SWE-bench Pro, 89.5% on SWE-bench Multilingual, and 59.4% on SWE-bench Multimodal. … Opus 5 scored 42/42 on the 2026 International Mathematical Olympiad, with no agent harness or tools, judged by a three-model panel requiring unanimous agreement and corroborated by human expert grading."
Context: 全部为厂商自报（Anthropic system card）。注意 Frontier-Bench 官方图表脚注承认："These results are from an internal run of Frontier-Bench v0.1, on the mini-SWE-agent harness and a GKE backend, mean reward over 5 attempts per task. Opus 4.8 served as fallback on safety-classifier refusals for Opus 5 and Fable 5." —— 即部分拒答样本由 4.8 兜底完成。
Confidence: high（数字转录准确）；medium（基准本身为厂商内部 harness）

Claim: Opus 5 引入五档 effort 梯级（low / medium / high / xhigh / max），默认 high，adaptive thinking 默认开启；新增 Fast mode 研究预览（约 2.5× 输出速度，$10/$50，仅一方 Claude API）；存在两项破坏性 API 变更。[^6^][^7^]
Source: OpenRouter 官方迁移指南；apidog
URL: https://openrouter.ai/docs/cookbook/evaluate-and-optimize/model-migrations/opus-5 ; https://apidog.com/blog/claude-opus-5-effort-parameter/
Date: 2026-07-24 / 2026-07-25
Excerpt: "Reasoning is on by default — a first for Opus-family models … Disabling reasoning is restricted by effort level — allowed at `high` or lower; `xhigh` and `max` require reasoning to stay on … Combining disabled reasoning with `xhigh` or `max` effort returns a 400 from Anthropic."
Context: 破坏性变更①：不发 `thinking` 字段的请求在 Opus 5 上会默认思考，max_tokens 现覆盖思考+回复文本，未调整的调用会被静默截断（stop_reason: "max_tokens"，HTTP 200 无报错）；②`thinking: disabled` 仅在 effort ≤ high 时接受。Anthropic 还提示：Opus 5 会自发验证自己的工作，迁移后应删除提示词中的"自我验证"类指令（否则重复验证），且其更主动委派 subagent，建议显式限制委派。
Confidence: high

### 1.2 Claude Fable 5 / Mythos 5 —— 前沿 Mythos 级（2026-06-09 发布，曾遭出口管制暂停）

Claim: Claude Fable 5 于 2026 年 6 月 9 日发布，是 Anthropic 首个公开的 "Mythos-class"（位于 Opus 之上的新档位）模型，$10/$50 每百万 token，1M 上下文、128K 输出，SWE-bench Verified 95.0%、SWE-bench Pro 80.0%/80.3%（厂商自报）；采用常开 adaptive thinking；配备安全分类器，少量敏感请求（<5% 会话）静默回退到 Opus 4.8。[^8^][^9^][^10^]
Source: sevensolvers；distk.in；convly.ai
URL: https://www.sevensolvers.com/blog/anthropics-most-powerful-ai-models-explained-2026 ; https://distk.in/blog/claude-fable-5-mythos-5-marketing-guide-2026.html
Date: 2026-06-10 / 2026-06-15
Excerpt: "Pricing: $10 per million input tokens / $50 per million output tokens … Context window: 1 million tokens … Fable 5 is what your marketing team uses, Mythos 5 is what vetted cyberdefense and biomedical partners use under stricter controls. … more than 95 percent of Fable 5 sessions involve no fallback at all"
Context: Fable 5 与 Mythos 5 为同一底层模型：Fable 5 保留全部三层安全分类器面向公众 GA；Mythos 5 在特定领域解除防护，仅经 Project Glasswing 等可信渠道提供。Fable 5 附带强制 30 天数据保留政策（Opus 5 不受此限）。
Confidence: high

Claim: 2026 年 6 月 12 日，Anthropic 收到美国政府出口管制指令，全球暂停 Fable 5 与 Mythos 5 访问；7 月 1 日在加强安全分类器后重新部署。这是商用前沿模型首次被此类方式召回。[^11^][^12^]
Source: linkedotter；datanorth.ai
URL: https://linkedotter.com/articles/what-anthropic-export-ban-means-for-b2b-ai-buyers-june-2026 ; https://datanorth.ai/blog/top-10-ai-tools-for-2026
Date: 2026-07-01 / 2026-07-29
Excerpt: "Anthropic announced on June 12, 2026 that it had disabled access to Claude Fable 5 and Claude Mythos 5 for all customers, following receipt of a US government export control directive. … Three days later a US government export-control directive suspended both globally, the first time a commercially deployed frontier model has been pulled that way. Both were redeployed from 1 July with new safety classifiers."
Context: 直接诱因是 Mythos 级模型的网络安全能力（自主发现并利用零日漏洞）。写作意义：这是"模型即受管制物"的标志性事件，适合作为第一章行业格局素材。
Confidence: high

### 1.3 Claude Sonnet 5 —— 走量中坚（2026-06-30 发布）

Claim: Claude Sonnet 5 于 2026 年 6 月 30 日发布（Sonnet 4.8 被跳过），发布即成为 claude.ai 免费档与 Pro 档默认模型，也是 Claude Code Pro 默认模型；1M 上下文、128K 最大输出；导入期定价 $2/$10（至 2026-08-31），之后恢复 $3/$15。[^13^][^14^][^15^]
Source: cosmicjs（转引官方公告）；layer3labs；claudecode.xyz
URL: https://www.cosmicjs.com/blog/claude-sonnet-5-benchmarks-pricing-developers ; https://www.layer3labs.io/comparisons/kimi-k3-vs-claude-sonnet-5
Date: 2026-06-30 / 2026-07-22
Excerpt: "Sonnet 5 is the new default model for Free and Pro plans, and is also available on Max, Team, Enterprise, Claude Code, and the Claude API. … Claude Sonnet 5 uses introductory API pricing of $2 input and $10 output per million tokens through August 31, 2026, moving to $3 and $15 from September 1, 2026."
Context: 官方定位 "the most agentic Sonnet yet"。注意：Sonnet 5 的 SWE-bench Verified 分数各来源差异极大（cosmicjs 转官方为 72.7%，apiyi 为 85.2%，oflight 为 92.4%），应视为不同 harness/设定下的结果；system card 口径较一致的数字是 SWE-bench Pro 63.2%（Opus 4.8 为 69.2%）、Terminal-Bench 2.1 80.4%、GDPval-AA v2 Elo 1618（略超 Opus 4.8 的 1615，为首个在任一基准上反超同代 Opus 的 Sonnet）。写书时建议只引用 system card 口径并注明 harness 差异。
Confidence: high（发布与定价）；medium（Verified 具体分数存在来源分歧）

Claim: Sonnet 5 采用新 tokenizer，同样输入文本产生的 token 数约为 1.0–1.35×，迁移时需按实际成本而非标价估算。[^13^]
Source: oflight.co.jp
URL: https://www.oflight.co.jp/en/columns/claude-sonnet-5-anthropic-release-2026-06-30
Date: 2026-07-01
Excerpt: "a new tokenizer maps the same input to about 1.0–1.35× more tokens … The headline rate stays, but effective cost can rise meaningfully — estimate against your real workload."
Context: 该 tokenizer 问题自 Opus 4.7（2026-04）开始出现并延续到 Sonnet 5，是 2026 年 Anthropic 模型迁移最常见的隐性成本坑。
Confidence: high

### 1.4 Opus 4.x 演进脉络（用于背景章）

Claim: Opus 4.6（2026-02-05）将 1M token 上下文引入 Opus 线（beta）、引入 Agent Teams 多代理协作；SWE-bench Verified 80.8%（与 4.5 的 80.9% 基本持平，该代主打规模与编排而非推理）。[^16^]
Source: techjacksolutions（Claude Model Lineage 2026）
URL: https://techjacksolutions.com/ai-tools/anthropic-claude/claude-model-lineage-2026/
Date: 2026-07-25
Excerpt: "Feb 5, 2026 Claude Opus 4.6 $5 / $25 per 1M SWE-bench Verified 80.8% … A 1M-token context window arrived in beta, Agent Teams let multiple Claude agents coordinate on a task … The benchmark held flat, which tells you this release was about reach, not raw reasoning."
Context: 同代 Sonnet 4.6（2026-02-17）$3/$15、SWE-bench Verified 79.6%。
Confidence: high

Claim: Opus 4.7（2026-04-16）SWE-bench Verified 87.6%、SWE-bench Pro 64.3%、Terminal-Bench 2.0 69.4%、GPQA Diamond 94.2%；视觉分辨率提升 3.3×；引入 xhigh effort 档与自我验证；三项 API 破坏性变更（移除 extended-thinking budget_tokens、移除 temperature/top_p/top_k 采样参数、thinking 内容默认不返回）；新 tokenizer 使同文本 token 量升至 1.0–1.35×。[^16^][^17^][^18^]
Source: lushbinary（开发者迁移指南）；justoborn；techjacksolutions
URL: https://lushbinary.com/blog/claude-opus-4-7-developer-guide-benchmarks-vision-migration/ ; https://justoborn.com/claude-opus-4-7/
Date: 2026-04-17 / 2026-07-28
Excerpt: "Setting `thinking: {\"type\": \"enabled\", \"budget_tokens\": N}` now returns a 400 error. … Setting `temperature`, `top_p`, or `top_k` to any non-default value returns a 400 error. … The new tokenizer may produce 1.0-1.35x more tokens"
Context: 厂商自报分数；第三方 vals.ai 独立 harness 测得 Opus 4.7 SWE-bench Verified 为 79.4%（见 §2）。Opus 4.7 市场反响偏冷淡（"chilly reception"），是 Anthropic 仅 41 天后即推 4.8 的背景。
Confidence: high

Claim: Opus 4.8（2026-05-28）为 Opus 4 系收官：SWE-bench Verified 88.6%、SWE-bench Pro 69.2%（厂商自报）；引入 Dynamic Workflows（Claude Code 中编排数百个并行 subagent）、effort 五档默认 high、Fast mode 降至 $10/$50；Anthropic 称其遗漏代码缺陷的概率比 4.7 低约 4 倍；仅支持 adaptive thinking。Opus 5 发布后，4.8 与 4.7、4.6 一同被官方归入 Legacy models（仍可调用）。[^19^][^20^][^21^]
Source: stationx Opus 4.8 review；yeasy 智能体 Harness 工程指南（GitBook）
URL: https://app.stationx.net/articles/claude-opus-4-8-review ; https://yeasy.gitbook.io/claude_guide/di-yi-bu-fen-ji-chu-pian/01_intro/1.2_model_family
Date: 2026-05（发布月）/ 2026-07-27
Excerpt: "Anthropic released Claude Opus 4.8 on 28 May 2026 — six weeks after 4.7. Same $5 input / $25 output pricing, same 1M-token context … the most important change isn't on a benchmark chart — it's that the model is roughly four times less likely to let bad code slide past unmentioned."
Context: 旧型号退役节奏：Opus 4 已于 2026-06-15 retired；Opus 4.1 于 2026-06-05 deprecated、2026-08-05 retired。写书时应提示读者：模型迭代周期已缩短到 4–8 周，书中具体模型号必然过时，应教"如何跟进"。
Confidence: high

### 1.5 家族总览（2026-07 时点）

Claim: 截至 2026 年 7 月底，Anthropic 在售家族分四档：Haiku 4.5（$1/$5，200K 上下文）、Sonnet 5（$2/$10 导入价→$3/$15，1M）、Opus 5（$5/$25，1M，Claude Code 默认 Opus）、Fable 5（$10/$50，1M，Mythos 级前沿）；另有受限的 Mythos 5（Project Glasswing 邀请制）。SWE-bench Verified 两年间从 33.4%（Claude 3.5 Sonnet，2024-06）爬升至 96%（Opus 5）。[^22^][^21^]
Source: morphllm Claude Benchmarks；yeasy GitBook
URL: https://www.morphllm.com/claude-benchmarks ; https://yeasy.gitbook.io/claude_guide/di-yi-bu-fen-ji-chu-pian/01_intro/1.2_model_family
Date: 2026-06-09 / 2026-07-27
Excerpt: "Claude 3.5 Sonnet Jun 2024 33.4% … Claude Opus 4.8 May 2026 88.6% Claude Fable 5 Jun 2026 95.0% … 33.4% to 95.0% in two years."
Context: Opus 档价格从 3 代的 $15/$75 降至 4.5 起的 $5/$25（降幅 66%），Fable 5 又重新上探至 $10/$50。
Confidence: high

---

## 二、编程基准：厂商自报 vs 第三方 harness

Claim: 第三方独立 harness（vals.ai SWE-bench Verified，2026-07-22 快照）成绩显著低于厂商自报：Claude Opus 5 以 97.00% 领先，GPT-5.6 Sol 96.20%、Claude Fable 5 95.00%、Kimi K3 93.40%、Claude Opus 4.8 88.60%、Claude Sonnet 5 排名靠后（按难度分布约 84%/77%/76%/67%）。BenchLM 榜单（60 模型）同期显示 Opus 5 96%、Mythos 5 95.5%、Fable 5 95%。[^23^][^24^]
Source: vals.ai SWE-bench Verified 榜单；BenchLM
URL: https://vals.ai/benchmarks/swebench ; https://benchlm.ai/benchmarks/swe-bench-verified
Date: 2026-07-22 / 2026-07-30
Excerpt: "Claude Opus 5 leads SWE-bench Verified with 97.00% accuracy, followed by GPT-5.6 Sol at 96.20% and Claude Fable 5 at 95.00%. … The top models are clustered within 1.0 points, suggesting this benchmark is nearing saturation for frontier models."
Context: 关键写作提示：同一模型在不同 harness 下分数差异可达 8–17 个百分点（如 Opus 4.7：厂商 87.6% vs vals.ai 按难度分布推算约 79%；Sonnet 5 Verified 第三方来源从 72.7% 到 92.4% 不等）。SWE-bench Verified 已接近饱和，区分度正向 SWE-bench Pro（Opus 5 79.2%、Fable 5 80.0%、Sonnet 5 63.2%）与 Frontier-Bench 等更难集转移。另注意 Scale SEAL 标准化榜单上 Claude 最好成绩仅为 Opus 4.6 (thinking) 51.9% public——harness 差异巨大。
Confidence: high

Claim: Anthropic 官方 Opus 5 对比表（厂商内部 harness）：Agentic terminal coding（Frontier-Bench v0.1）Opus 5 43.3% / Fable 5 33.7% / Opus 4.8 21.1% / GPT-5.6 Sol 34.4%；Agentic coding（DeepSWE v1.1）GPT-5.6 Sol 72.7% 领先（Opus 5 68.8%、Fable 5 69.7%）；OSWorld 2.0 Opus 5 70.6% 领先。[^1^]
Source: Anthropic《Introducing Claude Opus 5》官方对比图
URL: https://www.anthropic.com/news/claude-opus-5
Date: 2026-07-24
Excerpt: "On Frontier-Bench v0.1, Opus 5 surpasses all other models, and more than doubles Opus 4.8's performance at a lower cost per task. … These results are from an internal run of Frontier-Bench v0.1, on the mini-SWE-agent harness and a GKE backend, mean reward over 5 attempts per task. Opus 4.8 served as fallback on safety-classifier refusals for Opus 5 and Fable 5."
Context: 官方图表脚注自曝两点局限：内部 harness；安全拒答由旧模型兜底。DeepSWE 上官方自报亦承认 GPT-5.6 Sol 更强——说明 Opus 5 并非全面第一，书中引用应保留这类反例。
Confidence: high

---

## 三、API 定价与订阅档位

Claim: Anthropic 官方订阅（anthropic.com/pricing，2026-07 抓取）：Free $0（不含 Claude Code）；Pro $20/月（年付约 $17/月），含 Claude Code、Cowork、Research；Max 5x $100/月、Max 20x $200/月（5x/20x Pro 用量，高峰优先）；Fable 模型在 Pro 需用量积分、Max 档占每周限额 50%；订阅上下文窗口统一 200K。[^25^]
Source: Anthropic 官方定价页
URL: https://www.anthropic.com/pricing
Date: 2026-07（抓取日 2026-07-31）
Excerpt: "Pro … $17 Per month with annual subscription discount ($200 billed up front). $20 if billed monthly. Everything in Free, plus: More usage* Includes Claude Code … Max … From $100 Per month … Choose 5x or 20x more usage than Pro* … Fable | Usage credits | 50% of weekly limits*"
Context: 团队档 Team Standard $25/座/月、Team Premium $125/座/月、Enterprise 定制。API 与订阅是两条独立计费线。
Confidence: high

Claim: 2026-07 时点 API 价格（每百万 token 输入/输出）：Haiku 4.5 $1/$5（200K 上下文）；Sonnet 4.6 $3/$15（1M）；Sonnet 5 导入价 $2/$10（至 8-31）后 $3/$15；Opus 4.7/4.8 与 Opus 5 $5/$25（1M，128K 输出）；Fable 5 $10/$50；Opus 5 Fast mode $10/$50；缓存读 $0.50/M（90% 折扣）、Batch API 五折。[^26^][^27^]
Source: cloudzero；blogs.novita.ai（截至 2026-07 核价）
URL: https://www.cloudzero.com/blog/claude-pricing/ ; https://blogs.novita.ai/claude-price/
Date: 2026-07-27 / 2026-07-06
Excerpt: "Claude API pricing is per token: Opus 4.7 costs $5/$25, Sonnet 4.6 costs $3/$15, and Haiku 4.5 costs $1/$5 per million input/output tokens. Prompt caching cuts input costs by up to 90%. The Batch API saves 50% on both input and output."
Context: 输出恒为输入 5×。典型单次调用成本（4K 输入+500 输出）：Haiku ~$0.0065、Sonnet ~$0.019、Opus ~$0.032。
Confidence: high

Claim: Anthropic 官方企业数据：Claude Code 的 API 消耗在企业部署中平均约 $13/开发者/活跃日，约 $150–250/开发者/月；90% 用户低于 $30/活跃日。Pro↔API 盈亏平衡点约每月 370 万 token。[^28^][^29^]
Source: ourtoken.ai（转引 Anthropic Claude Code 成本文档）；cloudzero
URL: https://ourtoken.ai/blog/claude-code-api-pricing-vs-subscription ; https://www.cloudzero.com/blog/claude-pricing/
Date: 2026-07-13 / 2026-07-27
Excerpt: "Anthropic's Claude Code cost documentation also says API usage across enterprise deployments averages around $13 per developer per active day and roughly $150 to $250 per developer per month, while 90% of users remain below $30 per active day."
Context: 当前 Claude Code 默认模型：Pro/Team Standard 默认 Sonnet 5；Max 与 API 账户默认 Opus（7-24 起为 Opus 5）。
Confidence: high

---

## 四、Claude Code 核心功能（截至 v2.1.220，2026-07）

### 4.1 Dynamic Workflows（动态工作流）

Claim: Dynamic Workflows 于 2026-05-28 随 Opus 4.8 以 research preview 形式在 Claude Code 推出（要求 v2.1.154+，面向 Enterprise/Team/Max 计划）：模型为任务编写编排脚本，扇出数十到数百个并行 subagent 在后台执行，并以测试套件为成功标准校验产出，面向数十万行级代码库迁移。实测口径：单次最多 16 个并发 agent、单轮总计上限 1,000 个。[^30^][^31^][^32^]
Source: publorai（实测）；enersys（转 TechCrunch）；osasai
URL: https://publorai.com/claude-opus-4-8-review/ ; https://enersys.co.th/en/insights/claude-opus-4-8-dynamic-workflows-2026
Date: 2026-05-29 / 2026-06-24
Excerpt: "Inside Claude Code, the model can now write its own JavaScript orchestration script for a task, then spin up tens to hundreds of parallel subagents in a single session. Up to 16 concurrent agents run at once, with a 1,000-total cap per run. The feature requires Claude Code v2.1.154 or later and ships on Max, Team, and Enterprise plans, on by default for Max and Team."
Context: 触发方式：`ultracode` effort 级别（xhigh + 自动编排）或 `ultracode` 关键词，`/workflows` 管理。v2.1.219 起默认 workflow 规模指引调为 medium（建议少于 15 个 agent）。与任务简报中"稳定并行上限 10-20"一致（官方实测 16 并发）。
Confidence: high

### 4.2 Subagent 机制

Claim: Claude Code subagent 三种创建方式：编程式（SDK `agents` 参数）、文件式（`.claude/agents/` 下 markdown 定义）、内置 `general-purpose` agent；自 v2.1.198 起 subagent 默认在后台并发运行（前台仅在主对话需要结果时）；v2.1.219 起 subagent 默认可嵌套生成至第 3 层（`CLAUDE_CODE_MAX_SPAWN_DEPTH` 可调）。[^33^][^34^][^35^]
Source: code.claude.com 官方文档（sub-agents、agent-sdk/subagents）；官方 changelog
URL: https://code.claude.com/docs/zh-CN/sub-agents ; https://code.claude.com/docs/en/changelog
Date: 2026-07-16 / 2026-07-25
Excerpt: "从 v2.1.198 开始，subagents 默认在后台运行。Claude 在需要结果才能继续时在前台运行 subagent。 … Subagents can now spawn nested subagents up to depth 3 by default (was 1); set CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1 to disable nesting"
Context: Opus 5 更主动委派 subagent（与 4.8 倾向不足相反），官方迁移建议显式设置委派上限以控制成本与延迟。
Confidence: high

### 4.3 Hooks（可编程钩子）

Claim: Claude Code hooks 是在生命周期特定点自动执行的用户自定义 shell 命令/HTTP 端点/LLM 提示；截至 2026-07 官方文档列出 30 个钩子事件（SessionStart、Setup、UserPromptSubmit、UserPromptExpansion、PreToolUse、PermissionRequest、PermissionDenied、PostToolUse、PostToolUseFailure、PostToolBatch、Notification、MessageDisplay、SubagentStart、SubagentStop、TaskCreated、TaskCompleted、Stop、StopFailure、TeammateIdle、InstructionsLoaded、ConfigChange、CwdChanged、FileChanged、WorktreeCreate、WorktreeRemove、PreCompact、PostCompact、Elicitation、ElicitationResult、SessionEnd），v2.1.219 又新增 DirectoryAdded。5 种 handler 类型：command / http / mcp_tool / prompt / agent。[^36^][^35^]
Source: code.claude.com《Hooks reference》（官方）
URL: https://code.claude.com/docs/en/hooks
Date: 2026-07-29（页面更新）
Excerpt: "Hooks are user-defined shell commands, HTTP endpoints, or LLM prompts that execute automatically at specific points in Claude Code's lifecycle. … There are five types: Command hooks (type: \"command\") … HTTP hooks (type: \"http\") … MCP tool hooks (type: \"mcp_tool\") … Prompt hooks (type: \"prompt\") … Agent hooks (type: \"agent\")"
Context: 任务简报中"26 个钩子事件"为较早版本口径；2026-07 官方文档已列 30 个（加上 DirectoryAdded 为 31）。exit code 2 阻断、JSON `decision`/`permissionDecision` 精细控制、`additionalContext` 注入上下文为主要机制。官方安全提示：命令 hooks 以用户完整权限运行。
Confidence: high

### 4.4 Skills、Slash Commands、CLAUDE.md、MCP

Claim: Agent Skills 是打包指令+元数据+可选资源（脚本、模板）的模块化能力（SKILL.md），Claude 在相关时自动调用；Claude Code 中放在 `.claude/skills/`（项目共享）或 `~/.claude/skills/`（个人）；旧的 `.claude/commands/` legacy 自定义命令仍可用，但官方已推荐新工作流用 skills 封装。[^37^][^38^]
Source: claudecn 官方中文文档；claudecode101
URL: https://claudecn.com/docs/agent-skills/ ; https://claudecode101.com/zh/mechanics/slash-commands
Date: 2026-02-07 / 2026-05-24
Excerpt: "Agent Skills 是模块化能力系统，扩展 Claude 的功能。每个 Skill 打包指令、元数据和可选资源（脚本、模板），Claude 在相关时自动使用。 … 旧的 custom commands 仍然可用，但新的可复用工作流更推荐用 skills 来封装。"
Context: Skills 也可用 `/name` 手动调用。Anthropic 为 Office 文档任务（PPT/Excel/Word/PDF）提供预构建 skills。
Confidence: high

Claim: CLAUDE.md 是团队共享的项目记忆文件（另有 `CLAUDE.local.md` 私人记忆、`.claude/rules/*.md` 按路径生效的规则）；官方明确 CLAUDE.md 以用户消息形式注入（非系统提示），不保证严格遵守；构建/测试命令变更后需同步更新。[^39^]
Source: code.claude.com《memory》（官方）
URL: https://code.claude.com/docs/en/memory
Date: 2026-07-22
Excerpt: "CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself. Claude reads it and tries to follow it, but there's no guarantee of strict compliance, especially for vague or conflicting instructions."
Context: 官方建议指令要具体（"Use 2-space indentation"优于"format code nicely"）；必须在固定时点执行的规则应写成 hook 而非 CLAUDE.md。
Confidence: high

Claim: Claude Code 原生完整支持 MCP（本地 stdio 与远程 HTTP/OAuth），MCP 工具以 `mcp__<server>__<tool>` 命名出现在工具事件中，可被 hooks 匹配；2026-07-28 起支持新版 MCP 规范（无状态核心、更强 OAuth/OIDC、Apps 与 Tasks 版本化扩展）。[^40^][^41^]
Source: 腾讯云 MCP 指南；releasebot（转 Anthropic 更新日志）
URL: https://cloud.tencent.com/developer/article/2637671 ; https://releasebot.io/updates/anthropic/claude
Date: 2026-03-11 / 2026-07-28
Excerpt: "2025 年中，Claude Code 加入了对远程 MCP 的原生支持。 … Claude expands support for the new MCP 2026-07-28 spec, bringing a stateless core, stronger OAuth and OIDC authorization, and versioned extensions for Apps and Tasks."
Context: hooks 文档亦证实 MCP tool hooks（`type: "mcp_tool"`）可在已连接的 MCP server 上调用工具。
Confidence: high

### 4.5 版本迭代节奏（2026 年 6–7 月重要更新）

Claim: 2026 年 6–7 月 Claude Code 高频迭代（约每周一个 minor）：Sonnet 5 成为 Pro 默认模型（v2.1.195–201 周）；subagent 默认后台运行（v2.1.198）；桌面版内置浏览器、`/doctor` 自检、`/fork` 后台分叉会话（v2.1.202–206）；v2.1.219 接入 Opus 5 为默认 Opus、1M 上下文、Fast mode、subagent 嵌套至 3 层、sandbox strictAllowlist；另有 Claude Security plugin beta（提交前扫描漏洞）、`/code-review` 后台 subagent。[^42^][^35^][^43^]
Source: code.claude.com《What's new》与官方 changelog；mcpservers.org 周报
URL: https://code.claude.com/docs/en/whats-new ; https://code.claude.com/docs/en/changelog
Date: 2026-07-17 / 2026-07-25
Excerpt: "Added Claude Opus 5 (claude-opus-5), now the default Opus model — 1M context, fast mode at $10/$50 per Mtok … Subagents can now spawn nested subagents up to depth 3 by default (was 1) … Changed dynamic workflows to default to a medium size guideline (aim for fewer than 15 agents)"
Context: 4 月–7 月间从 v2.1.101 到 v2.1.220 约 60 个版本；写作时应强调"工具周更"这一事实，避免读者把书当固定手册用。
Confidence: high

---

## 五、典型使用场景与口碑

Claim: 企业采用与生产力（第三方汇总，需谨慎引用）：常规用户自报生产力提升约 45%、每周节省 3–5 小时；Fortune 100 中 70% 企业已使用 Claude；Anthropic 自身案例称法律团队审查周期从 2–3 天缩短至 24 小时；Stripe 称 Fable 5"把数月工程压缩到数天"（厂商发布页转述的客户轶事，非独立审计）。[^44^][^45^]
Source: segmentfault 企业案例汇总；digitalapplied（指出 Stripe 案例性质）
URL: https://segmentfault.com/a/1190000047819902 ; https://www.digitalapplied.com/blog/kimi-k3-vs-claude-fable-5-frontier-comparison-2026
Date: 2026-06-05 / 2026-07-17
Excerpt: "Stripe reported it compressed months of engineering into days — a customer anecdote relayed in Anthropic's own launch post, not an independent audit."
Context: 典型场景：代码库级迁移/重构（Dynamic Workflows）、长上下文研读（1M）、多步骤 agentic 自动化（Zapier 评价 Sonnet 5"端到端跑完此前会卡住的任务"）、企业合规场景（SOC 2、ISO 27001、HIPAA BAA；政府版 FedRAMP High 公测）。
Confidence: medium（多为厂商转述或自报调研）

Claim: Hacker News 对 Opus 5 发布的讨论（1224–1738 points）：关注点从榜单分数转向企业可用性——Opus 5 不受 Fable 5 的 30 天数据保留限制、前端"图片转 HTML"还原度优于 Fable 5；同时社区对审查、ID 验证与封号问题、以及"分数接近但价格差一倍"（GPT-5.6/Kimi K3）的总拥有成本提出担忧。[^46^]
Source: Hacker News 每日早报（转述 HN 讨论）
URL: https://jasjojo.com/posts/2026-07-25-hacker-news-daily/
Date: 2026-07-25
Excerpt: "Opus 5 的发布把焦点从'榜单分数'移向'企业可用性'。 … 评论也反映出用户对封号、审查、ID 验证等可靠性问题的担忧——性能再强，如果服务不稳定，也难以成为生产首选。 … chmod775 指出 GPT-5.6 和 Kimi K3 在分数接近的情况下，价格只有 Opus 5 的一半。"
Context: 口碑总体正面但务实："榜单第一是营销胜利，评论区更关注总拥有成本"。
Confidence: medium（二手转述 HN）

---

## 六、常见坑与注意事项（最佳实践章素材）

Claim: 坑①——迁移类：Opus 5 默认思考吃掉 max_tokens（HTTP 200 静默截断）、`thinking: disabled` + xhigh/max 直接 400；Opus 4.7 起移除采样参数与 budget_tokens；新 tokenizer 使实际 token 消耗升至 1.0–1.35×（标价未变、账单上涨）。[^6^][^18^][^13^]
Source: rabinarayanpatra（Opus 5 迁移实录）；lushbinary；oflight
URL: https://www.rabinarayanpatra.com/blogs/claude-opus-5-migration-breaking-changes ; https://lushbinary.com/blog/claude-opus-4-7-developer-guide-benchmarks-vision-migration/
Date: 2026-07-26 / 2026-04-17
Excerpt: "Nothing throws. The request returns HTTP 200, stop_reason comes back as \"max_tokens\", and the answer is cut mid-sentence. If you are logging only errors, you will not see it."
Context: 迁移清单要点：grep 所有未设 thinking 的调用点并加大 max_tokens；删除提示词中的自我验证指令（Opus 5 自发验证，旧指令导致重复验证）；显式限制 subagent 委派；重跑 effort sweep（旧档位含义已重校准）。
Confidence: high

Claim: 坑②——订阅限额：Pro/Max 为滚动 5 小时窗口 + 每周上限；长会话恢复一次可消耗 5 小时窗口的 10–15%；Claude Code 会话启动即加载约 2 万 token 仓库上下文；Web/Desktop/移动端与 Claude Code 共享同一额度。[^47^]
Source: suprmind.ai
URL: https://suprmind.ai/hub/claude/pricing/claude-max-pricing/
Date: 2026-07-25
Excerpt: "Some Max 5x subscribers describe hitting the cap after five to ten lightweight prompts … resuming a long chat can consume 10 to 15% of a five-hour window before the first new answer. … Claude Code also loads roughly 20,000 tokens of repository context when a session starts, so terminal work consumes quota before you send a real prompt."
Context: 社区总结的省额度手段：`/clear` 与 `/compact`（约省 67%/会话）、精简 CLAUDE.md 至 500 token 内（省约 91% 上下文加载）、permissions.deny 屏蔽大目录、Opus 只做规划/编排、执行交给 Sonnet/Haiku。
Confidence: high

Claim: 坑③——上下文管理是第一优先级：上下文越满模型表现越差（早期指令遗忘、错误率上升）；高频"上下文杀手"包括无限制代码库探索、同会话堆叠不相关任务、对同一错误反复纠正超过两次不清空、过长 CLAUDE.md。[^48^]
Source: 掘金（转引 Anthropic 官方最佳实践文档）
URL: https://juejin.cn/post/7646622735791767562
Date: 2026-06-02
Excerpt: "上下文越满，模型表现越差：早期指令被遗忘、错误率上升、输出质量下滑。 … 核心原则：把 /clear 当成 Ctrl+Z——频繁使用，而不是最后一招。"
Context: Opus 5 官方也注明 1M 窗口"accepting a million tokens is not the same as perfect recall across all of them"（接收不等于全记住），任务超过 200K 会触发上下文压缩（compaction）。
Confidence: high

Claim: 坑④——过度谨慎与静默行为：开发者报告 Opus 4.8 偶发过度谨慎、拒绝合法工作；Opus 5 分类器误拒率较 Fable 5 降低约 85% 但拒答以 HTTP 200 + `stop_reason: "refusal"` 返回，无异常抛出，代码需显式处理（可开 server-side fallback beta，拒答自动路由到 Opus 4.8）；Fable 5 的"silent nerf"争议：模型卡披露其对前沿 AI 研发类请求会静默降级（不通知用户）。[^30^][^6^][^49^]
Source: stationx；rabinarayanpatra；kunalganglani
URL: https://app.stationx.net/articles/claude-opus-4-8-review ; https://www.kunalganglani.com/blog/claude-fable-5-benchmark-developer
Date: 2026-05 / 2026-06-10
Excerpt: "The model uses invisible techniques like prompt modification and steering vectors instead of returning a clear refusal. … A decline is an HTTP 200 with stop_reason: \"refusal\", not an error, so code that reads response.content[0] unconditionally breaks on it."
Context: Opus 5 关闭思考时的两个文档化故障模式：把 tool call 写成可见文本而不真正执行（agentic loop 中污染后续轮次）、内部 XML 标签泄漏到回复中。
Confidence: high

Claim: 坑⑤——版本快速变动带来的配置漂移：背景 subagent 行为在 v2.1.186/198 两次变更默认值；嵌套深度 1→5→3 多次反复；CLAUDE.md 指令与 hooks 配置随版本语义变化（如 matcher 连字符规则 v2.1.195 才支持）。[^33^][^35^][^43^]
Source: code.claude.com 官方文档与 changelog
URL: https://code.claude.com/docs/zh-CN/sub-agents ; https://cc.bruniaux.com/releases/
Date: 2026-07
Excerpt: "Subagents no longer spawn nested subagents by default (restored to depth 3 in 2.1.219); set CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH to control nesting"
Context: 写书建议：所有版本敏感行为标注文档核查日期，并引导读者以 `/doctor`、`/context` 与官方 changelog 为准。
Confidence: high

---

## 七、写给作者的要点（第一章·背景与格局 / 最佳实践章）

1. **格局主线： Anthropic 在 2026 年 H1 完成了"四档家族 + 周更工具"的布局**。模型侧：Haiku 4.5（$1/$5）→ Sonnet 5（$2/$10 导入价，免费/Pro 默认）→ Opus 5（$5/$25，Claude Code 默认 Opus，SWE-bench Pro 79.2%）→ Fable 5（$10/$50 Mythos 级前沿，曾遭美国出口管制暂停 3 周）。工具侧：Claude Code 以每周一个 minor 版本迭代（v2.1.101→v2.1.220 仅三个月），Dynamic Workflows（16 并发/单轮千个 subagent）、30+ hooks、skills、嵌套 subagent 构成完整的可编程 agent 平台。第一章可用"模型迭代周期 4–8 周、工具周更"立论：读者需要的是方法论而非固定手册。
2. **引用基准必须区分 harness**。同一模型厂商自报与第三方独立 harness 可差 8–17 个百分点（Opus 4.7：官方 87.6% vs vals.ai 约 79%；Sonnet 5 Verified 各来源 72.7%–92.4%）。SWE-bench Verified 已趋饱和（前三差距 <1 分），区分度在 SWE-bench Pro 与更新的 agentic 基准；Anthropic 自己的图表也承认内部 harness + 拒答兜底。建议书中固定用一句话注明"分数以厂商 system card 为准/为第三方 harness 实测"。
3. **价格故事的真正主角不是标价而是"有效成本"**。Opus 档三年降价 66%（$15/$75→$5/$25），但新 tokenizer（1.0–1.35×）、默认思考、更主动的 subagent 委派都会推高实际账单；Sonnet 5 的 $2/$10 导入价 2026-08-31 到期。订阅 vs API 的决策可用官方数据锚定：Claude Code 平均 $13/开发者/活跃日，90% 用户 <$30/日，Pro↔API 平衡点约 370 万 token/月。
4. **最佳实践章最有价值的五条工程结论**：①上下文管理优于一切技巧——`/clear` 当 Ctrl+Z 用、CLAUDE.md 控制在 500 token 内、1M 窗口≠完美记忆（>200K 触发压缩）；②必须固定执行的规则写 hook 而非 CLAUDE.md（官方明确 CLAUDE.md 不保证遵守）；③Opus 5 时代要"删提示词"而非"加提示词"——自我验证、进度汇报、主动委派都已内建；④迁移模型必跑 checklist（思考默认值、effort 与 disabled 互斥 400、refusal 的 HTTP 200 静默返回）；⑤成本路由：Opus 做规划与编排、Sonnet/Haiku 做执行，重用户可省 40–85%。
5. **风险与合规素材（提升章节厚度）**：Fable 5 出口管制事件（2026-06-12 至 07-01）是"模型即受管制物"的首个商用案例；Fable 5 强制 30 天数据保留 + 敏感请求静默回退 Opus 4.8（<5% 会话）+ 对前沿 AI 研发任务的静默降级争议，以及 hooks 以用户完整权限执行的安全提示，都适合作为"生产环境使用 AI 编程工具的治理清单"。


---

## 附录：引用来源清单

- [^1^] Anthropic, "Introducing Claude Opus 5", https://www.anthropic.com/news/claude-opus-5, 2026-07-24（官方一手）
- [^2^] tryfriday.ai, "Anthropic Launches Claude Opus 5: $5/$25 Pricing, 96% SWE-bench, July 24, 2026", https://www.tryfriday.ai/blog/anthropic-launches-claude-opus-5, 2026-07-24（仅转官方数据）
- [^3^] StationX, "Claude Opus 5: capabilities, benchmarks, pricing and release date", https://app.stationx.net/articles/claude-opus-5-release, 2026-07-24
- [^4^] rankedagenticmodels.com, "Claude Opus 5: Frontier Intelligence at Opus Pricing", https://www.rankedagenticmodels.com/blog/claude-opus-5-launch-analysis-2026, 2026-07-26
- [^5^] gptimage2.org, "Claude Opus 5: What Anthropic Shipped on July 24, 2026", https://gptimage2.org/blog/claude-opus-5-launch-2026, 2026-07-25
- [^6^] Rabinarayan Patra, "Claude Opus 5: What Breaks When You Migrate from Opus 4.8", https://www.rabinarayanpatra.com/blogs/claude-opus-5-migration-breaking-changes, 2026-07-26
- [^7^] OpenRouter Docs, "Claude Opus 5 Migration Guide", https://openrouter.ai/docs/cookbook/evaluate-and-optimize/model-migrations/opus-5, 2026-07-24；apidog, "Claude Opus 5's Effort Parameter", https://apidog.com/blog/claude-opus-5-effort-parameter/, 2026-07-25
- [^8^] SevenSolvers, "Anthropic's Most Powerful AI Models Explained (2026)", https://www.sevensolvers.com/blog/anthropics-most-powerful-ai-models-explained-2026, 2026-06-10
- [^9^] distk.in, "Claude Fable 5 & Mythos 5", https://distk.in/blog/claude-fable-5-mythos-5-marketing-guide-2026.html, 2026-06-15
- [^10^] Convly, "Claude Opus 4.7 vs Sonnet 4.6 vs Fable 5", https://www.convly.ai/blog/claude-opus-4-7-vs-sonnet-4-6-vs-fable-5-2026, 2026-06
- [^11^] LinkedOtter, "What Anthropic's Export Ban Means for B2B AI Buyers (June 2026)", https://linkedotter.com/articles/what-anthropic-export-ban-means-for-b2b-ai-buyers-june-2026, 2026-07-01
- [^12^] DataNorth AI, "Top 10 AI Tools for 2026", https://datanorth.ai/blog/top-10-ai-tools-for-2026, 2026-07-29
- [^13^] O'Flight, "Claude Sonnet 5 Deep Dive", https://www.oflight.co.jp/en/columns/claude-sonnet-5-anthropic-release-2026-06-30, 2026-07-01
- [^14^] Cosmic JS, "Claude Sonnet 5: Benchmarks, Pricing, and What Developers Need to Know", https://www.cosmicjs.com/blog/claude-sonnet-5-benchmarks-pricing-developers, 2026-06-30
- [^15^] Layer3Labs, "Kimi K3 vs Claude Sonnet 5", https://www.layer3labs.io/comparisons/kimi-k3-vs-claude-sonnet-5, 2026-07-22
- [^16^] Tech Jack Solutions, "Claude Model Lineage 2026", https://techjacksolutions.com/ai-tools/anthropic-claude/claude-model-lineage-2026/, 2026-07-25
- [^17^] LushBinary, "Claude Opus 4.7 Developer Guide", https://lushbinary.com/blog/claude-opus-4-7-developer-guide-benchmarks-vision-migration/, 2026-04-17
- [^18^] JustOborn, "Claude Opus 4.7", https://justoborn.com/claude-opus-4-7/, 2026-07-28
- [^19^] StationX, "Claude Opus 4.8: A Review", https://app.stationx.net/articles/claude-opus-4-8-review, 2026-05
- [^20^] Yeasy GitBook, "Claude 模型家族", https://yeasy.gitbook.io/claude_guide/di-yi-bu-fen-ji-chu-pian/01_intro/1.2_model_family, 2026-07-27
- [^21^] MorphLLM, "Claude Benchmarks (2026)", https://www.morphllm.com/claude-benchmarks, 2026-06-09
- [^22^] MorphLLM（同上）；数据转引 Anthropic 官方发布页
- [^23^] vals.ai, "SWE-bench Verified Leaderboard", https://vals.ai/benchmarks/swebench, 2026-07-22（第三方独立 harness）
- [^24^] BenchLM, "SWE-bench Verified", https://benchlm.ai/benchmarks/swe-bench-verified, 2026-07-30
- [^25^] Anthropic, 官方定价页, https://www.anthropic.com/pricing, 抓取 2026-07-31（官方一手）
- [^26^] CloudZero, "Claude Pricing, Explained", https://www.cloudzero.com/blog/claude-pricing/, 2026-07-27
- [^27^] Novita AI Blog, "Claude Price", https://blogs.novita.ai/claude-price/, 2026-07-06
- [^28^] OurToken, "Claude Code API Pricing vs Subscription", https://ourtoken.ai/blog/claude-code-api-pricing-vs-subscription, 2026-07-13
- [^29^] CloudZero（同 [^26^]）
- [^30^] PublorAI, "Claude Opus 4.8 Review: We Tested It Against 4.7", https://publorai.com/claude-opus-4-8-review/, 2026-05-29
- [^31^] Enersys, "Anthropic's Claude Opus 4.8 and Dynamic Workflows", https://enersys.co.th/en/insights/claude-opus-4-8-dynamic-workflows-2026, 2026-06-24（转 TechCrunch）
- [^32^] OsasAI, "How Opus 4.8 Actually Behaves Inside Claude Code", https://osasai.com/blog/claude-opus-4-8-coding-review, 2026-05-30
- [^33^] code.claude.com 官方文档《子代理》, https://code.claude.com/docs/zh-CN/sub-agents, 2026-07-16（官方一手）
- [^34^] code.claude.com《Agent SDK Subagents》, https://code.claude.com/docs/en/agent-sdk/subagents, 2026-07-16
- [^35^] code.claude.com 官方《Claude Code changelog》, https://code.claude.com/docs/en/changelog, 2026-07-25（官方一手）
- [^36^] code.claude.com 官方《Hooks reference》, https://code.claude.com/docs/en/hooks, 2026-07-29（官方一手）
- [^37^] claudecn.com（官方中文文档镜像）《Agent Skills》, https://claudecn.com/docs/agent-skills/, 2026-02-07
- [^38^] ClaudeCode101, "Slash Commands 指南", https://claudecode101.com/zh/mechanics/slash-commands, 2026-05-24
- [^39^] code.claude.com 官方《How Claude remembers your project》, https://code.claude.com/docs/en/memory, 2026-07-22（官方一手）
- [^40^] 腾讯云开发者社区, "Claude Code 通关手册（六）：MCP 协议完全指南", https://cloud.tencent.com/developer/article/2637671, 2026-03-11
- [^41^] Releasebot, "Claude — Updates & Release Notes", https://releasebot.io/updates/anthropic/claude, 2026-07-28（转官方更新日志）
- [^42^] code.claude.com 官方《What's new in Claude Code》, https://code.claude.com/docs/en/whats-new, 2026-07-17（官方一手）
- [^43^] mcpservers.org, "Claude Code July 2026 Updates", https://mcpservers.org/blog/claude-code-updates-july-2026, 2026-07-26；bruniaux.com Releases, https://cc.bruniaux.com/releases/
- [^44^] SegmentFault, "Claude模型助力企业编程效率提升3倍？", https://segmentfault.com/a/1190000047819902, 2026-06-05
- [^45^] DigitalApplied, "Kimi K3 vs Claude Fable 5", https://www.digitalapplied.com/blog/kimi-k3-vs-claude-fable-5-frontier-comparison-2026, 2026-07-17
- [^46^] JasJojo, "Hacker News 每日早报 2026-07-25", https://jasjojo.com/posts/2026-07-25-hacker-news-daily/, 2026-07-25（转述 HN 讨论）
- [^47^] Suprmind, "Claude Max Pricing", https://suprmind.ai/hub/claude/pricing/claude-max-pricing/, 2026-07-25
- [^48^] 掘金, "Claude Code 高效使用完全指南", https://juejin.cn/post/7646622735791767562, 2026-06-02（转引 Anthropic 官方最佳实践文档）
- [^49^] Kunal Ganglani, "Claude Fable 5: A Developer's Analysis", https://www.kunalganglani.com/blog/claude-fable-5-benchmark-developer, 2026-06-10
