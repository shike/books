# AI Coding：人人都是程序员 — 配套数字资源

> 本仓库是《**AI Coding：人人都是程序员**》一书的**可执行资产**集合。
> 原书方法论、案例现场与延伸阅读见主书；本仓库只放**读者可直接复制、可立即执行**的内容。
>
> 📖 **作者**:[施可 (Shi Ke)](https://shike.github.io/) — 水滴跃动 Dropleap 创始人 / 前邻汇吧 COO / 中科大软工硕士
> 📧 联系:shike@dropleap.cn
> 🔗 主页:https://shike.github.io/
> 🐙 GitHub:https://github.com/shike

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Prompts](https://img.shields.io/badge/prompts-16-blue.svg)](prompts/)
[![Case Studies](https://img.shields.io/badge/case_studies-11-green.svg)](case_studies/)
[![Cheatsheet](https://img.shields.io/badge/cheatsheet-4-orange.svg)](cheatsheet/)
[![Images](https://img.shields.io/badge/images-53-purple.svg)](images/)

---

## 📚 这本书是什么

**《AI Coding：人人都是程序员 — 让非技术人做出可交付的产品》**

不是"如何向 AI 提问"的书,而是"如何让 AI 替你交付一个真实、可收款、可维护的产品"的方法论。

| 维度 | 数据 |
|------|------|
| 案例章 | 10 个真实项目复盘(消费级 / 企业级 / 前沿) |
| 方法论章 | 4 类反复发作的工程问题 + 1 套脚手架方法 |
| 完整提示词 | 16 个(每章 1 个,可直接复制) |
| 引用来源 | 200+ 条(均经过二次核验) |
| 插图 | 53 张 |
| 数据截止 | 2026-07-31 |

**读者画像**:创业者(尤其一人公司)、产品经理、运营负责人、设计师、独立顾问、自媒体作者 — 任何想用 AI 做出真实产品、但本身并非职业程序员的人。

---

## 🎯 这个仓库是什么

本仓库是这本书的**数字附件**,把原书里的"完整提示词""案例骨架""速查表"提取出来,做成可以**直接复制**的资产。

读者读原书时,可以扫封底二维码(主书最后页)进入本仓库,复制资产,落地实操。

### 4 个核心资源

| 目录 | 作用 | 适用场景 |
|------|------|----------|
| `prompts/` | 16 个完整提示词(对应原书 16 个「完整提示词」段) | 复制到 AI 工具,作为系统提示 |
| `case_studies/` | 11 个案例骨架(第 2—12 章) | 按"实践步骤"在小项目上跑一遍 |
| `cheatsheet/` | 4 张一页纸速查表(选型/诊断/数据源/四杠杆) | 打印贴墙,日常翻阅 |
| `images/` | 53 张原书插图索引 | 二次引用、二次创作 |

---

## 🚀 快速开始(3 步)

### 第 1 步:让 AI 进入角色(5 分钟)

打开 [`prompts/00_general_baseline.md`](prompts/00_general_baseline.md),把代码块整段复制到你的 AI 工具(Claude / GPT / Gemini / Cursor / Trae 等),作为系统提示发送。

这一步让 AI 知道:
- 它的角色(工程协作 AI)
- 必须遵守的方法论纪律(数据可追溯、决策可复核、任务可回滚、时间成本完整记录)
- 工作方式(任务理解 → 执行 → 汇报)
- 边界(不替用户做最终决策、不假装无所不知)

### 第 2 步:选对应章节的提示词(2 分钟)

从 `prompts/01_three_questions.md` 到 `prompts/15_scaffolding.md` 中,选与你当前任务最相关的章节,叠加在基线之上。

例如:你今天要选 AI 编程工具 → 复制 `01_three_questions.md`;要复刻一个网站 → 复制 `02_clone_website.md`。

### 第 3 步:按案例骨架跑一遍(1-7 天)

打开 `case_studies/` 下对应章节的骨架文件,按"实践步骤"在小项目上跑一遍,记录踩到的坑。

例如:你做的是"复刻网站"项目 → 打开 [`case_studies/sec02_clone_website.md`](case_studies/sec02_clone_website.md),按"目标 → 方法 → 资产 → 步骤 → 坑"五段式跑一遍。

**完成 3 步后,你应产出**:一份自己的项目方案 + 一份「哪些坑踩到了」的复盘笔记。

---

## 📖 完整目录

```
ai_coding_book_assets/
├── README.md                          ← 你正在读的(仓库总入口)
├── LICENSE                            ← CC BY-NC-SA 4.0(施可署名)
├── CHANGELOG.md                       ← 配套资源更新日志
├── prompts.jsonl                      ← 16 个提示词打包(每行 JSON,便于脚本批处理)
│
├── prompts/                           ← 16 个完整提示词(独立 .md)
│   ├── 00_general_baseline.md         ← 前言基线(必读,系统提示)
│   ├── 01_three_questions.md          ← 第 1 章:三问选型
│   ├── 02_clone_website.md            ← 第 2 章:复刻网站
│   ├── 03_clone_saas.md               ← 第 3 章:复刻 SaaS
│   ├── 04_24h_demo.md                 ← 第 4 章:24 小时 Demo 对齐
│   ├── 05_weekly_report.md            ← 第 5 章:经营周报
│   ├── 06_feishu_agent.md             ← 第 6 章:飞书常驻 Agent
│   ├── 07_industry_research.md        ← 第 7 章:行业调研
│   ├── 08_experience_distill.md       ← 第 8 章:经验沉淀
│   ├── 09_feedback_loop.md            ← 第 9 章:反馈回路
│   ├── 10_7day_mvp.md                 ← 第 10 章:7 天 MVP
│   ├── 11_legacy_system.md            ← 第 11 章:遗留系统改造
│   ├── 12_competitor_monitor.md       ← 第 12 章:竞品监控
│   ├── 13_four_issues.md              ← 第 13 章:四类工程问题
│   ├── 14_data_acquisition.md         ← 第 14 章:数据获取
│   └── 15_scaffolding.md              ← 第 15 章:脚手架
│
├── case_studies/                      ← 11 个案例骨架(第 2—12 章)
│   ├── README.md                      ← 案例目录索引 + 读者复用路径
│   ├── sec02_clone_website.md         ← 复刻网站
│   ├── sec03_clone_saas.md            ← 复刻 SaaS
│   ├── sec04_demo_alignment.md        ← Demo 对齐需求
│   ├── sec05_weekly_report.md         ← 经营周报
│   ├── sec06_feishu_agent.md          ← 飞书常驻 Agent
│   ├── sec07_industry_research.md     ← 行业调研
│   ├── sec08_experience_distill.md    ← 经验沉淀
│   ├── sec09_feedback_loop.md         ← 反馈回路
│   ├── sec10_7day_mvp.md              ← 7 天 MVP
│   ├── sec11_legacy_system.md         ← 遗留系统改造
│   └── sec12_competitor_monitor.md    ← 竞品监控
│
├── cheatsheet/                        ← 4 张一页纸速查表
│   ├── model_selection.md             ← 第 1 章选型决策树
│   ├── issue_diagnosis.md             ← 第 13 章四类问题 + 20 条仓库自检
│   ├── data_source_decision.md        ← 第 14 章数据源四问
│   └── four_levers.md                 ← 第 15 章四杠杆 + 20 条自检
│
└── images/                            ← 53 张原书插图索引
    └── README.md                      ← 图片清单(实际 PNG 在原书目录)
```

---

## 📑 引用规范

主书所有引用清单见原书末尾(出版后由出版社提供页码),本仓库不重复。

本仓库内的可执行资产(提示词 / 案例骨架 / 速查表),可以被读者:

- ✅ **自由复制** — 用于个人学习、内部团队、非商业项目
- ✅ **自由修改** — 按自己的场景定制
- ✅ **自由分发** — 保留原作者署名、相同方式共享即可
- ❌ **不可商用** — 商业使用需联系版权人(shike@dropleap.cn)

详细条款见 [`LICENSE`](LICENSE)(CC BY-NC-SA 4.0)。

---

## 📛 命名约定

- 章节号 `0` = 前言,`1` = 第 1 章,以此类推
- `prompts/NN_xxx.md` 中 `NN` = 章节号(`00`—`15`)
- `case_studies/secNN_*.md` 中 `secNN` = 第 NN 章
- `cheatsheet/*.md` 用英文短描述命名
- 全部使用小写英文 + 下划线,便于脚本批处理

---

## 💬 贡献与反馈

- **作者**:[施可 (Shi Ke)](https://shike.github.io/)
- **作者邮箱**:shike@dropleap.cn
- **作者主页**:https://shike.github.io/
- **作者 GitHub**:https://github.com/shike
- **微信**:扫下方二维码加好友,备注"读者群"

<img src="wechat_qr.png" alt="施可个人微信二维码" width="180" />

- **勘误**:见主书 `promotion/corrections.md`;新发现的错误可直接发 [Issue](https://github.com/shike/ai-coding-book/issues)
- **配套主书 P0/P1 出版项**:见主书目录 `promotion/`(13 个文件:推荐序 / 致谢 / 简介 / 商标声明 / AI 披露 / 封底 / 勘误表 / 元数据 / 作者介绍 / 图片索引 / 术语表 / 工具表 / 后记)

---

## 📄 许可证

本仓库采用 **CC BY-NC-SA 4.0** 许可证 — 非商业使用、相同方式共享。

```
版权人:施可 (Shi Ke) <shike@dropleap.cn>
年份:2026
```

完整条款:https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

如需超出本许可证范围的授权(例如商业使用授权),请联系版权人。

---

## 🗓️ 更新日志

详见 [`CHANGELOG.md`](CHANGELOG.md)。
