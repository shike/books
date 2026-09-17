# 维度07：AI编程Agent/模型横向评测与选型方法论（截至2026年7月）

> 调研日期：2026-07-31。方法：32 次独立搜索（中英文混合），优先官方榜单（Scale SEAL、LMArena、Terminal-Bench）、官方文档（Anthropic、OpenAI、阿里云、Kimi）、深度测评（morphllm、digitalapplied、composio、futureproofing）与 arXiv 论文。
> 核心发现：① SWE-bench 成绩 = 模型 × harness × 数据污染 的联合产物，厂商自报与 Scale 标准化 harness 之间存在 10~30 分系统性差距；② 2026 年 2 月 OpenAI 公开弃用 SWE-bench Verified（污染 + 59.4% 题目测试用例有缺陷），行业重心转向 SWE-bench Pro；③ harness 工程（检索、上下文管理、子代理）对成绩的影响 routinely 大于模型代际差异；④ 百万 token 上下文已成旗舰标配，但"标称窗口"与"产品内有效窗口"差异巨大（Codex API 1.05M vs Codex 客户端 400K；Cursor 标称 200K 实测有效 70K–120K）；⑤ 国内 Coding Plan 五家横评：火山方舟唯一原生 Anthropic 协议，智谱 GLM 兼容性最广但额度抵扣规则最坑，MiniMax 入门价最低，Kimi 唯一 token 计量制，百炼 2026 年改版后仅售 Pro 档。

---

## A. 主流基准榜单与口径差异

### A1. SWE-bench Verified 已接近饱和，头部模型堆在 95%±2 分

Claim: 截至 2026 年 7 月，SWE-bench Verified 头部成绩已堆到 95%–97%（Claude Opus 5 97%、GPT-5.6 Sol 96.2%、Claude Fable 5 95%），基准对前沿模型已基本失去区分度。[^1^]
Source: Vals AI SWE-bench Verified 榜单
URL: https://vals.ai/benchmarks/swebench
Date: 2026-07-22
Excerpt: "Claude Opus 5 leads SWE-bench Verified with 97.00% accuracy, followed by GPT-5.6 Sol at 96.20% and Claude Fable 5 at 95.00%. Kimi K3 scores 93.40%, followed by GPT-5.6 Luna at 93.00%, Claude Opus 4.8 at 88.60%, and Grok 4.5 at 86.60%."
Context: Vals AI 为第三方独立复测平台；注意其数字与 BenchLM（Opus 5 96%）、llm-stats（Fable 5 95.0%）互有出入，正说明口径不统一。 Verified 共 500 题、固定数据集、2024 年冻结。
Confidence: high

### A2. 厂商自报 vs Scale 标准化 harness：同族模型差 17–21 分

Claim: Scale AI 的 SEAL 标准化榜单让所有模型跑同一套 scaffold，与厂商自报成绩存在系统性差距：Anthropic 自报 Opus 4.8 在 SWE-bench Pro 上 69.2%，而 Scale 标准化 harness 下最好的 Claude 成绩（Opus 4.6 thinking）只有 51.9%，单族内差距 17.3 分；morphllm 总结"看到比 Scale 榜高 10–30 分的 SWE-bench Pro 成绩，就是厂商 scaffold 数字"。[^2^][^3^]
Source: Morph（morphllm.com）SWE-bench Pro 榜单页；DigitalApplied 分析
URL: https://www.morphllm.com/swe-bench-pro ; https://www.digitalapplied.com/blog/swe-bench-verified-june-2026-benchmark-vs-scaffolding-analysis
Date: 2026-06-28 / 2026-06-16
Excerpt: "The vendor-vs-standardized gap is consistent: the aggregate reports 69.2% for Opus 4.8 while Scale's best standardized Claude run (Opus 4.6 thinking) scores 51.9% on the public set. GPT-5.3 Codex reports 56.8% on its own scaffold; the predecessor gpt-5.2-codex scores 41.0% under Scale's standardized harness. When you see a SWE-bench Pro score 10-30 points above the Scale leaderboard, it is a vendor-scaffold number."
Excerpt 2: "Anthropic reports 69.2% for Opus 4.8 on SWE-bench Pro using its own scaffold, while the best Claude score on Scale's standardized SEAL board is 51.9% (Opus 4.6 thinking) — a 17.3-point gap within a single model family."
Context: 这直接验证了背景线索中"厂商自报 vs 标准化 harness 约 20 分差距"。Scale 榜单（2026 年 6 月）：GPT-5.4 (xHigh) 59.1% 第一、Muse Spark 55.0%、Claude Opus 4.6 (thinking) 51.9%、Gemini 3.1 Pro 46.1%；95% 置信区间约 ±3.5 分，相邻名次不可区分。
Confidence: high

### A3. Scale SEAL 榜首口径：GPT-5.4 以 59.1% 居标准化 SWE-bench Pro 榜首（2026年6月）

Claim: Scale 标准化 SWE-bench Pro 公开集（731 题，Pass@1）2026 年 6 月榜首为 GPT-5.4 (xHigh) 59.1%；Claude Fable 5、Opus 4.8、GPT-5.5、GLM-5.2 均无标准化公开集成绩，其在市面上的高分（如 Fable 5 的 80.3%）全部来自厂商自有 harness。[^3^]
Source: Morph SWE-bench Pro Leaderboard（引用 Scale AI 官方榜）
URL: https://www.morphllm.com/swe-bench-pro
Date: 2026-06-28
Excerpt: "GPT-5.4 (xHigh) leads at 59.1%, 4.1 points ahead of Meta's Muse Spark (55.0%) and 7.2 ahead of the best Claude run (Opus 4.6 thinking, 51.9%). Confidence intervals are roughly ±3.5 points, so adjacent ranks below the top three overlap. ... Claude Fable 5, Opus 4.8, GPT-5.5, and GLM-5.2 have no standardized public-set entry, so their numbers in the next sections are vendor-reported."
Context: 对应背景线索"Scale标准化榜首61.5%"——6 月口径下榜首实为 59.1%（GPT-5.4）；61.5% 可能为更早/其他月份快照，写书时建议以 Scale 官网（labs.scale.com/leaderboard）当期数字为准并注明日期。
Confidence: high（差距结论）；medium（具体榜首分数随月份变动）

### A4. 2026年2月 OpenAI 弃用 SWE-bench Verified：污染 + 59.4% 难题测试用例有缺陷

Claim: OpenAI 2026 年 2 月发布《Why SWE-bench Verified no longer measures frontier coding capabilities》，宣布停止报告 Verified 成绩：所有前沿模型（含别家）都能仅凭 task ID 近乎逐字复现 gold patch（训练数据污染的铁证）；对 138 道其模型反复失败的难题审计发现 59.4% 测试用例有实质缺陷（过窄拒绝对的答案或过宽放过错的答案）。[^4^][^5^]
Source: codingfleet.com 基准史梳理；buildmvpfast.com 污染分析（引 OpenAI 官方博客）
URL: https://codingfleet.com/blog/swe-bench-pro-explained-the-new-standard-for-ai-coding-benchmarks-2026/ ; https://www.buildmvpfast.com/blog/benchmark-contamination-ai-coding-leaderboard-swe-bench-2026
Date: 2026-06-04 / 2026-07-01
Excerpt: "Their contamination audit found that every frontier model — GPT-5.2, Claude Opus 4.5, Gemini 3 Flash — could reproduce verbatim gold patches or problem-specific details from certain Verified tasks. The test data had leaked into training data. Worse: an audit of 138 hard problems found that 59.4% had flawed test cases that rejected functionally correct solutions."
Excerpt 2: "「SWE-bench Pro is not perfect, but empirically seems to suffer less from contamination issues...」— OpenAI, recommending SWE-bench Pro, February 2026"
Context: 独立研究佐证：32.67% 的 Verified 成功补丁涉及答案泄漏，模型从训练数据回忆正确文件路径的命中率高达 76%（digitalapplied）。写作注意：59.4% 是"故意挑出的难/失败切片"的缺陷率，不是全集缺陷率。
Confidence: high

