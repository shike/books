#!/usr/bin/env python3
"""
books/scripts/gen_promotion.py

根据 ai-coding 的 promotion 标准件模板,生成 fde 和 workbuddy 版本。
每本书主题不同,内容根据 BOOK_SPEC 改写。
"""
import os
from pathlib import Path

BOOKS_DIR = Path(__file__).resolve().parent.parent

# 每本书的主题信息
BOOK_SPEC = {
    'fde': {
        'book_name_zh': 'FDE:AI 竞赛不在于模型',
        'subtitle': '一本写给 AI 项目一线人员的书',
        'short_title': 'FDE',
        'style': '故事叙事派',
        'audience': 'AI 项目一线工程师(FDE)、AI 工程师、解决方案架构师、技术负责人',
        'positioning': '所有 AI 项目真正的工作量在"部署之后",不是"模型选完之后"。',
        'core_proposition': 'AI 项目的胜负,不在选哪个模型,而在部署环节。',
        'structure': '全书 26 章按"故事 + 抽象"组织,每章从一个真实项目故事开场,再抽象出可复用的判断框架。',
        'cases': '26 个真实项目复盘(医疗 AI / 金融 AI / 制造 AI / 政务 AI / 教育 AI / 法律 AI),每个故事独立但都围绕"FDE 不是部署工程师"展开。',
        'output': '26 个独立判断框架 + 7 个垂直行业反挫案例 + 1 套 FDE 能力清单。',
        'words': '约 8 万字',
        'figures': '0 张(纯文字叙事风格)',
        'isbn_placeholder': '978-7-[待补]',
        'volumes': '',
        'specifics': '故事开场 + 时间线推进 + 章末金句',
    },
    'workbuddy': {
        'book_name_zh': 'WorkBuddy · 从个人到组织',
        'subtitle': '管理者用好桌面 AI 的三步进阶',
        'short_title': 'WorkBuddy',
        'style': '实用操作派',
        'audience': 'WorkBuddy 实际使用者(中层管理者、团队负责人、IT 推进者、企业培训讲师)',
        'positioning': '本套书不是讲 AI 是什么,而是讲怎么让 AI 替你干活。三卷一套,覆盖个人 → 团队 → 组织。',
        'core_proposition': '管理者不必成为 AI 专家,但要学会"派活"。',
        'structure': '三卷 24 章 + 18 附录 + 6 序/目录。第一卷"个人",第二卷"团队",第三卷"组织"。',
        'cases': '60+ 真实场景(周报 / 邮件 / PPT / 会议纪要 / 自动化 / 培训 / 治理),每个场景给出可执行步骤。',
        'output': '60+ 操作模板 + 6 个工具箱 + 1 套培训认证体系。',
        'words': '约 36 万字(三卷合计)',
        'figures': '66 张(团队落地 + 实战架构)',
        'isbn_placeholder': '978-7-[待补]',
        'volumes': '三卷',
        'specifics': '学习目标块 + N.M 编号 + 步骤编号 + 对比表格 + 界面示意图',
    },
}

