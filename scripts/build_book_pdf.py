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
  height: auto;
  display: block;
  margin: 1.2em auto;
  page-break-inside: avoid;
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

    print(f"  📚 书名: {book_title}")
    print(f"  📝 副标题: {subtitle}")
    print(f"  📂 章节: {len(chapter_files)} 个")
    if appendix_files:
        print(f"  📎 附录: {len(appendix_files)} 个")

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
    """把 figures/ 复制到 HTML 同级,返回 HTML 路径。

    关键路径设计:
    - HTML 放在 tmpdir/<book>/<vol>/chapters/book.html(vol 可省)
    - figures 放在 tmpdir/<book>/<vol>/figures/
    - 这样 chapters/ 里 md 引用的 ../figures/xxx 仍然有效
    - 跨卷合(--all)时,三卷 figures 都合并到 tmpdir/.../figures/(同名会冲突,但每卷命名不冲突)
    """
    tmpdir = Path(tempfile.mkdtemp(prefix=f"book_pdf_{book_name}_"))
    sub = tmpdir / book_name
    sub.mkdir()

    vols = (['第一卷', '第二卷', '第三卷'] if all_vols
            else ([vol_subdir] if vol_subdir else [None]))

    figs_copied = 0
    for vol in vols:
        if vol:
            target = sub / vol
            target.mkdir(parents=True, exist_ok=True)
        else:
            target = sub
        chapters_dir = target / "chapters"
        chapters_dir.mkdir(parents=True, exist_ok=True)

        if vol:
            figs_src = book_dir / vol / "figures"
        else:
            figs_src = book_dir / "figures"
        if figs_src.exists():
            figs_dst = target / "figures"
            if figs_dst.exists():
                # 跨卷合时各卷 figs_dst 不同,不会冲突
                shutil.rmtree(figs_dst)
            shutil.copytree(figs_src, figs_dst)
            figs_copied += sum(1 for _ in figs_dst.rglob('*') if _.is_file())

    print(f"  📸 复制 figures/ 总计: {figs_copied} 张")

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
        # 把 ../figures/ → figures/
        html_str = html_str.replace('../figures/', 'figures/')
        html_path.write_text(html_str, encoding='utf-8')
    else:
        # 单卷或单书:HTML 放在 sub/<vol>/chapters/book.html,figures 在 sub/<vol>/figures/
        # 这样 ../figures/ 仍然有效
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
