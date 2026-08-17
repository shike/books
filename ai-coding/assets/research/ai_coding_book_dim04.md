# 维度04：月之暗面（Moonshot AI）Kimi 模型与 Kimi Code 编程工具现状

> 调研截止日期：2026-07-31。聚焦 2026 年，尤其近 3 个月。
> 说明：标注「厂商自报」的基准均来自官方发布材料；第三方数据单独注明。月之暗面官方信息渠道为 kimi.com（原 moonshot.cn 体系）、platform.kimi.com（原 platform.moonshot.cn）、GitHub MoonshotAI 组织。

---

## 一、版本演进总览（2025-07 → 2026-07）

| 版本 | 发布日期 | 参数/激活 | 上下文 | 定位 |
|---|---|---|---|---|
| Kimi K2 | 2025-07-11 | 1T / 32B | 256K | 首个万亿参数开源基座（纯文本） |
| Kimi K2 Thinking | 2025-11 | 1T / 32B | 256K | 复杂推理 |
| Kimi K2.5 | 2026-01-27 | 1T / 32B | 256K | 首个原生多模态旗舰，首次引入 Agent 集群（100 子智能体/1500 步） |
| Kimi K2.6 | 2026-04-20 | 1T / 32B | 256K | 通用旗舰，Agent Swarm 扩至 300 子智能体/4000 步 |
| Kimi K2.7 Code | 2026-06-12（高速版 6-15） | 约 1T / 32B（一说 1.1T） | 256K | 编程专项，强制 Thinking |
| Kimi K3 | 2026-07-16 深夜发布，7-27 开源权重 | 2.8T / 约 104B（896 专家激活 16） | 1M | 全球最大开源模型，新架构（KDA+AttnRes） |

---

## 二、Kimi K2.5（2026-01-27 发布）

### 证据 1：发布日期与定位
Claim: Kimi K2.5 于 2026 年 1 月 27 日发布，是原生多模态开源旗舰，首次引入「Agent 集群」能力 [^1^]
Source: 百度百科「Kimi K2.5」词条
URL: https://baike.baidu.com/item/Kimi%20K2.5/67297451
Date: 2026-07-24（词条更新日）
Excerpt: "Kimi K2.5是2026年1月27日由月之暗面Kimi发布的新一代开源模型。该模型基于原生多模态架构设计，支持视觉与文本输入，集成了视觉理解与推理、编程、智能体等多种能力"
Context: 百度百科词条内容汇编自官方发布与媒体报道；发布日期与多家媒体一致。
Confidence: high

### 证据 2：架构规格（厂商与第三方一致）
Claim: K2.5 总参数约 1T、激活 32B、384 个专家（每 token 激活 8+1 共享）、256K 上下文、MLA 注意力、MoonViT 视觉编码器、Modified MIT 开源协议 [^5^]
Source: 什么值得买《Kimi K2系列深度解析》
URL: https://post.smzdm.com/p/a95dd7no
Date: 2026-06-18
Excerpt: "|总参数量|约1T|1T|约1T| 激活参数量|32B|32B|32B| 专家总数|384|384|384| 每token激活专家数|8 + 1共享|8 + 1共享|8 + 1共享| 上下文长度|256K|256K|256K|"
Context: K2.5/K2.6/K2.7 Code 三代同堂对比表；与 vLLM 等第三方披露的 K2.6 架构一致 [^7^]。
Confidence: high

### 证据 3：Agent Swarm 机制（K2.5 代）
Claim: K2.5 的 Agent Swarm 基于 PARL（并行智能体强化学习），最多调度 100 个子智能体并行、支持 1500 次工具调用，宽搜场景延迟最高降 4.5 倍 [^3^]
Source: 51CTO 博客《2026年发布的Kimi K2.5》
URL: https://blog.51cto.com/u_13539/14632989
Date: 2026-05-26
Excerpt: "基于PARL（并行智能体强化学习），动态拆解复杂任务，调度最多 100 个子智能体并行执行，支持1500 次工具调用。相比单智能体，宽搜场景延迟最高降4.5 倍，F1 从 72.8% 提升至 79.0%"
Context: 转述自官方发布材料；百度百科亦载「处理步骤可达1500个」。
Confidence: high（厂商自报数据）

### 证据 4：SWE-Bench Verified 76.8%
Claim: K2.5 在 SWE-Bench Verified 得分 76.8%（厂商自报口径） [^2^]
Source: 新浪财经转载券商深度报告《传媒行业国产模型系列深度(3)：月之暗面(KIMI)》
URL: https://stock.finance.sina.com.cn/stock/go.php/vReport_Show/kind/lastest/rptid/834286113544/index.phtml
Date: 2026-07-27
Excerpt: "K2.5的SWE-bench Verified得分76.8%，超越同期主流闭源模型，标志着Kimi从"规模突破"转向"能力落地"。"
Context: 券商研报引用官方数据；smzdm 对比文 [^5^] 给出同一数字。
Confidence: high（数字一致性高；性质为厂商自报）

### 证据 5：首个登顶 LMSYS Chatbot Arena 的开源模型
Claim: Kimi K2.5 是首个在 LMSYS Chatbot Arena 总榜登顶的开源模型 [^4^]
Source: 掘金《2026半年盘点：AI界发生的6件大事》
URL: https://juejin.cn/post/7652263740117319707
Date: 2026-06-18
Excerpt: "月之暗面的Kimi K2.5成为 **首个在LMSYS Chatbot Arena登顶的开源模型**。这不仅是技术上的突破，也是对"开源=落后"成见的打破。"
Context: 第三方媒体盘点；另一篇掘金半年报 [^4b^] 同样表述「Kimi K2.5（首个LMSYS登顶的开源模型）」。
Confidence: high

### 证据 6：商业表现
Claim: K2.5 发布后不到一个月（约 20 天）的收入即超过月之暗面 2025 年全年总收入；2026 年 3 月 ARR 突破 1 亿美元、4 月环比翻倍至 2 亿美元 [^1^][^2^]
Source: 百度百科（引知情人士）；新浪财经券商报告
URL: https://baike.baidu.com/item/Kimi%20K2.5/67297451 ; https://stock.finance.sina.com.cn/stock/go.php/vReport_Show/kind/lastest/rptid/834286113544/index.phtml
Date: 2026-02-24（报道日）/ 2026-07-27
Excerpt: "2026年2月24日，多位知情人士透露，Kimi推出的K2.5大模型自发布以来不足一个月，近二十天内实现的收入已超过其2025年全年的总收入。" / "26年3月随着K2.5的发布，ARR突破1亿美金，4月ARR进一步环比翻倍至2亿美金。"
Context: 收入数据为知情人士/券商口径，非审计数据。
Confidence: medium

### 证据 7：Cursor Composer 2 基于 K2.5（重要生态事件）
Claim: 2026 年 3 月，Cursor 发布的 Composer 2 模型被发现基于 Kimi K2.5 构建（经 Fireworks 托管 RL 平台接入，属授权商业合作）；马斯克公开评论「没错，这就是 Kimi 2.5」 [^48^][^49^]
Source: 百度百科「北京月之暗面科技股份有限公司」词条；china3dprint.com
URL: https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E6%9C%88%E4%B9%8B%E6%9A%97%E9%9D%A2%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/63575472 ; https://www.china3dprint.com/archives/4198.html
Date: 2026-03-21
Excerpt: "Cursor团队也公开承认，未在发布时提及Kimi基座模型是沟通失误，并称Composer 2是在Kimi K2.5基础上，完成了4倍规模的强化学习和编程场景专属适配"
Context: 网友操作 base URL 发现模型路径含 "kimi-k2p5-rl"；月之暗面官方 3 月 21 日微博确认授权合作。这是 K2.5 编程能力被海外头部工具商采用的关键佐证。
Confidence: high

---

## 三、Kimi K2.6（2026-04-20 发布并开源）

### 证据 8：发布与定位
Claim: K2.6 于 2026 年 4 月 20 日发布并开源（HuggingFace），为 1T 参数 MoE 旗舰，Agent Swarm 从 100 子智能体/1500 步扩至 300 子智能体/4000 步 [^6^][^48^]
Source: TheRouter 博客；百度百科公司词条
URL: https://therouter.ai/zh/blog/may-2026-model-wave/ ; https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E6%9C%88%E4%B9%8B%E6%9A%97%E9%9D%A2%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/63575472
Date: 2026-05-05 / 2026-07-30
Excerpt: "**2026-04-20 发布。** Kimi K2.6 是月之暗面的 1T 参数 MoE 旗舰。 编码评测追平 GPT-5.5,但价格仍是开源权重的水平。Agent swarm 子系统从 K2.5 的 100 个 sub-agent / 1500 步扩到 K2.6 的 300 个 sub-agent / 4000 步。"
Context: 第三方模型网关的发布记录；「编码评测追平 GPT-5.5」为该网关表述，注意与下文厂商基准区分。
Confidence: high（发布日期与规格）；medium（「追平 GPT-5.5」表述）

