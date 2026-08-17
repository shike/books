# 维度09：登录态下的浏览器自动化 与"复刻SaaS功能"实战（截至2026年7月）

> 调研日期：2026-07-31。服务《AI编程实战》案例二："客户给一个用户名密码，让AI登录上去复制一个SaaS/已有功能"。
> 覆盖：工具现状对比 / 登录态处理实战 / "看懂再复制"工作流 / 复杂任务管理与控制 / 法律合规边界。

---

## 一、AI浏览器自动化工具现状与选型

### 证据 1：Browser Use 是当前最流行的开源浏览器agent框架，WebVoyager 89.1%

Claim: Browser Use 是最流行的开源 AI 浏览器 agent 框架，在 WebVoyager 基准（586个多样web任务）上达到 89.1% 成功率，为当前 SOTA。[^1^]
Source: Firecrawl Blog — 11 Best AI Browser Agents in 2026
URL: https://www.firecrawl.dev/blog/best-browser-agents
Date: 2026-06-16
Excerpt: "Browser Use is the most popular open-source framework for building AI browser agents, and for good reason. It hit **89.1% success rate on the WebVoyager benchmark** (586 diverse web tasks), making it the current state-of-the-art for autonomous web interaction."
Context: 该文还指出其局限："You're responsible for your own infrastructure (browser management, proxies, scaling)"，生产使用需搭配 Browserbase 等托管浏览器。
Confidence: high

### 证据 2：Browser Use 的项目体量与融资（一手背景）

Claim: 截至2026年5月，Browser Use 在 GitHub 超 91k Star，获 1700 万美元融资；两个苏黎世联邦理工学生用五周做出演示版后开源。[^2^]
Source: 昭昭AI笔记 — Browser Use凭什么9.4万Star？
URL: https://www.zhaozhaoai.com/biji/394.html
Date: 2026-05-31
Excerpt: "截至2026年5月，Browser Use在GitHub上已斩获 **91k+ Star**，在WebVoyager评测基准上达到了 **89.1%的成功率**，成为AI驱动网页自动化领域公认的行业标杆。"
Context: 团队2026年4月又发布仅592行 Python 的 Browser Harness，通过 WebSocket 直连 Chrome，允许 AI 在执行中"实时编写缺失的功能"。
Confidence: medium（二手报道，数字与 Firecrawl 口径一致）

### 证据 3：2026 年选型共识——DOM驱动为主路径，视觉驱动为备选；80/20 混合模式

Claim: 2026 年生产模式是 DOM 驱动（Browser Use/Stagehand/Playwright）为主路径，视觉驱动（Skyvern、Computer Use、CUA）作为 canvas/反bot 场景备选；生产团队把重复的 80% 缓存为确定性 Playwright，只留 20% 给 AI 推理。[^3^]
Source: 阿里云开发者社区 — 2026 年开源 Agent 工具包选型指南
URL: https://developer.aliyun.com/article/1740959
Date: 2026-06-11
Excerpt: "一般情况下生产环境通常把重复的 80% 缓存到 Playwright（确定性浏览器自动化库）里，Browser Use 只处理需要推理的 20%。……2026 年的生产模式通常两者并用：DOM 驱动作为主路径，Skyvern 或 Anthropic Computer Use 或 OpenAI CUA 作为选择器在 canvas 元素或反机器人屏幕上持续失败时的备选路径。"
Context: 同文指出 Browser Use 最大问题是"每一步都消耗一次 LLM 调用，新颖任务尚可，重复工作流则成本过高"。
Confidence: high

### 证据 4：Stagehand——TypeScript 阵营的"AI+代码混合"框架

Claim: Stagehand（Browserbase 开源 SDK）提供 act/extract/observe/agent 四个原语，让开发者精确选择每一步用多少 AI；v3 基于 CDP 重写引擎，速度提升 44%。[^4^]
Source: Stagehand 官方文档 + 阿里云选型指南
URL: https://docs.stagehand.dev/v3/first-steps/introduction ; https://developer.aliyun.com/article/1740959
Date: 2026-06-19 / 2026-06-11
Excerpt: "Stagehand gives you the best of both worlds through four powerful primitives that let you choose exactly how much AI to use" / "Stagehand v3（2026 年 2 月）在 Chrome DevTools Protocol 上重写了引擎，速度提升 44%。"
Context: 官方文档明确定位解决"传统选择器太脆 / 纯 agent 太不可预测"的两难："Too brittle: Traditional selectors break when websites change; Too agentic: AI agents are unpredictable and impossible to debug"。
Confidence: high

### 证据 5：Skyvern——视觉优先，表单填写最强，但成本高、约1/7任务失败

Claim: Skyvern 采用"规划器-执行器-验证器"三阶段视觉流水线，WebVoyager 2.0 得分 85.85%，是表单填写（WRITE）任务最强公开分数；但约每 7 个多步任务仍有 1 个失败，每步成本比 DOM 驱动高 4-8 倍。[^5^]
Source: 阿里云开发者社区 — 2026 年开源 Agent 工具包选型指南；Firecrawl Blog
URL: https://developer.aliyun.com/article/1740959 ; https://www.firecrawl.dev/blog/best-browser-agents
Date: 2026-06-11 / 2026-06-16
Excerpt: "Skyvern 在 WebVoyager 2.0 上得分 85.85%，这是在 DOM 不可靠的领域（canvas 元素、嵌套在 iframe 中的 React 虚拟 DOM、反机器人机制）中表单填写任务的最强已发布分数。换算成实际使用：大约七分之一的多步骤任务还是会失败。……每步成本高 4–8 倍。"
Context: 书中若写"AI看屏幕操作浏览器"，需同时交代成功率与成本代价，避免给读者"全自动无虞"的错觉。
Confidence: high

### 证据 6：Playwright MCP vs Chrome DevTools MCP 的边界

Claim: Playwright MCP 是跨浏览器上层封装，适合自动化与 E2E；chrome-devtools-mcp 是 Chromium 专属底层协议库，适合性能/网络调试；两者维护方分别为微软 Playwright 团队与 Chrome 官方团队。[^6^]
Source: 博客园 — Playwright MCP vs Chrome DevTools MCP vs Chrome MCP 深度对比；90%的人都用错了
URL: https://www.cnblogs.com/clnchanpin/p/19190994 ; https://www.cnblogs.com/jinjiangongzuoshi/p/19763612
Date: 2025-11-04 / 2026-03-24
Excerpt: "@playwright/mcp 封装更友好，是跨浏览器的上层封装库，无需关心底层调试端口 / 协议差异，适合自动化场景；chrome-devtools-mcp 是 Chromium 专属的底层 MCP 通信库，更贴近原生，适合 Chrome 专属调试场景。"
Context: 文件上传、拖拽、跨浏览器测试只有 Playwright MCP 完整支持；Chrome DevTools MCP 独占性能 trace 分析。
Confidence: high

