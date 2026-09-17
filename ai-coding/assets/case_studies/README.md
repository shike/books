# 案例骨架索引

> 配套《AI Coding:人人都是程序员》第 2—12 章。本目录共 11 个案例骨架,对应书中 11 个「完整方法论」章节。
> 第 0/1/13/14/15 章是方法论章,不提供案例骨架;其方法论请直接读原书,工具性资产见 `cheatsheet/` 目录。

## 目录

| 章节 | 标题 | 核心方法 | 关键文件/资源 | 估算工时 |
|---|---|---|---|---|
| 第 2 章 | 复刻网站的全流程编排 | 四段式(侦察—设计—重建—验收),把模糊需求变为可验收的中间产物。 | [sec02_clone_website.md](sec02_clone_website.md) + [02_clone_website.md](../prompts/02_clone_website.md) | 5—15 工作日 |
| 第 3 章 | 复刻 SaaS 系统的 80/20 编排 | 五件套(凭据隔离/白名单/检查点/人工接管/行为留痕)+ 80/20 边界划分,把 SaaS 复刻做成可上线的成品而非演示品。 | [sec03_clone_saas.md](sec03_clone_saas.md) + [03_clone_saas.md](../prompts/03_clone_saas.md) | 15—30 工作日 |
| 第 4 章 | 24 小时 Demo 对齐流程 | 三个原则:让客户看到东西而非描述东西;形容词不能验收,数字才能验收;规格必须固化,与代码同源。 | [sec04_demo_alignment.md](sec04_demo_alignment.md) + [04_24h_demo.md](../prompts/04_24h_demo.md) | 1—2 工作日 |
| 第 5 章 | 经营周报的自动化管道 | 四段式数据管道(取数—清洗—分析—呈现)+ 口径即代码 + 数据分层隔离 + 每个数字可回溯。 | [sec05_weekly_report.md](sec05_weekly_report.md) + [05_weekly_report.md](../prompts/05_weekly_report.md) | 3—5 工作日(首次搭建)/ 1 小时/周(运行时) |
| 第 6 章 | 飞书常驻 Agent 的部署与运行 | 把 AI 当作虚拟员工:替代执行(不是辅助);常驻会话;隔离子 Agent;最小权限。 | [sec06_feishu_agent.md](sec06_feishu_agent.md) + [06_feishu_agent.md](../prompts/06_feishu_agent.md) | 5—10 工作日(首次部署)/ 1 小时/月(运维) |
| 第 7 章 | 行业调研的全流程编排 | 三件套按特性分工(搜索补缺/RAG 主分析/爬虫建库)+ 先建库后查询 + AI 整合人工审核 + 引用规范。 | [sec07_industry_research.md](sec07_industry_research.md) + [07_industry_research.md](../prompts/07_industry_research.md) | 10—20 工作日(首次建库)/ 1—3 工作日/次(复用库做调研) |
| 第 8 章 | 经验三层沉淀的执行编排 | 三层沉淀(知识库检索 / Skill AI 调用 / Prompt 模板人工复用)+ 经验条目五项结构(场景-现象-原因-解法-效果)+ 持续维护。 | [sec08_experience_distill.md](sec08_experience_distill.md) + [08_experience_distill.md](../prompts/08_experience_distill.md) | 5—10 工作日(沉淀机制搭建)/ 1 小时/周(条目维护) |
| 第 9 章 | 反馈回路的工程化编排 | 四原则:采集自动化(反馈回路让知识库从静态变动态)/ 三类触发(异常/决策/新模式)/ 人工审核最小化 / 知识库定期瘦身。 | [sec09_feedback_loop.md](sec09_feedback_loop.md) + [09_feedback_loop.md](../prompts/09_feedback_loop.md) | 10—15 工作日(回路搭建)/ 持续运行 |
| 第 10 章 | 7 天 MVP 的时间盒编排 | 五原则:时间盒约束(逼你做减法)/ 关键路径优先 / 关键决策集中在前 2 天 / AI 做执行人做判断 / 第一笔收款比想象中重要。 | [sec10_7day_mvp.md](sec10_7day_mvp.md) + [10_7day_mvp.md](../prompts/10_7day_mvp.md) | 7 个日历日 |
| 第 11 章 | 遗留系统三阶段改造的执行编排 | 四原则:改造目标是「可被理解」而非「重写」 / 第一阶段必须充分理解 / 沙盒测试不可省略 / 灰度发布是上线标准流程。 | [sec11_legacy_system.md](sec11_legacy_system.md) + [11_legacy_system.md](../prompts/11_legacy_system.md) | 6—8 周(8 万行代码参考规模) |
| 第 12 章 | 竞品监控系统的全流程编排 | 四原则:三层管道解耦 / 三级分类(NOISE/MINOR/MAJOR)/ 边界清晰(只监控公开页面)/ 成本远低于商业方案。 | [sec12_competitor_monitor.md](sec12_competitor_monitor.md) + [12_competitor_monitor.md](../prompts/12_competitor_monitor.md) | 10—15 工作日(系统搭建)/ 1 小时/天(运行时) |

## 读者复用路径(标准 3 步)

1. **读章节**:打开原书对应章节,理解方法论背景与案例现场段。
2. **复制提示词**:从 `prompts/` 目录复制对应章节的完整提示词,粘贴到你的 AI 工具(Claude / GPT / Cursor / Trae 等)。
3. **按骨架跑一遍**:打开本目录下对应的骨架文件,按「实践步骤」在小项目上跑一遍,记录踩到的坑。

完成 3 步后,读者应产出:一份自己的项目方案 + 一份「哪些坑踩到了」的复盘笔记。

## 命名约定

- `sec0X_*`:对应原书第 X 章(X 为 0—15)
- 文件名用小写英文 + 下划线,便于脚本批处理
- 章节号 0=前言,1=第 1 章,2—12=第 2—12 章(本目录覆盖范围),13/14/15 在 `cheatsheet/` 速查表中

## 不在本目录的情况

- 第 0 章(前言)与第 1 章(三问选型)是工具书式方法论,详见 `prompts/00_general_baseline.md` 与 `prompts/01_three_questions.md`,速查版见 `cheatsheet/model_selection.md`
- 第 13/14/15 章是工程治理方法论,速查版见 `cheatsheet/issue_diagnosis.md` / `data_source_decision.md` / `four_levers.md`
