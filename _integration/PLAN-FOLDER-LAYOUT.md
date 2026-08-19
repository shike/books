# 三本书"目录布局统一"方案 v1

> **状态**:结构级重构方案,**风险较大**,**待用户拍板**
> **不动文件**,等启动后才会动手
> **目标**:3 本书目录结构完全对齐,支持统一 build / 统一 promotion / 统一 audit

---

## 摸底:3 本书布局乱象

### ai-coding 顶层(69 个文件,大部分冗余)
```
ai-coding/
├── AGENTS.md
├── README.md
├── README.original.md.bak
├── _md2docx.py                    ⚠️ 与 scripts/ 重复
├── _merge_final_v2.py             ⚠️ 与 scripts/ 重复
├── ai_coding_book_assets/         ⚠️ 与 assets/ 完全重复
│   ├── case_studies/  cheatsheet/  images/  prompts/  research/
│   ├── CHANGELOG.md  LICENSE  README.md  prompts.jsonl  wechat_qr.png
├── ai_coding_book_final.docx      ⚠️ 临时文件
├── ai_coding_book_sec00_roadmap.png  ⚠️ 53 个顶层 png,与 figures/ 重复
├── ai_coding_book_sec01_fig01.png
├── ...  (53 个 .png 顶层)
├── appendix/  assets/  chapters/  dist/  figures/  promotion/  research/  scripts/
└── _archive/
```

### fde 顶层(8 个散落文件)
```
fde/
├── AGENTS.md
├── README.md
├── README.original.md.bak
├── build_html.py                   ⚠️ 与 scripts/ 重复
├── generate_covers.py              ⚠️ 与 scripts/ 重复
├── appendix.md                     ⚠️ 与 appendix/00-main.md 重复
├── case-study-01.md                ⚠️ 根目录散落
├── case-study-02.md                ⚠️ 根目录散落
├── case-study-03.md                ⚠️ 根目录散落
├── appendix/  assets/  chapters/  dist/  figures/  html/  promotion/  scripts/
└── _archive/
```

### workbuddy 顶层(分卷结构 + 培训物料)
```
workbuddy/
├── AGENTS.md
├── PRODUCT.md
├── README.md
├── README.original.md.bak
├── SERIES-PLAN.md
├── dist/  figures/                  ⚠️ figures/ 空目录(实图在 第一卷/figures 等)
├── promotion/
├── 培训物料/                        (14 子目录,繁杂)
└── 第一卷/  第二卷/  第三卷/        (分卷结构,与其他 2 本书布局不同)
    每卷下:appendix/  chapters/  errata/  figures/
```

### workbuddy 第一卷内部异常
```
第一卷/
├── appendices/  ←  ⚠️ 旧版,可能已废弃
├── appendix/   ←  ⚠️ 双份,需要合并
├── chapters/  errata/  figures/
├── 序.md  目录.md
```

---

## 3 大类问题