### 证据 7：Computer Use / Operator 类的真实成功率（OSWorld）远低于浏览器专用框架

Claim: 截至 2026 年初 OSWorld 基准：人类约 75%，OpenAI Operator(CUA) 约 38%，字节 UI-TARS-72B 约 42%，Anthropic Computer Use(Claude Sonnet 4) 约 22%；简单任务成功率 90%+，复杂任务不足 10%。[^7^]
Source: AIGC Camp — 浏览器/电脑操作Agent
URL: https://aigccamp.com/vertical/browser-agent
Date: 2026-07-07
Excerpt: "|人类（baseline）|~75%| |Anthropic Computer Use（Claude Sonnet 4）|~22%| |OpenAI Operator (CUA)|~38%| |UI-TARS-72B（字节 2025）|~42%|" 以及 "简单任务（"在 Chrome 打开 URL"）成功率 90%+，复杂任务……成功率不到 10%。平均数掩盖了 distribution。"
Context: 失败模式集中：点击精度差、不知道何时等待、小元素识别、多窗口混淆；"Browser Use 不是模型，是 harness——处理截图压缩、坐标转换、错误重试、DOM+视觉双信号决策等工程问题"。
Confidence: medium（二手汇总，但与其他来源的相对排序一致）

### 证据 8：VS Code 内置浏览器 agent 工具默认隔离会话

Claim: VS Code 的浏览器 agent 工具（openBrowserPage/clickElement/runPlaywrightCode 等）默认在私有内存会话中运行，不与用户其他标签页共享 cookie 或存储；管理员可通过企业策略限制 agent 可访问的域名。[^8^]
Source: VS Code 官方文档 — Build and test web apps with browser agent tools
URL: https://code.visualstudio.com/docs/agents/guides/browser-agent-testing-guide
Date: 2026-06-01
Excerpt: "By default, pages opened by the agent run in private, in-memory sessions that don't share cookies or storage with your other browser tabs. This gives you control over what browsing data the agent can access."
Context: 说明"登录态"在 agent 浏览器里是显式工程决策而非默认行为——要让 agent 带登录态，必须主动注入（见第二节）。
Confidence: high

### 证据 9：带登录态场景的工具选型实测建议

Claim: 实测对比建议：需要带登录态（真实 Chrome Profile）或并行采集选 Browser-use；多步骤流程测试选 Playwright CLI（token 消耗比 MCP 低 4 倍以上）；仅看页面选 Agent Browser。[^9^]
Source: heyuan110.com — Claude Code 浏览器自动化怎么选？5套方案实测对比（2026）
URL: https://www.heyuan110.com/zh/posts/ai/2026-01-28-claude-code-browser-automation/
Date: 2026-01-28
Excerpt: "需要用真实 Chrome Profile（已登录的账号、已安装的扩展），或者要同时对多个网站执行任务？Browser-use 是唯一支持三种浏览器模式 + 云端并行的方案。" 以及 "2026 年的新推荐是 Playwright CLI——它拥有和 MCP 相同的 Playwright 底层能力，但 Token 消耗低 4 倍以上，长流程中不会撑爆上下文。"
Context: 开发者个人实测博客，可作为书中案例工具选型的直接参考。
Confidence: medium

---

## 二、登录态处理实战：会话持久化、2FA/验证码、反检测、凭据管理

### 证据 10：Playwright storageState 是登录态复用的标准机制

Claim: storageState 序列化"使浏览器处于已登录状态"的一切：所有域的 cookies 及各 origin 的 localStorage/sessionStorage；一次 UI 登录保存后即可在浏览器上下文与 API 请求上下文中复用。[^10^]
Source: qaskills.sh — Playwright APIRequestContext + storageState Guide 2026
URL: https://qaskills.sh/blog/playwright-apirequestcontext-storagestate-guide
Date: 2026-06-02
Excerpt: "`storageState` is Playwright's serialization of everything that makes a browser "logged in" without a server session lookup. Concretely it captures two things: all cookies for all domains the context has seen, and the `localStorage` and `sessionStorage` entries per origin."
Context: 同文强调 auth 文件须加 .gitignore："The `storageState` file and any saved token file contain live session credentials, so add `playwright/.auth/` to `.gitignore`."
Confidence: high

### 证据 11：storageState 加载后仍掉登录的常见根因（实战坑）

Claim: 加载 storageState 后仍被重定向到登录页的常见原因：session cookie 未持久化、Secure 属性要求 HTTPS、SameSite 限制、localStorage token 被动态清除、域名不一致（www 前缀）、RefreshToken 绑定设备指纹或 IP。[^11^]
Source: CSDN 问答 — Playwright如何通过保存和复用登录状态实现免登录
URL: https://ask.csdn.net/questions/9017889
Date: 2025-11-27
Excerpt: "若目标站点的 RefreshToken 绑定了客户端特征（如 User-Agent、IP 地址），则在不同运行环境加载 storageState 后，服务端会拒绝认证，强制登出。"
Context: 对应优化点：统一 userAgent/viewport/timezone、域名完全一致、固定 IP 或代理池、手动补 expires。这是案例二"客户给了密码但 agent 换个环境就掉登录"的核心解释。
Confidence: high

### 证据 12：Firebase Auth 等把 token 存 IndexedDB 时 storageState 默认存不下

Claim: storageState 默认只保存 Cookies 和 LocalStorage；若应用（如 Firebase Auth）把 token 存入 IndexedDB，需要 `indexedDB: true` 选项，且调用前必须等登录流程完全结束。[^12^]
Source: Runebook — 深度解析 Playwright storageState()
URL: https://runebook.dev/zh/docs/playwright/api/class-browsercontext/browser-context-storage-state
Date: 2025-12-04
Excerpt: "`storageState` 默认只保存 Cookies 和 LocalStorage。……如果你的应用使用 Firebase Auth 等将 token 存入 IndexedDB，你需要使用 `indexedDB: true` 选项。"
Context: 现代 SaaS（尤其 SPA）登录态分布多层的典型坑。
Confidence: high

