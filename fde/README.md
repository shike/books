# FDE:AI 竞赛不在于模型

> 一本写给 AI 项目一线人员的书。不是关于"用哪个模型"——是关于"模型之外的那些事"。

**作者**:[施可 (Shi Ke)](https://shike.github.io/) — 水滴跃动 Dropleap 创始人
**联系**:shike@dropleap.cn | [主页](https://shike.github.io/) | [GitHub](https://github.com/shike)
**数据截止**:2026-07-28

---

## 📖 关于这本书

AI 项目的胜负,不在选哪个模型,而在**部署**这个环节。

模型能力会趋同。GPT-4、Claude、Gemini、Qwen、DeepSeek——半年后都能做对方能做的事。PoC 谁都能做,差距产生在:

- 能不能蹲到客户现场看到真问题,而不是听需求会上说的
- 能不能把 PoC 推进到产品化,而不是停在 demo 视频
- 上线后能不能扛住真实流量、沉默故障、组织漂移
- 能不能让业务方真的用起来、离不开

本书围绕这条主线展开。所有内容来自一线项目里的真实场景,不是咨询报告里的"最佳实践"。

## 适合谁读

- **CTO / 技术负责人**:要在 AI 项目里做 Go/No-Go 判断、分配资源的人
- **产品经理 / 业务负责人**:要把 AI 真正落进业务流,而不是做一个 demo 出来汇报的人
- **想做 FDE 这条路的人**:想从后方研发转向前线交付的工程师
- **正在做 AI 项目的工程师**:想理解"模型之外"那些事为什么决定项目生死的人

不适合:想找"用 X 框架 3 步搞定 AI 应用"教程的人。这本书不教怎么用框架。

---

## 📊 数据卡片

| 维度 | 数据 |
|---|---|
| 章数 | 26 章正文 + 3 个 case study + 1 个综合附录 |
| 字数 | ~30 万字 |
| 配图 | 31 张 SVG 封面(每章一图) |
| 篇章结构 | 4 篇:认知 → 侦察 → 推进 → 反挫 |

---

## 🗂 目录结构

```
fde/
├── README.md                  ← 本文件
├── AGENTS.md                  ← 写作规范(给 AI 协作者)
├── chapters/                  ← 26 章正文(带中文标题命名)
│   ├── 01-FDE 不是部署工程师.md
│   ├── 02-PoC 地狱.md
│   └── ... ~ 26-法律 AI:当精确的定义完全不同.md
├── figures/                   ← 31 张 SVG 封面图
│   ├── chapter-01.svg
│   ├── chapter-02.svg
│   └── ... ~ case-study-03.svg
├── appendix/                  ← 附录(4 件)
│   ├── 00-main.md             ← 综合附录
│   └── case-studies/
│       ├── case-study-01.md   ← 医疗 AI
│       ├── case-study-02.md   ← 金融 AI
│       └── case-study-03.md   ← 政务 AI
├── promotion/                 ← 营销文案(暂无,出版前需补)
├── assets/                    ← 配套资源(暂无,根据需要补)
├── scripts/                   ← 工具脚本
│   ├── build_html.py
│   └── generate_covers.py
└── dist/                      ← 已构建的发布件
    └── html/                  ← 32 个 HTML(章节 + case + 附录)
        ├── chapter-01.html
        ├── ...
        ├── case-study-01.html
        └── appendix.html
```

---

## 📑 篇章大纲

### 第一篇 | 认知(第 1-4 章)
FDE 是什么、不是什么;项目为什么在 PoC 阶段死;"够好"为什么是工程气概;什么时候根本不该用 AI。

### 第二篇 | 侦察(第 5-8 章)
需求挖掘、问题翻译、决策验证、期望管理。前线工作的核心动作。

### 第三篇 | 推进(第 9-18 章)
模型与提示词、RAG、Agent、评估、成本、上线、运维、故障、复盘——把 PoC 推到产品的全过程。

### 第四篇 | 反挫(第 19-26 章)
FDE 的能力建设 + 7 个垂直行业(医疗/金融/制造/政务/教育/法律)的反挫案例。

---

## ✅ 当前已就绪的发布件

| 件 | 状态 | 位置 | 用途 |
|---|---|---|---|
| 主书 PDF | ✅ | `dist/main.pdf` | 阅读、打印、出版前 review |
| HTML 版本(32 个) | ✅ | `dist/html/` | 在线阅读(打开 chapter-XX.html) |
| 章节源(26 章) | ✅ | `chapters/NN-标题.md` | 维护、修改 |
| 案例研究(3 个) | ✅ | `appendix/case-studies/` | 配套深度阅读 |
| 附录 | ✅ | `appendix/00-main.md` | 综合工具/清单 |
| 封面 SVG(31 张) | ✅ | `figures/` | HTML 渲染、PPT 使用 |
| 工具脚本 | ✅ | `scripts/`、`../../scripts/build_book_pdf.py` | 重新构建 HTML / 重新生成封面 / 重新生成 PDF |

## 🟡 已知缺口(可后续补齐)

- **主书合并版(markdown)**:目前只有 26 个分章节,无合并版 md(类似 ai-coding 的 `dist/main.md`)
- **DOCX / EPUB / PDF**:均未生成
- **推广营销文案**(`promotion/` 为空):出版/自荐需要
- **配套案例音频/视频**:可选
- **勘误区**:暂未建立(可建 `errata/` 目录)

---

## 🚀 快速使用

### 在线阅读
- PDF:打开 `dist/main.pdf`
- HTML:打开 `dist/html/chapter-01.html`,按章节顺序阅读

### 重新构建 HTML
```bash
python3 scripts/build_html.py
```

### 重新生成 PDF
```bash
python3 ../../scripts/build_book_pdf.py fde
```

### 重新生成封面
```bash
python3 scripts/generate_covers.py
```

---

## 📜 许可证

待定(出版前需明确)。建议与 ai-coding 对齐:**CC BY-NC-SA 4.0**。
