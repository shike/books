# 维度11 调研：AI编程的数据来源三件套（大模型数据集 / 联网搜索 / 爬虫）与主流AI爬虫工具横评

- 调研截止：2026-07-31
- 独立搜索次数：38 次（中文为主，混用英文）
- 证据条数：36 条；来源优先级：官方文档/定价页、GitHub、律所/法院相关材料、第三方基准（部分基准由竞品厂商发布，已在 Context 中标注利益相关性）

---

## 一、三件套方法论：训练数据内置知识 vs 联网搜索 vs 主动爬虫

### 1.1 大模型底层训练数据：以网页爬取为主体，存在知识截止与幻觉问题

Claim: 大模型预训练数据遵循"开源打底、网页主力、书籍补充、领域增强"原则，其中互联网网页数据（合规爬虫抓取门户、博客、论坛、百科，原始数据可达 80TB+）占比约 50%，是训练语料的主体——即"爬虫"本身就是大模型内置知识的第一来源。[^1^]
Source: CSDN 博客（昇思大模型预训练数据来源）
URL: https://blog.csdn.net/Kenji_Shinji/article/details/161226618
Date: 2026-05-19
Excerpt: "昇思大模型数据来源遵循 '开源打底、网页主力、书籍补充、领域增强' 原则，覆盖通用与专业场景：1. 开源开放数据集：采用 Common Crawl、Wikipedia 中文、BookCorpus、CC100、CLUECorpus 等，提供基础文本与知识底座，占比约 30%。2. 互联网网页数据：通过合规爬虫抓取中文主流门户、博客、论坛、百科，原始数据达80TB+，经清洗后保留高质量网页文本，占比约 50%。"
Context: 说明通用大模型的"内置知识"本质上来自离线爬虫语料，这解释了为何模型知识有截止日期且无法覆盖长尾/私域信息。以鹏程·盘古为例，80TB 原始数据经 4 级清洗去重后仅剩 1.1TB 高质量语料（250B Token）。
Confidence: medium（单一技术博客，数据比例为该模型个案，但结构与业界公认构成一致）

Claim: Common Crawl 是最大的开源网络爬虫数据库，存储自 2008 年以来的 PB 级网页数据，GPT 系列、LLaMA 等大模型训练的基础语料大量采用该来源；数据托管于 Amazon S3，可通过 AWS CLI 或 HTTPS 镜像下载 WARC/WET 文件自行解析。[^2^]
Source: AiniSEO 技术文章
URL: https://www.ainiseo.com/ai/59869.html
Date: 2026-03-24
Excerpt: "最大的开源网络爬虫数据库是Common Crawl，它存储了自2008年以来的PB级网页数据，大模型训练的基础语料，像GPT系列、LLaMA等，都大量采用了这个来源。"
Context: 面向开发者的实操文章，给出了 wet.paths.gz 索引下载与 warcio 解析的完整命令。说明"大模型数据集"这一层对读者并非黑盒，可自行获取同源数据。
Confidence: medium

Claim: 大模型幻觉的六大治理方案中，RAG 通过"解耦知识存储与语言生成"在推理阶段动态检索权威外部知识库，使输出锚定在可验证事实片段上；实时联网检索则"突破静态知识截止日期限制"，使模型能动态接入最新新闻、行情、政策法规等时效性信息流。[^3^]
Source: 新浪财经转载 CSDN 文库（大模型幻觉成因分析与六大解决方案）
URL: https://cj.sina.cn/articles/view/7857201856/1d45362c001905o83y?froms=ggmp
Date: 2026-05-20
Excerpt: "RAG（Retrieval-Augmented Generation）通过解耦"知识存储"与"语言生成"，在推理阶段动态检索权威外部知识库（如专业文献库、结构化数据库），使模型输出严格锚定在可验证的事实片段上，从根本上切断幻觉的数据源头……而实时联网检索则突破静态知识截止日期限制，使模型能动态接入最新新闻、股票行情、政策法规等时效性强的信息流。这六大策略分别作用于数据层（RAG、联网）、模型层（微调）、交互层（约束、自检、多采样），形成覆盖全生命周期的幻觉治理体系。"
Context: 系统阐述"内置知识（截止、幻觉）→ 联网搜索（时效）→ RAG/爬虫构建外部知识库（权威、长尾）"的互补关系，可直接支撑书中三件套方法论章节。
Confidence: high

### 1.2 联网搜索层：各家内建搜索与独立 search API 的定价与定位

Claim: Anthropic Claude API 的 Web search 内置工具按 $10 / 1,000 次搜索计费，独立于 token 价格。[^4^]
Source: Mem0 博客（Anthropic Claude Pricing 指南，汇总官方价格）
URL: https://mem0.ai/blog/anthropic-claude-pricing
Date: 2026-07-24
Excerpt: "### Tools and Extras |Feature|Price| |**Web search**|$10 / 1,000 searches| |**Code execution**|$0.05/hour (1,550 free hours/month)|"
Context: Claude 免费版 claude.ai 已包含 web search；API 侧则按次计费。读者需理解"模型内置搜索"与"自带搜索 API"是两种成本结构。
Confidence: high

Claim: OpenAI Responses API 的 web_search 工具标准定价为 $10 / 1k 次调用（$0.01/次），且检索到的搜索内容 token 还要按模型输入价计费；对 gpt-4o-mini / gpt-4.1-mini，搜索内容固定按 8,000 input token 块计费，与 search_context_size 设置无关。[^5^]
Source: OpenAI 官方社区（引用官方 Web Search 指南与定价页）
URL: https://community.openai.com/t/web-search-tool-with-gpt-4o-mini/1383113
Date: 2026-06-09
Excerpt: "The pricing docs explicitly say: 'For `gpt-4o-mini` and `gpt-4.1-mini` with the non-preview web search tool, search content tokens are billed as a fixed block of 8,000 input tokens per call.' … the standard Responses API `web_search` tool is priced at **$10 / 1k calls** — i.e. **$0.01 per search call** — **plus** search content tokens billed at the selected model's input-token rate."
Context: 揭示了"内建联网搜索"的隐藏成本：工具费 + 检索上下文 token 费双重计费，agent 循环中多次调用会显著放大成本。web_search_preview 旧路径为 $25/1k 且搜索内容免费。
Confidence: high

