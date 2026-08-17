#!/usr/bin/env python3
"""
build_book_pdf.py — 把 books/ 下任意一本书的所有 chapters/*.md 合并并生成 PDF。

用法:
    python3 scripts/build_book_pdf.py <book-name> [--vol <vol-dir>]

示例:
    python3 scripts/build_book_pdf.py ai-coding
    python3 scripts/build_book_pdf.py fde
    python3 scripts/build_book_pdf.py workbuddy              # 三卷合并
    python3 scripts/build_book_pdf.py workbuddy --vol 第一卷  # 只出第一卷

输出:
    <book-name>/dist/main.pdf(默认)
    <book-name>/dist/<vol>.pdf(指定 --vol 时)

依赖:
    - Python 3.9+  + markdown 3.x
    - macOS Google Chrome.app(headless 模式打印 PDF)
    - 中文字体:STHeiti(macOS 自带)
"""
import sys
import os
import re
import shutil
import subprocess
import tempfile
import argparse
from pathlib import Path

import markdown

# ====== 常量 ======
SCRIPT_DIR = Path(__file__).resolve().parent
BOOKS_DIR = SCRIPT_DIR.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# ====== CSS(中文字体 STHeiti,排版舒适) ======
CSS = """
@page {
  size: A4;
  margin: 2.2cm 1.8cm 2.5cm 1.8cm;
  @bottom-center {
    content: counter(page) " / " counter(pages);
    font-family: "STHeiti", "PingFang SC", "Hiragino Sans GB", sans-serif;
    font-size: 9pt;
    color: #888;
  }
}
body {
  font-family: "STHeiti", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  font-size: 11pt;
  line-height: 1.7;
  color: #222;
  max-width: 100%;
}
h1 {
  font-size: 24pt;
  margin-top: 0.8em;
  margin-bottom: 0.5em;
  page-break-before: always;
  page-break-after: avoid;
  border-bottom: 2px solid #333;
  padding-bottom: 0.2em;
}
h2 {
  font-size: 17pt;
  margin-top: 1.4em;
  margin-bottom: 0.4em;
  page-break-after: avoid;
  border-left: 4px solid #444;
  padding-left: 0.4em;
}
h3 {
  font-size: 13.5pt;
  margin-top: 1.2em;
  margin-bottom: 0.3em;
  page-break-after: avoid;
  color: #333;
}
h4, h5, h6 {
  font-size: 11.5pt;
  margin-top: 1em;
  margin-bottom: 0.2em;
  page-break-after: avoid;
}
p {
  margin: 0.5em 0;
  text-align: justify;
}
img {
  max-width: 100%;
  max-height: 26cm;          /* 略小于 A4 可用页面高度,避免单张图撑爆 */
  height: auto;
  width: auto;
  display: block;
  margin: 0.5em auto;
  /* page-break-inside: avoid;  ← 删掉,让大图也能跨页或缩放 */
  object-fit: contain;
}
figure {
  margin: 1.5em 0;
  text-align: center;
  page-break-inside: avoid;
}
figcaption {
  font-size: 9.5pt;
  color: #666;
  margin-top: 0.4em;
  text-align: center;
}
blockquote {
  margin: 0.8em 1.2em;
  padding: 0.4em 0.8em;
  border-left: 3px solid #ccc;
  background: #f7f7f7;
  color: #555;
  font-size: 10.5pt;
}
code {
  font-family: "SF Mono", "Menlo", "Consolas", monospace;
  font-size: 0.9em;
  background: #f4f4f4;
  padding: 0.1em 0.3em;
  border-radius: 2px;
}
pre {
  background: #f4f4f4;
  padding: 0.8em 1em;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 9.5pt;
  line-height: 1.5;
  page-break-inside: avoid;
}
pre code {
  background: transparent;
  padding: 0;
}
table {
  border-collapse: collapse;
  margin: 1em auto;
  font-size: 10pt;
  page-break-inside: avoid;
}
th, td {
  border-top: 1px solid #ddd;
  border-bottom: 1px solid #ddd;
  padding: 0.4em 0.8em;
  text-align: left;
}
th {
  background: #f0f0f0;
  border-top: 2px solid #333;
  border-bottom: 2px solid #333;
  font-weight: bold;
}
ul, ol {
  margin: 0.5em 0;
  padding-left: 1.8em;
}
li {
  margin: 0.2em 0;
}
hr {
  border: none;
  border-top: 1px dashed #aaa;
  margin: 1.5em 0;
  page-break-after: avoid;
}
sup {
  color: #c00;
  font-size: 0.85em;
}
.toc {
  background: #fafafa;
  padding: 1.2em 1.5em;
  border: 1px solid #ddd;
  border-radius: 4px;
  page-break-after: always;
}
.book-title {
  text-align: center;
  margin: 4em 0 1em 0;
  page-break-before: always;
  border: none;
}
.book-title .main {
  font-size: 32pt;
  font-weight: bold;
  display: block;
  margin-bottom: 0.3em;
}
.book-title .sub {
  font-size: 14pt;
  color: #666;
  display: block;
  margin-bottom: 0.5em;
}
.book-title .author {
  font-size: 12pt;
  color: #999;
  display: block;
  margin-top: 1.5em;
}
.chapter-title {
  page-break-before: always;
}

/* ===== 出版前置(封面/版权/序/推荐序/作者介绍/简介/致谢) ===== */
.cover-page {
  page-break-after: always;
  text-align: center;
  padding: 0;
  margin: 0;
  page-break-inside: avoid;
}
.cover-page img {
  max-width: 100%;
  max-height: 100vh;
  width: auto;
  height: auto;
  display: block;
  margin: 0 auto;
  page-break-inside: avoid;
}
.cover-text-page {
  page-break-after: always;
  text-align: center;
  padding: 4em 1em 2em 1em;
  background: linear-gradient(135deg, #1a3a5c 0%, #0a1a2e 100%);
  color: white;
  min-height: 90vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  page-break-inside: avoid;
}
.cover-text-page .cover-title {
  font-size: 38pt;
  font-weight: 900;
  border: none;
  color: white;
  margin: 0 0 0.3em 0;
  page-break-before: avoid;
}
.cover-text-page .cover-subtitle {
  font-size: 14pt;
  color: #4a90e2;
  border: none;
  margin: 0 0 2em 0;
  padding: 0;
  page-break-after: avoid;
}
.cover-text-page .cover-volumes {
  margin: 2em 0;
  font-size: 13pt;
  color: rgba(255,255,255,0.7);
}
.cover-text-page .cover-volumes .vol {
  display: inline-block;
  margin: 0.3em 1em;
  padding: 0.4em 1em;
  background: rgba(255,255,255,0.1);
  border-radius: 4px;
}
.cover-text-page .cover-author {
  margin-top: 3em;
  font-size: 12pt;
  color: rgba(255,255,255,0.6);
  letter-spacing: 2px;
}
.front-matter {
  page-break-before: always;
  page-break-after: always;
  padding-top: 0.5em;
}
.front-matter h1 {
  border-bottom: 2px solid #333;
  font-size: 22pt;
}
.front-matter h2 {
  font-size: 16pt;
  border-left: none;
  padding-left: 0;
}
.vol-marker {
  background: #f0f0f0;
  border-left: 4px solid #4a90e2;
  padding: 0.3em 0.8em;
  font-size: 16pt;
  margin-bottom: 1em;
  color: #333;
}
.copyright-page {
  font-size: 10pt;
  line-height: 1.6;
}
.copyright-page h1 {
  font-size: 18pt;
  border: none;
  text-align: center;
  margin-bottom: 1em;
}
.copyright-page hr {
  border-top: 1px solid #ccc;
  margin: 1em 0;
}
.toc-page {
  font-family: "STHeiti", "PingFang SC", "Hiragino Sans GB", sans-serif;
}
"""