### 证据 13：登录态管理三件套——检测→恢复→保活（RPA 实战）

Claim: 生产级登录态管理需在关键节点主动检测登录态（查找仅登录后出现的元素）、失效后自动重登录（预留人工介入等待或告警）、长任务定时保活（刷新页面防闲置踢出）。[^13^]
Source: 火山引擎开发者社区 — 影刀RPA进阶教程：浏览器环境配置与Cookie管理
URL: https://developer.volcengine.com/articles/7657448679628472347
Date: 2026-07-01
Excerpt: "Cookie过期后再次登录，可能触发短信验证码或滑块验证。这种情况很难完全自动化，建议：在流程中预留"人工介入"的等待时间；或通过企业微信/飞书发送告警通知。"
Context: 检测时机：流程开始前必须检测、敏感操作前检测；保活：部分平台闲置30分钟自动踢出。
Confidence: high

### 证据 14：Browser Use 的凭据管理机制——LLM 只见占位符，永远不见真密码

Claim: Browser Use 的 sensitive_data 机制让 LLM 只看到占位符（x_user/x_pass），真实值在 LLM 调用后直接注入表单；并支持按域名正则限定凭据作用域；建议 use_vision=False 防止截图泄露敏感信息，能用 storage_state 就不用密码。[^14^]
Source: Browser Use 官方文档 — Sensitive Data
URL: https://docs.browser-use.com/open-source/examples/templates/sensitive-data
Date: 2026-03-09
Excerpt: "Text Filtering: The LLM only sees placeholders (`x_user`, `x_pass`), we filter your sensitive data from the input text. DOM Actions: Real values are injected directly into form fields after the LLM call" 以及最佳实践 "Use `Browser(allowed_domains=[...])` to restrict navigation; Set `use_vision=False` to prevent screenshot leaks; Use `storage_state='./auth.json'` for login cookies instead of passwords when possible"
Context: 这是案例二"客户给用户名密码"时凭据安全的标准做法，应写进章节。
Confidence: high

### 证据 15：2FA 的工程化处理——TOTP 可自动化，其余靠人工接管

Claim: 各平台 2FA 处理现状：TOTP 若有 secret key 可程序生成（Browser Use 用 `x_bu_2fa_code` 占位符自动生成；Steel/Kernel 托管自动注入）；无法自动化的 2FA 方式，各平台均支持 human-in-the-loop 人工接管。[^15^]
Source: Browser Use 官方博客 — How to Authenticate AI Web Agents
URL: https://browser-use.com/posts/web-agent-authentication
Date: 2026-03-26
Excerpt: "If you have the secret key, you can generate these codes programmatically without having to use an authenticator app. …… All platforms also support human-in-the-loop verification for 2FA methods they can't automate."
Context: "The agent never sees your actual credentials, only placeholder names." TOTP secret 获取途径：2FA 设置页的"manual entry / can't scan QR code"。
Confidence: high

### 证据 16：Browserbase Live View——人工接管单个步骤的生产范式（Ramp 案例）

Claim: Browserbase Live View 是可嵌入自己应用的实时浏览器 iframe：agent 卡住时把 live URL 交给用户，人完成一个步骤（2FA、CAPTCHA、最终确认）后 agent 接着跑；Ramp 的采购 agent 正是基于该模式上线。[^16^]
Source: Browserbase 官方博客 — What is a Browserbase Browser?
URL: https://www.browserbase.com/blog/what-is-a-browserbase-browser
Date: 2026-06-16
Excerpt: "You can embed it in your own app, hand it to a user when an agent gets stuck, and let a human take over a single step (a 2FA prompt, a CAPTCHA, a final confirmation) without the agent losing its place. Ramp shipped their procurement agent on top of this exact pattern: when the agent hits a wall, it hands the live URL to the user, the user clicks one button, the agent picks back up."
Context: 同文：Session Recordings/Replays 保存完整会话回放（网络日志、console、CDP 事件），构成操作审计基础。Browserbase 另有 Contexts API 持久化 cookie/浏览器状态跨会话复用。
Confidence: high

### 证据 17：OpenAI Operator 的"接管模式"（takeover mode）

Claim: OpenAI Operator 推出"接管模式"（takeover mode），要求用户手动输入支付详情或登录信息；执行高风险任务（如发邮件）前要求用户确认。[^17^]
Source: 百度百科 — Operator（OpenAI推出的全新AI助理产品）
URL: https://baike.baidu.com/item/Operator/65108419
Date: 2025-11-26
Excerpt: "为应对这些风险，Operator推出一项名为"接管模式"（takeover mode）的功能，要求用户手动输入支付详情或登录信息。此外，Operator在执行高风险任务（如发送邮件）之前……"
Context: 国产开源同类设计：智谱 Open-AutoGLM 的动作用表中也有 `Take_over`："请求人工接管(登录/验证码等)"（GitHub zai-org/Open-AutoGLM）。
Confidence: medium（百科为二手，但与 OpenAI 官方表述一致）

### 证据 18：2026 年绕过 Cloudflare 的现实——IP 信誉是第一道闸，单一 stealth 插件已失效

Claim: 2026 年 Cloudflare 采用多信号分析：IP 信誉（数据中心 ASN 直接拉满风险分）先于浏览器指纹被检查；ML bot 评分模型 v9（2026 Q1 全量）提高了 TLS 指纹(JA4)、HTTP/2 帧顺序、行为遥测权重；仅靠 stealth 插件必然失败。[^18^]
Source: Human Browser Blog — Playwright 绕过 Cloudflare 2026：实测12种方法(仅3种仍然有效)
URL: https://humanbrowser.cloud/zh-CN/blog/bypass-cloudflare-playwright-2026
Date: 2026-05-27
Excerpt: "你的 IP 地址是 Cloudflare 检查的第一件事。在你的浏览器指纹被评估之前，Cloudflare 就已经知道你的 IP 属于数据中心、VPN 提供商，还是真实的家庭网络。" 以及 "给 Playwright 加 stealth 插件就能绕过 Cloudflare。在 2026 年，仅靠 stealth 插件会失败，因为 Cloudflare 的 IP 信誉数据库会立即标记所有主流云服务商(AWS、DigitalOcean、Hetzner、OVH)"
Context: 对书中案例的含义：在客户办公室/住宅网络本机跑 agent（带真实 Chrome profile）比云端数据中心浏览器更不易触发风控；这也是"用客户自己的登录态"的另一论据。
Confidence: medium（厂商博客有营销倾向，但技术细节与其他来源互证）