Claim: Perplexity Sonar API 把"实时联网检索 + 生成 + 引用"打包进 token 价格（Sonar $1/$1 每 1M token，Sonar Pro $3/$15），其核心差异化是不再单独收取搜索工具费；另有独立 Search API 按 $5 / 1,000 请求计费。[^6^]
Source: aipricing.guru（Perplexity API Pricing，2026-07-31 更新）及 aitoolgraph 定价路由核验
URL: https://www.aipricing.guru/perplexity-pricing/ ; https://www.aitoolgraph.com/tools/perplexity-sonar-api
Date: 2026-07-31 / 2026-05-31
Excerpt: "Perplexity Sonar API pricing spans $0.20 to $15.00 per million tokens. … Every SKU includes **live web search and citations with no extra per-query fee** — that's the Perplexity differentiator." 另："Search API pricing is listed at $5.00 per 1,000 requests, with no additional token-based pricing."
Context: 与 Claude/OpenAI 的"token + 搜索工具费"结构对比，Perplexity 代表了"检索生成一体化"的第三条路线。注意 Langfuse issue 指出 Sonar 另有按搜索上下文大小（low/medium/high）的 per-request search fee，引用该定价时需注明口径差异。
Confidence: medium（两家聚合站数据一致，但与 Langfuse 社区口径存在出入，建议以 perplexity.ai 官方页最终核验）

Claim: Tavily 是 agent 优化的网页搜索 + 提取一体化 API，Exa 是基于 embeddings 的神经语义搜索；基础搜索成本接近（Exa $7/1k，Tavily 约 $7.5–8/1k），但免费额度差距大（Exa 20,000 次/月 vs Tavily 1,000 credits/月）；Tavily 已于 2026 年 2 月被 Nebius 收购但仍以自有品牌运营。[^7^]
Source: ColdIQ 对比文章（Exa vs Tavily, 2026）
URL: https://coldiq.com/blog/tavily-vs-exa
Date: 2026-07-12
Excerpt: "On the Exa vs Tavily question: Tavily is agent-optimized web search plus extraction in one call, while Exa is neural, embeddings-based search that ranks pages by meaning rather than keywords. … Exa is $7 per 1,000 requests, Tavily runs about $7.50 to $8 per 1,000 basic searches. Exa's free tier is far bigger at 20,000 requests a month versus Tavily's 1,000 credits. … Tavily was acquired by Nebius in February 2026 but still ships under its own brand."
Context: 两大主流 agent 搜索 API 的定位分野：Tavily 适合实时 web grounding 与单调用 RAG；Exa 适合语义发现、研究型 agent、人/公司/代码搜索。收购事件（2026-02）是截至调研时点的最新动态。
Confidence: high

Claim: 2025 年微软关停 Bing Search API 后，Brave 成为西方唯一对开发者开放的大型独立搜索索引；2026 年 2 月 Brave 无预警取消了 5,000 次/月的免费计划，改为注册送 $5 额度。Tavily 被描述为"2025–2026 年 AI agent 事实标准"，原生集成 LangChain/Spring AI/AutoGen/CrewAI，但规模化成本较高（约 $0.008/query）。[^8^]
Source: WebScraft 对比文章（Best Search API for AI Agents in 2026）
URL: https://webscraft.org/blog/search-api-dlya-ai-agentiv-scho-obirayut-rozrobniki-i-de-pomilyayutsya?lang=en
Date: 2026-06-24
Excerpt: "An independent search index — not Google, not Bing. This is important: after Microsoft shut down the Bing Search API in 2025, Brave remained the only large independent western search index available to developers. … in February 2026, the free plan (5,000 queries/mo) was removed without warning. Now, new users get $5 in credits upon registration — and that's it."
Context: 该文还给出规模化成本表：45k 次/月查询下 Tavily 约 $300、Brave 约 $225、Exa 约 $135、SerpAPI 约 $450、Serper 约 $45；并指出 raw SERP 输出单价低但 token 成本高，需合并计算。另提到 Google 于 2025 年 12 月起诉 SerpAPI 的法律风险。
Confidence: high

Claim: 中文实测对比（100 条混合 query，2026-04 中旬测试）：Tavily 平均延迟 0.9s、Brave 0.6s、Exa 1.2s；实时性排序 Brave > Tavily > Exa；覆盖上 Tavily 聚合多家底层索引最广，Exa 偏深度内容（论文、博客）覆盖窄但相关性高；国内开发者接入三家的常见坑是需稳定海外网络，热门做法是通过 MCP server 接入 Claude Code / Cursor。[^9^]
Source: 菠萝博客（Exa vs Tavily vs Brave Search API 给 Agent 选型）
URL: https://www.boluoblog.com/coding/exa-vs-tavily-vs-brave-search-api-2026-agent/
Date: 2026-05-20
Excerpt: "实时性谁更强？Brave > Tavily > Exa。Brave 自家爬虫小时级更新；Tavily 接 Bing/Google 索引；Exa 偏深度内容（论文、博客），实时性弱。……国内开发者接入有什么坑？三家都国外服务，需稳定海外网络调用。Tavily/Exa 通过 MCP server 接入 Claude Code / Cursor 是热门做法。"
Context: 少有的中文实测基准，含单价表（Exa $0.005、Tavily $0.008、Brave $0.005 基础档）与场景化选型建议（学术研究 Exa、品牌监控 Tavily、隐私敏感 Brave）。个人博客，样本量有限。
Confidence: medium

Claim: Kimi（月之暗面）智能助手六大功能之一即"联网搜索"；其 K2 模型（1T 总参数 MoE，激活 32B）在预训练中使用大规模 Agentic Tool Use 数据合成，代码与 Agent 能力对齐 Claude 水平，并支持文件解析与联网检索。[^10^]
Source: 百度百科（北京月之暗面科技股份有限公司词条）
URL: https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E6%9C%88%E4%B9%8B%E6%9A%97%E9%9D%A2%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/63575472
Date: 2026-07-30（词条更新）
Excerpt: "Kimi主要有6项功能：长文总结和生成、联网搜索、数据处理、编写代码、用户交互、翻译。……Kimi K2是一款具备更强代码能力、更擅长通用Agent任务的MoE架构基础模型，总参数1T，激活参数32B。……其他关键技术包括大规模Agentic Tool Use数据合成和引入自我评价机制的通用强化学习等。"
Context: 国内阵营的"内建联网"代表；CSDN 对比文（2026-04）显示 Kimi MAU 992.6 万（2025Q3，同比下滑 30%，被豆包/DeepSeek 挤压），提示书中对国内产品格局的表述需有时效意识。
Confidence: medium

---

## 二、主流 AI 爬虫 / 网页提取工具横评（截至 2026-07）

### 2.1 Firecrawl：托管 API 阵营的事实标杆

