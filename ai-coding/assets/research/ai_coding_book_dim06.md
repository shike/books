# 维度06：DeepSeek 现状与其在 AI 编程中的定位（截至2026年7月）

> 调研日期：2026-07-31。检索方法：24 组独立搜索（中文为主）+ 直接抓取 DeepSeek 官方 API 文档（pricing / updates / news）等一手页面。
> 重要时效提示：调研当天（2026-07-31）DeepSeek 刚刚发布 **DeepSeek-V4-Flash 正式版**（API 公测），V4-Pro 正式版尚未发布——本书付印前务必复核。
> 对任务背景的两点修正：①"V3.2 是当前主力"已过时——2026-04-24 V4 预览版发布后 API 主力已切换至 V4 系列，旧名 deepseek-chat/deepseek-reasoner 已于 2026-07-24 退役；②"V3.2 定价 0.27/1.10 美元"与官方价格不符（详见 §4 定价条目，0.27/1.10 是 2025 年初 V3 时代的美元价，V3.2 官方价为 2元/3元人民币每百万 token，约合 0.28/0.42 美元）。

---

## 一、版本与发布

**证据 1.1**
- Claim: DeepSeek-V3.2 正式版于 2025-12-01 发布，同时发布 V3.2-Speciale，API 的 deepseek-chat / deepseek-reasoner 分别对应其非思考/思考模式 [^1^][^2^]
- Source: DeepSeek API Docs（更新日志 & V3.2 发布公告）
- URL: https://api-docs.deepseek.com/updates ; https://api-docs.deepseek.com/zh-cn/news/news251201
- Date: 2025-12-01
- Excerpt: "Both `deepseek-chat` and `deepseek-reasoner` have been upgraded to DeepSeek-V3.2. - `deepseek-chat` corresponds to DeepSeek-V3.2's **non-thinking mode** - `deepseek-reasoner` corresponds to DeepSeek-V3.2's **thinking mode**"
- Context: 官方一手更新日志。V3.2 是"融入思考推理"的正式版模型，官方称推理类 Benchmark 达 GPT-5 水平、仅略低于 Gemini-3.0-Pro [^3^]
- Confidence: high

**证据 1.2**
- Claim: V3.2 的前身为 2025-09-29 发布的实验版 V3.2-Exp，首次引入 DeepSeek 稀疏注意力（DSA），架构上这是相对 V3.1-Terminus 的唯一改动；API 价格同步下调 50% 以上 [^4^]
- Source: DeepSeek API Docs（Introducing DeepSeek-V3.2-Exp）
- URL: https://api-docs.deepseek.com/news/news250929
- Date: 2025-09-29
- Excerpt: "Built on V3.1-Terminus, it debuts DeepSeek Sparse Attention (DSA) for faster, more efficient training & inference on long context. … 💰 API prices cut by 50%+!"
- Context: 官方一手公告。DSA 后被智谱 GLM-5 等第三方模型复用（2026-02）
- Confidence: high

**证据 1.3**
- Claim: DeepSeek-V4 预览版于 2026-04-24 正式发布并开源（MIT 协议），含 V4-Pro（1.6T 总参/49B 激活）与 V4-Flash（284B/13B）两个 MoE 模型，均支持 1M 上下文，预训练 33T/32T token [^5^]
- Source: DeepSeek API Docs（DeepSeek V4 Preview Release）
- URL: https://api-docs.deepseek.com/news/news260424
- Date: 2026-04-24
- Excerpt: "🚀 **DeepSeek-V4 Preview** is officially live & open-sourced! Welcome to the era of cost-effective 1M context length. 🔹 **DeepSeek-V4-Pro:** 1.6T total / 49B active params. Performance rivaling the world's top closed-source models. 🔹 **DeepSeek-V4-Flash:** 284B total / 13B active params."
- Context: 官方一手公告。同日 OpenAI 发布 GPT-5.5，形成正面对垒 [^6^]
- Confidence: high

**证据 1.4**
- Claim: 旧 API 模型名 deepseek-chat / deepseek-reasoner 于 2026-07-24 完全退役，此前已分别路由至 deepseek-v4-flash 的非思考/思考模式 [^5^][^1^]
- Source: DeepSeek API Docs
- URL: https://api-docs.deepseek.com/news/news260424
- Date: 2026-04-24（公告）；2026-07-24（生效）
- Excerpt: "⚠️ Note: deepseek-chat & deepseek-reasoner will be fully retired and inaccessible after Jul 24th, 2026, 15:59 (UTC Time). (Currently routing to deepseek-v4-flash non-thinking/thinking)."
- Context: 意味着截至 2026-07-31，DeepSeek 官方 API 仅提供 deepseek-v4-pro 与 deepseek-v4-flash 两个型号
- Confidence: high

**证据 1.5**
- Claim: 2026-07-31，DeepSeek-V4-Flash 正式版（DeepSeek-V4-Flash-0731）API 上线公测，架构与参数量同预览版一致、仅重新后训练；V4-Pro 正式版"将尽快发布"，App/网页端未更新 [^7^][^8^]
- Source: 财新网；DeepSeek API Docs 更新日志
- URL: https://www.caixin.com/2026-07-31/102470229.html ; https://api-docs.deepseek.com/updates
- Date: 2026-07-31
- Excerpt: "DeepSeek-V4-Flash-0731 keeps the same model architecture and size as DeepSeek-V4-Flash-Preview, and was only re-post-trained. … **The official release of DeepSeek-V4-Pro will follow soon.**"（官方更新日志）；财新："DeepSeek-V4的预览版在4月24日发布，按大小分为Pro和Flash两个版本。其中，Pro版本总参数量为1.6T，激活参数为49B，成为当时参数量最大的开源权重模型"
- Context: 正式版较官方 6 月预告的"7月中旬"跳票约两周；公测仅限 API
- Confidence: high

---

## 二、架构（MoE、稀疏注意力、上下文窗口）

**证据 2.1**
- Claim: V4 采用 CSA（压缩稀疏注意力）+ HCA（高度压缩注意力）混合注意力架构，结合 DSA；1M 上下文下 V4-Pro 单 token 推理 FLOPs 仅为 V3.2 的 27%、KV cache 为 10%；V4-Flash 为 10% 和 7% [^9^]
- Source: 百度百科"DeepSeek-V4技术报告"词条（引述官方55页技术报告《DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence》）
- URL: https://baike.baidu.com/item/DeepSeek-V4%E6%8A%80%E6%9C%AF%E6%8A%A5%E5%91%8A/67719806
- Date: 2026-06-02（词条）
- Excerpt: "报告摘要指出，在百万级token上下文设定下，与DeepSeek-V3.2相比，DeepSeek-V4-Pro仅需其27%的单token推理FLOPs，以及10%的KV缓存；更经济的V4-Flash版本则将这两个数字分别压到了10%和7%"
- Context: 二手转述一手技术报告；同内容亦见安全内参深读 [^10^]。其他技术点：mHC 流形约束超连接、Muon 优化器（替代 AdamW）、MoE 专家层 FP4 + 其余 FP8 混合精度
- Confidence: high