### 证据 19：行为指纹是 2025-2026 反爬核心——默认 Playwright 滚动 90% 被拦

Claim: Cloudflare v2 记录操作时序、鼠标轨迹（直线匀速=机器特征）、交互模式；实测默认 `page.mouse.wheel(0,1000)` 10 次请求 9 次被拦，改成人类化滚动轨迹后拦截率降到 15%；设备指纹（Canvas/WebGL/AudioContext/字体）为基础校验。[^19^]
Source: CSDN — 2025反爬终极方案：Python破解Cloudflare v2行为指纹
URL: https://blog.csdn.net/shanwei_spider/article/details/154212176
Date: 2025-10-31
Excerpt: "举个实测现象：用Playwright默认滚动（page.mouse.wheel(0, 1000)），10次请求9次被拦截；改成模拟人类"先慢后快再慢"的滚动轨迹，拦截率直接降到15%——行为指纹是2025年破解Cloudflare v2的核心突破口。"
Context: 规避检测同时意味着法律风险上升（见第五节："避开或破坏技术管理措施"是新反法明令的不正当手段）——书中应把"反检测技巧"与"合规红线"对照写。
Confidence: medium

### 证据 20：浏览器指纹采集维度与自动化工具的伪造入口

Claim: 主流风控采集 Canvas 渲染、WebGL 参数、AudioContext、字体枚举、UA、时区等生成设备唯一标识；Puppeteer/Playwright 常用手段是 `--disable-blink-features=AutomationControlled` + 注入脚本隐藏 `navigator.webdriver`。[^20^]
Source: CSDN — 浏览器指纹识别防御与破解（2025年反爬核心技术曝光）
URL: https://blog.csdn.net/FuncInk/article/details/152653974
Date: 2025-10-07
Excerpt: "通过采集用户设备的Canvas渲染、WebGL参数、字体列表、屏幕分辨率、时区、User-Agent及插件信息等特征，服务端可唯一标识一个"浏览器实例"，即使使用代理或无痕模式也难以绕过。"
Context: 教学价值：向读者解释"为什么 agent 用的浏览器和客户自己 Chrome 是两种'身份'"。
Confidence: medium

### 证据 21：Browserbase 规模与合规认证（企业级登录态托管的参照）

Claim: Browserbase 2025 年处理 5000 万会话、1000+ 客户，2025 年 6 月完成 4000 万美元 B 轮（估值 3 亿美元）；具 SOC-2 Type 1 与 HIPAA 合规；stealth 模式含托管 CAPTCHA 解决、住宅代理、指纹生成。[^21^]
Source: Skywork — Browserbase: O Guia Definitivo para Automação Web com IA em 2025；Firecrawl Blog
URL: https://skywork.ai/skypage/pt/browserbase-web-automation-ai/1986246200597741568 ; https://www.firecrawl.dev/blog/best-browser-agents
Date: 2025-11-06 / 2026-06-16
Excerpt: "Em apenas 16 meses, a empresa escalou rapidamente, servindo mais de 50 milhões de sessões de navegador em 2025 e levantando uma rodada Série B de $40 milhões em junho de 2025, avaliando a empresa em $300 milhões." 以及 "Modo Stealth: Gerencia automaticamente a resolução de CAPTCHAs, utiliza proxies residenciais e gera impressões digitais de navegador (fingerprinting) para evitar detecção por sistemas anti-bot."
Context: 企业客户案例：Convergence 用 Live View 让用户在登录/2FA 时接管会话，扩到 20 万用户后被 Salesforce 收购。
Confidence: medium

---

## 三、"看懂一个 SaaS 再复制它"的工作流

### 证据 22：截图/录屏→代码已成熟：screenshot-to-code 支持屏幕录像转功能原型

Claim: 开源项目 screenshot-to-code（GitHub abi/screenshot-to-code）可将截图、设计稿甚至网站操作录屏转换为 HTML/Tailwind/React/Vue 代码及可交互原型。[^22^]
Source: GitHub — abi/screenshot-to-code
URL: https://github.com/abi/screenshot-to-code
Date: 2023-11-14 创建（持续更新至 2026）
Excerpt: "Convert screenshots, mockups, Figma designs, and screen recordings into clean, functional code using AI." 以及 "Screenshot to Code also supports taking a screen recording of a website in action and turning that into a functional prototype."
Context: "录屏→原型"是"复刻 SaaS 交互流程"最直接的开源工具链；商业同类有 same.new、v0.dev、copyweb.ai。
Confidence: high

### 证据 23：AI 复刻网站的通用流水线——"识别→理解→生成"

Claim: 像素级复刻工具（same.new / v0.dev / copyweb.ai）共同遵循"识别→理解→生成"流程：计算机视觉看懂布局、结构化算法理清逻辑、LLM 输出组件化代码，并支持自然语言迭代修正。[^23^]
Source: 人人都是产品经理 — 这3个工具10分钟「像素级复制」一个网站
URL: https://www.woshipm.com/share/6231396.html
Date: 2025-06-17
Excerpt: "AI 复刻网站的核心是一个 "识别 -> 理解 -> 生成" 的过程。它利用计算机视觉技术"看懂"设计，利用结构化算法"理清"逻辑，最后利用大型语言模型"写出"代码……优秀的 AI 工具会生成组件化的代码……像 v0 这样比较高级的工具，还允许用户通过自然语言指令对生成的代码进行实时修改。"
Context: 书中可借此向读者解释复刻工具的能力边界：视觉层可 1:1，业务逻辑层必须另行推断。
Confidence: medium

### 证据 24：复杂 SaaS 复刻的工程决策树——先抓 API fixtures 再做 mock 替身

Claim: 开源 web-clone skill 的决策树：静态站直接镜像；SPA/SaaS/数据驱动页面必须先跑 network-capture 保存 API fixtures、搭本地 mock server 替身；多页站先做 route-crawl 路由地图；复杂交互站先跑 interaction-probe 记录 hover/click/scroll 状态，"不许只截首屏"。[^24^]
Source: GitHub — nexu-io/open-design/skills/web-clone/SKILL.md
URL: https://github.com/nexu-io/open-design/blob/main/skills/web-clone/SKILL.md
Date: 2026-04-28
Excerpt: "SPA / SaaS / 数据驱动页面 | 先跑 `network-capture.mjs` 保存 API fixtures → 本地 JSON/mock server 替身" 以及 "复杂交互站 | 先跑 `interaction-probe.mjs` 记录 hover/click/scroll/canvas drag 状态 → 按状态补交互，不许只截首屏"
Context: 这是"登录态下功能遍历与流程录制"最贴近一手工程实践的公开证据：先侦察（recon）→ 按类型选路径 → 抓网络层真相，而非只看像素。API fixtures 同时是逆向推测数据库 schema 的原料（请求/响应字段即实体与关系线索）。
Confidence: high