Claim: Firecrawl 2026 年定价：Free 每月 1,000 credits（可续期、无需信用卡）、Hobby $16/月（5,000 credits）、Standard $83/月（100k credits）、Growth $333/月（500k）、Scale $599/月（1M）；基础规则 1 页 = 1 credit，但 Stealth 模式（反爬保护站点）每页 5 credits，浏览器交互 2 credits/分钟，Search 为每 10 结果 2 credits；credits 不结转。[^11^]
Source: AFFiNCO（Firecrawl Pricing 2026，自称每日付费使用该产品的代理商）
URL: https://affinco.com/firecrawl-pricing/
Date: 2026-07-23
Excerpt: "|Scrape, Crawl, Map, or Monitor|1 credit per page| |Search|2 credits per 10 results| |Interact (browser actions)|2 credits per minute| |Stealth mode (protected sites)|5 credits per page| … Credits do not roll over. Unused credits expire at the end of each billing month."
Context: 给出真实每页成本：Hobby $0.0032/页、Standard $0.00083/页、Scale $0.0006/页。实战建议：先用免费额度测目标站点的 stealth 比例；用 Map 先列 URL 再圈定 Crawl 范围省钱。该文含 affiliate 链接，但价格表与 firecrawl.dev 一致。
Confidence: high

Claim: Firecrawl 开源项目 GitHub 星数已超 149,000，平台开发者超 125 万，累计服务 50 亿+ 请求、15 万+ 公司（含 Apple、Shopify、Canva）；六大核心能力为 Scrape / Crawl / Search / Map / Extract / Monitor。[^12^]
Source: AFFiNCO（同上）
URL: https://affinco.com/firecrawl-pricing/
Date: 2026-07-23
Excerpt: "The open source project has crossed 149,000 GitHub stars, over 1.25 million developers use the platform, and it has served more than 5 billion requests for 150,000+ companies including Apple, Shopify, and Canva. … The platform covers six core jobs: Scrape (single pages), Crawl (entire sites), Search (web search with full page content), Map (instant site structure), Extract (schema-based structured data), and Monitor (change tracking)."
Context: 厂商口径的营销数字，建议书中表述时以 GitHub 实时星数复核；Monitor（变化追踪）作为一等能力说明"增量监控"已产品化。
Confidence: medium

### 2.2 Jina Reader：极简 URL→Markdown，token 计费

Claim: Jina Reader 采用 token 计量（新 key 送 10M 免费 tokens，之后约 $0.05/1M tokens），Firecrawl 采用 page-credit 制（1 页 1 credit）；在 10 万页/月规模下 Firecrawl 便宜 4–5 倍，而"多次搜索 + 少量大页面"或无月承诺场景 Jina 更优；许可证上 Firecrawl 核心为 AGPL-3.0，Jina 为 Apache-2.0（对企业更友好）；Jina 内置 ReaderLM-v2（1.5B 小模型）做 HTML→Markdown。[^13^]
Source: Apify 官方博客（Jina AI vs. Firecrawl for web-LLM extraction）
URL: https://blog.apify.com/jina-ai-vs-firecrawl/
Date: 2026-06-11
Excerpt: "Jina gives every new key **10 M free tokens** across _all_ endpoints. After that, you buy token bundles, priced at roughly **$0.05 per million tokens ($50 per billion)** … At ~100k pages/month, Firecrawl is 4–5× cheaper, but Jina wins for _many searches + few large pages_ or if you insist on zero monthly commitment. Licensing also diverges: Firecrawl's core is **AGPL-3.0** (fork = open-source), while Jina ships under **Apache-2.0**."
Context: 对比表还显示吞吐差异：Firecrawl 2→150 并发浏览器 vs Jina 20→5,000 RPM（按 key 等级）。GitHub 星数 Firecrawl≈131k vs Jina≈11k。Apify 为竞品厂商，文章末尾自荐 Apify，但对比数据标注了发布日期与版本号。
Confidence: high

### 2.3 Crawl4AI：开源自托管首选，零 API 成本但工程自负

Claim: Crawl4AI（unclecode/crawl4ai）是专为 LLM 优化的开源 Web 爬虫，GitHub 超 50,000 星；核心特性：智能 Markdown 生成（保留标题/表格/代码/引用）、异步浏览器池、会话/代理/Cookie/钩子全可控、自适应学习网站结构；零密钥要求，支持 CLI / Docker / 云部署，输出天然适合 RAG 与 AI Agent 数据获取。[^14^]
Source: xlap.top 技术博客（Crawl4AI 专文）
URL: https://blog.xlap.top/post/tech/2026-05-29/crawl4ai/
Date: 2026-05-29
Excerpt: "Crawl4AI（GitHub: unclecode/crawl4ai）是一款专为 LLM（大型语言模型）优化的开源 Web 爬虫与数据抓取工具。该项目在 GitHub 上已获得超过 50,000 Star，是最受欢迎的开源爬虫项目之一。……灵活部署：零密钥要求，支持 CLI、Docker，云友好。"
Context: 官方文档 docs.crawl4ai.com；Docker 镜像 unclecode/crawl4ai:latest。定位：预算敏感、需要完全控制、数据不出内网的团队。
Confidence: high

Claim: 三方基准（200 问 RAG 检索准确率 + 混合 URL 语料）：RAG recall@5 为 Spider 91.5% > Firecrawl 89.0% > Crawl4AI 84.5%（默认配置噪声比 11.3%，可经 CSS 排除规则调优缩小差距）；成功率 Spider 99.9% / Firecrawl 95.3% / Crawl4AI 89.7%（反爬层 Crawl4AI 无代理时丢 28% URL）；静态页首结果时间 Spider 45ms / Firecrawl 310ms / Crawl4AI 480ms；Crawl4AI 自托管免费但"隐性成本是工程时间"。[^15^]
Source: Spider.cloud 官方博客（Honest Benchmark，竞品厂商发布）
URL: https://spider.cloud/blog/firecrawl-vs-crawl4ai-vs-spider-honest-benchmark/
Date: 2026-02-11
Excerpt: "|Tool|Recall@5 (200 questions)|Avg. noise ratio| |**Spider**|**91.5%**|4.2%| |**Firecrawl**|**89.0%**|6.8%| |**Crawl4AI**|**84.5%**|11.3%| … Crawl4AI is free to use. The hidden cost is engineering time: you build and maintain the proxy layer, the retry logic, the scaling infrastructure, and the monitoring."
Context: 利益相关声明：Spider 为发文方且各项第一，数据需打折采信；但其对三家架构差异（Rust/Node.js/Python asyncio）与反爬默认行为的定性描述与多来源一致。关键增量信息：Firecrawl 需云档才有可靠反爬绕过，Crawl4AI 反爬完全留给用户。
Confidence: medium