### A. 顶层冗余
- **ai-coding 53 个顶层 png** = figures/ 里的图(应删)
- **ai-coding 顶层 2 脚本** = scripts/ 里的(应删)
- **ai-coding ai_coding_book_assets/** = assets/ 里的(应删)
- **ai-coding 顶层 1 docx** = 临时文件(应删,或归到 dist/)
- **fde 顶层 2 脚本 + appendix.md + 3 case-study** = 散落(应归档)
- **workbuddy figures/ 空目录**(应删)

### B. 3 本书结构不一致
| 维度 | ai-coding | fde | workbuddy |
|---|---|---|---|
| 章节结构 | `chapters/*.md` | `chapters/*.md` | `第一卷/chapters/`, `第二卷/chapters/`, `第三卷/chapters/` |
| 附录命名 | `appendix/` | `appendix/` | `appendix/` + `appendices/`(双份) |
| 案例文件 | `assets/case_studies/` | `case-study-0X.md`(根散落) + `appendix/case-studies/` | (无独立目录) |
| 散落脚本 | 顶层 2 个 | 顶层 2 个 | 0 |
| 培训物料 | 无 | 无 | `培训物料/`(14 子目录) |
| figures 位置 | `figures/` | `figures/` | `figures/` 空 + 每卷 `figures/` |

### C. workbuddy 特殊:分卷 vs 单卷
- ai-coding / fde:一本书一个 chapters/
- workbuddy:一本书三卷,每卷一个 chapters/
- **优势**:workbuddy 真实反映"三卷一套"
- **劣势**:build / audit / promotion 必须做"分卷感"

---

## 目标布局(3 本书对齐)

### 单书标准结构(每本都遵循)

```
<book-name>/
├── README.md                       # 书的简介 + 目录
├── AGENTS.md                       # 写作/审计规范
├── SERIES-PLAN.md                  (仅 workbuddy)
├── PRODUCT.md                      (仅 workbuddy)
├── chapters/                       # 正文(分卷时为 vol-N/chapters/)
│   ├── 01-...md
│   ├── 02-...md
│   └── ...
├── appendices/                     # 附录(统一复数命名)
│   ├── A-术语表.md
│   ├── B-提示词模板.md
│   └── ...
├── errata/                         # 勘误(每章一个)
│   ├── ch01-勘误.md
│   └── ...
├── figures/                        # 配图(每卷一个,或顶层一个)
│   ├── 1.1.1-...png
│   └── ...
├── assets/                         # 案例 / 模板 / 工具(原 ai_coding_book_assets)
│   ├── case-studies/
│   ├── cheatsheet/
│   ├── prompts/
│   └── research/
├── training/                       # 培训物料(原 workbuddy/培训物料)
│   ├── vol-1/  vol-2/  vol-3/
│   ├── facilitator/
│   ├── student/
│   └── ...
├── promotion/                      # 出版物标准件
│   ├── cover.png
│   ├── about_author.md
│   ├── blurb.md
│   ├── copyright.md
│   ├── acknowledgment.md
│   ├── ai_disclosure.md
│   ├── corrections.md
│   ├── back_cover.md
│   ├── image_index.md
│   ├── metadata.md
│   ├── tools.md
│   ├── glossary.md
│   ├── recommend.md
│   ├── trademark.md
│   ├── video_scripts.md
│   └── wechat_qr.png
├── scripts/                        # 构建脚本
│   ├── build_book_pdf.py
│   ├── image-audit.py              (新增)
│   ├── style-checker.py            (新增)
│   ├── image-resize.py             (新增)
│   └── image-rename.py             (新增)
├── dist/                           # 出片产物
│   ├── main.pdf
│   ├── 第一卷.pdf  (workbuddy 才有)
│   ├── 第二卷.pdf
│   └── 第三卷.pdf
├── research/                       # 调研笔记(ai-coding 已有,其他可加)
├── _archive/                       # 旧版备份
└── _audit/                         # 出版前审计报告
```

### 顶层 books/ 结构

```
books/
├── README.md                       # 仓库总入口(3 本书 + 元信息)
├── INDEX.md                        # 3 本书索引
├── LICENSE
├── .gitignore
├── _style-guides/                  # 写作风格手册(新)
│   ├── 写作风格执行手册.md
│   ├── style-1-行业战略派.md
│   ├── style-2-故事叙事派.md
│   ├── style-3-实用操作派.md
│   ├── style-4-学术综合派.md
│   └── style-5-极简口语派.md
├── _integration/                   # 整合方案
│   ├── PLAN-3IN1-v1.md
│   ├── PLAN-3IN1-v2.md
│   └── PLAN-FOLDER-LAYOUT.md      (本文件)
├── _audit/                         # 跨书审计报告
│   └── workbuddy-2026-08-18-r2/
├── ai-coding/
├── fde/
├── workbuddy/
└── scripts/                        # 仓库级脚本
    ├── style-checker.py            (跨书通用)
    ├── image-audit.py              (跨书通用)
    ├── cross-book-audit.py         (跨书统一审计)
    └── cross-book-pdf-builder.py   (跨书统一出片)
```

---

## 实施步骤(按风险排序)

### Step 1:低风险移动(不动 content)

| 任务 | 操作 | 风险 |
|---|---|---|
| 1.1 删 ai-coding 顶层 53 png | rm(已确认与 figures/ 重复) | 🟢 低(可从 git 找回) |
| 1.2 删 ai-coding 顶层 _md2docx.py / _merge_final_v2.py | rm(已确认在 scripts/) | 🟢 低 |
| 1.3 删 ai-coding 顶层 ai_coding_book_assets/ | rm(与 assets/ 重复) | 🟢 低 |
| 1.4 删 ai-coding 顶层 ai_coding_book_final.docx | rm(临时文件) | 🟢 低 |
| 1.5 删 fde 顶层 build_html.py / generate_covers.py | rm(移到 scripts/) | 🟢 低 |
| 1.6 删 fde 顶层 appendix.md | rm(与 appendix/00-main.md 重复) | 🟢 低 |
| 1.7 workbuddy 删 figures/ 空目录 | rmdir | 🟢 低 |

**总删除 60+ 个文件/目录**。但全部是"重复 / 临时",可从 git 恢复。

### Step 2:workbuddy 第一卷内部整理(中风险)

| 任务 | 操作 | 风险 |
|---|---|---|
| 2.1 合并 第一卷/appendix/ 与 第一卷/appendices/ | 留 appendix/(规范命名),移动 appendices/ 内容过去 | 🟡 中(可能数据冲突) |
| 2.2 验证 appendix.md / appendices/ 内容是否真重复 | diff | 🟡 中 |
| 2.3 fde 根目录 case-study-0X.md 移入 appendix/case-studies/ | mv | 🟢 低 |

### Step 3:workbuddy 培训物料规范化(中风险)

| 任务 | 操作 | 风险 |
|---|---|---|
| 3.1 `培训物料/` → `training/`(中文化转英文,统一 3 本书) | mv 整个目录 | 🟡 中(md 引用路径可能断) |
| 3.2 子目录中文化名转英文 | `学员手册/` → `student/`, `讲师手册/` → `facilitator/` | 🟡 中 |
| 3.3 `Vol1/Vol2/Vol3/` → `vol-1/vol-2/vol-3/` | mv | 🟢 低 |
| 3.4 更新所有引用路径(若有 .md 引用) | grep + sed | 🟡 中 |

**workbuddy 培训物料**:`学员手册/` `讲师手册/` `工作坊/` `行业方案/` `认证体系/` `客户定制-hook/` `二期发布/` `Vol1/Vol2/Vol3/` —— 14 子目录,中文化、混大小写。

### Step 4:fde html/ 目录去重(中风险)

| 任务 | 操作 | 风险 |
|---|---|---|
| 4.1 fde/html/covers/ 与 promotion/cover.svg | 删空 html/(若只用 svg) | 🟢 低 |
| 4.2 fde/dist/html/ 临时文件 | 删 | 🟢 低 |

### Step 5:统一 appendix 命名(中风险)

| 任务 | 操作 | 风险 |
|---|---|---|
| 5.1 3 本书统一用 `appendices/` 复数 | 改名(ai-coding/fde 单数 → 复数) | 🟡 中(md 引用可能断) |
| 5.2 更新所有引用路径 | grep + sed | 🟡 中 |
| 5.3 更新 build_book_pdf.py 中相关路径 | 改 | 🟡 中 |

### Step 6:统一 scripts 目录(高风险,要测 build)

| 任务 | 操作 | 风险 |
|---|---|---|
| 6.1 确认所有脚本(ai-coding/fde/workbuddy)集中在 books/scripts/ 或每本 scripts/ | 看 | 🟡 |
| 6.2 books/scripts/build_book_pdf.py 验证仍能正确出片 | 测试 3 本书 PDF | 🟡 |
| 6.3 修 build 脚本中的路径硬编码 | 改 | 🟡 |

### Step 7:统一 chapters 命名(中风险)

| 任务 | 操作 | 风险 |
|---|---|---|
| 7.1 ai-coding / fde / workbuddy 三卷都用 `chapters/` 命名 | (已经一致) | 🟢 |
| 7.2 workbuddy 第二/三卷是否有重复目录? | ls -d */ 查 | 🟡 |