### 证据 9：K2.6 基准（厂商自报，经第三方核对）
Claim: K2.6 官方数据：SWE-Bench Verified 80.2%、SWE-Bench Pro 58.6%、HLE w/ tools 54.0、BrowseComp 83.2；是首个在两个基准同时超越三家闭源旗舰的开源权重 [^7^][^8^]
Source: 什么值得买《Kimi K2.6开源发布》；CSDN《AI 订阅策略调研报告》
URL: https://post.smzdm.com/p/ak8eo53k ; https://blog.csdn.net/wwwwwwgame/article/details/161090593
Date: 2026-05-15 / 2026-05-14
Excerpt: "HLE w/ tools 54.0 压 Claude Opus 4.6 的 53.0、GPT-5.4 的 52.1；SWE-Bench Pro 58.6 压 GPT-5.4 的 57.7。这是第一个在这两个基准上同时超过三家闭源旗舰的开源权重。" / "K2.6 于 2026.4.20 发布并开源，SWE-bench Verified 80.2%（接近 Claude Opus 4.7 的 80.8%），开源代码能力第一。"
Context: 分数为厂商发布口径，第三方作者逐条核对过公开 leaderboard。
Confidence: high（数字）；注意为厂商自报基准

### 证据 10：长程执行能力
Claim: K2.6 可持续 12-13 小时不间断编码、完成超 4000 次自主工具调用（如金融撮合引擎 4000+ 行代码重构） [^47^][^5^]
Source: i黑马（腾讯新闻）；smzdm
URL: https://view.inews.qq.com/a/20260604A04XH200 ; https://post.smzdm.com/p/a95dd7no
Date: 2026-06-04 / 2026-06-18
Excerpt: "该模型在不间断编码测试中可以连续工作13小时，支持最多300个子Agent并行协作，实现超过4000次自主工具调用。"
Context: 官方在 Kimi Work 发布时披露的数据。
Confidence: high（厂商口径）

---

## 四、Kimi K2.7 Code（2026-06-12 发布并开源，高速版 6-15 上线）

### 证据 11：发布、架构与强制 Thinking
Claim: K2.7 Code 为编程专项模型，约 1T 总参/32B 激活、256K 上下文，思考模式强制开启（关闭则 API 报错、Kimi Code 回退 K2.6）；官方建议非编程任务仍用 K2.6 [^9^][^10^]
Source: IT之家；SegmentFault
URL: https://www.ithome.com/0/963/661.htm ; https://segmentfault.com/a/1190000047863643
Date: 2026-06-12 / 2026-06-16
Excerpt: "官方表示， **在非编程任务中，仍然推荐能力更加全面的 K2.6 模型**。使用 Kimi K2.7 Code 模型须打开思考模式（Thinking）以发挥最佳性能。Kimi API 和 Kimi Code 均默认开启思考，如果手动关闭思考模式，API 会报错，Kimi Code 会回退到 K2.6 模型。"
Context: 官方发布通稿。总参数存在口径分歧：多数来源称 1T，百度百科称 1.1 万亿 [^12^]。
Confidence: high（功能事实）；medium（总参数 1T vs 1.1T 存分歧）

### 证据 12：基准与 token 效率（厂商自报）
Claim: K2.7 Code 相比 K2.6：Kimi Code Bench v2 +21.8%（达 62.0）、Program-Bench +11%、MLS Bench Lite +31.5%，Agent 类基准（Kimi Claw 24/7 Bench、MCP Atlas、MCP Mark Verified）提升约 10%；平均 token 消耗减少 30% [^9^][^5^]
Source: IT之家；smzdm
URL: https://www.ithome.com/0/963/661.htm ; https://post.smzdm.com/p/a95dd7no
Date: 2026-06-12 / 2026-06-18
Excerpt: "在评估代码能力的内外部基准测试中，K2.7 Code 相比 K2.6 性能显著提升：Kimi Code Bench v2 提升 21.8%、Program-Bench 提升 11%、MLS Bench Lite 提升 31.5%。"
Context: 注意 Kimi Code Bench v2、Kimi Claw 24/7 Bench 为厂商自建基准（内部口径），Program-Bench、MCP Mark 为外部基准。
Confidence: high（厂商自报口径）

### 证据 13：MCP 工具调用首超 Claude（外部基准）
Claim: K2.7 Code 在 MCP Mark Verified 以 81.1 分首超 Claude Opus 4.8（76.4），但综合编程基准（Kimi Code Bench v2 62.0%）仍落后 GPT-5.5（69.0%）与 Opus 4.8（67.4%） [^11^][^10^]
Source: 掘金《Kimi K2.7 Code 深度拆解》；SegmentFault
URL: https://juejin.cn/post/7650899618197225535 ; https://segmentfault.com/a/1190000047863643
Date: 2026-06-14 / 2026-06-16
Excerpt: "在衡量Agent工具调用能力的 MCP Mark Verified 基准上，K2.7 Code以81.1分首次超越Claude Opus 4.8（76.4分）" / "在 MCP Mark Verified 工具调用基准上，K2.7 Code 以 81.1% 超越 Claude Opus 4.8 的 76.4%，但在综合编程基准（Kimi Code Bench v2 62.0%）上仍落后于 GPT-5.5（69.0%）和 Opus 4.8（67.4%）。"
Context: MCP Mark Verified 为第三方基准；Kimi Code Bench 为厂商自建基准，跨厂商比较时需注意口径。
Confidence: high

### 证据 14：高速版与定价
Claim: K2.7 Code API 定价与 K2.6 持平（输入 6.5 元/输出 27 元/百万 token，缓存命中输入 1.3 元）；高速版输出速度 5-6 倍（常规约 180 token/s、短上下文最高 260 token/s），价格为普通版 2 倍 [^9^][^12^]
Source: IT之家；百度百科「Kimi K2.7 Code」
URL: https://www.ithome.com/0/963/661.htm ; https://baike.baidu.com/item/Kimi%20K2.7%20Code/67986864
Date: 2026-06-12 / 2026-07-03
Excerpt: "1M token 的标准输入和输出价格与 K2.6 模型一致，分别为 6.5 元和 27 元；命中缓存的输入价格调整为 1.3 元" / "该版本响应效率较高，输出速度较标准版有所提升，常规编程场景下输出速度约为180 Token/s，短上下文场景最高可达260 Token/s。"
Context: 高速版在 Kimi Code Plan 中用量消耗为普通版 3 倍 [^402 引自官方发布全文]。
Confidence: high

---

## 五、Kimi K3（2026-07-16 深夜发布；7-27 开源权重）

### 证据 15：发布时间与规格
Claim: Kimi K3 于 2026 年 7 月 16 日深夜（WAIC 开幕前夕，官方公告落款为 17 日凌晨）发布：2.8 万亿参数 MoE（896 专家、单次激活 16，激活量约 104B）、KDA 混合线性注意力 + 注意力残差（AttnRes）新架构、原生视觉理解、100 万 token 上下文，系全球最大/首个 3 万亿级开源模型 [^13^][^14^][^15^]
Source: 北京商报（搜狐）；新京报贝壳财经（东方财富）；IT之家
URL: https://www.sohu.com/a/1051384603_115865 ; https://wap.eastmoney.com/a/202607173810197948.html ; https://www.ithome.com/0/982/259.htm
Date: 2026-07-17 / 2026-07-17 / 2026-07-27
Excerpt: "Kimi K3 是一个 2.8 万亿参数模型，基于 KDA 混合线性注意力机制（Kimi Delta Attention）和注意力残差（Attention Residuals）技术构建，原生支持视觉理解，并拥有 100 万 token 上下文窗口。" / "结合 Stable LatentMoE 框架后，模型可以在 896 个专家中高效激活 16 个。"
Context: 发布时间各媒体表述为「7月16日深夜」或「7月17日凌晨」，属同一发布事件；激活参数约 104B 为媒体披露口径（精度中等）。官方称规模化效率较 K2 提升约 2.5 倍。
Confidence: high