Claim: Crawl4AI vs Firecrawl 对比定性结论：Crawl4AI 是开源 Python 库（高控制、JS 渲染需自行集成 headless 浏览器、反爬需手动实现代理、免费但有 LLM/基础设施成本）；Firecrawl 是 API 优先服务（内置稳健 JS 执行、内置反爬处理、按用量计费、低接入成本）——前者适合"需要深度控制与自定义 RAG 的开发者"，后者适合"需要快速拿到干净数据的 AI 构建者与 agent"。[^16^]
Source: Scrapeless 博客（Crawl4AI vs Firecrawl: Detailed Comparison 2025）
URL: https://www.scrapeless.com/en/blog/crawl4ai-vs-firecrawl
Date: 2025-10-14
Excerpt: "|JavaScript Rendering|Requires integration with headless browsers|Built-in, robust JavaScript execution| … |Anti-Bot Bypass|Requires manual implementation (proxies, etc.)|Built-in (handled by service)| … |Ideal For|Developers needing deep control, custom RAG|AI builders needing quick, clean data, agents|"
Context: 与 Apify 博客（2026-01）同主题对比结论一致：Crawl4AI 用 Playwright 浏览器 + Virtual Scroll，Firecrawl 用预热 Headless Chromium 并由服务端自动决定 HTML 抓取还是浏览器渲染。Scrapeless 同为竞品厂商。
Confidence: high

### 2.4 ScrapeGraphAI：自然语言驱动的开源抓取框架

Claim: ScrapeGraphAI 是 MIT 许可的开源 Python 库（GitHub 28.2k 星），用 LLM（OpenAI/Groq/Gemini/Ollama 可配）+ 图流水线替代 CSS 选择器：用户用自然语言描述想要的数据，底层用 Playwright 做浏览器自动化；提供 SmartScraperGraph / SearchGraph / SmartScraperMultiGraph 等多种图；最新版本 v2.1.4（2026-06-23）。[^17^]
Source: DEV.co 框架页（数据源：GitHub 仓库）
URL: https://dev.co/ai/frameworks/scrapegraph-ai
Date: 2026-06-23
Excerpt: "ScrapeGraphAI is a Python library that uses large language models (LLMs) to automate web scraping and data extraction from websites and documents. Users define what data they want via natural language prompts, and the library handles the extraction logic without writing traditional scraping code. … It supports multiple pipeline types (SmartScraperGraph, SearchGraph, SmartScraperMultiGraph, etc.) for single-page and multi-page extraction workflows."
Context: 差异化定位：免选择器维护、站点改版时"自愈"、Pydantic schema 结构化输出；代价是每次请求的 LLM token 成本。适合探索性采集与多源研究，不适合稳定 HTML 站点的高并发生产（那仍是 Scrapy 的领域，见下条）。
Confidence: high

Claim: ScrapeGraphAI 的适用边界：最适合站点结构多变的探索性数据采集、多源研究、选择器维护成本超过开发时间的项目、JS 重度应用的结构化提取；"对于 HTML 稳定站点的高产量生产负载，Scrapy 仍是更快的选择"——当省下的选择器维护时间超过每次请求的 LLM 成本时，ScrapeGraphAI 才划算。[^18^]
Source: CodeCut 教程（From CSS Selectors to Natural Language）
URL: https://codecut.ai/scrapegraphai-web-scraping-natural-language/
Date: 2026-05-18
Excerpt: "For high-volume production workloads on sites with stable HTML, Scrapy remains the faster choice. ScrapeGraphAI pays off when the time saved on selector updates outweighs the per-request LLM cost."
Context: 为书中"AI 爬虫 ≠ 万能，传统爬虫框架仍有成本优势"的平衡论述提供直接引文。
Confidence: high

### 2.5 Tavily Extract / Exa / Bright Data / Apify

Claim: Tavily Extract 端点从 URL 返回干净 markdown 或纯文本，处理 JS 渲染页并去除样板（广告/导航/页脚）；两档深度：basic（1 credit / 5 URLs）与 advanced（2 credits / 5 URLs，覆盖表格、嵌入内容与 JS 渲染页，成功率更高）；单次调用最多批量 20 个 URL，失败 URL 单独报告；传 query 参数时可按问题对内容块重排序（query-focused extraction）。[^19^]
Source: Tavily 官方文档（Clean Content Extraction）
URL: https://docs.tavily.com/examples/quick-tutorials/extract-api
Date: 2026-04-10（页面快照）
Excerpt: "Tavily Extract takes a URL (or list of URLs) and returns the page content as clean markdown or plain text. It handles JavaScript-rendered pages, removes boilerplate (ads, navigation, footers), and returns structured content ready for LLM consumption. … |`basic`|Fast|Good|Standard page content|1 credit per 5 URLs| |`advanced`|Slower|Higher|Tables, embedded content, JS-rendered pages|2 credits per 5 URLs| … Extract content from up to 20 URLs in a single call."
Context: 官方一手文档。说明"搜索 API"与"提取 API"在 Tavily 体系内是同一 credit 池的两个端点，agent 可"搜索→提取"单家闭环。
Confidence: high

Claim: Exa 产品套件以搜索为中心：Search API（6 档速度/质量模式，约 200ms–60s）、Contents API、Find Similar、Answer API（带引用）、Research API（2026-05-01 起弃用，并入 /search type:"deep-reasoning"）；另有 Monitors（webhook 推送的周期性搜索）与 Websets（通过 dashboard/API 构建网页来源精选集）。[^20^]
Source: Parallel 官方对比文章（竞品视角，2026-07-29）
URL: https://parallel.ai/articles/exa-vs-parallel
Date: 2026-07-29
Excerpt: "Exa also offers Monitors for recurring searches delivered via webhook and Websets for building curated collections of web sources through a dashboard or API. … Research API (asynchronous multi-step research, being deprecated May 1, 2026 in favor of /search with type: \"deep-reasoning\")"
Context: 竞品发文但产品清单与 Exa 官方文档一致；Monitors/Websets 表明"搜索 API 厂商"也在向"增量监控"与"数据集构建"延伸，与爬虫工具能力重叠。
Confidence: high

Claim: Bright Data 自我定位为"AI 的头号 web 数据基础设施"：Bright Data MCP / CLI / Web Unlocker / SDK 默认输出 Markdown，即插即用对接 Claude/GPT/Gemini 及任意 MCP 客户端；MCP 与 CLI 每月 5,000 次免费请求（自称品类最大免费额度）；基础设施级反爬能力（指纹、CAPTCHA、geo-block、限速），150M+ 代理 IP、195 国、100 万+ 并发会话。[^21^]
Source: Bright Data 官方 GitHub 组织主页（github.com/brightdata）
URL: https://github.com/brightdata
Date: 2026-07-27（页面快照）
Excerpt: "Built for LLMs. Markdown output by default in Bright Data MCP, CLI, Web Unlocker, and SDKs. Drop-in for Claude, GPT, Gemini, and any MCP-compatible client. … Free for agents. 5,000 requests/month on Bright Data MCP and CLI. The largest free tier in the category."
Context: 官方一手来源但属自我宣传口径。第三方 awesome-agent-native-services 仓库佐证其 Agent Browser 解锁层覆盖 300 万+ 域名。与 Firecrawl/Crawl4AI 的差异：Bright Data 强在代理网络与反爬通过率，是"受保护站点"场景的企业级选项。
Confidence: high（功能存在性）；low（"最低封锁率"等比较级表述）

