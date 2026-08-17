# 维度12 调研报告：AI编程工程化（skill 生态 / 子agent / 上下文工程）与 AI编程常见病治理

调研日期：2026-07-31　|　调研范围：2025–2026 年（重点 2026 年）　|　检索量：约 40 次独立检索（中英混合）+ 4 个一手页面精读

---

## 〇、openspec 与 superpowers 考证结论（先读这里）

**两者均真实存在，且都是 2025Q4–2026 年 GitHub 上最炙手可热的 AI 编程工程化项目，但性质不同：一个是「规范驱动开发（SDD）框架」，一个是「agent 技能（skills）框架 / 方法论」。**

### OpenSpec

- **正式名称 / 仓库**：`Fission-AI/OpenSpec`（GitHub），npm 包 `@fission-ai/openspec`，官方自述「Spec-driven development (SDD) for AI coding assistants」[^1^][^2^]。
- **作者/组织**：Fission AI（开源社区团队；核心维护者之一在 X 上为 @0xTab），TypeScript 实现，MIT 协议[^1^][^3^]。
- **Star 量级**：2026-05 约 45.7k，2026-06 约 55.5k stars（3.9k forks）——**五万级**，2026 年上半年增长迅猛[^2^][^4^]。
- **功能**：为 AI coding 助手提供轻量级「spec 层」——每个变更一个文件夹，内含 proposal、specs、design、tasks 四件套，人类与 AI 在写代码前先就「要建什么」达成一致；通过 `/opsx:propose`、`/opsx:apply`、`/opsx:archive` 等 slash command 驱动，兼容 30+ AI 助手（Claude Code、Cursor、Codex、Copilot 等）[^1^][^5^]。自我定位为 Spec Kit（重型、阶段门）与 Kiro（绑定 IDE/模型）之外的轻量、工具中立选项，强调 brownfield（存量项目）适配[^5^]。
- **置信度：high**（README 一手原文 + 多个第三方独立来源交叉印证）。

### superpowers

- **正式名称 / 仓库**：`obra/superpowers`（GitHub），官方自述「An agentic skills framework & software development methodology that works」[^6^]。市面亦有 `obra/superpowers-skills`（社区技能库）、`obra/superpowers-marketplace`（插件市场）等姊妹仓库[^7^][^8^]。
- **作者**：**Jesse Vincent（GitHub ID: obra）**，知名开源老兵（Keyboardio 创始人，现为 Prime Radiant 团队）。项目创建于 **2025-10-09**，MIT 协议[^9^]。
- **Star 量级（爆发式增长，按时间线）**：2026-03 约 28k → 2026-04 超 147k（单日曾 +1,589 stars，登 GitHub Trending 第二）→ 2026-06 约 224,691 stars / 19,975 forks → 2026-07 超 250k–264k stars。**二十万级，是 2026 年增速最快的开发者工具仓库之一**[^10^][^11^][^9^][^12^]。（注：不同第三方抓取时点不同，书中引用建议写「2026 年 7 月已超过 25 万 stars」并标注抓取日期。）
- **功能**：一套以 Markdown 编写的「技能（skills）」库 + 强制工作流加载器，让 coding agent 自动执行 **brainstorming → writing-plans → (subagent-driven-development / executing-plans) → TDD（红-绿-重构）→ requesting-code-review → finishing-a-development-branch** 的完整工程方法论；14 个可组合 skill（早期约 20+），涵盖 TDD、系统化调试、完成前验证、git worktree、并行子代理调度等[^6^][^13^][^9^]。支持 Claude Code（Anthropic 官方插件市场已收录）、Codex、Cursor、Gemini CLI、OpenCode、GitHub Copilot CLI、Kimi Code 等 8+ harness[^6^][^9^]。
- **与 OpenSpec 的关系**：**互补而非竞争**。OpenSpec/Spec Kit 管「计划工件」（planning artifacts，先写什么），superpowers 管「执行习惯」（execution habits，怎么写：TDD、评审、隔离）。社区常见组合用法「Spec Kit/OpenSpec + Superpowers」[^14^][^15^]。
- **争议**：2026 年中有 Hacker News / 中文社区用户反馈其流程强制过重、token 消耗大、「装了之后 Claude 反而犯更多错」；维护者曾把 14 个 skill 的代码从 3150 行砍到 977 行（-69%）以缓解上下文占用[^16^][^17^]。著名成功案例：chardet v7 重写（5 天完成、性能提升最高 48 倍）[^18^]。
- **置信度：high**（README 一手原文 + 多来源时间线互相印证；star 精确数字以抓取时点为准）。

---

## 一、Spec 驱动开发（SDD）：先规划后编码的工作流

Claim: Spec-Driven Development（SDD）是 2025–2026 年确立的方法论范式——规格说明（spec）取代代码成为「唯一事实来源」，开发流程从「编码→测试→修复」重构为「规范→设计→实现→验证」；微软开发者博客将其生命周期概括为 Constitution → Specify → Clarify → Plan → Tasks → Implement → Validate 七步。[^19^][^20^]
Source: Microsoft Developer Blog「A Spec-First Approach to AI-Native Engineering」
URL: https://developer.microsoft.com/blog/spec-driven-development-ai-native-engineering/
Date: 2026-06-10
Excerpt: "GitHub Spec Kit is the toolkit that helps teams put SDD into practice... The lifecycle is simple: define intent, remove ambiguity, plan with constraints, implement with AI, and validate against the spec."
Context: 微软官方博客，系统阐述 SDD 理念并推介 GitHub Spec Kit。
Confidence: high

Claim: OpenSpec 的核心价值主张是「在写任何代码之前，人与 AI 先就规格达成一致」，每个变更拥有独立文件夹（proposal/specs/design/tasks），且不设刚性阶段门、可随时更新任何工件。[^5^]
Source: Fission-AI/OpenSpec GitHub README（一手原文）
URL: https://github.com/Fission-AI/OpenSpec
Date: 抓取于 2026-07-31
Excerpt: "AI coding assistants are powerful but unpredictable when requirements live only in chat history. OpenSpec adds a lightweight spec layer so you agree on what to build before any code is written. ... **Agree before you build** ... **Work fluidly** — update any artifact anytime, no rigid phase gates"
Context: 一手 README。README 中演示工作流：`/opsx:explore` → `/opsx:propose add-dark-mode`（生成 proposal.md、specs/、design.md、tasks.md）→ `/opsx:apply` → `/opsx:archive`。
Confidence: high

Claim: OpenSpec 官方 README 直接给出与竞品的对比定位：比 Spec Kit 更轻、无刚性阶段门；比 Kiro 更开放、不锁定 IDE 与模型。[^5^]
Source: Fission-AI/OpenSpec GitHub README（一手原文）
URL: https://github.com/Fission-AI/OpenSpec
Date: 抓取于 2026-07-31
Excerpt: "**vs. Spec Kit** (GitHub) — Thorough but heavyweight. Rigid phase gates, lots of Markdown, Python setup. OpenSpec is lighter and lets you iterate freely. **vs. Kiro** (AWS) — Powerful but you're locked into their IDE and limited to Claude models."
Context: 一手 README「How we compare」小节；2026 年 7 月版宣称支持 30+ AI 助手。
Confidence: high