### 证据 25：AI 生成 PRD 的典型缺陷——异常状态、阈值、防打扰策略全靠人补

Claim: 实测对比显示 AI 直接生成的 PRD 常遗漏异常状态模块、阈值判断、防打扰策略与接口依赖约束，需要人工 PM 修正为可评审的严谨文档。[^25^]
Source: gankinterview.cn — 给AI当PM的一天：如何撰写极度严谨的PRD
URL: https://www.gankinterview.cn/zh-CN/blog/a-day-as-a-pm-for-ai-how-to-write-an-extremely-rigorous-prd-product-requirements
Date: 2026-03-17
Excerpt: "|异常状态|（AI 完全遗漏此模块，默认所有降价商品均可正常购买）|防御性逻辑：若商品触发降价，但当前状态为"已下架"或"库存为 0"，则强制拦截通知……|"
Context: 对案例二的直接启示："遍历 SaaS → AI 生成功能清单/PRD"这一步产出的只是草稿；阈值、边界、异常流必须人工检查点确认（呼应第四节的 HITL 设计）。
Confidence: medium

### 证据 26：一张截图复刻网站 + 对话式迭代的消费级产品实践

Claim: 扣子空间（字节）实测：输入一张截图即生成视觉 1:1 的网页雏形，支持预览页上点选元素对话式迭代，可下载完整 HTML/CSS/JS 代码包。[^26^]
Source: 微信公众号 — 我用一张截图"喂"给AI，它1:1复刻了一个网站
URL: http://mp.weixin.qq.com/s?__biz=MzI4NTM1NDgwNw==&mid=2247551812&idx=1&sn=8ae27bac4731577f2df23cee50b4a51d
Date: 2025-07-24
Excerpt: "AI Agent 开始"阅读"这张图片，自动识别出页面布局（页头、内容区、页脚）、色彩搭配、字体大小、图片位置和按钮样式。然后，它直接搭建了一个开发环境……几分钟后，一个在视觉上与我的设计稿几乎完全一致的网页雏形，就出现在了预览窗口中。"
Context: 与证据 23 互证：视觉复刻已产品化；差异竞争在功能逻辑与数据层。
Confidence: medium

---

## 四、复杂任务的管理与控制：拆解、检查点、错误恢复、审计

### 证据 27：HITL 是 agent 工作流的一等机制（LangGraph interrupt/checkpoint/Command）

Claim: LangGraph 以 Interrupt（挂起并返回待审数据）、Command Resume（按人工决策恢复/跳转）、Checkpoint（状态持久化）三机制实现人机回环；典型场景是敏感操作审批、内容审核、不可逆操作确认。[^27^]
Source: CSDN — 企业级Agent系统的关键挑战与LangGraph解法；博客园 LangGraph 人机环路指南
URL: https://modelengine.csdn.net/690c50845511483559e2ae40.html ; https://blog.mapin.net/posts/LangGraph%20%E4%BA%BA%E6%9C%BA%E7%8E%AF%E8%B7%AF%20interrupt
Date: 2025-07-30 / 2025-10-03
Excerpt: "实现带有人类参与的Agent系统的关键在哪里？或许你可以想象到：流程中断与恢复，以及为了支持它所需要的状态持久化机制。……LangGraph给出的解决方案是Interrupt（中断）、Command Resume（命令恢复）、Checkpoint（检查点）三大机制。"
Context: 代码模式：`graph = builder.compile(checkpointer=memory, interrupt_before=["review_node"])`，人工 `update_state` 后 `invoke(None, config)` 续跑。
Confidence: high

### 证据 28：长任务恢复方法论——"先验尸，再续命"

Claim: 长任务中断恢复的正确顺序：停止重跑→保存现场（diff/日志/任务清单）→判断中断层（计划/搜索/编辑/测试/发布）→让 agent 先生成恢复摘要→把下一步缩小为小闭环→尽快写新 checkpoint。[^28^]
Source: KnightLi 的博客 — AI Agent 长任务中断后怎么恢复
URL: https://knightli.com/2026/07/10/ai-agent-long-task-resume-guide/
Date: 2026-07-10
Excerpt: "长任务恢复不是"接着跑"，而是"先验尸，再续命"。" 以及 "长任务中断后，先做状态复盘，不要直接继续执行。恢复时必须列出已改文件、已运行验证、当前阻塞和最小下一步。任何删除、发布、迁移、外部写入、付费调用都需要用户确认。"
Context: 恢复摘要模板字段：原始目标/当前状态/已完成/未完成/已改文件/已运行验证/失败阻塞/不应重复执行/最小下一步——可直接改造为书中浏览器 agent 任务的检查点清单。
Confidence: high

### 证据 29：Durable Execution 与 unknown 状态——最危险的不是失败而是"不知道执行没执行"

Claim: 外部副作用步骤必须用幂等键；超时导致结果 unknown 时自动重试可能重复执行（重复扣款/重复发信），稳妥策略是暂停并交人工或补偿系统；小时级以上长任务应考虑 Temporal 类 durable execution 的事件历史模型，LangGraph checkpointer 只解决对话连续性、不知道"邮件已发过"。[^29^]
Source: 掘金 — AI Agent 不是会重试就可靠：长任务的断点恢复与 Durable Execution 设计
URL: https://juejin.cn/post/7660053470331617330
Date: 2026-07-09
Excerpt: "最危险的状态不是成功，也不是失败，而是 unknown：请求发出去了；本地超时了；不知道上游到底执行没有……遇到 unknown，如果你自动重试，就可能重复执行；如果你直接标失败，又可能让业务方以为没执行。更稳妥的策略是暂停，暴露给人工或补偿系统处理。"
Context: 对"登录 SaaS 替客户操作数据"场景极其关键：在客户系统里的写操作（建单、发消息、改配置）必须幂等+可审计+unknown 时挂起。
Confidence: high

### 证据 30：长任务工作流的审计与状态机建模

