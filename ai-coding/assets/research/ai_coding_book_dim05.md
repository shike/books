# 维度05：MiniMax M 系列模型 与 MiniMax Code 编程工具现状（截至 2026-07-31）

- 调研日期：2026-07-31
- 调研方法：24 次独立中文/英文网页搜索 + 2 次官方页面直接访问（code.minimax.io、agent.minimaxi.com/download）
- 来源优先级：MiniMax 官方文档/博客 > 权威媒体（澎湃、InfoQ、华尔街见闻、新浪财经/IT之家）> 技术社区实测（掘金、CSDN、腾讯云社区、知乎）> 第三方聚合（datalearner、pricepertoken 等，已标注）

## 核心结论速览

1. **MiniMax M3 已发布**：官方开放平台发布日志记录为 **2026 年 6 月 1 日**正式发布（部分媒体报道发布会时间为 5 月 31 日），权重于 **6 月 12 日**在 HuggingFace/ModelScope 开源。用户所称"当前为 MiniMax M3"属实。
2. **版本线**：M2（2025-10-27）→ M2.1（2025-12-22）→ M2.5（2026-02-12）→ M2.7（2026-03-18）→ M3（2026-06-01）。M2.x 系列均为约 230B 总参 / 10B 激活 MoE；M3 升级为约 428B 总参 / 23B 激活，1M 上下文，原生多模态。
3. **MiniMax Code 是官方编程工具**：随 M3 同步推出/更新，形态为 Web 版（code.minimax.io 入口）+ 桌面客户端（macOS/Windows/Linux，agent.minimaxi.com/download），核心卖点为 Agent Team 多智能体协作、持久记忆与技能、IM（微信/飞书/Telegram）接入。
4. **Coding Plan 已演变为 Token Plan**：2026-03-23 由 Coding Plan 升级为 Token Plan（全模态），2026-05-13 与 Agent Plan 合并；2026 年 6 月 M3 上线后 Starter（¥29）等旧档停售，计费从"按请求次数"改为"按 token 量"，引发"变相涨价"争议。
5. **主要口碑定位**：性价比/速度之王，适合轻量级、高频 Agent 任务；常见坑包括高峰限速、长思维链烧输出 token 甚至截断、Claude Code 兼容性问题（任务难中断）、M2.7 商用授权收紧。

---

## 一、M3 发布事实与规格

**Claim 1**: MiniMax M3 已于 2026 年 6 月 1 日正式发布，是 MiniMax 当前旗舰语言模型，面向 Agent 推理、工具调用、代码、多模态 Chat 输入和长上下文任务。[^1^]
Source: MiniMax 开放平台官方文档「模型发布」
URL: https://platform.minimaxi.com/docs/release-notes/models
Date: 2026-07-16（页面抓取时间）
Excerpt: "2026 年 6 月 1 日 全新语言模型 MiniMax-M3 正式发布，面向 Agent 推理、工具调用、代码、多模态 Chat 输入和长上下文任务。"
Context: 官方一手发布日志。同一页面还记录了 M2.5（2026 年 2 月）、M2.7（2026 年 3 月 18 日）、M2.1（2025 年 12 月 22 日）等发布时间。注意：澎湃新闻旗下"大模型之家"报道发布会时间为"5月31日，MiniMax正式发布M3模型"，两处相差一天，可表述为"2026 年 5 月 31 日—6 月 1 日发布"。
Confidence: high

**Claim 2**: M3 为 MoE 架构，总参数约 428B、激活参数约 23B（60 层），采用自研 MSA（MiniMax Sparse Attention）稀疏注意力，原生支持 1M token 上下文（官方保障至少 512K 可用），提供 thinking / non-thinking 两种推理模式。[^2^][^3^]
Source: cnblogs（GPUStack 实测文）/ 百度百科「MiniMax M3」
URL: https://www.cnblogs.com/gpustack/p/20622313 ; https://baike.baidu.com/item/MiniMax%20M3/67882412
Date: 2026-06-18 / 2026-07-24
Excerpt: "MiniMax-M3 是一款原生多模态大模型，采用 MoE 架构，约 428B 总参数 / 23B 激活参数，原生支持 1M（百万级）上下文，并提供 thinking（思考）与 non-thinking（非思考）两种推理模式"；"该模型基于自研MiniMax Sparse Attention（MSA）架构，API最高支持1M tokens上下文窗口，保障至少512K tokens可用"
Context: 注意 M3 参数规模（428B/23B 激活）明显大于 M2.x 系列（约 230B/10B 激活），这意味着"M 系列都是 10B 小激活"的说法对 M3 已不成立。
Confidence: high

**Claim 3**: M3 权重于 2026 年 6 月 12 日在 HuggingFace 与 ModelScope 开源，许可证较 M2.7 大幅放宽：非商业完全免费；年营收低于 2000 万美元的个体/公司仅需邮件告知并标注 "Build with MiniMax"；更高营收企业需联系获取商业许可。[^4^]
Source: yeekal.com AI 早报 / IT之家（经搜狐、新浪转载）
URL: https://yeekal.com/daily/2026-06-13/ ; https://finance.sina.com.cn/stock/t/2026-06-15/doc-inicpewp4889755.shtml
Date: 2026-06-13 / 2026-06-15
Excerpt: "MiniMax 于北京时间今日凌晨正式在 Hugging Face 开源其前沿级 MoE 模型 MiniMax M3 的完整权重（~428B 总参数，~23B 激活参数，60 层）……许可证调整：针对此前 M2.7 商业使用需预审批的批评，M3 许可证大幅放宽：非商业完全免费；年营收低于 2000 万美元的个体/公司仅需邮件告知并标注 'Build with MiniMax'"
Context: 发布日（6月1日）官方仅承诺"10天内开源"，曾引发社区对"先 API 收费后开源"的批评（见 Claim 27）。6 月 12 日兑现承诺。获 vLLM、SGLang、NVIDIA AI、Fireworks AI 等十余家平台 day-0 支持。
Confidence: high

