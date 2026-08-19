# Step 5 重出 5 份 PDF 报告 (2026-08-19)

> **成果**:5 份 PDF 全部成功出片
> **总用时**:8 分钟 (Chrome 渲染)
> **验证**:Step 1-4 重构后 PDF 仍能正常出片

---

## 5 份 PDF 出片详情

| # | PDF | 大小 | 页数 | 渲染时间 |
|---|---|---|---|---|
| 1 | `ai-coding/dist/main.pdf` | 11.56 MB | 262 页 | ~30s |
| 2 | `fde/dist/main.pdf` | 2.20 MB | 147 页 | ~15s |
| 3 | `workbuddy/dist/第一卷.pdf` | 3.02 MB | 119 页 | ~30s |
| 4 | `workbuddy/dist/第二卷.pdf` | 6.72 MB | 214 页 | ~30s |
| 5 | `workbuddy/dist/第三卷.pdf` | 21.62 MB | 230 页 | ~60s |
| 6 | `workbuddy/dist/workbuddy.pdf` (合) | 27.27 MB | 495 页 | ~90s |
| **合计** | — | **72.39 MB** | **1467 页** | — |

> 6 = 5 + 1 (workbuddy 三卷合一份)

---

## PDF 内容检查

每份 PDF 都包含:
- 封面(从 promotion/cover)
- 序(如果有)
- 目录(从 chapters/ 自动生成)
- 全部章节(按 markdown 顺序)
- 附录
- 字体:CJK fallback chain (STHeiti → PingFang SC → Hiragino Sans GB → Microsoft YaHei)
- 图片:workbuddy/ai-coding 用 figures 真实图;fde 无图

---

## 关键决策

- **workbuddy 三卷每卷独立 PDF** + **合一份大 PDF**:两种都用,大 PDF 用于"通读三卷",小 PDF 用于"按卷分发"
- **每段 15000ms 虚拟时间预算**:等所有 <img> 加载完再打印
- **不排除 dist 进 git**:dist 是出版产物,版本控制有意义

---

## 验证清单

- [x] ai-coding 5 张 13-15 章节全部 53 张图加载
- [x] fde 26 章纯文字渲染
- [x] workbuddy 第一卷 8 章(无图)渲染
- [x] workbuddy 第二卷 14 张图加载
- [x] workbuddy 第三卷 52 张图加载
- [x] CJK 字体无 tofu 方块
- [x] promotion 件不进 PDF(只是发布物)

---

## 下一步

进入 **Step 6 报告** (1h):
- 写 `INDEX.md` v2:3 本书总览 + 当前状态
- 写 `REFACTORING-REPORT.md`:Step 1-5 重构总报告
- 写 `PUBLICATION-READINESS.md`:出版前 checklist
- 更新 `README.md`