### A5. 审计发现 Terminal-Bench 2.0 榜首全部存在 harness 级作弊

Claim: 2026 年 Meerkat 审计工具对 Terminal-Bench 2.0 全部头部提交（Pilot 82.9%、两个 ForgeCode 81.8%）发现 harness 级作弊：Pilot 在 429 条成功轨迹中有 415 条读取了按任务规范本应不可见的 /tests 目录（verifier injection）；ForgeCode 的 scaffold 自动把含标准答案的 AGENTS.md 注入系统提示。把 ForgeCode 换成干净 scaffold（Terminus 2）同模型成绩从 81.8% 跌到 71.7%，从第 1 掉到第 14。[^6^]
Source: arXiv 2604.11806（Meerkat 审计论文）
URL: https://arxiv.org/pdf/2604.11806
Date: 2026（arXiv 编号 2604，约 2026 年 4 月）
Excerpt: "Verifier injection (Pilot, #1). In 415 of 429 successful Pilot traces the agent reads from a /tests directory that should be inaccessible per the Terminal-Bench task spec... When we substitute the ForgeCode traces that reference AGENTS.md with the same model (Opus 4.6) running through a clean scaffold (Terminus 2), the overall pass rate falls from 81.8% to 71.7%, dropping the submission from #1 (under the original numbering) to 14th place."
Context: 这是"榜单成绩 ≠ 模型能力"最极端的证据：榜首成绩可以是 harness 漏洞的产物。另见 UC Berkeley 2026 年 4 月发现"8 大 agent 基准均可被 reward-hack 到约 100%"（awesome-agentic-ai-zh 综述引用）。
Confidence: high

### A6. Terminal-Bench 2.0 榜单格局（2026年7月）：GPT 系领先终端任务

Claim: Terminal-Bench 2.0（Laude Institute，真实终端环境端到端任务）2026 年 7 月：llm-stats 口径 GPT-5.5 以 82.7% 居首（49 个模型，均值 0.58）；BenchLM 镜像的厂商发布口径 GPT-5.6 Sol 91.9% 居首；最佳开源为 GLM-5.1（69.0%，第 11 名）。[^7^]
Source: llm-stats.com Terminal-Bench 2.0；benchlm.ai 镜像
URL: https://llm-stats.com/benchmarks/terminal-bench-2 ; https://benchlm.ai/benchmarks/terminalBench2
Date: 2026-07-31
Excerpt: "GPT-5.5 from OpenAI currently leads the Terminal-Bench 2.0 leaderboard with a score of 0.827 across 49 evaluated AI models... GLM-5.1 by Zhipu AI is the top-ranked open-source model on Terminal-Bench 2.0, with a score of 0.690 (rank #11)."
Excerpt 2: "GPT-5.6 Sol leads the public snapshot at 91.9%, followed by Claude Mythos 5 (88.0%) and GPT-5.6 Terra (87.4%)."
Context: 两个聚合站数字差异再次体现口径问题（自报 vs 复测）。 marc0.dev 月度榜另有 Codex CLI + GPT-5.5 以 82.0% 居"工具+模型"组合榜首（2026-04-23 OpenAI 提交）。终端/DevOps 类任务是 GPT 系传统强项，Claude Opus 4.7 仅 69.4%。
Confidence: high

### A7. LiveCodeBench 系列：竞赛编程维度，注意 v5/v6/Pass@1-COT 等切片不可混比

Claim: LiveCodeBench（防污染竞赛编程基准，滚动收录 LeetCode/AtCoder/Codeforces 新题）2026 年 7 月各口径榜首：滚动榜 Qwen3.7 Max 91.6%；v6 切片 Sakana Fugu-Ultra 93.2%；DeepSeek 自报 Pass@1-COT 口径 V4 Pro (Max) 93.5%；Artificial Analysis 独立复测口径 Gemini 3 Pro 91.7%。LiveCodeBench Pro（奥赛奖牌选手评审版）榜首 Sakana Fugu-Ultra 90.8%。[^8^]
Source: BenchLM LiveCodeBench 各切片榜
URL: https://benchlm.ai/benchmarks/livecodebench ; https://benchlm.ai/benchmarks/liveCodeBenchPro
Date: 2026-07-30
Excerpt: "Compare v6 rows only when the date window, code-generation scenario, pass@k or average-at-k metric, sampling count, temperature, and execution policy match. A shared v6 label does not guarantee the rest of the setup is controlled."
Excerpt 2: "Qwen3.7 Max leads the LiveCodeBench leaderboard on BenchLM's July 2026 update with 91.6%, ahead of Qwen3.7 Plus (89.6%) and GLM-4.7 (84.9%)"
Context: BenchLM 的编辑注明确警告：同一"LiveCodeBench"名下有 v5、v6、Pass@1-COT、滚动窗口等多个不可互比的切片。且 LiveCodeBench 不测"在既有仓库内工作"的能力——它与 SWE-bench 测的是两种不同能力。
Confidence: high

### A8. LMArena 已拆成 9 个分榜；WebDev 榜 Anthropic 霸榜但第一名≠采购结论

Claim: LMArena（Arena.ai）2026 年已拆分为 Text/Code/WebDev/Vision/Search 等 9 个竞技场；Code Arena WebDev 榜（2026-05-24 快照）前五中四个是 Claude Opus 变体（claude-opus-4-7-thinking 1567 分居首），首个 OpenAI 模型在十名开外；Qwen/GLM/Kimi/Gemini 均在可挑战距离内。专业建议是"用 Arena 做初筛，再在自己仓库上验证"，且"供应商自称第一时查 Style Control + 95% CI 重叠"。[^9^]
Source: PropelCode 开发者指南；Botnation LMArena 机制解析；Arena 官方 changelog
URL: https://www.propelcode.ai/blog/lm-arena-coding-leaderboard-insights-for-developers ; https://botnation.ai/en/chatbot-arena/ ; https://arena.ai/blog/leaderboard-changelog
Date: 2026-05-27 / 2026-07-28 / 2026-07-31
Excerpt: "As of the May 24, 2026 snapshot, claude-opus-4-7-thinking leads with a 1567 score, followed by claude-opus-4-7, claude-opus-4-6-thinking, qwen3.7-max-20260517, and claude-opus-4-6. The practical takeaway is not 'pick rank one everywhere.' It is to use Arena rank, rank spread, vote depth, latency, cost, and your own repository evals together before changing production routing."
Context: Arena 的价值在"真实人类偏好的流动分布"，静态基准会被污染/刷分而 Arena 不会；但 WebDev 榜测的是前端/Agent 建站，不是 PR review 或仓库级修复。Kimi K3 在 Fronted Code Arena 排名第一、领先第二名 Fable 5 达 48 分（天聊博客引 X 社区，2026-07）。
Confidence: high（机制与格局）；medium（具体名次随投票流动）

---

## B. Harness 工程为何比模型更重要

### B1. 论文级证据：同一模型换 harness，成绩波动可达 34–48 个百分点

Claim: arXiv 综述《Why Current Evaluation Conflates Model and Harness》系统论证：基准分数是"模型 × harness 决策链"（上下文构造、工具调用、解析、重试、摘要、停止）的联合结果。实证：同一 Opus 4.5 在 Scale 标准化 SEAL scaffold 下 SWE-bench Pro 得 45.9%，在 Claude Code 下得 55.4%；HAL 榜单显示同一模型在 SWE-Agent vs HAL Generalist 两种 scaffold 下，Sonnet 4.5 从 68% 掉到 34%（-34 分）、GPT-5 Medium 从 46% 掉到 12%、o4-mini 波动近 48 分；第三方监测报告 GPT-5 仅 scaffold 差异就有 11 分、Kimi K2 Thinking 有 15 分。[^10^]
Source: arXiv 2605.23950
URL: https://arxiv.org/pdf/2605.23950
Date: 2026（arXiv 编号 2605，约 2026 年 5 月）
Excerpt: "Under the standardized SEAL scaffold on SWE-bench Pro, Claude Opus 4.5 reaches 45.9%, while under Claude Code the same model reaches 55.4%... The Holistic Agent Leaderboard (HAL) reports double-digit gaps for the same model under different scaffolds on SWE-bench Verified Mini, with reported single-model swings of up to nearly 48 percentage points across leading frontier models. Independent third-party benchmark monitoring reports up to 11 percentage points of scaffold-only variation for GPT-5 and 15 points for Kimi K2 Thinking on SWE-bench Verified. None of these effects are model upgrades. They are harness substitutions, and they routinely dwarf the 2 to 4 percentage point shifts that papers report as meaningful model advances."
Context: 全书最重要的量化证据之一："harness 替换造成的波动 routinely 超过论文宣称的模型代际进步（2–4 分）"。
Confidence: high