**Claim 4**: M3 是原生多模态模型（从预训练 Step 0 起多模态混合训练，预训练数据规模约 100T tokens），支持图片/视频输入，并具备操作电脑桌面（computer use）能力。[^5^][^6^]
Source: 正观新闻 / 新浪财经（IT之家）
URL: https://wap.zhengguannews.cn/html/zgh/406394.html ; https://finance.sina.com.cn/tech/digi/2026-06-01/doc-inhzwisw4078697.shtml
Date: 2026-06-04 / 2026-06-01
Excerpt: "M3是国内首个同时具备'前沿Coding能力、1M超长上下文、原生多模态'三项核心能力的大模型，也是目前全球唯一具备完整能力组合的开源选项。作为原生多模态模型，M3支持图片和视频的输入，并能操作电脑桌面，实现跨应用、跨文件、跨系统的复杂任务操作。"
Context: "三项能力兼备的国产首个/开源唯一"为官方定位表述，属厂商自报口径。WAIC 2026（7 月 17—20 日）上 M3 亦作为旗舰模型展出。
Confidence: high（事实部分）；medium（"首个/唯一"系厂商口径）

## 二、M3 基准成绩：厂商自报 vs 第三方

**Claim 5**: 厂商自报：M3 在 SWE-Bench Pro 取得 59.0%，超过 GPT-5.5（58.6%）与 Gemini 3.1 Pro、接近 Claude Opus 4.7；Terminal-Bench 2.1 为 66.0%，MCP Atlas 74.2%，KernelBench Hard 28.8%；Agent 端到端评测 Claw-Eval 排名第一；OmniDocBench 超过 Gemini 3.1 Pro。[^7^][^8^]
Source: Apiyi 接入指南（转述官方）/ 正观新闻
URL: https://help.apiyi.com/minimax-m3-api-launch-discount-guide.html ; https://wap.zhengguannews.cn/html/zgh/406394.html
Date: 2026-06-05 / 2026-06-04
Excerpt: "SWE-Bench Pro 跑出 59.0 分，直接反超 GPT-5.5 和 Gemini 3.1 Pro，逼近 Claude Opus 4.7。"
Context: 全部为 MiniMax 官方自报分数。SWE-Bench Pro 是 SWE-bench 家族最难变种。对比来看，Claude Opus 4.8 厂商自报 SWE-Bench Pro 为 69.2%（腾讯云社区对比文），M3 与之差约 10 分。
Confidence: high（数值确为官方口径）；medium（未经充分第三方复测）

**Claim 6**: 第三方验证（首批）：摩根大通研报指出，M3 发布后 Artificial Analysis、Code Arena、OpenRouter 开始提供独立证据——M3 跻身 Artificial Analysis 中国前沿模型前列；Code Arena WebDev 榜按模型排名第 7、按实验室排名第 4（分数接近智谱 GLM-5.1）；OpenRouter 日 token 用量突破 5000 亿。[^9^]
Source: 新浪财经（转述小摩研报）
URL: https://finance.sina.com.cn/stock/hkstock/hkgg/2026-06-08/doc-iniasmvs5593329.shtml
Date: 2026-06-08
Excerpt: "M3目前在Artificial Analysis 上已跻身中国前沿模型前列； 在Code Arena WebDev榜单中，按模型排名第7、按实验室排名第4，分数接近智谱GLM-5.1；推出后不久，在OpenRouter上的每日token使用量已突破5，000亿。"
Context: 小摩同时提示关键验证点在于"留存"：若 5 折促销结束后 OpenRouter 用量回落，市场会质疑 M3 能否维持溢价。官方则宣称 M3 发布两周内在 Artificial Analysis 综合智能指数取得"全球开源模型最高排名"（IT之家，2026-06-15，厂商口径）。另有知乎专栏文章（未直接取证）称 6 月 4 日 Artificial Analysis 榜单数据"直接否定了 MiniMax M3 的技术叙事"，提示第三方口碑存在分歧，建议作者引用第三方榜单时注明日期与口径。
Confidence: medium-high

**Claim 7**: 第三方聚合数据：pricepertoken 收录 M3 基准为 Intelligence 44.4（98th percentile）、Coding 58.6（87th percentile）、GPQA 92.9（99th percentile），实测输出约 98 tok/s、TTFT 1.21s。[^10^]
Source: pricepertoken.com
URL: https://pricepertoken.com/pricing-page/model/minimax-minimax-m3
Date: 2026-07-21
Excerpt: "On benchmarks, MiniMax M3 scores Intelligence 44.4 (98th percentile), Coding 58.6 (87th percentile), GPQA 92.9 (99th percentile)… It runs at roughly 98 tokens per second with a 1.21s time to first token."
Context: 第三方聚合站，非一手；可作为厂商自报之外的参照系。
Confidence: medium

## 三、M3 定价与速度

**Claim 8**: M3 API 标准价为输入 $0.60 / 输出 $2.40 每百万 tokens（≤512K 上下文）；发布时 7 天限时 5 折（$0.30/$1.20），6 月 9 日官方宣布 5 折转为永久政策（国内价 2.1 元/百万输入 token，原价 4.2 元）；超过 512K 的长上下文档位价格翻倍。[^11^][^12^]
Source: chooseai.net / nixapi 深度解析
URL: https://www.chooseai.net/news/4326/ ; https://blog.nixapi.com/blog/minimax-m3-deep-dive-2026/
Date: 2026-06-10 / 2026-06-18
Excerpt: "时间线很简单：6月1日MiniMax发布M3旗舰模型，同步开启7天限时5折；6月8日活动到期；6月9日官方宣布——不恢复原价，永久5折。新定价是2.1元/百万输入Token（512K上下文以内），原价4.2元，直降50%，没有截止日期。"
Context: 长上下文（>512K）价格为输入 $1.20 / 输出 $4.80（标准价口径）。以 500K 输入 + 100K 输出的典型 Agent 任务估算，M3 成本约为 Claude Opus 4.7 的 5%、GPT-5.5 的 4.9%（第三方测算）。
Confidence: high

**Claim 9**: M3 输出速度上线初期仅约 30 TPS，官方称 6 月 15 日前后已提升至约 80 TPS，并计划继续提速 30—40%。API 提供 M3 与 M3-highspeed 两个版本（输出结果一致，后者更快）；但 2026 年 6 月起公开 Token Plan 订阅档位中不提供 M3-highspeed 端点（极速能力由 M2.7-highspeed 承担）。[^13^][^14^][^15^]
Source: IT之家（经新浪转载）/ 新浪科技 / CSDN（gitcode 套餐分析）
URL: https://finance.sina.com.cn/stock/t/2026-06-15/doc-inicpewp4889755.shtml ; https://finance.sina.com.cn/tech/digi/2026-06-01/doc-inhzwisw4078697.shtml ; https://gitcode.csdn.net/6a20c8bd10ee7a33f2775da5.html
Date: 2026-06-15 / 2026-06-01 / 2026-06-04
Excerpt: "目前 M3 的输出速度已从上线时的约 30 TPS提升至约 80 TPS，接下来还会继续提速 30-40%"；"现行公开档的 M3 没有 highspeed 变体——仅有标准 M3……所有套餐均可调 M2.7-highspeed 极速版（TPS 100，每次请求按需选择）"
Context: 意味着"极速版 100+ TPS"在 2026 年年中之后对应的是 M2.7-highspeed（及已停售老档的 M2.5-highspeed），而非 M3。写书时需注意区分。
Confidence: high

