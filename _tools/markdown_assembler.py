#!/usr/bin/env python3
"""
图书打包器:合并 markdown → 生成 EPUB / PDF / DOCX。
不依赖 pandoc / brew / weasyprint,纯 Python。
"""
import os
import io
import re
import sys
import zipfile
import shutil
from pathlib import Path
from typing import List, Dict, Tuple, Optional

import markdown as md_lib
from PIL import Image

from book_config import BOOKS, ROOT


# ==================== Markdown 处理 ====================

def read_md(path: str) -> str:
    """读 md 文件,容错"""
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_title(md_text: str, fallback: str = "") -> str:
    """提取第一个 # 标题"""
    for line in md_text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def assemble_markdown(book_key: str) -> Tuple[str, Dict]:
    """合并一本书的所有 md → 返回 (markdown_text, stats)"""
    cfg = BOOKS[book_key]
    parts: List[Tuple[str, str]] = []  # [(section_title, content), ...]
    stats = {"chapters": 0, "appendices": 0, "intro_pages": 0, "outro_pages": 0,
             "word_count": 0, "figure_refs": []}

    # 1. intro pages
    for title, path in cfg.get("intro_pages", []):
        if title == "封面":
            parts.append((title, "<!-- COVER_SLOT -->\n"))
            continue
        content = read_md(path)
        if content:
            parts.append((title, content))
            stats["intro_pages"] += 1

    # 2. chapters (单卷 vs 多卷)
    if book_key == "workbuddy":
        for vol in cfg["volumes"]:
            # 卷首页
            vol_cover = parts.append((vol["title"],
                                    f"# {vol['title']}\n\n*{vol['subtitle']}*\n\n---\n\n"))
            # 章节
            ch_dir = vol["chapters_dir"]
            if os.path.isdir(ch_dir):
                chs = sorted([f for f in os.listdir(ch_dir) if f.endswith(".md")])
                for ch in chs:
                    content = read_md(os.path.join(ch_dir, ch))
                    if content:
                        parts.append((ch, content))
                        stats["chapters"] += 1
            # 附录
            for ap in vol.get("appendix_files", []):
                content = read_md(ap)
                if content:
                    parts.append((os.path.basename(ap), content))
                    stats["appendices"] += 1
    elif book_key.startswith("workbuddy-"):
        # 单卷 workbuddy(单卷配置已有 chapters_dir)
        ch_dir = cfg.get("chapters_dir")
        if ch_dir and os.path.isdir(ch_dir):
            chs = sorted([f for f in os.listdir(ch_dir) if f.endswith(".md")])
            for ch in chs:
                content = read_md(os.path.join(ch_dir, ch))
                if content:
                    parts.append((ch, content))
                    stats["chapters"] += 1
        for ap in cfg.get("appendix_files", []):
            content = read_md(ap)
            if content:
                parts.append((os.path.basename(ap), content))
                stats["appendices"] += 1
    else:
        ch_dir = cfg.get("chapters_dir")
        if ch_dir and os.path.isdir(ch_dir):
            chs = sorted([f for f in os.listdir(ch_dir) if f.endswith(".md")])
            for ch in chs:
                content = read_md(os.path.join(ch_dir, ch))
                if content:
                    parts.append((ch, content))
                    stats["chapters"] += 1
        for ap in cfg.get("appendix_files", []):
            content = read_md(ap)
            if content:
                parts.append((os.path.basename(ap), content))
                stats["appendices"] += 1

    # 3. outro pages
    for title, path in cfg.get("outro_pages", []):
        if path.endswith(".png") or path.endswith(".jpg"):
            # 嵌入图片(用 markdown 语法)
            rel = os.path.basename(path)
            parts.append((title, f"![{title}]({rel})\n"))
        else:
            content = read_md(path)
            if content:
                parts.append((title, content))
                stats["outro_pages"] += 1

    # 合并
    merged = []
    for i, (title, content) in enumerate(parts):
        if i > 0:
            merged.append("\n\n---\n\n")
        merged.append(content)

    full = "".join(merged)
    stats["word_count"] = len(re.findall(r'\S', full))

    # 统计图引用
    fig_refs = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', full)
    stats["figure_refs"] = fig_refs

    return full, stats


def write_main_md(book_key: str, md_text: str):
    """写 main.md 到 dist/"""
    cfg = BOOKS[book_key]
    out_dir = cfg["dist_dir"]
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "main.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md_text)
    return out_path


# ==================== EPUB 构建 ====================