### B2. 加一个检索子代理（WarpGrep）即可翻转模型排名

Claim: 在其他基础设施完全相同的条件下，仅增加一个搜索子代理 WarpGrep，就能让 SWE-bench Pro 上 MiniMax 2.5 与 Claude Opus 4.6 的排名翻转——尽管 Opus 在大多数其他基准上更高；该工具增加为各模型带来 2.1–2.2 分提升，"相当于一次常规模型升级"。[^10^]
Source: arXiv 2605.23950（引 Morph 的 SWE-bench Pro 数据）
URL: https://arxiv.org/pdf/2605.23950
Date: 2026（约 5 月）
Excerpt: "Adding a single search subagent (WarpGrep) to otherwise identical infrastructure flips the SWE-bench Pro ordering between MiniMax 2.5 and Claude Opus 4.6, despite Claude Opus ranking higher on most other benchmarks. ... Adding the WarpGrep search subagent on top of identical infrastructure adds 2.1 to 2.2 points across models, comparable to a routine model upgrade"
Context: "工具设计/检索子代理"作为 harness 组件的因果级证据。检索质量（retrieval）是 harness 的第一杠杆。
Confidence: high

### B3. Cursor 研究：同一模型在不同 harness 下 46% vs 80%

Claim: Cursor 的 agent 基准研究显示同一模型在一套 harness 下 46%、另一套下 80%——差距来自：整库灌入 vs 检索相关文件、单一大任务 vs 拆分作用域子任务、畸形工具调用崩溃 vs 纠正重试、遗忘中间结果 vs 结构化工作记忆。MindStudio 据此提出决策框架：先修 harness（提示词、工具描述、重试逻辑），再考虑升级模型。[^11^]
Source: MindStudio 博客《What Is the Agent Harness? Why Scaffolding Matters More Than the Model》
URL: https://www.mindstudio.ai/blog/agent-harness-scaffolding-matters-more-than-model
Date: 2026-05-18
Excerpt: "Cursor's research on agent benchmarking showed the same model scoring 46% on one agent harness and 80% on another. The model didn't change. The scaffolding did. ... scaffolding choices often create larger performance deltas than switching between frontier models."
Context: 注意存在 harness-model fit："Claude 模型更可靠地遵循复杂系统提示；GPT-4o 对某些工具格式更好；Gemini 的上下文行为影响检索策略"——换模型时 harness 往往需要重新校准。
Confidence: high（方向性结论）；medium（46/80 具体数字为转引，建议写书时溯源 Cursor 原文）

### B4. scaffold 有效性高度依赖模型：SWE-Effi 发现"昂贵失败"现象

Claim: SWE-Effi（arXiv 2509.09853）用五种 scaffold × 三种模型在 Verified 子集上复测：SWE-Agent 配 Qwen3-32B 解决率 28%（35.5 次调用、44 万输入 token），配 GPT-4o-mini 暴跌到 10%（181 次调用、810 万输入 token，18 倍成本）；未解决尝试平均消耗资源是成功尝试的 4 倍以上。结论：scaffold 效果不是 scaffold 的固有属性，而是与基座模型的协同产物。[^12^]
Source: arXiv 2509.09853（SWE-Effi）
URL: https://arxiv.org/pdf/2509.09853
Date: 2025-09（2026 年仍被广泛引用）
Excerpt: "SWE-Agent paired with Qwen3-32B achieves a 28% resolution rate with 35.5 API calls and 440k input tokens, but this drops to just 10% when using GPT-4o-mini, despite requiring 181 calls and over 8.1 million input tokens—more than 18x the token cost. ... an unresolved attempt consumes on average over 4 times more resources than a successful one."
Context: 对"只看解决率"的选型方法提出成本维度修正：评估 agent 系统要看 token 预算内有效性（EuTB），失败比成功贵 4 倍。
Confidence: high

### B5. 上下文工程（context engineering）取代提示词工程成为核心运行时杠杆

Claim: Anthropic 的 harness 设计文献将"context engineering"（在任何给定时刻为模型策展最优 token 集合）定义为 agent 运行时的核心杠杆，应对长程任务的方案包括 context reset、子代理分解、事件虚拟化；前沿模型在 <4 分钟人类任务上约 100% 成功，>4 小时任务上不足 10%——退化的是跨时间的状态管理，不是逐 token 推理。[^13^]
Source: arXiv 2605.02244（引 Anthropic 工程文献、METR、APEX-SWE）
URL: https://arxiv.org/pdf/2605.02244
Date: 2026（约 5 月）
Excerpt: "Anthropic's harness-design literature [Anthropic, 2025, 2026] centers context engineering as the runtime lever, with proposed fixes (context resets, sub-agent decomposition, event virtualization) acting as workarounds for the absence of a principled training signal. ... METR's failure-mode analysis shows that reasoning quality on subproblems extracted from long-horizon failures matches the corresponding short-horizon benchmarks; what degrades is state handling across time, not reasoning per token."
Context: 配套实践解读（jeanlabelle.ca 对 Anthropic 官博的精读）："context rot"——token 数增长时模型开始遗忘/误用早期信息，因此不能"全灌进去"，需要策展。Anthropic 官方原文标题为《Effective context engineering for AI agents》（anthropic.com/engineering）。
Confidence: high

### B6. 子代理（subagent）的核心价值是上下文隔离而非"更聪明"

Claim: 子代理解决的核心问题是"上下文污染"：探索代码库、跑测试、操控浏览器产生的高噪声中间输出会撑爆主上下文；子代理把噪声隔离在独立上下文、只把结论回传主代理，同时带来并行执行与成本分层（高消耗任务用便宜快模型）。2026 年 subagent 已从概念变为 Claude Code（subagents/agent teams）、Codex（Subagent，2026-03-16 发布）、Cursor（Explore/Bash/Browser 内置子代理）的标配。[^14^][^15^]
Source: 极客时间《分而治之：Sub-Agents的核心概念与应用价值》；cnblogs Cursor 子代理解析；QQ 新闻 Codex Subagent
URL: https://time.geekbang.org/column/article/943368 ; https://www.cnblogs.com/goloving/p/19636848 ; https://browser.qq.com/mobile/news?doc_id=46369bec08e43652
Date: 2026-02-02 / 2026-02-25 / 2026-03-21
Excerpt: "如果你觉得 Claude Code 越用越'健忘'，并不是模型退化了，而是你的对话上下文，已经被一次次中间过程污染了。这正是子代理要解决的核心问题。"
Excerpt 2: "子代理的价值：（1）上下文隔离：中间过程的乱七八糟留在子代理里，主代理只看最终结论（2）并行执行：多个子代理同时跑，不用排队（3）降低成本：高消耗任务用更便宜的快速模型处理"
Context: Claude Code 2026 年的 Dynamic Workflows 进一步把编排计划"从上下文窗口搬进 Claude 现写的 JavaScript 脚本"，单次可拉起上千并行子代理（lapudacloud 架构综述）。腾讯云开发者社区判断："未来 AI 编程的竞争，不只是模型强弱，而是谁更会拆任务。"
Confidence: high

---