**证据 2.2**
- Claim: V3 系列（V3/V3.1/V3.2）为 671B 总参/37B 激活、128K 上下文；V4 将上下文提至 1M（约为 V3.2 的 8 倍）[^11^]
- Source: GitHub 社区版本谱系整理（deepseek-mechanism-atlas，含 arXiv 编号）；CSDN 转载的 V4 对比文
- URL: https://github.com/fooSynaptic/deepseek-mechanism-atlas/blob/main/docs/reports/deepseek-version-lineage-20260625.md ; https://blog.csdn.net/dotaherox/article/details/161409976
- Date: 2026-06-25 / 2026-05-26
- Excerpt: "|**DeepSeek-V3.2**|2025-12|同 V3.1-T|同 V3.1-T|128K|…|**唯一架构改动** 即为稀疏注意力| … |**DeepSeek-V4-Pro**|2026|1.6T|49B|**1M**|DeepSeek|2606.19348|CSA + HCA + mHC + Muon；MoE FP4|"
- Context: 社区整理，与官方公告数字一致；CSDN 文中"V3 发布时间 2024年12月"等细节与官方一致，但个别表述（如"V4 API 输入 1 元/百万 token"）混用 Pro/Flash，引用时需注意
- Confidence: medium

---

## 三、编程基准表现（区分厂商自报与第三方）

### 3.1 厂商自报（官方口径）

**证据 3.1.1**
- Claim: 官方自报：V4-Pro-Max 在 SWE-bench Verified 80.6%（与 Claude Opus 4.6 持平）、Codeforces 评分 3206（超 GPT-5.4 的 3168，人类选手榜第 23）、LiveCodeBench 93.5%、Terminal Bench 2.0 67.9%；并自承"发展轨迹大约落后最前沿闭源模型 3 到 6 个月" [^12^][^5^]
- Source: 量子位（智源社区转载，引官方技术报告与官方推文）；DeepSeek API Docs
- URL: https://hub.baai.ac.cn/view/54241 ; https://api-docs.deepseek.com/news/news260424
- Date: 2026-04-26 / 2026-04-24
- Excerpt: "论文中，DeepSeek表示：'DeepSeek-V4-Pro-Max在标准推理benchmark上优于GPT-5.2和Gemini-3.0-Pro，但略落后于GPT-5.4和Gemini-3.1-Pro。这表明其发展轨迹大约落后最前沿闭源模型3到6个月。' … 官方推文：'目前DeepSeek-V4已成为公司内部员工使用的Agentic Coding模型，据评测反馈使用体验优于Sonnet 4.5，交付质量接近Opus 4.6非思考模式，但仍与Opus 4.6思考模式存在一定差距。'"
- Context: 厂商自报数据；官方难得地自曝差距，可信度高
- Confidence: high

**证据 3.1.2**
- Claim: 官方内部 R&D Coding Benchmark（50 多名工程师、约 200 个真实研发任务筛出 30 题）上，V4-Pro-Max 通过率 67%，高于 Claude Sonnet 4.5 的 47%、接近 Opus 4.5 的 70% [^10^]
- Source: 安全内参（secrss，引 V4 技术报告）
- URL: https://www.secrss.com/articles/89756
- Date: 2026-04-26
- Excerpt: "报告说，DeepSeek 从 50 多名内部工程师那里收集了约 200 个真实研发任务，覆盖功能开发、bug 修复、重构、诊断，技术栈包括 PyTorch、CUDA、Rust、C++。经过筛选后，保留 30 个任务作为评测集。DeepSeek-V4-Pro-Max 在该 benchmark 上通过率为 67%，高于 Claude Sonnet 4.5 的 47%，接近 Opus 4.5 的 70%。"
- Context: 厂商自建内部评测，非独立第三方，引用时应标注"官方内部评测"
- Confidence: high（对"官方如此声称"而言）

**证据 3.1.3**
- Claim: 官方自报：V4-Flash 正式版（0731）Agent 能力大幅增强，9 项基准"远超 V4-Pro 预览版"：Terminal Bench 2.1 82.7、DeepSWE 54.4、Cybergym 76.7、Toolathlon verified 70.3 等；测试使用"DeepSeek Harness 极简模式（即将发布）"作为框架 [^1^]
- Source: DeepSeek API Docs 更新日志
- URL: https://api-docs.deepseek.com/updates
- Date: 2026-07-31
- Excerpt: "**Significantly enhanced agent capabilities, with benchmark results far exceeding V4-Pro-Preview:** - Terminal Bench 2.1: 82.7 - NL2Repo: 54.2 - Cybergym: 76.7 - DeepSWE: 54.4 … Note 1: For the Code Agent tasks in the public benchmark sets, the official DeepSeek-V4-Flash was tested using the DeepSeek Harness minimal mode (to be released soon) as the framework"
- Context: 注意自报口径使用了自家 Harness 框架与 max effort，横向比较时不可与其他模型的裸调数据直接对比。财新同日报道指出：Terminal Bench 2.1 的 82.7 与 GLM-5.2 一致、不及 Kimi K3 的 88.3；DeepSWE 54.4 高于 GLM-5.2 的 46.2、低于 Kimi K3 的 67.5 [^7^]
- Confidence: high

### 3.2 第三方独立评测

**证据 3.2.1**
- Claim: 第三方（LushBinary 发布 24 小时内横评）：DeepSeek V4-Pro Max 在 SWE-bench Pro 55.4%（GPT-5.5 58.6%、Claude Opus 4.7 64.3%）、Terminal-Bench 2.0 67.9%（GPT-5.5 82.7%）；但 LiveCodeBench 93.5 与 Codeforces 3206 领先 [^13^]
- Source: 腾讯新闻（引独立评测机构 LushBinary 三方横评）
- URL: https://view.inews.qq.com/a/20260425A077HM00
- Date: 2026-04-25
- Excerpt: "| SWE-bench Pro（真实工程） | 55.4% | 58.6% | 64.3% | | Terminal-Bench 2.0（Agent工作流） | 67.9% | 82.7% | 69.4% | | LiveCodeBench（算法竞赛） | 93.5 | — | 88.8 |"
- Context: 第三方数据与 DataCamp 口径一致（SWE-Bench Pro：Claude 64.3% > GPT-5.5 58.6% > V4 Pro 55.4%）[^14^]。结论：竞赛型代码能力顶尖，真实工程/Agent 工作流仍逊于最新闭源旗舰——与任务背景中"代码生成被 GPT-5.4/Claude Opus 4.6 等超越"的定性吻合（注意：对标的闭源版本已迭代至 GPT-5.5 / Opus 4.7）
- Confidence: medium-high

