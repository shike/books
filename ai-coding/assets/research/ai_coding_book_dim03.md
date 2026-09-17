# 维度03：智谱AI（Z.ai）GLM-5 系列 与 Z Code 编程工具现状（截至 2026-07-31）

- 调研日期：2026-07-31
- 方法：31 次独立中文/英文搜索 + 直接打开智谱官方文档（docs.bigmodel.cn）3 页；一手来源优先（官方文档、财新、澎湃、证券时报、科创板日报、36氪、钛媒体、IT之家），社区/内容站仅作佐证并标注低置信度。
- 注意：本文件所有"跑分"均区分【厂商自报】与【第三方】；价格均注明币种与来源日期，AI 行业调价频繁，引用前需复核官网。

---

## A. GLM-5（2026 年 2 月发布）

### 证据 A1：GLM-5 于 2026-02-11 深夜/02-12 正式发布并开源，定位复杂系统工程与长程 Agent 任务
Claim: 智谱于 2026 年 2 月 11 日深夜发布、2 月 12 日正式上线并开源新一代旗舰基座模型 GLM-5，此前曾以"Pony Alpha"匿名在 OpenRouter 测试 [^1^][^2^]
Source: 财新网 / 36氪
URL: https://www.caixin.com/2026-02-12/102413861.html ; https://m.36kr.com/p/3679611307617928
Date: 2026-02-12 / 2026-02-11
Excerpt: "智谱数日前就在国外开源社区上线了GLM-5，但命名为pony（赛马）。在市场资金追捧下，2月9日、10日两个交易日，智谱股价分别涨36%、14%。GLM-5正式发布的2月12日，智谱港股高开8%。"（财新）；"2月12日，智谱正式发布并开源新一代旗舰基座模型 GLM-5，定位为面向复杂系统工程与长程Agent任务的基座模型……几周前，开源社区曾流传一个名为Pony Alpha的模型……Pony Alpha正是GLM-5的匿名测试版本。"（36氪）
Context: 发布窗口为 2 月 11 日深夜至 2 月 12 日（媒体两个日期均有，官方发布记录记 2 月 12 日）。 GLM-5 主打"Agentic Engineering（智能体工程）"叙事，对标"从 Vibe Coding 到 Agentic Engineering"的范式转移。
Confidence: high

### 证据 A2：GLM-5 官方规格——744B 总参/40B 激活、28.5T 预训练数据、首次集成 DeepSeek 稀疏注意力、Slime 异步强化学习框架
Claim: GLM-5 参数规模从 GLM-4.7 的 355B（激活 32B）扩展至 744B（激活 40B），预训练数据 23T→28.5T，首次集成 DeepSeek Sparse Attention，并构建"Slime"异步智能体强化学习框架 [^3^]
Source: 智谱AI开放文档（官方）GLM-5 模型页
URL: https://docs.bigmodel.cn/cn/guide/models/text/glm-5
Date: 2026-07-30（页面抓取日期）
Excerpt: "参数规模扩展：从 355B（激活 32B）扩展至 744B（激活 40B），预训练数据从 23T 提升至 28.5T……异步强化学习：构建全新的 'Slime' 框架……提出异步智能体强化学习算法，使模型能够持续从长程交互中学习……稀疏注意力机制：首次集成 DeepSeek Sparse Attention，在维持长文本效果无损的同时，大幅降低模型部署成本，提升 Token Efficiency"
Context: 官方文档还给出架构细节（78 层隐藏层、256 专家、每 token 激活 8 个、稀疏度 5.9% 等见于百度百科转述官方资料）。"异步智能体强化学习"即"原生智能体"能力的训练侧来源——GLM-5 从设计上是 agent-native 模型，而非后期缝合。
Confidence: high

### 证据 A3：GLM-5 编程基准（厂商自报）：SWE-bench-Verified 77.8%、Terminal Bench 2.0 56.2，官方称"对齐 Claude Opus 4.5"
Claim: GLM-5 在 SWE-bench-Verified 与 Terminal Bench 2.0 分获 77.8 与 56.2 的开源最高分，官方宣称编程能力对齐 Claude Opus 4.5（厂商自报）[^3^]
Source: 智谱AI开放文档（官方）GLM-5 模型页
URL: https://docs.bigmodel.cn/cn/guide/models/text/glm-5
Date: 2026-07-30（页面抓取日期）
Excerpt: "在 SWE-bench-Verified 和 Terminal Bench 2.0 中分别获得 77.8 和 56.2 的开源模型最高分数，性能表现超过 Gemini 3.0 Pro。在内部 Claude Code 评估集合中，GLM-5 在前端、后端、长程任务等编程开发任务上显著超越 GLM-4.7……使用体验逼近 Opus 4.5。"
Context: 注意 77.8% 是 SWE-bench **Verified**，与 GLM-5.1/5.2 宣传的 SWE-bench **Pro**（58.4/62.1）是两套不同基准，写作时勿混用。财新引述榜单称 GLM-5 综合能力列全球第四（次于 Claude Opus 4.6、GPT-5.2、Claude Opus 4.5）。
Confidence: high（数字为厂商自报口径）

### 证据 A4：GLM-5 全程在约 10 万块华为昇腾 910B 上训练，未使用 NVIDIA GPU
Claim: GLM-5 全程在 10 万块华为昇腾 910B 芯片上完成训练，"没碰过一块 NVIDIA GPU" [^4^]
Source: 钛媒体（TMTPost）
URL: https://www.tmtpost.com/agent/ai-article?id=18274
Date: 2026-06-17
Excerpt: "今年2月11日，智谱AI（已更名为Z.ai）发布了GLM-5——一个744B总参数、40B激活参数的MoE混合专家模型。……更重要的是，它全程在10万块华为昇腾910B芯片上完成训练——没碰过一块NVIDIA GPU。发布当天，智谱港股单日暴涨26%，一周内累计上涨约70%——市场对全华班芯片训出前沿模型的故事给出了直接定价。"
Context: 这是"GLM-5 是首个完全用华为昇腾芯片训练的前沿模型"线索的主要来源之一；第三方 API 文档站（API易）称 GLM-5.1 同样"完全使用 100,000 颗华为昇腾 910B 芯片训练"（低权威来源，中等置信）。"首个"限定词多见于媒体表述，官方口径为"训练与推理均未依赖海外算力"。
Confidence: medium-high（10 万块 910B 为媒体数字，建议向智谱核实）

---

## B. GLM-5.1（2026 年 4 月发布）

### 证据 B1：GLM-5.1 于 2026-04-08 正式发布并开源（注意：任务线索中的 04-09 有误）
Claim: GLM-5.1 正式发布并开源的日期是 2026 年 4 月 8 日；部分媒体记为 4 月 7 日（或为海外/平台上线时间差），4 月 9 日为媒体集中报道日 [^5^][^6^][^7^]
Source: 东方财富网（转证券时报）/ 澎湃新闻 / 百度百科"智谱GLM-5.1"
URL: https://finance.eastmoney.com/a/202604083697753675.html ; https://m.thepaper.cn/newsDetail_forward_32923133 ; https://baike.baidu.com/item/%E6%99%BA%E8%B0%B1GLM-5.1/67544623
Date: 2026-04-08
Excerpt: "4月8日，智谱正式发布GLM-5.1，并宣布正式开源。二级市场上，港股开盘后智谱大涨，一度涨近18%，股价触及925港元……GLM-5.1是全球第一个在真实工程任务中验证了8小时持续工作能力的开源模型。"（证券时报/东方财富）；"2026年4月8日，智谱正式发布新一代开源模型 GLM-5.1。同日，该模型上线华为云，并完成与华为云多款产品的对接。"（百度百科）
Context: 钛媒体与部分社区帖记为 4 月 7 日（可能对应 z.ai 海外发布或 Coding Plan 开放时间）；CSDN 有文章称 3 月 27 日已面向 Coding Plan 用户开放、4 月 6/7 日开源权重。正式对外发布+开源口径以 4 月 8 日为主流权威口径。任务背景中的"2026-04-09"应修正。
Confidence: high（4 月 8 日）；medium（4 月 7 日并存口径）