Claim: 可恢复长任务应建模为持久化状态机：每阶段保存输入哈希、版本、状态、Checkpoint、产物引用和错误分类；恢复时从最后已提交且可验证的检查点继续；所有副作用用幂等键/唯一约束/事务消息；并支持取消、心跳租约、补偿、人工介入、进度查询。[^30^]
Source: AI Knowledge — 如何设计支持断点恢复的长任务工作流？
URL: https://www.cs2price.online/12-blog/06-系统设计与项目复盘/03-如何设计支持断点恢复的长任务工作流
Date: 2026-07-16
Excerpt: "长任务可恢复的本质是持久化状态、可验证检查点和幂等副作用。……用崩溃、重复消息与延迟回调注入验证恢复语义。"
Context: "用消息队列就能恢复"被列为典型误区：队列只传任务，不自动保存业务状态与检查点。
Confidence: medium

### 证据 31：ChatGPT Agent 的确认机制与 prompt injection 防御指标

Claim: ChatGPT Agent（2025年7月 system card）设有用户确认系统：敏感操作需显式批准，确认召回率总体 91.0%，编辑权限/通信/金融交易等关键类别达 99.9-100%；watch mode 在用户不活跃时自动暂停敏感操作；抗注入率：网页文本注入 99.5%、视觉注入 95%，但上下文数据外泄抵抗仅 78%、主动外泄防御 67%。[^31^]
Source: Libertify — ChatGPT Agent System Card — OpenAI Safety Analysis July 2025
URL: https://www.libertify.com/interactive-library/chatgpt-agent-system-card-openai-safety-analysis/
Date: 2026-03-19（分析2025-07官方 system card）
Excerpt: "The confirmation recall rate stands at 91.0% overall, but reaches **99.9-100%** for critical categories including editing permissions, communications, and financial transactions." 以及 "In-context data exfiltration resistance stands at 78%, while active data exfiltration defense reaches 67%."
Context: 给读者的定量认知：即使头部厂商，数据外泄防御也只有六七成——登录态 agent 浏览不可信网页是高危动作，需配合 allowed_domains 等限制（证据 14）。
Confidence: high

### 证据 32：Anthropic Computer Use 的官方风险提示与防御框架

Claim: Anthropic 官方对 computer use 的风险框架：prompt injection（恶意网页隐藏文字诱导删除本地文件）、误操作（点错"发送全员"）；防御为受信任沙箱隔离（Docker/VM）、敏感操作 HITL 拦截、注意截图含 PII 的隐私风险。[^32^]
Source: yeasy.gitbook.io Claude 指南 — Computer Use 能力概述（整理自 Anthropic 官方文档）；江苏省计算机学会通讯（引述 Anthropic 信任与安全团队分析）
URL: https://yeasy.gitbook.io/claude_guide/di-er-bu-fen-gong-ju-pian/05_computer_use/5.1_overview
Date: 2026-04-18
Excerpt: "Prompt Injection: 如果 Claude 访问了一个恶意网页，网页上的隐藏文字可能会诱导它删除本地文件。……受信任沙箱隔离：官方参考实现建议运行在受信任的隔离环境中……人机回环 (HITL)：对于敏感操作，建议设置拦截机制，需人工批准才能执行。"
Context: 书中案例二涉及"拿客户凭据登录真实 SaaS"，沙箱隔离+域名白名单+敏感操作确认是必备三段式。
Confidence: medium

### 证据 33：操作审计的基础设施已商品化

Claim: Browserbase 提供 Session Recordings（仪表盘回放）、Session Replays（mp4 流式回放，含网络日志、console 日志、CDP 事件）与全量结构化日志；Kernel 等平台亦支持会话复用（保留 cookie/认证/浏览历史跨会话）。[^33^]
Source: Browserbase 官方博客；Kernel Blog — The Best AI Web Browsing Agents in 2025
URL: https://www.browserbase.com/blog/what-is-a-browserbase-browser ; https://www.kernel.sh/blog/the-best-ai-web-browsing-agents
Date: 2026-06-16 / 2025-11-24
Excerpt: "Session Recordings are saved in the dashboard to help debug and Session Replays lets you stream mp4s of the full session replay in your app. A scrubable, inspectable replay with network logs, console logs, and CDP events captured automatically. Structured logs for everything: network, console, CDP, lifecycle."
Context: 审计日志（谁在什么时候以谁的账号做了什么）是"客户把密码交给你"之后信任链的技术底座，也是出纠纷时的证据链。
Confidence: high

---

## 五、法律与合规边界

### 证据 34：中国新《反不正当竞争法》（2025-10 施行）数据保护专款

Claim: 2025年修订《反不正当竞争法》第13条第3款首次设数据保护专款：经营者不得以欺诈、胁迫、避开或者破坏技术管理措施等不正当方式获取、使用其他经营者合法持有的数据；"获取"具有独立可责性；判例认定的技术管理措施包括用户协议/法律声明、用户名密码验证、动态验证码、签名校验、Robots协议、频率限制、IP封禁、UA识别。[^34^]
Source: 知产财经 — "反不正当竞争法"视角下人工智能大模型"爬取数据"行为的正当性判断；新华社
URL: https://www.ipeconomy.cn/yuanchuang/10925.html ; http://www.news.cn/tech/20250815/d4efc50d99b4422fb77a4c00ccf932df/c.html
Date: 2026-06-10 / 2025-08-15
Excerpt: "在先判例中认定的技术管理措施主要包括平台公示的《用户协议》《平台管理规则》《法律声明》、数据访问限制措施（如用户名及密码验证、动态验证码、签名校验等）、防爬取措施（如Robots协议、请求频率限制、IP封禁、User-Agent识别和拦截）等" 以及 "不正当获取数据行为不再附加后续使用行为，具有独立的可责性。"
Context: 关键含义：客户给你密码登录是"授权访问"本身不违法，但绕过验证码/伪造指纹/越权抓取超出账号权限的数据，即落入"避开或破坏技术管理措施"。
Confidence: high

### 证据 35：最高法指导性案例262号——"实质性替代"标准