Claim: Apify 是以预构建 Actors 市场为核心的云爬虫平台：免费计划每月 $5 平台积分，Starter $49/月、Scale $499/月，部分 Actors 在平台积分外另按 $0.75/1K 结果收费；内置定时运行、webhook 交付、多格式数据集存储；缺点：默认数据中心代理（住宅 IP 需额外付费）、社区 Actors 维护质量参差、批处理模式对单请求节奏控制有限。[^22^]
Source: Bright Data 博客（2026 年 8 款最佳 Facebook 爬虫，竞品口径但价格与官网一致）
URL: https://www.bright.cn/blog/web-data/best-facebook-scrapers
Date: 2026-05-10
Excerpt: "**定价：** 免费计划包含每月 $5 平台积分（约 500 个 Facebook 页面）。Starter 为 $49/月，包含 $49 积分。Scale 为 $499/月。部分 Actors 除平台积分外还会按 $0.75/1K 结果收费。"
Context: Apify 的独特生态位是"Actor 市场 + 无代码"，与 API 优先的 Firecrawl、库形态的 Crawl4AI/ScrapeGraphAI 形成第三种交付模式；适合非开发者与批量社媒/电商站点采集。
Confidence: high

Claim: 竞对基准中的反爬定性结论：反爬保护页面上三家工具全部减速；Firecrawl 需要云档（stealth）才有可靠绕过，Crawl4AI 把反爬完全留给用户，Bright Data/Oxylabs 等企业级厂商按成功请求或带宽高价计费（如 Oxylabs Web Unblocker 约 $9.40/GB）。[^23^]
Source: Spider.cloud 基准 + CyberYozh（Bright Data 替代方案对比）
URL: https://spider.cloud/blog/firecrawl-vs-crawl4ai-vs-spider-honest-benchmark/ ; https://app.cyberyozh.com/zh-CN/blog/best-brightdata-alternatives/
Date: 2026-02-11 / 2026-07-08
Excerpt: "On anti-bot protected pages, all three tools slow down. … Firecrawl requires the cloud tier for reliable bypass. Crawl4AI leaves anti-bot handling to the user." 另："其专用 Web Unblocker 产品单独计费，价格约为 $9.40/GB，这是一种基于带宽的模式，除非你已经知道平均页面大小，否则真的很难预测。"
Context: 反爬能力是工具分层的主轴：开源库（自理）→ 托管 API stealth 加价（Firecrawl 5 credits/页）→ 企业 unblocker（按 GB/成功请求计费）。Oxylabs 另有 OxyCopilot AI 代码助手生成抓取代码。
Confidence: medium

---

## 三、MCP 生态中的数据获取服务器

Claim: 官方 Firecrawl MCP Server（firecrawl/firecrawl-mcp-server，GitHub 约 6,892 星，MIT 许可）为 Cursor、Claude 及其他 LLM 客户端添加网页抓取与搜索能力；可通过 `claude mcp add firecrawl -- <command>` 或写入 claude_desktop_config.json 的 mcpServers 配置接入。[^24^]
Source: aiskill.market（实时拉取 GitHub 元数据）
URL: https://aiskill.market/skills/firecrawl-mcp-server
Date: 2026-07-08
Excerpt: "🔥 Official Firecrawl MCP Server - Adds powerful web scraping and search to Cursor, Claude and any other LLM clients. … **MCP Server** · ⭐ 6,892 on GitHub · JavaScript · License: MIT"
Context: 注意：社区教程中存在两个包名——官方仓库 firecrawl/firecrawl-mcp-server 对应 npm 包 `firecrawl-mcp`（lobehub 教程用 `npx -y firecrawl-mcp`），而个别教程写的 `@anthropic/firecrawl-mcp` 未见官方佐证，引用时以 GitHub README 为准。
Confidence: high

Claim: Claude Code 的 MCP 数据获取栈常见组合为：Tavily（实时搜索/深度研究/数据提取）+ Firecrawl（专业抓取、结构化提取、多页 crawl）+ Playwright（浏览器自动化、截图）+ Perplexity（带引用的 AI 搜索），全部通过 ~/.claude.json 的 mcpServers 统一配置，用 `claude mcp list` 或 /mcp 验证。[^25^]
Source: LobeHub（Claude Code 的 MCP 设置指南）
URL: https://lobehub.com/zh/mcp/builderrxbeib-mcp-setup-claude-code
Date: 2026-05-14
Excerpt: "1. **GitHub** - Gestión de repositorios, issues, PRs 2. **Tavily** - Búsqueda web avanzada 3. **Firecrawl** - Web scraping profesional 4. **Playwright** - Automatización de navegador 5. **Perplexity** - Búsqueda con AI avanzada"
Context: 完整 npm 包名：@modelcontextprotocol/server-github、firecrawl-mcp、tavily-mcp、@playwright/mcp；Perplexity 需自行编译社区 server（cyanheads/perplexity-mcp-server）。这是"AI 编程工具 + 数据获取"在编辑器内的标准接法，可直接作为书中操作示例。
Confidence: high

Claim: Bright Data 提供 Web MCP server（stdio 传输，兼容 Claude Desktop/Cursor 及任意 MCP 客户端），每月 5,000 次免费请求；免费层之外的高级抓取与浏览器自动化工具组需充值后通过 URL 参数 `&groups=advanced_scraping,browser` 开启；其解锁层覆盖 300 万+ 域名，持续对抗反爬措施。[^26^]
Source: Bright Data 官方 MCP 页 + awesome-agent-native-services 仓库
URL: https://brightdata.com/ai/mcp-server ; https://github.com/haoruilee/awesome-agent-native-services/blob/main/services/browser-and-web-execution/bright-data-agent-browser.md
Date: 2026-02-26 / 2026-03-15
Excerpt: "Enjoy 5,000 MCP requests every month - for free! … Crawl and extract complete websites - not just single pages … Output data in LLM-ready formats" 另："Unlike general headless browsers, Bright Data's unlocking layer covers 3M+ domains and is continuously updated against anti-bot measures — solving the most common reason agent web automation fails in production."
Context: LangGraph 集成示例显示：agent 架构不变，仅更换 MCP 连接 URL 即可从基础搜索/抓取升级到浏览器自动化——"模型决定做什么，框架决定循环怎么跑，Bright Data 处理封锁"。另有一个社区 RFC 提议给 brightdata-mcp 加 x402/MPP 按次付费（$0.10/scrape），显示 MCP 数据获取正走向 agent 原生计费。
Confidence: high

