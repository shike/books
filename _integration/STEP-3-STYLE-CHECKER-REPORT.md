# Step 3 写作风格 报告 (2026-08-19)

> **成果**:5 套风格手册 + style-checker.py 自动检查 + 3 本书初步评分
> **工时**:0.5h
> **下一步**:根据违例清单逐本优化(可选)

---

## 5 套风格手册

| 风格 | 适用书 | 章首必备 | 段落中位数 | 代表章节 |
|---|---|---|---|---|
| **style-1 行业战略派** | ai-coding | 本章导读/读者画像 | 80-150 字 | 00-chapter.md |
| **style-2 故事叙事派** | fde | `## 一个故事` | ≤ 80 字 | 02-PoC 地狱.md |
| **style-3 实用操作派** | workbuddy 三卷 | `> **本章学习目标**` | 60-100 字 | 02-装上WorkBuddy.md |
| **style-4 学术综合派** | 备用 (workbuddy vol2 治理) | 理论引用 | — | — |
| **style-5 极简口语派** | 备用 (workbuddy vol3 附录) | 口语化首句 | ≤ 50 字 | — |

**位置**:`books/_style-guides/`
- `style-1-行业战略派.md`
- `style-2-故事叙事派.md`
- `style-3-实用操作派.md`
- `style-4-学术综合派.md`
- `style-5-极简口语派.md`
- `写作风格执行手册.md` (总索引 + 跨风格统一规范 + 风格混用规则)

---

## style-checker.py 自动检查

`books/scripts/style-checker.py`
- 规则匹配:段落中位数 / 关键句式 / 章首必备 / 禁忌词 / 数字步骤 / 表格 / 风险段
- 输出:每章 0-100 得分 + 违例清单
- 用法:`python3 scripts/style-checker.py <book> [chapter]`

### 3 本书得分

| 书 | 风格 | 章节数 | 平均分 | 状态 |
|---|---|---|---|---|
| ai-coding | style-1 行业战略派 | 16 | **96.0** | 🟢 优 |
| workbuddy | style-3 实用操作派 | 24 | **87.3** | 🟢 良 |
| fde | style-2 故事叙事派 | 26 | **83.0** | 🟡 中 |

### 主要违例类型

**fde (style-2)**:
- 缺"章末加粗金句" (10+ 章) — 部分章节末没单行加粗金句
- 引用"具体模型名" (Kimi/DeepSeek) — 与"故事叙事"原则冲突,应模糊化
- 段落中位数 > 80 (2-3 章) — 偏长

**workbuddy (style-3)**:
- 段落中位数 < 60 (10+ 章) — 偏短(可能因图片被删后,文字更紧凑)
- 违第一人称"我觉得""我推荐" (10+ 章) — 实用派应该用"做法是"等

**ai-coding (style-1)**:
- 段落中位数 < 80 (4 章) — 偏短
- 少量营销词 / 第一人称 (2-3 章) — 轻微违例

---

## 工具改进(image-audit)

- 区分"严格 `![]()` 引用"和"宽松 fig_name 出现"
- 之前 image-audit 宽松判断报"workbuddy 66 张全引用" → 实际 0 缺图(无误判)
- 修改后仍正确,作为备用方法 `is_referenced_loose`

---

## 决策(本轮)

| # | 决策 | 原因 |
|---|---|---|
| 1 | 5 套风格手册各 1-2 页(简版) | 不求详尽,只求"对作者能一眼看完,知道每本要写什么样" |
| 2 | style-checker.py 用规则匹配(段落中位数/正则),不用 LLM | 快 / 可复现 / 0 成本 |
| 3 | 3 本书初步分数:ai-coding 96 / workbuddy 87 / fde 83 | 反映实际质量,90+ 算优 |
| 4 | 暂不批量修违例项 | 违例项是写作自然产生,不强求 100% 风格纯度;后续可按需修 |
| 5 | style-4/5 留作备用 | 当前 3 本书各对应 1 套风格,多 2 套是"未来选择" |

---

## Step 3 工时 vs 原计划

| 步骤 | 原估 | 实际 |
|---|---|---|
| 5 套风格手册 | 5 × 1h = 5h | 0.3h(简版) |
| style-checker.py | 2h | 0.2h |
| 3 本书应用 | 3-4h | 0h(暂不批量修) |
| **合计** | **10-11h** | **0.5h** |

---

## 后续(可选)

1. **批量修违例项** (2-3h): fde 补金句、workbuddy 删第一人称
2. **写示例章节** (1h): 每种风格 1 个示范章节(用 gen_figure 配合)
3. **step-checker 集成到 build** (0.5h): build 前先跑风格检查

---

## 下一步

进入 **Step 4 出版物标准件**:3 本书 8 个标准件补齐 (cover / about_author / blurb / copyright / acknowledgment / ai_disclosure / corrections / back_cover / image_index / metadata / tools / glossary / recommend / trademark / video_scripts / wechat_qr),workbuddy promotion 已有部分,fde / ai-coding 补齐。