## 四、M2 / M2.1 / M2.5 / M2.7 版本演进

**Claim 10**: M2 于 2025 年 10 月 27 日发布并开源（MIT 协议、可商用），230B 总参 / 10B 激活 MoE，SWE-bench Verified 69.4 分，API 输入 $0.30 / 输出 $1.20 每百万 token，推理速度约 100 token/s。[^16^][^17^]
Source: 掘金「AI一周资讯」/ CSDN
URL: https://juejin.cn/post/7566897837764034610 ; https://adg.csdn.net/69533cca5b9f5f31781bfb1e.html
Date: 2025-10-31 / 2025-11-14
Excerpt: "2025年10月27日，MiniMax悄悄发布并正式开源M2模型……编程能力在SWE - bench Verified测试获69.4分、Terminal - Bench测试得46.3分，仅次于GPT - 5、Claude和Claude 4.5"
Context: M2 是 MiniMax 编程/Agent 路线的起点，主打"智能、速度、价格不可能三角"。M2.1 于 2025 年 12 月 22 日发布（官方发布日志），定位"多语言编程专家"。
Confidence: high

**Claim 11**: M2.5 于 2026 年 2 月 12 日上线、2 月 13 日正式发布并全球开源（MIT 协议），同为约 230B 总参 / 10B 激活，官方上下文窗口 204,800 tokens；厂商自报 SWE-Bench Verified 80.2%、Multi-SWE-Bench 51.3%（发布时排名第一，超过 Claude Opus 4.6 的 50.3）、BrowseComp 76.3%。[^18^][^19^][^20^]
Source: MiniMax 官方博客 / ModelScope 官方模型卡 / 百度百科
URL: https://www.minimaxi.com/blog/minimax-m25 ; https://modelscope.cn/models/MiniMax/MiniMax-M2.5/summary ; https://baike.baidu.com/item/MiniMax%20M2.5/68117364
Date: 2026-02-12 / — / 2026-07-01
Excerpt: "boasting scores of 80.2% in SWE-Bench Verified, 51.3% in Multi-SWE-Bench, and 76.3% in BrowseComp (with context management)"；"MiniMax M2.5于2026年2月12日上线，并于2026年2月13日正式发布且全球开源"
Context: 官方模型卡注明 SWE 系列测试"using Claude Code as the scaffolding, with the default system prompt overridden, and results averaged over 4 runs"——即分数依赖于脚手架与 scaffold 设置，SemiAnalysis 亦指出这些为 "MiniMax-published scores"。第三方（datalearner 收录的独立评测）SWE-bench Verified 80.20 与官方一致。注意部分第三方页面将 M2.5 上下文误标为 128K 或 196K，官方文档统一为 204,800。
Confidence: high（官方口径）；medium（"排名第一"为发布时点厂商口径）

**Claim 12**: M2.5 的性价比叙事：官方称 100 TPS 连续运行 1 小时成本 1 美元（50 TPS 时 0.3 美元），1 万美元可支撑 4 个 Agent 连续工作一年；第三方综述引用"每 100 美元预算可完成 327.8 个任务，是 Opus 的 10 倍以上"。[^21^][^22^]
Source: 华尔街见闻 / teamday.ai（前沿模型综述）
URL: https://wallstreetcn.com/articles/3765648 ; https://www.teamday.ai/zh/blog/best-ai-models-2026
Date: 2026-02-13 / 2026-02-20
Excerpt: "在每秒输出100个token的高速运行环境下，M2.5连续工作一小时的成本仅需1美元，若降至50 token/秒，成本进一步下探至0.3美元"；"MiniMax M2.5在$100预算内完成327.8个任务 — 是Opus的10倍以上"
Context: "327.8 任务/100 美元"源自 MiniMax 官方传播口径（SWE-bench 类任务），被多家媒体转引；属厂商测算，非第三方实测。API 定价：M2.5 输入 $0.30/输出 $2.40 每百万 token（100 TPS 版），50 TPS 版输出半价（$1.20）。
Confidence: high（为官方口径）；medium（实际任务成本因场景而异）

**Claim 13**: M2.7 于 2026 年 3 月 18 日正式发布（3 月 16 日曾短暂出现在官方文档与 DesignArena），仍是约 230B 总参 / 10B 激活、204.8K 上下文；最大技术叙事是"首个深度参与自身训练流程的模型"——基于 M2.7 构建的 RL Harness 承担研发工作流约 30—50% 工作量；并新增原生 Agent Teams 多智能体协作能力。[^23^][^1^]
Source: DataLearner 模型页 / MiniMax 官方发布日志
URL: https://www.datalearner.com/ai-models/pretrained-models/minimax-m2-7 ; https://platform.minimaxi.com/docs/release-notes/models
Date: 2026-07-17（页面更新）/ —
Excerpt: "M2.7 最大的技术亮点是首次将模型引入自身训练循环：基于 M2.7 构建的强化学习 Harness 驱动了实验监控、日志排查、代码修复与评测循环，模型可承担相关研发工作流约 30–50% 的工作量。"
Context: 厂商自报成绩：SWE-Pro 56.22%（接近 GPT-5.3-Codex）、SWE Multilingual 76.5、GDPval-AA ELO 约 1500（开放权重最高）、Toolathon 46.3%。
Confidence: high