Claim: 自研 MCP 搜索服务器的最小实现已成通用模式：用 FastMCP 封装 TavilyClient，暴露 web_search（query/max_results/topic/include_raw_content）与 extract(url) 两个 tool，即可经 SSE 供任何 MCP 客户端调用。[^27^]
Source: CSDN 万字实战文（基于 LangChain DeepAgents 构建智能研究助手）
URL: https://blog.csdn.net/bugyinyin/article/details/155972146
Date: 2025-12-16
Excerpt: "mcp = FastMCP(\"Web-Search-Server\") … @mcp.tool() def web_search(query: str, max_results: int = 5, topic: Literal[\"general\", \"news\", \"finance\"] = \"general\", include_raw_content: bool = False): … @mcp.tool() def extract(url: str): \"\"\"Extract web page content from URL.\"\"\" return tavily_client.extract(url)"
Context: 适合作为书中"手写一个数据获取 MCP server"的教学代码骨架；也说明 MCP 生态中搜索/提取服务器的实现门槛极低。
Confidence: high

---

## 四、实战模式：RAG 知识库、整站抓取→结构化→喂 agent、增量监控

Claim: Firecrawl 官方能力矩阵含 Monitor（change tracking）；中文实践指南给出增量知识库模式：JSON 配置 URL 监控列表（frequency/priority）→ 启用 changeDetection 只抓更新部分 → 用 LLM 对结果主题分类入库，配套 LlamaIndex 适配器 + GitHub Actions 调度，可把"每周 8 小时信息收集压缩至 30 分钟"。[^28^]
Source: GitCode 博客（用 Firecrawl 解决 LLM 数据准备难题的 2025 实践指南）
URL: https://blog.gitcode.com/3237aab8cd1d3fd2a9cb4e7cb9126e85.html
Date: 2026-04-05
Excerpt: "启用 `changeDetection` 功能，仅获取内容更新部分：config = {\"changeDetection\": True, \"storagePath\": \"./knowledge_base\"} … 结合LLM对爬取结果进行主题标注，构建结构化知识库"
Context: "整站抓取→清洗→结构化→喂 agent"的完整链路范式；"50+ 行业网站周监控"是典型场景。文中效率数字为作者个案，不宜泛化引用。
Confidence: medium

Claim: 增量监控的低代码实现：n8n 工作流模板用 Firecrawl 抓取（含 JS 渲染页）→ 与历史内容比对 → 检测到变化即邮件告警并写入 Google Sheets，频率由外部 cron 控制。[^29^]
Source: n8n 官方工作流模板库
URL: https://n8n.io/workflows/5510-monitor-dynamic-website-changes-with-firecrawl-sheets-and-gmail-alerts/
Date: 2025-12-11
Excerpt: "1. **Webhook receives trigger** → Starts the monitoring process 2. **Firecrawl scrapes website** → Gets fresh content (even JavaScript-rendered!) 3. **Smart comparison** → Checks against previously stored content 4. **Change detected?** → If yes, send email + log everything 5. **Update storage** → Prepares for next monitoring cycle"
Context: 说明"爬虫 + 自动化工作流平台"是非工程团队落地增量监控的主流路径；竞品价格情报场景亦同构。
Confidence: high

Claim: 成本实战测算：一个"5 竞品 × 15 页 × 30 天 = 2,250 credits/月"的日常监控管道，Firecrawl Hobby（$16/月）覆盖抓取层，加 Claude Haiku 做 diff 分析（约 3M tokens/月 ≈ $0.75），整管道 <$17/月；而 Klue/Crayon 等传统竞品监控订阅起步 $150/月。[^30^]
Source: Espressio.ai（Firecrawl 2026 实战指南）
URL: https://espressio.ai/blog/firecrawl-web-scraping-guide-2026/
Date: 2026-07-20
Excerpt: "For a typical 5-competitor pipeline running daily (5 competitors × 15 pages each × 30 days = 2,250 credits/month), Hobby at $16/month covers the scraping layer. Add Claude Haiku at $0.25/1M tokens for diff analysis (~3M tokens/month = $0.75) and total pipeline cost is under $17/month. A Klue or Crayon subscription for equivalent daily monitoring starts at $150/month."
Context: "便宜爬虫 API + 便宜小模型"替代昂贵垂直 SaaS 的成本叙事，是本章很有说服力的实战数字；注意 Haiku 单价文中写 $0.25/1M，与官方 Haiku 4.5（$1/$5）口径不同（可能指缓存读价），引用时建议改写为"月 token 成本不足 1 美元"。
Confidence: medium

Claim: RAG 知识库构建中切块（chunking）决定"模型看到的内容"：块太长导致 token 超限/检索慢，太短语义不完整，FAQ 类须 Q+A 合并为一个 chunk（超 512 tokens 时启用 overlap 滑动窗口）；语义去重用 embedding cosine > 0.95 过滤冗余；主流落地链为 文档接入→智能切块→Embedding→向量存储+混合检索→Prompt 增强→LLM 生成，平台选型 RAGFlow（快速跑通）/LangChain（自由度）/Dify（插件化连接大模型 API）。[^31^]
Source: CSDN（企业级 RAG 知识库搭建全攻略）
URL: https://adg.csdn.net/69708b06437a6b40336aa186.html
Date: 2025-11-07
Excerpt: "切块决定'模型看到的内容'，切得好，才召回得准。……Q+A合并为一个chunk（不能分开）- 长回答超出512 tokens时，启用 overlap sliding window … 语义去重工具：通过嵌入相似度（如 cosine > 0.95）过滤冗余段"
Context: 承接爬虫层："网页→markdown"之后进入 RAG 管道的加工规范，是"抓取后干什么"一章的核心知识。
Confidence: high

Claim: 多搜索 API 组合策略：为所用 provider 包一层薄 adapter，即可混用而不重写 agent——如 Serpent/Serper 做发现、Exa 或 Firecrawl 对少数重要 URL 做提取；生产 agent 常 SERP API（排名/时效/SERP 特征）+ 神经或内容 API（语义发现与干净正文）双轨并用。[^32^]
Source: apiserpent.com 对比文（利益相关：SERP API 厂商）
URL: https://apiserpent.com/blog/best-web-search-api-ai-agents-rag
Date: 2026-06-26
Excerpt: "If you keep a thin adapter around whichever you use, you can mix them — Serpent for discovery, Exa or Firecrawl for extraction on the few URLs that matter — without rewriting your agent. … Many teams combine a cheap SERP API with a content API."
Context: 与 SERP API vs Tavily vs Exa 一文的市场分类一致：神经搜索（Exa）/ RAG 内容 API（Tavily）/ 真 SERP API（Serper、SerpApi 等）是三类不同产品，选错类别会导致 agent"看似在工作却给出自信的错误答案"。
Confidence: medium