**证据 3.2.2**
- Claim: Artificial Analysis 智能指数：V4-Pro 获 52 分（V3.2 为 42 分），为仅次于 Kimi K2.6 的全球第二大开源推理模型；V4-Flash 47 分；但 AA-Omniscience 幻觉率 V4-Pro 约 94%、V4-Flash 约 96%（V3.2 为 82%），在顶级模型中最高 [^15^][^16^]
- Source: 新浪财经（引 Artificial Analysis）；博客园（cnblogs 三榜齐发）
- URL: https://finance.sina.cn/stock/jdts/2026-04-25/detail-inhvsuvi0881323.d.html ; https://www.cnblogs.com/AlayaNeW/articles/19946995
- Date: 2026-04-25 / 2026-04-28
- Excerpt: "V4-Pro在人工分析智能指数中斩获52分，相较V3.2版本的42分实现10分跃升，成为仅次于Kimi K2.6的全球第二大开源推理模型。"（新浪）；"根据Artificial Analysis 在 2026 年 4 月 24 日发布的测试……在 AA-Omniscience 测试中，V4 Pro 的幻觉率约为 94%，V4 Flash 约为 96%，在所有顶级大模型中排名第1和第3"（cnblogs）
- Context: 第三方负面数据，作者写"适用场景"时必须纳入：事实核查敏感场景（法律、医疗、合同）慎用
- Confidence: high

**证据 3.2.3**
- Claim: 截至 2026 年 6 月下旬，DeepSeek V4 Pro 在 LiveBench 综合排名第 15、LMArena Agent 榜第 16、LMArena WebDev 榜第 24，落后于 GLM-5.2（分别第 7/10/2）等国产新旗舰 [^17^]
- Source: CSDN 博客（引 LiveBench / LMArena 榜单截图）
- URL: https://blog.csdn.net/weixin_43764974/article/details/162395364
- Date: 2026-06-28
- Excerpt: "在LiveBench上综合排名第7（Qwen 3.7 Max 第13，DeepSeek V4 Pro 第15，Kimi K2.7 Code 第21）…… 在LMArena 的Agent能力中排名第10（DeepSeek V4 Pro 第16……）…… 在LMArena 的WebDev能力中排名第2（……DeepSeek V4 Pro 第24）"
- Context: 第三方众包/动态榜单，反映 V4 预览版发布两个月后即被国产竞品在主观偏好榜上反超；榜单随时间变动，书中引用需注明截取时间
- Confidence: medium

**证据 3.2.4**
- Claim: Artificial Analysis 2026-07-31 更新的智能指数给 V4-Flash-0731（最高推理档）50 分，明显高于同类可比模型中位数 17 分；但完成评测生成 2.1 亿 token，输出量显著偏高（可比模型中位数 6200 万）[^8^]
- Source: 观察者网（引 Artificial Analysis）
- URL: https://www.guancha.cn/economy/2026_07_31_825764.shtml
- Date: 2026-07-31
- Excerpt: "海外模型评测机构Artificial Analysis在7月31日更新的智能指数测试中，给予V4-Flash-0731（最高推理档位）50分。在同类可比模型中明显高于平均水平，其可比模型的中位数为17分。而Artificial Analysis在进行智能指数评测时，V4-Flash-0731共生成了2.1亿个Token，输出量明显偏高，可比模型的中位数则为6200万个Token。"
- Context: 第三方当日评测；"高 token 消耗"是 DeepSeek 模型实际成本的隐藏变量（详见 §7 口碑）
- Confidence: high

---

## 四、API 定价

**证据 4.1**
- Claim: V4 官方定价（2026-04-24 起）：deepseek-v4-pro 输入 $0.145（缓存命中）/$1.74（未命中）、输出 $3.48；deepseek-v4-flash 输入 $0.028/$0.14、输出 $0.28（均为每百万 token 美元价）[^^5^]
- Source: DeepSeek API Docs（V4 Preview Release，内嵌价格表）
- URL: https://api-docs.deepseek.com/news/news260424
- Date: 2026-04-24
- Excerpt: "deepseek-v4-pro | $0.145 | $1.74 | $3.48 | 1M ; deepseek-v4-flash | $0.028 | $0.14 | $0.28"
- Context: 官方一手价格表。第三方（Mashable/OpenRouter）口径一致：V4 输入 1.74/输出 3.48 美元，对比 GPT-5.5 为 5/30、Claude Opus 4.7 为 5/25 [^14^][^18^]
- Confidence: high

**证据 4.2**
- Claim: 官方定价页预告将实行峰谷定价：高峰时段（北京时间每日 9:00–12:00、14:00–18:00）所有计费项价格为常规价 2 倍；Responses API 目前仅支持 deepseek-v4-flash，v4-pro 支持将于 2026 年 8 月初加入 [^19^]
- Source: DeepSeek API Docs（Models & Pricing）
- URL: https://api-docs.deepseek.com/quick_start/pricing
- Date: 抓取于 2026-07-31
- Excerpt: "(1) The Responses API currently only supports the `deepseek-v4-flash` model, and does not yet support the `deepseek-v4-pro` model. We will add support for the `deepseek-v4-pro` model in early August 2026. (2) The DeepSeek API service will soon adopt a peak/off-peak pricing policy. During peak hours, prices will be 2x the regular prices, applicable to all billing items."
- Context: 官方一手。与量子位"破天荒涨价"报道（2026-07-01，正式版涨价、峰值 2 倍）互证 [^20^]——作者写"性价比"叙事时需纳入这一变化
- Confidence: high

**证据 4.3**
- Claim: V3.2 时代官方价格（2025-09-29 起）：缓存命中输入 0.2 元、未命中输入 2 元、输出 3 元/百万 token（人民币），较此前下调 50%+（原命中 0.5 元/未命中 4 元/输出 12 元）[^^21^]
- Source: 财联社（新浪转载）
- URL: https://finance.sina.com.cn/stock/t/2025-09-29/doc-infseiwf8262587.shtml
- Date: 2025-09-29
- Excerpt: "在缓存命中的情况下，输入价格由0.5元/百万token降低为0.2元。在缓存未命中的情况下，输入价格由4元/百万token减低为2元。输出价格则从12元/百万token大幅降低为3元。"
- Context: 权威媒体转官方公告。修正背景中"0.27/1.10 美元"的说法：那是 2025 年 2 月 V3 优惠期结束后的美元折算价（2元/8元）；第三方聚合站 devtk.ai 2026-05 仍将 V3.2（legacy）标为 $0.27/$1.10 [^22^]，与官方人民币价（2元/3元 ≈ $0.28/$0.42）的输出项不符，应以官方为准
- Confidence: high