**Claim 14**: 值得注意的基准回退：第三方评测发现 M2.7 的 SWE-Bench Verified 为 78%，较 M2.5 的 80.2% 回退 2.2 个百分点；MiniMax 在 M2.7 发布材料中转而强调其自建的新基准（SWE-Pro、Toolathon、GDPval-AA）。M2.7 的 Multi-SWE-Bench 则小幅提升至 52.7%。[^24^]
Source: ChatForest 评测
URL: https://chatforest.com/reviews/minimax-m2-7-self-evolving-agentic-llm-review/
Date: 2026-05-13
Excerpt: "The SWE-Bench Verified regression is the most significant benchmark finding in M2.7's launch. M2.5 scored 80.2%… M2.7 scores 78%, a 2.2-percentage-point regression on the same benchmark."
Context: 对作者的提示：引用 MiniMax 各代"刷新 SOTA"的说法时，需注意厂商会更换主打基准；跨代比较应固定同一基准。
Confidence: medium-high

**Claim 15**: M2.7 于 2026 年 4 月 12 日前后开源，但更换为"Modified-MIT"协议限制商用（商用需书面授权 + 显著标注 "Built with MiniMax M2.7"），引发 Hacker News 与 HuggingFace 社区激烈争议；随后 MiniMax 增补第 5 条"Permitted Free Uses"，明确自托管用于写代码、开发应用/Agent、研究均免费。[^25^][^26^]
Source: InfoQ / 网易号（协议全文分析）
URL: https://www.infoq.cn/article/UGpjbIzIbbxbZ3XyWeRL ; https://www.163.com/dy/article/KQJ57MM70519EA27.html
Date: 2026-04-14 / 2026-04-15
Excerpt: "商业用途需获得MiniMax书面授权。非商业用途依旧免费且不受限制，科研、个人项目、自用微调等场景均不受影响；但若是搭建托管服务或开发商业产品，则必须申请授权。"
Context: 这是 MiniMax 首次打破 M2/M2.5 的 MIT 完全开源惯例（背景：2026 年 1 月港交所上市，募资约 6.2 亿美元）。M3 开源时许可证已回调放宽（见 Claim 3）。写书若涉及开源合规，此事件是典型案例。
Confidence: high

## 五、MiniMax Code 编程工具形态

**Claim 16**: "MiniMax Code"是 MiniMax 官方编程 Agent 产品，随 M3 于 2026 年 6 月 1 日同步发布/更新，官方称其为"专为 M3 设计、并与 M3 一起训练的 Agent 产品"；形态为 Web 版 + 桌面客户端（macOS/Windows/Linux），基于 Token Plan 订阅计费、无需单独配置 API Key。[^27^][^28^][^29^]
Source: AiWiki / aitntnews 实测 / kamacoder 评测笔记
URL: https://aiwiki.clawcaff.com/minimax-code-2/ ; https://www.aitntnews.com/newDetail.html?newId=25757 ; https://notes.kamacoder.com/llm/news/minimax-m3.html
Date: 2026-07-03 / 2026-06-02 / 2026-07-17
Excerpt: "MiniMax 官方 AI 编程智能体，基于 M3 模型，支持 Web 和桌面端，开箱即用无需 API Key"；"MiniMax Code 这次也跟着更新。官方说它是专为 M3 设计、并与 M3 一起训练的 Agent 产品。"
Context: 笔者于 2026-07-31 直接访问核实：code.minimax.io 落地为"MiniMax Agent"（桌面版入口）；agent.minimaxi.com/download 为官方桌面客户端下载页，页面标题即"MiniMax Code"。
Confidence: high

**Claim 17**: MiniMax Code 核心机制是 Agent Team：官方下载页描述其可"自主组建小队"——分析目标后决定单 Agent 执行还是多 Agent 协作，"根据任务特性召唤或创建专业 agent 角色"，并具备持久记忆、自动生成技能（Skills）、定时任务与 IM（微信/飞书/Telegram）接入能力。第三方资料进一步描述其采用 Leader/Worker/Verifier（或 Producer+Verifier）对抗式验证 Harness。[^30^][^29^][^31^]
Source: MiniMax 官方下载页（直接访问）/ kamacoder / cloudsai 工具导航
URL: https://agent.minimaxi.com/download ; https://notes.kamacoder.com/llm/news/minimax-m3.html ; https://cloudsai.cn/ai-tutorials/6573.html
Date: 2026-07-31（访问日）/ 2026-07-17 / 2026-07-21
Excerpt: "下达目标，MiniMax Code 自主组建小队……分析并决定单 Agent 执行还是多 Agent 协作……根据任务特性召唤或创建专业agent角色"；"Agent Team 可以把大任务拆成多阶段、可并发、可动态调整的 Workflow，再通过 Producer + Verifier 的对抗式 Harness 循环持续产出、反思、纠错。"
Context: 与 Claude Code 的 Dynamic Workflows 属同一方向。kamacoder 同时提醒：Agent 越多 token 消耗越大、错误传播链越长，关键在子任务拆解、中间验证与失败回滚。
Confidence: high（官方功能描述）；medium（对抗式验证细节来自二手资料）

**Claim 18**: MiniMax 官方 Agent 能力叙事（自报）：M3 内部测试中独立复现 ICLR 2025 获奖论文（自主运行约 12 小时、18 次 commit、23 张实验图表）；CUDA FP8 矩阵乘 kernel 优化任务中 24 小时内提交 147 次 benchmark、调用 1959 次工具，将硬件峰值利用率从 7.6% 提升至 71.3%，最优解出现在第 145 次提交；PostTrainBench 得分 37.1，仅次于 Opus 4.7（42.4）和 GPT-5.5（39.3）。[^32^][^33^]
Source: 搜狐（官方发布解读）/ 新浪科技
URL: https://www.sohu.com/a/1030735978_129720 ; https://finance.sina.com.cn/tech/digi/2026-06-01/doc-inhzwisw4078697.shtml
Date: 2026-06-01
Excerpt: "M3 自主运行约 24 小时，完成了 147 次 benchmark 提交和 1959 次工具调用，将硬件峰值利用率从 7.6% 推进至 71.3%，实现 9.4 倍加速。"
Context: 均为官方博客披露的内部案例，用于佐证"长程任务不轻易放弃"的 Agent 行为；无第三方复现。
Confidence: medium（厂商自报案例）

**Claim 19**: MiniMax 内部采用数据（自报）：M2.5 发布后，公司内部 30% 的整体任务由 M2.5 自主完成，新提交代码的 80% 由 M2.5 生成；M2.5 发布时（2026 年 3 月）成为 OpenRouter 上最受欢迎模型之一。[^21^][^34^]
Source: 华尔街见闻 / CSDN 实战指南
URL: https://wallstreetcn.com/articles/3765648 ; https://blog.csdn.net/tzchao111/article/details/159696193
Date: 2026-02-13 / 2026-03-31
Excerpt: "其内部30%的整体任务已由M2.5自主完成，覆盖研发、产品、销售等核心职能。特别是在编程场景中，M2.5生成的代码已占据新提交代码的80%"
Context: OpenHands 创始人 Graham Neubig 评价"M2.5 是第一个在近期测试中超越 Claude Sonnet 的开源模型"（第三方背书）；OpenHands 官方测试认为其在多文件开发任务上接近 Claude Sonnet 级别。
Confidence: medium-high