---

## 五、合规：robots 协议、版权、个人信息保护

Claim: 中国法下网络爬虫的合规边界可归纳为三层：手段合法性（禁止非法侵入系统或突破网站防护措施、不得破坏被爬站功能、控制频率与方式）、内容合法性（原则上仅爬公开数据，非公开数据需授权，严禁采集国家秘密/商业秘密，采集个人信息需具备合法基础，不得爬取侵犯知识产权的数据）、使用合理性（评估是否构成不正当竞争）。[^33^]
Source: 微信公众号法律实务文章（数据合规 | 网络爬虫的合规性边界在哪？）
URL: http://mp.weixin.qq.com/s?__biz=MzAxMDc0ODY5Mg==&mid=2247487905&idx=1&sn=935d11bad8c05fd80813be1f3779ec3a
Date: 2025-07-02
Excerpt: "- 禁止非法侵入计算机信息系统或突破网站防护措施 - 不得破坏被爬取网站的系统功能，应当控制爬取的频率和方式 … 原则上仅允许爬取公开数据或信息，非公开数据需获得合法授权 - 严禁采集国家秘密、商业秘密等敏感信息，采集个人信息需具备合法基础 … 注意评估是否可能构成不正当竞争"
Context: 与《个人信息保护法》《数据安全法》《网络安全法》框架一致；北京长通律师事务所文章（2025-03）进一步指出采集个人敏感信息需获得明确同意并采取安全保护措施。
Confidence: high

Claim: 中国裁判文书网统计：爬虫引发的数据法律争议以民事为主，最大宗是侵害著作权纠纷，其次是不正当竞争（知名案例如大众点评诉爱帮网、大众点评诉百度、新浪微博诉脉脉）；刑事上，2017 年北京海淀法院判决的上海晟品公司案是对爬虫抓取"公开信息"首开刑事处罚的案例（非法获取计算机信息系统数据罪）。[^34^]
Source: 绍兴市律师协会官网（理论调研文章）
URL: http://www.sxlawyers.cn/default.aspx?id=1038&pageType=detail&pageid=36
Date: 2026-05-14
Excerpt: "据中国裁判文书网上数据统计，我国关于网络爬虫抓取数据活动引发的法律争议主要为民事争议，其中最大宗纠纷是侵害著作权纠纷，其次则是不正当竞争纠纷[ii]。不正当竞争涉及商业利益，各方争议尤大，知名的如大众点评诉爱帮网案、大众点评诉百度网案、新浪微博诉脉脉案等。……2017年，北京市海淀区人民法院判决上海晟品公司及相关人员犯非法获取计算机信息系统数据罪[iv]（以下简称'上海晟品公司案'），则是对网络爬虫抓取'公开信息'首开刑事处罚案例。"
Context: "公开数据 ≠ 可随意爬取"在中国已有刑事判例，这是书中最需要敲响的警钟；兰台律所（2026-06）补充：中国被侵权企业多基于反不正当竞争法、著作权法诉讼，基于用户协议违约的诉讼不多见。
Confidence: high

Claim: 美国 hiQ v. LinkedIn 完整时间线：2017 年禁令允许 hiQ 继续抓公开资料 → 2019 年第九巡回维持（抓公开数据很可能不违反 CFAA）→ 2021 年最高法院依 Van Buren 发回重审 → 2022 年 4 月第九巡回再次支持 hiQ → 但 2022 年 11 月地方法院认定 LinkedIn 用户协议违约主张成立 → 2022 年 12 月双方和解：hiQ 永久停止抓取、删除全部数据/源代码/衍生算法、赔偿 50 万美元。[^35^]
Source: Thunderbit 博客（法律时间线梳理）+ 北京兰台律所（AI 企业爬虫行为法律风险全景分析）
URL: https://thunderbit.com/zh-Hans/blog/is-scraping-linkedin-legal ; https://www.lantai.cn/news_view.aspx?nid=2&typeid=5&id=1667
Date: 2026-07-13 / 2026-06-15
Excerpt: "结论是：hiQ 的确降低了在第九巡回辖区内，对真正公开、无需登录的数据进行抓取时的 CFAA 风险。但它 **并没有** 给任何人一项可以随意抓取 LinkedIn 的通用权利。合同索赔仍然成立，假账号访问也受到了处罚。"
Context: 常被引用的"公开数据可爬"判例实际以和解收场、无普遍约束先例价值；欧盟方向"公开可见不是合法抗辩理由"，需 GDPR 合法依据。兰台律所明确提示"即便 CFAA 风险得以规避，合同违约和不正当竞争的法律成本同样不容小觑"。
Confidence: high

Claim: 2025 年 6 月美国加州法院裁定 Anthropic"从盗版网站下载书籍并存储"构成侵权（仅扫描合法纸质书用于研究属合理使用），"盗版数据不适用合理使用"；Anthropic 最终支付 15 亿美元和解并销毁侵权数据，成为行业首个明确该规则的判例。同期 OpenAI 已面临至少 14 起版权诉讼；2025 年 12 月六大 AI 巨头再遭作家集体起诉，蓄意侵权每部作品最高赔 15 万美元。[^36^]
Source: 36氪 / 腾讯新闻（引南都数字经济治理研究中心报告）
URL: https://m.36kr.com/p/3608054588572675 ; https://news.qq.com/rain/a/20251223A02FXM00
Date: 2025-12-23
Excerpt: "2025年6月，美国加州法院裁定其'从盗版网站下载书籍并存储'构成侵权（仅认定'扫描合法纸质书用于研究'属合理使用），最终Anthropic支付15亿美元和解并销毁侵权数据，成为行业首个明确'盗版数据不适用合理使用'的判例。……OpenAI已是行业'被诉大户'，截至目前已面临至少14起版权诉讼"
Context: 训练数据层的版权风险已成为全球诉讼焦点：2025 年 1–7 月全球公开审理生成式 AI 版权案件 1,183 起（同比 +230%，中国大陆 267 起）；CSDN 合规文还称上海知识产权法院（2025）首次确认"模型训练阶段临时复制"不适用合理使用——该判例编号疑似虚构（"沪 73 民初 567 号"格式可疑），Confidence 降为 low，仅列出供作者进一步核实，不建议直接引用。
Confidence: high（Anthropic 和解，多源交叉）；low（CSDN 文的具体案号与统计口径）