def preprocess_ai_coding_pandoc_footnotes(text: str) -> str:
    """处理 ai-coding 的 pandoc 风格脚注 [^N^] → <sup>[N]</sup>"""
    return re.sub(r'\[\^(\d+)\^\]', r'<sup>[\1]</sup>', text)


def collect_chapters(book_dir: Path, vol_subdir: str = None, all_vols: bool = False) -> list:
    """收集章节文件路径(已排序)。workbuddy 需指定 --vol 或 --all。"""
    if all_vols:
        # 跨卷合:按 第一卷 → 第二卷 → 第三卷 顺序
        files = []
        for vol in ['第一卷', '第二卷', '第三卷']:
            ch_dir = book_dir / vol / "chapters"
            if ch_dir.exists():
                vol_files = sorted([
                    p for p in ch_dir.glob("*.md")
                    if not p.name.startswith("_")
                    and not p.name.startswith(".")
                ])
                files.extend(vol_files)
        if not files:
            raise SystemExit(f"❌ {book_dir} 三卷都没有 chapters/")
        return files

    if vol_subdir:
        ch_dir = book_dir / vol_subdir / "chapters"
    else:
        ch_dir = book_dir / "chapters"

    if not ch_dir.exists():
        raise SystemExit(f"❌ 找不到 chapters 目录: {ch_dir}")

    # 排除 _archive 等
    files = sorted([
        p for p in ch_dir.glob("*.md")
        if not p.name.startswith("_")
        and not p.name.startswith(".")
    ])
    if not files:
        raise SystemExit(f"❌ {ch_dir} 里没有 .md 文件")
    return files