Claim: OpenSpec 的 README 明确把「上下文卫生（context hygiene）」写进使用须知：建议开始实现前清空上下文窗口，并推荐高推理模型（2026-07 版推荐 Codex 5.5 / Opus 4.7）。[^5^]
Source: Fission-AI/OpenSpec GitHub README（一手原文）
URL: https://github.com/Fission-AI/OpenSpec
Date: 抓取于 2026-07-31
Excerpt: "**Context hygiene**: OpenSpec benefits from a clean context window. Clear your context before starting implementation and maintain good context hygiene throughout your session."
Context: 一手 README「Usage Notes」——SDD 工具本身已将上下文工程列为最佳实践。
Confidence: high

Claim: GitHub Spec Kit（github/spec-kit）是 GitHub 官方出品的 SDD 工具包，2025-08-21 创建，Python 实现、MIT 协议，2026 年 6 月达约 111k stars / 9.8k forks，支持 30+ AI coding agent 集成；核心工作流为 `/speckit.constitution` → `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`。[^21^][^22^][^23^]
Source: github/spec-kit README（一手）+ Ry Walker Research + 博客园
URL: https://github.com/github/spec-kit ; https://rywalker.com/research/github-spec-kit ; https://www.cnblogs.com/zhang-yd/p/20316928
Date: README 抓取于 2026-07-31；统计数据 2026-06
Excerpt: "Spec-Driven Development **flips the script** on traditional software development... **specifications become executable**, directly generating working implementations rather than just guiding them."
Context: README 一手原文；star 数据来自第三方时序跟踪（2026-02 约 71k → 2026-04 约 92k → 2026-06 约 111k）。
Confidence: high

Claim: Kiro 是 AWS 出品的 agentic IDE，2025 年 7 月预览、2025 年 11 月 GA（预览期超 25 万开发者），以 SDD 为默认工作流：由 prompt 依次生成 requirements.md（EARS 记法验收标准）、design.md、tasks.md，每阶段有人工批准门，再由并行 agent 执行；配套 steering files、agent hooks（PreToolUse 可阻断）、Powers（按需加载 MCP）。[^24^][^25^]
Source: effloow.com（深度评测）+ byteiota.com
URL: https://effloow.com/articles/aws-kiro-spec-driven-development-ide-scout-2026 ; https://byteiota.com/aws-kiro-replaces-amazon-q-developer-spec-driven-ide/
Date: 2026-07-20 / 2026-05-14
Excerpt: "The core design principle: **specs are the source of truth, and code is a build artifact derived from them.**"
Context: Kiro 是 Amazon Q Developer 的继任者（Q Developer 2026-05-15 停止新注册，2027-04-30 终止支持，新模型仅上 Kiro）。
Confidence: high

Claim: SDD 工具生态 2026 年已形成清晰分工并被社区组合使用：Spec Kit（重生命周期治理、greenfield/合规场景）、OpenSpec（轻量、brownfield/快速迭代）、Superpowers（执行方法论，与前两者互补而非竞争）；Thoughtworks 技术雷达已将 Spec Kit 列入 Assess 环。[^15^][^14^][^26^]
Source: spec-coding.dev（中文对比）+ vibecoding.app + skillhub.brabrix.com（Spec Kit 月报）
URL: https://spec-coding.dev/zh/blog/spec-driven-development-tools-openspec-spec-kit-superpowers ; https://vibecoding.app/blog/spec-kit-review ; https://skillhub.brabrix.com/items/newsletters-2026-april
Date: 2026-05-11 / 2026-07-09 / 2026-05-16
Excerpt: "**Spec Kit is an artifact scaffold.** ... **Superpowers is a behavioral methodology.** ... That difference is why they stack cleanly instead of competing"
Context: 多个独立对比文章一致认为「Spec Kit/OpenSpec 二选一 + Superpowers 叠加」是主流组合；中文社区（6xyun.cn）亦给出相同的决策树。
Confidence: high

Claim: SDD 亦有公开批评声音：Spec Kit 仓库讨论区有用户直言「SpecKit creates the illusion of work」（spec 阶段制造了「工作的工作」）；评测普遍建议小改动、探索性工作不要套用重型 spec 流程。[^22^][^27^]
Source: Ry Walker Research 引 github/spec-kit Discussion #1784；vibecoding.app Spec Kit Review
URL: https://rywalker.com/research/github-spec-kit ; https://vibecoding.app/blog/spec-kit-review
Date: 2026-06 / 2026-07-09
Excerpt: "The countervailing signal is real, vocal user pushback that the spec phase generates work about work — a critique GitHub itself hosts on its discussion board."
Context: 书中介绍 SDD 时应平衡呈现「纪律 vs 仪式开销」之争。
Confidence: medium-high

---

## 二、superpowers 与 skill 生态详考

Claim: superpowers 是一套「完整的软件开发方法论」，构建在一组可组合 skills 与「确保 agent 使用它们」的初始指令之上；agent 从启动起就不直接写代码，而是先追问需求、分块展示设计、生成细到「没有判断力的初级工程师也能执行」的实现计划，然后启动 subagent-driven-development 自主工作数小时。[^6^]
Source: obra/superpowers GitHub README（一手原文）
URL: https://github.com/obra/superpowers
Date: 抓取于 2026-07-31
Excerpt: "Superpowers is a complete software development methodology for your coding agents, built on top of a set of composable skills and some initial instructions that make sure your agent uses them. ... it launches a _subagent-driven-development_ process, having agents work through each engineering task, inspecting and reviewing their work"
Context: 一手 README「How it works」。README 同时列出 7 步基础工作流（brainstorming → using-git-worktrees → writing-plans → subagent-driven-development/executing-plans → TDD → requesting-code-review → finishing-a-development-branch），并强调「Mandatory workflows, not suggestions」。
Confidence: high

Claim: superpowers 的 skill 库覆盖四大域：Testing（test-driven-development）、Debugging（systematic-debugging、verification-before-completion）、Collaboration（brainstorming、writing-plans、executing-plans、dispatching-parallel-agents、code-review、git-worktrees、subagent-driven-development 等）、Meta（writing-skills、using-superpowers）。[^6^][^13^]
Source: obra/superpowers README（一手）+ kyle.pericak.com（实装体验）
URL: https://github.com/obra/superpowers ; https://kyle.pericak.com/exploring-claude-plugin-obra-superpowers.html
Date: README 抓取 2026-07-31；博客 2026-05-09
Excerpt: "**test-driven-development** has a rule: 'NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.' If the agent writes code before the test, the skill instructs it to delete the code, not adapt it."
Context: 第三方实装文章记录了「using-superpowers」加载器 skill 的激进措辞（"If you think there is even a 1% chance a skill might apply... you ABSOLUTELY MUST invoke the skill"），这是其「自动触发」机制的关键。
Confidence: high