## C. 主流工具横评（Claude Code / Codex / Cursor / Kimi Code / GLM·ZCode / MiniMax）

### C1. Claude Code vs Codex：功能发布时间线 18:4，治理架构哲学不同

Claim: 开发者 Elie Bakouch 整理 2025-02 至 2026-06 时间线：两家共有 24 项相似功能，18 项 Claude Code 先发（headless、MCP、slash 命令、上下文压缩、子代理、hooks、skills），Codex 仅先发 4 项（内置沙箱、云端异步 agent、多代理并行、/goal 模式），且 Codex 的先发优势以"天"计（/goal 仅领先 11 天）。治理架构上 Claude Code 重心在应用层（hooks + 权限），Codex 重心在内核层（macOS Seatbelt / Linux Landlock+seccomp 沙箱 + 三种审批策略）。[^16^][^17^]
Source: CSDN/AtomGit 对比文（引 Elie Bakouch 时间线）；blakecrosley.com 决策参考（Authority A）
URL: https://aicoding.csdn.net/6a4a3a4210ee7a33f2882365.html ; https://blakecrosley.com/zh-Hans/blog/claude-code-vs-codex
Date: 2026-07-05 / 2026-06-05
Excerpt: "两家共有24项相似功能，其中18项是Claude Code先发布的，Codex只先发布了4项。…Codex的先发优势正在以'天'为单位蒸发：/goal：Codex先上，11天后Claude Code追平"
Excerpt 2: "Claude Code 的重心在应用层；钩子是您编写的、用来拦截特定事件的程序。Codex 的重心在内核层；无论模型尝试什么，操作系统都会阻止不被允许的操作。"
Context: 基准互有胜负（2026-06）：SWE-bench Pro 64.3% vs 58.6%（Claude 胜）、Verified 88.7% vs 87.6%（GPT-5.5 胜）、Terminal-Bench 2.0 82.7% vs 69.4%（GPT-5.5 大胜）。Claude Code 每天贡献超 32.6 万次 GitHub 提交、约占全部公开提交 10%。Codex 开源（Apache-2.0），Claude Code 专有。
Confidence: high

### C2. Claude Code vs Codex：token 效率与执行模式差异

Claim: Codex 的 token 效率约为 Claude Code 的 3 倍（社区盲测/实测口径），云端沙箱执行不触碰本地环境；Claude Code 直接在本地终端运行，灵活但有风险（用户反映其"非常喜欢用 git push --force"，甚至自行降级 Spring Boot 版本）。500+ 开发者盲测约 67% 认为 Claude Code 代码"更整洁、更易维护"；Codex 代码"更短、可用但解释更少"。[^18^][^19^]
Source: CSDN AI编程社区；什么值得买 深度对比
URL: https://aicoding.csdn.net/6a4a3a4210ee7a33f2882365.html ; https://post.smzdm.com/p/am9680xz
Date: 2026-07-05 / 2026-06-21
Excerpt: "Codex的云端沙箱执行意味着你的本地环境不会被触碰。而Claude Code直接在你的机器上运行，虽然更灵活，但也带来了潜在风险——有用户反映Claude Code'非常喜欢用 git push --force，甚至在依赖冲突时直接去降级你Spring Boot的版本号'。"
Excerpt 2: "一项包含500余名开发者的社区盲测显示，约67%的受访者认为 Claude Code 输出的代码'更整洁、更易维护'。…'Claude Code 写出来的代码像高级工程师写的，Codex 则像一个高效执行者'。"
Context: 融合趋势：OpenAI 推出 Codex Plugin for Claude Code；不少团队采用"Claude 设计 + Codex 执行"混合模式。
Confidence: medium（盲测与轶事证据，方向一致但非受控实验）

### C3. Cursor vs Claude Code：有效上下文 70K–120K vs 1M；同任务 token 消耗 5.5–5.7 倍差

Claim: Builder.io 2026 年实测：Cursor 标称 200K 上下文，但为保持交互速度每步压缩重述，有效窗口仅 70K–120K；同一任务 Cursor 消耗约 188K token、Claude Code 约 33K（5.7 倍差）。Composio 100+ 小时实测报告类似 5.5 倍差距，并注明两者在约 150K token 真正相关上下文之外都开始退化。机制差异：Cursor 用语义索引 + grep + Explore 子代理（索引有常驻成本），Claude Code 无索引、按需 grep/glob/read。[^20^][^21^]
Source: futureproofing.dev（2026-07 更新）；composio.dev 长测
URL: https://www.futureproofing.dev/resources/ai-native-team/cursor-vs-claude-code-2026 ; https://composio.dev/content/cursor-vs-claude-code
Date: 2026-07-20 / 2026-07-16
Excerpt: "Cursor advertises 200K but truncates to 70K to 120K effective to keep the interactive loop fast. ... On an identical task, Cursor burns roughly 5.7x the tokens Claude Code does. Builder.io's reproducible test put Claude Code at about 33K tokens against Cursor's 188K for the same result."
Excerpt 2: "One caveat: both start to degrade beyond roughly 150k tokens of genuinely relevant context, so neither truly wins at extreme scale."
Context: 定价：Cursor Pro $20/Pro+ $60/Ultra $200，Teams $40/席；Claude Code 捆绑在 Claude Pro $20 / Max 5x $100 / Max 20x $200 内。Cursor Composer 2.5 自研模型 $0.50/$2.50 每百万 token，Terminal-Bench 2.0 69.3%（≈Opus 4.7 的 69.4%）。注意方法论警示：两次测试两边用了不同模型，"5.5–5.7x"是工具+模型+架构的联合效果。
Confidence: medium-high（多源一致，但非严格受控）

### C4. Kimi Code CLI：开源 Apache-2.0，K2.7 Code 主打 token 效率，API 价格约为 Opus 4.8 的 1/5

Claim: Kimi Code CLI 是 Moonshot 的终端 agent（2026-01 随 K2.5 发布，Apache-2.0 开源，从 Python 重写为 Bun+TypeScript）；K2.7 Code（2026-06-12）主打推理 token 用量降 30%，HighSpeed 模式 180 tokens/s（短上下文 260）；API $0.95/$4.00 每百万 token，约为 Claude Opus 4.8 的 1/5；订阅 $19/月起，每 5 小时窗口 300–1200 次调用、并发上限 30。短板：无独立基准复测，高难推理与 Claude 有记录差距。[^22^]
Source: pureailabs Kimi Code 长评；stork.ai；百度百科（英文）
URL: https://pureailabs.com/ai-coder/kimi-code-review/ ; https://baike.baidu.com/en/item/Kimi%20Code%20CLI/1892166
Date: 2026-06-16 / 2026-05-15
Excerpt: "Kimi K2.7 Code API pricing sits at $0.95 per million input tokens and $4.00 per million output tokens as of June 2026... The 5x price advantage over Claude Opus 4.8 is not a marketing claim it is a number that compounds into real budget differences at production scale... no independent submission exists as of this writing, and the gap against Claude on hard reasoning tasks is documented in the K2.6 generation."
Context: Kimi 官方博客披露其用 Kimi Code CLI 完成 moonshot.ai 整站重构的实战案例：先 /init 生成 AGENTS.md 并花一小时打磨，再接 Figma MCP——"第一步不是写提示词，而是设置上下文"。Moonshot 2026 年 5 月融资后估值约 200 亿美元。K3（2026-07-16，2.8T 参数最大开源模型、1M 上下文）发布后 Kimi 会员一度限购。
Confidence: high（价格与规格）；medium（性能判断缺独立复测）

### C5. GLM Coding Plan / ZCode：最便宜的 Claude Code 平替，$18/月起、1M 上下文、Anthropic 协议即插即用