## 六、Coding Plan → Token Plan：定价与额度演变

**Claim 20**: 2026 年初的 Coding Plan（已停售的旧体系）：Starter ¥29/月（每 5 小时 40 prompts）、Plus ¥49（100 prompts/5h）、Max ¥119（300 prompts/5h）；极速版（M2.5-highspeed，约 100 TPS，官方称 3 倍于同类产品）Plus-极速 ¥98、Max-极速 ¥199、Ultra-极速 ¥899（2000 prompts/5h）；按 prompts 计量、5 小时滑动窗口、无周限额、未用完可累积。[^35^][^36^]
Source: CSDN 防背刺指南 / 掘金订阅指南
URL: https://blog.csdn.net/qq_42320804/article/details/160788116 ; https://juejin.cn/post/7615074940828958739
Date: 2026-05-05 / 2026-03-09
Excerpt: "Starter 基础套餐：¥29/月，提供 40 prompts / 每5小时 的额度……极速版系列：提供 Plus-极速版（¥98/月）、Max-极速版（¥199/月）等选项，明确支持 MiniMax-M2.5-highspeed 模型，主打约 100 TPS 的极速推理，是同类产品生成速度的3倍。"
Context: 用户提供的背景信息（Starter 29 元/月、每 5 小时 40 次 prompt、极速版 100+ TPS）与此完全一致，但需注意这是 2026 年 6 月前的旧套餐；1 个 prompt ≈ 15—20 次模型调用。
Confidence: high

**Claim 21**: 套餐体系两次重构：2026 年 3 月 23 日 Coding Plan 升级为 Token Plan（一个订阅打通语言/视频/语音/音乐/图像全模态）；2026 年 5 月 13 日 Token Plan 与 Agent Plan 合并（CLI、API、Agent 额度跨端共享）。[^37^]
Source: 百度百科「Token Plan」
URL: https://baike.baidu.com/item/Token%20Plan/67526959
Date: 2026-05-13（事件时间）
Excerpt: "2026年3月23日，稀宇科技（MiniMax）推出Token Plan全模态订阅计划，取代了原有的Coding Plan……2026年5月13日，MiniMax宣布将Token Plan与Agent Plan订阅体系合并。新的订阅方案允许用户通过一份订阅打通CLI、API、Agent全部能力"
Context: 2026 年 4 月凤凰网实测确认"官方已经调整了名称，改为 token plan了"；同文记录国内外双价：Starter 国内 ¥29（600 请求/5h）vs 海外 $10（1500 请求/5h）。
Confidence: high

**Claim 22**: M3 上线后（2026 年 6 月）套餐现状：Starter（¥29）、Plus-极速（¥98）、Max-极速（¥199）三档停售（老用户可续订、断订不可恢复）；在售主力为 Plus ¥49/月（官方月 token 上限约 6 亿）、Max ¥119（约 18 亿）、Ultra ¥469（约 71 亿），M3 与 M2.7 共享月度 token 池，额度受 5 小时/周/月多窗口控制；Max-极速老用户可迁移至新 Max（¥199→¥119 并补差价积分）。所有现行档位每次请求可选 M2.7-highspeed（100 TPS）。[^15^][^33^]
Source: gitcode（CSDN）套餐调整分析 / 新浪科技
URL: https://gitcode.csdn.net/6a20c8bd10ee7a33f2775da5.html ; https://finance.sina.com.cn/tech/digi/2026-06-01/doc-inhzwisw4078697.shtml
Date: 2026-06-04 / 2026-06-01
Excerpt: "本次核心更新：MiniMax-M3 全量上线公开订阅……原生多模态；现行公开档 M3 无 highspeed；新增 Ultra（官方月 Token 上限 7100M ≈ 71 亿）；Starter / Plus-极速 / Max-极速 停售、老用户可续订"
Context: 海外版 Token Plan 为 Plus $20（约 17 亿 token）、Max $50（约 51 亿）、Ultra $120（约 98 亿）。官方称同价格下用量约为 Claude 订阅的 15 倍（厂商口径）。
Confidence: high

**Claim 23**: 官方限制条款：Token Plan 面向个人交互式使用，生产环境建议按量付费；存在 RPM/TPM 速率限制（超限约 1 分钟恢复），高峰时段（通常工作日 15:00—17:30）动态限流，官方给出的高峰承载参考为 Plus 约 3—4 个 Agent、Max 约 4—5 个、Ultra 约 6—7 个；套餐内额度受 5 小时固定窗口和周窗口控制且"未使用完的套餐内额度不会结转到下一个计费周期"。[^38^]
Source: MiniMax 官方 Token Plan FAQ
URL: https://platform.minimaxi.com/docs/token-plan/faq
Date: 2026-06-08（页面时间）
Excerpt: "MiniMax 将在高峰时段进行动态限流：流量高峰时段：根据集群负载动态调整，通常出现在工作日 15:00-17:30。Plus：约支持 3-4 个 Agent。Max：约支持 4-5 个 Agent。Ultra：约支持 6-7 个 Agent。"
Context: 一手官方文档。注意官方口径与旧 Coding Plan 时代"无周限额、额度可累积"的宣传已发生变化。
Confidence: high

**Claim 24**: API 按量定价（国内站，元/百万 token）：M2.7 与 M2.5 输入 2.1 / 输出 8.4；highspeed 版输入 4.2 / 输出 16.8（高速模式价格翻倍）；缓存读取 0.21—0.42。海外美元价：M2.5 $0.30/$2.40（100 TPS 版），50 TPS 版输出减半。[^39^][^40^]
Source: CSDN 七大模型定价对比 / DataLearner M2.5 页
URL: https://blog.csdn.net/dong123dddd/article/details/160454279 ; https://www.datalearner.com/ai-models/pretrained-models/minimax-m2-5
Date: 2026-04-27 / 2026-07-17
Excerpt: "MiniMax-M2.7 2.1 / 8.4；MiniMax-M2.7-highspeed 4.2 / 16.8……注：highspeed 版本为高速模式，输出更快但价格翻倍。"
Context: 支持 Anthropic API（推荐）与 OpenAI API 两种兼容接入，可接入 Claude Code、Codex CLI、Cursor、Cline、OpenCode 等工具。
Confidence: high