**证据 4.4**
- Claim: 2026-05-31 起，V4-Pro 的 2.5 折限时优惠转为常态化定价（即原定价的 1/4）；V4-Flash 输入低至 0.2 元/百万 token（缓存命中）[^^23^]
- Source: 快科技（mydrivers，引 DeepSeek 官方 5 月 22 日宣布）
- URL: https://news.mydrivers.com/1/1124/1124689.htm
- Date: 2026-05-25
- Excerpt: "5月22日晚间，DeepSeek官方宣布，DeepSeek-V4-Pro模型API的价格将于2026年5月31日结束2.5折优惠活动后，正式调整为原定价的四分之一。这意味着此前的限时优惠已从短期促销转向常态化定价安排。"
- Context: "原定价"指公告中的标价（$1.74/$3.48 量级）；具体落地价格以官方定价页为准
- Confidence: medium-high

**证据 4.5**
- Claim: 国内云厂商转售价格（火山方舟）：deepseek-v4-pro 输入 12 元/输出 24 元每百万 token；deepseek-v4-flash 输入 1 元/输出 2 元；deepseek-v3.2 输入 2–4 元/输出 3–6 元（分档）[^^24^]
- Source: 火山方舟官方文档
- URL: https://www.volcengine.com/docs/82379/1544106
- Date: 文档页面（抓取于 2026-07-31）
- Excerpt: "deepseek-v4-pro​|-​|12.00​|-​|0.017​|1.00​|-​|24.00​| … deepseek-v4-flash​|-​|1.00​|-​|0.017​|0.20​|-​|2.00​|"
- Context: 国内开发者大量经由云平台调用 DeepSeek，转售价格与官方直连不同，书中若给成本测算需注明渠道
- Confidence: high

---

## 五、DeepSeek 在 AI 编程工作流中的实际角色

### 5.1 作为 Claude Code / Cline / Codex 等工具的后端模型

**证据 5.1.1**
- Claim: DeepSeek 官方提供 Anthropic 兼容端点（https://api.deepseek.com/anthropic），Claude Code 只需改环境变量即可切换后端至 DeepSeek；官方 V4 公告明确"已与 Claude Code、OpenClaw、OpenCode 等主流 AI 智能体无缝集成" [^5^][^25^]
- Source: DeepSeek API Docs；腾讯云开发者社区教程
- URL: https://api-docs.deepseek.com/news/news260424 ; https://cloud.tencent.com/developer/article/2653743
- Date: 2026-04-24 / 2026-04-12
- Excerpt: 官方："🔹 DeepSeek-V4 is seamlessly integrated with leading AI agents like Claude Code, OpenClaw & OpenCode."；教程：""ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic", "ANTHROPIC_MODEL": "deepseek-reasoner" … DeepSeek 提供了与 Anthropic API 格式完全兼容的接口"
- Context: 社区教程进一步给出档位映射实践：Opus/Sonnet 档映射 deepseek-v4-pro、Haiku 档映射 deepseek-v4-flash [^26^]
- Confidence: high

**证据 5.1.2**
- Claim: 2026-07-31 发布的 V4-Flash 正式版首次原生支持 Responses API，并针对 OpenAI Codex 做了适配 [^8^][^1^]
- Source: 观察者网；DeepSeek API Docs
- URL: https://www.guancha.cn/economy/2026_07_31_825764.shtml
- Date: 2026-07-31
- Excerpt: "另一方面，这次更新还有值得关注的地方，是DeepSeek首次原生支持Responses API，并针对Codex进行了适配。"
- Context: 标志 DeepSeek 从"兼容 Anthropic 协议"扩展到"兼容 OpenAI 最新 Responses 协议"，同时进入两大编程智能体生态
- Confidence: high

**证据 5.1.3**
- Claim: DeepSeek 已成海外推理平台与 Agent 框架的常驻选项（Fireworks、Together、Ollama），并进入腾讯 WorkBuddy 等国产桌面 Agent 的内置模型列表 [^27^][^28^]
- Source: 人人都是产品经理；火山引擎开发者社区
- URL: https://www.woshipm.com/ai/6419515.html ; https://developer.volcengine.com/articles/7665936353855635519
- Date: 2026-06-24 / 2026-07-23
- Excerpt: "DeepSeek 已经是 Fireworks、Together、Ollama 这些海外推理平台的常驻选项"；"内置11种主流国产模型，包括腾讯混元Hy3、智谱GLM-5.2、Kimi-K2.7-Code、DeepSeek-V4等，用户可自由切换"
- Context: 说明 DeepSeek 在工作流中的角色是"被集成的基础模型供应商"，而非终端工具本身
- Confidence: high

### 5.2 国内 Coding Plan 聚合平台中的地位

**证据 5.2.1**
- Claim: 2026 年国内 Coding Plan（包月编程订阅）市场爆发，DeepSeek 是各家套餐的标配模型：火山方舟 Coding Plan 支持 DeepSeek-V3.2/V4-Flash/V4-Pro；无问芯穹聚合平台（¥19.9/月起）含 deepseek-v3.2；讯飞星火套餐含 DeepSeek-V3.2 并对 V4-Pro 限时 2.5 倍用量 [^29^][^30^]
- Source: 博客园（六大平台横评）；codingplan.fyi 对比工具；火山引擎官方
- URL: https://www.cnblogs.com/jzssuanfa/p/20098883 ; https://www.codingplan.fyi/ ; https://www.volcengine.com/article/37781
- Date: 2026-05-20 / 2026-07-01 / 2026-04-09
- Excerpt: "当前主流平台包括火山方舟（字节跳动）、阿里云百炼、MiniMax、Kimi（月之暗面）、智谱GLM五大厂商，以及新兴的无问芯穹（Infini）聚合平台"；火山官方："订阅后，开发者可通过两种方式配置DeepSeek-V3.2模型……在Claude Code、Cursor、Cline（VSCode）等工具的配置文件中，直接设置Model Name为 deepseek-v3.2"
- Context: 关键格局判断：DeepSeek 自己没有推出官方包月 Coding Plan（仅有按量 API），其在国内编程订阅市场的存在完全依托第三方平台转售；套餐里 DeepSeek 与 GLM、Kimi、MiniMax 并列，是可替换选项之一
- Confidence: high

### 5.3 调用量与市场份额（用脚投票的证据）

**证据 5.3.1**
- Claim: OpenRouter 官方博客：DeepSeek 在平台的 token 份额从 2026 年 1 月的约 9%（2–3 月一度跌至 5%）升至 6 月初的近 20%，5 月中旬起成为 OpenRouter 第一大模型；增长主要由 agentic 工作负载驱动 [^18^]
- Source: OpenRouter 官方博客
- URL: https://openrouter.ai/blog/insights/deepseek-v4-adoption/
- Date: 2026-06-30
- Excerpt: "By the start of June, DeepSeek had earned nearly 20% of token share and has been the top model on OpenRouter since mid-May. … DeepSeek V4 Flash, on the cheapest endpoint, costs $0.09 input / $0.18 output per million tokens. For comparison, GPT-5.5 is currently priced at $5 input / $30 output per million tokens."
- Context: 一手平台数据（样本：2026-01-01 至 06-14 超 450 万亿 token）。份额指 token 量而非金额——低价模型的花费份额远低于用量份额
- Confidence: high