### 证据 B2：GLM-5.1 官方规格——200K 上下文、128K 最大输出、单次任务可持续自主工作 8 小时
Claim: GLM-5.1 上下文窗口 200K、最大输出 128K，官方宣称可在单次任务中持续自主工作长达 8 小时，完成"规划—执行—测试—修复—交付"闭环 [^8^]
Source: 智谱AI开放文档（官方）GLM-5.1 模型页
URL: https://docs.bigmodel.cn/cn/guide/models/text/glm-5.1
Date: 2026-07-30（页面抓取日期）
Excerpt: "GLM-5.1 是智谱面向复杂代码与长程任务场景打造的高性能模型，代码能力大大增强，长程任务显著提升，能够在单次任务中持续、自主地工作长达 8 小时，完成从规划、执行到迭代优化的完整闭环，交付工程级成果。……上下文窗口：200K；最大输出 Tokens：128K"
Context: 官方还给出三个工程案例：8 小时从零构建完整 Linux 桌面系统；655 轮自主迭代将向量数据库查询吞吐提升至初始版本 6.9 倍；KernelBench Level 3 千轮工具调用实现 3.6 倍几何平均加速（对比 torch.compile max-autotune 的 1.49 倍）。定位"构建 Autonomous Agent 与长程 Coding Agent 的理想基座"。
Confidence: high（能力描述为厂商口径）

### 证据 B3：GLM-5.1 编程基准（厂商自报）：SWE-bench Pro 58.4，号称超 GPT-5.4、Claude Opus 4.6、Gemini 3.1 Pro
Claim: GLM-5.1 在 SWE-bench Pro 取得 58.4，官方称"刷新全球最佳表现"，三大代码基准综合平均分"全球第三、国产第一、开源第一"（厂商自报）[^8^][^9^]
Source: 智谱AI开放文档 / IT之家
URL: https://docs.bigmodel.cn/cn/guide/models/text/glm-5.1 ; https://www.ithome.com/0/936/851.htm
Date: 2026-04-08 / 2026-07-30
Excerpt: "在 SWE-Bench Pro 基准测试中，GLM-5.1 取得 58.4 的成绩，超过 GPT-5.4、Claude Opus 4.6 和 Gemini 3.1 Pro，刷新全球最佳表现。"（官方文档）；"下图是业内最具代表性的三个代码评测基准的平均结果，包括衡量模型专业软件开发工作的 SWE-Bench Pro、操作命令行解决问题的 Terminal-Bench 2.0、从零构建完整代码仓库的 NL2Repo，GLM-5.1 取得全球模型第三、国产模型第一、开源模型第一。"（IT之家附官方介绍）
Context: 同期竞品分数（官方图表）：GPT-5.4 57.7、Claude Opus 4.6 57.3。注意官方图为"三大基准平均"，单看 SWE-bench Pro 的 58.4 领先幅度很小（约 0.7 分）。
Confidence: high（数字为厂商自报口径）

### 证据 B4：GLM-5.1 第三方验证——Artificial Analysis Coding Agent Index 开源第一（在 Claude Code 中运行）
Claim: 2026 年 5 月 Artificial Analysis 发布 Coding Agent Index，GLM-5.1（在 Claude Code 中运行）取得开源第一（第三方）[^10^]
Source: 百度百科"智谱GLM-5.1"（转述评测机构发布）
URL: https://baike.baidu.com/item/%E6%99%BA%E8%B0%B1GLM-5.1/67544623
Date: 2026-07-24（词条更新）；事件 2026-05-12
Excerpt: "2026年5月12日消息，全球权威评测机构Artificial Analysis发布全新Coding Agent基准Artificial Analysis Coding Agent Index，用于衡量Agent harnesses与模型的组合在SWE-Bench-Pro-Hard-AA、Terminal-Benchv2和SWE-Atlas-QnA主流基准上的表现。其中，GLM-5.1（在ClaudeCode运行）取得开源第一。"
Context: 这是少数针对"Agent 框架+模型"组合的第三方实测，比厂商自报基准更有说服力，适合在书中引用。
Confidence: medium-high（建议直接引用 Artificial Analysis 原页复核）

### 证据 B5：GLM-5.1 发布同步提价 10%，缓存命中价格逼近 Claude Sonnet 4.6
Claim: GLM-5.1 发布同时智谱再度提价约 10%，Coding 场景缓存命中 Token 价格接近 Claude Sonnet 4.6，为国产模型首次与海外头部厂商价格对齐 [^9^][^7^]
Source: IT之家 / 澎湃新闻
URL: https://www.ithome.com/0/936/851.htm ; https://m.thepaper.cn/newsDetail_forward_32923133
Date: 2026-04-08
Excerpt: "OpenRouter 显示，伴随此次发布，智谱 GLM 再度提价 10%。调价后，GLM-5.1 在 Coding 场景的缓存命中 Token 价格已接近 Anthropic 旗下 Claude Sonnet4.6 水平。这是国产大模型首次在核心场景实现与海外头部厂商的价格对齐。"
Context: 这是 2026 年内智谱系列提价动作之一（2 月 Coding Plan +30% 起、3 月 GLM-5-Turbo +20%、4 月 +10% 且海外 Coding Plan 涨 80%–150%，详见 C/D 节）。
Confidence: high

### 证据 B6：GLM-5.1 参数规模 754B（媒体报道口径）
Claim: GLM-5.1 总参数 754B（7540 亿），MIT 协议开源，提供 FP8 版本 [^11^]
Source: 搜狐科技（编辑部分析稿）/ CocoLoop 社区（引用 z.ai/blog/glm-5.1）
URL: https://www.sohu.com/a/1006998488_122653685 ; https://www.cocoloop.cn/t/topic/2662
Date: 2026-04-09 / 2026-04-08
Excerpt: "智谱AI于同日正式发布并开源GLM-5.1。该模型拥有7540亿参数，采用MIT许可证开放，支持200K上下文窗口。"（搜狐）；"参数与窗口：总参数量 754B，上下文 204K，单次生成上限 131K tokens。目前模型权重已在Hugging Face组织页面zai-org上架。"（CocoLoop，注明参考 https://z.ai/blog/glm-5.1）
Context: 官方文档页未直接标注参数；754B 为媒体引用官方博客/模型卡的口径（GLM-5 为 744B）。开源地址：github.com/zai-org/GLM-5、huggingface.co/zai-org/GLM-5.1、modelscope.cn/models/ZhipuAI/GLM-5.1。
Confidence: medium-high

---

## C. GLM-5.2（2026 年 6 月发布）

### 证据 C1：GLM-5.2 分两步发布——6 月 13 日 Coding Plan 全量开放，6 月 16 日公开 API/开源（MIT），财新记开源日为 6 月 17 日
Claim: GLM-5.2 于 2026-06-13 面向 GLM Coding Plan 全量用户（Lite/Pro/Max/团队版）开放，6 月 16 日开放独立 API、上线 OpenRouter 并以 MIT 协议开源权重（财新记 6 月 17 日"上线并开源"）[^12^][^13^][^14^]
Source: 36氪 / 钛媒体 / 财新
URL: https://www.36kr.com/p/3864006047929605 ; https://www.tmtpost.com/agent/ai-article?id=18274 ; https://www.caixin.com/2026-07-23/102467238.html
Date: 2026-06-22 / 2026-06-17 / 2026-07-23
Excerpt: "6月13日，国产大模型龙头智谱宣布旗下开源旗舰GLM-5.2面向其Coding Plan全量用户开放（Lite/Pro/Max及团队版），并预告API上线，同时称模型权重按MIT协议开源。"（36氪）；"6月13日17:21，GLM-5.2全量向Coding Plan用户开放。核心变化：上下文窗口从200K直接跳到100万token，输出上限131,072 token，引入High和Max两种思考深度档位，原生兼容Claude Code和OpenClaw。一周内开源权重上架HuggingFace，MIT协议，商用无限制。6月16日，登陆OpenRouter。"（钛媒体）；"2026年6月17日，智谱上线并开源GLM-5.2。"（财新）
Context: 背景是 6 月 12 日美国商务部要求 Anthropic 暂停 Claude Fable 5 / Mythos 5 对海外用户服务，智谱次日全量开放 GLM-5.2 并称"前沿智能不应只属于少数人，也不应被少数规则随时收回"。开源仓库：huggingface.co/zai-org/GLM-5.2（含 FP8 版）、modelscope.cn/models/ZhipuAI/GLM-5.2、github.com/zai-org/GLM-5。
Confidence: high