### 证据 16：开源与配套 Infra
Claim: 2026 年 7 月 27 日晚，月之暗面开源 K3 模型权重与技术报告，并同步开源三项关键 Infra：MoonEP（超大细粒度 MoE 通信库）、FlashKDA（KDA 高性能算子）、AgentEnv（与 KVCache.ai 合作的沙箱系统）；采用修改版 MIT 协议 [^15^][^17^]
Source: IT之家；东方财富
URL: https://www.ithome.com/0/982/259.htm ; https://wap.eastmoney.com/a/202607283823453572.html
Date: 2026-07-27 / 2026-07-28
Excerpt: "月之暗面官方今晚正式开源 Kimi K3 模型。官方发布了 Kimi K3 的模型权重、技术报告，并开源支撑 Kimi K3 模型训练的关键 Infra 技术：MoonEP、FlashKDA 和 AgentEnv。"
Context: 阿里云真武、摩尔线程等当日完成适配；国家超算互联网 7-21 上线 K3 API 服务。
Confidence: high

### 证据 17：编程基准（厂商自报，注意 harness 口径）
Claim: K3 官方评测（max 思考强度）：SWE-Marathon 42.0% 第一（Opus 4.8 40.0、GPT-5.6 Sol 39.0、Fable 5 35.0）、ProgramBench 77.8% 第一（GPT-5.6 Sol 77.6%）、Terminal-Bench 2.1 88.3（第二，GPT-5.6 Sol 88.8）、FrontierSWE 81.2（第二，次于 Fable 5）、DeepSWE 67.3；官方同时承认整体仍落后 Claude Fable 5 与 GPT-5.6 Sol [^16^][^17^][^18^]
Source: Kimi K3 官方 Tech Blog；东方财富；Fenxi 分析
URL: https://www.kimi.com/blog/kimi-k3 ; https://wap.eastmoney.com/a/202607283823453572.html ; https://fenxi.fr/en/blog/kimi-k3-moonshot-ai-architecture-benchmarks-explained/
Date: 2026-07 / 2026-07-28 / 2026-07-27
Excerpt: "在SWE-Marathon这一面向GPU内核优化的评测中，Kimi K3以42.0%领先于Claude Fable 5的35.0%和GPT-5.6 Sol的39.0%。" / 官方博客脚注："Additionally, Claude Fable 5 hit fallbacks on 35% of the tasks in our evaluation, which may have negatively impacted its measured performance."
Context: 关键口径警告：官方脚注承认各模型使用不同 agent harness（K3 用 Kimi Code，OpenAI 用 Codex，Anthropic 用 Claude Code/Terminus），且 K3 全部在 reasoning effort=max、temperature=1 下测得；SWE-Marathon 用了 H20 重新校准的分支。跨模型比较应视为「模型+工具链组合」而非纯模型对比。
Confidence: high（官方口径本身）；引用时必须附带口径说明

### 证据 18：第三方基准——前端代码登顶 & Artificial Analysis
Claim: K3 在（第三方）Frontend Code Arena 以 1679 Elo 登顶（超 Claude Fable 5 的 1631、GPT-5.6 Sol 的 1618）；Artificial Analysis 综合智能指数 K3 为 57（Fable 5 为 60、GPT-5.6 Sol 为 59），AA 私有长时程知识工作评估 K3 Elo 1547 仅次于 Fable 5，单任务成本约 $0.94 [^20^][^22^][^21^]
Source: IT之家（引 Bloomberg）；CSDN AI 编程社区；shengyayun 编译的 AA 报告
URL: https://www.ithome.com/0/978/670.htm ; https://aicoding.csdn.net/6a5af9ab10ee7a33f28ea86c.html ; https://www.shengyayun.com/blog/english-translation-2026-07-18/
Date: 2026-07-19 / 2026-07-18 / 2026-07-18
Excerpt: "在 Frontend Code Arena 全球 AI 大模型榜单中，Kimi K3 以 1679 分超越 Claude Fable 5，位居第一。" / "在 Artificial Analysis 综合智能指数上，K3 为 57 分，Claude Fable 5 为 60 分、GPT-5.6 Sol 为 59 分、Opus 4.8 为 56 分" / "在我们的私有长时程知识工作评估中，Kimi K3 总 Elo 得分为 1547，比 Kimi K2.6 高出 732 分，仅次于 Claude Fable 5。"
Context: Frontend Code Arena 为第三方人类偏好榜单（编程维度最有力的第三方证据）；AA 指数为第三方综合评估。马斯克在相关评测下留言 "Impressive" [^20^]。
Confidence: high

### 证据 19：API 定价大幅上调
Claim: K3 API 定价：输入（缓存命中）2 元/百万 token、输入（未命中）20 元、输出 100 元（国际价 $0.30/$3/$15）；较 K2.6（6.5 元/27 元，$0.95/$4）输入涨 208%、输出涨 270%，首次站进美国旗舰价位带；官方称编程场景缓存命中率超 90% [^13^][^28^][^23^]
Source: 北京商报（搜狐）；新浪财经《Kimi不再便宜》；新浪微博科技
URL: https://www.sohu.com/a/1051384603_115865 ; https://finance.sina.com.cn/roll/2026-07-27/doc-inikfsuy8461071.shtml ; https://www.sina.cn/news/detail/5321623272167138.html
Date: 2026-07-17 / 2026-07-27 / 2026-07-17
Excerpt: "价格为每百万 Token 输入：2 元（命中缓存）和 20 元（未命中缓存），输出：100 元。借助 Mooncake 分离式推理架构，Kimi 官方 API 编程场景的缓存率超过 90%" / "相比上一代旗舰 K2.6 的 6.5 元和 27 元，K3 的输入价格上涨 208%，输出价格上涨 270%。"
Context: K3 输出价约为 DeepSeek V4-Pro 的 16.7 倍，但约为 Claude Fable 5（$10/$50）的三分之一。成本效率方面，官方技术报告称 K3 在 Kimi Code Bench 2.0 得分比 Fable 5 低约 4 个百分点但推理成本仅为其 38% [^17^]。
Confidence: high

### 证据 20：48 小时自主芯片设计 demo（厂商演示，需注明局限）
Claim: K3 官方演示了「48 小时无人工干预、仅用开源 EDA 工具完成一颗芯片全流程设计」：Nangate 45nm 开源工艺库、4mm²、100MHz、146 万标准单元，用于运行 K3 自己的 Nano 推理模型（仿真解码 8721 tok/s）；官方定性为 early proof of concept，未流片、无第三方复现 [^25^]
Source: 新浪财经（引官方技术博客）
URL: https://www.sina.cn/news/detail/5322758776946810.html
Date: 2026-07-20
Excerpt: "工艺 / 规格：Nangate 45nm 开源单元库，4mm²，100MHz，146 万标准单元 + 0.277MB SRAM……官方定性：early proof of concept，目前只有时序收敛 + 仿真吞吐，没有流片、回片、测试板运行、第三方复现"
Context: 发布当日 Cadence -9.47%、Synopsys -7.85%；但分析指出 45nm 教学级流程开源工具本就能跑，未触及先进工艺 PDK/Signoff 等护城河。书中引用时务必保留 PoC 定性。
Confidence: high（事实层面）；演示能力外推需谨慎

### 证据 21：K3 发布 48 小时后暂停 C 端新订阅
Claim: 7 月 19 日深夜官方发布《关于算力紧缺与会员暂停开放的说明》：K3 发布 48 小时内请求量逼近集群承载极限，即日起暂停 C 端新用户订阅，并计划将订阅拆分为 Kimi 主权益与 Kimi Code 专项权益 [^26^][^27^]
Source: SmartHey（全文转载官方公告）；观察者网
URL: https://www.smarthey.com/detail/286231203112.html ; https://www.guancha.cn/economy/2026_07_21_824589.shtml
Date: 2026-07-19 / 2026-07-21
Excerpt: "过去48小时，用户请求量已大幅超出我们的预估，并且逼近现有集群的承载极限。为了保障已有订阅用户的体验，我们决定即日起，暂停C端新用户订阅……对于后续新订阅用户，我们将拆分Kimi主权益（涵盖Kimi Web、Kimi APP、Kimi Work）与Kimi Code专项权益"
Context: 截至 7 月 27 日各付费档仍显示「售罄」，官方称新会员计划即将推出 [^52^]。这已是年内第二次：4 月 K2.6 上线后也曾出现会员排队、功能短暂不可用和权益误扣，公司随后将全体用户当月额度恢复至 100% [^56^]。
Confidence: high