**证据 5.3.2**
- Claim: Mozilla《2026 开源 AI 现状报告》：基于 OpenRouter 2026 年 6 月数据，DeepSeek V4 Flash 以 18.4T token 月消耗量居 API 调用榜首，前五名均为开源模型；开源与闭源模型能力平均差距 3.3%，差距集中在推理、长上下文检索与智能体任务 [^31^]
- Source: Mozilla 报告（aioga 转述/IT之家）
- URL: https://www.aioga.com/news/cmrlppdld00kdbih5h26221vs/
- Date: 2026-07-15
- Excerpt: "基于 2026 年 6 月全球最大 AI 聚合平台 OpenRouter 数据，在 API 调用月消耗量 Tokens 方面，前五名均为开源模型，其中 DeepSeek V4 Flash 凭借 18.4T Tokens 位居榜首；小米 Mimo-V2.5 以 14.9T Tokens 位居第二；腾讯 Hy3 Preview 模型以 14.8T Tokens 位居第三。"
- Context: 权威基金会报告，二手转述；报告原文 stateofopensource.ai
- Confidence: medium-high

**证据 5.3.3**
- Claim: 2026 年 7 月初，中国大模型周调用量达 23.45 万亿 token、连续 10 周超美国；DeepSeek-V4-Flash 连续 3 周蝉联 OpenRouter 调用榜首，国产模型占 OpenRouter 约 60% 使用量 [^32^]
- Source: 掘金科技日报（引财联社/智源社区）
- URL: https://juejin.cn/post/7660007537018830875
- Date: 2026-07-09
- Excerpt: "中国 AI 大模型周调用量已达 23.45 万亿 Token，连续 10 周超越美国。DeepSeek-V4-Flash 连续 3 周蝉联 OpenRouter 调用榜首，国产模型整体占据 OpenRouter 60% 使用量。"
- Context: 媒体聚合数据，与 OpenRouter 官方博客趋势一致
- Confidence: medium

---

## 六、公司动态：融资、IPO、人才、战略

### 6.1 融资与 IPO

**证据 6.1.1**
- Claim: DeepSeek 首轮融资 2026 年 5 月底签署完成，规模超 500 亿元人民币（约 74 亿美元）：梁文锋个人出资 200 亿（最大单一出资方）、腾讯 100 亿、宁德时代 50 亿、网易/京东/IDG 各 30 亿、国家 AI 产业基金 10 亿；投后估值约 520 亿美元；除国家基金外投资方仅享分红权、无董事会席位，股份锁 5 年，梁文锋掌握近 78% 控制权 [^33^][^34^]
- Source: 《财经》（新浪转载"融资实录"）；观察者网
- URL: https://finance.sina.com.cn/roll/2026-06-18/doc-inicuyvv3333148.shtml ; https://www.guancha.cn/economy/2026_05_06_816054.shtml
- Date: 2026-06-18 / 2026-05-06
- Excerpt: "据媒体报道，本轮融资超500亿元，约合74亿美元。其中，梁文锋个人出资200亿元……腾讯出资100亿元，宁德时代出资50亿元，网易、京东和IDG资本分别出资30亿元，国家人工智能产业投资基金出资10亿元。……首轮融资结束后DeepSeek投前估值约3500亿元，但加上增发5%的ESOP（员工期权池），实际投前估值约为3675亿元，约合543亿美元。"
- Context: 成立三年首次对外融资，此前坚持"不融资、不上市、不商业化"；估值路径：4 月传闻 100 亿美元 → 首轮投后 520 亿 → 7 月二轮投前 710 亿美元
- Confidence: high

**证据 6.1.2**
- Claim: 2026-07-14（FT 报道），DeepSeek 启动第二轮融资洽谈，投前估值约 710 亿美元（约 4800 亿元人民币），较首轮投后涨 37%，计划募资至少 100 亿元 [^35^]
- Source: 钛媒体（引英国《金融时报》）
- URL: https://www.tmtpost.com/8066516.html
- Date: 2026-07-16
- Excerpt: "据英国《金融时报》7月14日报道，公司已开始接触新投资者，投前估值约710亿美元（约合人民币4800亿元），较首轮投后上涨37%。计划募资至少100亿元，实际可能数倍于此。"
- Context: 任务背景"估值100亿美元"仅为 4 月初传闻起点，已严重过时；最新口径是 710 亿美元投前
- Confidence: high

**证据 6.1.3**
- Claim: DeepSeek 被传冲刺 A 股科创板 IPO：依托上交所 6 月 17 日 AI 大模型第五套上市标准，已启动会计师尽调，力争 2026 年 12 月底前备齐财务申报资料，目标 2027 年挂牌 [^36^]
- Source: 36氪
- URL: https://www.36kr.com/p/3896949637695363
- Date: 2026-07-19
- Excerpt: "上市选址上，DeepSeek放弃港股通道选择内地科创板，核心依托6月17日上交所出台的AI大模型专属第五套上市标准……公司也已启动会计师尽调，力争12月底前备齐全套财务申报资料。"
- Context: 媒体报道（"或冲刺"），非公司官宣；交易所、募资额、承销商均未定
- Confidence: medium

### 6.2 人才流动

**证据 6.2.1**
- Claim: 2025 下半年至 2026 上半年至少 5 名核心研发成员离职：郭达雅（R1 核心研究员→字节 Seed Agent 负责人）、王炳宣（初代大模型核心作者→腾讯混元）、罗福莉（V2 关键开发者→小米 MiMo 负责人）、魏浩然（OCR 核心→百度）、阮翀（多模态核心→元戎启行首席科学家）[^^37^]
- Source: 36氪（2026-07-09）；EET/SECCW（2026-06-26）
- URL: https://36kr.com/p/3888085124184709
- Date: 2026-07-09
- Excerpt: "从2025年下半年到2026年上半年，DeepSeek至少有5名核心研发成员确认离职。DeepSeek-R1的核心研究员郭达雅，去了字节跳动的Seed团队；第一代大模型的核心作者王炳宣，加入了腾讯的混元团队；DeepSeek早期成员罗福莉，被小米创始人雷军亲自下场、以千万元级别的年薪挖走……此外还有魏浩然、阮翀等人，也先后离开。"
- Context: 权威媒体确认；是融资（建立股权激励）的重要动因之一
- Confidence: high