Claim: superpowers 作者 Jesse Vincent（obra）是 30 年开源老兵（Keyboardio 创始人），2025 年 10 月 9 日发布项目，以「methodology-as-code」定位；2026 年 6 月仓库达 224,691 stars / 19,975 forks，最新 release v5.1.0（2026-05-04），已进入 Anthropic 官方 Claude 插件市场及其他 7 个 harness 的分发渠道。[^9^]
Source: Ry Walker Research「Superpowers Skills Framework」
URL: https://rywalker.com/research/superpowers-skills-framework
Date: 2026-06（页面首更 2026-02-22）
Excerpt: "Superpowers is a **methodology-as-code** for AI coding agents by Jesse Vincent (@obra, founder of Keyboardio). ... As of June 2026 the repo has 224,691 stars and 19,975 forks on GitHub — roughly 4x its February 2026 count"
Context: 第三方系统考证，给出作者、创建日期（2025-10-09）、版本节奏与分发渠道（Claude Code、Codex CLI/App、Factory Droid、Gemini CLI、OpenCode、Cursor、GitHub Copilot CLI）。
Confidence: high

Claim: superpowers 已被 Anthropic 官方插件市场收录（`/plugin install superpowers@claude-plugins-official`），同时支持 Antigravity、Codex App/CLI、Cursor、Factory Droid、Gemini CLI、GitHub Copilot CLI、Kimi Code、OpenCode、Pi 等 11 种 harness；README 署名「Superpowers is built by Jesse Vincent and the rest of the folks at Prime Radiant」。[^6^]
Source: obra/superpowers GitHub README（一手原文）
URL: https://github.com/obra/superpowers
Date: 抓取于 2026-07-31
Excerpt: "Give your agent Superpowers: Claude Code, Antigravity, Codex App, Codex CLI, Cursor, Factory Droid, Gemini CLI, GitHub Copilot CLI, Kimi Code, OpenCode, Pi."
Context: 一手 README「Quickstart / Installation」；说明 2026 年 skill 框架已跨工具通用化，不再绑定 Claude Code。
Confidence: high

Claim: superpowers 社区评价两极：Reddit/HN 正面评价「体验完全不同且更好」「理解了它是 AI 编程缺的纪律」；批评者认为其拖慢速度、烧 token，且 14 个 skill 占用上下文会分散 agent 注意力——维护者为此将 skill 代码从 3150 行砍至 977 行。[^17^][^18^][^16^]
Source: 掘金「曾经人手一个的Superpowers，为什么现在都在卸」+ CSDN「Superpowers：给 Claude Code 装上工程大脑」
URL: https://juejin.cn/post/7662691781214437412 ; https://blog.csdn.net/lihui49/article/details/162037707
Date: 2026-07-15 / 2026-06-16
Excerpt: "有个Hacker News用户的评论让我印象特别深，他说「I personally don't like superpowers very much... I think Claude makes more mistakes when using superpowers than when not」。... 维护者自己也意识到了这个问题。后来专门做了一次大优化，把14个skill的代码从3150行砍到了977行，砍掉了69%。"
Context: 中文社区 2026 年 7 月的「卸载潮」讨论，是书中呈现「skill 框架代价」的好素材；另一 HN 批评原文：「Superpowers was really just slowing things down and burning more tokens than vanilla」。
Confidence: medium-high（HN 评论为转引，建议书中引用时注明出处层级）

Claim: superpowers 最著名实战案例是 chardet v7 重写：维护者 Dan Blanchard 用 Claude Code + Superpowers 在不访问旧源码树的情况下 5 天完成字符编码检测库重写，性能最高提升 48 倍，与旧版代码重叠仅 1.29%，并借机将许可证从 LGPL 改为 0BSD。[^18^]
Source: CSDN「Superpowers：给 Claude Code 装上工程大脑」
URL: https://blog.csdn.net/lihui49/article/details/162037707
Date: 2026-06-16
Excerpt: "项目维护者 Dan Blanchard 使用 Claude Code + Superpowers 进行完全重写... 仅用 5 天完成整个重写... 性能最高提升 48 倍... 代码相似度分析显示与旧版本仅有 1.29% 的重叠"
Context: 该案例同时引发「AI 重写能否合法换许可证」的社区讨论，可作书中争议案例。
Confidence: medium-high

Claim: Anthropic 官方对 Skills 的工程规范：SKILL.md 主体保持 500 行以内、命名用动名词（如 processing-pdfs）、描述同时说明「做什么+何时用」、长参考材料拆分到独立文件按需加载（渐进式披露）；skill 与 CLAUDE.md 的本质区别是「延迟加载」——不调用不进上下文。[^28^][^29^]
Source: 01.me 整理的 Anthropic Context Engineering 演讲 + duotach.com（引官方 skills 文档）
URL: https://01.me/2025/12/context-engineering-from-claude/ ; https://duotach.com/en/blog/subagentes-claude-code
Date: 2025-12-20 / 2026-07-19
Excerpt: "The key difference with `CLAUDE.md` is **deferred loading**: CLAUDE.md content enters the context every session, while a skill's body loads only when used. In the official doc's words: 'long reference material costs almost nothing until it is needed'."
Context: 官方 skills 文档给出的创建判据：当你反复向聊天粘贴同一多步流程，或 CLAUDE.md 某段从「事实」变成「流程」时，就该建 skill。
Confidence: high

Claim: 社区技能生态已分层：除 superpowers 主仓库外，存在 obra/superpowers-skills（社区可编辑技能库，context7 信任分 9.5、824 个代码片段）与 superpowers-lab（实验性 skill 孵化仓）。[^7^][^11^]
Source: context7.com + agentconn.com
URL: https://context7.com/obra/superpowers-skills ; https://agentconn.com/blog/obra-superpowers-agentic-skills-framework-guide/
Date: 2026-06-09 / 2026-04-11
Excerpt: "A community-editable skills library for Claude Code's superpowers plugin that provides reusable... Trust Score: 9.5"
Context: 可作为「skill 生态」小节的生态图谱素材。
Confidence: medium-high

---

## 三、子 agent（subagent）模式与多 agent 编排

Claim: Claude Code 的 subagent 是带 YAML frontmatter（name/description/tools/model）的 Markdown 文件，存放于 `.claude/agents/`（项目级）或 `~/.claude/agents/`（用户级）；每个 subagent 拥有独立上下文窗口、独立系统提示、可限制工具权限与模型；`description` 字段就是自动委派触发器。[^30^][^31^]
Source: Claude Code 官方文档（zh-CN「创建自定义subagents」）
URL: https://code.claude.com/docs/zh-CN/sub-agents
Date: 2026-07-16（文档更新日）
Excerpt: "Subagents 是带有 YAML frontmatter 的 Markdown 文件。... Claude 使用每个 subagent 的描述来决定何时委托任务。创建 subagent 时，请编写清晰的描述，以便 Claude 知道何时使用它。Claude Code 包括几个内置 subagents，如 Explore、Plan 和 general-purpose。"
Context: 官方一手文档。另记载：自 v2.1.198 起 `/agents` 命令不再打开交互式创建向导；v2.1.63 起 Task 工具更名为 Agent；可用 `Agent(agent_type)` 白名单语法限制可生成的子代理类型。
Confidence: high

Claim: Claude Code 内置 subagent 的设计本身就体现上下文工程：Explore（只读探索）和 Plan（规划研究）会跳过主会话的 CLAUDE.md 与 git status，以保持研究「快速且经济高效」；自定义 subagent 则完整加载两者。[^31^]
Source: Claude Code 官方文档（zh-TW 版措辞更完整）
URL: https://code.claude.com/docs/zh-TW/sub-agents
Date: 2026-07-16
Excerpt: "Explore 和 Plan 會跳過您的 CLAUDE.md 檔案和父工作階段的 git status，以保持研究快速且經濟高效。其他所有內建和 自訂 subagent 都會載入兩者。"
Context: 官方文档对「什么进入子代理上下文」的精细控制，是书中讲 subagent 与上下文隔离关系的一手依据。
Confidence: high