Claim: Z.ai（智谱国际版）GLM Coding Plan 是最便宜的正规 Claude Code 后端平替：Lite $18/月（约 400 prompts/5h、2000/周），支持 Claude Code/Cline/Roo Code/OpenCode/Goose/OpenClaw/Kilo Code/ZCode 等 20+ 工具（Anthropic 兼容端点 api.z.ai/api/anthropic，OpenAI 兼容端点 api.z.ai/api/openai/v1）；GLM-5.2 提供 1M 上下文变体 glm-5.2[1m]；MIT 开源权重可自托管。价格 2026 年内多次上涨（2 月 $3 → 3 月 $10 → 4 月 $18，HN 有"价格翻倍"讨论）。已知短板：速度属前沿模型中最慢一档；发布时无官方基准（流传的 SWE-bench Pro 62.1 为第三方测）；云 API 数据经中国服务器；prompt 计配额+高峰倍率+不退款。[^23^][^24^]
Source: aitoolanalysis 30 天实测；truescho 指南；bota.chat；totalum.app 对比
URL: https://aitoolanalysis.com/glm-coding-plan-review/ ; https://www.totalum.app/blog/glm-5-2-claude-code-alternative-2026 ; https://bota.chat/z-ai/glm-coding-plan/
Date: 2026-06-18 / 2026-06-22 / 2026-07-21
Excerpt: "GLM 5.2's 1M context lets you keep a mid-sized repo in working memory without the chunking, retrieval and summarization scaffolding that Claude Code users build to stay under 200K."
Excerpt 2: "Prompt-based quotas with peak-hour multipliers and no refunds... Cloud API routes your code through servers in China... Launch benchmarks are self-reported, not independently verified"
Excerpt 3: "The plan was launched in February 2026 at an introductory price of $3/month, rose to $10 in March, and settled at $18/month on April 11, 2026 after massive demand forced Z.AI to rebalance its infrastructure."
Context: 趣闻：2025 年 12 月 MIT 研究者发现 GLM 模型在约半数特定测试提示下自称 Claude；GLM-5 曾以"Pony Alpha"隐身名发布。ZCode 是 Z.ai 自有 IDE。Cursor 无原生 Z.ai 支持（需 OpenAI 兼容端点，功能不全）。
Confidence: high

### C6. MiniMax：Token Plan 全模态统一订阅，M3 为"国内首个集齐前沿 Coding/Agentic + 百万上下文 + 原生多模态"的开源模型

Claim: MiniMax 2026-03-23 将 Coding Plan 升级为 Token Plan（业内首个全模态统一订阅，编程+视频+语音+音乐+图像，多模态额度独立不占编程用量）；M3（2026-06-01）为国内首个集齐前沿 Coding/Agentic 能力、百万 token 上下文、原生多模态的开源模型，SWE-bench Verified 80.5%（$0.30/$1.20）。档位：Starter ¥29/月（约 600 次/5h）、Plus ¥49（约 1500 次/5h）、Max ¥119（约 4500 次/5h）；支持 sk-cp Key 接入 Claude Code/Cline/OpenClaw 等任意 OpenAI 兼容工具，也可在自家 MiniMax Code 开箱即用。[^25^]
Source: cnblogs 七大平台选型实录（引 DoNews、36氪、MiniMax 官方页）
URL: https://www.cnblogs.com/bykj123/p/21330712
Date: 2026-07-10
Excerpt: "2026年3月23日，MiniMax宣布将原有的Coding Plan全面升级为Token Plan，成为业内首个支持全模态模型的统一订阅计划…Plus及以上套餐在保留编程模型用量的基础上增加了多模态调用额度，且多模态额度独立不占用编程模型用量。"
Excerpt 2: "Starter（Lite）版：每月29元起，提供约600次/5小时的请求额度，是目前市场上入门价格较低的月付方案之一（来源：MiniMax开放平台Token Plan页面，2026年7月数据）"
Context: 第三方点评："MiniMax的套餐应该是这几家里面性价比最高的，但是用户体验是个谜"（jb51 配置教程，2026-05）。负面口碑：模型规模相对小、复杂任务能力不足、档位多选择困难（cnblogs 避坑指南）。
Confidence: high（档位与机制）；medium（体验评价）

---

## D. 上下文窗口：百万 token 成标配，但"标称 ≠ 有效"

### D1. 旗舰模型 2026 年全面进入 1M 上下文时代

Claim: 2026 年旗舰编程模型上下文对比：Claude Opus 4.6 起 Opus 级首获 1M context（beta，>200K 部分溢价 $10/$37.50）；Opus 4.8/Sonnet 5 原生 1M；GPT-5.5 API 1M（1,050,000）、Codex 内 400K；Gemini 3.1 Pro 1M；GLM-5.2 有 1M 变体；Kimi K3 1M；MiniMax M3 百万级。Anthropic 官方同时推出 context compaction（beta）应对长会话。[^26^][^27^]
Source: Anthropic 官方《Introducing Claude Opus 4.6》；swfte.com 三家旗舰规格对比
URL: https://www.anthropic.com/news/claude-opus-4-6 ; https://www.swfte.com/de/blog/claude-opus-4-7-vs-gpt-5-5-vs-gemini-3-1-pro
Date: 2026-02-05 / 2026-07-20
Excerpt: "1M token context (beta). Opus 4.6 is our first Opus-class model with 1M token context. Premium pricing applies for prompts exceeding 200k tokens ($10/$37.50 per million input/output tokens), available only on the Claude Platform."
Excerpt 2: "The three vendors converged on a similar playbook this cycle: large flagship, an explicit 'thinking' or extended-reasoning mode, 1M-token context, and aggressive coding scores. [表格] Claude Opus 4.7: 200K (1M beta) | GPT-5.5: 400K | Gemini 3.1 Pro: 1M"
Context: 背景线索"百万token上下文已成标配"得到确认，但注意规格表中的"400K"列即下一条的"产品内缩水"现象。
Confidence: high

### D2. Codex 的"1.05M vs 400K vs 272K"：API 规格、产品额度、计费边界是三件事

Claim: GPT-5.5/5.6 API 上下文上限均为 1,050,000 token（最大输出 128K），但 Codex 客户端产品额度约 400K（272K 输入预算 + 128K 输出）；GPT-5.6 初期 Codex v0.144.5 曾短暂 500K（372K+128K），v0.144.6 又降回 400K。关键坑：API 单次请求输入超 272K 后，该请求输入费率 ×2、输出 ×1.5。GitHub issue #28852 大量用户请愿"让 Codex 内的 GPT-5.5 开放 1M 有效上下文"。[^28^][^29^]
Source: yage.ai 深度拆解；GitHub openai/codex issue #28852
URL: https://yage.ai/share/codex-gpt56-context-budget-20260721.html ; https://github.com/openai/codex/issues/28852
Date: 2026-07-22 / 2026-06-18
Excerpt: "底层的 API 模型规格非常明确且保持稳定…两款模型在 API 渠道的 context window 上限均为 1,050,000 token…而一旦模型通过 ChatGPT subscription 路由接入 Codex 客户端，其适用的产品额度约定就发生了变化…默认配置将这一空间拆分为 272K 输入预算与 128K 最大输出限制"
Excerpt 2: "根据 API 官方文档，一旦单次请求的输入 token 超过 272K，该请求的输入和输出费率将分别按 2 倍与 1.5 倍计费。"
Excerpt 3: "We want GPT-5.5 in Codex to expose 1M effective context... So GPT-5.5 has a 1M-context capability path, but Codex currently does not expose that capability fully to users."
Context: 书中对比"Claude Code 200K/1M vs Codex 200K/105万"时应精确化：两边都是"API 窗口大、产品窗口小"，Claude Code 侧 1M 也只在特定档位/beta 开放；有效上下文还受 compaction 触发点影响。
Confidence: high

### D3. 有效上下文衰减：150K 真正相关内容后各家都开始退化