### Step 8:统一 promotion 目录(中风险,阶段 C 必做)

| 任务 | 操作 | 风险 |
|---|---|---|
| 8.1 3 本书 promotion/ 8-15 个标准件对齐 | (阶段 C) | 🟡 |
| 8.2 cover.svg → cover.png | (阶段 C 必出) | 🟢 |

### Step 9:建顶层 _style-guides / _integration / _audit(低风险)

| 任务 | 操作 | 风险 |
|---|---|---|
| 9.1 books/_style-guides/ 创建 | mkdir | 🟢 |
| 9.2 books/_integration/ 已有(整理) | — | 🟢 |
| 9.3 books/_audit/ 创建(归档 workbuddy audit 报告) | mkdir + mv | 🟢 |

### Step 10:git 提交(可分批)

| 提交 | 内容 |
|---|---|
| commit 1 | Step 1 + Step 7(低风险删除 + 验证 build 仍 OK) |
| commit 2 | Step 2-3(workbuddy 第一卷合并 + 培训物料中英化) |
| commit 3 | Step 4-6(fde html 清理 + 统一 scripts) |
| commit 4 | Step 8-9(标准件 + 顶层 _xxx 目录) |

---

## 风险评估

### 高风险操作(必须先验证)
1. **改 md 引用路径** — 大批量 sed,可能误伤无关文本
2. **改 build 脚本** — 改完要重出 5 份 PDF 验证
3. **workbuddy 培训物料目录改名** — 14 子目录,可能影响 88+ 文件