### 证据 22：K3 在 Kimi Code 中的模型与档位
Claim: Kimi Code 提供三个模型 ID：kimi-k3（旗舰，最高 1M 上下文）、kimi-for-coding（即 K2.7 Code，256K）、kimi-for-coding-highspeed（6 倍速、3 倍消耗）；K3 思考强度分 low/high/max 三档 [^57^][^56^]
Source: MornAI《Kimi K3全解析》；新浪财经
URL: https://www.mornai.cn/news/llm/kimi-k3-full-analysis-agent-coding-flagship/ ; https://finance.sina.com.cn/wm/2026-07-20/doc-iniimzhe8307985.shtml
Date: 2026-07-17 / 2026-07-20
Excerpt: "Kimi Code提供了三个模型ID：kimi-k3是旗舰款……上下文最高支持1M；kimi-for-coding是K2.7 Code，256K上下文；kimi-for-coding-highspeed速度是前者的6倍，但消耗是3倍。"
Context: 档位门控详见「会员体系」节（Andante 不可用 K3，Moderato 限 256K，Allegretto 起 1M）。
Confidence: high

---

## 六、Kimi Code CLI（终端编程 Agent）

### 证据 23：产品沿革与开源许可（注意两代仓库协议不同）
Claim: Kimi Code 有两代仓库：旧版 kimi-cli（Python，Apache-2.0，已停止维护，约 9.2k-10.8k stars）与现行版 kimi-code（TypeScript 重写，MIT，npm 分发，2026-07-24 核验约 4,857 stars）；2026-01-26 由「Kimi CLI」统一更名为「Kimi Code CLI」 [^29^][^30^][^31^][^51^]
Source: 百度百科「Kimi Code CLI」；MarkTechPost；GitHub MoonshotAI/kimi-code；magicnetworld
URL: https://baike.baidu.com/item/Kimi%20Code%20CLI/67975444 ; https://www.marktechpost.com/2026/06/06/moonshot-ai-releases-kimi-code-cli-a-terminal-ai-coding-agent-built-in-typescript-for-next-gen-agents/ ; https://github.com/MoonshotAI/kimi-code ; https://magicnetworld.com/tools/kimi-code/
Date: 2026-07-02 / 2026-06-06 / 2026-05-22（repo 快照）/ 2026-07-24
Excerpt: "Kimi Code CLI is the successor to the older kimi-cli. The new agent is written in TypeScript and distributed via npm." / GitHub 仓库页脚："Released under the MIT License." / "现行版本是 TypeScript 实现（GitHub 4,857 stars，2026-07-24 核验），旧 Python 版（kimi-cli）已停止维护。"
Context: 部分二手资料（含百度百科）把「Kimi Code CLI」笼统标为 Apache-2.0，实为旧版 Python 仓库的协议；引用时应区分两代仓库。
Confidence: high

### 证据 24：功能形态
Claim: Kimi Code CLI 为终端 AI Agent：读写代码、执行 Shell、搜索文件、抓取网页；支持 Plan 模式（Shift-Tab）、内置 coder/explore/plan 三个子代理、MCP（/mcp-config 对话式配置）、Skills、生命周期 hooks、视频输入（拖入屏幕录制/演示视频作为编码上下文）；支持 --yolo 免确认、/fork、/compact [^30^][^31^]
Source: MarkTechPost；GitHub README
URL: https://www.marktechpost.com/2026/06/06/moonshot-ai-releases-kimi-code-cli-a-terminal-ai-coding-agent-built-in-typescript-for-next-gen-agents/ ; https://github.com/MoonshotAI/kimi-code
Date: 2026-06-06
Excerpt: "Subagents for parallel work. Dispatch built-in `coder`, `explore`, and `plan` subagents in isolated contexts." / "Video input. Drop a screen recording or demo clip into the chat."
Context: 安装：官方脚本（macOS/Linux install.sh；Windows PowerShell install.ps1，需 Git Bash）或 npm（Node.js ≥ 24.15.0）。
Confidence: high

### 证据 25：IDE/编辑器集成
Claim: Kimi Code 通过 ACP（Agent Client Protocol）接入 Zed、JetBrains 全系 IDE；另有官方 VS Code 扩展与 Zsh 插件（Ctrl-X 切换 Shell 模式） [^31^][^32^][^44^]
Source: GitHub README；官方文档；CSDN
URL: https://github.com/MoonshotAI/kimi-code ; https://moonshotai.github.io/kimi-cli/zh/guides/ides.html ; https://blog.csdn.net/2611_96382751/article/details/163014954
Date: 2026-05-22 / 未注明 / 2026-07-19
Excerpt: "Kimi Code CLI speaks the Agent Client Protocol, so ACP-compatible editors and IDEs (Zed, JetBrains, …) can drive a session over stdio." / "IDE 集成 — 通过 ACP 协议接入 Zed、JetBrains（需要在编辑器配置 `agent_servers`）；VS Code — 有官方扩展"
Context: 其 API 兼容 Anthropic 协议，因此 Claude Code 内可直接填 Kimi 的 Key 使用 [^51^]。
Confidence: high

### 证据 26：第三方客户端白名单限制（常见坑 #1）
Claim: 会员附带的 kimi-for-coding 模型实行客户端白名单制：仅 Kimi CLI、Claude Code、Roo Code、Kilo Code 等指定 Coding Agent 可用；Cline（56k stars）等非白名单客户端调用返回 403 access_terminated_error；接入需向 code@moonshot.ai 提交 User-Agent 申请 [^33^][^34^]
Source: GitHub Discussion #2323（kimi-cli 官方仓库）；TRAE 官方社区（含 kimi 官方回复）
URL: https://github.com/MoonshotAI/kimi-cli/discussions/2323 ; https://forum.trae.cn/t/topic/25283
Date: 2026-05-18 / 2026-06-16
Excerpt: "Every request returns a `403 access_terminated_error` with the message: Kimi For Coding is currently only available for Coding Agents such as Kimi CLI, Claude Code, Roo Code, Kilo Code, etc." / 官方回复："请联系开源社区或产品负责人，由对方向 **code@moonshot.ai** 提交客户端接入申请……滥用白名单资格将被直接移除。"
Context: 2026 年 2 月的第三方横评亦提示「工具适配少，非指定工具使用可能封号」[^35^]。这是 Kimi Coding Plan 相对智谱（20+ 工具）的主要短板。
Confidence: high

---

## 七、Kimi 会员 / Coding Plan 定价与计费机制

### 证据 27：档位与价格（截至 2026-07，国内）
Claim: 会员共五档（音乐速度术语）：Adagio 免费、Andante ¥49/月（年付 ¥468，月均 ¥39）、Moderato ¥99/月（年付 ¥948，月均 ¥79）、Allegretto ¥199/月（年付 ¥1,908，月均 ¥159）、Allegro ¥699/月（年付 ¥6,708，月均 ¥559）；Kimi Code 额度系数分别约 1×/4×/20×/60×；海外版为 Moderato $19、Allegretto $39、Allegro $99、Vivace $199/月 [^28^][^38^][^24^]
Source: 新浪财经《Kimi不再便宜》；codeagentswarm.com；搜狐
URL: https://finance.sina.com.cn/roll/2026-07-27/doc-inikfsuy8461071.shtml ; https://www.codeagentswarm.com/en/guides/kimi-code-plans-and-pricing ; https://www.sohu.com/a/1051436889_122920010
Date: 2026-07-27 / 2026-07-18 / 2026-07-17
Excerpt: "按照年付价格计算，Kimi 目前四档会员 Andante、Moderato、Allegretto 和 Allegro，分别为每月 39 元、79 元、159 元和 559 元，对应每年 468 元、948 元、1908 元和 6708 元。" / "C端会员同步改了档位，五档全用音乐速度术语命名：Adagio免费，Andante每月49元，Moderato 99元，Allegretto 199元，Allegro 699元。Kimi Code额度分别是1倍、4倍、20倍、60倍"
Context: 价格为 K3 发布后口径；2026 年 5 月前 Andante 曾长期以 ¥39 活动价销售。多设备登录、Agent 并行数等权益随档位提升。
Confidence: high