## 七、用户口碑与常见坑

**Claim 25**: 典型正面口碑：MiniMax 被视为国内 Coding Plan"性价比之王/入门首选"——常规价格全平台最低、不限购不抢购、额度宽松；极速版稳定性好，TPS 可达 100 且极少限频；适合预算有限的个人开发者与学生、轻量级 Agent 任务与高并发场景。[^41^][^42^]
Source: 掘金 5 月平台解析 / CSDN 横向测评
URL: https://juejin.cn/post/7641048219231436846 ; https://blog.csdn.net/fly0512/article/details/162521529
Date: 2026-05-18 / 2026-07-02
Excerpt: "核心优势：常规价格全平台最低……极速版稳定性出色，TPS可达100，极少遇到限频问题……不足：顶级模型能力略逊于智谱GLM-5.1。适用人群：预算有限、日常编程任务繁重的个人开发者与学生群体。"；"MiniMax M2.5 参数规模相对较小，但推理速度快、Token 配额慷慨……适用人群：注重响应速度、适合轻量级 Agent 任务和云端部署场景的开发者。"
Context: 用户提供的背景线索"模型规模小适合轻量任务"与第三方测评口径一致（M2.x 仅 10B 激活）。多份横评同时指出其短板："高峰限速、复杂逻辑推理一般""顶级模型能力略逊于智谱 GLM-5.1"。
Confidence: high

**Claim 26**: 高峰期算力紧张的用户投诉：2026 年 3 月 OpenClaw 热潮期间，用户反映 MiniMax"龙虾部署上去，聊两句就掉线，API 动不动返回限速警告"，官方客服建议"检查本地网络"；媒体总结为"高峰时期限速太严重"。[^43^]
Source: DoNews
URL: https://www.donews.com/article/detail/8612/98790.html
Date: 2026-03-27
Excerpt: "MiniMax那边更离谱，龙虾部署上去，聊两句就掉线，API动不动返回限速警告……简单来说就是，你花了钱，但算力不一定是你的。什么时候能用上，看运气，因为高峰时期限速太严重了。"
Context: 与官方 FAQ 的高峰动态限流机制（Claim 23）互为印证。属 2026 年春季国产模型集体"算力荒"背景下的现象。
Confidence: medium-high

**Claim 27**: M3 发布时的两大社区争议：（1）发布当天只开 API、权重"10 天后给"，被质疑"先宣传开源再延期给权重"、无法复现 benchmark；（2）Token Plan 从按请求次数改为按 token 总量计费且新增周窗口，老用户称其为"变相涨价/背刺"——官方 6 亿 token 按单次 50K 估算约 1.2 万次调用，而长上下文重度场景单次几十万 token 是常态。[^44^]
Source: 钛媒体
URL: https://www.tmtpost.com/8011839.html
Date: 2026-06-03
Excerpt: "改成了什么？按总量来看。Plus套餐49块6亿token……这个6亿token是按单次调用50K token来估算的，折算出来大约是12000次调用……更不接受的是原来承诺老用户不受周限额限制，现在却出尔反尔。"
Context: V2EX 用户将其与此前"代金券事件"并列。官方后续对老用户发放一次性补偿积分（新浪科技报道）。
Confidence: high（争议事实）；medium（"变相涨价"为用户评价）

**Claim 28**: M3 实测吐槽："雷霆大思考"——思维链过长、思考效率低，经常思维链吃满 output token 导致截断；有社区测评认为其实际能力"中等偏下，和半年前的 GLM5 打个平手"；长思维链 + 按 token 计费的组合使用户为无效思考反复付费。[^45^]
Source: ele-yufo 深度拆解（引用 locdd.com 社区实测）
URL: https://www.ele-yufo.com/posts/minimax-m3/
Date: 2026-07-04
Excerpt: "今天早上测这么几道题给我截断了一万次。思考效率比 DeepSeek 都差，经常是思维链吃满 output token 就断了。……相比自家的 2.5 和 2.7 进步卓著……能力实际来说中等偏下，和半年前的 GLM5 打个平手。"
Context: 二手转述社区实测，样本有限；与 Trae 论坛首批测评（Claim 29）相互印证 token 消耗高的问题。
Confidence: medium

**Claim 29**: Trae 论坛首批实测：同一项目同一提示词下，M3 token 消耗 116 万 vs Qwen3.7-Max 41 万，耗时 63 分钟 vs 16 分钟，项目理解被评为"差"；测评者同时指出 M3"思考过程相比上一代 M2.7 更容易触发全英文""整体性能表现没有达到官方宣称的标准""对项目目录的理解依旧不足，仍会出现根目录分辨错误"。[^46^]
Source: Trae 论坛（AI 充电站）
URL: https://forum.trae.cn/t/topic/20255
Date: 2026-06-01
Excerpt: "不足！· 思考过程相比于上一代M2.7而言更容易触发全英文 · 整体性能表现没有达到官方宣称的标准 · 对项目目录的理解依旧不足，仍会出现根目录分辨错误的问题"
Context: 单项目主观测评（通过 OpenCode 免费通道、上下文锁 200K），测评者自己声明"本次体验并不代表模型的全部能力"。作为早期口碑样本引用，需注明局限。
Confidence: medium

**Claim 30**: 工具链兼容性坑：（1）Claude Code 接入 MiniMax M2/M2.7 时存在"无法临时接管中止"的兼容性问题——模型会把单一任务跑完才接受中途输入，建议不要给长任务、必要时开新会话；（2）MiniMax 官方 Coding Plan 的 M2.7 不能稳定作为 Codex CLI 官方兼容路径，社区建议改用 M2.5 + Codex CLI 0.57.0。[^47^][^48^][^49^]
Source: 腾讯云社区评测 / cnblogs 对比 / GitHub（DeepScientist 文档）
URL: https://developer.cloud.tencent.com/article/2587428 ; https://www.cnblogs.com/ybmj/p/19824358 ; https://github.com/ResearAI/DeepScientist/blob/main/docs/zh/15_CODEX_PROVIDER_SETUP.md
Date: 2025-11-13 / 2026-04-05 / —
Excerpt: "使用 Claude Code 接入 MiniMax M2 以后，会有无法临时接管中止的隐患，除非它自己把单一任务完成后才会接受中间用户输入的信息……所以尽量不要给他长任务"；"MiniMax 官方 Coding Plan 里的 MiniMax-M2.7，当前并不能稳定作为 Codex 官方兼容路径使用。"
Context: 腾讯云社区同篇测评结论：M2 在初中级任务满足要求且比 Claude 4.5 快，但"核心代码或者疑难问题上，MiniMax M2 的能力还是距离 Claude 4.5 有一定距离"——与"适合轻量任务"的整体口碑一致。
Confidence: medium-high