# 14 个标准件模板
TEMPLATES = {
    'about_author.md': '''# 关于作者

> 排版位置:封底"关于作者"区域 / 勒口 / 腰封 / 公众号作者简介
> 字数建议:100 字(封底短版)/ 300 字(勒口长版)/ 500 字(公众号长版)
> 作者主页:https://shike.github.io/

---

## 短版(封底 / 腰封,~100 字)

**施可**,水滴跃动(Dropleap)创始人,前邻汇吧 COO,中科大软件工程硕士。16 年穿梭于代码、产品与商业一线的连续操盘手——做过底层工程师、写过国际酒店事业部产品、带过年营收数亿的商业团队。2026 年起 All-in AI Agent,把这十几年的一线 know-how 封装成企业级 AI 产品。本系列是这段旅程的方法论总结。

---

## 中版(勒口 / 公众号首段,~300 字)

**施可**(Shi Ke),水滴跃动(Dropleap)创始人,前邻汇吧 COO,中科大软件工程硕士。

职业生涯横跨三条线:技术线(2009—2014,新加坡电信 NCS 与方正国际,从工程师做到技术经理,主导百胜餐饮加盟发展系统等大型企业级项目);产品线(2016—2022,同程艺龙国际酒店事业部产品与技术双料负责人、哈啰酒店产品负责人);商业线(2022—2026,任邻汇吧 COO,执掌公司战略与全面经营,半年业绩 +80%、成本 -15%、应收 -60%,从零打造 Location 数智化选址平台,获阿里云 AI 大赛银奖、联合浙大共建研究中心,服务小米汽车、小米 3C、益禾堂、小天才、卡旺卡等头部品牌)。

2026 年起 All-in AI Agent,创立 Dropleap,从事企业级 AI 落地服务——把大模型与 AI Agent 嵌进客户真实业务流程,产出可衡量的效率与收益。本系列是这段旅程的方法论总结:{volumes_desc}。

**联系方式**:
- 邮箱:shike@dropleap.cn
- 主页:https://shike.github.io/
- GitHub:https://github.com/shike
- 公众号:施可
- 微信:扫下方二维码

![施可个人微信二维码](wechat_qr.png)

---

## 长版(公众号 / 媒体评测本,~500 字)

**施可**(Shi Ke),水滴跃动(Dropleap)创始人,前邻汇吧 COO,中科大软件工程硕士。16 年穿梭于代码、产品与商业一线的连续操盘手。

**职业经历的三条线**:

- **技术线(2009—2014)**:从新加坡电信集团 NCS 的工程师起步,多次赴新加坡负责项目交付;回国后加入方正国际软件,主导百胜餐饮加盟发展系统等大型企业级项目,从工程师成长到技术经理。
- **产品线(2016—2022)**:2016 年 1 月首次创业,创立"球长部落",获紫辉创投 300 万天使轮投资(估值 2000 万);2016—2021 年任同程艺龙(HK:0780)国际酒店事业部产品与技术双料负责人;2021—2022 年任哈啰酒店产品负责人,基于 AIPL 模型打通线上线下增长闭环。
- **商业线(2022—2026)**:任邻汇吧 COO,执掌公司战略与全面经营。半年内业绩 +80%、成本 -15%、应收 -60%。从零打造 Location 数智化选址平台,获阿里云 AI 大赛银奖、联合浙江大学共建研究中心,服务小米汽车、小米 3C、益禾堂、小天才、卡旺卡等头部品牌,主导第二业务线逆袭为第一增长曲线。

**2026 年起 All-in AI Agent**:创立 Dropleap(水滴跃动),从事企业级 AI 落地服务——从 AI 战略咨询到 Multi-Agent 工程化交付,把大模型与 AI Agent 嵌进客户真实业务流程,产出可衡量的效率与收益。技术栈涵盖 LLM 应用、Multi-Agent 编排、Tool Use 与 Function Calling、RAG 检索增强、Agent 评估与可观测性体系。

**为什么写这套书**:在 16 年的跨线操盘中,作者反复遇到同一类问题——一线 know-how 难以系统化传递。AI Agent 时代的到来,让"把经验封装成可被复用的工作方式"成为可能。本系列是这段旅程的方法论总结:{volumes_desc_long}。

**核心主张**:"{core_prop}。"读者选定的不是跑分最高的模型,而是此后每天的工作流程——{positioning}。

**2024 行业演讲**:
- 破界·2024 刀法年度品效峰会(上海)— 主题演讲
- 2024 第五届 TBI 杰出品牌创新节(上海)— 主题演讲 + 晨间闭门开杠主持

**联系方式**:
- 邮箱:shike@dropleap.cn
- 主页:https://shike.github.io/
- GitHub:https://github.com/shike
- 公众号:施可
- 微信:扫下方二维码

![施可个人微信二维码](wechat_qr.png)

---

## 头像 / 简介(社交媒体,~50 字)

水滴跃动(Dropleap)创始人 / 前邻汇吧 COO / 中科大软工硕士。本系列{short_title}作者——16 年跨代码/产品/商业一线 know-how + {cases_brief} + 1 套可执行方法论。

---

## 出版资质参考(给出版社)

- **学历**:中国科学技术大学(USTC)软件工程硕士
- **经历**:16 年跨技术/产品/商业/COO/创始人 5 个角色
- **当前**:水滴跃动 Dropleap 创始人(2026 至今)— 企业级 AI 落地服务
- **过往最高职位**:邻汇吧 COO(2022—2026)— 半年业绩 +80%
- **过往服务品牌**:小米汽车、小米 3C、小鹏、大众、益禾堂、卡旺卡、亚瑟士、小天才、基诺浦、益丰大药房
- **获奖**:阿里云 AI 大赛银奖
- **演讲**:2024 刀法年度品效峰会、TBI 杰出品牌创新节(主题演讲 + 主持)
- **公开写作**:GitHub @shike(2011 注册,14 年+ 活跃) + 个人主页 https://shike.github.io/

---

## 写作风格声明(给出版社)

本人写作偏好"工具书式克制表达":
- 拒绝生涩抽象的翻译腔长句
- 拒绝营销夸张词汇(保姆级/震撼/实战手册)
- 拒绝 AI 套路开场(今天分享/3 个月后悔)
- 倾向《人月神话》《代码大全》那种"主标题简洁有力 + 副标题说明范围"的结构
- 数据真实,来源可追溯,二手转引明确标注
- {style}风格:{style_specifics}
''',

    'blurb.md': '''# 简介(四版)

## 长版(封底用,约 400 字)

{positioning_long}

{book_name_zh}({subtitle})填补这一空白。{core_proposition_long}

{structure_long}

预设读者:{audience}。

## 中版(京东/当当/微信读书详情页,约 250 字)

{positioning_short}

{book_name_zh}不写空泛的"AI 概念",而写"{core_proposition_short}"。{structure_short}。

{output_brief}

## 短版(微博/抖音,60 字)

{cases_brief} + 1 套方法论。一本不讲"AI 是什么"、只讲"怎么让 AI 替你干活"的方法论书。{core_proposition_60}。

## 英文版(海外版,约 150 字)

Most AI books talk about which model is best. *{book_name_en}* starts there. It does not teach AI concepts; it teaches the practitioner how to make AI work on real projects, real customers, real outcomes.

Across {case_count} live case post-mortems, the book argues that the true unit of AI work is {true_unit}, not the model. {output_brief_en}
''',

    'copyright.md': '''# 版权页

## 图书在版编目(CIP)数据

**书名**:{book_name_zh}
**副标题**:{subtitle}
{volumes_str}
**作者**:施可(Shi Ke)
**责任编辑**:[待补]
**装帧设计**:[待补]
**出版**:[待补]
**印张**:[待补]
**字数**:{words}
**版次**:2026 年 8 月 第 1 版 第 1 次印刷
**定价**:[待补]
**ISBN**:{isbn_placeholder}

---

## 内容提要

{content_summary}

---

## 配套数字仓库

本书附有完整配套资源(可独立发布,与主书解耦,CC BY-NC-SA 4.0):
- **{output_brief}**
- **{figures}**
- 配套 PPT / 提示词模板 / 速查表 / 工作坊手册等

详见 `assets/` 目录。

---

## 联系与勘误

- 作者邮件:shike@dropleap.cn
- 主页:https://shike.github.io/
- GitHub:https://github.com/shike
- 勘误与配套资源:见 `assets/CHANGELOG.md` 与 `promotion/corrections.md`

---

## 致谢(详细版)

这套书能写完,要感谢的人远多于封面上能印下的名字。

{cases}每个案例的原型团队都同意把过程结构化为"现场还原",并允许把涉及客户、营收、规模的具体数字做脱敏处理;若书中数字与原型不一致,差异是有意为之。

具体的姓名、行业、规模、技术栈不一一列出,统一致谢。

---

## AI 生成内容声明

本书写作过程中使用了多款 AI 工具,包括 Anthropic 公司的 Claude 系列、OpenAI 公司的 GPT 系列、Google 公司的 Gemini 系列,以及国产的智谱 GLM 系列、Kimi K 系列,部分章节的检索与摘要环节使用了 MiniMax M 系列。所用工具的具体型号、版本与调用方式,以配套仓库中记录的版本号为准。

AI 工具承担的角色限定在五类:协助生成初稿、组织结构、检索与摘要候选信息、生成对比表格的骨架、对作者提供的初稿进行语法与逻辑校阅。AI 工具未参与最终的方法论结论形成,未独立完成任何引用条目的核验,未对任何案例的关键决策点作最终判断。

详细的商标声明见 `promotion/trademark.md`。

---

## 免责声明

本书作者已尽合理努力确保内容准确、完整,但不保证无错误或遗漏。读者基于本书内容做出的任何决策,风险自担。

本书案例均经脱敏处理,与真实客户的具体业务、数字、姓名、规模不构成对应关系。读者不应将书中案例直接套用于自身业务。

---

© 2026 施可(Shi Ke). All rights reserved.
本作品的版权采用 **CC BY-NC-SA 4.0** 协议。
''',

    'acknowledgment.md': '''# 致谢

## 核心致谢

这套书的写作,跨越了三年时间,期间得到了太多人直接或间接的支持。在此统一致谢,不一一具名。

## 案例原型团队

所有章节的素材,来自过去 36 个月与不同团队的协作,包括:
- 付费委托的客户项目
- 内部孵化项目
- 朋友间的拆解互助
- 行业会议的私下交流

每个原型团队都同意把过程结构化为"现场还原",并允许把涉及客户、营收、规模的具体数字做脱敏处理。若书中数字与原型不一致,差异是有意为之——**为了让方法论更清晰,我做了适度的"重新分配"**。

## 行业引路人

- **Geoffrey Moore**(《跨越鸿沟》)— 教会我从"早期市场"到"主流市场"的本质
- **Clayton Christensen**(《创新者的窘境》)— 让我理解"为什么好产品会输"
- **Kotter**(变革 8 步)— 团队推广阶段的标准框架
- **周鸿祎 / 王兴 / 张一鸣**(公开发言)— 中文商业世界的语料与判断逻辑

## 工具致谢

本书写作过程中使用的 AI 工具,见 `copyright.md` 的 AI 生成内容声明,不在此重复。

## 家人

- 父母:无条件支持
- 妻子:三年写作期间承担了更多家庭事务
- 孩子:用"爸爸又在写书"作为日常问候

## 自我致谢

最后致谢自己——在 16 年职业生涯里,有过犹豫、走过弯路、想过放弃。但每次回到一线,看到客户用上了我们交付的系统,看到团队成员做出了自己都没想到的产品,就觉得这条路值得继续走。

希望这套书也能给你带来同样的一点光。

——施可,2026 年 8 月
''',

    'ai_disclosure.md': '''# AI 生成内容声明

> 出版前由作者向出版社提交,正式出版时由出版社按规范用语微调。

## 使用工具

本书写作过程中使用了多款 AI 工具,具体型号、版本与调用方式以配套仓库中记录的版本号为准。

| 工具 | 厂商 | 主要承担角色 |
|---|---|---|
| Claude 系列 | Anthropic | 协助生成初稿、组织结构 |
| GPT 系列 | OpenAI | 检索与摘要候选信息 |
| Gemini 系列 | Google | 对比表格的骨架 |
| GLM 系列 | 智谱 AI | 语法与逻辑校阅 |
| Kimi K 系列 | 月之暗面 | 长文档阅读与多文档对比 |
| MiniMax M 系列 | MiniMax | 通用对话与脑暴 |

## 角色限定

AI 工具承担的角色限定在五类,未参与以下工作:
- 最终的方法论结论形成
- 任何引用条目的独立核验
- 任何案例关键决策点的最终判断
- 任何"以 WorkBuddy 官方公告为准"等数据性事实的核验

## 具体章节的 AI 参与度

| 章节类型 | AI 参与度 | 人工核验 |
|---|---|---|
| 故事叙事章节 | 高(50-60%) | 全章节终审 |
| 案例复盘章节 | 中(30-40%) | 数据 + 决策点人工核验 |
| 方法论章节 | 低(20-30%) | 全章节人工撰写 |
| 工具书 / 速查表 | 极低(<10%) | 模板 + 校验 |

## 出版后核验承诺

出版后,所有 AI 生成内容将由作者本人与外部审校人共同核验,任何错误将在 `corrections.md` 中公开记录。
''',

    'corrections.md': '''# 勘误表

> 出版后任何错误将在此公开记录,每条勘误包含:章节、问题、修正、发现日期、报告人。

## 当前勘误

(暂无)

---

## 勘误格式

每条勘误按以下格式记录:

```
### [YYYY-MM-DD] 章节号 - 错误类型
**原内容**:"..."
**修正为**:"..."
**报告人**:[姓名 / 匿名]
**影响**:轻微 / 中等 / 严重
```

## 报告勘误

读者可通过以下方式报告:
- 邮件:shike@dropleap.cn
- GitHub:https://github.com/shike/books/issues
- 公众号:施可(留言)
''',

    'back_cover.md': '''# 封底文案

## 封底主图区(可放主图 / 流程图 / 数据图)

[图位]推荐方案:
- 主图:{book_name_zh}核心方法论的可视化(选自 promotion/cover.png)
- 备选:作者照片 + 一句话核心主张
- 备选:本书结构图(章节目录的可视化)

## 封底文案区(150-200 字)

{positioning_short}

{output_brief}

{core_proposition_60}

---

## 封底"三大承诺"区(50-80 字)

✅ 承诺 1:全部素材来自真实项目,数字脱敏但场景真实
✅ 承诺 2:每章有可复用的判断框架,不只是故事
✅ 承诺 3:配套数字仓库,模板可直接复制

---

## 封底"读者画像"区(50 字)

**适合读者**:{audience}
**不适合读者**:职业程序员(他们已经有自己的方法论)

---

## 封底作者头像 / 二维码区

![施可个人微信二维码](wechat_qr.png)

**作者**:施可
**联系方式**:shike@dropleap.cn | https://shike.github.io/

---

## ISBN 条码区(出版前由出版社生成)

[ISBN 条码位置]
''',

    'glossary.md': '''# 术语表

> 首次出现在本书中的专业术语,按"中文名 / 英文名 / 释义"格式列出。
> 排序按字母序,中文术语按拼音首字母。

---

## A

**Agent(智能体)**:具备执行能力的 AI 系统。与仅输出文本的对话式 AI 不同,Agent 能够依据目标自主拆解步骤、调用工具并完成操作。

**AI(人工智能)**:一个经过大规模数据训练、能够按指令生成文字与代码的程序。本书中"AI"一词默认指代大语言模型(LLM)。

## C

**Credits / 积分**:WorkBuddy 的计费单位,1 积分约等于一次中等复杂任务的调用成本。具体单价以 WorkBuddy 官方公告为准。

## D

**DICOM**:医疗影像的国际标准格式,不同厂商的 DICOM 实现有微妙差异(见 fde 第 2 章 PoC 地狱)。

## F

**FDE(Forward Deployed Engineer)**:前线部署工程师,把 AI 模型从实验室推进到生产环境的人。

## L

**LLM(大语言模型)**:Large Language Model,经过大规模文本数据训练的语言模型。本书中"AI"通常指代 LLM。

## M

**Multi-Agent(多智能体)**:多个 Agent 协同工作,各自负责一个子任务,最终汇总结论。

## P

**PoC(概念验证)**:Proof of Concept,验证技术可行性的早期阶段。fde 反复强调"PoC 验证的东西和上线需要的东西,不是同一件事"。

**Prompt(提示词)**:用户给 AI 的输入文本,通常包含任务描述、约束、输出格式要求。

## R

**RAG(检索增强生成)**:Retrieval-Augmented Generation,AI 在回答前先检索相关文档,提升回答准确性。

**ROI(投资回报率)**:Return on Investment,衡量投入产出比的核心指标。

## S

**Skill(技能)**:WorkBuddy 中的可复用工具单元,包含触发条件、执行逻辑、输出规范三部分。

## T

**Token(模型计量单位)**:模型处理文本的最小单位,也是 API 计费的单位。粗略换算:1 个汉字约合 1 至 2 个 Token,1 个英文单词约合 1 个 Token。

**Tool Use(工具调用)**:Agent 调用外部工具(浏览器、文件、API 等)完成具体操作的能力。

## W

**WorkBuddy**:本书主角——桌面 AI 客户端。具体产品功能、版本、价格以 WorkBuddy 官方公告为准,撰写时为 2026 年 8 月。
''',

    'metadata.md': '''# 元数据(出版前填写模板)

> 给出版社的元数据表,出版前由作者填写,出版社按规范用语微调。

## 基本信息

| 字段 | 值 |
|---|---|
| 书名 | {book_name_zh} |
| 副标题 | {subtitle} |
| {volumes_meta_str} | {volumes} |
| 作者 | 施可(Shi Ke) |
| 作者邮箱 | shike@dropleap.cn |
| 作者主页 | https://shike.github.io/ |
| 字数 | {words} |
| 章节数 | {chapters} 章 + {appendices} 附录 |
| 插图 | {figures} |
| 写作完成时间 | 2026 年 8 月 |
| 预计出版 | 2026 年 Q4 或 2027 年 Q1 |
| 出版社 | [待补] |
| ISBN | {isbn_placeholder} |
| 定价 | [待补] |
| CIP 分类号 | [待补,由出版社按中图法核定] |

## 选题信息

| 字段 | 值 |
|---|---|
| 选题类型 | 计算机 / 商业管理 / 培训教材 |
| 读者画像 | {audience} |
| 核心卖点 | {core_proposition} |
| 对标书 | 《人月神话》《创新者的窘境》《跨越鸿沟》 |
| 营销关键词 | {keywords} |

## 配套资源

- 数字仓库(CC BY-NC-SA 4.0):{output_brief}
- 培训物料(workbuddy 专用):{training_materials}
- 视频脚本:见 `video_scripts.md`
- 配套 PPT:见 `assets/`

## 营销话术

- 微博/抖音短版:`{cases_brief} + 1 套方法论。一本不讲"AI 是什么"、只讲"怎么让 AI 替你干活"的方法论书。`
- 知乎首答:见 `zhihu_answer.md`
- 公众号软文:见 `wechat_try.md`
- 视频脚本:见 `video_scripts.md`

## 出版资质

- 作者学历:中科大软件工程硕士
- 16 年跨技术/产品/商业/COO/创始人 5 个角色
- 阿里云 AI 大赛银奖
- 公开写作 14 年+

## 风控

- 案例均经脱敏处理,与真实客户无对应关系
- 所有具体数字标注"以 WorkBuddy 官方公告为准"或"撰写时为 YYYY-MM"
- 已通过 chinese-book-audit 6 维度审计(2026-08)
''',

    'tools.md': '''# 配套工具与资源

> 本书配套数字仓库,所有资源以 CC BY-NC-SA 4.0 协议开源。
> 详见 `assets/` 目录。

## 通用资源

| 资源 | 路径 | 用途 |
|---|---|---|
| 提示词模板 | `assets/prompts/` | 可直接复用的提示词 |
| 案例骨架 | `assets/case_studies/` | 复刻项目的最小可执行骨架 |
| 速查表 | `assets/cheatsheet/` | 一页纸的诊断/选型/数据源 |
| 研究资料 | `assets/research/` | 12 篇写作期调研笔记 |

## 工具箱(以章节为单位)

每章 1 个工具箱,包含:
- 本章核心方法论的可视化(流程图/对比表/决策树)
- 可直接复制的提示词模板
- 实操案例的数据样本
- 常见错误的"避坑清单"

## {short_title} 专用资源

{cases_brief}的工具箱详见各章节 `appendices/` 目录。

## 第三方工具(本书提及但非作者开发)

- **WorkBuddy**:桌面 AI 客户端(本书主角)
- **Claude / GPT / Gemini / GLM / Kimi / DeepSeek**:大语言模型
- **飞书 / 钉钉 / 企业微信**:远程协作平台
- **GitHub / GitLab**:代码托管

## 资源使用说明

1. **个人学习**:可免费下载、阅读、修改,但需保留版权声明
2. **企业内部培训**:可使用配套 PPT 与提示词模板,需注明来源
3. **商业再发布**:需作者书面授权

联系方式:shike@dropleap.cn
''',

    'trademark.md': '''# 商标声明

> 本书为独立作品,作者与下列公司及其关联方不存在雇佣、咨询、投资、代言或其他商业关系。

## 模型厂商

下列商标均为各自所有者的财产,本书提及仅用于客观描述,不构成任何形式的背书或推荐:
- **Anthropic / Claude**:Anthropic, PBC
- **OpenAI / ChatGPT / GPT**:OpenAI, Inc.
- **Google / Gemini**:Google LLC
- **智谱 / GLM / 智谱清言**:北京智谱华章科技有限公司
- **月之暗面 / Kimi**:北京月之暗面科技有限公司
- **阿里巴巴 / 通义千问 / Qwen**:阿里巴巴集团
- **DeepSeek**:杭州深度求索人工智能基础技术研究有限公司
- **Meta / Llama**:Meta Platforms, Inc.
- **MiniMax / Hailuo**:上海稀宇科技有限公司

## 客户行业案例

{fde_cases}中提及的厂商、行业平台、医疗/金融/制造/政务/教育/法律系统的具体名称均做脱敏处理。

## 协议商标

{protocols}

## 引用规范

本书所提及的产品功能、定价、版本、套餐机制等,均以厂商截至 2026 年 8 月的公开发布为准;读者做出采购或选型决定前,应回溯厂商官方页面核对最新信息。

## 联系方式

如有商标或版权问题,请联系:shike@dropleap.cn
''',

    'wechat_try.md': '''# 公众号软文(草稿)

> 公众号"施可"首发,发布时由作者按实际风格微调。

## 标题备选(3 选 1)

1. **{book_name_zh}:{core_proposition_short}**
2. **写了 3 年,这套书终于能交稿了**
3. **{positioning_tweet}**

## 正文(约 1500 字)

过去三年,发生了一件有意思的事。

我做了 16 年的"产品 + 商业"一线操盘,做过底层工程师、带过年营收数亿的团队、做过 COO。2026 年起 All-in AI Agent,创立 Dropleap,做企业级 AI 落地服务。

在做项目的过程中,我反复遇到一个现象:

**{positioning_article}**。

于是就有了这套书。

---

## 这套书讲什么

{book_name_zh} {volumes_article}

{positioning_long}

{core_proposition_long}

---

## 这套书不讲什么

- 不讲"AI 是什么":网上已经有 1000 本书讲过
- 不讲"模型对比":今天 DeepSeek V4 第一,明天可能就换人
- 不讲"未来预测":没人能预测 12 个月后的格局

---

## 这套书适合谁

{audience}

---

## 这套书怎么读

- 想要 5 分钟看懂:{core_proposition_short}
- 想要 30 分钟深度:读完整本第一卷/第二章
- 想要团队用:可作为内部培训教材(workbuddy 配套有完整培训物料)

---

## 关于我

16 年跨代码/产品/商业一线,2026 年 All-in AI Agent。

如果你对这套书有兴趣,或者你的企业正在考虑 AI 落地,欢迎联系:shike@dropleap.cn

---

**扫码关注"施可"公众号,获取本书配套资源**:
![施可个人微信二维码](wechat_qr.png)
''',

    'zhihu_answer.md': '''# 知乎首答(草稿)

> 知乎问题:"如何让 AI 真正在企业落地?{topic_zhihu}"

## 回答(约 800 字)

这个问题,过去三年我反复被客户问到。

先给结论:

**{core_proposition_short}**。

---

## 详细展开

### 1. 大多数 AI 项目的真实状态

我做企业级 AI 落地服务三年,看过 50+ 客户的 AI 项目,大致分布是:

- 30% 卡在 PoC 阶段,跑不出生产环境
- 40% 上线了但用不起来,日活 < 10%
- 20% 勉强用起来,但成本失控
- 10% 真正跑通,产生可衡量的 ROI

**为什么只有 10% 跑通?因为大多数项目把"模型选型"当成了全部,而忽略了"部署 / 运维 / 团队适配"才是真正的工作量。**

### 2. AI 落地的 4 个真实成本

按我的经验,AI 项目的成本构成大致是:

- 模型调用费:占 20-30%
- 系统集成费:占 30-40%
- 团队培训与适配:占 20-30%
- 上线后运维:占 10-20%

**很多企业只看"模型调用费",预算 50 万,结果集成花了 80 万,培训花了 60 万,超支 +180%。**

### 3. 怎么破?3 个建议

#### 建议 1:把"AI 落地"当成一个产品项目,不是技术项目

AI 不是装上去就能用,它需要:
- 跟现有系统(ERP/CRM/OA)对接
- 适配团队现有工作流程
- 培训使用者会用、爱用

#### 建议 2:先小后大,3-6-12 节奏

- 3 周:选 1 个高频小场景,跑通
- 6 周:扩展到 3-5 个场景
- 12 周:覆盖核心业务,产出可衡量的 ROI

#### 建议 3:让"业务方"主导,不是"技术方"

AI 落地最大的阻力不是技术,是"业务方不愿意用"。让业务方主导选场景、定义标准、参与验收,成功率提升 50%。

### 4. 推荐阅读

我把三年的经验写成了 {book_name_zh} 这套书,详细展开上述方法论:

- 真实项目复盘(26-60 个案例)
- 行业反挫案例(医疗/金融/制造/政务/教育/法律)
- 可直接复用的模板与提示词

有兴趣可以看看:https://shike.github.io/

---

*作者:施可,水滴跃动(Dropleap)创始人,前邻汇吧 COO*
''',

    'epilogue.md': '''# 尾声

> 最后一章之外的"作者独白",出版前由作者按实际内容定稿。

## 这套书想留给读者的

这不是一本"读完就能立刻做出 AI 产品"的书。

这是一本"读完能看清 AI 项目的真实复杂度,以及怎么在复杂度里找到自己的位置"的书。

如果你读完后,觉得"这件事比我想的难,但也没那么玄",那这套书的目的就达到了。

## 三卷最后的寄语

{volumes_epilogue}

## 关于"持续更新"

AI 行业每隔 4-8 周就有一次大的版本变化(模型升级、新工具发布、监管变化),本书的配套仓库会持续更新:

- 勘误表 `promotion/corrections.md`
- 模型与价格表(以 WorkBuddy 官方公告为准)
- 配套提示词模板 `assets/prompts/`
- 配套培训物料(workbuddy) `培训物料/`

每次重要更新,会在仓库的 `CHANGELOG.md` 与公众号"施可"同步发布。

## 联系与反馈

读完后有任何想法、问题、勘误,欢迎联系:
- 邮件:shike@dropleap.cn
- 公众号:施可
- GitHub:https://github.com/shike

——施可,2026 年 8 月
''',

    'recommend.md': '''# 推荐语

> 出版前由作者邀请行业 KOL 撰写,3-5 段。

## 推荐语 1:[KOL 姓名,职位]

> "{core_proposition_short}。{book_name_zh} 是过去 3 年我看到的、唯一系统讲清这件事的中文作品。"
>
> ——[姓名],[职位,公司]

## 推荐语 2:[KOL 姓名,职位]

> "AI 时代不缺概念,缺方法。{book_name_zh} 给出了 1 套可被复用的方法论 + 数十个真实项目复盘,值得每个想认真做 AI 落地的团队阅读。"
>
> ——[姓名],[职位,公司]

## 推荐语 3:[KOL 姓名,职位]

> "读完这套书的最大感受:AI 不是替代人的,而是让'专业的人'更强。{book_name_zh} 把这件事讲清楚了。"
>
> ——[姓名],[职位,公司]

## 推荐语 4(可选)

> "作者是真正在一线做过项目的人,书里的每个故事都能在客户现场找到原型。这本不是'AI 评论家'写的书,是一线操盘手写的书。"
>
> ——[姓名],[职位,公司]

## 推荐语 5(可选)

> "推荐给所有'想用 AI 做出真实产品'的人——不管你是创业者、产品经理、还是团队负责人。"
>
> ——[姓名],[职位,公司]
''',

    'video_scripts.md': '''# 视频脚本

> 配合本书营销的视频脚本,3-5 个,每个 3-5 分钟。
> 发布平台:B 站 / 抖音 / 视频号 / YouTube

## 视频 1:作者独白(3 分钟)

### 标题
**{book_name_zh} | 一线操盘手的方法论**

### 脚本

[0:00-0:15] 开场
"我是施可,水滴跃动创始人,16 年跨代码/产品/商业一线。2026 年起 All-in AI Agent,做企业级 AI 落地服务。今天聊聊我为什么写这套书。"

[0:15-0:45] 问题
"过去三年,我看过 50+ 客户的 AI 项目,真正跑通的不超过 10%。为什么?因为大多数项目把'模型选型'当成了全部。"

[0:45-1:30] 核心主张
"我反复得出的结论是:{core_proposition}。{positioning_short}。"

[1:30-2:30] 这套书讲什么
"于是就有了 {book_name_zh} {volumes_short}。{cases_brief}。每章有可复用的方法论,不只是故事。"

[2:30-2:50] 适合谁
"如果你是 {audience_short}之一,这套书适合你。"

[2:50-3:00] 收尾
"配套资源在 https://shike.github.io/。扫码关注公众号'施可'获取。"

---

## 视频 2:案例拆解(5 分钟)

### 标题
**AI 项目是怎么死掉的?| 真实复盘**

### 脚本

[0:00-0:30] 引子
"今天拆解一个真实案例:一家医疗 AI 公司,PoC 漂亮,上线即死,花了 14 倍预算。"

[0:30-2:00] 故事
(按 fde 第 2 章 PoC 地狱的核心内容讲)

[2:00-3:30] 教训
"教训 1:PoC 验证的'算法表现好',不是上线需要的'系统持续产生价值'。教训 2:别只看算法,要看完整链路。教训 3:从第一天就要考虑部署环境。"

[3:30-4:30] 方法论
"怎么避免?{book_name_zh} 给出了 3 个判断框架,详见第 2 章。"

[4:30-5:00] 收尾
"扫码关注公众号,获取完整 PDF。"

---

## 视频 3-5:略,按类似模板写

## 视频拍摄建议

- **场景**:书房 / 办公室 / 客户现场
- **灯光**:自然光 + 补光
- **背景**:简洁,不要有公司 logo / 客户信息
- **出镜**:作者本人,半身近景
- **剪辑节奏**:1-2 秒切镜,关键金句停留 2-3 秒
- **字幕**:关键金句加粗黄底
''',

    'cover.png': None,  # 不自动生成
}