### 证据 28：Token 计量制与缓存命中率（核心机制，常见坑 #2）
Claim: Kimi Code 于 2026 年 1 月底全面切换为 Token 计量：仅按「未命中缓存的输入 token + 输出 token」计额度，缓存命中部分不计入；Vibe Coding 场景输入约占 99.5%、其中缓存命中约 90-95%，故实际可用量与缓存命中率强相关、透明度较低 [^35^][^37^]
Source: 博客园《2026年国内主流AI Coding Plan套餐全对比》；塔猴/aitntnews 汇总
URL: https://www.cnblogs.com/wzxNote/p/19648084 ; https://www.tahou.com/article/202245162112700421
Date: 2026-02-27 / 2026-04-01
Excerpt: "Token计量：Kimi于2026年1月28日全面切换为此模式，按输入输出Token计费，且仅统计未命中缓存的Token（缓存命中率直接影响实际额度）" / "计费方式按 uncached input + output tokens 计量，缓存命中的部分不计入限额。在典型的 Vibe Coding 场景中，input tokens 占总量的 99.5% 左右，其中缓存命中部分约占 90%-95%。实际可用请求数与缓存命中率强相关。"
Context: 实测（199 元档、K3、95% 缓存命中率）：4 轮编程对话输入累积 230 万 token、输出仅约 5 万，推算 5 小时内有效吞吐约 1385 万 token、折合约 $10 [^43^]。这一机制使 Kimi 在重度编程场景边际成本极低，但用户难以预估额度。
Confidence: high

### 证据 29：「不限 5 小时窗口」已过时——2026 年中起 Kimi Code 也有 5 小时/周限额（重要事实修正）
Claim: 2026 年初 Kimi 确实是国内唯一不设 5 小时窗口的 Coding Plan；但最迟 2026 年 6 月起，Kimi Code 已引入「5 小时 + 7 天（周）」双层限额（7 天周期自订阅日起刷新、不累积；5 小时滚动频控），官方帮助页 2026-07-29 明确「Kimi Code 另有 5 小时 / 周限额，仅作用于 Kimi Code」 [^36^][^39^][^38^][^202^]
Source: GitHub ForceInjection 报告（2026-04）；Kimi 官方帮助页；codeagentswarm；CSDN
URL: https://github.com/ForceInjection/forceinjection.github.io/blob/main/09_inference_system/cost_analysis/coding_plan/coding_plan_report.md ; https://www.kimi.com/zh-cn/help/membership/membership-pricing ; https://www.codeagentswarm.com/en/guides/kimi-code-plans-and-pricing ; https://blog.csdn.net/ab977a1081268482/article/details/162017132
Date: 2026-04-18 / 2026-07-29 / 2026-07-18 / 2026-06-16
Excerpt: 2026-04 报告："Kimi Code Plan……用量限制：基于 Token 动态计量。关键限制条款：无特殊封控机制，且不设 5 小时窗口拦截。" / 官方帮助页："此外 Kimi Code 另有 5 小时 / 周限额，仅作用于 Kimi Code。" / "Kimi Code quota has two layers…The first layer is a weekly cycle…The second layer is a rolling 5 hour window on top."
Context: 【给作者的修正】「唯一不限 5 小时窗口」是 2026 年 1-4 月的事实，截至 2026-07 已不成立；当前差异点变为「按 token 计量（缓存命中不计）」而非「无窗口」。额度用磬可买「加油包」（25 元起）[^51^]。
Confidence: high

### 证据 30：档位能力门控（K3 与 1M 上下文）
Claim: Kimi Code 中：Andante（¥49）不可用 K3（仅 K2.7 Code）；Moderato（¥99）起可用 K3 但限 256K 上下文；1M 全量上下文与 K2.7 高速版需 Allegretto（¥199）及以上；Agent Swarm 子代理数随档位 2/4/8 个 [^42^][^38^][^44^]
Source: coding-plan.org 横评页；codeagentswarm；CSDN
URL: https://coding-plan.org/ ; https://www.codeagentswarm.com/en/guides/kimi-code-plans-and-pricing ; https://blog.csdn.net/2611_96382751/article/details/163014954
Date: 2026-07-18 / 2026-07-18 / 2026-07-19
Excerpt: "Andante……K2.7 Code · 不支持 K3；Moderato……K3 256K · K2.7 Code，Swarm 最多 2 个子 Agent；Allegretto……20x 额度 · K3 最高 1M · K2.7 高速版，Kimi Claw · Swarm 最多 4 个子 Agent" / "on Moderato you get 256k tokens of context, and the full 1M requires Allegretto or higher"
Context: 第三方整理页，与官方会员页口径一致；K3 上线后官方页面曾出现「哪档含 Kimi Code」表述不一致，购买前应以官网为准 [^38^]。
Confidence: medium-high（第三方整理，多处交叉一致）

### 证据 31：额度池结构
Claim: 会员内为「统一额度池」：Agent、深度研究、PPT 等共享一个池；Kimi Code 为独立额度池（按上述系数扣减）；K2.6 模型在 C 端对话中不消耗额度；额度刷新分 5 小时/周/月多档 [^58^][^39^]
Source: chooseai 指南；Kimi 官方帮助页
URL: https://www.chooseai.net/news/5222/ ; https://www.kimi.com/zh-cn/help/membership/membership-pricing
Date: 2026-07-21 / 2026-07-29
Excerpt: "1、Agent系列、深度研究、PPT这些会员功能共享一个额度池，按token消耗计算……2、Kimi Code单独享有独立额度池……3、K2.6模型不消耗额度" / 官方："可以。所有会员功能共享一个额度池，你可以自由支配。但请注意：某个功能把额度用完，会影响其他功能的使用"
Context: 官方口径与第三方指南略有出入（官方强调「一个额度池」，第三方称 Code 独立池）；以官方帮助页为准：功能间会互相挤占，Code 另有独立窗口限制。
Confidence: medium-high

### 证据 32：API 定价全景（开放平台，按量计费，人民币/百万 token）
Claim: K2.5：输入 4 元（缓存命中 0.7 元）/输出 21 元；K2.6 与 K2.7 Code：输入 6.5 元（命中 1.3 元）/输出 27 元，高速版 2 倍价；K3：输入 20 元（命中 2 元）/输出 100 元；Batch API 为标准价 6 折；联网搜索每次额外 ¥0.03 [^59^][^9^][^13^][^189^][^40^]
Source: ooo.run；IT之家；北京商报；ai-nav.store；smzdm
URL: https://ooo.run/post/try-kimi-k25-free-in-opencode.html ; https://www.ithome.com/0/963/661.htm ; https://www.sohu.com/a/1051384603_115865 ; https://www.ai-nav.store/tools/moonshot-kimi ; https://post.smzdm.com/p/az846klp
Date: 2026-06-24 / 2026-06-12 / 2026-07-17 / 2026-07-27 / 2026-06-21
Excerpt: "|Kimi K2.5|￥4.00|￥0.70|￥21.00|256k|" / "1M token 的标准输入和输出价格与 K2.6 模型一致，分别为 6.5 元和 27 元；命中缓存的输入价格调整为 1.3 元" / "每百万Token缓存命中输入为2元，未命中输入为20元，输出为100元" / "Kimi K2.5 Batch API ~~CNY4~~→CNY2.4省 40%" / "联网搜索功能每次额外收费¥0.03，独立于Token消耗"
Context: 美元价：K2.6 $0.16（命中）/$0.95/$4.00；K3 $0.30/$3/$15。注意：Kimi 开放平台 API 与 Kimi Code（会员）是两套独立计费体系，权益不互通；经火山方舟等第三方网关调用时计费限流由网关方控制 [^40^]。
Confidence: high

### 证据 33：售罄状态（截至 2026-07-27）
Claim: K3 发布后全部四档付费会员显示「售罄」，官方称新会员计划即将推出；拟拆分主权益与 Kimi Code 权益 [^52^][^26^]
Source: glbgpt.com；官方公告
URL: https://www.glbgpt.com/hub/zh/kimi-k3-pricing/ ; https://www.smarthey.com/detail/286231203112.html
Date: 2026-07-21 / 2026-07-19
Excerpt: "这四款付费卡均显示已售罄，Kimi表示新会员计划即将推出，购买前请再次确认。"
Context: 书中若写「Kimi 不限购」需注意时效：2026 年 5-6 月确实「不限购、全档位常态开放」[^8 系]，7-19 起转为暂停新增。
Confidence: high

---

## 八、Agent Swarm 机制