Claim: subagent 的三大工程属性是隔离（独立上下文窗口）、单一职责（完成即返回、上下文即弃）、并行（主会话可同时派发多个子代理）；代价是 token 消耗——subagent 密集型工作流可达单线程会话约 7 倍 token。[^32^]
Source: Nimbalyst Blog「Claude Code Subagents: A Practical 2026 Guide」
URL: https://nimbalyst.com/blog/claude-code-subagents-guide/
Date: 2026-05-05
Excerpt: "subagent-heavy workflows can use roughly 7 times the tokens of a single-thread session because each subagent maintains its own context."
Context: 2026 年实践指南，区分了 subagent（单会话内的工人）与 Agent Teams（跨会话编排，带消息传递）的适用边界。
Confidence: high

Claim: 工程团队使用 subagent 的治理共识：从「一个主 agent + 少量专职 subagent」起步（如 code reviewer 只给 Read/Grep/Glob，不给 Write/Edit），权限最小化，「减少瓶颈而不是让工作流变得戏剧化」。[^33^][^34^]
Source: developersdigest.tech「The 2026 Playbook」+ blog.laozhang.ai（安全模板）
URL: https://www.developersdigest.tech/blog/claude-code-agent-teams-subagents-2026 ; https://blog.laozhang.ai/en/posts/claude-code-subagents-documentation
Date: 2026-05-02 / 2026-05-19
Excerpt: "Most tasks do not need five agents. Start with one main agent and add specialists only when context separation provides clear value. ... The goal is reducing bottlenecks, not making workflows theatrical."
Context: 后者给出「刻意保守」的只读 review subagent 模板（maxTurns: 8、禁止 Write/Edit/Bash），适合书中作为落地示例。
Confidence: high

Claim: Anthropic 官方把「sub-agent 架构」列为长任务上下文工程三大技术之一：子代理可以消耗数万 token 深度探索，但只向主代理返回 1,000–2,000 token 的蒸馏摘要，实现关注点分离。[^35^]
Source: Anthropic Engineering Blog「Effective context engineering for AI agents」（一手原文）
URL: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
Date: 2025-09（发布；抓取 2026-07-31）
Excerpt: "Each subagent might explore extensively, using tens of thousands of tokens or more, but returns only a condensed, distilled summary of its work (often 1,000-2,000 tokens)."
Context: Anthropic Applied AI 团队署名文章，发布一周获约 50 万阅读（据 Towards AI 转述）。
Confidence: high

Claim: Anthropic 对长周期编码 agent 的官方解法是「harness」模式：initializer agent 首次运行搭建环境（feature 清单、git 仓库、进度文件），coding agent 每个会话做增量推进并留下清晰工件供下一班「交接」——类比「没有记忆的换班工程师」。[^36^][^37^]
Source: Anthropic Engineering Blog「Effective harnesses for long-running agents」（CSDN 全文转译）
URL: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
Date: 2025-11-26
Excerpt: "The core challenge of long-running agents is that they must work in discrete sessions, and each new session begins with no memory of what came before. Imagine a software project staffed by engineers working in shifts, where each new engineer arrives with no memory of what happened on the previous shift."
Context: 该文同时坦承未解问题：单一通用 coding agent 与多 agent 架构（测试 agent、QA agent、代码清理 agent）孰优尚无定论。ZenML 案例库记录：即使 Opus 4.5，在多会话下只靠高层 prompt 也无法完成生产级应用，harness 工件是成败关键。
Confidence: high

Claim: 中国厂商同方向实践：月之暗面 Kimi K2.5 的 Agent Swarm 允许主代理统一协调最多 100 个并行子代理（各自独立执行搜索/生成/分析），官方宣称在大型研究、长文创作等场景任务时间缩短至单代理的 1/4.5；子代理的生成、分配与结果整合由模型自身完成而非外部调度框架。[^38^]
Source: aimodeling.com（Kimi K2.5 Agent Swarm 报道）
URL: https://www.aimodeling.com/news/a9e4bd12-171c-47d3-8ecd-2c532aac9daf
Date: 2026-05-14
Excerpt: "Agent Swarm的核心创新在于将任务进行智能切分，由主代理（Kimi K2.5）统一协调，根据任务性质动态分配给子代理池，实现真正的并行处理。根据官方披露，Agent Swarm在大型研究、长篇内容创作、批量下载等场景中，可将任务执行时间缩短至传统单代理模式的1/4.5"
Context: 中文来源转述官方口径；「1/4.5」为官方宣称值，书中引用建议注明「据官方披露」。
Confidence: medium-high

Claim: 社区已有规模化 subagent 集合生态（如 awesome-claude-code-subagents 收录 100+ 社区 subagent），好 subagent 的标准被总结为「职责单一、描述清晰、权限恰当」。[^39^]
Source: 掘金「5 分钟上手 Claude 自定义 Subagents」
URL: https://juejin.cn/post/7618884137738797110
Date: 2026-03-20
Excerpt: "记住：好的 Subagent 是职责单一、描述清晰、权限恰当的。"
Context: 中文社区实践总结；Anthropic 演讲资料亦建议在 description 中使用「PROACTIVELY」「MUST BE USED」字样鼓励自动委派（01.me 整理）。
Confidence: medium-high

---

## 四、上下文工程（context engineering）

Claim: Anthropic 官方定义：上下文工程是「在 LLM 推理过程中策划并维持最优 token 集合的策略全集」；核心原则是「找到尽可能小的高信号 token 集合，使期望结果概率最大化」——上下文是有限资源，每个新 token 都在消耗模型的「注意力预算」。[^35^]
Source: Anthropic Engineering Blog「Effective context engineering for AI agents」（一手原文）
URL: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
Date: 2025-09（抓取 2026-07-31）
Excerpt: "**Context engineering** refers to the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference... good context engineering means finding the _smallest possible_ set of high-signal tokens that maximize the likelihood of some desired outcome."
Context: 业界公认的「上下文工程」纲领性文献，发布一周内约 50 万阅读（Towards AI 转述）。
Confidence: high

Claim: Anthropic 官方确认「context rot（上下文腐烂）」客观存在：随上下文窗口 token 数增加，模型准确回忆信息的能力下降，且该特性「出现在所有模型中」；原因是 Transformer n² 注意力对随长度被摊薄，模型对长程依赖的训练经验也更少。[^35^]
Source: Anthropic Engineering Blog（一手原文）
URL: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
Date: 2025-09
Excerpt: "Studies on needle-in-a-haystack-style benchmarking have uncovered the concept of context rot: as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases. While some models exhibit more gentle degradation than others, this characteristic emerges across all models."
Context: 官方一手；可与 Chroma 的独立实验互证。
Confidence: high