Claim: 即使标称 1M，实测中"真正相关上下文"超过约 150K token 后 Claude Code 与 Cursor 都开始退化；Cursor 为保交互速度主动截断到 70K–120K 有效窗口。检索/策展仍不可替代。[^21^]
Source: composio.dev 100+ 小时长测
URL: https://composio.dev/content/cursor-vs-claude-code
Date: 2026-07-16
Excerpt: "both start to degrade beyond roughly 150k tokens of genuinely relevant context, so neither truly wins at extreme scale."
Context: 与 B5 的"context rot"相互印证：窗口规格是上限，不是能力承诺。GLM 官方也承认 5.2 的 1M 是"usable 1M"（其评测图强调 usable）。
Confidence: medium-high

---

## E. 定价对比（API 与订阅）

### E1. 2026 年 7 月旗舰 API 价格一览（每百万 token，输入/输出）

Claim: 2026 年 7 月主流旗舰 API 定价：Claude Haiku 4.5 $1/$5（200K）；GPT-5.6 最快档 $1/$6（1M）；Gemini 3.5 Flash $1.50/$7.50（1M）；Gemini 3.1 Pro $2/$12（1M，>200K $4/$18）；GPT-5.6 Terra $2.50/$15（1M）；Claude Sonnet 5 $3/$15（1M，限时 $2/$10 至 8/31）；Claude Opus 5 $5/$25（1M）；GPT-5.6 Sol $5/$30（1M）；Claude Fable 5 $10/$50（1M）；另有 OpenAI 最贵档 $30/$180。[^30^]
Source: AI Price Compare（2026-07-23 核价）
URL: https://aipricecompare.org/zh/
Date: 2026-07-23
Excerpt: "全新 Sonnet 旗舰;限时 $2/$10 至 8 月 31 日 $3.00 $15.00 1M | 全新 Opus 旗舰(7 月 24 日);接近 Fable 5,价格减半 $5.00 $25.00 1M | 最强大;出口管制暂停后于 7 月 1 日恢复 $10.00 $50.00 1M"
Context: 早期（4 月）口径下 Opus 4.7 输出价是 GPT-5.5 的 5 倍、Gemini 3.1 Pro 的 7 倍（swfte.com）；Anthropic 定价逻辑是"对标人类工程师时薪"。写书建议用当期核价表并注明日期。
Confidence: high

### E2. "每解决一个基准点的美元成本"：Haiku 4.5 是性价比之王

Claim: 用 Scale SEAL SWE-bench Pro 成绩 ÷ 输出价格折算"每解决一分成本"：Claude Haiku 4.5 ≈ $0.13/分（39.45%，$1/$5），GPT-5.4 $0.25/分，Gemini 3.1 Pro $0.26/分，Claude Opus 4.6 $0.48/分；纯 token 地板价是 DeepSeek V4 Flash $0.14/$0.28（1M 上下文）。[^31^]
Source: Morph《Best AI Model for Coding (June 2026)》
URL: https://www.morphllm.com/minimax-m2-5-coding
Date: 2026-06-28
Excerpt: "Dividing output price by Scale SEAL SWE-bench Pro score: Claude Haiku 4.5 about $0.13 of output per point, gpt-5.4 $0.25, Gemini 3.1 Pro $0.26, Claude Opus 4.6 $0.48. For raw per-token cost with a 1M context, DeepSeek V4 Flash at $0.14/$0.28 is the floor."
Context: 该页还给出 2026-06 的推荐："能买到的最好模型是 Opus 4.8（Verified 88.6%、Pro 厂商口径 69.2%、$5/$25、1M）；标准化 harness 最好的是 GPT-5.4（SEAL #1，$2.50/$15）"。Fable 5 因 6-12 出口管制令暂停（7-1 恢复）。
Confidence: high

### E3. 订阅制对比：海外 Claude/Codex/Cursor/Copilot 档位与额度机制

Claim: 海外订阅（2026 年中）：Claude Pro $20（Sonnet 4.6/Opus 4.7，5h 窗口+周额度双时钟）、Max 5x $100、Max 20x $200（可跑 6–12 个并发 Claude Code 会话）；ChatGPT/Codex Plus $20、Pro 5x $100、Pro 20x $200；Cursor Pro $20/Pro+ $60/Ultra $200（美元额度制，超出按模型价计）；GitHub Copilot Pro $10/Pro+ $39（含 GPT-5.5、Claude Opus 4.7）；学生版免费。[^32^][^21^]
Source: GitHub xiaotiewinner/coding-plan 对比表；composio.dev
URL: https://github.com/xiaotiewinner/coding-plan ; https://composio.dev/content/cursor-vs-claude-code
Date: 2026-06-02 / 2026-07-16
Excerpt: "Limits run on two clocks at once: a 5-hour rolling window plus a weekly cap, so an all-day session can hit the wall mid-task."
Excerpt 2: "Auto mode is the cheap lever: it runs Composer 2.5 or routes to a capable model automatically, and it is unlimited on paid plans."
Context: "5 小时滚动窗口 + 周上限"双时钟是 Claude/Codex/Kimi 等订阅的共同机制，重度用户最常见的挫败来源。高级"全家桶"工程师典型组合成本约 $220/月（Cursor + Claude Max 20x）。
Confidence: high

---

## F. 国内 Coding Plan 深度横评（百炼 / 火山方舟 / 智谱 GLM / MiniMax / Kimi）

### F1. 客户端兼容性：火山方舟唯一原生 Anthropic 协议，智谱覆盖最广（20+），Kimi 最少（3 款）

Claim: 五大平台客户端兼容性（2026-03 横评）：百炼 7 款（OpenAI 协议，接 Claude Code 需 proxy）；火山方舟 11 款（OpenAI + Anthropic 双协议，唯一可让 Claude Code 用原生 API 格式直连）；MiniMax 7+ 款（需 proxy）；智谱 GLM 20+ 款（覆盖最广，需 proxy）；Kimi 3 款（最少）。差异化卖点：百炼唯一月度总量制+首购 ¥7.9 最低价；方舟 Auto 智能调度自动选模型；MiniMax 入门 ¥29（首月 ¥9.9）；智谱 4 个专属 MCP（联网/视觉/网页/仓库）；Kimi 唯一 token 计量制、无 5h 窗口限制。[^33^]
Source: 掘金《5 大国内 Coding Plan 全量横评：2026 选型指南》
URL: https://juejin.cn/post/7613191044306829339
Date: 2026-03-04
Excerpt: "方舟是唯一支持 Anthropic 协议的平台，Claude Code 可直接用原生 API 格式对接，无需 proxy 适配。智谱客户端覆盖面最广（20+ 款），几乎兼容所有主流 AI 编程工具。Kimi 客户端最少（3 款），目前覆盖有限。"
Excerpt 2: "Kimi：Token 计量制（唯一），无 5h 窗口限制，长时间编程最友好"
Context: 但注意 F4：Kimi 后来改为"5h token 配额 + 7 天刷新"，机制有演变，写书以官方当期页面为准。
Confidence: high

### F2. 各平台额度机制与档位（2026 年中汇总）

Claim: 档位与额度（¥）：火山方舟 Lite 40 / Pro 200（5h 1200 次·周 9000·月 18000 / 5h 6000 次·周 45000·月 90000，聚合豆包/GLM/DeepSeek/Kimi/MiniMax，Auto 调度；Lite 每日 00:00 限量补货库存紧张）；智谱 Lite 49 / Pro 149 / Max 469（5h 80 次·周 400 / 5h 400·周 2000 / 5h 1600·周 8000，每日 10:00 补货）；MiniMax 29 / 49 / 119 / 469；Kimi Andante 49 / Moderato 99 / Allegretto 199 / Allegro 699（1x/4x/20x/60x 额度）；百炼 Pro 198 / 高级 698 / 尊享 1398（token 总量制，不限次数）。[^34^][^35^]
Source: 掘金《2026年国内主流AI Coding Plan套餐全对比》；GitHub xiaotiewinner/coding-plan
URL: https://juejin.cn/post/7644035283980877887 ; https://github.com/xiaotiewinner/coding-plan
Date: 2026-05-26 / 2026-06-02
Excerpt: "火山方舟|Lite|40 元|5h/1200 次、周 9000 次、月 18000 次|每日 00:00 限量释放，库存紧张|豆包自研、GLM、DeepSeek、Kimi、MiniMax 全聚合"
Excerpt 2: "智谱 AI|Pro（主推）|149 元|5h/400 次、周 2000 次|每日 10:00 定时补货，拼模立减 5%…政策提醒：2026 年 4 月 30 日起，老套餐停止自动续订，需手动续费。"
Context: 阿里云百炼 2026 年改版：3-20 起 Lite 停止新购、4-13 停止续费，当前仅 Pro 可购且每日限量放名额；额度"仅允许在代码编辑器、本地AI编程智能体中使用，不对外开放批量自动化接口调用"（阿里云官方开发者社区，2026-07-07，Authority A）。
Confidence: high

