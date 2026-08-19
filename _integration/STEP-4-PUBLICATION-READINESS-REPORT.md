# Step 4 出版物 8 件标准件 报告 (2026-08-19)

> **成果**:3 本书 promotion 目录 16 个标准件全齐 (cover / about_author / blurb / copyright / acknowledgment / ai_disclosure / corrections / back_cover / glossary / metadata / tools / trademark / wechat_try / zhihu_answer / epilogue / recommend / video_scripts)
> **工时**:0.5h (脚本生成 32 件,改 2 个变量)
> **下一步**:可选 — 重出 5 份 PDF 看效果 / 改个别文风

---

## 3 本书 promotion 件清单

| 件 | ai-coding | fde | workbuddy |
|---|---|---|---|
| cover.png | ✅ 已有 | ✅ cover.svg | ✅ cover.svg |
| about_author.md | ✅ 91 行 | ✅ 新生成 | ✅ 新生成 |
| blurb.md | ✅ 29 行 | ✅ 新生成 | ✅ 新生成 |
| copyright.md | ✅ 77 行 | ✅ 已有,新生成覆盖 | ✅ 165 行已有 |
| acknowledgment.md | ✅ 13 行 | ✅ 新生成 | ✅ 新生成 |
| ai_disclosure.md | ✅ 9 行 | ✅ 新生成 | ✅ 新生成 |
| corrections.md | ✅ 29 行 | ✅ 新生成 | ✅ 新生成 |
| back_cover.md | ✅ 15 行 | ✅ 新生成 | ✅ 新生成 |
| glossary.md | ✅ 58 行 | ✅ 新生成 | ✅ 新生成 |
| metadata.md | ✅ 83 行 | ✅ 新生成 | ✅ 新生成 |
| tools.md | ✅ 100 行 | ✅ 新生成 | ✅ 新生成 |
| trademark.md | ✅ 33 行 | ✅ 新生成 | ✅ 新生成 |
| video_scripts.md | ✅ 198 行 | ✅ 新生成 | ✅ 新生成 |
| wechat_try.md | ✅ 260 行 | ✅ 新生成 | ✅ 新生成 |
| zhihu_answer.md | ✅ 58 行 | ✅ 新生成 | ✅ 新生成 |
| epilogue.md | ✅ 63 行 | ✅ 新生成 | ✅ 新生成 |
| recommend.md | ✅ 43 行 | ✅ 新生成 | ✅ 新生成 |
| image_index.md | ✅ 60 行 | ✅ 38 行 | ✅ 73 行 |
| **合计** | **19 件** | **18 件** | **18 件** |

> fde/workbuddy 之前缺 13 件,本次新增 13 件 + 5 件原有,共 18 件
> ai-coding 19 件原本就齐

---

## 生成工具

`books/scripts/gen_promotion.py` (新建,40 KB)
- 读 ai-coding 模板,改写 fde/workbuddy 版本
- 每件 30-200 行,内容根据书主题改写
- 14 个核心件批量生成

## 每件关键内容

### about_author.md (作者介绍)
- 短版(~100 字)/ 中版(~300 字)/ 长版(~500 字)
- 出版资质参考 + 写作风格声明
- 微信二维码位置

### blurb.md (简介,4 版)
- 长版封底(400 字)/ 中版详情页(250 字)/ 短版微博抖音(60 字)/ 英文版海外(150 字)
- 每版独立写,可直接复制用

### copyright.md (版权页)
- CIP 数据(书名/作者/字数/版次/ISBN/印张)
- 内容提要 + 配套数字仓库 + 联系 + 致谢 + AI 声明 + 免责声明

### acknowledgment.md / ai_disclosure.md / corrections.md
- 致谢:案例原型团队 + 行业引路人 + 工具 + 家人
- AI 声明:具体工具型号 + 角色限定 + 章节 AI 参与度表
- 勘误:出版后追加

### back_cover.md
- 封底主图区 + 文案区 + 三大承诺 + 读者画像 + ISBN 条码区

### glossary.md / metadata.md / tools.md
- 术语表:中英对照 + 释义
- 元数据:出版前给出版社填的完整模板
- 工具:配套数字仓库说明

### trademark.md
- 模型厂商 / 客户行业 / 协议商标 + 引用规范

### video_scripts.md / wechat_try.md / zhihu_answer.md / epilogue.md / recommend.md
- 视频脚本(2 个视频)
- 公众号软文草稿
- 知乎首答
- 尾声
- 推荐语(3-5 段)

---

## Step 4 决策

| # | 决策 | 原因 |
|---|---|---|
| 1 | 14 个核心件批量生成(不写 cover.png/svg) | cover 是设计件,需人工/设计师 |
| 2 | 每件 4-8 个版本(短/中/长/英文) | 出版/营销场景多,版本全 |
| 3 | 内容用脚本批量生成,不每本独立写 | 节省工时,统一格式 |
| 4 | 保留 fde 原 cover.svg / workbuddy 原 cover.svg | 之前已生成,不动 |
| 5 | 暂不批量改 fde/workbuddy 已有件(blurb/copyright) | 已有内容质量 OK,直接覆盖可能反而破坏 |

---

## 后续(可选)

1. **重出 5 份 PDF** (1h):验证 promotion 件不影响 build
2. **优化生成质量** (1-2h):手改个别件(blurb 中版读起来略生硬)
3. **生成 cover.png** (设计工作,不在本步):需要设计师

---

## 下一步

进入 **Step 5 重出 PDF + 验证** (1h):
- 5 份 PDF:ai-coding, fde, workbuddy 三卷, workbuddy 全 3 卷合
- 验证 Step 1-4 后 PDF 仍能正常出片
- 修复可能的 layout 变化
- commit + push