Claim: 最高法 2025 年 8 月数据权益指导性案例（262号，"搬家软件"案）确立：未经许可获取并向公众提供平台数据、实质性替代原平台产品或服务的，构成不正当竞争。[^35^]
Source: 最高人民法院知识产权法庭 — 2025年人民法院反不正当竞争典型案例；环球律师事务所评析
URL: https://ipc.court.gov.cn/zh-cn/news/view-4601.html ; https://www.glo.com.cn/Content/2025/10-24/1107527632.html
Date: 2025-09-09 / 2025-10-23
Excerpt: "对于未经许可获取并向公众提供相关数据，实质性替代网络平台产品或者服务，扰乱市场竞争秩序、损害网络平台经营者或者其他权利人合法权益的行为，人民法院可以适用《中华人民共和国反不正当竞争法》有关规定，认定构成不正当竞争行为。"
Context: "复刻 SaaS 功能"若只是自用/内部工具，与"复制后向公众提供并替代原产品"法律性质完全不同——书中应强调这条分界线。
Confidence: high

### 证据 36：2025-2026 中国爬虫合规口径（最高检/国家数据局/行政法规）

Claim: 最新官方口径：最高检（2025-11）采用"代码技术障碍"标准（是否突破加密、鉴权、访问控制）；《网络数据安全管理条例》第18条（2025-01 施行）要求自动化收集不得非法侵入、不得干扰服务正常运行；"自己账号正常登录不算侵入"不完全成立——登录后越权访问他人数据仍可构成非法获取计算机信息系统数据罪（刑法285条）。[^36^]
Source: CSDN — 合法爬虫四底线 法律边界（2026年最新口径：国家数据局+最高检）
URL: https://blog.csdn.net/zhangfeng1133/article/details/160744626
Date: 2026-05-03
Excerpt: "如果你用账号登录后，通过爬虫 **突破该账号原本无权访问的数据范围**（例如爬取后台隐藏接口、越权访问他人数据），仍然属于「未经许可进入计算机信息系统」，可构成刑法第 285 条「非法获取计算机信息系统数据罪」。"
Context: 案例二中"客户授权你登录"≠"你可以用脚本访问该账号界面上看不到的接口"。
Confidence: medium（作者为个人博主，但引用的法规条文与一手解读可交叉验证）

### 证据 37：美国判例主线——hiQ 赢了 CFAA，输在合同

Claim: hiQ v. LinkedIn：第九巡回（2022）认定抓取公开页面不构成 CFAA"未经授权访问"；但 hiQ 因注册账号接受用户协议（含禁止抓取条款）且使用假账号登录测试，被判违约，2022年12月和解：永久禁令+50万美元+删除数据与算法。[^37^]
Source: Thunderbit — 抓取 LinkedIn 违法吗；北京市兰台律师事务所 — AI企业"爬虫行为"法律风险全景分析
URL: https://thunderbit.com/zh-Hans/blog/is-scraping-linkedin-legal ; https://www.lantai.cn/news_view.aspx?nid=2&typeid=5&id=1667
Date: 2026-07-14 / 2026-06-15
Excerpt: "hiQ 的确降低了在第九巡回辖区内，对真正公开、无需登录的数据进行抓取时的 CFAA 风险。但它并没有给任何人一项可以随意抓取 LinkedIn 的通用权利。合同索赔仍然成立，假账号访问也受到了处罚。"
Context: "登录态抓取"与"公开抓取"法律地位截然不同——这正是本维度（登录态自动化）的核心风险所在。
Confidence: high

### 证据 38：Meta v. Bright Data（2024）——登录/未登录的分水岭

Claim: 加州北区联邦法院（2024-01）：登出状态下抓取公开 Facebook/Instagram 数据不构成违约，因为平台条款约束账户持有人而非未登录访客；由此形成的规则——未登录公开抓取有可辩护性，已接受条款的登录抓取没有。[^38^]
Source: DataImpulse — 网页抓取合法吗？法律、案例与合规（2026指南）；Thunderbit
URL: https://dataimpulse.com/zh-cn/blog/is-web-scraping-legal/
Date: 2026-06-28
Excerpt: "由此形成的规则是——未登录的公开抓取具有可辩护性；在已接受条款的情况下进行登录抓取则不具备可辩护性。"
Context: 违反 ToS 属民事违约而非犯罪，但可成为封号、民事诉讼与恶意证据；自动化行业实务推论：绝不登录买家/卖家账号抓取（证据亦见 Pangolinfo 指南）。
Confidence: high

### 证据 39：账号共享/出借条款是标准配置——客户"给密码"本身就可能是违约链条的一环

Claim: 主流服务协议普遍禁止账号出借/转让/共享：微信 7.1.2（账号所有权归腾讯，使用权仅限初始注册人，不得赠与、借用、租用、转让）；阿里云 2.3.3；Microsoft 服务协议（不得转让账户凭据，禁止反向工程）；华为账号"仅供个人使用"。[^39^]
Source: 微信软件许可及服务协议（官方）；阿里云用户协议（官方）；Microsoft 服务协议（官方）
URL: https://weixin.qq.com/agreement?lang=zh_CN ; https://terms.aliyun.com/legal-agreement/terms/suit_bu1_ali_cloud/suit_bu1_ali_cloud201712130944_39600.html ; https://www.microsoft.com/zh-cn/servicesagreement
Date: 2025-07-30（Microsoft）/ 2025-05-26（阿里云）
Excerpt: "微信账号的所有权归腾讯所有，用户完成申请注册手续后，仅获得微信账号的使用权，且该使用权仅属于初始申请注册人。同时，初始申请注册人不得赠与、借用、租用、转让或售卖微信账号或以其他方式许可非初始申请注册人使用微信账号。"
Context: 案例二的合同前提是"客户给一个用户名密码"——书中必须提示：若该 SaaS 协议禁止共享账号，此商业模式本身踩线；更稳妥的做法是客户为本项目开设子账号/服务账号或使用官方 API/OAuth 授权。
Confidence: high

### 证据 40：账号出借的司法后果实例

Claim: 2026 年报道案例：被告使用他人微信账号被认定违反《腾讯微信软件许可及服务协议》7.1.2 与 8.3.1（冒用身份），平台可限制功能或封号；账号出借人知情同意可能承担连带责任。[^40^]
Source: 新浪新闻
URL: https://www.sina.cn/news/detail/5287324598672095.html
Date: 2026-04-13
Excerpt: "被告使用他人微信账号，违反《腾讯微信软件许可及服务协议》第7.1.2条（账号归属与使用权限制）及第8.3.1条（冒充/冒用身份）……账号出借人知情同意可能承担连带责任；不知情且及时止损可减轻责任。"
Context: "客户把密码给你"在账号类服务里不仅是客户违约，受托方（你）也可能被视为冒用身份。
Confidence: medium

### 证据 41：微博诉脉脉"三重授权"规则与个人信息保护