EPUB_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="{lang}">
<head>
<meta charset="utf-8"/>
<title>{title}</title>
<link rel="stylesheet" type="text/css" href="../styles/main.css"/>
</head>
<body>
{body}
</body>
</html>"""

EPUB_CSS = """body {
    font-family: "PingFang SC", "Microsoft YaHei", "Helvetica Neue", sans-serif;
    line-height: 1.7;
    color: #2D2D2D;
    background: #FAF7F0;
    margin: 2em;
    font-size: 1em;
}
h1, h2, h3, h4, h5, h6 { color: #0F4C81; margin-top: 1.5em; }
h1 { font-size: 2em; border-bottom: 2px solid #0F4C81; padding-bottom: 0.3em; }
h2 { font-size: 1.6em; border-bottom: 1px solid #D8D2C5; padding-bottom: 0.2em; }
h3 { font-size: 1.3em; }
code { background: #F0EBE0; padding: 2px 6px; border-radius: 4px; font-family: ui-monospace, Menlo, monospace; font-size: 0.9em; }
pre { background: #F0EBE0; padding: 1em; border-radius: 6px; overflow-x: auto; }
pre code { background: none; padding: 0; }
blockquote { border-left: 4px solid #16A085; padding-left: 1em; color: #555; margin-left: 0; }
table { border-collapse: collapse; margin: 1em 0; width: 100%; }
th, td { border: 1px solid #D8D2C5; padding: 8px 12px; text-align: left; }
th { background: #F0EBE0; color: #0F4C81; }
img { max-width: 100%; height: auto; display: block; margin: 1em auto; }
hr { border: 0; border-top: 1px solid #D8D2C5; margin: 2em 0; }
"""

CONTAINER_XML = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""


def build_epub(book_key: str, md_text: str, md_parts: List[Tuple[str, str]]):
    """生成 EPUB,基于原生 zipfile"""
    cfg = BOOKS[book_key]
    out_dir = cfg["dist_dir"]
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{book_key}.epub")

    md_obj = md_lib.Markdown(extensions=['extra', 'tables', 'fenced_code'])
    html_body = md_obj.convert(md_text)

    # EPUB 3.0 结构
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        # mimetype (必须,无压缩)
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)

        # META-INF/container.xml
        z.writestr("META-INF/container.xml", CONTAINER_XML)

        # styles
        z.writestr("OEBPS/styles/main.css", EPUB_CSS)

        # content
        z.writestr("OEBPS/cover.xhtml", _xhtml_cover(book_key))

        # 章节 XHTML (用 main.md 整个当一个 chapter,简化处理)
        z.writestr("OEBPS/main.xhtml", EPUB_TEMPLATE.format(
            lang=cfg["language"], title=cfg["title"], body=html_body))

        # 嵌入 cover.png
        if os.path.exists(cfg["cover"]):
            z.write(cfg["cover"], "OEBPS/images/cover.png")

        # content.opf
        z.writestr("OEBPS/content.opf", _opf(book_key))

        # toc.ncx (EPUB2 兼容)
        z.writestr("OEBPS/toc.ncx", _ncx(book_key))

        # nav.xhtml (EPUB3 标准导航)
        z.writestr("OEBPS/nav.xhtml", _nav_xhtml(book_key))

    return out_path


def _xhtml_cover(book_key: str) -> str:
    cfg = BOOKS[book_key]
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="{cfg["language"]}">
<head><meta charset="utf-8"/><title>封面</title>
<link rel="stylesheet" type="text/css" href="styles/main.css"/></head>
<body>
<div style="text-align:center; padding:2em 0;">
<img src="images/cover.png" alt="封面" style="max-width:90%;"/>
<h1>{cfg["title"]}</h1>
<h2>{cfg["subtitle"]}</h2>
<p style="color:#666;">{cfg["author"]} · {cfg["year"]}</p>
</div>
</body></html>"""


def _opf(book_key: str) -> str:
    cfg = BOOKS[book_key]
    m = cfg["metadata"]
    now = __import__('datetime').datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="BookId">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="BookId">{m["identifier"]}</dc:identifier>
<dc:title>{m["title"]}</dc:title>
<dc:creator>{m["creator"]}</dc:creator>
<dc:language>{m["language"]}</dc:language>
<dc:publisher>{m["publisher"]}</dc:publisher>
<dc:rights>{m["rights"]}</dc:rights>
<dc:description>{m["description"]}</dc:description>
<dc:subject>{m["subject"]}</dc:subject>
<dc:date>{cfg["year"]}-{cfg.get("release_month", "01")}-{cfg.get("release_day", "01")}</dc:date>
<meta property="dcterms:created">{cfg["year"]}-{cfg.get("release_month", "01")}-{cfg.get("release_day", "01")}T00:00:00Z</meta>
<meta property="dcterms:modified">{now}</meta>
<meta property="schema:version">v1.0.0</meta>
</metadata>
<manifest>
<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>
<item id="main" href="main.xhtml" media-type="application/xhtml+xml"/>
<item id="css" href="styles/main.css" media-type="text/css"/>
<item id="cover-img" href="images/cover.png" media-type="image/png" properties="cover-image"/>
<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
</manifest>
<spine toc="ncx">
<itemref idref="cover" linear="yes"/>
<itemref idref="main" linear="yes"/>
</spine>
</package>"""


def _nav_xhtml(book_key: str) -> str:
    """EPUB 3 nav 文档(EPUB3 现代阅读器优先用这个)"""
    cfg = BOOKS[book_key]
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="{cfg["language"]}">
<head>
<meta charset="utf-8"/>
<title>目录</title>
<link rel="stylesheet" type="text/css" href="styles/main.css"/>
</head>
<body>
<nav epub:type="toc" id="toc">
<h1>目录</h1>
<ol>
<li><a href="cover.xhtml">封面</a></li>
<li><a href="main.xhtml">正文</a></li>
</ol>
</nav>
<nav epub:type="landmarks" hidden="yes">
<h2>导航地标</h2>
<ol>
<li><a epub:type="cover" href="cover.xhtml">封面</a></li>
<li><a epub:type="bodymatter" href="main.xhtml">正文</a></li>
</ol>
</nav>
</body></html>"""


def _ncx(book_key: str) -> str:
    cfg = BOOKS[book_key]
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head><meta name="dtb:uid" content="{cfg['metadata']['identifier']}"/></head>
<docTitle><text>{cfg['title']}</text></docTitle>
<navMap>
<navPoint id="cover" playOrder="1"><navLabel><text>封面</text></navLabel><content src="cover.xhtml"/></navPoint>
<navPoint id="main" playOrder="2"><navLabel><text>正文</text></navLabel><content src="main.xhtml"/></navPoint>
</navMap>
</ncx>"""


# ==================== PDF 构建 ====================

def build_pdf(book_key: str, md_text: str):
    """生成 PDF(基于 reportlab + svglib) — 输出到书根目录"""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont

    cfg = BOOKS[book_key]
    out_dir = cfg["root_dir"]
    os.makedirs(out_dir, exist_ok=True)

    # 注册中文字体(reportlab 内置 STSong-Light)
    try:
        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
        chinese_font = 'STSong-Light'
    except Exception:
        chinese_font = 'Helvetica'

    out_path = os.path.join(out_dir, f"{book_key}.pdf")

    doc = SimpleDocTemplate(out_path, pagesize=A4,
                           leftMargin=2*cm, rightMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm,
                           title=cfg["title"], author=cfg["author"])

    # 样式
    styles = getSampleStyleSheet()
    body_style = ParagraphStyle(
        'Body', parent=styles['BodyText'],
        fontName=chinese_font, fontSize=10, leading=16,
        textColor=colors.HexColor("#2D2D2D"),
    )
    h1_style = ParagraphStyle(
        'H1', parent=styles['Heading1'],
        fontName=chinese_font, fontSize=22, leading=28,
        textColor=colors.HexColor("#0F4C81"),
        spaceAfter=12, spaceBefore=18,
    )
    h2_style = ParagraphStyle(
        'H2', parent=styles['Heading2'],
        fontName=chinese_font, fontSize=16, leading=22,
        textColor=colors.HexColor("#0F4C81"),
        spaceAfter=10, spaceBefore=14,
    )
    h3_style = ParagraphStyle(
        'H3', parent=styles['Heading3'],
        fontName=chinese_font, fontSize=13, leading=18,
        textColor=colors.HexColor("#16A085"),
        spaceAfter=8, spaceBefore=10,
    )

    story = []

    # 封面
    if os.path.exists(cfg["cover"]):
        try:
            img = Image(cfg["cover"], width=14*cm, height=14*cm, kind='proportional')
            story.append(img)
            story.append(Spacer(1, 1*cm))
        except Exception as e:
            story.append(Paragraph(f"[封面图加载失败: {e}]", body_style))

    story.append(Paragraph(cfg["title"], h1_style))
    story.append(Paragraph(cfg["subtitle"], h2_style))
    story.append(Paragraph(f"{cfg['author']} · {cfg['year']}", body_style))
    story.append(PageBreak())

    # 内容流
    flow = _md_to_flowables(md_text, chinese_font, body_style, h1_style, h2_style, h3_style, cfg)
    story.extend(flow)

    doc.build(story)
    return out_path


def _md_to_flowables(md_text: str, font, body_style, h1_style, h2_style, h3_style, cfg):
    """md → reportlab flowables 流"""
    from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle, PageBreak, Flowable
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF, renderPM

    flow = []

    code_style = ParagraphStyle(
        'Code', parent=body_style, fontName='Courier',
        fontSize=8, leading=12, textColor=colors.HexColor("#2D2D2D"),
        backColor=colors.HexColor("#F0EBE0"), borderPadding=6, leftIndent=10,
    )
    quote_style = ParagraphStyle(
        'Quote', parent=body_style, fontName=font,
        leftIndent=20, rightIndent=20,
        textColor=colors.HexColor("#555555"),
    )

    lines = md_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        # 跳过空行
        if not line.strip():
            flow.append(Spacer(1, 0.3*cm))
            i += 1
            continue

        # 分隔线
        if line.strip() == "---":
            from reportlab.platypus import HRFlowable
            flow.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#D8D2C5"),
                                  spaceBefore=10, spaceAfter=10))
            i += 1
            continue

        # 标题
        if line.startswith("# "):
            text = line[2:].strip()
            text = _escape_xml(text)
            flow.append(Paragraph(text, h1_style))
            i += 1
            continue
        if line.startswith("## "):
            text = line[3:].strip()
            text = _escape_xml(text)
            flow.append(Paragraph(text, h2_style))
            i += 1
            continue
        if line.startswith("### "):
            text = line[4:].strip()
            text = _escape_xml(text)
            flow.append(Paragraph(text, h3_style))
            i += 1
            continue

        # 图片
        m = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line)
        if m:
            alt, path = m.group(1), m.group(2)
            # 解析路径:相对路径 → 绝对路径
            abs_path = _resolve_img_path(path, cfg)
            if abs_path and os.path.exists(abs_path):
                try:
                    if abs_path.endswith(".svg"):
                        # SVG → svglib → reportlab Flowable
                        drawing = svg2rlg(open(abs_path).read())
                        if drawing:
                            # 缩放到 14cm 宽(默认 1200 = 14cm 等比例)
                            scale = 14 * cm / drawing.width
                            drawing.scale(scale, scale)
                            drawing.width = 14 * cm
                            drawing.height = drawing.height * scale

                            class SvgFlowable(Flowable):
                                def __init__(self, dr):
                                    Flowable.__init__(self)
                                    self.dr = dr
                                    self.width = dr.width
                                    self.height = dr.height
                                def draw(self):
                                    self.dr.drawOn(self.canv, 0, 0)
                            flow.append(SvgFlowable(drawing))
                        else:
                            flow.append(Paragraph(f"[SVG 解析失败: {alt}]", body_style))
                    else:
                        # PNG / JPG
                        img = Image(abs_path, width=14*cm, height=14*cm, kind='proportional')
                        flow.append(img)
                except Exception as e:
                    flow.append(Paragraph(f"[图片加载失败: {alt} ({e})]", body_style))
            else:
                flow.append(Paragraph(f"[图片缺失: {alt}]({path})", body_style))
            i += 1
            continue

        # 表格(简化:按行渲染,识别 |---| 分隔)
        if "|" in line and i + 1 < len(lines) and re.match(r'^\|[\s\-:|]+\|\s*$', lines[i + 1]):
            table_lines = [line]
            i += 1
            # 第一行表头
            # 第二行分隔
            table_lines.append(lines[i])
            i += 1
            # 数据行(必须跟表头同列数)
            header_cols = len([c for c in line.strip().strip('|').split('|')])
            while i < len(lines) and "|" in lines[i]:
                cols = len([c for c in lines[i].strip().strip('|').split('|')])
                if cols != header_cols:
                    break  # 不一致,停止表格收集
                table_lines.append(lines[i])
                i += 1
            flow.append(_render_table(table_lines, body_style))
            continue

        # 引用
        if line.startswith("> "):
            text = line[2:].strip()
            text = _escape_xml(text)
            flow.append(Paragraph(text, quote_style))
            i += 1
            continue

        # 列表
        if re.match(r'^[\-\*\+] ', line):
            text = line
            while i < len(lines) and re.match(r'^\s*[\-\*\+] |^\s*\d+\. ', lines[i]):
                text += "\n" + lines[i]
                i += 1
            text = _escape_xml(text)
            text = text.replace("\n", "<br/>")
            flow.append(Paragraph(text, body_style))
            continue

        # 代码块
        if line.startswith("```"):
            lang = line[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # 跳结束 ```
            code = "\n".join(code_lines)
            code = _escape_xml(code)
            flow.append(Paragraph(code, code_style))
            continue

        # 普通段落(合并连续行)
        para_lines = [line]
        i += 1
        while i < len(lines):
            nxt = lines[i].rstrip()
            if not nxt or nxt.startswith("#") or nxt.startswith(">") or \
               nxt.startswith("```") or nxt.startswith("---") or \
               nxt.startswith("!") or nxt.startswith("|") or \
               re.match(r'^[\-\*\+] ', nxt):
                break
            para_lines.append(nxt)
            i += 1
        text = " ".join(para_lines)
        text = _escape_xml(text)
        # 简单加粗 **...**
        text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
        # 行内 code
        text = re.sub(r'`([^`]+)`', r'<font face="Courier">\1</font>', text)
        try:
            flow.append(Paragraph(text, body_style))
        except Exception:
            # 太长的行截断
            flow.append(Paragraph(text[:5000], body_style))

    return flow


def _render_table(table_lines, body_style):
    from reportlab.platypus import Table, TableStyle, Paragraph
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle

    # 第一行是表头,第二行是分隔(跳过)
    rows = []
    cell_style = ParagraphStyle('Cell', parent=body_style, fontSize=8, leading=11)

    # 标准化:所有行补齐到统一列数
    expected_cols = max(len([c for c in ln.strip().strip('|').split('|')]) for ln in table_lines)

    for j, ln in enumerate(table_lines):
        if j == 1 and re.match(r'^\|[\s\-:|]+\|\s*$', ln.strip()):
            continue
        cells = [c.strip() for c in ln.strip().strip('|').split('|')]
        # 补齐到 expected_cols
        while len(cells) < expected_cols:
            cells.append("")
        cells = [_escape_xml(c)[:500] for c in cells]  # 截断防止溢出
        cells = [Paragraph(c, cell_style) for c in cells]
        rows.append(cells)

    if not rows or len(rows) < 2:
        return Paragraph("", body_style)

    if not rows:
        return Paragraph("", body_style)

    # 强制每列宽度相等,避免 negative availWidth
    from reportlab.lib.units import cm
    avail_w = 17 * cm
    n_cols = max(len(rows[0]), 1)
    col_w = avail_w / n_cols
    col_widths = [col_w] * n_cols

    t = Table(rows, colWidths=col_widths, hAlign='LEFT', repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0EBE0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#0F4C81")),
        ('FONTNAME', (0, 0), (-1, -1), body_style.fontName),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D8D2C5")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    return t


def _escape_xml(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _resolve_img_path(rel_path: str, cfg) -> Optional[str]:
    """把 md 里的图片路径解析到绝对路径

    支持扩展名适配:.png 引用但实际是 .svg 时自动切换
    """
    # 0. 扩展名适配:如果 .png 不存在但 .svg 存在,切换
    candidates_ext = [rel_path]
    if rel_path.endswith(".png"):
        svg_alt = rel_path[:-4] + ".svg"
        candidates_ext.insert(0, svg_alt)
    elif rel_path.endswith(".jpg") or rel_path.endswith(".jpeg"):
        candidates_ext.insert(0, rel_path[:-4] + ".svg")

    # 1. 在 root_dir 里找
    for rel in candidates_ext:
        for base in [
            cfg["root_dir"],
            os.path.dirname(cfg.get("chapters_dir", cfg["root_dir"])),
        ]:
            if not base:
                continue
            for cand in [
                os.path.join(base, rel),
                os.path.join(base, rel.replace("../", "")),
                os.path.join(base, rel.replace("../../", "")),
            ]:
                if os.path.exists(cand):
                    return cand

    # 2. workbuddy 多卷:在每个 volume 的 figures 里找
    if cfg.get("volumes"):
        for vol in cfg["volumes"]:
            for rel in candidates_ext:
                for base in [vol["chapters_dir"], vol["figures_dir"]]:
                    if not base:
                        continue
                    cand = os.path.join(base, "..", rel)
                    if os.path.exists(cand):
                        return cand

    # 3. 在 promotion 里找(二维码 / 封面)
    name = os.path.basename(rel_path)
    for sub in ["promotion", "assets"]:
        candidate = os.path.join(cfg["root_dir"], sub, name)
        if os.path.exists(candidate):
            return candidate

    # 4. 直接路径
    if os.path.exists(rel_path):
        return rel_path

    return None


# ==================== DOCX 构建 ====================

def build_docx(book_key: str, md_text: str):
    """生成 docx(简化版)"""
    try:
        from docx import Document
        from docx.shared import Inches, Pt, RGBColor
        from docx.enum.text import WD_ALIGN_PARAGRAPH
    except ImportError:
        return None

    cfg = BOOKS[book_key]
    out_dir = cfg["dist_dir"]
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{book_key}.docx")

    doc = Document()
    doc.core_properties.title = cfg["title"]
    doc.core_properties.author = cfg["author"]
    doc.core_properties.subject = cfg["metadata"].get("subject", "")

    # 封面
    if os.path.exists(cfg["cover"]):
        try:
            doc.add_picture(cfg["cover"], width=Inches(4.5))
            last_para = doc.paragraphs[-1]
            last_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        except Exception:
            pass

    p = doc.add_heading(cfg["title"], 0)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = doc.add_paragraph(cfg["subtitle"])
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = doc.add_paragraph(f"{cfg['author']} · {cfg['year']}")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_page_break()

    # 内容流
    for line in md_text.split("\n"):
        line = line.rstrip()
        if not line:
            doc.add_paragraph("")
        elif line.startswith("# "):
            doc.add_heading(line[2:].strip(), 1)
        elif line.startswith("## "):
            doc.add_heading(line[3:].strip(), 2)
        elif line.startswith("### "):
            doc.add_heading(line[4:].strip(), 3)
        elif line.startswith("> "):
            p = doc.add_paragraph(line[2:].strip(), style="Intense Quote")
        elif line.startswith("```"):
            continue  # 简化跳过代码块
        elif line.startswith("!["):
            # 图片
            m = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line)
            if m:
                alt, path = m.group(1), m.group(2)
                abs_path = _resolve_img_path(path, cfg)
                if abs_path and os.path.exists(abs_path) and not abs_path.endswith(".svg"):
                    try:
                        doc.add_picture(abs_path, width=Inches(5))
                    except Exception:
                        doc.add_paragraph(f"[图片: {alt}]")
                else:
                    doc.add_paragraph(f"[图片: {alt}]")
        elif line.startswith("|") and "|" in line:
            doc.add_paragraph(line.replace("|", " | "))  # 简化表格
        else:
            doc.add_paragraph(line)

    doc.save(out_path)
    return out_path


# ==================== 主入口 ====================

def build_book(book_key: str, formats: List[str] = None):
    """构建一本书的全部产物

    默认只生成 PDF(最终交付物,放书根)
    md 是中间产物(合并所有章),放 dist
    epub / docx 不再生成(已从交付物列表移除)
    """
    if formats is None:
        formats = ["md", "pdf"]

    cfg = BOOKS[book_key]
    print(f"\n📖 构建 {cfg['title']}...")

    # workbuddy 是多卷结构:每卷单独打包
    if book_key == "workbuddy":
        return build_workbuddy_volumes(formats)

    # 1. 合并 markdown
    md_text, stats = assemble_markdown(book_key)
    print(f"  ✓ 合并 markdown: {stats['chapters']} 章 + {stats['appendices']} 附录 "
          f"({stats['word_count']} 字符, {len(stats['figure_refs'])} 图引用)")

    results = {}

    if "md" in formats:
        path = write_main_md(book_key, md_text)
        results["md"] = path
        print(f"  ✓ main.md → {path}")

    if "pdf" in formats:
        path = build_pdf(book_key, md_text)
        results["pdf"] = path
        print(f"  ✓ PDF → {path} ({os.path.getsize(path)/1024:.1f} KB)")

    return results, stats


def build_workbuddy_volumes(formats: List[str]):
    """workbuddy 是三卷结构:分别生成每卷的产物"""
    cfg = BOOKS["workbuddy"]
    all_results = {}
    all_stats = {"chapters": 0, "appendices": 0, "intro_pages": 0, "outro_pages": 0,
                 "word_count": 0, "figure_refs": [], "volumes": []}

    for vol in cfg["volumes"]:
        # 把单卷作为独立"book"打包
        vol_key = f"workbuddy-{vol['name']}"
        vol_cfg = {
            "title": vol["title"],
            "subtitle": vol["subtitle"],
            "author": cfg["author"],
            "year": cfg["year"],
            "language": cfg["language"],
            "cover": cfg["cover"],
            "root_dir": cfg["root_dir"],
            "chapters_dir": vol["chapters_dir"],
            "appendices_dir": vol.get("appendices_dir"),
            "appendix_files": vol.get("appendix_files", []),
            "dist_dir": cfg["dist_dir"],
            "intro_pages": cfg.get("intro_pages", []),
            "outro_pages": cfg.get("outro_pages", []),
            "metadata": {
                "title": vol["title"],
                "creator": cfg["author"],
                "language": cfg["language"],
                "subject": f"WorkBuddy {vol['name']}",
                "description": vol["subtitle"],
                "publisher": cfg["publisher"],
                "rights": cfg["metadata"]["rights"],
                "identifier": {
                    "第一卷": "urn:uuid:027c99d0-b11c-5b19-a363-d5a39e9a2f39",
                    "第二卷": "urn:uuid:f6967cab-2430-5908-a0a4-a0e3570c13f0",
                    "第三卷": "urn:uuid:10998eb2-cb9f-503c-b8c7-90fc13dd9bdf",
                }.get(vol["name"], f"books://workbuddy/{vol['name']}"),
            }
        }
        # 临时注册单卷
        BOOKS[vol_key] = vol_cfg

        print(f"\n  📘 {vol['name']}: {vol['title']}")

        # 合并该卷 markdown
        md_text, stats = assemble_markdown(vol_key)
        print(f"    ✓ 合并: {stats['chapters']} 章 + {stats['appendices']} 附录 "
              f"({stats['word_count']} 字符)")

        slug = vol.get("out_slug", vol['name'])

        if "md" in formats:
            path = os.path.join(cfg["dist_dir"], f"{slug}.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(md_text)
            print(f"    ✓ {slug}.md → {path}")
            all_results[f"{slug}.md"] = path

        if "pdf" in formats:
            path = build_pdf_for_vol(vol_key, md_text, slug)
            print(f"    ✓ {slug}.pdf → {path} ({os.path.getsize(path)/1024:.1f} KB)")
            all_results[f"{slug}.pdf"] = path

        all_stats["chapters"] += stats["chapters"]
        all_stats["appendices"] += stats["appendices"]
        all_stats["word_count"] += stats["word_count"]
        all_stats["figure_refs"].extend(stats["figure_refs"])
        all_stats["volumes"].append(vol['name'])

        # 清理临时注册
        del BOOKS[vol_key]

    # 三卷合一 markdown
    if "md" in formats:
        merged_path = os.path.join(cfg["dist_dir"], "workbuddy.md")
        merged_parts = []
        for vol in cfg["volumes"]:
            md_path = os.path.join(cfg["dist_dir"], f"{vol.get('out_slug', vol['name'])}.md")
            if os.path.exists(md_path):
                with open(md_path, "r", encoding="utf-8") as f:
                    merged_parts.append(f.read())
        with open(merged_path, "w", encoding="utf-8") as f:
            f.write("\n\n---\n\n".join(merged_parts))
        print(f"  ✓ workbuddy.md (合订) → {merged_path}")
        all_results["workbuddy.md"] = merged_path

    return all_results, all_stats


def build_epub_for_vol(vol_key: str, md_text: str, slug: str):
    """单卷 EPUB"""
    cfg = BOOKS[vol_key]
    out_dir = cfg["dist_dir"]
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{slug}.epub")

    md_obj = md_lib.Markdown(extensions=['extra', 'tables', 'fenced_code'])
    html_body = md_obj.convert(md_text)

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", CONTAINER_XML)
        z.writestr("OEBPS/styles/main.css", EPUB_CSS)
        z.writestr("OEBPS/cover.xhtml", _xhtml_cover(vol_key))
        z.writestr("OEBPS/main.xhtml", EPUB_TEMPLATE.format(
            lang=cfg["language"], title=cfg["title"], body=html_body))
        if os.path.exists(cfg["cover"]):
            z.write(cfg["cover"], "OEBPS/images/cover.png")
        z.writestr("OEBPS/content.opf", _opf(vol_key))
        z.writestr("OEBPS/toc.ncx", _ncx(vol_key))
        z.writestr("OEBPS/nav.xhtml", _nav_xhtml(vol_key))

    return out_path


def build_pdf_for_vol(vol_key: str, md_text: str, slug: str):
    """单卷 PDF — 输出到书根目录"""
    cfg = BOOKS[vol_key]
    out_dir = cfg["root_dir"]
    os.makedirs(out_dir, exist_ok=True)

    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont

    try:
        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
        chinese_font = 'STSong-Light'
    except Exception:
        chinese_font = 'Helvetica'

    out_path = os.path.join(out_dir, f"{slug}.pdf")
    doc = SimpleDocTemplate(out_path, pagesize=A4,
                           leftMargin=2*cm, rightMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm,
                           title=cfg["title"], author=cfg["author"])

    styles = getSampleStyleSheet()
    body_style = ParagraphStyle('Body', parent=styles['BodyText'],
        fontName=chinese_font, fontSize=10, leading=16,
        textColor=colors.HexColor("#2D2D2D"))
    h1_style = ParagraphStyle('H1', parent=styles['Heading1'],
        fontName=chinese_font, fontSize=22, leading=28,
        textColor=colors.HexColor("#0F4C81"), spaceAfter=12, spaceBefore=18)
    h2_style = ParagraphStyle('H2', parent=styles['Heading2'],
        fontName=chinese_font, fontSize=16, leading=22,
        textColor=colors.HexColor("#0F4C81"), spaceAfter=10, spaceBefore=14)
    h3_style = ParagraphStyle('H3', parent=styles['Heading3'],
        fontName=chinese_font, fontSize=13, leading=18,
        textColor=colors.HexColor("#16A085"), spaceAfter=8, spaceBefore=10)

    story = []
    if os.path.exists(cfg["cover"]):
        try:
            story.append(Image(cfg["cover"], width=14*cm, height=14*cm, kind='proportional'))
            story.append(Spacer(1, 1*cm))
        except Exception:
            pass
    story.append(Paragraph(cfg["title"], h1_style))
    story.append(Paragraph(cfg["subtitle"], h2_style))
    story.append(Paragraph(f"{cfg['author']} · {cfg['year']}", body_style))
    story.append(PageBreak())

    flow = _md_to_flowables(md_text, chinese_font, body_style, h1_style, h2_style, h3_style, cfg)
    story.extend(flow)

    doc.build(story)
    return out_path


def build_docx_for_vol(vol_key: str, md_text: str, slug: str):
    """单卷 DOCX"""
    try:
        from docx import Document
        from docx.shared import Inches
        from docx.enum.text import WD_ALIGN_PARAGRAPH
    except ImportError:
        return None

    cfg = BOOKS[vol_key]
    out_dir = cfg["dist_dir"]
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{slug}.docx")

    doc = Document()
    doc.core_properties.title = cfg["title"]
    doc.core_properties.author = cfg["author"]

    if os.path.exists(cfg["cover"]):
        try:
            doc.add_picture(cfg["cover"], width=Inches(4.5))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        except Exception:
            pass
    p = doc.add_heading(cfg["title"], 0)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(cfg["subtitle"]).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(f"{cfg['author']} · {cfg['year']}").alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_page_break()

    for line in md_text.split("\n"):
        line = line.rstrip()
        if not line:
            doc.add_paragraph("")
        elif line.startswith("# "):
            doc.add_heading(line[2:].strip(), 1)
        elif line.startswith("## "):
            doc.add_heading(line[3:].strip(), 2)
        elif line.startswith("### "):
            doc.add_heading(line[4:].strip(), 3)
        elif line.startswith("> "):
            doc.add_paragraph(line[2:].strip(), style="Intense Quote")
        elif line.startswith("```"):
            continue
        elif line.startswith("!["):
            m = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line)
            if m:
                alt, path = m.group(1), m.group(2)
                abs_path = _resolve_img_path(path, cfg)
                if abs_path and os.path.exists(abs_path) and not abs_path.endswith(".svg"):
                    try:
                        doc.add_picture(abs_path, width=Inches(5))
                    except Exception:
                        doc.add_paragraph(f"[图片: {alt}]")
                else:
                    doc.add_paragraph(f"[图片: {alt}]")
        elif line.startswith("|") and "|" in line:
            doc.add_paragraph(line.replace("|", " | "))
        else:
            doc.add_paragraph(line)

    doc.save(out_path)
    return out_path


def main():
    """主入口"""
    print("=" * 60)
    print("📚 三本书打包 · 施可")
    print("=" * 60)

    all_results = {}
    for key in ["ai-coding", "fde", "workbuddy"]:
        results, stats = build_book(key, formats=["md", "epub", "pdf", "docx"])
        all_results[key] = (results, stats)

    print("\n" + "=" * 60)
    print("✅ 全部构建完成")
    print("=" * 60)
    for key, (results, stats) in all_results.items():
        print(f"\n{key}:")
        for fmt, path in results.items():
            print(f"  {fmt}: {path}")

    # 自动调 epub_validate 做一遍校验
    print("\n" + "=" * 60)
    print("🔍 自动 EPUB 结构校验")
    print("=" * 60)
    try:
        from epub_validate import check as epub_check
        epubs = []
        for key, (results, _) in all_results.items():
            if "epub" in results:
                epubs.append(results["epub"])
            else:
                # workbuddy 多卷:每卷一个 EPUB
                for vol in BOOKS["workbuddy"]["volumes"]:
                    slug = vol.get("out_slug", vol["name"])
                    p = os.path.join(BOOKS["workbuddy"]["dist_dir"], f"{slug}.epub")
                    if os.path.exists(p):
                        epubs.append(p)
        from pathlib import Path
        fatal_total = 0
        for p in epubs:
            issues, info = epub_check(Path(p))
            score_v = max(0, 100 - sum(20 if i.level == "FATAL" else 5 if i.level == "WARN" else 0 for i in issues))
            status = "✅" if not [i for i in issues if i.level == "FATAL"] else "❌"
            print(f"  {status} {os.path.basename(p):<30} 评分 {score_v}/100  "
                  f"nav={info['has_nav']} ncx={info['has_ncx']} "
                  f"id={info['identifier'][:40]}")
            fatal_total += len([i for i in issues if i.level == "FATAL"])
        if fatal_total == 0:
            print("\n  ✅ 全部 EPUB 通过")
        else:
            print(f"\n  ⚠️ {fatal_total} 个 FATAL 错误")
    except Exception as e:
        print(f"  ⚠️ 校验调用失败: {e}")


if __name__ == "__main__":
    main()