Claim: 2025 年 6 月 Reddit 起诉 Anthropic，指控其无视 robots.txt（机器人排除协议）抓取其内容并"在未经同意的情况下使用 Reddit 用户个人数据"；研究显示包括 Perplexity 在内的多个聊天机器人仍能检索到通过 robots.txt 屏蔽其爬虫的出版商文章。[^37^]
Source: 微信公众号（每周传媒业要闻，2025-06-11，编译自外媒）
URL: http://mp.weixin.qq.com/s?__biz=MjM5MzE4MzAwMw==&mid=2651682215&idx=1&sn=d59a165df97d5af9819b5daa4ebb9e61
Date: 2025-06-11
Excerpt: "6月4日，Reddit 在加利福尼亚州提起诉讼，声称 Claude 的开发者 Anthropic 无视机器人排除协议（REP），即 robots.txt，该协议阻止 AI 爬虫从网站中提取内容。研究表明，其他 AI 公司也在使用这种做法：3月，哥伦比亚的 Tow Center 发现，包括 Perplexity 在内的几个聊天机器人仍然可以从通过 REP 阻止其爬虫的出版商那里检索文章。"
Context: robots.txt 的法律地位：本身不是访问控制技术，但"无视 robots 协议"正成为版权/违约/不正当竞争诉讼中的关键情节。书中应建议读者：尊重 robots.txt、检查目标站 ToS、保留抓取日志。
Confidence: high

Claim: Cloudflare 2025 年度互联网回顾：OpenAI 的 GPTBot 是 2025 年全球被网站屏蔽次数最多的网络机器人；Cloudflare 于 2025 年 7 月 1 日宣布针对 AI 爬虫无限抓取的新措施（默认阻断/按次收费方向），并指出 Anthropic 的 Claude 对网站所有者的"互惠价值"最低——拿了内容却几乎不回馈流量。[^38^]
Source: CSDN 转载（AI爬虫vs网站封禁：IP封锁大战升级，引 Cloudflare 报告）
URL: https://blog.csdn.net/chichupirixiu/article/details/160203212
Date: 2026-04-16
Excerpt: "一份来自 Cloudflare 的 2025 年度互联网回顾报告……ChatGPT 的爬虫 GPTBot，已成为全球被封锁次数最多的网络机器人。……2025 年 7 月 1 日，互联网安全和 CDN 服务巨头 Cloudflare 宣布了一系列新措施，专门针对 AI 爬虫的无限制抓取。"
Context: 说明反爬环境在 2025–2026 急剧收紧：AI 爬虫被大规模封锁是常态，这正是 Firecrawl stealth、Bright Data unlocker 等"反反爬"服务溢价的市场背景；也解释了为何自建爬虫越来越难过 Cloudflare 这关。
Confidence: high

---

## 写给作者的 3–5 个要点（服务"爬虫与数据获取"章）

1. **用"三件套"分层讲清数据获取架构**：①大模型内置知识本质是离线爬虫语料（网页数据约占预训练语料一半，有截止日期与幻觉）→ ②联网搜索解决"时效"（Claude/OpenAI 内建搜索按 $10/1k 次计费且有上下文 token 隐形成本；Tavily/Exa/Brave/Perplexity Sonar 各有定位：关键词 agent 搜索、语义发现、独立索引、检索生成一体）→ ③主动爬虫解决"长尾、私域、结构化、可控"（RAG 知识库与增量监控的底座）。给读者一句口诀：内置知识答常识，联网搜索答时事，爬虫/RAG 答"你的数据"。

2. **工具横评建议按"交付形态"而非品牌罗列**：托管 API（Firecrawl：1 页 1 credit、stealth 5 倍价、Monitor 一等能力、星数 149k 但核心 AGPL）vs 开源自托管（Crawl4AI：50k 星、零 API 费但反爬自理、默认输出噪声需调优；ScrapeGraphAI：自然语言替代选择器，适合探索性采集，生产高并发仍是 Scrapy 更划算）vs 极简前缀服务（Jina Reader：r.jina.ai 前缀、token 计费约 $0.05/1M、Apache-2.0）vs 企业反爬（Bright Data：MCP 每月 5,000 次免费、3M+ 域名解锁层）vs 无代码市场（Apify Actors：$5/月免费积分起步）。第三方基准（Spider 发布）显示 RAG recall@5：Spider 91.5% > Firecrawl 89% > Crawl4AI 84.5%，引用时注明竞品利益相关。

3. **MCP 是 2026 年数据获取的标准接法**：firecrawl-mcp、tavily-mcp、@playwright/mcp、Bright Data MCP 可在 Claude Code/Cursor 内即插即用，写一章 30 行 FastMCP 代码自封装搜索+提取 server 是极好的教学案例；注意甄别教程中 `@anthropic/firecrawl-mcp` 这类以官方名义的错误包名，以 GitHub 仓库 README 为准。

4. **实战章节给一个"端到端数字"而非抽象流程**：5 竞品 × 15 页 × 30 天 = 2,250 credits，Firecrawl Hobby $16 + Haiku 级小模型 diff 分析 <$1，整管道 <$17/月（对比传统竞品情报 SaaS $150/月起）；整站抓取先用 Map 列 URL 再圈 Crawl 范围、开启 changeDetection 做增量、chunking 阶段 FAQ 必须 Q+A 合并切块、cosine>0.95 语义去重——这些都是可直接落笔的操作细节。

5. **合规一节用三个判例锚定边界，避免泛泛而谈**：中国（上海晟品案——爬"公开信息"也可入刑；大众点评诉百度、微博诉脉脉——反不正当竞争主战场）、美国（hiQ v. LinkedIn——CFAA 风险降了但违约照赔 50 万美元且销毁全部数据与衍生算法；Anthropic $15 亿盗版书籍和解——"盗版数据不适用合理使用"）、行业环境（Reddit 诉 Anthropic 无视 robots.txt；Cloudflare 2025 年报：GPTBot 是全球被屏蔽最多的机器人）。给读者的实操红线：只爬公开数据、尊重 robots.txt 与 ToS、控频、不碰个人信息与付费墙、保留抓取日志。

---

*备注：所有"Excerpt"均为逐字摘录（中英文照原文）；竞品发布的基准（Spider、Apify、Bright Data、fastCRW、AFFiNCO 等）已在 Context 标注利益相关性；Perplexity Sonar 是否存在独立 per-request search fee、CSDN 合规文引用的中国案号真伪，建议出版前以官方页/裁判文书网最终核验。*