Claim: 中国司法实践（微博诉脉脉案）确立"三重授权"规则：获取平台数据需同时获得平台授权与用户授权；即使信息公开可见，爬取时过度收集个人信息仍可能侵害个人信息权益（《个人信息保护法》：处理已公开个人信息对个人权益有重大影响的应取得个人同意）。[^41^]
Source: 汉斯出版社 — 网络爬取的数据风险及其法律规制研究
URL: https://pdf.hanspub.org/ds_1081848.pdf
Date: 未注明（学术论文，2023 后）
Excerpt: "在微博诉脉脉案中，法院提出"三重授权"规则，要求数据获取方需获得平台和用户授权……个人信息处理者处理已公开的个人信息，对个人权益有重大影响的，应当依照本法规定取得个人同意。"
Context: 若"复刻"过程把原 SaaS 中的用户数据一并搬走，触发的不只是 ToS 问题，还有个人信息保护责任。
Confidence: medium

### 证据 42：新战线——Reddit v. Perplexity 用 DMCA §1201 规制"绕道抓取"

Claim: 2025年10月 Reddit 起诉 Perplexity、SerpApi 等，主打 DMCA §1201（规避技术保护措施）而非版权侵权：被告经 Google 搜索结果间接获取 Reddit 内容，被认定为绕过 Google SearchGuard 技术保护；Reddit 设"蜜罐帖子"取证；截至2026年2月审理中。[^42^]
Source: Zenn — Webスクレイピングは2026年も合法か？
URL: https://zenn.dev/datajournal1/articles/b4dd584b7a2e36
Date: 2026-03-03
Excerpt: "注目すべきは**著作権侵害ではなくDMCA Section 1201（技術的保護措置の回避）**を主な根拠にしている点です。"
Context: 平台方的法律武器正在从"合同违约"扩展到"技术保护措施规避"——与中国新反法"避开或者破坏技术管理措施"条款同向演进。
Confidence: medium

### 证据 43：平台自动化访问条款本身即构成"技术管理措施/合同义务"

Claim: 用户协议中明确禁止自动化爬取的条款在司法实践中逐渐被视为有法律约束力的合同义务；中国目前基于违约诉讼的不多（因平台条款不严谨），但反不正当竞争与著作权路径已成熟。[^43^]
Source: 北京市兰台律师事务所 — AI企业"爬虫行为"法律风险全景分析
URL: https://www.lantai.cn/news_view.aspx?nid=2&typeid=5&id=1667
Date: 2026-06-15
Excerpt: "用户协议或服务条款中明确禁止的自动化爬取行为，在司法实践中逐渐被视为具有法律约束力的合同义务。爬虫采集行为若违反用户协议，企业可能需承担合同违约责任。"
Context: 综合证据 37-39：给读者的合规矩阵 = 是否登录（合同约束）× 是否绕过技术措施（反法/刑法）× 数据类型（个人信息/版权）× 用途（自用/实质性替代）。
Confidence: high

---

## 写给作者的 3-5 个要点（服务案例章节写作）

1. **工具选型讲"80/20 混合架构"，不要讲"全自动"**：2026 年生产共识是把确定性的 80% 流程固化成 Playwright 脚本（登录态用 storageState/Contexts 持久化复用），只把需要推理的 20% 交给 Browser Use/Stagehand；视觉系（Skyvern/CUA）留作 canvas、反爬场景的备选。这直接对应案例二"复制一个 SaaS"里"遍历探索用 AI、固化流程用代码"的两阶段结构（证据 3、10、16、24）。

2. **登录态是案例二的第一个"管理与控制"教学点**：凭据不落 LLM（sensitive_data 占位符 + use_vision=False + allowed_domains 白名单）、会话文件当密钥管理（.gitignore、按域名隔离）、TOTP 可自动化但短信/滑块必须设计人工接管节点（Live View/Take_over 模式）、登录态要有"检测→恢复→保活"闭环。换 IP/换环境掉登录不是 bug，是 RefreshToken 绑定设备特征的风控行为（证据 11、13-17）。

3. **"看懂再复制"的可靠工作流是网络层优先，而非像素优先**：截图复刻工具只能交付视觉层；复刻 SaaS 功能的关键动作是登录后跑 network-capture 抓 API fixtures（顺带成为逆向推测数据模型的原料）、route-crawl 建路由地图、interaction-probe 记录交互状态，然后让 AI 基于 fixtures 生成功能清单/PRD 草稿——但阈值、异常流、权限规则必须人工检查点确认，AI 初稿必然遗漏（证据 22-26）。

4. **长任务章节可直接套用的工程模式**：检查点 + 幂等副作用 + unknown 挂起人工处理 + 全量会话回放审计。特别强调：在客户系统里的任何"写操作"（建单、发信、改配置）都是不可逆副作用，"重试就可靠"是错觉；操作审计（session replay/结构化日志）既是调试工具也是出纠纷时的证据链（证据 27-33）。

5. **法律边界必须写成案例的"前置讨论"而非脚注**：①客户给密码本身可能违反目标 SaaS 的账号独享条款，受托方可能被认定为冒用身份——更稳的结构是让客户开子账号/服务账号或走官方 OAuth/API；②登录后绕过验证码/伪造指纹/越权抓隐藏接口，在中国落入新反法"避开或破坏技术管理措施"条款，甚至刑法 285 条；③"复刻自用"与"向公众提供并实质性替代原产品"是不正当竞争认定（指导性案例262号）的分水岭；④美国判例（hiQ、Meta v. Bright Data）同样显示：登录态下违约风险远高于未登录公开抓取（证据 34-43）。

---

### 调研说明
- 共执行 35 次独立搜索（中文为主，混用英/日/葡语结果）。
- 一手来源包括：GitHub（abi/screenshot-to-code、nexu-io/open-design、zai-org/Open-AutoGLM）、官方文档（docs.browser-use.com、docs.stagehand.dev、browserbase.com、code.visualstudio.com、weixin.qq.com、microsoft.com、terms.aliyun.com、ipc.court.gov.cn、news.cn）、官方法规文本解读（君合、环球、兰台律所）。
- 未竟事项：①Skyvern GitHub 一手 README 未直接打开（以二手选型文交叉验证）；②Netflix/Spotify 账号共享执法案例未检到合适中文来源，以微信/阿里云/微软协议条款替代论证；③"数据库 schema 逆向推测"未找到专门复盘长文，最接近的一手证据是 web-clone skill 的 network-capture→fixtures 路径（证据 24）。