### 证据 C2：GLM-5.2 官方规格——1M（"Solid 1M 无损"）上下文、128K 最大输出、glm-5.2[1m] 变体
Claim: GLM-5.2 支持官方称"真正可用"的 1M token 上下文（模型名 glm-5.2[1m] 启用）、最大输出 128K/131,072 tokens，单次任务实测处理超 85 万 tokens（厂商口径）[^15^]
Source: 智谱AI开放文档（官方）GLM-5.2 模型页
URL: https://docs.bigmodel.cn/cn/guide/models/text/glm-5.2
Date: 2026-07-30（页面抓取日期）
Excerpt: "GLM-5.2 是面向长任务时代的旗舰模型。支持真正可用的 1M 上下文，实测可承载项目级工程上下文……GLM-5.2 实现了 Solid 1M 无损上下文，并针对长程 Coding Agent 场景进行了数月强化训练……在实际体验中，GLM-5.2 可自主完成任务拆解、架构设计、前后端开发、测试修复与部署交付，最终生成可上线的 Web、移动端和小程序应用。整个流程累计处理超过 85 万（850K）tokens，接近用满 1M 上下文窗口。"
Context: 官方定位语："一次任务即可完成'从需求到多端可部署产物'的完整开发链路"。上下文窗口字段：1M；最大输出 Tokens：128K。启用方式为模型名后缀 [1m]。
Confidence: high（规格）；medium（"无损/真正可用"为厂商承诺，第三方复测有限）

### 证据 C3：GLM-5.2 编程基准（厂商自报）：SWE-bench Pro 62.1（vs GPT-5.5 58.6、Claude Opus 4.8 69.2）、Terminal-Bench 2.1 81.0、FrontierSWE 74.4%
Claim: GLM-5.2 官方自报 SWE-bench Pro 62.1，超 GPT-5.5（58.6）但低于 Claude Opus 4.8（69.2）；Terminal-Bench 2.1 81.0；FrontierSWE 74.4% 仅落后 Opus 4.8 约 1%；SWE-Marathon 13.0% 落后 Opus 4.8 约 13 个百分点（厂商自报）[^15^]
Source: 智谱AI开放文档（官方）GLM-5.2 模型页
URL: https://docs.bigmodel.cn/cn/guide/models/text/glm-5.2
Date: 2026-07-30（页面抓取日期）
Excerpt: "在 FrontierSWE、SWE-Marathon、PostTrainBench 等长程任务基准上，GLM-5.2 整体表现介于 Claude Opus 4.7 与 4.8 之间，是当前排名最高的开源模型。其中，在 FrontierSWE 上仅落后 Opus 4.8 约 1%，同时超过 GPT-5.5（1%）和 Opus 4.7（11%）；在更具挑战性的 SWE-Marathon 上仍有提升空间，与 Opus 4.8 存在约 13% 的差距。"（官方图表数据：SWE-bench Pro——GLM-5.2 62.1 / GLM-5.1 58.4 / Claude Opus 4.8 69.2 / GPT-5.5 58.6 / Gemini 3.1 Pro 54.2；Terminal-Bench 2.1——81.0 / 63.5 / 85.0 / 84.0 / 74.0）
Context: 重要纠偏：网传"GLM-5.2 在 SWE-bench Pro 击败 Claude/GPT-5.5 登顶"不准确——官方图显示 Opus 4.8 的 69.2 仍领先；GLM-5.2 胜的是 GPT-5.5 与 Gemini 3.1 Pro。个别英文内容站（llmcheck）称 68.5%，与官方模型卡 62.1 矛盾，可信度低。
Confidence: high（数字为厂商自报口径）

### 证据 C4：GLM-5.2 参数规模 753B MoE / 约 40B 激活，IndexShare 技术将 1M 上下文单 token FLOPs 降 2.9 倍
Claim: GLM-5.2 总参数约 753B（MoE，架构标识 glm_moe_dsa），激活约 40B；IndexShare（每 4 个稀疏注意力层共享 indexer）使 1M 上下文单 token FLOPs 降低约 2.9 倍；MTP 投机解码接受长度提升最高约 20% [^16^][^17^]
Source: aidaily.wiki（基于 HF 模型卡的溯源稿）/ einkcn（引模型卡）
URL: https://aidaily.wiki/2026-06-22/glm-52-open-weights-cost/ ; https://www.einkcn.com/html/product_6a40ae2499ecd9473.html
Date: 2026-06-28 / 2026-06-28
Excerpt: "规模：753B 总参数，MoE 架构。模型卡的架构标签为 glm_moe_dsa，与上一代 GLM-5.1（754B）同属一个家族……上下文：1M token。模型卡称其为 'solid 1M-token context'，并通过名为 IndexShare 的机制（每四个稀疏注意力层复用同一个 indexer）把 1M 上下文下的单 token FLOPs 降低约 2.9 倍；同时改进了用于投机解码的 MTP 层，把接受长度（acceptance length）最高提升约 20%。"
Context: 注意媒体中并存 744B/753B/754B 三种写法（什么值得买称"GLM-5/5.1/5.2 均基于 7440 亿总参数"，与模型卡口径 744/754/753B 不一致），建议书中统一写"约 750B 级 MoE、激活约 40B"并注明官方模型卡为准。支持 vLLM/SGLang/KTransformers/Transformers/Unsloth 及昇腾 NPU 部署。
Confidence: medium-high（以 HF 模型卡为最终依据）

### 证据 C5：GLM-5.2 第三方评价——Artificial Analysis 综合榜 51 分并列前三（开源第一）；Code Arena 前端盲测"全球可用模型第一"
Claim: 第三方 Artificial Analysis 综合榜单上 GLM-5.2 取得 51 分，与 Anthropic、OpenAI 并列前三，为开源模型最高；Code Arena 前端盲测中 GLM-5.2 排名仅次于受限的 Claude Fable 5，为"全球可用模型第一"（第三方）[^14^][^18^]
Source: 财新 / 每日投研（转券商研报口径）
URL: https://www.caixin.com/2026-07-23/102467238.html ; https://www.meiritouyan.com/43151.html
Date: 2026-07-23 / 2026-06-17
Excerpt: "在第三方大模型榜单Artificial Analysis综合榜单上，GLM-5.2取得51分，与Anthropic、OpenAI一起位居前三，为开源模型中质量最好的。GLM-5.2发布后，一度刺激智谱股价涨至2980港元/股，公司市值突破万亿港元。"（财新）；"在全球百万用户参与盲测的前端开发评估系统Code Arena上，GLM-5.2 Max排名第2，仅次于Claude Fable 5，高于Claude Opus 4.7 Thinking、Claude Opus 4.8 Thinking等多代Claude模型。考虑到Fable 5目前可用性受限，GLM-5.2实际取得全球可用模型第一的表现。"（每日投研）
Context: 另有七牛云转载稿引第三方测评 AICodeKing（KingBench）评价"代码洁净度极高、UX 设计品味出众、One-shot 能力强"；英文开发者实测（danilchenko.dev）称代码质量高但输出冗长（平均每任务约 43K output tokens，GLM-5.1 约 26K），OpenRouter 典型任务约 75 秒，慢于 Opus 4.8。安全厂商 Semgrep 实测 IDOR 漏洞检测 F1 39% 胜 Claude Code（Opus 4.6 的 37%）——单一英文站来源，中低置信。
Confidence: high（AA 51 分）；medium-high（Code Arena）；medium-low（Semgrep）

