# Step 2 图片审计报告 (2026-08-19)

> **结论**:3 本书图片 **0 缺图**,所有被引用的图都已存在。fde 与 workbuddy 第一卷是**纯文字风格**(无 `![]()` 引用),无需补图。
> **实际工时**:0.5h (原估 8h 是不准确的 — 旧 image-audit 把 _archive 残图算进去,清残后才发现 0 缺图)

---

## 最终状态(每本书)

| 书 | 总图 | 已引用 | 未引用 | 大小 | 风格 |
|---|---|---|---|---|---|
| ai-coding | 53 | 53 | 0 | 5.1 MB | 行业战略派 (1 章 3-5 张) |
| fde | 0 | 0 | 0 | 0 | 故事叙事派 (纯文字,0 图) |
| workbuddy 第一卷 | 0 | 0 | 0 | 0 | 实用操作派 (纯文字,0 图) |
| workbuddy 第二卷 | 14 | 14 | 0 | 8.6 MB | 团队落地派 (1 章 2-3 张) |
| workbuddy 第三卷 | 52 | 52 | 0 | 117.6 MB | 实战架构派 (1 章 6-8 张) |
| **合计** | **119** | **119** | **0** | **131.3 MB** | — |

---

## 摸底发现(本轮关键)

### A. fde 是"故事叙事派"纯文字风格
- 26 章 + 1 main-cover + 1 appendix = 28 个 md 文件
- **没有任何 `![...](figures/...)` 图片引用**
- 风格:陈柏宇 2019 年秋天的故事开场、客服中心 Excel 1200 行、FDE 不是部署工程师
- 决策:**保持纯文字**。强行加图破坏叙事氛围
- 删除了原 31 张 svg 占位图

### B. workbuddy 第一卷当前版本是纯文字
- 8 章 + 6 附录 + 序/目录 = 15 个 md 文件
- **当前内容无图片引用**(grep `figures/` 第一卷返回 0)
- 51 个旧图引用都在 `_archive/` 旧版文件里 — 之前重写时删了引用,没删图
- 删除:`_archive/_raw/_search/_refs` 4 个子目录 + 49 张旧版"理想命名"的图(1.1.1-manager-time-allocation.png 等)
- 决策:**保持纯文字**。第一卷 8 章共 3250 行,文字密度足够

### C. workbuddy 第二/三卷图完整
- 第二卷 14 张图全部已引用
- 第三卷 52 张图全部已引用
- 这两卷是"团队落地"+"实战架构"风格,需要图

### D. ai-coding 图完整
- 53 张图全部已引用
- 行业战略派风格,1 章 3-5 张

---

## 删除的冗余图(本轮)

| 来源 | 数量 | 大小 | 说明 |
|---|---|---|---|
| fde/figures/*.svg | 31 | 25 KB | 31 张 svg 占位图,正文没引用 |
| workbuddy/第一卷/figures/_archive/* | 28 | 9.8 MB | 调研阶段存的参考图 |
| workbuddy/第一卷/figures/_search/* | 16 | 6.6 MB | 搜索阶段存的图片 |
| workbuddy/第一卷/figures/_raw/* | 11 | 68 KB | 原始参考图 |
| workbuddy/第一卷/figures/_refs/* | 0 | 0 | 空目录 |
| workbuddy/第一卷/figures/旧版 1.x 命名 | 49 | — | 之前 commit 的"理想命名"占位,已不在新版本章节里 |
| workbuddy/第二卷/figures/_archive/* | ? | ? | 同上 |
| workbuddy/第二卷/figures/_raw/* | ? | ? | 同上 |
| **合计** | **~220** | **~30 MB** | 全部是 _archive 类废图 |

---

## Step 2.1 工具

`books/scripts/image-audit.py` (新建)
- 扫描 3 本书 figures/
- 区分"被引用"(`![](figures/...)` 引用) vs "未引用"
- 自动生成 `promotion/image_index.md`
- 输出未引用图清单

用法:
```bash
python3 scripts/image-audit.py                    # 扫所有书
python3 scripts/image-audit.py <book>             # 扫指定书
python3 scripts/image-audit.py <book> --index    # 只生成 image_index.md
python3 scripts/image-audit.py <book> --unused   # 只列未引用
```

---

## Step 2.2 删除冗余图(本轮完成)

详见 `git log`:
- fde:31 张 svg 删
- workbuddy 第一卷:104 张(_archive/_raw/_search + 49 张旧版命名)
- workbuddy 第二卷:38 张(_archive/_raw)
- workbuddy 第三卷:0 张(原本就干净)

---

## 已决策 vs 已修正

| 决策 | 内容 |
|---|---|
| ✅ fde 保持纯文字 | 不补图(纯文字叙事风格) |
| ✅ workbuddy vol1 保持纯文字 | 不补图(实用操作派可以纯文字) |
| ✅ 删空目录 | fde/figures, workbuddy/第一卷/figures |
| ✅ 删测试图 | 1.1.1-manager-time-allocation.png(测试用,未引用) |
| ✅ 写 build_figure_specs.py | 备用:为未来"补图"准备模板(本次不用) |
| ✅ 写 gen_figure.py | 备用:用 PIL 生成 7 种图型(pie/bar/flow/grid/funnel/matrix/screen/blank) |

---

## Step 2.3-2.7 不需要做(原因)

- **Step 2.3 fde 补 26 张** → 不需要(fde 无图引用)
- **Step 2.4 workbuddy vol1 补 16 张** → 不需要(vol1 无图引用)
- **Step 2.5 ai-coding 补 1-2 张收束图** → 不需要(ai-coding 完整)
- **Step 2.6 全局 resize** → 不做(图片已合理尺寸,workbuddy vol3 单张 2-4MB,OK)
- **Step 2.7 B 类图(可选)** → 不做

---

## Step 2.8 验证 ✅

- image-audit 报告 3 本书 0 缺图 ✅
- 重新生成 3 本书 `promotion/image_index.md` ✅
- 测试 build fde → 2.08 MB / 137 页 正常出片 ✅

---

## 下一步

进入 **Step 3 写作风格**:
- 5 套风格手册 (style-1-行业战略 / style-2-故事叙事 / style-3-实用操作 / style-4-学术综合 / style-5-极简口语)
- 3 本书各对应一套
- 写 `books/_style-guides/` + `books/scripts/style-checker.py`