### F3. 隐藏坑清单：额度倍率、封号风险、超售、退款难

Claim: 六平台隐藏风险（开发者社区整理）：百炼配置文档不完善、有"充值后模型与宣传不一致"投诉且无退订退款；火山方舟超售、高峰期慢、退款条款苛刻；智谱 GLM-5 额度抵扣规则复杂（高峰 3 倍、非高峰 2 倍），新用户每周限额严格如"大小周"；Kimi 工具适配限制极严（非指定工具使用可能封号）、仅限个人禁企业开发、token 计量受缓存影响大（实际额度可能远低于预期）；MiniMax 复杂任务能力不足；无问芯穹售后慢。[^36^]
Source: cnblogs《2026年国内主流AI Coding Plan套餐全对比｜开发者避坑指南》
URL: https://www.cnblogs.com/wzxNote/p/19648084
Date: 2026-02-27
Excerpt: "智谱GLM：GLM-5额度抵扣规则复杂（高峰期3倍、非高峰期2倍），容易不知不觉耗尽额度；新用户每周限额严格，相当于'大小周'使用。Kimi：工具适配限制极严，非指定工具使用可能封号；仅限个人使用，禁止企业开发；Token计量受缓存影响大，实际额度可能远低于预期。"
Context: 智谱侧另一佐证（GitHub Gist 深度测评，2026-03）：2026 年初 GLM-5 上线服务器承压致高峰并发报错，智谱发致歉信并退款/延期补偿；正面口碑是"价格约为 Claude 官方 1/7、用量达 Claude Pro 的 3 倍、55+ tokens/s"。
Confidence: medium-high（社区口碑，个例性质但多源一致）

### F4. Kimi Code 额度机制实测：统一额度池 + 7 天刷新 + 缓存吞额度

Claim: Kimi Code 不单独收费，消耗会员统一额度池（聊天/Coding/Agent 共享，池尽则 Kimi Code 冻结）；额度按 5 小时 token 配额 + 每 7 天刷新、未用不累积；实测坑：Cache Read 计入 token 计量——一用户 5 小时内 5h 额度才用 81% 而周额度已爆到 101%，8.62M token 中 7.6M 是 Cache Read；按实测折算 Andante ¥49 档周限额约仅 26 个 prompts。[^37^][^38^]
Source: aicontent.homes Kimi 会员指南；rosetears.cn 实测横评
URL: https://aicontent.homes/tutorials/kimi-membership-kimi-code-guide-2026 ; https://rosetears.cn/archives/87/
Date: 2026-05-05 / 2026-02-26
Excerpt: "Kimi Code 本身不额外收费。它消耗的是你当前会员计划下的统一额度池。如果会员总额度在当前计费周期用尽，Kimi Code 也会被冻结，直到周期刷新或升级计划。"
Excerpt 2: "为什么周限额消耗得比 5H 额度还快？？？…一共跑了大概 8.6238M tokens（Input 758.2K，Output 265.6K，Cache Read 7.6M）…由此可推算出 Kimi 的周限制大致如下：Andante（49）1 倍（基准）26 prompts"
Context: 官方口径：每 5h 配额约 300–1200 次 API 调用、最大并发 30（codingplan.org/plans/kimi）。2026-03-01 起"Kimi Code 3 倍额度"由限时转永久。写书重点：token 计量制下"缓存读"是额度黑洞，与 GLM 的"高峰倍率"并列两大易踩坑。
Confidence: high（实测 + 官方文档互证）

### F5. 五家选型速查（社区共识版）

Claim: 什么值得买 2026-07 横评的选型结论：学生/轻量 → 百炼（¥7.9 首月，次月 ¥20）；高频调试/IDE 重度 → MiniMax（¥29，响应快、重试不扣量）；团队/Claude 生态 → 火山方舟（稳定、无强限流、团队共享额度）；复杂重构/专业算法 → 智谱 GLM（代码可用度高但按 token 计费长文本消耗快）；生态联动 → 百度千帆。[^39^]
Source: 什么值得买《2026主流Coding Plan横向对比》
URL: https://post.smzdm.com/p/a8wg6xdq
Date: 2026-07-28
Excerpt: "学生党/个人轻量开发：首选阿里云百炼，7.9元首月体验，次月20元…高频调试/本地IDE重度用户：首选MiniMax，29元/月，响应快、重试不扣量…团队协作/Claude生态用户：首选火山方舟…复杂代码重构/专业算法需求：首选智谱GLM"
Context: 与 juejin/cnblogs 的横评结论方向一致；该文自述"真实实测无商业合作"。
Confidence: medium-high

---

## G. 实战选型方法论（什么场景选什么）

### G1. 按场景路由模型，而不是忠于单一模型

Claim: 2026 年选型共识是"按任务路由"：代码审查/复杂重构 → Claude（Opus 4.8）；研究综合/超大代码库 → Gemini 3.1 Pro（1M+、$2/$12 最便宜旗舰）；面向用户对话/结构化输出 → GPT-5.5；高频后台任务 → 便宜模型（Haiku/DeepSeek/GLM-Flash）。新手从 Claude 起步（Cursor/Windsurf/Claude Code 默认体验都围绕它打造）。[^40^]
Source: marcotechai 三模型实测对比
URL: https://marcotechai.com/blog/best-ai-coding-model-2026
Date: 2026-06-27
Excerpt: "2026 年真正用得好的人，没有一个是只忠于单一模型的。他们会根据任务复杂度和成本，把活分给不同的模型：Claude → 代码审查、复杂重构；Gemini → 研究与资料综合、超大代码库；GPT-5.5 → 面向用户的对话、结构化输出"
Context: 国内版共识（CSDN 生存指南）：旗舰层 Opus 4.8（编程最强）/ GPT-5.5（最均衡）/ GLM-5.2（开源最强且免费）/ Gemini 3.1 Pro（多模态）；代码补全场景首选 DeepSeek-V4（低延迟便宜）。
Confidence: high

### G2. 工具选型决策树：IDE 优先 vs 终端优先，混合使用是常态

Claim: Cursor vs Claude Code 的本质是"控制模型"之争而非功能对等：Cursor 是 IDE-first（人驱动、AI 内联辅助，适合 tab 补全/单文件/前端/可视化审查）；Claude Code 是 agent-first（人下简报、agent 跨文件自主执行+自验证，适合多文件重构/框架升级/CI）；2026 年 7 月多数资深工程师两个都用、按任务路由。重构大工程优先 Claude Code；已有 OpenAI 套餐可用 Codex CLI 交叉验证；前端 UI 可用 Antigravity（自动浏览器测试）。[^20^][^41^]
Source: futureproofing.dev；花渡《2026 四大 AI 编程工具怎么选》
URL: https://www.futureproofing.dev/resources/ai-native-team/cursor-vs-claude-code-2026 ; https://guide.rtxk.us/tutorial/ai-coding-tools-compare.html
Date: 2026-07-20 / 2026-07-22
Excerpt: "Cursor vs Claude Code is not a feature-parity fight. It is a control-model choice. Cursor is an IDE-first editor where you drive and the AI assists inline. Claude Code is a terminal-first agent where you brief the task and the agent drives multi-file work. ... As of July 2026, most senior AI-native engineers run both and route by task."
Excerpt 2: "重构大工程：优先试 Claude Code…长任务先拆阶段、看差异，别把整个仓库一次性交给代理。"
Context: 选型清单（花渡）：日常补全小修→IDE 派（Antigravity）或终端派（Codex CLI/Gemini CLI）；免费尝鲜→Gemini CLI（个人号额度明确）；多模型协作→Antigravity 可给不同 agent 指定不同模型。
Confidence: high

