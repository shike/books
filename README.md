# Books

> 施可的三本书 — 一个统一的 GitHub 文档仓库

这是 [施可 (Shi Ke)](https://shike.github.io/) 全部书籍的统一仓库。三本书从不同视角切入"AI 时代如何做事":

```
        ┌─────────────────────────────┐
        │  ① AI Coding · 人人都是程序员  │  ← 让非技术人用 AI 做出可交付产品
        └──────────────┬──────────────┘
                       ▼
        ┌─────────────────────────────┐
        │  ② FDE · AI 竞赛不在于模型     │  ← 工程师在 AI 项目里做部署交付
        └──────────────┬──────────────┘
                       ▼
        ┌─────────────────────────────┐
        │  ③ WorkBuddy 三部曲           │  ← 管理者用桌面 AI 从个人 → 团队 → 组织
        └─────────────────────────────┘
```

**读者画像演进**:
- **① AI Coding**:创业者 / 产品经理 / 设计师 / 独立顾问 — 任何想用 AI 做出真实产品、但本身并非职业程序员的人
- **② FDE**:CTO / 技术负责人 / 产品经理 / 工程师 / 想转 FDE 的人
- **③ WorkBuddy**:中层及以上管理者 / 带团队用 AI 的人

---

## 📚 三本书数据卡片

| 维度 | ① AI Coding | ② FDE | ③ WorkBuddy |
|---|---|---|---|
| 路径 | [`ai-coding/`](./ai-coding/) | [`fde/`](./fde/) | [`workbuddy/`](./workbuddy/) |
| 章节数 | 16 | 26 + 3 case + 1 附录 | 24(8+8+8) + 18 附录 |
| 字数 | ~18 万 | ~30 万 | 28-34 万 |
| 配图 | 53 张 PNG | 31 张 SVG 封面 | 161 张 PNG(53+56+52) |
| 形态 | 出版(docs)+ 配套数字仓库 | 出版前(HTML) | 出版前(第一卷 review) + 培训交付件 |
| 状态 | ✅ 已发布 | 🟡 待出版 | 🟡 第一卷 review,二三卷写中 |

---

## 🗂 顶层目录

```
books/
├── README.md                ← 本文件(三本书统一入口)
├── INDEX.md                 ← 跨书主题对照(读者按需挑选)
├── LICENSE                  ← 顶层许可证(继承各书 CC BY-NC-SA 4.0)
├── .gitignore               ← 顶层忽略规则
├── ai-coding/               ← ① AI Coding:人人都是程序员
│   ├── README.md            # 项目入口
│   ├── AGENTS.md            # 写作规范
│   ├── chapters/            # 16 章
│   ├── figures/             # 53 张配图
│   ├── appendix/
│   ├── promotion/           # 18 件营销/出版物料
│   ├── assets/              # 配套数字仓库(可独立发布)
│   ├── scripts/             # 工具脚本
│   └── dist/                # 已构建发布件(main.md + main.docx)
├── fde/                     ← ② FDE:AI 竞赛不在于模型
│   ├── README.md
│   ├── AGENTS.md
│   ├── chapters/            # 26 章(带中文标题)
│   ├── figures/             # 31 张 SVG
│   ├── appendix/            # 4 件
│   ├── scripts/
│   └── dist/html/           # 32 个 HTML(可读版)
└── workbuddy/               ← ③ WorkBuddy 三部曲
    ├── README.md
    ├── AGENTS.md
    ├── SERIES-PLAN.md
    ├── 第一卷/              # 8 章 + 序/目录/勘误
    ├── 第二卷/              # 8 章
    ├── 第三卷/              # 8 章
    └── 培训物料/            # 衍生物料(企业培训交付件)
        ├── Vol1/ Vol2/ Vol3/
        ├── 学员手册/
        ├── 讲师手册/
        ├── 题库.md
        ├── 认证体系.md
        └── ...
```

---

## 🚀 快速开始

### 我该从哪本开始?

按你的角色挑书:

| 我是谁 | 推荐阅读顺序 |
|---|---|
| 我不是程序员,想用 AI 做产品 | ① AI Coding → ③ WorkBuddy 第一卷 |
| 我是工程师,在做 AI 项目 | ② FDE → ① AI Coding(看产品视角) |
| 我是团队管理者,想带团队用 AI | ③ WorkBuddy 全三卷 → ② FDE(看组织视角) |
| 我是创业者,什么都想干 | ① AI Coding → ② FDE → ③ WorkBuddy 第一卷 |

### 详细主题对照

见 [INDEX.md](./INDEX.md) — 按"提示词工程 / RAG / Agent / 评估 / 上线运维 / 团队落地 / 组织变革"等主题,在三本书里找相关内容。

---

## 🛠 仓库约定

### 统一子目录结构(每本书)

```
<book>/
├── README.md               # 项目入口
├── AGENTS.md               # 写作规范
├── chapters/               # 章节 md
├── figures/                # 配图
├── appendix/               # 附录
├── promotion/              # 营销/出版物料
├── assets/                 # 配套资源
├── scripts/                # 工具脚本
└── dist/                   # 已构建发布件
```

### 跨书命名一致性

- 章节:`chapters/NN-标题.md`(两位章号,中文标题)
- 配图:`figures/<原命名>`(不强制重命名,避免破坏引用)
- 引用:`![](相对路径)`
- 顶层:`README.md` + `AGENTS.md` 每本都有
- 备份:原 `README.md` 备份为 `README.original.md.bak`(被 .gitignore 忽略)

### 原仓库关系

- **`ai-coding/` 目录** ← 来源:`shike/ai_coding_book`(原仓库保留)
- **`fde/` 目录** ← 来源:`shike/FDE-AI-race-isn-t-won-on-models`(原仓库保留)
- **`workbuddy/` 目录** ← 来源:`workbuddy-books/`(本地目录,首次入 git)

原仓库与本仓库**互不影响**,可独立更新、发布。本仓库作为统一聚合 + 跨书主题入口。

---

## 📜 许可证

本仓库整体采用 **CC BY-NC-SA 4.0**(署名-非商业-相同方式共享)。各书内部可能附加更细的许可声明,见对应书的 `assets/LICENSE` 或 `README.md`。