### 证据 34：机制与代际演进
Claim: Agent Swarm 基于 PARL（并行智能体强化学习）：主 Agent 拆解任务、并行分配给子 Agent，配实例化/完成/最终结果三种动态权重奖励；K2.5 为 100 子智能体/1500 步，K2.6 起扩至 300 子智能体/4000 步，K3 发布会（GTC 2026，杨植麟演讲）口径亦为 300 个 Agent 并行 [^3^][^2^][^106^]
Source: 51CTO；新浪财经券商报告；aicxd（转宝玉）
URL: https://blog.51cto.com/u_13539/14632989 ; https://stock.finance.sina.com.cn/stock/go.php/vReport_Show/kind/lastest/rptid/834286113544/index.phtml ; https://aicxd.com/ai-hot/article/91877
Date: 2026-05-26 / 2026-07-27 / 2026-07-18
Excerpt: "K2.6又引入Agent Swarm，单次会话最多调度300个子Agent、协调4000 步，相比K2.5的100个子Agent /1500步，分别增长200%/167%。" / "引入Agent Swarm智能体集群，主Agent拆解任务并行分配给子Agent，设计实例化、完成和最终结果三种动态权重奖励，将串行任务转为并行"
Context: 产品化形态：App 端「K3集群·Max」档；Kimi Code 中子代理数按会员档位 2/4/8 个（见证据 30）；Kimi Work 中最多自主创建 300 子 Agent 团队 [^47^]。
Confidence: high

---

## 九、Kimi Claw 是什么

### 证据 35：Kimi Claw = 云端托管的 OpenClaw Agent 服务
Claim: Kimi Claw Beta 于 2026 年 2 月 16 日（春节）上线，是基于开源 Agent 框架 OpenClaw + Kimi K2.5 的云端 AI 代理服务：具备长期记忆、自主操作能力，支持云端原生部署或桥接本地/第三方 OpenClaw 实例，可调用 ClawHub 社区插件、远程操控电脑，提供 40GB 存储，接入专业财经实时数据 API；首批仅 Allegretto 及以上会员开放 [^45^]
Source: 百度百科「Kimi Claw Beta」词条
URL: https://baike.baidu.com/item/Kimi%20Claw%20Beta/67406551
Date: 2026-07-24（词条更新）；产品发布 2026-02-16
Excerpt: "KimiClaw Beta是月之暗面旗下Kimi推出的AI代理服务测试版，于2026年2月16日推出。该服务基于开源AI Agent框架OpenClaw和Kimi K2.5模型，结合实用技能库，具备长期记忆、自主操作等能力，并提供云端集成……目前该功能处于早期实验阶段，首批面向Allegretto及以上会员计划的用户开放体验"
Context: 2026 年 5 月公司申请注册多枚「KimiClaw」商标 [^48^]；微博 3 月官宣接入 KimiClaw（私信发指令）。
Confidence: high

### 证据 36：Kimi Claw 云主机持续扣费（常见坑 #3）
Claim: Kimi Claw 云主机即使不主动发起任务也每天扣除约会员额度 0.6% 的沙箱运行费（每日下午 4 点结算）；不用时建议备份 memory/soul/workspace 后删除云主机 [^39^]
Source: Kimi 官方帮助页《会员套餐价格与权益对比》
URL: https://www.kimi.com/zh-cn/help/membership/membership-pricing
Date: 2026-07-29
Excerpt: "这是 Kimi Claw 云主机的沙箱运行费用。Kimi Claw 是部署在云端的 OpenClaw：每次调用 Claw，系统都会在云端启动一个隔离沙箱来执行代码、操作浏览器或调用工具。沙箱不是"免费待机"的，而是按运行时长和资源消耗持续计费——即使你没有主动发起任务，已部署的云主机仍会保留运行环境和数据，因此每天会产生约会员额度 0.6% 的费用"
Context: 官方一手说明；另「Agent Website 发布网站」每天扣约 0.08%。Allegretto 及以上会员权益含免费 Kimi-Claw [^8 系]。
Confidence: high

### 证据 37：OpenClaw 安全风险（监管层提示，适用于 Kimi Claw 底层框架）
Claim: 2026 年 3 月 10 日国家互联网应急中心（CNCERT）发布 OpenClaw 安全风险提示：默认安全配置脆弱，存在提示词注入、误操作（可彻底删除邮件/生产数据）、插件（skills）投毒、高中危漏洞四类风险，建议隔离运行环境、严管凭证与插件来源 [^46^]
Source: 新华社
URL: https://www.news.cn/tech/20260310/959f13d18edb4759ae031a5e30523d23/c.html
Date: 2026-03-10
Excerpt: "由于其默认的安全配置极为脆弱，攻击者一旦发现突破口，便能轻易获取系统的完全控制权……多个适用于OpenClaw的功能插件已被确认为恶意插件或存在潜在的安全风险，安装后可执行窃取密钥等恶意操作"
Context: 提示针对 OpenClaw 生态整体（非单独点名 Kimi Claw），但 Kimi Claw 即「部署在云端的 OpenClaw」（官方表述，证据 36），写作时应将二者关联但避免把生态风险直接等同于 Kimi Claw 已被攻破。
Confidence: high

---

## 十、相关产品：Kimi Work（桌面 Agent）

### 证据 38
Claim: Kimi Work（Beta）2026-06-03 开启公测：面向知识工作者的通用型本地 Agent，随 Mac/Windows 测试版客户端推出；内核即 Kimi Code，底层模型 K2.6，支持最多 300 子 Agent 集群；其 Beta 客户端本身由 AI 参与编写（5 万+ 行有效代码，92% 由 AI 生成，一周内完成双平台） [^47^][^55^]
Source: i黑马（腾讯新闻）；OSCHINA
URL: https://view.inews.qq.com/a/20260604A04XH200 ; https://www.oschina.net/news/451781
Date: 2026-06-04
Excerpt: "Kimi Work的内核是Kimi Code，后者是月之暗面已在本地Coding Agent领域验证了十几万日活用户的技术底座" / "累计产出超过 5 万行有效代码，其中 92% 由 AI 自主生成，Kimi工程师在一周内完成了跨Mac和Windows的双平台Beta版客户端。"
Context: 「Kimi Code 十几万日活用户」为官方在 Kimi Work 发布时披露的数字。
Confidence: high

---

## 十一、用户口碑与常见坑（汇总）

### 证据 39：额度误扣与服务稳定性事件
Claim: 4 月 K2.6 上线后出现会员排队、功能短暂不可用与权益误扣，公司将全体用户当月额度恢复至 100%；7 月 K3 上线 48 小时再次算力告急、暂停新订阅 [^56^]
Source: 新浪财经《IPO在途、会员"售罄"：Kimi需算三笔账》
URL: https://finance.sina.com.cn/wm/2026-07-20/doc-iniimzhe8307985.shtml
Date: 2026-07-20
Excerpt: "今年4月，Kimi K2.6上线后同样出现会员排队、功能短暂不可用和权益误扣，公司随后将全体用户当月额度恢复至100%。财联社当时的报道中，同样出现了"用户热情远超预期"的表述。不到三个月，相似剧情重演，服务承载力仍在追赶模型迭代速度。"
Context: 社区亦有 429 错误、响应慢等反馈 [^8 系 CSDN 横评]。
Confidence: high

### 证据 40：低档位偏紧、模型 token 消耗偏高
Claim: 社区共识：¥49/¥99 档对重度 Coding 偏紧，¥199 对个人略过剩；Andante 实测月 token 约 84M，在同价位中偏少；OpenAI 战略负责人 Dean Ball 亦指出 K3「单次任务 Token 消耗量较高，实际运行成本未必低廉」 [^202^][^941^][^53^]
Source: CSDN（两篇）；电子工程专辑
URL: https://blog.csdn.net/ab977a1081268482/article/details/162017132 ; https://devpress.csdn.net/v1/article/detail/162400039 ; https://www.eet-china.com/mp/a511083.html
Date: 2026-06-16 / 2026-06-29 / 2026-07-20
Excerpt: "社区反馈中， **¥49 / ¥99 档** 对重度 Coding 往往偏紧， **¥199** 对个人又略过剩" / "Andante 实测月 Token 约 84M，在同价位中偏少" / "他同时指出，该模型单次任务 Token 消耗量较高，实际运行成本未必低廉。"
Context: 84M 数字为第三方实测估算；Dean Ball 评价属竞品公司人士观点，但其「agentic 编程达 2026 Q1 最佳公开模型水平」的肯定部分同样值得引用。
Confidence: medium-high

### 证据 41：Kimi CLI 早期质量问题（4-5 月，多已修复）
Claim: 2026 年 4-5 月社区曾报告令牌消耗异常、会话限额、界面可读性、快捷键冲突等问题；OpenClaw 生态中出现 Kimi k2p5 工具调用参数丢失 bug（10/10 失败，因 kimi-coding 缺少 moonshot-thinking payload 兼容配置） [^29^][^50^]
Source: 百度百科「Kimi Code CLI」；GitHub openclaw/openclaw issue #53735
URL: https://baike.baidu.com/item/Kimi%20Code%20CLI/67975444 ; https://github.com/openclaw/openclaw/issues/53735
Date: 2026-07-02（词条）/ 2026-03-24
Excerpt: "在2026年4月至5月的社区反馈中，曾报告过令牌消耗异常、会话限额、界面可读性、快捷键冲突等问题，项目方对此进行了关注或修复" / issue 标题："Kimi k2p5 模型工具调用参数丢失问题"，测试表 "Kimi k2p5|10|0|10|❌ 参数丢失"
Context: CLI 为较晚进入 AI CLI 市场的产品，迭代快；第三方框架接入 Kimi 模型时 thinking 签名的兼容性是一类已知坑。
Confidence: high