### 证据 C6：GLM-5.2 训练与推理均未依赖海外算力，Day 0 完成八大国产芯片平台推理适配
Claim: 智谱称 GLM-5.2"模型训练与线上推理均未依赖海外算力"，上线首日完成与华为昇腾、寒武纪、摩尔线程、海光、壁仞、沐曦、昆仑芯、平头哥八大国产算力平台推理适配；昇腾 950 超节点预计下半年成为其算力底座 [^19^]
Source: 富途新闻（转科创板日报）
URL: https://news.futunn.com/post/74724143/...
Date: 2026-06-17
Excerpt: "在性能之外，GLM-5.2以最宽松的 MIT 协议开放，允许免费商用，且模型训练与线上推理均未依赖海外算力。上线首日，GLM-5.2的线上推理已在Day 0完成与八大国产算力平台的推理适配……智谱方面同时对《科创板日报》记者表示，预计下半年昇腾950超节点上市后，将成为GLM-5.2重要的算力底座。"
Context: 科创板日报评论："'Day 0适配'不是指模型'能在国产芯片上跑起来'，而是意味着在发布当天就已经完成了深度推理适配与算子级优化——这代表国产芯片不是作为'备胎'存在，而是与海外算力平台同等对待的第一梯队底座。"
Confidence: high（引自科创板日报采访）

---

## D. Z Code（智谱官方编程工具）

### 证据 D1：Z Code 于 2025-12-26 首发，定位轻量级 AI 代码编辑器（Alpha，Mac/Windows），整合 Claude Code、Codex、Gemini
Claim: Z Code 是智谱 2025 年 12 月 26 日发布的轻量级 AI 协同开发工具/代码编辑器，首发为 Alpha 测试版，支持 macOS 与 Windows，核心卖点是用统一可视化桌面整合 Claude Code、Codex、Gemini 三家命令行 Agent，一个 API key 即可切换 [^20^][^21^]
Source: 新浪科技（转 IT之家）/ 百度百科"Z Code"
URL: https://finance.sina.com.cn/tech/roll/2025-12-26/doc-inhecfim2740550.shtml ; https://baike.baidu.com/item/Z%20Code/67385330
Date: 2025-12-26 / 2026-06-29
Excerpt: "12 月 26 日消息，智谱为解决命令行 AI 编程工具（如 Claude Code、Codex、Gemini 等）操作门槛高的问题，最新推出了名为 Z Code 的 AI 协同开发工具，提供统一、友好的可视化桌面，使用一个 api key，就能丝滑切换体验多个 Agent 编程工具。……编辑器内置了'思考模式'……此外，Z Code 提供了强大的'历史重构'能力，用户不仅能修改历史对话中的提示词，还能对整个交互节点进行全面重构并重新执行。"
Context: 早期定位是"AI Agent 容器"——本身不带模型，靠接入各家 Agent/订阅（智谱 GLM Coding Plan、Claude/Codex/Gemini 原生订阅、OpenRouter 及任意 Anthropic/OpenAI 兼容服务）工作；支持手机远程指挥桌面端 Agent。
Confidence: high

### 证据 D2：2026 年 2 月 Z Code 随 GLM-5 升级定位"智能体开发环境"
Claim: 2026 年 2 月 GLM-5 发布后，Z Code 基于 GLM-5 能力增强，被定位为"智能体开发环境"，支持自然语言拆解任务、调度多智能体完成编写、调试、预览、提交全流程 [^21^]
Source: 百度百科"Z Code"
URL: https://baike.baidu.com/item/Z%20Code/67385330
Date: 2026-06-29（词条更新）
Excerpt: "2026年2月，随着智谱GLM-5模型的发布，Z Code被描述为基于GLM-5能力的开发工具，其AI辅助编程功能有所增强。此次随GLM-5同步推出的Z Code被定位为一个智能体开发环境。用户可通过自然语言描述需求，模型可拆解任务，并调度多智能体完成代码编写、调试、预览及提交等流程。"
Context: Z Code 由 GLM 模型参与开发（AI 写 AI 工具），这是智谱官方叙事的一部分。
Confidence: medium-high（二手汇编词条，关键事件均有新闻源互证）

### 证据 D3：ZCode 3.0（2026-06-13）全面切换自研 ZCode Agent 内核，放弃第三方 Agent 适配，深度绑定 GLM-5.2
Claim: 2026 年 6 月 13 日智谱发布 ZCode 3.0，全面切换自研 ZCode Agent 内核，官方明确"后续版本将聚焦自研 Agent 体验，不再内置或维护其他 Agent 适配"，从"多 Agent 集成器"转为 GLM 专属 ADE（Agentic Development Environment）[^22^][^23^]
Source: 17173（转 IT之家）/ AI星球评测
URL: http://news.17173.com/content/06142026/020442457.shtml ; https://www.aixq.cc/47739.html
Date: 2026-06-14 / 2026-07-03
Excerpt: "官方表示，ZCode 3.0 全面切换自研 ZCode Agent 内核。针对满血 GLM 深度优化长程推理、工具调用和大型工程执行链路，整体任务完成效果已显著优于第三方 Agent；后续版本将聚焦自研 Agent 体验，不再内置或维护其他 Agent 适配。此外，升级或已订阅 GLM Coding Plan 用户应用内相比 API 调用专享 150% 配额。"（IT之家）；"ZCode 是智谱 AI 推出的一款 AI 编程工具，官方定位是 ADE（Agentic Development Environment），一个以 Agent 为驱动的开发环境。"（AI星球）
Context: 3.0 新功能：分组式任务工作区（多 Agent 并发管理）、Zread 智能项目知识库、可视化 Git 分支图谱、状态监控看板。官网 zcode.z.ai/cn，文档 docs.bigmodel.cn/cn/coding-plan/tool/zcode。工具本身免费下载，付费部分是 GLM Coding Plan。外部模型（Claude/GPT/DeepSeek 等）仍可经 OpenAI 兼容端点接入，但官方优化重心在 GLM。
Confidence: high

### 证据 D4：ZCode 平台与版本现状——v3.5.2 稳定版支持 macOS/Windows，Linux 内测中；新用户 5 天×500 万 token/天体验
Claim: 截至 2026 年 7 月，ZCode 稳定版 v3.5.2 提供 macOS（arm64/x64）与 Windows（x64/ARM64）安装包，Linux 处内测阶段；新用户连接 BigModel/Z.ai 账号可获 5 天体验期，每天 500 万 token（GLM-5.2 300 万 + GLM-5-turbo 200 万）[^24^][^25^]
Source: 七牛云开发者社区（转官方文档）/ 博客园上手实录
URL: https://news.qiniu.com/archives/1785117449028 ; https://www.cnblogs.com/youring2/p/21143184
Date: 2026-07-27 / 2026-07-05
Excerpt: "ZCode 当前稳定版本 v3.5.2 提供 macOS 与 Windows 双端安装包，Linux 处于内测阶段（据智谱官方文档，2026）。……下载入口统一在 ZCode 中文官网 zcode.z.ai/cn，安装包托管于官方 CDN cdn-zcode.z.ai。"（七牛云）；"新用户首次连 BigModel 或 Z.ai，有 5 天免费体验额度：GLM-5.2：300 万 Token / 天；GLM-5-turbo：200 万 Token / 天；合计每天 500 万 Token。"（博客园）
Context: 移动端可远程控制桌面端 Agent（Bot 功能）。常见安装坑：macOS"已损坏"提示需 xattr 去隔离属性；Linux 需 fuse 依赖。
Confidence: high

---

## E. GLM Coding Plan（编程订阅套餐）