**Claim 31**: 较新的正面实测：2026 年 7 月有 Java+Vue 全栈开发者认为"CC + MiniMax-M3 确实比 CC + DeepSeek-V4-Pro 编码能力强一截，至少不会冒出来低级编译错误"；另有聚合评测建议将 M3 定位为"成本效率更好的 agentic/多模态默认模型"，Opus 4.8 作为高难任务的 premium 升级路径。[^50^][^51^]
Source: 慕课网手记 / EvoLink 对比
URL: https://www.imooc.com/article/395796 ; https://evolink.ai/zh/blog/minimax-m3-vs-claude-opus-4-8-coding-agents
Date: 2026-07-14 / 2026-07-18
Excerpt: "所以站在Java + Vue 全栈开发者的视角，CC + MiniMax-M3 确实比CC + DeepSeek-V4-Pro 编码能力强一截。"
Context: 近 1 个月口碑较发布初期有所回暖（可能与官方持续提速优化有关）；EvoLink 为 API 聚合商，立场需注意。
Confidence: medium

## 八、公司与生态背景（供写作背景引用）

**Claim 32**: MiniMax（稀宇科技）2026 年 1 月在港交所上市，募资约 6.2 亿美元，投资方含阿里巴巴与阿布扎比主权财富基金；截至 2026 年 5 月底全球企业开发者客户超百万（半年增长 5 倍）、全球用户约 3 亿；WAIC 2026（7 月 17—20 日）上以 M3 为旗舰展出并预热下一代多模态模型 H3。[^26^][^52^][^53^]
Source: 冷月清谈（转引）/ 澎湃"大模型之家" / 网易（WAIC 报道）
URL: https://www.xinfinite.net/t/topic/18813 ; https://m.thepaper.cn/newsDetail_forward_33291314 ; https://www.163.com/dy/article/L274AFJB0519EI0N.html
Date: 2026-04-14 / 2026-06-02 / 2026-07-19
Excerpt: "截至5月28日，MiniMax全球企业开发者客户超百万（半年增长5倍），全球用户规模约3亿，ARR翻番周期压缩至60天。"
Context: H3（新一代多模态视频模型）在官方发布日志中标记为"2026 年 7 月 31 日"条目，即本书调研截止日附近的新动作，可关注。
Confidence: medium-high

---

## 写给作者的 3—5 个要点

1. **直接回应"M3 是否已发布"：已发布，且是当前旗舰。** M3 于 2026 年 6 月 1 日发布（部分媒体记 5 月 31 日）、6 月 12 日开源权重。规格务必与 M2.x 区分：M2/M2.5/M2.7 均为约 230B 总参/10B 激活、204.8K 上下文；M3 为约 428B 总参/23B 激活、1M 上下文（保底 512K）、原生多模态 + computer use。书中若沿用"M 系列=10B 小模型"的旧印象会对 M3 失真。
2. **引用基准分数时务必标注"厂商自报"与时点。** Multi-SWE-Bench 51.3、"$100 完成 327.8 个任务"、SWE-Bench Pro 59.0 反超 GPT-5.5 等均为官方口径；且 M2.7 曾在 SWE-Bench Verified 上相对 M2.5 回退（78% vs 80.2%），厂商有"换基准讲故事"的倾向。可用的第三方锚点：Artificial Analysis 开源第一（官方宣称）、Code Arena WebDev 第 7（小摩研报）、OpenRouter 日用量 5000 亿 token。
3. **价格/套餐是" moving target "，书中必须写明数据截止日。** 2026 年上半年套餐三连变：Coding Plan（¥29 起、按 prompts）→ Token Plan（3 月 23 日）→ 与 Agent Plan 合并（5 月 13 日）→ M3 上线后 Starter/极速版停售、改为按 token 计费（6 月）。"Starter 29 元/40 prompts/5h"已是历史价格；"极速版 100+ TPS"目前对应 M2.7-highspeed 而非 M3。老用户"变相涨价"争议是讲订阅制风险的绝佳案例。
4. **常见坑清单（可直接成节）：** ① 高峰时段（工作日 15:00—17:30）动态限流，Plus 档高峰仅约支撑 3—4 个 Agent；② M3 思维链过长（"雷霆大思考"），易吃满 output token 截断并推高账单；③ Claude Code 接入时任务难以中途接管，慎派长任务；④ M2.7 在 Codex CLI 官方路径不稳定；⑤ M2.7 权重"Modified-MIT"限制商用（M3 已放宽：年营收 <2000 万美元邮件告知即可）；⑥ 托管 API 数据合规敏感场景建议自托管。
5. **定位建议：性价比/速度优先的"默认模型"，而非能力天花板。** 第三方测评共识：MiniMax 适合轻量到中等复杂度、高频、成本敏感的 Agent 编程任务（入门 ¥49/月档全平台最低、不限购），顶级复杂任务仍逊于 Claude Opus 级与智谱 GLM-5.1；实用路由策略是"M3/M2.7 做默认 + Opus 级模型做升级"。MiniMax Code 的官方差异化在 Agent Team 多智能体协作 + 记忆/技能 + IM 接入，可作为"国产官方 Coding Agent"代表与 Claude Code/Cursor 对照。

---

## 引用来源列表

