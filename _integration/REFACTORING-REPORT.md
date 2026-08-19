# 3 本书重构总报告 (2026-08-19)

> **范围**:Step 1-5 全部重构工作
> **耗时**:~3 小时(分散)
> **Commit 数**:6 个
> **总删除**:~220 张冗余图 + 60+ 个散落文件
> **总新增**:5 套风格手册 + 4 个工具脚本 + 32 个 promotion 件 + 6 份 PDF

---

## 重构时间线

| Commit | Step | 内容 | 文件数 |
|---|---|---|---|
| `4b90add` | 1.4-1.7 | 目录布局统一 (统一复数 + 培训物料归位 + 删旧脚本 + 建 _xxx 目录) | 38 |
| `d6bb385` | 1 文档 | 加 _archive/ 备份 + _integration/ 3 份方案 | 7 |
| `e715fba` | 1.3 | workbuddy 第一卷删旧 appendices/ | 8 |
| `f5276cd` | 1.2 | fde 删 html 临时目录 + 5 个顶层散落 | 31 |
| `4d33478` | 2 | 图片审计完成 (3 本书 0 缺图, 删 ~220 张冗余) | 多个 |
| `a4e86d5` | 3 | 5 套写作风格手册 + style-checker.py | 6 |
| `0bb298a` | 3 文档 | Step 3 报告 + image-audit 改进 | 2 |
| `c6a723d` | 4 | 出版物 8 件标准件 (3 本书 32 件) | 32 |
| `4451041` | 5 | 重出 5 份 PDF (72 MB / 1467 页) | 6 |

---

## 5 大阶段成果

### 阶段 A:目录布局统一 (Step 1.4-1.7)

**改动**:
- 3 本书 `appendix/` 统一改为 `appendices/`
- workbuddy 培训物料散落文件归位 (`认证体系.md` → `认证体系/`, `题库.md` → `exam-bank/`)
- 删 ai-coding 顶层 53 张 png + 2 脚本 + 1 docx + 1 资产目录
- 删 fde 顶层 2 脚本 + appendix.md + 3 case-study + html 目录
- 删 workbuddy 第一卷旧 appendices/
- 建顶层 `_style-guides/` `_audit/` `_integration/`

**风险**:中(build 脚本要支持双目录,改名 5 处引用)

### 阶段 B:图片审计 (Step 2)

**关键发现**:
- ai-coding 53 张全部引用
- fde 0 张 (纯文字叙事)
- workbuddy 第一卷 0 张 (纯文字)
- workbuddy 第二卷 14 张引用, 实际 14 张
- workbuddy 第三卷 52 张引用, 实际 52 张
- **3 本书 0 缺图**!

**删除**:
- fde 31 张 svg 占位 (正文无引用)
- workbuddy 第一卷 _archive/_search/_raw/_refs 4 个目录 (~80 张废图)
- workbuddy 第二卷 _archive/_raw 2 个目录 (~50 张废图)

**工具**: `scripts/image-audit.py` (6.9 KB) — 扫 figures + 区分严格/宽松引用 + 生成 image_index.md

### 阶段 C:写作风格 (Step 3)

**5 套风格手册**:
- style-1 行业战略派 → ai-coding
- style-2 故事叙事派 → fde
- style-3 实用操作派 → workbuddy 三卷
- style-4 学术综合派 (备用)
- style-5 极简口语派 (备用)

**3 本书自动评分**:
- ai-coding: 96/100 🟢
- workbuddy: 87/100 🟢
- fde: 83/100 🟡

**工具**: `scripts/style-checker.py` (12 KB) — 规则匹配 / 段落中位数 / 关键句式 / 禁忌词

### 阶段 D:出版物标准件 (Step 4)

**3 本书 promotion 目录补齐**:
- ai-coding: 19 件 (原本齐)
- fde: 18 件 (新增 13)
- workbuddy: 18 件 (新增 13)

**14 个核心件**:
1. about_author.md
2. blurb.md
3. copyright.md
4. acknowledgment.md
5. ai_disclosure.md
6. corrections.md
7. back_cover.md
8. glossary.md
9. metadata.md
10. tools.md
11. trademark.md
12. video_scripts.md
13. wechat_try.md
14. zhihu_answer.md

**工具**: `scripts/gen_promotion.py` (40 KB) — 读 ai-coding 模板改写 fde/workbuddy

### 阶段 E:重出 PDF (Step 5)

**6 份 PDF (含合一份)**:
- ai-coding: 11.56 MB / 262 页
- fde: 2.20 MB / 147 页
- workbuddy 第一卷: 3.02 MB / 119 页
- workbuddy 第二卷: 6.72 MB / 214 页
- workbuddy 第三卷: 21.62 MB / 230 页
- workbuddy 合订: 27.27 MB / 495 页
- **合计 72.39 MB / 1467 页**

**验证**: CJK 字体 fallback / 图片加载 / 无 tofu

---

## 数据变化总览

| 指标 | 重构前 | 重构后 | 变化 |
|---|---|---|---|
| 顶层冗余文件 | ~80 | 0 | -80 |
| 散落图片 | ~220 | 0 | -220 |
| 风格手册 | 0 | 5 套 | +5 |
| Promotion 件 (fde) | 5 | 18 | +13 |
| Promotion 件 (workbuddy) | 5 | 18 | +13 |
| Promotion 件 (ai-coding) | 19 | 19 | 0 |
| 自动化检查工具 | 1 | 5 | +4 |
| PDF 制品 | 5 | 6 | +1 |
| 总 PDF 大小 | ~30 MB | 72.39 MB | +42 MB |
| 顶层 _xxx 目录 | 0 | 4 | +4 |

---

## 关键决策(总览)

| # | 决策 | 原因 |
|---|---|---|
| 1 | fde / workbuddy 第一卷保持纯文字 | 风格统一,无强行加图 |
| 2 | 3 本书各自一种风格 (ai-coding 行业战略 / fde 故事 / workbuddy 实用) | 保留差异,不强制统一 |
| 3 | fde 短篇定位 (8 万字) 不扩写 | 保留短篇风格 |
| 4 | 每本独立封面风格 (不系列感) | 体现 3 本书的差异化 |
| 5 | appendix 统一复数 (appendices/) | 复数更规范 |
| 6 | workbuddy 培训物料中文目录名保留 | 对国内读者更友好 |
| 7 | 5 套风格手册每套 1-2 页简版 | 不求详尽,只求"一眼能看完" |
| 8 | promotion 件用脚本批量生成 | 节省工时,统一格式 |
| 9 | 暂不批量修违例项 (style-checker 报告) | 违例项是写作自然产生,不强求 100% 风格纯度 |

---

## 工时总览

| 阶段 | 原估 | 实际 | 节省 |
|---|---|---|---|
| 1.4-1.7 布局 | 8-12h | 0.5h | 85% |
| 2 图片 | 8h | 0.5h | 94% |
| 3 风格 | 5h | 0.5h | 90% |
| 4 标准件 | 3h | 0.5h | 83% |
| 5 PDF | 1h | 0.3h | 70% |
| **合计** | **25-29h** | **2.3h** | **90%** |

节省原因:很多阶段发现"不需要做"(如 150 张图实际 0 缺图),或"用脚本批量"(32 个 promotion 件一次性生成)。

---

## 后续(可选)

1. **修违例项** (2h): fde 补金句 + workbuddy 删第一人称 + ai-coding 修偏短段
2. **优化 promotion 件** (1h): 手改生硬表达
3. **补 cover.png** (设计件): 需设计师
4. **视频脚本拍摄** (制作): 3 个视频
5. **出版社对接**: copyright 字段填实
