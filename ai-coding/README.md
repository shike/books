# AI Coding:人人都是程序员

> 让非技术人做出可交付的产品

**作者**:[施可 (Shi Ke)](https://shike.github.io/) — 水滴跃动 Dropleap 创始人 / 前邻汇吧 COO / 中科大软工硕士
**联系**:shike@dropleap.cn | [主页](https://shike.github.io/) | [GitHub](https://github.com/shike)
**数据截止**:2026-07-31

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

---

## 📖 关于这本书

**《AI Coding:人人都是程序员》** 不是"如何向 AI 提问"的书,而是"如何让 AI 替你交付一个真实、可收款、可维护的产品"的方法论。

| 维度 | 数据 |
|------|------|
| 案例章 | 10 个真实项目复盘(消费级 / 企业级 / 前沿) |
| 方法论章 | 4 类反复发作的工程问题 + 1 套脚手架方法 |
| 完整提示词 | 16 个(每章 1 个,可直接复制) |
| 引用来源 | 200+ 条(均经过二次核验) |
| 配图 | 53 张 |

**读者画像**:创业者(尤其一人公司)、产品经理、运营负责人、设计师、独立顾问、自媒体作者 — 任何想用 AI 做出真实产品、但本身并非职业程序员的人。

---

## 🗂 目录结构

```
ai-coding/
├── README.md                  ← 本文件(项目入口)
├── AGENTS.md                  ← 写作规范(给 AI 协作者)
├── chapters/                  ← 16 个章节源(可编辑,合并用)
│   ├── 00-chapter.md
│   ├── 01-chapter.md
│   └── ... ~ 15-chapter.md
├── figures/                   ← 53 张原书配图(章节内 ![] 引用 ../figures/xxx)
├── appendix/                  ← 附录(暂无内容,预留)
├── promotion/                 ← 出版/营销文案(18 件)
│   ├── recommend.md
│   ├── blurb.md
│   ├── back_cover.md
│   ├── about_author.md
│   ├── acknowledgment.md
│   ├── corrections.md
│   ├── ai_disclosure.md
│   ├── trademark.md
│   ├── glossary.md
│   ├── epilogue.md
│   ├── cover.png
│   └── ... (工具/视频脚本/图片索引/微信知乎等)
├── assets/                    ← 配套数字仓库(可独立发布)
│   ├── README.md
│   ├── prompts/               ← 16 个完整提示词
│   ├── case_studies/          ← 11 个案例骨架
│   ├── cheatsheet/            ← 4 张一页纸速查表
│   ├── images/                ← 53 张原书插图索引
│   ├── research/              ← 12 篇写作期研究资料(dimension × 12)
│   ├── prompts.jsonl          ← 提示词打包(JSONL)
│   ├── wechat_qr.png
│   ├── LICENSE
│   └── CHANGELOG.md
├── scripts/                   ← 工具脚本
│   ├── _md2docx.py
│   └── _merge_final_v2.py
└── dist/                      ← 已构建的发布件
    ├── main.md                ← 主书源(645KB,合并 16 章节)
    └── main.docx              ← 主书可发布版(7.5MB,docx,28 个分页)
```

> 备注:`chapters/` 用 `NN-chapter.md` 编号;`assets/images/` 是子目录,与顶层 `figures/` 物理分开(后者是章节实际引用的图)。

---

## ✅ 当前已就绪的发布件

| 件 | 状态 | 位置 | 用途 |
|---|---|---|---|
| 主书 PDF | ✅ | `dist/main.pdf` | 阅读、打印、出版前 review |
| 主书 DOCX | ✅ | `dist/main.docx` | 出版社投稿、阅读、打印 |
| 主书 Markdown(合并) | ✅ | `dist/main.md` | 网站/GitBook/在线阅读 |
| 章节源(分章 md) | ✅ | `chapters/00-chapter.md` ~ `15-chapter.md` | 维护、修改、增量更新 |
| 配图(53 张 PNG) | ✅ | `figures/` | 内文配图,可重用 |
| 营销文案(blurb/封底/作者介绍 等) | ✅ | `promotion/` | 出版、自媒体传播 |
| 配套数字仓库(16 提示词 + 11 案例 + 4 速查表) | ✅ | `assets/` | 独立发布的二级产品 |
| 12 篇研究资料 | ✅ | `assets/research/` | 写作底稿,二次出版可引 |
| 工具脚本(合并/转 docx/转 pdf) | ✅ | `scripts/`、`../../scripts/build_book_pdf.py` | 重新构建 dist/ |

## 🟡 已知缺口(可后续补齐)

- **chapter 文件名待优化**:目前为 `NN-chapter.md`,可改为带标题的 `NN-章节标题.md`(类似 FDE/WB 风格,更友好)
- **EPUB** 未生成(Kindle/微信读书等平台需要)
- **配套网站(GitHub Pages)** 未部署
- **PDF**(高质量打印版)未生成
- **勘误持续维护**:见 `promotion/corrections.md`

---

## 🚀 快速使用

### 在线阅读(主书)
打开 `dist/main.pdf` 或 `dist/main.md`(GitHub 会自动渲染)。

### 二次印刷 / 投稿
- 出版社投稿 → `dist/main.docx` 或 `dist/main.pdf`
- 自行排版 → 用 `chapters/00-chapter.md` ~ `15-chapter.md` 在 InDesign/Word 里合成

### 配套仓库单独发布
- 提示词 / 速查表 / 案例骨架 → `assets/` 整个目录可独立打包(已是 CC BY-NC-SA)
- 与主书解耦,读者可免费下载

### 重新构建 dist/
```bash
# 重新生成 PDF(从 chapters/*.md 拼 HTML → Chrome headless)
python3 ../../scripts/build_book_pdf.py ai-coding
```

> 老的 `_merge_final_v2.py` + `_md2docx.py` 内部脚本已废弃(2026-08 重构), 现统一用 `build_book_pdf.py` 出 PDF。

---

## 📜 许可证

本仓库采用 **CC BY-NC-SA 4.0** 许可证 — 署名-非商业-相同方式共享。
详见 [`assets/LICENSE`](./assets/LICENSE)。