Claim: Chroma Research 的 Context Rot 研究测试 18 个前沿模型（GPT/Claude/Gemini/Qwen/Llama 全系列），结论「无一例外」：所有模型随输入长度增加持续退化；三大机制为 Lost in the Middle（中间位置准确率降 30%+）、注意力稀释、语义相近干扰物的主动误导；工程界据此提出「生产有效上下文 ≈ 广告窗口的 25–30%」的经验法则。[^40^][^41^]
Source: 掘金「1M上下就好么？Claude Code的上下文设置分析」+ 掘金「Token 成本优化实战」（引 Chroma 报告原文）
URL: https://juejin.cn/post/7663105530873266212 ; https://juejin.cn/post/7658074717572153387
Date: 2026-07-17 / 2026-07-03
Excerpt: "Chroma Research 在 2025 年测试了 18 个前沿模型（覆盖 GPT、Claude、Gemini、Qwen、Llama 全系列），得出一个无例外的结论：每个模型都随输入长度增加而持续退化，没有任何例外。"
Context: 中文技术社区对 Chroma 报告的系统转述；含 RULER 基准的「有效窗口」量化表（1M 窗口硬任务建议 250–350K）。
Confidence: medium-high（中文二手转述，但所引为一手研究报告；建议书中引用 Chroma 原始报告）

Claim: Anthropic 给出的长任务三大上下文技术——Compaction（近上限时摘要历史并重开窗口，Claude Code 保留架构决策与未解 bug、丢弃冗余工具输出）、Structured note-taking（agent 把笔记持久化到窗口外，如 NOTES.md/记忆工具）、Sub-agent 架构；并指出 Claude Code 采用「CLAUDE.md 前置 + glob/grep 即时检索」的混合策略。[^35^]
Source: Anthropic Engineering Blog（一手原文）
URL: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
Date: 2025-09
Excerpt: "To enable agents to work effectively across extended time horizons, we've developed a few techniques that address these context pollution constraints directly: compaction, structured note-taking, and multi-agent architectures. ... Claude Code is an agent that employs this hybrid model: CLAUDE.md files are naively dropped into context up front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time"
Context: 一手原文，「just-in-time retrieval / 渐进式披露」概念出处。
Confidence: high

Claim: Claude Code 的双记忆系统（2026 现状）：CLAUDE.md（人写的指令与规则，每会话全量加载）+ Auto Memory（Claude 自写的经验笔记，v2.1.59 起默认开启，`MEMORY.md` 每会话仅加载前 200 行或 25KB，细则拆到 topic files 按需读取）；CLAUDE.md 是「上下文而非强制配置」，要硬约束须用 hook。[^42^][^43^]
Source: Claude Code 官方文档「How Claude remembers your project」（一手）
URL: https://code.claude.com/docs/en/memory
Date: 2026-07-22
Excerpt: "Claude Code has two complementary memory systems. Both are loaded at the start of every conversation. Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead."
Context: 官方一手文档；中文社区（JavaGuide 2026-07-07）据此总结「规则人写、经验 Claude 记、MEMORY.md 只做索引」的用法分层。
Confidence: high

Claim: CLAUDE.md 最佳实践共识：写构建/测试命令、代码风格、「不要做什么」；保持 200–500 行（官方建议越短遵守度越高）；用命令式语气；分层加载（`~/.claude/CLAUDE.md` 全局 + 项目根 + 子目录叠加继承）；随项目演进定期删改。[^44^]
Source: agent-interview-hub「Context Engineering 上下文工程」（GitHub）
URL: https://github.com/Zchary1106/agent-interview-hub/blob/main/通用知识/Context%20Engineering上下文工程.md
Date: 2026-04-09
Excerpt: "**保持简洁**：CLAUDE.md 每次对话都会被加载，内容过长会浪费 Token。200-500 行是推荐范围 ... **用命令式语气**：`使用 pnpm 而非 npm` 比 `我们的项目使用 pnpm` 更清晰"
Context: 中文社区整理的分层加载机制（全局/项目/子目录叠加）与写作规范；官方文档佐证「shorter files produce better adherence」。
Confidence: medium-high

Claim: AGENTS.md 已成为跨工具的开放标准（Linux Foundation 旗下 Agentic AI Foundation 托管）：一个仓库根目录的 Markdown 文件，「README for AI agents」，被超 60,000 个开源项目采用，Codex、Jules、Cursor、Copilot、Claude Code（fallback/导入）等均支持；实践建议是「核心规则写 AGENTS.md，工具特有指令保留 CLAUDE.md 等适配文件」。[^45^][^46^]
Source: vibecoding.app「AGENTS.md Review」+ deployhq.com 配置指南
URL: https://vibecoding.app/blog/agents-md-review ; https://www.deployhq.com/blog/ai-coding-config-files-guide
Date: 2026-03-18 / 2026-06-12
Excerpt: "The standard is stewarded by the Agentic AI Foundation under the Linux Foundation... It has been adopted by over 60,000 repositories on GitHub, including projects from OpenAI, Apache Airflow, and Temporal."
Context: 2025-08 发布的格式；deployhq 给出 CLAUDE.md / AGENTS.md / copilot-instructions.md 三者的加载范围、层级与大小限制对照表。
Confidence: high

Claim: 指令文件本身也会「生病」：2026 年 6 月一项对 100 个热门仓库的预印本研究归纳出六类 instruction-file 配置「坏味道」——lint 泄漏 62%、上下文膨胀 42%、skill 泄漏 35%；KyenAI 抽样显示 62–68% 的 AGENTS.md/CLAUDE.md 缺少安全/批准规则，53–58% 缺少验证/完成标准。[^47^]
Source: kyenai.com「AGENTS.md vs CLAUDE.md ...」（引用 arXiv 预印本）
URL: https://www.kyenai.com/guides/agents-md-vs-claude-md-cursorrules-copilot-instructions
Date: 2026-06-14
Excerpt: "A separate June 2026 preprint analyzed 100 popular repositories and cataloged six instruction-file configuration smells. It reported lint leakage in 62% of files, context bloat in 42%, and skill leakage in 35%."
Context: 说明「写了上下文文件 ≠ 写好」——文档混乱同样会污染 agent 上下文，直接呼应「文档混乱」病症。
Confidence: medium-high

---

## 五、AI 编程常见病与治理

### 5.1 病症：代码质量与技术债

Claim: 大规模实证研究（arXiv 2026-04，30.26 万个 AI 署名 commit、6,299 个 GitHub 仓库）证实 AI 助手把技术债带进了真实生产仓库：五种工具全部中招、超过 15% 的 commit 引入至少一个可检测问题；code smell 是最常见类型；存活的 AI 引入问题累计数到 2026 年 2 月已超 10 万。[^48^]
Source: arXiv「Debt Behind the AI Boom: A Large-Scale Empirical Study of AI-Generated Code in the Wild」
URL: https://arxiv.org/html/2603.28592v2
Date: 2026-04-26
Excerpt: "We observed that across all five tools we studied, more than 15% of commits introduce at least one detectable issue... Figure 9 shows that the cumulative number of surviving AI-introduced issues continues to rise over time, exceeding 100k by February 2026."
Context: 学术论文一手；作者指出开发者对 AI 建议的「过度信任」导致问题在评审中被放过并长期累积。
Confidence: high