### 证据 E1：套餐定位与可用模型——所有套餐支持 GLM-5.2/GLM-5-Turbo/GLM-4.7，调用 GLM-5.1/GLM-5 自动切换至 GLM-5.2
Claim: GLM Coding Plan 是智谱面向 AI 编码的订阅套餐，截至 2026 年 7 月所有套餐均支持 GLM-5.2、GLM-5-Turbo、GLM-4.7；调用历史模型 GLM-5.1/GLM-5 将自动切换至 GLM-5.2 [^26^]
Source: 智谱AI开放文档（官方）套餐概览
URL: https://docs.bigmodel.cn/cn/coding-plan/overview
Date: 2026-07-30（页面抓取日期）
Excerpt: "GLM Coding Plan 是专为 AI 编码打造的订阅套餐，仅需少量投入，即可覆盖需求理解、代码生成、调试修复、代码库问答与自动化任务处理等开发全流程……所有套餐均支持 GLM-5.2、GLM-5-Turbo、GLM-4.7。调用历史模型 GLM-5.1/GLM-5 都将自动切换至 GLM-5.2。"
Context: 重要限制："套餐仅限在官方支持的指定工具与产品环境中使用。在除规定工具外调用 API，不可享用 Coding 套餐的额度。"OpenClaw 场景为次级调度（高负载自动排队限流）。任务背景中"Coding Plan 200K 上下文"已过时——GLM-5.2 套餐内可用 1M（glm-5.2[1m]）。
Confidence: high

### 证据 E2：额度机制——积分制双限额（5 小时 + 每周），Lite 2,000/10,000、Pro 12,000/60,000、Max 28,000/140,000
Claim: Coding Plan 采用积分制，同时设每 5 小时与每周上限：Lite 2,000/10,000 积分、Pro 12,000/60,000、Max 28,000/140,000；按 token×抵扣系数折算积分，高峰期（周一至周五 14:00–18:00 UTC+8）全价，非高峰按 50% 抵扣 [^26^]
Source: 智谱AI开放文档（官方）套餐概览
URL: https://docs.bigmodel.cn/cn/coding-plan/overview
Date: 2026-07-30（页面抓取日期）
Excerpt: "套餐同时设有每 5 小时和每周额度上限……Lite 套餐 2,000/10,000；Pro 套餐 12,000/60,000；Max 套餐 28,000/140,000。……模型消耗积分数=（输入 Token × Input 抵扣系数 + 缓存命中 Token × Cached Input 抵扣系数 + 输出 Token × Output 抵扣系数）/ 10000……GLM-5.2：Input 6.9 / Cached 1.7 / Output 24……非高峰时段内，模型调用按基础积分消耗的 50% 抵扣。高峰时段：每周一至周五的 14:00～18:00（UTC+8）。"
Context: 官方估算（全用 GLM-5.2、缓存命中率 90.9%）：每周可用 token 约 Lite 0.43–0.87 亿、Pro 2.63–5.26 亿、Max 6.13–12.26 亿；"当充分利用非高峰时段优惠时，相较于按量调用 GLM-5.2 标准 API，最高可节省 92% 成本"。注意：媒体报道的"高峰期 3 倍、非高峰 2 倍、限时 1 倍"是 2 月致歉信后的旧口径；7 月官方文档现行口径为"高峰 1 倍、非高峰 0.5 倍积分"——两种表述等效（基准不同），写作时建议直接引用官网最新页。
Confidence: high

### 证据 E3：4 个专属 MCP——视觉理解（GLM-4.6V）、联网搜索、网页读取、开源仓库
Claim: Coding Plan 附赠 4 个专属 MCP Server：视觉理解（由旗舰视觉推理模型 GLM-4.6V 驱动）、联网搜索、网页读取、开源仓库（GitHub 检索/结构/文件读取），所有套餐档位均可用 [^27^][^26^]
Source: 智谱AI开放文档（官方）快速开始 / 套餐概览
URL: https://docs.bigmodel.cn/cn/coding-plan/quick-start ; https://docs.bigmodel.cn/cn/coding-plan/overview
Date: 2026-07-30（页面抓取日期）
Excerpt: "套餐用户可以使用视觉理解 MCP Server，可以通过旗舰视觉推理模型 GLM-4.6V 来理解和分析图像内容。……套餐用户可以使用网络搜索 MCP Server，获取最新的技术信息。……套餐用户可以使用网页读取 MCP Server，获取并解析网页内容。……套餐用户可以使用开源仓库 MCP Server，访问开源仓库文档、目录结构和文件内容。"（快速开始）；"扩展覆盖更多能力：套餐包含专属图像视频理解、联网搜索、网页读取、开源仓库 MCP，上线 GLM in Excel (Beta) 权益"（套餐概览）
Context: MCP 调用也消耗积分（联网搜索/网页读取/开源仓库按 Output 抵扣系数 1.2 计）。可用官方一键安装工具 `npx @z_ai/coding-helper` 配置到 Claude Code/OpenCode 等。
Confidence: high

### 证据 E4：兼容工具——官方列表含 Claude Code、Cline、OpenCode、Roo Code、Kilo Code、Cursor、Crush、Goose、TRAE、CodeBuddy 等（社区称 20+）
Claim: Coding Plan 官方支持 Claude Code、Kilo Code、OpenClaw、OpenCode、TRAE、CodeBuddy 等主流编码工具（官方文档枚举约 9 款：Claude Code、Cline、OpenCode、Roo Code、Kilo Code、Cursor、Crush、Goose 等）；社区资料普遍称"兼容 20+ 款工具" [^26^][^28^]
Source: 智谱AI开放文档（官方）/ 什么值得买横评（引官方文档）/ GitHub 资源汇总仓
URL: https://docs.bigmodel.cn/cn/coding-plan/overview ; https://post.smzdm.com/p/a823mknn ; https://github.com/guihuashaoxiang/FreeLLM-API-KeyHub
Date: 2026-07-30 / 2026-07-28 / 2026-07-17
Excerpt: "兼容多款编码工具：支持 Claude Code、Kilo Code、OpenClaw、OpenCode、TRAE、CodeBuddy 等主流编码工具，灵活适配多种开发场景。"（官方）；"支持工具（官方列出 9 款）：Claude Code、Cline、OpenCode、Roo Code、Kilo Code、Cursor、Crush、Goose，以及持续扩展中的其他工具。"（什么值得买）；"兼容工具：Claude Code、Cline、Cursor、Kilo Code、Roo Code 等20+"（GitHub 汇总）
Context: 协议层支持 Anthropic Messages 与 OpenAI Chat Completion 双协议（见 F1），理论上任何兼容这两家协议的工具都可接入；"20+"为社区口径。
Confidence: high（官方列表）；medium（"20+"确数）

### 证据 E5：套餐定价——国内 ¥49/149/469 每月（Lite/Pro/Max），国际版 $18/72/160（折扣后约 $16.2/64.8/144）
Claim: 国内 Coding Plan 定价约 Lite ¥49/月、Pro ¥149/月、Max ¥469/月（年付约 8 折）；国际版（z.ai）标价 Lite $18、Pro $72、Max $160/月，2026 年 7 月折扣后约 $16.2/64.8/144 [^29^][^25^][^30^]
Source: 博客园六大平台横评 / 博客园 ZCode 实录 / CSDN 套餐指南
URL: https://www.cnblogs.com/jzssuanfa/p/20098883 ; https://www.cnblogs.com/youring2/p/21143184 ; https://adg.csdn.net/6a31180010ee7a33f27de27f.html
Date: 2026-05-20 / 2026-07-05 / 2026-06-07
Excerpt: "智谱 GLM：¥49/月……核心模型 GLM-5 / GLM-4.7……3档"（横评表）；"Coding Plan 分三档（美元计价）：Lite：约 $16.2 / 月（原价 $18）……Pro：约 $64.8 / 月（原价 $72），5 倍 Lite 额度……Max：约 $144 / 月（原价 $160），20 倍 Lite 额度"（ZCode 实录）；"Lite 新套餐 49 元/月（年付 39 元×12）；Pro 新套餐 149 元/月（年付 119×12）；Max 新套餐 469 元/月（年付 375×12）"（CSDN）
Context: 价格随促销波动大（官网 Banner 曾出现首月 ¥20 特惠、季度付 $27/季等）；团队版（Team）已上线，按组织统一管理成员/预算/权限，价格需商务询价。国际版"无需抢购"，国内热门档位常限售。
Confidence: medium-high（调价频繁，引用前必查官网）