**证据 6.2.2**
- Claim: 反向证据：《财经》梳理 27 篇论文 391 位署名作者，标注离职者 25 人（6.4%）；高频署名前 15 人仅 2 人离职；V3 论文 86 人中 71 人仍出现在 V4 论文名单中——"人才流失"定性至少目前不成立，属正常流动 [^38^]
- Source: 财经网（《财经》杂志）
- URL: https://m.caijing.com.cn/s/202605/5158438
- Date: 2026-05-08
- Excerpt: "DeepSeek 27篇论文中出现频率最高的15个人，仅有2人离职。DeepSeek LLM发布时的86人，仍有71位出现在DeepSeek-V4论文的名单中。……27篇论文累计出现的391位作者，明确标注'*'的离职人数仅25人，占比6.4%。"
- Context: 写作时两组数据应并置：明星个体流失属实，但团队整体稳定性高；同期公司全员扩招一倍（33 岗位）
- Confidence: high

### 6.3 战略重心：Coding Agent 为第一优先级 + Harness 团队（DeepSeek Code）

**证据 6.3.1**
- Claim: 梁文锋 2026-05-20 近四小时投资人会议（录音 7 月中旬流出）：明确不做视频/3D/世界模型，多模态定位组件而非主线；"当前优先级最高的是 Coding Agent，其次是通用 Agent"；商业化只做基础设施（API、私有化部署、算力赋能），不做 SaaS 与 ToC 产品；已采购华为 950 超节点 [^39^]
- Source: DOIT《算力"芯"动向》（会议实录整理）
- URL: https://www.doit.com.cn/ai/830104315560005.html
- Date: 2026-07-23
- Excerpt: "多模态被定位为组件而非主线，当前优先级最高的是Coding Agent，其次是通用Agent，金融、医疗等垂直领域Agent的优先级反而较低。……明确不做SaaS应用、不推出ToC端产品，不与客户直接竞争，所有商业化均通过API、私有化部署、底层算力赋能完成，只做基础设施提供商。"
- Context: 一手会议实录的二手整理；回答"DeepSeek 战略重心"的最直接证据：押注 Coding Agent 与持续学习（"通向 AGI 的核心门槛"）
- Confidence: medium-high

**证据 6.3.2**
- Claim: DeepSeek 于 2026 年 3 月新设 Harness 团队，对标 Anthropic Claude Code，打造"DeepSeek Code Harness"；负责人崔添翼（浙大计算机、ACM 金牌、Jane Street 9 年、TSY Capital 联创）；公式"Model + Harness = Agent"；团队持续急招研究员/工程师/产品经理 [^40^][^41^]
- Source: 36氪；凤凰网科技/IT之家
- URL: https://36kr.com/p/3888085124184709 ; https://h5.ifeng.com/c/vivoArticle/v0024--DOjN9tgZP2Uu4VXbjdM7SwpegWYwHnDbc7or2XqzE__
- Date: 2026-07-09 / 2026-06-23
- Excerpt: "崔添翼是DeepSeek Harness团队的负责人。Harness是今年3月新成立的团队，聚焦代码智能体产品研发，奉行一个简洁的公式：'Model + Harness = Agent'。……这个团队要对标Anthropic的智能体编程工具Claude Code，要做的是'DeepSeek Code Harness'。"
- Context: 资深研究员陈德里 5 月 20 日 X 平台证实"从零构建 Code Harness，或可叫 DeepSeek Code"；截至 7 月底产品仍在冲刺、未上线 [^42^]
- Confidence: high

---

## 七、用户口碑与适用场景

**证据 7.1（正面：性价比与中文）**
- Claim: 开发者实测（Linux.do 社区）：V4 Pro 开最大思考深度约 1 小时完成 30 个文件的重构修改，总费用 8.35 元人民币（Claude Opus 预估 30 元以上）；PingCAP CTO 黄东旭已将日常 Hermes 工作流迁移至 V4，称"整体语言能力比 Opus 和 GPT 更符合中文母语者的使用习惯" [^43^][^44^]
- Source: 80aj（转 Linux.do 实测）；CSDN（霍格沃兹测试开发学社）
- URL: https://www.80aj.com/2026/04/27/deepseek-v4-programming-test/ ; https://agent.csdn.net/6a293bbc10ee7a33f27a8255.html
- Date: 2026-04-27 / 2026-05-12
- Excerpt: "在处理一个工程量大但逻辑不复杂的任务时，DeepSeek V4在开启最大思考深度的模式下，耗时约1小时完成了30个文件的修改……该项目总费用仅为8.35元人民币"；"我已经把自己的Hermes工作流迁移到DeepSeek V4上……'整体语言能力比Opus和GPT更符合中文母语者的使用习惯'"
- Context: 个体实测，样本小但具体；适合"日常任务可直接切换"的口碑证据
- Confidence: medium

**证据 7.2（负面：幻觉、长上下文稳定性、过度标记）**
- Claim: V4 预览版两个多月用户反馈集中三点：幻觉率偏高（自信但不靠谱）；百万上下文实际稳定性不收敛，agent workflow 中上下文堆积+多轮工具调用时"容易不稳定或直接炸掉"；复杂代码任务过度保守、代码审查中"过度标记问题"（把正常逻辑当 bug）[^^20^]
- Source: 量子位（智源社区转载）
- URL: https://hub.baai.ac.cn/view/55980
- Date: 2026-07-01
- Excerpt: "一个是幻觉率偏高。……一个是超长上下文的实际稳定性还不够收敛。V4是'百万上下文窗口'，但实际体验并不尽如人意。上下文堆积、复杂推理或多轮工具调用叠加时容易不稳定或直接炸掉……在真实代码审查类测试里，V4会出现明显的'过度标记问题'，也就是把大量正常逻辑当成潜在bug来提示。"
- Context: 与 Artificial Analysis 幻觉数据（94%/96%）互证；官方内部调查亦称 52%（另一处口径 91%）开发者认为 V4-Pro 可作主力编程模型——技术报告第 44 页的两个数字在不同二手报道中不一致，引用需回查原报告 [^9^][^12^]
- Confidence: high

**证据 7.3（负面：服务稳定性）**
- Claim: 2026 年 2 月 28 日与 3 月 29 日 DeepSeek 两次大规模宕机（后者持续近 12 小时），过去 15 个月至少 7 次显著宕机；2025 年日活增长 66.7% 而算力仅增 8.3%，供需失衡 [^45^][^46^]
- Source: 腾讯云开发者社区；51CTO
- URL: https://cloud.tencent.com/developer/article/2648143 ; https://www.51cto.com/article/839479.html
- Date: 2026-03-30 / 2026-03-31
- Excerpt: "过去15个月里，它至少出现7次显著宕机，要么是被恶意攻击，要么是用户量激增、服务器过载"；"2025年DeepSeek日活增长了66.7%，但算力只增长了8.3%"
- Context: 企业生产环境选型的关键风险项；V4 预览版阶段官方 API RPM 限制紧（免费 10 RPM、付费 60 RPM）[^47^]
- Confidence: medium-high