def collect_appendix(book_dir: Path, vol_subdir: str = None, all_vols: bool = False) -> list:
    """收集附录文件。"""
    files = []
    vols = ['第一卷', '第二卷', '第三卷'] if all_vols else (
        [vol_subdir] if vol_subdir else [None]
    )
    for vol in vols:
        if vol:
            ap_dirs = [book_dir / vol / "appendix", book_dir / vol / "appendices"]
        else:
            ap_dirs = [book_dir / "appendix", None]
        for d in ap_dirs:
            if d and d.exists():
                for p in sorted(d.rglob("*.md")):
                    if p.is_file() and "_archive" not in str(p):
                        files.append(p)
    return files


def md_to_html(md_text: str, md_engine=markdown.Markdown(
    extensions=['fenced_code', 'tables', 'sane_lists', 'toc', 'attr_list'],
    output_format='html5',
)):
    return md_engine.convert(md_text)


def find_promotion_files(book_dir: Path, vol_subdir: str = None) -> dict:
    """从 promotion/ 找出版前置所需的源文件。"""
    promo_dir = book_dir / "promotion"
    if not promo_dir.exists():
        return {}

    # 优先级
    candidates = {
        "cover": ["cover.png", "cover.svg", "封面.png", "封面.svg"],
        "about_author": ["about_author.md", "关于作者.md"],
        "blurb": ["blurb.md", "简介.md"],
        "copyright": ["copyright.md", "版权.md", "trademark.md"],
        "recommend": ["recommend.md", "推荐序.md"],
        "acknowledgment": ["acknowledgment.md", "致谢.md"],
        "ai_disclosure": ["ai_disclosure.md", "AI声明.md"],
        "back_cover": ["back_cover.md", "封底.md"],
    }
    out = {}
    for key, names in candidates.items():
        for name in names:
            p = promo_dir / name
            if p.exists():
                out[key] = p
                break
    return out


def find_vol_front_matter(vol_dir: Path) -> dict:
    """从 workbuddy 某卷找 序.md / 目录.md。"""
    out = {}
    for key, name in [("preface", "序.md"), ("toc", "目录.md")]:
        p = vol_dir / name
        if p.exists():
            out[key] = p
    return out


def build_cover_html(promo_files: dict) -> str:
    """封面页 HTML。"""
    cover = promo_files.get("cover")
    if cover:
        # 图片封面:用 cover.png 或 cover.svg
        # 路径在 prepare_html_with_assets 里会处理(把 promotion/ 复制到 figures 同级)
        rel = f"../promotion/{cover.name}"
        return f"""
<div class="cover-page">
  <img src="{rel}" alt="封面" />
</div>
"""
    else:
        # 无封面图:留空
        return ""