### 证据 42：正面口碑
Claim: 用户与开发者口碑集中在：前端代码美观度/实用性强（「能直接生成带设计感的网站」）、商业化稳定不「背刺」老用户、重度编程场景额度耐用（高缓存命中率下 199 元档一天高强度开发仅耗当周约 30%） [^410^][^414^][^54^]
Source: 掘金实测；搜狐实测；laoyutang 博客
URL: https://juejin.cn/post/7651973052532178971 ; https://www.sohu.com/a/1051855095_122073250 ; https://blog.laoyutang.cn/openai/kimi-vs-chatgpt-plus
Date: 2026-06-17 / 2026-07-18 / 2026-05-28
Excerpt: "前端代码美观度和实用性大幅提升，能直接生成带设计感的网站" / "整个项目从需求梳理、原型设计、前后端开发，到测试和后面的几轮功能迭代，折腾了一整天，最后本周额度大概用了 30%" / "高频读代码、改代码、跑大量上下文，Kimi Code 更耐用……正常写一天代码，额度可能也就掉 2% 左右"
Context: 个人实测样本，代表性有限但多源一致；Cloudflare 官方案例称采用 K2.5 降低 77% 成本（Kimi 官方博客标题，厂商口径）。
Confidence: medium-high

---

## 十二、写给作者的 5 个要点

1. **版本线必须先纠偏再写**：截至 2026-07-31，Kimi 最新模型不是 K2.5/K2.6，而是 **Kimi K3**（7-16 深夜发布、7-27 开源权重）：2.8T 参数、896 专家激活 16、KDA 线性注意力+注意力残差新架构、1M 上下文、Modified MIT。中间还有两代容易被漏掉：**K2.6**（4-20，通用旗舰）与 **K2.7 Code**（6-12，编程专项、强制 Thinking、token 消耗 -30%，即 Kimi Code 默认模型 kimi-for-coding）。写编程工具章节时，K2.7 Code 和 K3 才是「现在时」。

2. **「Kimi 是唯一不限 5 小时窗口的 Coding Plan」已过时**。这是 2026 年 1-4 月的事实；最迟 6 月起 Kimi Code 已引入 5 小时滚动 + 7 天周期双层限额（官方帮助页 7-29 明确「Kimi Code 另有 5 小时/周限额」）。Kimi 真正的差异化是 **Token 计量 + 缓存命中不计额度**：编程场景缓存命中率可达 90%+，重度使用边际成本极低，但额度透明度差、用户难预估——「缓存命中率决定实际额度」这个坑仍在，且比窗口机制更值得写。

3. **引用基准必须分三层**：(a) 厂商自报且用自建基准（Kimi Code Bench v2、Kimi Claw 24/7 Bench）——只能用于纵向代际对比；(b) 厂商自报用外部基准（SWE-Marathon、ProgramBench）——K3 的评测各家 harness 不同（K3 用 Kimi Code、GPT 用 Codex、Claude 用 Claude Code），且 Fable 5 在 SWE-Marathon 有 35% 任务触发 fallback，官方脚注自己承认了；(c) 真正第三方——Frontend Code Arena 1679 Elo 登顶、Artificial Analysis 综合指数 57（落后 Fable 5 仅 3 分）、MCP Mark Verified 81.1 首超 Opus 4.8。建议正文以 (c) 为主。

4. **Kimi Code 工具现状的三个「坑」要写全**：① kimi-for-coding 实行客户端白名单（仅 Kimi CLI/Claude Code/Roo Code/Kilo Code 等，Cline 长期 403），工具适配数量远少于智谱；② 档位门控细碎——¥49 档不能用 K3、¥99 档 K3 只有 256K、1M 上下文和高速版要 ¥199 起，「为 1M 上下文而来」的读者实际入门价是 Allegretto；③ K3 发布 48 小时后全部付费档「售罄」、暂停 C 端新订阅（年内第二次算力事故，4 月 K2.6 也曾额度误扣），订阅制度的稳定性本身就是风险点。

5. **Kimi Claw 不是编程工具，是「云端托管版 OpenClaw」**：2026-02-16 上线的通用 AI 代理（长期记忆、远程操控电脑、ClawHub 插件、40GB 存储），Allegretto+ 专属权益；底层 OpenClaw 框架 3 月遭 CNCERT 安全风险提示（提示词注入/插件投毒/高危漏洞），且 Claw 云主机闲置也每天扣约 0.6% 会员额度。另外两个可写的生态彩蛋：Cursor Composer 2 被证实基于 K2.5 RL（马斯克亲自「认证」）；K3 的 48 小时开源 EDA 芯片设计 demo 当日砸下 Cadence/Synopsys 股价，但官方定性为 early PoC、未流片，引用时必须保留这个限定。

---

## 参考来源

