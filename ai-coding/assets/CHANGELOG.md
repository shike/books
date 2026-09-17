# 更新日志

本仓库所有重要变更均记录于此。格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 标准,
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范。

## [1.0.0] - 2026-08-03

### 新增

- **16 个完整提示词**(对应原书 16 个「完整提示词」段)
  - `prompts/00_general_baseline.md` — 前言基线
  - `prompts/01_three_questions.md` — 第 1 章三问选型
  - `prompts/02_clone_website.md` — 第 2 章复刻网站
  - `prompts/03_clone_saas.md` — 第 3 章复刻 SaaS
  - `prompts/04_24h_demo.md` — 第 4 章 24 小时 Demo
  - `prompts/05_weekly_report.md` — 第 5 章经营周报
  - `prompts/06_feishu_agent.md` — 第 6 章飞书常驻 Agent
  - `prompts/07_industry_research.md` — 第 7 章行业调研
  - `prompts/08_experience_distill.md` — 第 8 章经验三层沉淀
  - `prompts/09_feedback_loop.md` — 第 9 章反馈回路
  - `prompts/10_7day_mvp.md` — 第 10 章 7 天 MVP
  - `prompts/11_legacy_system.md` — 第 11 章遗留系统改造
  - `prompts/12_competitor_monitor.md` — 第 12 章竞品监控
  - `prompts/13_four_issues.md` — 第 13 章四类工程问题
  - `prompts/14_data_acquisition.md` — 第 14 章数据获取
  - `prompts/15_scaffolding.md` — 第 15 章脚手架四杠杆
  - 配套 `prompts.jsonl`(16 行,每行一个 JSON,便于脚本批处理)

- **11 个案例骨架**(对应原书第 2—12 章)
  - `case_studies/sec02_clone_website.md` — 复刻网站
  - `case_studies/sec03_clone_saas.md` — 复刻 SaaS
  - `case_studies/sec04_demo_alignment.md` — 24 小时 Demo 对齐
  - `case_studies/sec05_weekly_report.md` — 经营周报自动化
  - `case_studies/sec06_feishu_agent.md` — 飞书常驻 Agent
  - `case_studies/sec07_industry_research.md` — 行业调研
  - `case_studies/sec08_experience_distill.md` — 经验三层沉淀
  - `case_studies/sec09_feedback_loop.md` — 反馈回路
  - `case_studies/sec10_7day_mvp.md` — 7 天 MVP
  - `case_studies/sec11_legacy_system.md` — 遗留系统改造
  - `case_studies/sec12_competitor_monitor.md` — 竞品监控
  - 配套 `case_studies/README.md`(目录索引 + 读者复用路径)
  - 注:第 0/1/13/14/15 章是方法论章,不放案例骨架,工具性资产在 `cheatsheet/`

- **4 张一页纸速查表**(可打印贴墙)
  - `cheatsheet/model_selection.md` — 第 1 章三问选型速查
  - `cheatsheet/issue_diagnosis.md` — 第 13 章四类问题诊断速查
  - `cheatsheet/data_source_decision.md` — 第 14 章数据源决策速查
  - `cheatsheet/four_levers.md` — 第 15 章脚手架四杠杆速查

- **53 张原书插图索引**(图片本体仍在原书目录,本仓库 `images/README.md` 提供指针式清单)
  - 涵盖第 0 章(1 张)/ 第 1 章(4 张)/ 第 2 章(4 张)/ 第 3 章(4 张)/ 第 4 章(3 张)/ 第 5 章(3 张)/ 第 6 章(4 张)/ 第 7 章(3 张)/ 第 8 章(3 张)/ 第 9 章(3 张)/ 第 10 章(4 张)/ 第 11 章(4 张)/ 第 12 章(3 张)/ 第 13 章(4 张)/ 第 14 章(3 张)/ 第 15 章(3 张)

- **仓库总入口**:`README.md` + `LICENSE`(CC BY-NC-SA 4.0) + 本更新日志

### 配套说明

- 本仓库与主书 P0/P1 出版项(在主书目录 `promotion/` 下,12 个文件)配套使用
- 出版项包含:推荐序 / 致谢 / 内容简介 / 商标声明 / AI 披露 / 封底文案 / 勘误表 / 元数据 / 图片索引 / 术语表 / 工具表 / 后记

[1.0.0]: #100----2026-08-03
