# 元数据(电子书上架用)

> 这是电子书上架时给平台的字段表,采用 **Dublin Core + ONIX Lite** 混合字段。
> 印刷书的开本/印张/装帧/印数等已全部删除;新增了平台标识、分发矩阵、关键词、分类。

## 一、基础信息(Dublin Core)

| 字段 | 值 | 平台必填 |
|---|---|---|
| 书名(Title) | AI Coding · 人人都是程序员 | KDP ✓ Apple ✓ 微信 ✓ 豆瓣 ✓ |
| 副标题(Subtitle) | 让非技术人做出可交付的产品 | KDP ✓ Apple ✓ |
| 英文名 | AI Coding: Everyone is a Programmer | KDP ✓ |
| 作者(Creator) | 施可(Shi Ke) | 全部 ✓ |
| 作者简介 | 见 `about_author.md` | KDP ✓ Apple ✓ 微信 ✓ |
| 语言(Language) | zh-CN | 全部 ✓ |
| 标识符(Identifier) | ISBN(EPUB,待申请) / ASIN(KDP,待分配) / DOI(可选) | KDP ✓ Apple ✓ |
| 出版者(Publisher) | 施可 · 三本书统一仓库(自出版) | KDP ✓ Apple ✓ |
| 出版日期(Date) | 2026-08-19 | KDP ✓ Apple ✓ |
| 最后更新(Date Modified) | 见 CHANGELOG.md | EPUB3 推荐 |
| 版本(Version) | v1.0.0 | 自定义 |
| 描述(Description) | 见 `back_cover.md` 第一段 | KDP ✓ Apple ✓ |
| 简介短版(Short Blurb) | "参数会过时,方法论不会。" | 微博/豆瓣 |
| 主题(Subject) | 人工智能、编程、创业、产品管理、效率工具 | KDP 2个 ✓ Apple 多选 |
| 分类(Category) | 计算机 / 商业 / 创业 | KDP Browse 2个 ✓ |

## 二、定价与分发矩阵

| 平台 | 格式 | 定价(占位) | 分成模式 | 状态 | 链接 |
|---|---|---|---|---|---|
| **GitHub** | md 源文件 | 免费 | CC BY-NC-SA 4.0 | ✅ 已发布 | `https://github.com/shike/books`(顶层仓,`ai-coding/` 子目录) |
| **微信读书** | EPUB | ¥29.90(待定) | 平台 50% / 作者 50% | 🟡 待上架 | 微信读书 ID 待分配 |
| **豆瓣阅读** | EPUB | ¥29.90(待定) | 平台 30% / 作者 70% | 🟡 待上架 | 豆瓣阅读 ID 待分配 |
| **KDP(Kindle)** | EPUB → MOBI/AZW3 | $4.99(70% 版税) | KDP 30% / 作者 70% | 🟡 待上架 | ASIN 待分配 |
| **Apple Books** | EPUB | $4.99(70% 版税) | Apple 30% / 作者 70% | 🟡 待上架 | Apple ID 待分配 |
| **Gumroad** | EPUB / PDF | $9(自营,直签) | Gumroad 10% / 作者 90% | 🟡 待上架 | — |
| **小报童** | EPUB / 在线 | ¥19.9(自营,直签) | 小报童 5% / 作者 95% | 🟡 待上架 | — |

> **定价建议**:¥29.9 是中文知识付费的甜区;KDP $4.99 是英文区入门价;Gumroad $9 给直签读者赠送 Markdown 源文件权限。

## 三、关键词与分类(KDP 优化用)

**核心关键词**(KDP 7 个槽):
1. AI 编程
2. AI Coding
3. 提示词工程
4. 一人公司
5. MVP
6. 非技术人
7. Claude

**长尾关键词**(Apple Books / 豆瓣搜索):
- 提示词怎么写、AI 产品经理、非程序员编程、AI 创业、AI 工具实战、Cursor 教程、Claude Code、AI 编程入门

**KDP Browse 分类**(选 2 个):
1. Computers & Technology > Programming > Software Development(主)
2. Business & Money > Entrepreneurship(辅)

**Apple Books 分类**:
1. 商业与投资 > 创业(主)
2. 计算机 > 编程(辅)

## 四、电子书专属技术字段

| 字段 | 值 |
|---|---|
| EPUB 版本 | 3.0 |
| 文件大小 | 2.08 MB(ai-coding.epub 实测) |
| 是否有 DRM | 无(CC BY-NC-SA 已含限制条款) |
| 是否可全文搜索 | 是 |
| 是否可复制文字 | 是(CC 协议要求) |
| 字体嵌入 | 是(内置中文字体) |
| 章节锚点 | 每章独立 spine itemref,可深链 |
| 引用方式 | 平台 ISBN / 自营 DOI(可选) |

## 五、封面规格(多平台)

| 平台 | 尺寸 | 比例 | 格式 | 状态 |
|---|---|---|---|---|
| KDP | 1600 × 2560 | 1:1.6 | JPG | ✅ `cover_kdp.jpg` (511 KB) |
| Apple Books | 1400 × 1873 | 1:1.34 | JPG | ✅ `cover_apple.jpg` (317 KB) |
| 微信读书 | 600 × 800 | 3:4 | JPG | ✅ `cover_wechat.jpg` (68 KB) |
| 豆瓣阅读 | 600 × 800 | 3:4 | JPG | ✅ `cover_douban.jpg` (68 KB) |
| 通用 web | 800 × 1200 | 2:3 | PNG | ✅ `cover_web.png` (924 KB) |

封面生成器脚本:`_tools/gen_covers.py`(中心裁剪 / 长边填充两策略,3 本书 × 5 平台 = 15 张)

## 七、版本与发布节奏

- **首发版本**:v1.0.0(2026-08-19)
- **更新策略**:每月一次小更新,每季度一次中改,每年一次大版本
- **平台同步**:GitHub Releases → 24 小时内推 KDP / Apple / 微信 / 豆瓣
- **退订机制**:读者通过订阅 Releases / 公众号"电子书架"获取更新通知

## 八、修订与审核节点(电子化)

1. **初校**:作者对全部章节完成自校,标注待核实数字与引用。
2. **互校**:合作者对第 1、13、15 三章进行深度审稿(方法论密度最高)。
3. **平台审核**:KDP / Apple / 微信 / 豆瓣 各自的合规审核(自动 + 抽样)。
4. **正式发布**:CHANGELOG 更新 + 邮件通知订阅者。
5. **持续反馈**:GitHub Issues + 邮箱 + 公众号留言,每月汇总一次。

## 九、版权与许可

- 本书文字版权归作者所有。
- 本书案例涉及的代码,以配套仓库的 LICENSE 文件为准;默认采用 MIT 协议,具体案例另有声明的从其声明。
- 本书引用清单中的第三方来源,版权归各自权利人所有;引用仅用于学术与教学目的。
- 本作品整体采用 **CC BY-NC-SA 4.0** 协议,允许在署名前提下非商业转载与改编,改编作品需同样以 CC BY-NC-SA 4.0 发布。