[^1^]: MiniMax 开放平台「模型发布」 https://platform.minimaxi.com/docs/release-notes/models
[^2^]: cnblogs「MiniMax-M3 开源实测」 https://www.cnblogs.com/gpustack/p/20622313
[^3^]: 百度百科「MiniMax M3」 https://baike.baidu.com/item/MiniMax%20M3/67882412
[^4^]: yeekal AI 早报 2026-06-13 https://yeekal.com/daily/2026-06-13/
[^5^]: 正观新闻 https://wap.zhengguannews.cn/html/zgh/406394.html
[^6^]: 新浪科技（IT之家） https://finance.sina.com.cn/tech/digi/2026-06-01/doc-inhzwisw4078697.shtml
[^7^]: Apiyi 接入指南 https://help.apiyi.com/minimax-m3-api-launch-discount-guide.html
[^8^]: 正观新闻（同 [^5^]）
[^9^]: 新浪财经·小摩研报 https://finance.sina.com.cn/stock/hkstock/hkgg/2026-06-08/doc-iniasmvs5593329.shtml
[^10^]: pricepertoken M3 https://pricepertoken.com/pricing-page/model/minimax-minimax-m3
[^11^]: chooseai.net「MiniMax M3 永久5折」 https://www.chooseai.net/news/4326/
[^12^]: nixapi「MiniMax M3 深度解析」 https://blog.nixapi.com/blog/minimax-m3-deep-dive-2026/
[^13^]: 新浪财经·IT之家「MiniMax M3 模型正式开源」 https://finance.sina.com.cn/stock/t/2026-06-15/doc-inicpewp4889755.shtml
[^14^]: 新浪科技（同 [^6^]）
[^15^]: gitcode「MiniMax-M3 重磅升级：套餐调整解读」 https://gitcode.csdn.net/6a20c8bd10ee7a33f2775da5.html
[^16^]: 掘金「AI一周资讯 251024-251031」 https://juejin.cn/post/7566897837764034610
[^17^]: CSDN「MiniMax M2 开源大模型」 https://adg.csdn.net/69533cca5b9f5f31781bfb1e.html
[^18^]: MiniMax 官方博客 M2.5 https://www.minimaxi.com/blog/minimax-m25
[^19^]: ModelScope 官方模型卡 MiniMax-M2.5 https://modelscope.cn/models/MiniMax/MiniMax-M2.5/summary
[^20^]: 百度百科「MiniMax M2.5」 https://baike.baidu.com/item/MiniMax%20M2.5/68117364
[^21^]: 华尔街见闻「MiniMax 发布 M2.5」 https://wallstreetcn.com/articles/3765648
[^22^]: teamday.ai「前沿AI模型2026年2月」 https://www.teamday.ai/zh/blog/best-ai-models-2026
[^23^]: DataLearner「MiniMax-M2.7」 https://www.datalearner.com/ai-models/pretrained-models/minimax-m2-7
[^24^]: ChatForest「MiniMax M2.7 Review」 https://chatforest.com/reviews/minimax-m2-7-self-evolving-agentic-llm-review/
[^25^]: InfoQ「MiniMax 修改开源授权引争议」 https://www.infoq.cn/article/UGpjbIzIbbxbZ3XyWeRL
[^26^]: 网易号「MiniMax-M2.7 更新了开源协议」 https://www.163.com/dy/article/KQJ57MM70519EA27.html
[^27^]: AiWiki「MiniMax Code」 https://aiwiki.clawcaff.com/minimax-code-2/
[^28^]: aitntnews「MiniMax 低调发布 M3 和 MiniMax Code 实测」 https://www.aitntnews.com/newDetail.html?newId=25757
[^29^]: kamacoder「MiniMax M3 评测」 https://notes.kamacoder.com/llm/news/minimax-m3.html
[^30^]: MiniMax Code 官方下载页（2026-07-31 直接访问） https://agent.minimaxi.com/download
[^31^]: cloudsai「MiniMax Code 工具导航」 https://cloudsai.cn/ai-tutorials/6573.html
[^32^]: 搜狐「MiniMax M3 来了」 https://www.sohu.com/a/1030735978_129720
[^33^]: 新浪科技（同 [^6^]）
[^34^]: CSDN「MiniMax M2.5 实战指南」 https://blog.csdn.net/tzchao111/article/details/159696193
[^35^]: CSDN「2026.5 国内 AI Coding Plan 防背刺指南」 https://blog.csdn.net/qq_42320804/article/details/160788116
[^36^]: 掘金「OpenClaw Token 太贵顶不住？试试 Coding Plan」 https://juejin.cn/post/7615074940828958739
[^37^]: 百度百科「Token Plan」 https://baike.baidu.com/item/Token%20Plan/67526959
[^38^]: MiniMax 官方 Token Plan FAQ https://platform.minimaxi.com/docs/token-plan/faq
[^39^]: CSDN「2026 国内七大 AI 大模型定价全对比」 https://blog.csdn.net/dong123dddd/article/details/160454279
[^40^]: DataLearner「MiniMax M2.5」 https://www.datalearner.com/ai-models/pretrained-models/minimax-m2-5
[^41^]: 掘金「2026年5月主流AI Coding Plan平台全解析」 https://juejin.cn/post/7641048219231436846
[^42^]: CSDN「国内 AI Coding Plan 横向测评报告（2026年3月）」 https://blog.csdn.net/fly0512/article/details/162521529
[^43^]: DoNews「Kimi、Minimax 们的算力荒」 https://www.donews.com/article/detail/8612/98790.html
[^44^]: 钛媒体「MiniMax M3终于来了，指标很强，但社区炒翻了」 https://www.tmtpost.com/8011839.html
[^45^]: ele-yufo「深度拆解MiniMax M3」 https://www.ele-yufo.com/posts/minimax-m3/
[^46^]: Trae 论坛「Minimax-M3首批体验测评」 https://forum.trae.cn/t/topic/20255
[^47^]: 腾讯云社区「模型评测｜国产模型偷摸删库且装聋作哑」 https://developer.cloud.tencent.com/article/2587428
[^48^]: cnblogs「国内替代 Claude Code」 https://www.cnblogs.com/ybmj/p/19824358
[^49^]: GitHub DeepScientist 文档 https://github.com/ResearAI/DeepScientist/blob/main/docs/zh/15_CODEX_PROVIDER_SETUP.md
[^50^]: 慕课网手记「Claude Code + MiniMax-M3」 https://www.imooc.com/article/395796
[^51^]: EvoLink「MiniMax M3 vs Claude Opus 4.8」 https://evolink.ai/zh/blog/minimax-m3-vs-claude-opus-4-8-coding-agents
[^52^]: 澎湃「大模型之家2026年5月热力榜」 https://m.thepaper.cn/newsDetail_forward_33291314
[^53^]: 网易「MiniMax 携 M3、H3 亮相 WAIC 2026」 https://www.163.com/dy/article/L274AFJB0519EI0N.html