def build_front_matter(book_name: str, book_dir: Path, vol_subdir: str = None, all_vols: bool = False, book_title: str = "", subtitle: str = "") -> str:
    """拼出版前置 HTML。返回字符串(已含 page-break-before: always)。

    顺序(出版级):
    1. 封面图
    2. 版权页(copyright.md | trademark.md)
    3. AI 生成内容声明(ai_disclosure.md)
    4. 序(workbuddy 各卷 序.md)
    5. 目录(workbuddy 各卷 目录.md)
    6. 推荐序(recommend.md)
    7. 作者介绍(about_author.md)
    8. 简介(blurb.md)
    9. 致谢(acknowledgment.md)
    10. 封底(back_cover.md,若有)
    """
    parts = []

    # 收集所有源文件
    promo_files = find_promotion_files(book_dir)

    # workbuddy 各卷的序/目录
    vol_prefaces = []
    vol_tocs = []
    if book_name == "workbuddy":
        if all_vols:
            # 全本:不放各卷序/目录(那些内容已经包含在分卷 PDF 中,且避免挤占前置)
            # 只放一个简短的"三卷合"总序(从第一卷序截取前 200 字)
            pass
        elif vol_subdir:
            fm = find_vol_front_matter(book_dir / vol_subdir)
            if "preface" in fm:
                vol_prefaces.append((vol_subdir, fm["preface"]))
            if "toc" in fm:
                vol_tocs.append((vol_subdir, fm["toc"]))

    # 1. 封面页:用 SVG 图(workbuddy 三卷合除外,改用 HTML 文字封面以避免 Chrome 卡住)
    cover = promo_files.get("cover")
    if cover and not (book_name == "workbuddy" and all_vols):
        rel = f"../promotion/{cover.name}"
        parts.append(f'<div class="cover-page"><img src="{rel}" alt="封面" /></div>')
    elif cover and book_name == "workbuddy" and all_vols:
        # workbuddy 三卷合:用 HTML 文字封面代替 SVG(避免 Chrome 加载 SVG 卡住)
        # 从 README 拿书名/副标题
        parts.append(f'''<div class="cover-text-page">
<h1 class="cover-title">{book_title}</h1>
<h2 class="cover-subtitle">{subtitle}</h2>
<div class="cover-volumes">
  <div class="vol">第一卷 · 上手</div>
  <div class="vol">第二卷 · 协作</div>
  <div class="vol">第三卷 · 重塑</div>
</div>
<div class="cover-author">施可(Shi Ke) · 著</div>
</div>''')

    md_engine = markdown.Markdown(
        extensions=['fenced_code', 'tables', 'sane_lists', 'toc', 'attr_list'],
        output_format='html5',
    )

    def add_module(file_path, css_class="front-matter"):
        nonlocal md_engine
        text = file_path.read_text(encoding='utf-8')
        parts.append(f'<div class="{css_class}">{md_to_html(text, md_engine)}</div>')
        md_engine.reset()

    # 2. 版权页(独立)
    if "copyright" in promo_files:
        add_module(promo_files["copyright"], "front-matter copyright-page")
    elif "trademark" in promo_files:
        # 降级:用 trademark 充版权页
        add_module(promo_files["trademark"], "front-matter copyright-page")

    # 3. AI 生成内容声明(独立)
    if "ai_disclosure" in promo_files:
        add_module(promo_files["ai_disclosure"], "front-matter")

    # 4. 序(每卷 workbuddy)
    for vol, path in vol_prefaces:
        text = path.read_text(encoding='utf-8')
        parts.append(f'<div class="front-matter preface"><h2 class="vol-marker">{vol} · 序</h2>{md_to_html(text, md_engine)}</div>')
        md_engine.reset()

    # 5. 目录(每卷 workbuddy)
    for vol, path in vol_tocs:
        text = path.read_text(encoding='utf-8')
        parts.append(f'<div class="front-matter toc-page"><h2 class="vol-marker">{vol} · 目录</h2>{md_to_html(text, md_engine)}</div>')
        md_engine.reset()

    # 6. 推荐序(ai-coding)
    if "recommend" in promo_files:
        add_module(promo_files["recommend"], "front-matter")

    # 7. 作者介绍
    if "about_author" in promo_files:
        add_module(promo_files["about_author"], "front-matter")
    else:
        # 缺 about_author 时,生成最小版本
        parts.append(f'''<div class="front-matter">
<h1>关于作者</h1>
<p><strong>施可(Shi Ke)</strong> — 水滴跃动 Dropleap 创始人 / 前邻汇吧 COO / 中科大软工硕士</p>
<p>联系:shike@dropleap.cn | 主页:https://shike.github.io/ | GitHub:https://github.com/shike</p>
</div>''')

    # 8. 简介
    if "blurb" in promo_files:
        add_module(promo_files["blurb"], "front-matter")

    # 9. 致谢
    if "acknowledgment" in promo_files:
        add_module(promo_files["acknowledgment"], "front-matter")

    # 10. 封底
    if "back_cover" in promo_files:
        add_module(promo_files["back_cover"], "front-matter back-cover-page")

    return "\n".join(parts)