### 证据 E6：套餐历史与商业化——2025 年国内首家推出，付费开发者 24.2 万，2026 年内四次提价仍供不应求
Claim: 智谱 2025 年在国内第一家推出 Coding 编程套餐，全球付费开发者超 24.2 万、Token 调用量 6 个月涨 15 倍；2026 年内四次提价（2 月 Coding Plan +30% 起、3 月 GLM-5-Turbo API +20%、4 月 GLM-5.1 +10% 且海外 Coding Plan 涨 80%–150%、6 月 GLM-5.2 取消短上下文档并推团队版），一季度 API 涨价 83% 后调用量反增 400% [^31^][^12^]
Source: 腾讯新闻（智谱 2025 年报报道）/ 36氪
URL: https://view.inews.qq.com/a/20260331A078Y400 ; https://www.36kr.com/p/3864006047929605
Date: 2026-03-31 / 2026-06-22
Excerpt: "2025年智谱在国内第一家推出GLM Coding Plan（编程套餐），凭借模型的高质量编码能力，全球付费开发者数量快速突破24.2万，Token调用量6个月涨了15倍。2026年2月，即使上调价格30%并取消首购优惠，编程套餐依然保持供不应求的态势。"（腾讯新闻）；"值得一提的是，智谱已经年内四次上调 API 定价。……据智谱CEO张鹏在业绩会上给出的一组数据：2026年一季度，智谱API涨价83%后，调用量不降反升，增长400%，市场依然供不应求。"（36氪）
Context: 智谱 2026-01-08 港股上市（"全球大模型第一股"，02513.HK），2025 年营收 7.24 亿元（+132%），MaaS API 平台 ARR 17 亿元；GLM-5.2 发布后市值一度突破 1 万亿港元。企业版 Coding Plan 于 2025-10-21 基于 GLM-4.6 首发。
Confidence: high

---

## F. API 定价 与 Claude Code/Codex 兼容性

### 证据 F1：Coding Plan 官方双协议端点——Anthropic（/api/anthropic）与 OpenAI（/api/coding/paas/v4），Claude Code 改 base URL 即可接入
Claim: GLM Coding Plan 官方同时提供 Anthropic Message 协议端点（https://open.bigmodel.cn/api/anthropic）与 OpenAI Chat Completion 协议端点（https://open.bigmodel.cn/api/coding/paas/v4）；在 Claude Code 的 settings.json 中设置 ANTHROPIC_BASE_URL 与 ANTHROPIC_AUTH_TOKEN 即可把 GLM 当 Claude 后端使用 [^32^][^33^]
Source: 智谱AI开放文档（官方）快速开始 / 腾讯云开发者社区教程
URL: https://docs.bigmodel.cn/cn/coding-plan/quick-start ; https://cloud.tencent.com/developer/article/2690537
Date: 2026-07-30 / 2026-06-16
Excerpt: "GLM Coding Plan 支持 Anthropic 协议和 OpenAI 协议两种接入方式，接入时请注意配置正确的 Base URL：Anthropic Message 协议 https://open.bigmodel.cn/api/anthropic；OpenAI Chat Completion 协议 https://open.bigmodel.cn/api/coding/paas/v4"（官方）；"本文系统梳理 Claude Code 安装流程 + 接入 GLM Coding Plan + 模型切换配置方法……ANTHROPIC_BASE_URL 设置"（腾讯云教程）
Context: 配置示例：`{"env":{"ANTHROPIC_BASE_URL":"https://open.bigmodel.cn/api/anthropic","ANTHROPIC_AUTH_TOKEN":"<智谱key>"},"model":"glm-5.2[1m]"}`。常见坑：① 智谱 key 形如 `xxxxxxxx.yyyyyyyy`，不要加 Bearer 前缀；② OpenAI 协议必须走 coding 专用端点 `/api/coding/paas/v4`，填成通用端点 `/api/paas/v4` 会走不通套餐额度；③ Claude Code 的 `/cost` 显示按 Anthropic 价目计算，接 GLM 后数字无意义；④ 无 Anthropic 兼容端点时可退而用 LiteLLM 桥接。Codex 走 OpenAI 兼容端点同理。
Confidence: high

### 证据 F2：GLM-5.2 API 按量定价——国内 ¥8/¥2/¥28 每百万 token（输入/缓存命中/输出），国际 $1.40/$0.26/$4.40；不分段计费
Claim: GLM-5.2 官方 API 国内定价输入 ¥8、缓存命中 ¥2、输出 ¥28（每百万 tokens），国际站 $1.40/$0.26/$4.40，不分段（无长短上下文档差），缓存存储限时免费 [^34^][^35^]
Source: GitHub BerriAI/litellm issue（逐条引用官方定价页）/ 掘金价格实测汇总
URL: https://github.com/BerriAI/litellm/issues/31075 ; https://juejin.cn/post/7667404454753812523
Date: 2026-06-23 / 2026-07-28
Excerpt: "International (Z.AI, USD per million tokens) — https://docs.z.ai/guides/overview/pricing：Input $1.4、Cached Input $0.26、Output $4.4……Domestic (智谱开放平台, CNY per million tokens) — https://open.bigmodel.cn/pricing：输入 8 元、缓存命中 2 元、输出 28 元、缓存存储限时免费……Tiered pricing: No — GLM-5.2 has a single flat price row on the official pricing page (unlike GLM-5 / GLM-5-Turbo which tier by input length)"（litellm issue）；"智谱GLM GLM-5.2 1M 8元/28元（open.bigmodel.cn）"（掘金）
Context: 对比（2026-07 掘金实测表）：DeepSeek-V4-Flash 约 ¥1.01/¥2.02、GPT-5.5 约 $5/$30、Claude Opus 4.8 约 $5/$25——GLM-5.2 输出价约为 Opus 4.8 的 1/5.7、GPT-5.5 的 1/6.8。OpenRouter 价格约 $0.95–1.00/$3.00–4.00。GLM-5.1 API 约 ¥6/¥24（<32K 档）。GLM-4.7-Flash 免费。
Confidence: high（双来源交叉，且引用官方页面）

### 证据 F3：GLM-5.2 已成多家第三方平台的默认/可选模型，国内云厂商 Coding Plan 普遍转售 GLM
Claim: GLM-5.2 上线后进入阿里云百炼、火山方舟、联通云等第三方 Coding Plan 的模型列表；GLM 系列成为 Windsurf 默认模型、OpenCode 默认模型之一，并部署于 AWS Bedrock、Google Vertex AI、Fireworks、Cerebras 等 [^36^][^31^]
Source: GitHub coding-plan-collection 汇总 / 腾讯新闻（智谱年报报道）
URL: https://github.com/will-17173/coding-plan-collection ; https://view.inews.qq.com/a/20260331A078Y400
Date: 2026-05-08 / 2026-03-31
Excerpt: "火山方舟（Coding Plan）支持模型：Auto, Doubao-Seed-2.0-Code……GLM-5.2, DeepSeek-V4-Flash, DeepSeek-V4-Pro"（GitHub 汇总）；"目前，GLM模型已全面部署于Google Vertex AI、AWS Bedrock、Fireworks、Cerebras等全球顶尖云服务商，并入驻OpenRouter、Vercel等国际主流模型聚合平台。GLM已成为国际知名Coding平台（如Windsurf）、知名CodingAgent平台（如OpenCode）的默认模型。"（腾讯新闻）
Context: 智谱称"中国前十大互联网公司中，有 9 家深度调用 GLM 模型"；GLM-5 发布 24 小时内获字节 TRAE、阿里 Qoder、腾讯 CodeBuddy、美团 CatPaw、快手万擎、百度智能云、WPS Office 官方接入。
Confidence: high

---

## G. 用户口碑与常见坑