Claim: GitClear 等机构数据勾勒出「代码霉变」机制：AI 倾向内联逻辑而非抽取函数（函数调用率下降 35%）、复制粘贴式生成激增（代码克隆 4 倍增长、重构活动下降 60%）；AI 的默认策略被概括为「永远不要抛出错误」——悄悄吞掉异常、代码「能跑」但隐患潜伏。[^49^][^50^]
Source: deepseek.csdn.net 引 GitClear / LeadDev + particula.tech
URL: https://deepseek.csdn.net/6a544b02662f9a54cb8ebb3b.html ; https://particula.tech/blog/ai-coding-tools-developer-productivity-paradox
Date: 2026-07-13 / 2026-03-13
Excerpt: "GitClear 把这种现象叫做「代码霉变」（Code Churn without Refactoring）... 函数调用率下降了 35%，意味着 AI 更倾向于在函数内"内联"逻辑，而不是把公共逻辑抽成可复用的函数。"
Context: 中文长文综合 GitClear（2.11 亿行代码分析）、LeadDev（2026-07「Code maintainability plummets in the AI coding era」）等来源。
Confidence: medium-high（GitClear 数据被多方引用，建议书中回溯 GitClear 原始报告）

Claim: 行业基准显示 AI 代码在评审与安全维度显著更差：Opsera 2026 基准称 AI 生成 PR 接受率 32.7%（人类 84.4%）、bug 多 1.7 倍、安全漏洞多 15–18%；另一组数据称 AI 生成代码漏洞率为人类 2.74 倍、PR 平均问题数 10.83 对 6.45。[^50^][^51^]
Source: particula.tech + unyform.ai（引 Veracode/IEEE Spectrum 等）
URL: https://particula.tech/blog/ai-coding-tools-developer-productivity-paradox ; https://unyform.ai/ai-coding-tools-enterprise-problems
Date: 2026-03-13 / 2026-03-15
Excerpt: "AI-generated pull requests have a **32.7% acceptance rate** compared to 84.4% for human-written code. ... AI code has 1.7x more bugs and 15–18% more security vulnerabilities."
Context: 二手引用 Opsera/Veracode 数据；量级可信但建议书中标注原始出处。
Confidence: medium

Claim: 「感知-现实落差」是 AI 编程效率的标志性研究：METR 随机对照试验（16 名资深开源维护者、246 个真实任务）发现使用 AI 工具任务耗时增加 19%，而开发者事前预测快 24%、事后仍自认快 20%——39 个百分点的感知偏差。[^52^]
Source: METR 官方博客 + byteiota 解读
URL: https://metr.org/blog/2026-02-24-uplift-update/ ; https://byteiota.com/ai-coding-tools-made-developers-19-slower-metr-study/
Date: 2025-07（原始研究）/ 2026-02-24（官方更新）
Excerpt: "Our early 2025 study found the use of AI causes tasks to take 19% longer, with a confidence interval between +2% and +39%."
Context: METR 2026-02 官方更新承认后续实验因「开发者不愿在无 AI 条件下工作」产生严重选择偏差，并认为 2026 年初 AI 的真实加速效果可能已转正——书中应同时呈现这两层信息。
Confidence: high

Claim: 学术界提出「三重债务模型」：AI 生成代码的速度超过团队理解速度时，除技术债外还积累「认知债」（团队共享心智模型的腐化）与「意图债」（设计理由、目标、约束未外化，人类与 agent 都无法安全演进系统）。[^53^]
Source: arXiv「From Technical Debt to Cognitive and Intent Debt」（Margaret-Anne Storey 等）
URL: https://arxiv.org/abs/2603.22106
Date: 2026-03-23
Excerpt: "As AI generates code faster than teams can understand it, two under appreciated forms of debt accumulate: cognitive debt, the erosion of shared understanding across a team, and intent debt, the absence of externalized rationale that developers and AI agents need to work safely with code."
Context: 「文档混乱」「架构越来越乱」两大病症的理论化表述——意图债正是 spec/ADR/steering files 要偿还的对象。
Confidence: high

### 5.2 病症：上下文丢失（及对策）

Claim: 上下文丢失的四大生产级对策已成共识：Compaction（摘要压缩）、Observation masking（隐藏旧工具输出）、Just-in-time retrieval（轻量索引 + 按需加载）、Sub-agent delegation（子代理返回 1–2k token 摘要）。[^54^]
Source: 掘金「为什么你的 AI 智能体上了生产就翻车？十二个模块」
URL: https://juejin.cn/post/7633640076662128680
Date: 2026-04-28
Excerpt: "**压缩（Compaction）**：上下文接近上限时，对对话历史做摘要处理... **即时检索（Just-in-time Retrieval）**：维护轻量级索引，动态加载所需数据。Claude Code 的做法是用 grep、glob、head、tail 命令精准提取内容... **子智能体委派**：把复杂的探索任务拆给子智能体，最终只返回 1000 到 2000 个 Token 的精简摘要"
Context: 中文社区对 Anthropic 上下文工程指南的工程化总结，与一手文献一致。
Confidence: medium-high

Claim: Claude Code 官方最佳实践承认两类高频上下文病症并给出对策——上下文溢出（用 /clear、精简文件集、拆大任务、子目录 CLAUDE.md）与上下文漂移（维护详细 CLAUDE.md、定期重申约束、重要决策后写回记录）。[^55^]
Source: gaccode.store「Claude Code 官方最佳实践指南」
URL: https://gaccode.store/post/claude-code-official-best-practices
Date: 2025-10-22
Excerpt: "**问题 1：上下文溢出（Context Overflow）** 症状：Claude 开始遗忘早期对话内容... **问题 2：上下文漂移（Context Drift）** 症状：Claude 的回答逐渐偏离项目规范或之前的决策。"
Context: 对官方最佳实践的中文系统整理；「上下文漂移」正对应书中「上下文丢失」病症。
Confidence: medium-high

### 5.3 病症：文档混乱与架构腐化（及治理）

Claim: SDD/steering 文件的本质价值是「让决策在会话更替、人员更替和时间流逝后仍可被 agent 读取」：当约束散落在 Slack、Issue 与老员工脑中时，agent 并非「忘记」而是「从未拥有」——这是上下文盲区导致架构级错误的根因。[^56^][^49^]
Source: javatask.dev（Kiro SDD 系列）+ deepseek.csdn.net
URL: https://javatask.dev/blog/agentic-ai-on-aws-spec-driven-development/ ; https://deepseek.csdn.net/6a544b02662f9a54cb8ebb3b.html
Date: 2026-04-29 / 2026-07-13
Excerpt: "The agent did not forget — it never had access in the first place. Spec-driven development is the practice of giving it access: structuring your requirements, design decisions, and task breakdown into files the agent reads as a first-class input at every session. The change is architectural, not cosmetic."
Context: 对「文档混乱 → AI 看不到全局契约 → 架构被破坏」链条的最好一手论述；中文社区实测案例（`role: string → string[]` 改坏下游契约）可作书中故事。
Confidence: high