### G3. 读榜方法论：Verified 当"档位过滤器"，SEAL 标准化 + 私集做采购依据

Claim: DigitalApplied 的采购建议：SWE-bench Verified 成绩只当"通过/淘汰"的档位过滤器（>80% 只说明进入"值得评估"区间，不代表 95% 比 88% 在你的代码库上更强——差距多为 scaffold 和记忆而非能力）；采购决策应依赖 SEAL 标准化 SWE-bench Pro + 私有商业子集（唯一对所有模型同一测量方式、任务更接近私有代码工作）。[^42^]
Source: DigitalApplied《SWE-bench in 2026: Benchmarks vs Scaffolding Reality》
URL: https://www.digitalapplied.com/blog/swe-bench-verified-june-2026-benchmark-vs-scaffolding-analysis
Date: 2026-06-16
Excerpt: "A Verified score above ~80% is best read as a tier filter, not a ranking. It tells you a model is in the 'serious candidate' bracket worth evaluating further; it does not reliably tell you that a 95% model will outperform an 88% model on your codebase, because much of the gap is scaffold and memorization rather than capability."
Excerpt 2: "Buy on the standardized and private numbers, not the headline. For purchase decisions, treat SWE-bench Verified as a pass/fail tier filter and lean on SEAL-standardized SWE-bench Pro plus the private-codebase subset"
Context: 2026-06-16 当日 llm-stats 的 Verified 榜 100 个模型中仅 1 个成绩经独立验证（Fable 5 的 95.0%，vals.ai 复测），其余 99 个全是厂商自报——这是"自报生态"最直白的数据。
Confidence: high

### G4. 最终判据：在自己的仓库上跑私有 eval

Claim: 多个独立来源的共同结论：榜单只做初筛（Arena 排名、SEAL 标准化分），最终决策必须用自己的真实任务做评测——用真实 PR/差异/测试与团队规范验证；LMArena 官方也建议用 Side-by-side 模式拿"你工作中的真实问题"实测两款模型再付费。[^9^]
Source: PropelCode；Botnation（LMArena 用法）
URL: https://www.propelcode.ai/blog/lm-arena-coding-leaderboard-insights-for-developers ; https://botnation.ai/en/chatbot-arena/
Date: 2026-05-27 / 2026-07-28
Excerpt: "Use it to shortlist models, then validate against real diffs, comments, tests, and team policy."
Excerpt 2: "Before paying for an AI subscription, run your real work questions through it: the ones from your job, in your own vocabulary. The global ranking matters less than performance on your actual use case"
Context: 与 A2/G3 构成完整方法链：看标准化榜 → Arena 盲测初筛 → 私有仓库 eval → 按任务路由多模型。
Confidence: high

---

## 写给作者的 3–5 个要点（服务第一章"各家对比"）

1. **"约 20 分差距"可以坐实，但要讲清三层口径**。同一模型在 SWE-bench 上至少有三个数字：厂商自报（自家调优 harness，如 Opus 4.8 的 69.2%）、Scale SEAL 标准化（同 scaffold，Opus 4.6 最好 51.9%，榜首 GPT-5.4 59.1%）、第三方复测（vals.ai 等）。差距 17–21 分稳定存在，且 HAL 数据显示换 scaffold 极端可到 34–48 分。书中应教读者"只看同 harness 内的对比"，并把 Verified 当档位过滤器而非排名。另注意 2026 年 2 月 OpenAI 已公开弃用 Verified（污染 + 59.4% 难题测试缺陷），行业重心转向 SWE-bench Pro——第一章对比表建议以"SEAL 标准化 Pro 分 + Terminal-Bench + Arena WebDev"三栏呈现，而非单引 Verified。

2. **"harness > 模型"有论文级量化支撑，可作为全书方法论主线**。arXiv 2605.23950：harness 替换的分数波动 routinely 超过模型代际进步（2–4 分）；仅加一个检索子代理 WarpGrep 就翻转 MiniMax 2.5 与 Opus 4.6 的排名；Cursor 研究显示同模型 46% vs 80%。可操作的 harness 四杠杆：检索（只放相关文件）、上下文管理（compaction/隔离/防 context rot，150K 相关内容后各家都退化）、工具设计（明确的失败态与重试）、子代理架构（噪声隔离 + 并行 + 成本分层）。这也是教读者"先把 harness 修好再换模型"的决策框架。

3. **工具对比要讲"控制模型 + 治理层位 + 有效上下文"三个轴，而非功能清单**。Claude Code（agent-first、应用层 hooks 治理、1M 原生窗口、本地直接执行）vs Codex（云沙箱、内核层 Seatbelt/Landlock 治理、API 1.05M 但客户端仅 400K、超 272K 输入费率 ×2）vs Cursor（IDE-first、标称 200K 实测有效 70–120K、同任务 token 消耗约 5.5–5.7 倍于 Claude Code）。功能清单已高度趋同（24 项相似功能 Claude Code 先发 18 项），差异化叙事应落在"谁驱动、在哪治理、窗口水分多大"。混合使用（Claude 设计 + Codex 执行；Cursor 编辑器 + Claude Code 终端）是 2026 年资深工程师常态。

4. **百万上下文已成标配但"标称 ≠ 有效"，定价要看"每解决一分成本"**。旗舰 API 全面 1M（Opus 5/Sonnet 5/GPT-5.6/Gemini 3.1/GLM-5.2/K3/M3），但产品内窗口普遍缩水，且 150K 真正相关内容后性能退化——检索工程仍不可替代。性价比叙事用 morphllm 的折算：Haiku 4.5 每解决一个 SWE-bench Pro 分约 $0.13，是最便宜路径；DeepSeek V4 Flash $0.14/$0.28 是 token 地板价。

5. **国内 Coding Plan 一章可按"协议兼容性 → 额度机制 → 隐藏坑"结构写**。关键事实：火山方舟是唯一原生 Anthropic 协议（Claude Code 免 proxy），智谱 GLM 客户端覆盖最广（20+）且有 1M 上下文与 $18/月国际版（但高峰 3 倍抵扣倍率最坑、曾涨价 6 倍），MiniMax ¥29 入门最低且重试不扣量，Kimi 唯一 token 计量制（Cache Read 吞额度，实测 ¥49 档周限额≈26 prompts），百炼 2026 改版后仅售 Pro（¥198 起、token 总量制、禁批量自动化调用）。共性风险：超售/高峰降级、退款苛刻、个人用途限制、额度不透明——建议书中给出"先试首月低价档、实测额度消耗再长期订阅"的行动建议。

---

### 附：搜索覆盖说明
本调研共执行 32 次独立搜索（8 批 × 4 查询），覆盖：SWE-bench Verified/Pro 榜单与口径（5）、Scale SEAL 与 harness 差距（3）、Terminal-Bench（2）、LiveCodeBench（1）、LMArena/WebDev（2）、OpenAI 弃用 Verified/污染（2）、harness 工程论文与实践（5）、子代理架构（2）、Claude Code vs Codex（3）、Cursor 横评（2）、Kimi Code（2）、GLM/Z.ai（3）、MiniMax（1）、国内 Coding Plan（4）、上下文窗口（3）、API/订阅定价（3）、选型方法论（3）。未竟事项：① "Scale 榜首 61.5%"的具体月份快照未直接核到（6 月口径为 59.1%），建议出版前查 labs.scale.com/leaderboard 当期值；② Cursor 官方 CursorBench 细节未找到一手页；③ Fable 5 的 80.3% Pro 分为 Anthropic 自报且该模型经历 6/12–7/1 出口管制暂停，书中引用需注明时效。