### 证据 G1：2026-02-21 智谱就 GLM Coding Plan 发致歉信——规则不透明、灰度太慢、升级机制粗糙；股价次日跌超 21%
Claim: GLM-5 发布后 Coding Plan 出现严重运营事故：高峰 3 倍/非高峰 2 倍消耗未提前讲清、按 Max→Pro→Lite 顺序灰度开放、老用户误升级；智谱 2 月 21 日公开致歉并提供"2026-01-01 至 02-21 费用全免"退款与一键回滚，2 月 23 日股价跌超 21%、市值蒸发约 682 亿港元 [^37^][^38^]
Source: 财联社 / 和讯网
URL: https://www.cls.cn/detail/2292546 ; https://m.hexun.com/stock/2026-02-23/223503508.html
Date: 2026-02-22 / 2026-02-23
Excerpt: "智谱称，这次改版主要犯了三个错：规则透明度不够、GLM-5灰度节奏太慢、老用户升级机制设计粗糙。……目前Max用户已经全面开放，Pro用户虽已开放，但高峰期可能会因集群负载较高遇到限流，Lite用户将会在节后非高峰期逐步灰度开放。针对受到影响的Lite和Pro用户，公司支持自主申请退款。"（财联社）；"2月23日……智谱跌超21%……智谱市值蒸发了约682亿港元（折合人民币603亿元）。消息面上，智谱于2月21日发布GLM Coding Plan致歉信"（和讯）
Context: 致歉信归因：流量超预期 + 扩容没跟上 + 灰产号池/黄牛党冲击。这是写"厂商信用与运营风险"的典型案例：模型能力出圈→算力供不应求→限售→沟通失误→公开道歉→全额退款。
Confidence: high

### 证据 G2：长期"售罄/抢购"——Coding Plan 各档位上线即秒空，2026-01-23 起曾限量发售（每日仅 20% 额度）
Claim: GLM Coding Plan 自 GLM-5.1 口碑爆发后长期供不应求，Lite/Pro/Max 三档均需抢购；媒体实录工程师连续 5 天蹲守未抢到 Max 档；智谱 2026-01-23 起实施限量发售（每日可售量调为 20%）[^39^][^40^]
Source: 重庆晨报（上游新闻）/ 百度百科"GLM Coding Plan"
URL: https://epaper.cqcb.com/html/202606/18/content_526900.html ; https://baike.baidu.com/item/GLM%20Coding%20Plan/67265860
Date: 2026-06-18 / 2026-07-28
Excerpt: "6月15日，两江新区一家互联网公司的算法工程师冯宇，为了给团队搞到智谱Coding Plan的Max档，连着守了五个早上。每天9:28准时打开阿里云百炼页面……结果9:30一到，库存直接从'可购买'跳成'已售罄'……智谱GLM Coding Plan从上线那天起就僧多粥少。GLM-5.1口碑爆了之后，'国产最强编程模型'的名号一传开，大批开发者蜂拥而至，套餐一放出来就没了。"（重庆晨报）；"随着模型能力提升导致需求激增，GLM Coding Plan曾出现上线即售罄的情况。为应对算力资源紧张，智谱曾于2026年1月23日起实施限量发售，将每日可销售量调整为当时的20%。"（百度百科）
Context: 国际版（z.ai 美元站）无需抢购——存在"国内抢购 vs 国际现货"的双轨现象，并催生账号代购灰产（云巴巴报道其合规风险）。
Confidence: high

### 证据 G3：实际使用摩擦——高峰期 3 倍系数烧额度快、ZCode 高峰"系统繁忙"、输出冗长推高成本
Claim: 用户实测的主要抱怨：① GLM-5.2 作为高阶模型高峰期（14:00–18:00）按 3 倍系数消耗额度，高强度 Agent 任务几小时可烧完周额度；② ZCode 高峰期频繁"系统繁忙"；③ GLM-5.2 输出冗长（平均每任务约 43K output tokens，比 GLM-5.1 的 26K 高 65%），按量计费下成本与等待时间上升 [^41^][^23^][^42^]
Source: 掘金评测 / AI星球 ZCode 评测 / danilchenko.dev 实测
URL: https://juejin.cn/post/7653847759125987368 ; https://www.aixq.cc/47739.html ; https://www.danilchenko.dev/posts/glm-5-2-review/
Date: 2026-06-22 / 2026-07-03 / 2026-07-18
Excerpt: "GLM-5.2 是高阶模型，对标 Claude Opus。高峰期（北京时间 14:00–18:00）按 3 倍额度消耗，非高峰期 2 倍。……你以为在用 1 个 prompt，实际计费是 3 个。高强度工作流下，一天的额度在两三个小时里就能烧完。"（掘金）；"算力瓶颈严重：高峰期频繁'系统繁忙'，体验卡顿，资源明显跟不上用户增长……封闭生态不可逆：不再兼容第三方 Agent 框架"（AI星球）；"GLM-5.2 is verbose. It used roughly 43K output tokens per task in Artificial Analysis's benchmark suite, compared to 26K for GLM-5.1. That verbosity inflates your bill... On OpenRouter, a typical coding task took around 75 seconds, which felt slow compared to Opus 4.8's sub-30-second responses"（danilchenko）
Context: 能力口碑整体正面（"能打了"），痛点集中在供给侧（算力/限流/抢购）与计费复杂度；GLM-5.2 被多篇评测认为与 Claude Opus 4.8 仍有可感知差距，但性价比显著。
Confidence: high（多源一致的负面模式）

### 证据 G4：其他常见坑——第三方平台"降智"争议、速度波动、端点配置错误
Claim: 社区持续跟踪第三方云平台（火山方舟等）上 GLM 模型"降智"问题（截至 2026-06-25 报告未确认修复）；官方渠道速度波动大；Coding Plan 的 OpenAI 端点必须填 coding 专用地址 [^43^][^44^][^25^]
Source: 掘金《AI Coding 工具评估报告》/ CSDN 套餐指南 / 博客园 ZCode 实录
URL: https://juejin.cn/post/7657433456431349801 ; https://adg.csdn.net/6a31180010ee7a33f27de27f.html ; https://www.cnblogs.com/youring2/p/21143184
Date: 2026-07-01 / 2026-06-07 / 2026-07-05
Excerpt: "火山方舟 GLM 降智：当前是否已修复/改善——社区持续跟踪（LINUX DO 等）"（评估报告待核验清单）；"智谱官网的速度波动挺大的……所有模型在 WSL 下的终端 Agent 中永远是最快的，在 AI IDE 中永远是最慢的"（CSDN）；"一个小坑：如果你用智谱 Coding Plan 的 API Key，OpenAI 端点必须填 Coding 专用地址 https://open.bigmodel.cn/api/coding/paas/v4，不能填通用端点 /api/paas/v4，不然额度走不通。"（博客园）
Context: "降智"指第三方托管方可能以量化/缩配方式提供服务导致体验劣于官方渠道——属于社区指控，未有官方确认，书中应标注为"未经证实的社区反馈"。
Confidence: medium（社区口径，未官方证实）

---

## H. 昇腾训练的意义

### 证据 H1：全昇腾训练 + 国产算力 Day 0 适配，被视为国产算力链"生存必需"的验证
Claim: GLM-5 全程用 10 万块昇腾 910B 训练（未用 NVIDIA GPU），GLM-5.2 训练与推理均未依赖海外算力并 Day 0 适配八大国产芯片平台；在出口管制背景下，这被产业界视为算力供应链自主可控从"战略储备"变为"生存必需"的标志性验证 [^4^][^19^]
Source: 钛媒体 / 富途新闻（转科创板日报）
URL: https://www.tmtpost.com/agent/ai-article?id=18274 ; https://news.futunn.com/post/74724143/...
Date: 2026-06-17
Excerpt: "国内大模型公司的算力成本中，GPU采购和租赁占据了大头，且高度依赖英伟达H100/H200等海外高端芯片。而在中美科技博弈持续升级的背景下，算力供应链的自主可控已经从'战略储备'变成了'生存必需'。"（科创板日报）；"它全程在10万块华为昇腾910B芯片上完成训练——没碰过一块NVIDIA GPU。"（钛媒体）
Context: 意义三层：① 技术验证——证明国产全栈（昇腾+MindSpore 系）可训出前沿级模型（此前 2026 年 1 月智谱联合华为开源 GLM-Image，为首个全程国产芯片训练的 SOTA 多模态模型，作技术铺垫）；② 供应链安全——推理 Day 0 适配意味着国产芯片从"备胎"变"第一梯队底座"；③ 资本叙事——GLM-5 发布日智谱港股 +26%、一周 +70%，GLM-5.2 后市值破万亿港元。注意智谱也因算力供不应求启动"算力合伙人"招募（2026-02），说明国产集群扩容压力真实存在。
Confidence: high（事实部分）；"首个"等最高级表述建议降格为"首批/代表性案例"