def build_html(book_name: str, book_dir: Path, vol_subdir: str = None, all_vols: bool = False) -> tuple:
    """返回 (html_str, title, subtitle)"""
    # 读 README 拿标题(简短)
    readme = book_dir / "README.md"
    if not readme.exists():
        raise SystemExit(f"❌ 找不到 README: {readme}")
    readme_text = readme.read_text(encoding='utf-8')

    # 提取书名 = README 第一行 # 后
    first_line = readme_text.split('\n', 1)[0]
    book_title = re.sub(r'^#+\s*', '', first_line).strip()
    # 副标题 = > 行
    subtitle = ""
    for line in readme_text.split('\n'):
        if line.strip().startswith(">"):
            subtitle = line.strip().lstrip("> ").strip()
            break

    # 收集章节 + 附录
    chapter_files = collect_chapters(book_dir, vol_subdir, all_vols)
    appendix_files = collect_appendix(book_dir, vol_subdir, all_vols)

    # 拼出版前置
    front_matter = build_front_matter(book_name, book_dir, vol_subdir, all_vols, book_title, subtitle)

    # 计数
    promo_files = find_promotion_files(book_dir)
    vol_fm_count = 0
    if book_name == "workbuddy":
        vols = ['第一卷', '第二卷', '第三卷'] if all_vols else ([vol_subdir] if vol_subdir else [])
        for vol in vols:
            vfm = find_vol_front_matter(book_dir / vol)
            vol_fm_count += len(vfm)

    print(f"  📚 书名: {book_title}")
    print(f"  📝 副标题: {subtitle}")
    print(f"  📂 章节: {len(chapter_files)} 个")
    if appendix_files:
        print(f"  📎 附录: {len(appendix_files)} 个")
    print(f"  📄 出版前置: {len(promo_files) + vol_fm_count} 个模块(封面/版权/序/推荐序/作者介绍/简介/致谢)")

    # 拼 HTML
    md_engine = markdown.Markdown(
        extensions=['fenced_code', 'tables', 'sane_lists', 'toc', 'attr_list'],
        output_format='html5',
    )

    body_parts = []
    for md_file in chapter_files:
        print(f"    → {md_file.name}")
        text = md_file.read_text(encoding='utf-8')
        # ai-coding 特化预处理
        if book_name == "ai-coding":
            text = preprocess_ai_coding_pandoc_footnotes(text)
        body_parts.append(md_to_html(text, md_engine))
        md_engine.reset()

    for md_file in appendix_files:
        rel = md_file.relative_to(book_dir)
        print(f"    + 附录: {rel}")
        text = md_file.read_text(encoding='utf-8')
        if book_name == "ai-coding":
            text = preprocess_ai_coding_pandoc_footnotes(text)
        body_parts.append(md_to_html(text, md_engine))
        md_engine.reset()

    body = "\n".join(body_parts)

    # 完整 HTML
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{book_title}</title>
<style>
{CSS}
</style>
</head>
<body>

{front_matter}

<div class="book-title">
  <span class="main">{book_title}</span>
  <span class="sub">{subtitle}</span>
  <span class="author">施可(Shi Ke) · shike@dropleap.cn</span>