Claim: 治理手段已形成「组合拳」共识：(1) 文档即代码——spec/steering/CLAUDE.md/AGENTS.md 入库评审、与代码同版本演进；(2) 测试守护——TDD 强制（superpowers 的「无失败测试不得写产品代码」）、hooks 在保存/提交时自动跑测试与 lint；(3) 架构约束——constitution.md、目录结构约定、PreToolUse 阻断；(4) 评审证据链——AI 生成的 PR 必须把每处修改映射回任务与验收标准。[^14^][^25^][^6^]
Source: spec-coding.dev + effloow.com + obra/superpowers README
URL: https://spec-coding.dev/zh/blog/spec-driven-development-tools-openspec-spec-kit-superpowers ; https://effloow.com/articles/aws-kiro-spec-driven-development-ide-scout-2026 ; https://github.com/obra/superpowers
Date: 2026-05 / 2026-07
Excerpt: "如果 AI 生成的 PR 不能把每个修改映射回任务和验收标准，这个 PR 就还没准备好。"
Context: 中文社区将 SDD 三大项目的共性提炼为「artifact 链 + 证据门禁」；Kiro hooks 的 PreToolUse 可阻断机制、superpowers 的 TDD 删除规则均为可引用实例。
Confidence: high

Claim: 评审瓶颈已成新问题：AI 让代码生成提速但评审团队没有扩容——PR 堆积、评审者橡皮图章、含 AI 代码的 PR 平均需要多 1.3 轮评审与 15% 更多评论；70% IT 负责人把治理列为 AI 编程落地前三挑战。[^51^][^57^]
Source: unyform.ai + arxiv 2512.01155（引 Harding/GitClear 2025 分析）
URL: https://unyform.ai/ai-coding-tools-enterprise-problems ; https://www.arxiv.org/pdf/2512.01155v2
Date: 2026-03 / 2025-12
Excerpt: "A 2025 analysis by Harding(GitClear) examining pull requests with AI-generated code found that such PRs required on average 1.3 additional review rounds and 15% more comments from reviewers compared to human-written code, suggesting that velocity gains in writing may be offset by slowdowns in review and validation."
Context: 「瓶颈下移」是书中「代码混乱治理」章节的重要论点：治理成本在评审端而非生成端。
Confidence: medium-high

---

## 六、写给作者的 5 个要点

1. **「openspec」与「superpowers」不是一个量级也不是一类东西，别并列写成「两个 skill 项目」。** OpenSpec（Fission-AI/OpenSpec，~5.5 万 stars）是 SDD 规范层工具；Superpowers（obra/superpowers，Jesse Vincent，2026-07 已超 25 万 stars）才是用户想找的「skill 框架」——它用 14 个 Markdown 技能把 TDD、系统化调试、子代理驱动开发变成强制工作流。正确写法是：Spec Kit / OpenSpec / Kiro 讲「先规划后编码」（planning artifacts），Superpowers 讲「怎么把活干好」（execution habits），两者互补、社区普遍叠加使用。
2. **子 agent 章节的官方骨架直接用 Claude Code 文档**：`.claude/agents/` 下「YAML frontmatter + Markdown 系统提示」的格式、`description` 即委派触发器、工具权限最小化（review 类只给 Read/Grep/Glob）、内置 Explore/Plan 跳过 CLAUDE.md 的上下文节俭设计；再配 Anthropic「子代理返回 1–2k token 蒸馏摘要」的上下文工程定位，以及 Kimi Agent Swarm（100 并行子代理、官方宣称 4.5× 提速）作为中国厂商对照案例。别忘了写代价：subagent 密集工作流约 7 倍 token。
3. **上下文工程有一条清晰的一手文献主线**：Anthropic《Effective context engineering for AI agents》（2025-09，「最小高信号 token 集合」）→ Chroma Context Rot 研究（18 模型无一例外退化，「生产有效上下文 ≈ 标称窗口 25–30%」）→ Claude Code 双记忆（CLAUDE.md 人写规则 + Auto Memory 机器写经验、MEMORY.md 200 行/25KB 索引）→ AGENTS.md 开放标准（Linux Foundation，60k+ 仓库）。书中可用「上下文溢出 / 上下文漂移 / 上下文腐烂」三病分诊的结构。
4. **常见病治理要数据化、且呈现正反两面**：METR RCT（资深开发者慢 19% 却自认快 20%，39 点感知偏差；2026-02 官方自承选择偏差、效果或已转正）、arXiv 30 万 AI commit 研究（>15% commit 引入问题、累计存活问题超 10 万）、GitClear（克隆 4×、重构 -60%、函数调用率 -35%）、「三重债务模型」（技术债/认知债/意图债）。治理组合拳 = spec 工件链（意图债）+ TDD/测试守护 + hooks 硬约束 + 评审证据链（每处修改映射回验收标准）。
5. **务必给「工程化派」配上反面声音，这恰恰是本书面向有经验读者的 credibility 所在**：Spec Kit 讨论区「SpecKit creates the illusion of work」；Superpowers 的 2026 年中「卸载潮」（强制流程拖慢、烧 token、分散注意力，官方被迫把 skill 代码砍掉 69%）；METR 后续研究的自我修正。结论落在「纪律与场景匹配」：greenfield/合规/大团队用重流程，brownfield/快速迭代用 OpenSpec 轻流程，探索性工作保持 vibe。

---

## 引用列表