**证据 7.4（从业者综合评价）**
- Claim: Pine AI 首席科学家李博杰：V4-Pro 工具调用与世界知识"基本追平前沿模型次一档（约 Claude 4.6 Sonnet 水平）"，但工具调用稳定性+幻觉是硬伤，需 Harness 层补足；V4-Flash 是 200B–300B 档位做垂直微调后训练的"首选基座" [^48^]
- Source: 36氪（10 位从业者访谈）
- URL: https://m.36kr.com/p/3788151000751364
- Date: 2026-04-29
- Excerpt: "V4-Pro的工具调用能力和通用世界知识，基本追平了前沿模型的次一档版本（大致相当于Claude 4.6 Sonnet水平）；但工具调用稳定性+幻觉率仍然是硬伤——这两点必须在Agent Harness层面补足……Flash会成为做业务微调的首选基座。"
- Context: 具名从业者的结构化评价，适合作为书中"适用场景"小节的主证据
- Confidence: medium-high

---

## 八、国产算力适配（与编程定位相关的供应侧背景）

**证据 8.1**
- Claim: V4 技术报告首次将华为昇腾 NPU 与英伟达 GPU 写入同一份硬件验证清单（"我们在英伟达GPU和华为昇腾NPU两个平台上均验证了细粒度EP方案"）；发布当天 8 家国产芯片厂商（昇腾、寒武纪、海光、摩尔线程、沐曦、昆仑芯、平头哥、天数智芯）完成 Day 0 适配；官方预告下半年昇腾 950 超节点批量上市后 Pro 价格将大幅下调 [^49^][^50^]
- Source: 每日经济新闻（腾讯新闻转载）；芯师爷（新浪转载）
- URL: https://view.inews.qq.com/a/20260424A08F2S00 ; https://www.sina.cn/news/detail/5293694748985614.html
- Date: 2026-04-24 / 2026-05-01
- Excerpt: "DeepSeek首次在官方技术报告中，把华为昇腾NPU和英伟达GPU写进了同一份硬件验证清单。'我们在英伟达GPU和华为昇腾NPU两个平台上均验证了细粒度EP（专家并行）方案。'这标志着万亿参数级别的模型首次在正式文档中完成了对国产AI芯片的'官方认定'。"
- Context: 每经同时注明"已确认完成推理适配（不一定基于昇腾950训练）"——避免写成"V4 完全由国产芯片训练"。另据 36 氪报道，V4 延期半年的重要原因是训练框架向昇腾迁移与内部决策分歧 [^51^]
- Confidence: high

---

## 九、写给作者的 3–5 个要点

1. **时间线必须更新**：截至 2026-07-31，"V3.2 是当前主力"已不成立。正确表述是：V3.2（2025-12-01）→ V4 预览版（2026-04-24，Pro 1.6T/49B + Flash 284B/13B，均 1M 上下文、MIT 开源）→ 旧 API 名 7 月 24 日退役 → V4-Flash 正式版 7 月 31 日公测（Agent 能力大涨、原生 Responses API + Codex 适配），**V4-Pro 正式版未发**，截稿前需复核。同时把"估值 100 亿美元"更新为"首轮投后 520 亿、二轮投前 710 亿美元（FT 2026-07-14）"。

2. **编程定位的一句话版本**：DeepSeek 不是编程工具，而是"被集成的基础设施"——官方 Anthropic/OpenAI 双协议兼容端点使其成为 Claude Code、Codex、Cline、OpenClaw 的廉价后端；国内它自己不卖 Coding Plan，靠火山方舟、无问芯穹等平台转售；OpenRouter token 份额半年翻倍至近 20%、5 月起居榜首，V4-Flash 是全球调用量最大的模型。叙事主线应是"性价比换份额"，而非"能力登顶"。

3. **基准表述要分层**：竞赛/单点代码能力（Codeforces 3206、LiveCodeBench 93.5、SWE-Verified 80.6）确属开源第一、逼近闭源；但第三方在真实工程与 Agent 工作流上（SWE-bench Pro 55.4% vs Opus 4.7 64.3%，Terminal-Bench 2.0 67.9% vs GPT-5.5 82.7%，LMArena WebDev 第 24）仍落后——且对标对象已迭代到 GPT-5.5/Opus 4.7/Gemini-3.1-Pro。官方自承"落后前沿 3–6 个月"，可直接引用，比二手吹捧更可信。引用 V4-Flash 正式版成绩时注意其用了自家 Harness 框架，非裸模型数据。

4. **三个必须写入的"坑"**：①幻觉率（AA-Omniscience：V4-Pro 94%、V4-Flash 96%，远高于 V3.2 的 82%）——事实敏感场景慎用；②Token 消耗畸高（AA 评测 2.1 亿 token vs 中位 6200 万），低单价不等于低总成本；③服务稳定性（15 个月 7 次宕机、峰谷 2 倍定价新政、预览版期 RPM 限制）。这些是从业者访谈与第三方评测反复出现的共识。

5. **战略叙事抓手**：梁文锋 5·20 投资人会议把 Coding Agent 列为最高优先级、明确"不做视频/3D/世界模型、不做 SaaS 和 ToC"，同时 3 月组建 Harness 团队对标 Claude Code（"Model + Harness = Agent"，崔添翼挂帅）——DeepSeek 正从"模型厂"向"模型+智能体脚手架"演进，DeepSeek Code 产品是 2026 下半年最值得跟踪的变量；人才侧用"明星流失属实（郭达雅/王炳宣/罗福莉/魏浩然/阮翀）+ 论文署名 6.4% 离职率"双口径并置，避免单向度的"流失"或"稳定"结论。

---

## 参考来源