### 证据 H2：商业背景——Anthropic 出口管制事件放大 GLM-5.2 开源+国产算力组合的战略价值
Claim: 2026-06-12 美国商务部要求 Anthropic 暂停 Claude Fable 5/Mythos 5 对外国国民服务，次日智谱全量开放 GLM-5.2 并强调"前沿智能不应只属于少数人，也不应被少数规则随时收回"，GLM-5.2 由此获得"国产 Claude 替代"的窗口期红利 [^12^]
Source: 36氪
URL: https://www.36kr.com/p/3864006047929605
Date: 2026-06-22
Excerpt: "6月12日，美国商务部依据出口管制相关授权，要求人工智能公司Anthropic暂停向所有外国国民……提供其最新旗舰模型Claude Fable 5与Claude Mythos 5的访问权限。……6月13日，国产大模型龙头智谱宣布旗下开源旗舰GLM-5.2面向其Coding Plan全量用户开放……智谱表示，此次开放的新模型是公司迄今为止能力最强的开源模型，又指在前沿模型突然变得不可用的时刻，科技不应该只属与少数人，也不应该被随时收回。"
Context: 虎嗅引述开发者访谈："不少开发者因为Claude对中国用户设限，转去找便宜好用的替代品，'在便宜的模型里，智谱GLM-5.2和DeepSeek很好用。'"这是 GLM-5.2 海外开发者增长的重要驱动力。
Confidence: high

---

## I. 数据矛盾与待核实清单（写作前请注意）

1. **GLM-5.1 发布日期**：权威口径 2026-04-08（证券时报/澎湃/IT之家/百度百科），部分媒体 04-07（钛媒体），任务线索中的 04-09 应为媒体报道日——建议书稿统一用 **4 月 8 日**。
2. **GLM-5.2 开源日**：多数来源 06-16（OpenRouter/API/权重），财新记 06-17"上线并开源"——建议写"6 月 13 日 Coding Plan 先行、6 月 16–17 日公开 API 并 MIT 开源"。
3. **参数规模**：GLM-5 官方文档 744B/激活 40B；GLM-5.1 媒体口径 754B；GLM-5.2 HF 模型卡口径 753B；激活参数 40B 与 44B 两种写法并存——建议统一"约 750B 级 MoE、激活约 40B"并脚注"以官方模型卡为准"。
4. **SWE-bench 版本**：GLM-5 宣传 SWE-bench **Verified** 77.8%；GLM-5.1/5.2 宣传 SWE-bench **Pro** 58.4/62.1——两套不同基准，不可横向连比成"下降"。
5. **"击败 Claude"说法纠偏**：GLM-5.2 在 SWE-bench Pro（62.1）超 GPT-5.5（58.6）但**低于** Claude Opus 4.8（69.2，官方自家图表）；英文内容站 llmcheck 称 68.5% 系错误/无源数据，勿引用。
6. **消耗倍率口径**：2 月致歉信口径"高峰 3 倍/非高峰 2 倍"（基准=旧 1 倍），7 月官方文档口径"高峰 1 倍/非高峰 0.5 倍积分"（基准=高峰）——同一机制的两种表述，引用时以 docs.bigmodel.cn 当期页面为准。
7. **"首个完全用昇腾训练的前沿模型"**：媒体普遍表述为"全程 10 万块昇腾 910B、未用 NVIDIA GPU"（GLM-5）；"首个"限定未见官方严格措辞，另有"GLM-Image 为首个全程国产芯片训练的 SOTA 多模态模型"（2026-01）在先——建议写"首批完全基于国产算力训练的前沿语言模型之一"。
8. **未证实项**：GLM-5.1/5.2 是否同样全程昇腾训练（仅低权威来源称 GLM-5.1 是；GLM-5.2 官方口径为"训练与推理均未依赖海外算力"）；"20+ 兼容工具"确数；第三方平台"降智"指控。
9. **"GLM-5 原生智能体模式"**：未找到名为"原生智能体模式"的官方产品功能；可坐实的表述是 GLM-5 系列为 agent-native 设计（异步智能体强化学习、官方定位"复杂系统工程与长程 Agent 任务"），ZCode/Claude Code 等承载其 Agent 模式。

---

## 写给作者的 3–5 个要点

1. **把 GLM-5 三部曲写成"两个月一更"的闪电战**：GLM-5（2026-02-12，744B，全昇腾 910B 训练，SWE-bench Verified 77.8%）→ GLM-5.1（2026-04-08，8 小时长程自主工作，SWE-bench Pro 58.4）→ GLM-5.2（2026-06-13/16，1M 上下文，SWE-bench Pro 62.1 厂商自报，MIT 开源）。叙事主线是"从写代码到写工程"（Agentic Engineering），而非单纯刷榜。
2. **跑分引用纪律**：务必区分厂商自报（SWE-bench Pro 62.1 等）与第三方（Artificial Analysis 51 分开源第一、Coding Agent Index 开源第一、Code Arena 盲测"全球可用模型第一"）；并纠偏"GLM-5.2 击败 Claude"的流传错误——官方图表里 Opus 4.8（69.2）仍高于 GLM-5.2（62.1），它赢的是 GPT-5.5 与 Gemini 3.1 Pro。
3. **Z Code 的故事是战略转向而非单个产品**：2025-12-26 以"AI Agent 容器"起家（整合 Claude Code/Codex/Gemini），2026-06-13 的 3.0 版切换自研 ZCode Agent 内核并放弃第三方 Agent 适配——智谱从"GLM 兼容 Claude Code 生态"转向"GLM+ZCode 垂直闭环"（对标 Anthropic 的 Claude+Claude Code 模式）。工具免费、ADE 形态、macOS/Windows 稳定版、Linux 内测，付费靠 Coding Plan。
4. **GLM Coding Plan 是全书"订阅制编程套餐"的最佳中国样本**：首创于 2025 年、付费开发者 24.2 万、积分制双限额（5 小时+每周）、4 个专属 MCP（视觉理解/联网搜索/网页读取/开源仓库）、Anthropic+OpenAI 双协议端点使 Claude Code 改一行 base URL 即可接入。同时它也是"能力出圈→算力短缺→限售抢购→致歉退款"运营风险的完整案例（2026-02 致歉信、市值单日蒸发 682 亿港元）。
5. **昇腾叙事要写但克制**：GLM-5"全程 10 万块昇腾 910B、零 NVIDIA GPU"（钛媒体）+ GLM-5.2"训练推理均未依赖海外算力、Day 0 适配八大国产芯片平台"（科创板日报采访）是有采访依据的硬事实；但"首个"等最高级表述缺官方严格措辞，建议表述为"首批完全基于国产算力训练的前沿模型之一"，并点出其时代背景——Anthropic 出口管制事件（2026-06-12）使"开源权重 MIT + 国产算力"从备胎叙事变成开发者的现实避险需求。

---

### 附：主要信息源分级
- 一手/官方：docs.bigmodel.cn（glm-5 / glm-5.1 / glm-5.2 / coding-plan/overview / quick-start）、z.ai 定价页（经 litellm issue 引用）、huggingface.co/zai-org（经溯源稿引用）
- 权威媒体：财新、澎湃、证券时报/东方财富、科创板日报/富途、财联社、36氪、钛媒体、虎嗅、IT之家
- 社区/实测（佐证用）：掘金、博客园、CSDN、SegmentFault、什么值得买、AI星球、danilchenko.dev、GitHub 汇总仓
- 已剔除/降权：内容农场（kkaiapi、bota.chat、llmcheck、avenchat 等）的独有数字（如 68.5% SWE-bench Pro、68 分说法、"3 亿免费 token"等）一律未采信或仅作反例标注。