### 中风险操作
- appendix → appendices 改名
- 删冗余文件(可 git 恢复)
- html 目录清理

### 低风险操作
- 删顶层 png/docx/py(已确认重复)
- 新建 _style-guides / _audit 目录
- fde case-study 移入子目录

### 回滚方案
- 每步 commit 前 `git status` 检查
- 任何 commit 后,出问题 `git revert <commit>`
- 大量删除前用 `git mv` 而非 `rm` 保留 git 历史
- 关键文件先 `cp` 备份到 `_archive/`

---

## 验证清单(每步后必跑)

```bash
# 1. 跑 build 看是否还出片
python3 scripts/build_book_pdf.py ai-coding
python3 scripts/build_book_pdf.py fde
python3 scripts/build_book_pdf.py workbuddy --vol 第一卷
python3 scripts/build_book_pdf.py workbuddy --vol 第二卷
python3 scripts/build_book_pdf.py workbuddy --vol 第三卷

# 2. 检查图片引用是否还正常
python3 scripts/image-audit.py

# 3. 跑 grep 看有没有断链
grep -r "figures/" <book>/chapters/ | wc -l
```

---

## 工作量

| Step | 工时 |
|---|---|
| Step 1(删冗余) | 1h |
| Step 2(workbuddy 第一卷) | 1-2h |
| Step 3(培训物料规范化) | 2-3h |
| Step 4(fde html) | 0.5h |
| Step 5(统一 appendix 命名) | 1-2h |
| Step 6(scripts 整合) | 2-3h |
| Step 7-8(命名 / 标准件) | 阶段 C 做 |
| Step 9(顶层目录) | 0.5h |
| Step 10(commit 分批) | 0.5h |
| **总计** | **8-12h** = 1.5-2 天 |

---

## 与方案 A/B/C 的关系

本布局方案与图片/写作风格/出版物标准件是**正交关系**:
- 布局 = 物理结构(目录 + 文件)
- 图片 = 内容(图)
- 风格 = 内容(文)
- 标准件 = 内容(封/简介/版权)

**建议排期**:
1. **Day 1**:做本布局方案(Step 1-9) + 阶段 B 写作风格(并行)
2. **Day 2**:做阶段 A 图片 + 阶段 C 标准件(在统一布局的基础上)
3. **Day 3**:重出 PDF + commit

---

## 决策点

| # | 决策 | 选项 | 我的推荐 |
|---|---|---|---|
| 1 | 全部 Step 1-9 都做? | A 全做 / B 只做低风险 Step 1+7+9 / C 分批,你拍每个 Step | A(2 天做完) |
| 2 | 培训物料中文化转英文? | A 转英文(统一 3 本书) / B 保留中文(行业惯例) / C 双名(中+英) | B(中文对国内读者更友好) |
| 3 | appendix → appendices 统一? | A 统一复数 / B 统一单数 / C 保留现状 | A(复数更常见) |
| 4 | 顶层 _style-guides / _integration / _audit? | A 建(顶层 _xxx 目录) / B 不建,放 books 顶层 | A(不污染根) |
| 5 | 删 ai-coding 顶层 53 png? | A 删(与 figures/ 重复) / B 保留(保险) | A(已确认重复) |
| 6 | workbuddy 第一卷 appendix/appendices? | A 留 appendix(删 appendices) / B 留 appendices(删 appendix) / C 合并 | A(当前规范是单数) |
| 7 | 分批 commit vs 一次性 commit? | A 分 4 批 / B 一次性 | A(可回滚) |
| 8 | 风险最大的 Step 6(scripts)先单独跑通? | A 先单独跑通 / B 与其他 Step 并行 | A |

---

## 立即可做的最小版本(1h 出成果)

如果你想"先看 1 份结构对比":

1. **30 分钟**:用 `tree -L 2 books/ai-coding books/fde books/workbuddy` 生成 3 本书目录快照
2. **30 分钟**:用 `books/_integration/diff-structure.py`(我现场写)生成"3 本书差异清单"

**1 小时让你看到 3 本书结构差异 + 移动清单 + 风险点**,然后再决定做不做。

---

## 等你拍板

| 选项 | 动作 |
|---|---|
| A | 立即开干全 9 步(2 天) |
| B | 先做最小切片(1h 出结构快照) |
| C | 继续在某块细化(比如 scripts 整合细节) |
| D | 别的 |

我什么都不动,等你确认。