[^1^]: DeepSeek API Docs — Change Log. https://api-docs.deepseek.com/updates （抓取 2026-07-31）
[^2^]: DeepSeek API Docs — DeepSeek V3.2 正式版：强化Agent能力，融入思考推理. https://api-docs.deepseek.com/zh-cn/news/news251201
[^3^]: 腾讯新闻 — DeepSeek-V3.2发布，推理能力达到了GPT-5水平. https://news.qq.com/rain/a/20251201A080EP00 （2025-12-01）
[^4^]: DeepSeek API Docs — Introducing DeepSeek-V3.2-Exp. https://api-docs.deepseek.com/news/news250929
[^5^]: DeepSeek API Docs — DeepSeek V4 Preview Release. https://api-docs.deepseek.com/news/news260424
[^6^]: 掘金 — AI 日报 2026-04-24. https://juejin.cn/post/7632135814106988586
[^7^]: 财新网 — DeepSeek-V4-Flash正式版发布 智能体基准测试远超V4-Pro预览版. https://www.caixin.com/2026-07-31/102470229.html
[^8^]: 观察者网 — DeepSeek V4正式版来了，但只来了一半. https://www.guancha.cn/economy/2026_07_31_825764.shtml
[^9^]: 百度百科 — DeepSeek-V4技术报告. https://baike.baidu.com/item/DeepSeek-V4%E6%8A%80%E6%9C%AF%E6%8A%A5%E5%91%8A/67719806
[^10^]: 安全内参 — DeepSeek-V4技术报告深读：百万上下文开源模型. https://www.secrss.com/articles/89756
[^11^]: GitHub fooSynaptic/deepseek-mechanism-atlas — deepseek-version-lineage. https://github.com/fooSynaptic/deepseek-mechanism-atlas/blob/main/docs/reports/deepseek-version-lineage-20260625.md
[^12^]: 智源社区（量子位）— DeepSeek V4报告太详尽了！484天换代之路全公开. https://hub.baai.ac.cn/view/54241
[^13^]: 腾讯新闻 — DeepSeek V4便宜9倍却输了最关键一局. https://view.inews.qq.com/a/20260425A077HM00
[^14^]: Studio Global — GPT-5.5、Claude Opus 4.7、Kimi K2.6、DeepSeek V4 基准对比. https://www.studioglobal.ai/zh-cn/discover/reports/gpt-5-5-claude-opus-4-7-kimi-k2-6-deepseek-v4-69eddd15dfe0645c91295fce
[^15^]: 新浪财经 — 海外评测DeepSeek-V4：智能体任务排名开源第一，幻觉率上升. https://finance.sina.cn/stock/jdts/2026-04-25/detail-inhvsuvi0881323.d.html
[^16^]: 博客园 — 三榜齐发，杀入前十！DeepSeek V4的真实水平到底如何？ https://www.cnblogs.com/AlayaNeW/articles/19946995
[^17^]: CSDN — GLM-5.2 性能跻身第一梯队. https://blog.csdn.net/weixin_43764974/article/details/162395364
[^18^]: OpenRouter Blog — DeepSeek V4 Is Earning Agentic Token Share. https://openrouter.ai/blog/insights/deepseek-v4-adoption/
[^19^]: DeepSeek API Docs — Models & Pricing. https://api-docs.deepseek.com/quick_start/pricing （抓取 2026-07-31）
[^20^]: 智源社区（量子位）— 破天荒！DeepSeek V4正式版居然要涨价. https://hub.baai.ac.cn/view/55980
[^21^]: 财联社（新浪转载）— DeepSeek-V3.2-Exp官宣发布，API价格下调超50%. https://finance.sina.com.cn/stock/t/2025-09-29/doc-infseiwf8262587.shtml
[^22^]: devtk.ai — DeepSeek V3.2 (legacy) API Pricing. https://devtk.ai/en/models/deepseek-v3-2/
[^23^]: 快科技 — 全球AI大模型周调用量五连涨 DeepSeek-V4-Flash登顶. https://news.mydrivers.com/1/1124/1124689.htm
[^24^]: 火山方舟文档 — 模型价格. https://www.volcengine.com/docs/82379/1544106
[^25^]: 腾讯云开发者社区 — Claude Code 接入DeepSeek 完整指南. https://cloud.tencent.com/developer/article/2653743
[^26^]: 博客园 — 手把手教你给Claude Code配置deepseek v4. https://www.cnblogs.com/youring2/p/20017622
[^27^]: 人人都是产品经理 — 别骂国产大模型了，老外们正用得不亦乐乎. https://www.woshipm.com/ai/6419515.html
[^28^]: 火山引擎开发者社区 — 2026国内AI Agent工具清单. https://developer.volcengine.com/articles/7665936353855635519
[^29^]: 博客园 — 2026年国产AI编程Coding Plan深度横评. https://www.cnblogs.com/jzssuanfa/p/20098883
[^30^]: Coding Plan 对比工具. https://www.codingplan.fyi/
[^31^]: aioga（IT之家/Mozilla）— Mozilla 2026 开源 AI 报告. https://www.aioga.com/news/cmrlppdld00kdbih5h26221vs/
[^32^]: 掘金 — 科技AI资讯日报 2026-07-09. https://juejin.cn/post/7660007537018830875
[^33^]: 《财经》（新浪转载）— DeepSeek融资实录. https://finance.sina.com.cn/roll/2026-06-18/doc-inicuyvv3333148.shtml
[^34^]: 观察者网 — 国家大基金领投DeepSeek？最新估值达到450亿美元. https://www.guancha.cn/economy/2026_05_06_816054.shtml
[^35^]: 钛媒体 — DeepSeek最新估值4800亿. https://www.tmtpost.com/8066516.html
[^36^]: 36氪 — DeepSeek或冲刺A股IPO，4800亿估值引行业热议. https://www.36kr.com/p/3896949637695363
[^37^]: 36氪 — 华为天才少年与DeepSeek冲突背后，梁文锋的人才观是什么？ https://36kr.com/p/3888085124184709
[^38^]: 财经网 — DeepSeek核心人才真的在流失吗？27篇论文里藏着答案. https://m.caijing.com.cn/s/202605/5158438
[^39^]: DOIT — 梁文锋四小时投资人会议. https://www.doit.com.cn/ai/830104315560005.html
[^40^]: 凤凰网科技（快科技）— DeepSeek Harness负责人坦言每日不停面试招人. https://h5.ifeng.com/c/vivoArticle/v0024--DOjN9tgZP2Uu4VXbjdM7SwpegWYwHnDbc7or2XqzE__
[^41^]: 36氪 — 梁文锋挖来一位学弟. https://m.36kr.com/p/3819926608204164
[^42^]: 淘宝大学 — DeepSeek Code 模型即将上线. https://daxue.taobao.com/information/detail.jhtml?id
[^43^]: 80aj — 开发者实测DeepSeek V4编程. https://www.80aj.com/2026/04/27/deepseek-v4-programming-test/
[^44^]: CSDN — 开源 vs 闭源的差距正在收窄，DeepSeek-V4做到了. https://agent.csdn.net/6a293bbc10ee7a33f27a8255.html
[^45^]: 腾讯云开发者社区 — 崩了近12小时！DeepSeek突发大规模宕机. https://cloud.tencent.com/developer/article/2648143
[^46^]: 51CTO — DeepSeek连续宕机背后：V4真的要来了？ https://www.51cto.com/article/839479.html
[^47^]: CSDN — DeepSeek V4 预览版实测：4 家 API 聚合平台延迟与稳定性横评. https://blog.csdn.net/ofoxcoding/article/details/160562211
[^48^]: 36氪 — 别急着All-in DeepSeek V4，先看看这10位从业者的真心话. https://m.36kr.com/p/3788151000751364
[^49^]: 每日经济新闻（腾讯新闻转载）— 万亿参数模型DeepSeek-V4"解锁"国产芯片. https://view.inews.qq.com/a/20260424A08F2S00
[^50^]: 芯师爷（新浪转载）— 8家国产芯无缝衔接DeepSeek-V4. https://www.sina.cn/news/detail/5293694748985614.html
[^51^]: 中国经营报 — DeepSeek何以拥有定价权. http://dianzibao.cb.com.cn/html/2026-05/04/content_340059.htm