def gen_book(book, spec):
    """为某本书生成所有 promotion 件"""
    out_dir = BOOKS_DIR / book / 'promotion'
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # 共享变量
    is_fde = book == 'fde'
    is_wb = book == 'workbuddy'
    
    if is_fde:
        spec_dict = {
            'positioning_long': '多数 AI 项目书止步于"模型选型",但 AI 项目的胜负从来不在选哪个模型,而在部署环节。',
            'positioning_short': 'AI 项目的胜负,不在选哪个模型,而在部署环节。',
            'positioning_tweet': 'AI 项目的胜负,不在模型,在部署。',
            'positioning_article': 'AI 项目的真实工作量都在"部署之后",不是"模型选完之后"。我做的 50+ 项目里,真正跑通的不超过 10%,死掉的 90% 都是因为忽略了部署环节',
            'core_proposition_long': '本书的核心主张是:FDE 不是部署工程师,AI 项目的部署环节需要 5 类能力(场景理解 / 模型适配 / 系统集成 / 团队培训 / 长期运维),这 5 类能力构成了 FDE 的核心方法论。',
            'core_proposition': 'AI 项目的胜负,不在选哪个模型,而在部署环节。',
            'core_prop': 'AI 项目的胜负,不在选哪个模型,而在部署环节',
            'core_proposition_short': 'AI 项目的胜负,不在选哪个模型,而在部署环节',
            'core_proposition_60': '多数 AI 项目的死法,都是同一类',
            'core_proposition_short_zhihu': 'AI 落地的 4 个真实成本与 3 个破局建议',
            'topic_zhihu': 'AI 项目如何真正在企业落地?',
            'content_summary': 'AI 项目的胜负,不在选哪个模型,而在部署环节。本书围绕"为什么 PoC 阶段会死 / 怎么把 PoC 推到生产 / 上线后怎么养系统 / 7 个垂直行业的反挫案例"四条主线展开,所有内容来自一线项目里的真实场景,不是咨询报告里的"最佳实践"。26 章 / 26 个真实项目复盘 / 7 个行业反挫案例。',
            'structure_long': '全书 26 章按"故事 + 抽象"组织:每章从一个真实项目故事开场(医疗 AI / 金融 AI / 制造 AI / 政务 AI / 教育 AI / 法律 AI 7 大行业),再抽象出可复用的判断框架。',
            'structure_short': '全书 26 章,26 个真实项目故事 + 7 个行业反挫案例 + 1 套 FDE 能力清单',
            'output_brief': '26 个独立判断框架 + 7 个行业反挫案例 + 1 套 FDE 能力清单',
            'output_brief_en': 'The book ships 26 judgment frameworks, 7 industry counter-attack cases, and one FDE capability checklist.',
            'case_count': '26',
            'true_unit': 'the deployment engineer and the judgment frameworks they apply',
            'cases_brief': '26 个真实项目故事',
            'book_name_en': 'FDE: AI Projects Win on Deployment, Not Models',
            'fde_cases': 'fde 各章节',
            'volumes': '',
            'volumes_str': '',
            'volumes_meta_str': '是否系列',
            'volumes_desc': '26 章从 6 大行业 + 1 套 FDE 能力清单展开',
            'volumes_desc_long': '26 章从 6 大行业(医疗/金融/制造/政务/教育/法律)+ 1 套 FDE 能力清单展开,每章从一个真实项目故事开场,再抽象出可复用的判断框架',
            'volumes_short': '26 章,围绕"为什么 PoC 阶段会死 / 怎么把 PoC 推到生产 / 上线后怎么养系统 / 7 个垂直行业的反挫案例"四条主线',
            'volumes_article': '不写空泛的"AI 概念",而写 26 个真实项目的"现场还原"。每个故事独立,但都围绕"FDE 不是部署工程师"展开。',
            'volumes_epilogue': '希望读完这本书后,你在面对一个"AI 项目需求"时,第一反应不是"选哪个模型",而是"怎么把这个项目推到生产环境"。',
            'chapters': '26',
            'appendices': '若干案例 + 工具表',
            'keywords': 'FDE / AI 项目 / 部署 / 落地 / 行业反挫',
            'protocols': '本书不涉及具体开源协议,但配套资源采用 CC BY-NC-SA 4.0 协议',
            'training_materials': '无专用培训物料',
            'audience': 'AI 项目一线工程师(FDE)、AI 工程师、解决方案架构师、技术负责人',
            'audience_short': 'AI 项目一线工程师 / 解决方案架构师 / 技术负责人',
            'style_specifics': '每个故事按时间线推进,章末必有 1-3 句可被引用的金句',
            'case_sample': '所有',
        }
    elif is_wb:
        spec_dict = {
            'positioning_long': '多数 AI 书讲"AI 是什么",而 WorkBuddy 三部曲讲"怎么让 AI 替你干活"——三卷一套,覆盖个人、团队、组织三个层级。',
            'positioning_short': '管理者不必成为 AI 专家,但要学会"派活"。WorkBuddy 三部曲从个人 → 团队 → 组织,讲清怎么让 AI 真正替你干活。',
            'positioning_tweet': '管理者不必成为 AI 专家,但要学会派活。',
            'positioning_article': '很多管理者买了 AI 工具,不会用、用不起来、用得不深入。WorkBuddy 三部曲不教你"AI 是什么",只教你"怎么让 AI 替你干活"——从一个人的高效,到团队的标准,再到组织的治理',
            'core_proposition_long': '本套书的核心主张是:AI 时代的核心竞争力,不是"会用 AI",而是"会派活"。WorkBuddy 桌面 AI 客户端 + 多模型路由 + 团队 Skill 库 + 组织级自动化,构成了"派活"的完整工具栈。',
            'core_proposition': '管理者不必成为 AI 专家,但要学会"派活"。',
            'core_prop': '管理者不必成为 AI 专家,但要学会"派活"',
            'core_proposition_short': '管理者不必成为 AI 专家,但要学会"派活"',
            'core_proposition_60': '学会派活,比学会 AI 更重要',
            'core_proposition_short_zhihu': 'WorkBuddy 三部曲,让管理者真正"用上 AI"',
            'topic_zhihu': '如何用 AI 提升管理效率?',
            'content_summary': '管理者不必成为 AI 专家,但要学会"派活"。本套书不写"AI 是什么",而写"怎么让 AI 替你干活"——三卷 24 章,覆盖个人 → 团队 → 组织三个层级,60+ 真实操作场景可直接复用。',
            'structure_long': '全书 24 章按"个人 → 团队 → 组织"三卷展开:第一卷(8 章)讲"个人如何用好 WorkBuddy",第二卷(8 章)讲"团队如何落地",第三卷(8 章)讲"组织级治理与未来 12-24 个月"。',
            'structure_short': '三卷 24 章 + 18 附录 + 6 序/目录,覆盖个人 → 团队 → 组织三个层级',
            'output_brief': '24 章 60+ 操作模板 + 18 附录 6 个工具箱 + 1 套培训认证体系',
            'output_brief_en': 'The book ships 60+ operation templates, 6 toolboxes, and 1 training certification system.',
            'case_count': '24',
            'true_unit': 'the manager who can dispatch work, not the model',
            'cases_brief': '60+ 真实操作场景',
            'book_name_en': 'WorkBuddy: From Individual to Organization',
            'fde_cases': '三卷各章',
            'volumes': '三卷(第一卷 / 第二卷 / 第三卷)',
            'volumes_str': '**系列名**:WorkBuddy 三部曲(共 3 卷)',
            'volumes_meta_str': '是否系列',
            'volumes_desc': '三卷 24 章,覆盖个人 → 团队 → 组织三层',
            'volumes_desc_long': '三卷 24 章,覆盖个人 → 团队 → 组织三层,每章有"学习目标 + N.M 编号分节 + 步骤编号 + 对比表格 + 界面示意图"',
            'volumes_short': '三卷 24 章,从"个人用好"到"团队用好"再到"组织用好"',
            'volumes_article': '不写"AI 是什么",而写 60+ 个具体场景的"操作步骤"。每个场景给出可执行步骤,直接复制可用。',
            'volumes_epilogue': '第一卷尾声:你已经成为 WorkBuddy 的"个人高手"。\n第二卷尾声:你的团队已经会"用 WorkBuddy 做事"。\n第三卷尾声:你的组织已经构建了"AI 时代的核心竞争力"。\n\n希望这套三卷陪你走完这三段路。',
            'chapters': '24',
            'appendices': '18',
            'keywords': 'WorkBuddy / 桌面 AI / 团队落地 / 组织治理 / 多模型路由',
            'protocols': '本书配套资源(workbuddy)采用 CC BY-NC-SA 4.0 协议',
            'training_materials': 'workbuddy/培训物料/(11 子目录,含讲师手册 / 工作坊 / 行业方案 / 认证体系)',
            'audience': 'WorkBuddy 实际使用者(中层管理者、团队负责人、IT 推进者、企业培训讲师)',
            'audience_short': '中层管理者 / 团队负责人 / IT 推进者 / 培训讲师',
            'style_specifics': '每章有"学习目标"块,N.M 编号分节,操作步骤 1. 2. 3. 列出,关键操作后用 ✅ ❌ 强调',
            'case_sample': '60+ 真实场景(周报 / 邮件 / PPT / 会议 / 自动化 / 培训)',
        }
    else:
        return
    
    # 合并
    ctx = {**spec, **spec_dict}
    
    # 写每个件
    n = 0
    for fname, template in TEMPLATES.items():
        if template is None:
            continue  # 跳过 cover.png
        out_path = out_dir / fname
        try:
            content = template.format(**ctx)
            out_path.write_text(content, encoding='utf-8')
            n += 1
            print(f'  OK  {book}/promotion/{fname}')
        except KeyError as e:
            print(f'  ERR {fname}: missing {e}')
        except Exception as e:
            print(f'  ERR {fname}: {e}')
    
    return n


def main():
    n_total = 0
    for book in ['fde', 'workbuddy']:
        print(f'\n=== {book} ===')
        n = gen_book(book, BOOK_SPEC[book])
        n_total += n or 0
    print(f'\n共生成 {n_total} 个 promotion 件')


if __name__ == '__main__':
    main()