[^1^]: npm @fission-ai/openspec — https://www.npmjs.com/package/@fission-ai/openspec （2026-07-29 更新）
[^2^]: popaiexplorer「Fission-AI/OpenSpec GitHub」— https://www.popaiexplorer.com/en/projects/Fission-AI/OpenSpec （2026-06-13，55,502 stars / 3,882 forks）
[^3^]: whatisgithub「fission-ai/openspec」— https://whatisgithub.com/fission-ai/openspec （2026-05-18，45,659 stars）
[^4^]: 同 [^2^]
[^5^]: Fission-AI/OpenSpec GitHub README（一手）— https://github.com/Fission-AI/OpenSpec （抓取 2026-07-31）
[^6^]: obra/superpowers GitHub README（一手）— https://github.com/obra/superpowers （抓取 2026-07-31）
[^7^]: context7「Superpowers Skills (obra/superpowers-skills)」— https://context7.com/obra/superpowers-skills （2026-06-09）
[^8^]: obra/superpowers-marketplace GitHub — https://github.com/obra/superpowers-marketplace （2025-10-09）
[^9^]: Ry Walker Research「Superpowers Skills Framework」— https://rywalker.com/research/superpowers-skills-framework （2026-06）
[^10^]: generativeai.pub「7 Claude Code Skills Every Developer Needs in 2026」— https://generativeai.pub/7-claude-code-skills-every-developer-needs-in-2026-52b15ae68685 （2026-03-16，28K stars）
[^11^]: agentconn「obra/superpowers: Claude Code Skills Framework Guide」— https://agentconn.com/blog/obra-superpowers-agentic-skills-framework-guide/ （2026-04-11，147k+ stars）
[^12^]: claudeskills.info「obra 的 superpowers」— https://claudeskills.info/zh/plugins/obra/superpowers/superpowers/ （2026-07-24，263,954 stars / v6.1.1）；另 vibecoding.app 2026-07-09 称「crossed 250,000 GitHub stars」— https://vibecoding.app/blog/spec-kit-review
[^13^]: kyle.pericak.com「Exploring Claude Plugin obra/superpowers」— https://kyle.pericak.com/exploring-claude-plugin-obra-superpowers.html （2026-05-09）
[^14^]: spec-coding.dev「OpenSpec vs Superpowers vs Spec Kit：SDD 实践模式」— https://spec-coding.dev/zh/blog/spec-driven-development-tools-openspec-spec-kit-superpowers （2026-05-11）
[^15^]: vibecoding.app「GitHub Spec Kit Review (2026)」— https://vibecoding.app/blog/spec-kit-review （2026-07-09）
[^16^]: 掘金「曾经人手一个的Superpowers，为什么现在都在卸」— https://juejin.cn/post/7662691781214437412 （2026-07-15）
[^17^]: CSDN「Superpowers：给 Claude Code 装上“工程大脑”」（HN 批评引文）— https://blog.csdn.net/lihui49/article/details/162037707 （2026-06-16）
[^18^]: 同 [^17^]（chardet v7 案例与社区声音）
[^19^]: Microsoft Developer Blog「A Spec-First Approach to AI-Native Engineering」— https://developer.microsoft.com/blog/spec-driven-development-ai-native-engineering/ （2026-06-10）
[^20^]: 博客园「AI规范编程：从SDD理念到Spec-Kit落地实践」— https://www.cnblogs.com/xuxueli/p/20145203 （2026-05-24）
[^21^]: github/spec-kit README（一手）— https://github.com/github/spec-kit （抓取 2026-07-31）
[^22^]: Ry Walker Research「GitHub Spec Kit」— https://rywalker.com/research/github-spec-kit （2026-06，111k stars）
[^23^]: 博客园「今日开源[第7期]spec-kit」— https://www.cnblogs.com/zhang-yd/p/20316928 （2026-06-05，108,392 stars）
[^24^]: effloow.com「AWS Kiro: Spec-Driven IDE for Agentic Development」— https://effloow.com/articles/aws-kiro-spec-driven-development-ide-scout-2026 （2026-07-20）
[^25^]: byteiota.com「AWS Kiro Replaces Amazon Q Developer」— https://byteiota.com/aws-kiro-replaces-amazon-q-developer-spec-driven-ide/ （2026-05-14）
[^26^]: skillhub.brabrix.com「Spec Kit - April 2026 Newsletter」— https://skillhub.brabrix.com/items/newsletters-2026-april （2026-05-16；Thoughtworks Radar / Will Torber 对比推荐 OpenSpec）
[^27^]: github/spec-kit Discussion #1784「SpecKit creates the illusion of work」（经 [^22^] 转引）
[^28^]: 01.me「Claude 的 Context Engineering 秘籍」— https://01.me/2025/12/context-engineering-from-claude/ （2025-12-20，整理自 Anthropic 演讲）
[^29^]: duotach.com「Claude Code Subagents and Skills: Complete Guide [2026]」— https://duotach.com/en/blog/subagentes-claude-code （2026-07-19）
[^30^]: Claude Code Docs（zh-CN）「创建自定义subagents」— https://code.claude.com/docs/zh-CN/sub-agents （2026-07-16）
[^31^]: Claude Code Docs（zh-TW）「建立自訂subagents」— https://code.claude.com/docs/zh-TW/sub-agents （2026-07-16）
[^32^]: Nimbalyst「Claude Code Subagents: A Practical 2026 Guide」— https://nimbalyst.com/blog/claude-code-subagents-guide/ （2026-05-05）
[^33^]: developersdigest.tech「Claude Code Agent Teams, Subagents, and MCP: The 2026 Playbook」— https://www.developersdigest.tech/blog/claude-code-agent-teams-subagents-2026 （2026-05-02）
[^34^]: blog.laozhang.ai「Claude Code Subagents Documentation」— https://blog.laozhang.ai/en/posts/claude-code-subagents-documentation （2026-05-19）
[^35^]: Anthropic Engineering「Effective context engineering for AI agents」（一手）— https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents （2025-09）
[^36^]: Anthropic Engineering「Effective harnesses for long-running agents」（一手，经 CSDN 全文转译）— https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents （2025-11-26）；转译 https://blog.csdn.net/D1237890/article/details/160634723
[^37^]: ZenML LLMOps Database「Long-Running Agent Harness」— https://www.zenml.io/llmops-database/long-running-agent-harness-for-multi-context-software-development
[^38^]: aimodeling.com「Kimi K2.5解锁Agent Swarm」— https://www.aimodeling.com/news/a9e4bd12-171c-47d3-8ecd-2c532aac9daf （2026-05-14）
[^39^]: 掘金「5 分钟上手 Claude 自定义 Subagents」— https://juejin.cn/post/7618884137738797110 （2026-03-20）
[^40^]: 掘金「1M上下就好么？Claude Code的上下文设置分析」— https://juejin.cn/post/7663105530873266212 （2026-07-17）
[^41^]: 掘金「Token 成本优化实战」— https://juejin.cn/post/7658074717572153387 （2026-07-03）
[^42^]: Claude Code Docs「How Claude remembers your project」（一手）— https://code.claude.com/docs/en/memory （2026-07-22）
[^43^]: JavaGuide「Claude Code 记忆系统详解」— https://javaguide.cn/ai-coding/principles/claude-code-memory.html （2026-07-07）
[^44^]: agent-interview-hub「Context Engineering 上下文工程」— https://github.com/Zchary1106/agent-interview-hub （2026-04-09）
[^45^]: vibecoding.app「AGENTS.md Review」— https://vibecoding.app/blog/agents-md-review （2026-03-18）
[^46^]: deployhq.com「CLAUDE.md, AGENTS.md & Copilot Instructions」— https://www.deployhq.com/blog/ai-coding-config-files-guide （2026-06-12）
[^47^]: kyenai.com「AGENTS.md vs CLAUDE.md vs Copilot Instructions」— https://www.kyenai.com/guides/agents-md-vs-claude-md-cursorrules-copilot-instructions （2026-06-14）
[^48^]: arXiv「Debt Behind the AI Boom」— https://arxiv.org/html/2603.28592v2 （2026-04-26）
[^49^]: deepseek.csdn.net「AI 写代码有70%更多Bug」— https://deepseek.csdn.net/6a544b02662f9a54cb8ebb3b.html （2026-07-13）
[^50^]: particula.tech「AI Coding Tools Developer Productivity Paradox」— https://particula.tech/blog/ai-coding-tools-developer-productivity-paradox （2026-03-13）
[^51^]: unyform.ai「AI Coding Tools Enterprise Problems」— https://unyform.ai/ai-coding-tools-enterprise-problems （2026-03-15）
[^52^]: METR「We are Changing our Developer Productivity Experiment Design」— https://metr.org/blog/2026-02-24-uplift-update/ （2026-02-24）
[^53^]: arXiv「From Technical Debt to Cognitive and Intent Debt」— https://arxiv.org/abs/2603.22106 （2026-03-23）
[^54^]: 掘金「为什么你的 AI 智能体上了生产就翻车」— https://juejin.cn/post/7633640076662128680 （2026-04-28）
[^55^]: gaccode.store「Claude Code 官方最佳实践指南」— https://gaccode.store/post/claude-code-official-best-practices （2025-10-22）
[^56^]: javatask.dev「Spec-Driven Development with AWS Kiro」— https://javatask.dev/blog/agentic-ai-on-aws-spec-driven-development/ （2026-04-29）
[^57^]: arXiv 2512.01155（引 Harding/GitClear 2025 评审轮次分析）— https://www.arxiv.org/pdf/2512.01155v2