</div>

{body}

</body>
</html>
"""
    return full_html, book_title, subtitle


def chrome_headless_pdf(html_path: Path, pdf_path: Path):
    """调用 Chrome headless 打印 PDF。"""
    if not Path(CHROME).exists():
        raise SystemExit(f"❌ 找不到 Chrome: {CHROME}")
    cmd = [
        CHROME,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--font-render-hinting=none",  # 中文渲染更稳
        f"--print-to-pdf={pdf_path}",
        "--print-to-pdf-no-header",
        "--no-pdf-header-footer",  # 自己控制 footer
        f"file://{html_path}",
    ]
    print(f"  🖨  Chrome headless 打印 → {pdf_path.name}")
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if not pdf_path.exists():
        print(f"  ❌ Chrome stderr: {res.stderr[:1000]}")
        raise SystemExit("PDF 生成失败")
    size_mb = pdf_path.stat().st_size / 1024 / 1024
    print(f"  ✓ PDF 大小: {size_mb:.2f} MB")


def prepare_html_with_assets(html_str: str, book_dir: Path, vol_subdir: str = None, book_name: str = "book", all_vols: bool = False) -> Path:
    """把 figures/ + promotion/ 复制到 HTML 同级,返回 HTML 路径。

    关键路径设计:
    - 单书/单卷:HTML 放 sub/<vol>/chapters/book.html,figures/promotion 放 sub/<vol>/
    - 跨卷合(--all):HTML 放 sub/book.html,figures 各卷合并到 sub/,promotion 放 sub/(顶层)
    """
    tmpdir = Path(tempfile.mkdtemp(prefix=f"book_pdf_{book_name}_"))
    sub = tmpdir / book_name
    sub.mkdir()

    figs_copied = 0
    promo_copied = False

    if all_vols:
        # 跨卷合:每卷 figures 合并到 sub/figures/,promotion 在 sub/promotion/(顶层,各卷共用)
        chapters_dir = sub / "chapters"  # 临时建一个(防止后续代码错)
        chapters_dir.mkdir(parents=True, exist_ok=True)

        for vol in ['第一卷', '第二卷', '第三卷']:
            figs_src = book_dir / vol / "figures"
            if figs_src.exists():
                figs_dst = sub / "figures"
                if not figs_dst.exists():
                    shutil.copytree(figs_src, figs_dst)
                else:
                    # 合并(各卷命名不冲突,如 1.x.x vs 2.x.x)
                    for item in figs_src.iterdir():
                        dst = figs_dst / item.name
                        if not dst.exists():
                            if item.is_dir():
                                shutil.copytree(item, dst)
                            else:
                                shutil.copy2(item, dst)
                figs_copied = sum(1 for _ in figs_dst.rglob('*') if _.is_file())

        # promotion 放 sub/promotion/(顶层,只有一份)
        promo_src = book_dir / "promotion"
        if promo_src.exists():
            promo_dst = sub / "promotion"
            if promo_dst.exists():
                shutil.rmtree(promo_dst)
            shutil.copytree(promo_src, promo_dst)
            promo_copied = True
    else:
        # 单书/单卷
        if vol_subdir:
            target = sub / vol_subdir
        else:
            target = sub
        chapters_dir = target / "chapters"
        chapters_dir.mkdir(parents=True, exist_ok=True)

        if vol_subdir:
            figs_src = book_dir / vol_subdir / "figures"
        else:
            figs_src = book_dir / "figures"
        if figs_src.exists():
            figs_dst = target / "figures"
            if figs_dst.exists():
                shutil.rmtree(figs_dst)
            shutil.copytree(figs_src, figs_dst)
            figs_copied = sum(1 for _ in figs_dst.rglob('*') if _.is_file())

        promo_src = book_dir / "promotion"
        if promo_src.exists():
            promo_dst = target / "promotion"
            if promo_dst.exists():
                shutil.rmtree(promo_dst)
            shutil.copytree(promo_src, promo_dst)
            promo_copied = True

    print(f"  📸 复制 figures/ 总计: {figs_copied} 张")
    if promo_copied:
        print(f"  📋 复制 promotion/ 完成")

    # 写 HTML 到第一个 chapters/ 目录(其余卷的 HTML 也指向该 chapters 不对——只能放第一个)
    # 实际策略:每卷一个 HTML,用 CSS page-break 分隔
    # 但用户传的是一个 html_str(已包含所有内容),所以只能放一个 chapters/
    # 简单做法:放 sub/chapters/book.html(用 all_vols=False 的位置,即无 vol 目录的 chapters)
    # 但 all_vols=True 时,volumes 各自有 chapters 目录,放哪里?
    # 解决:把 html 放到 sub/book.html,figures 放 sub/figures/(每卷合并)
    # 然后让 html 里所有 <img src="../figures/xxx.png"> → 改写为 figures/xxx.png
    # 但 md 源是 ../figures/,html 已经在 sub/ 根,../figures/ 会到 tmpdir/figures/(不存在)

    # 重新设计:把 html_str 里的 ../figures/ 全部预处理为相对路径 figures/(因 HTML 就在 figures/ 同级)
    # 但 all_vols=True 时,各卷 figures 拼到 sub/figures/ 会有冲突(workbuddy 命名 1.x.x vs 2.x.x 不冲突,good)
    if all_vols:
        html_path = sub / "book.html"
        # 把 ../figures/ → figures/ 和 ../promotion/ → promotion/
        # (HTML 在 sub/book.html,figures/promotion 在 sub/figures、sub/promotion)
        html_str = html_str.replace('../figures/', 'figures/')
        html_str = html_str.replace('../promotion/', 'promotion/')
        html_path.write_text(html_str, encoding='utf-8')
    else:
        # 单卷或单书:HTML 放在 sub/<vol>/chapters/book.html,figures/promotion 在 sub/<vol>/
        # 这样 ../figures/ 和 ../promotion/ 仍然有效
        if vol_subdir:
            html_path = sub / vol_subdir / "chapters" / "book.html"
        else:
            html_path = sub / "chapters" / "book.html"
        html_path.write_text(html_str, encoding='utf-8')
    return html_path, tmpdir


def main():
    ap = argparse.ArgumentParser(description="把书的 chapters/*.md 合并生成 PDF")
    ap.add_argument("book", help="书名(ai-coding / fde / workbuddy)")
    ap.add_argument("--vol", help="workbuddy 单独出某卷(第一卷/第二卷/第三卷)")
    ap.add_argument("--all", action="store_true", help="workbuddy 跨三卷合一个 PDF")
    args = ap.parse_args()

    if args.vol and args.all:
        raise SystemExit("❌ --vol 和 --all 不能同时用")

    book_dir = BOOKS_DIR / args.book
    if not book_dir.exists():
        raise SystemExit(f"❌ 找不到书目录: {book_dir}")

    # 决定输出 PDF 路径
    dist_dir = book_dir / "dist"
    if args.all:
        out_pdf = dist_dir / "workbuddy.pdf"  # 三卷合一的主书
        out_label = "三卷合"
    elif args.vol:
        out_pdf = dist_dir / f"{args.vol}.pdf"
        out_label = args.vol
    else:
        out_pdf = dist_dir / "main.pdf"
        out_label = "全本"
    dist_dir.mkdir(exist_ok=True)

    print(f"\n📖 构建 {args.book} ({out_label}) → PDF")
    print("=" * 60)

    # 1. 拼 HTML
    html_str, title, subtitle = build_html(args.book, book_dir, args.vol, args.all)

    # 2. 准备 HTML(复制 figures 到正确位置)
    html_path, tmpdir = prepare_html_with_assets(
        html_str, book_dir, args.vol, args.book, args.all
    )
    print(f"  📄 HTML 临时文件: {html_path} ({html_path.stat().st_size/1024:.0f} KB)")

    try:
        # 3. Chrome 转 PDF
        chrome_headless_pdf(html_path, out_pdf)
    finally:
        # 清理临时目录
        try:
            shutil.rmtree(tmpdir)
        except OSError:
            pass

    print(f"\n✅ 完成: {out_pdf}")


if __name__ == "__main__":
    main()