[^1^] 百度百科「Kimi K2.5」https://baike.baidu.com/item/Kimi%20K2.5/67297451（2026-07-24）
[^2^] 新浪财经·券商深度《月之暗面(KIMI)：从长上下文到率先迈入万亿参数》https://stock.finance.sina.com.cn/stock/go.php/vReport_Show/kind/lastest/rptid/834286113544/index.phtml（2026-07-27）
[^3^] 51CTO 博客《2026年发布的Kimi K2.5》https://blog.51cto.com/u_13539/14632989（2026-05-26）
[^4^] 掘金《2026半年盘点：AI界发生的6件大事》https://juejin.cn/post/7652263740117319707（2026-06-18）
[^4b^] 掘金《2026年AI大模型半年报》https://juejin.cn/post/7651223863050453044（2026-06-15）
[^5^] 什么值得买《Kimi K2系列深度解析》https://post.smzdm.com/p/a95dd7no（2026-06-18）
[^6^] TheRouter《2026年5月AI新模型发布汇总》https://therouter.ai/zh/blog/may-2026-model-wave/（2026-05-05）
[^7^] 什么值得买《Kimi K2.6开源发布》https://post.smzdm.com/p/ak8eo53k（2026-05-15）
[^8^] CSDN《AI 订阅策略调研报告（2026-05-12）》https://blog.csdn.net/wwwwwwgame/article/details/161090593（2026-05-14）
[^9^] IT之家《月之暗面开源 Kimi K2.7 Code 编程模型》https://www.ithome.com/0/963/661.htm（2026-06-12）
[^10^] SegmentFault《Kimi K2.7 Code 上线》https://segmentfault.com/a/1190000047863643（2026-06-16）
[^11^] 掘金《Kimi K2.7 Code 深度拆解》https://juejin.cn/post/7650899618197225535（2026-06-14）
[^12^] 百度百科「Kimi K2.7 Code」https://baike.baidu.com/item/Kimi%20K2.7%20Code/67986864（2026-07-03）
[^13^] 北京商报（搜狐）《月之暗面上线Kimi K3模型》https://www.sohu.com/a/1051384603_115865（2026-07-17）
[^14^] 新京报贝壳财经（东方财富）《月之暗面发布2.8万亿参数模型Kimi K3》https://wap.eastmoney.com/a/202607173810197948.html（2026-07-17）
[^15^] IT之家《月之暗面开源Kimi K3 模型，2.8 万亿参数》https://www.ithome.com/0/982/259.htm（2026-07-27）
[^16^] Kimi 官方 Tech Blog《Kimi K3: Open Frontier Intelligence》https://www.kimi.com/blog/kimi-k3（2026-07）
[^17^] 东方财富《Kimi K3正式开源，阿里、华为等厂商首日适配》https://wap.eastmoney.com/a/202607283823453572.html（2026-07-28）
[^18^] Fenxi《Kimi K3: Moonshot AI's 2.8 trillion parameter model》https://fenxi.fr/en/blog/kimi-k3-moonshot-ai-architecture-benchmarks-explained/（2026-07-27）
[^20^] IT之家《Kimi K3 登顶全球榜单后，彭博社称美国 AI 领先中国固有认知被打破》https://www.ithome.com/0/978/670.htm（2026-07-19）
[^21^] ShengyaYun 编译《Kimi K3 与鹈鹕基准测试的启示》（含 Artificial Analysis 摘要）https://www.shengyayun.com/blog/english-translation-2026-07-18/（2026-07-18）
[^22^] CSDN AI编程社区《Kimi K3 深度解析》https://aicoding.csdn.net/6a5af9ab10ee7a33f28ea86c.html（2026-07-18）
[^23^] 新浪科技微博《Kimi K3 API 涨价》https://www.sina.cn/news/detail/5321623272167138.html（2026-07-17）
[^24^] 搜狐《Kimi K3发布：2.8万亿参数全球最大开源模型，月之暗面为何敢卖这个价》https://www.sohu.com/a/1051436889_122920010（2026-07-17）
[^25^] 新浪财经《月之暗面发布Kimi K3（48小时芯片分析）》https://www.sina.cn/news/detail/5322758776946810.html（2026-07-20）
[^26^] SmartHey（全文转载官方公告）《Kimi K3爆火致算力告急，即日起暂停C端新用户订阅》https://www.smarthey.com/detail/286231203112.html（2026-07-19）
[^27^] 观察者网《Kimi紧急叫停新订阅》https://www.guancha.cn/economy/2026_07_21_824589.shtml（2026-07-21）
[^28^] 新浪财经（新财富）《Kimi不再便宜》https://finance.sina.com.cn/roll/2026-07-27/doc-inikfsuy8461071.shtml（2026-07-27）
[^29^] 百度百科「Kimi Code CLI」https://baike.baidu.com/item/Kimi%20Code%20CLI/67975444（2026-07-02）
[^30^] MarkTechPost《Moonshot AI Releases Kimi Code CLI》https://www.marktechpost.com/2026/06/06/moonshot-ai-releases-kimi-code-cli-a-terminal-ai-coding-agent-built-in-typescript-for-next-gen-agents/（2026-06-06）
[^31^] GitHub MoonshotAI/kimi-code https://github.com/MoonshotAI/kimi-code
[^32^] Kimi Code CLI 官方文档《在 IDE 中使用》https://moonshotai.github.io/kimi-cli/zh/guides/ides.html
[^33^] GitHub Discussion #2323（Cline 白名单请求）https://github.com/MoonshotAI/kimi-cli/discussions/2323（2026-05-18）
[^34^] TRAE 官方中文社区（含 kimi 官方白名单说明）https://forum.trae.cn/t/topic/25283（2026-06-16）
[^35^] 博客园《2026年国内主流AI Coding Plan套餐全对比》https://www.cnblogs.com/wzxNote/p/19648084（2026-02-27）
[^36^] GitHub ForceInjection《Coding Plan 成本分析报告》https://github.com/ForceInjection/forceinjection.github.io/blob/main/09_inference_system/cost_analysis/coding_plan/coding_plan_report.md（2026-04-18）
[^37^] 塔猴速递《国内大模型厂商 Token/Coding Plan 汇总对比》https://www.tahou.com/article/202245162112700421（2026-04-01）
[^38^] CodeAgentSwarm《Kimi Code Plans and Pricing: Every Tier Explained (2026)》https://www.codeagentswarm.com/en/guides/kimi-code-plans-and-pricing（2026-07-18）
[^39^] Kimi 官方帮助页《会员套餐价格与权益对比》https://www.kimi.com/zh-cn/help/membership/membership-pricing（2026-07-29）
[^40^] 什么值得买《Kimi改用Token计费后，用户为何越用越焦虑？》https://post.smzdm.com/p/az846klp（2026-06-21）
[^41^] CodingPlan.org《Kimi Code Plan 详解》https://codingplan.org/plans/kimi
[^42^] Coding-Plan.org 国内 AI 编程套餐横评 https://coding-plan.org/（2026-07-18）
[^43^] 80aj（Linux.do 社区）《Kimi Coding Plan实测：K3模型高负载下的额度消耗与真实成本分析》https://www.80aj.com/2026/07/20/kimi-coding-plan-k3-cost-analysis/（2026-07-20）
[^44^] CSDN《K3 与 Kimi Code 实战：模型到终端 Agent》https://blog.csdn.net/2611_96382751/article/details/163014954（2026-07-19）
[^45^] 百度百科「Kimi Claw Beta」https://baike.baidu.com/item/Kimi%20Claw%20Beta/67406551（2026-07-24）
[^46^] 新华社《国家互联网应急中心发布关于OpenClaw安全应用的风险提示》https://www.news.cn/tech/20260310/959f13d18edb4759ae031a5e30523d23/c.html（2026-03-10）
[^47^] i黑马（腾讯新闻）《Kimi Work桌面端公测，定位通用型本地Agent》https://view.inews.qq.com/a/20260604A04XH200（2026-06-04）
[^48^] 百度百科「北京月之暗面科技股份有限公司」https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E6%9C%88%E4%B9%8B%E6%9A%97%E9%9D%A2%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/63575472（2026-07-30）
[^49^] china3dprint《Cursor发布新模型"Composer 2"疑套壳》https://www.china3dprint.com/archives/4198.html（2026-03-21）
[^50^] GitHub openclaw/openclaw issue #53735《Kimi k2p5 模型工具调用参数丢失问题》https://github.com/openclaw/openclaw/issues/53735（2026-03-24）
[^51^] MagicNetWorld《Kimi Code CLI》https://magicnetworld.com/tools/kimi-code/（2026-07-24）
[^52^] GLBGPT《Kimi K3 Pricing: API Costs, Subscription Plans》https://www.glbgpt.com/hub/zh/kimi-k3-pricing/（2026-07-21）
[^53^] 电子工程专辑《每日瞰AI（OpenAI 战略负责人评价 Kimi K3）》https://www.eet-china.com/mp/a511083.html（2026-07-20）
[^54^] 老鱼塘博客《Kimi 200 元三档会员 vs ChatGPT Plus》https://blog.laoyutang.cn/openai/kimi-vs-chatgpt-plus（2026-05-28）
[^55^] OSCHINA《月之暗面Kimi Work 开启公测》https://www.oschina.net/news/451781（2026-06-04）
[^56^] 新浪财经《IPO在途、会员"售罄"：Kimi需算三笔账》https://finance.sina.com.cn/wm/2026-07-20/doc-iniimzhe8307985.shtml（2026-07-20）
[^57^] MornAI《Kimi K3全解析》https://www.mornai.cn/news/llm/kimi-k3-full-analysis-agent-coding-flagship/（2026-07-17）
[^58^] ChooseAI《Kimi网页版怎么用？最新指南》https://www.chooseai.net/news/5222/（2026-07-21）
[^59^] O's World《在 OpenCode 中免费体验 Kimi K2.5 模型》https://ooo.run/post/try-kimi-k25-free-in-opencode.html（2026-06-24）
[^106^] AICXD《月之暗面在 GTC 2026 披露 Kimi K2.5 技术路线》https://aicxd.com/ai-hot/article/91877（2026-07-18）
[^189^] AI-Nav《Kimi 开放平台定价》https://www.ai-nav.store/tools/moonshot-kimi（2026-07-27）
[^202^] CSDN《Kimi K2.7 Code 发布并开源：编程专项大升级，高速版今日上线》https://blog.csdn.net/ab977a1081268482/article/details/162017132（2026-06-16）
[^410^] 掘金《编程卷王 Kimi K2.7 Code 上线！一手实测》https://juejin.cn/post/7651973052532178971（2026-06-17）
[^414^] 搜狐《Kimi K3，夯爆了！编程直逼 Fable 5 和 GPT-5.6》https://www.sohu.com/a/1051855095_122073250（2026-07-18）
[^941^] CSDN《2026年6月28日 主流Coding Plan平台全面对比》https://devpress.csdn.net/v1/article/detail/162400039（2026-06-29）

---

## 调研方法与局限

- 本报告基于 21 组独立检索（中文为主），优先采用官方页面（kimi.com 帮助页、官方 Tech Blog、GitHub MoonshotAI）、新华社/财联社/新京报/北京商报/IT之家等权威媒体；内容农场类来源仅在多源交叉一致时采用并已标注。
- 主要不确定点：① K2.7 Code 总参数存在 1T vs 1.1T 两种口径；② K3 激活参数约 104B 为媒体口径，未见技术报告原文确认；③ Kimi Code CLI 两代仓库协议不同（Apache-2.0 / MIT），部分二手资料混淆；④ 会员档位权益在 K3 发布后处于调整期（售罄、权益拆分），书中付印前需以 kimi.com 官网最新页面复核；⑤ K2.5「LMSYS 登顶」为多家媒体一致表述，未逐一核对 Arena 官方快照。
