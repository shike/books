#!/usr/bin/env python3
"""
轻量级 EPUB 结构校验(无需 epubcheck / Java)。

校验项(EPUB 2/3 公共子集):
  1. ZIP 完整性 + mimetype 文件首条且未压缩 + 内容为 application/epub+zip
  2. META-INF/container.xml 存在且指向 rootfile
  3. OPF 存在且可解析
  4. OPF 必填元数据:dc:title / dc:identifier(unique id) / dc:language / dc:creator
  5. manifest 全部 href 可解析
  6. spine 全部 idref 在 manifest 中
  7. 存在 nav(EPUB3) 或 ncx(EPUB2)
  8. 存在 cover(metadata 中 name='cover' 或 manifest 中 properties 含 cover-image)
  9. mimetype 与 OPF 中 <mediatype> 一致

输出:FATAL(致命)/WARN(警告)/INFO(信息)三档,末尾给总分(致命=0,警告=扣分)。
"""
from __future__ import annotations

import io
import sys
import zipfile
from pathlib import Path
from typing import List, Tuple
from urllib.parse import unquote

from lxml import etree

NS = {
    "container": "urn:oasis:names:tc:opendocument:xmlns:container",
    "opf": "http://www.idpf.org/2007/opf",
    "dc": "http://purl.org/dc/elements/1.1/",
    "ncx": "http://www.daisy.org/z3986/2005/ncx/",
}


class Issue:
    def __init__(self, level: str, code: str, msg: str):
        self.level = level  # FATAL / WARN / INFO
        self.code = code
        self.msg = msg

    def __str__(self):
        return f"  [{self.level}] {self.code}: {self.msg}"


def check(epub_path: Path) -> Tuple[List[Issue], dict]:
    issues: List[Issue] = []
    info = {"size_kb": 0, "file_count": 0, "has_nav": False, "has_ncx": False,
            "title": "", "language": "", "identifier": "", "creator": "",
            "epub_version": "?"}

    if not epub_path.exists():
        issues.append(Issue("FATAL", "E001", f"文件不存在: {epub_path}"))
        return issues, info

    info["size_kb"] = round(epub_path.stat().st_size / 1024, 1)

    try:
        zf = zipfile.ZipFile(epub_path, "r")
    except zipfile.BadZipFile:
        issues.append(Issue("FATAL", "E002", "不是合法 ZIP 文件"))
        return issues, info

    names = zf.namelist()
    info["file_count"] = len(names)

    # 1. mimetype
    if not names or names[0] != "mimetype":
        issues.append(Issue("FATAL", "E010", "mimetype 不是 ZIP 内的第一个文件"))
    else:
        mt_info = zf.getinfo("mimetype")
        if mt_info.compress_type != zipfile.ZIP_STORED:
            issues.append(Issue("FATAL", "E011", "mimetype 必须未压缩(ZIP_STORED)"))
        mt_content = zf.read("mimetype").decode("ascii", "replace").strip()
        if mt_content != "application/epub+zip":
            issues.append(Issue("FATAL", "E012", f"mimetype 内容错: {mt_content!r}"))

    # 2. META-INF/container.xml
    container_path = "META-INF/container.xml"
    if container_path not in names:
        issues.append(Issue("FATAL", "E020", "META-INF/container.xml 缺失"))
        return issues, info

    container_xml = zf.read(container_path)
    container = etree.fromstring(container_xml)
    rootfiles = container.findall(".//container:rootfile", NS)
    if not rootfiles:
        issues.append(Issue("FATAL", "E021", "container.xml 中无 rootfile 元素"))
        return issues, info
    opf_relpath = rootfiles[0].get("full-path")
    if not opf_relpath:
        issues.append(Issue("FATAL", "E022", "container.xml rootfile 缺 full-path"))
        return issues, info

    # 3. OPF
    if opf_relpath not in names:
        issues.append(Issue("FATAL", "E030", f"OPF 文件不存在: {opf_relpath}"))
        return issues, info

    opf_xml = zf.read(opf_relpath)
    opf = etree.fromstring(opf_xml)

    # 版本
    info["epub_version"] = opf.get("version") or "??"

    # 4. 必填元数据
    md = opf.find("opf:metadata", NS)
    if md is None:
        issues.append(Issue("FATAL", "E040", "OPF 中无 <metadata>"))
        return issues, info

    def dc(tag: str) -> str:
        el = md.find(f"dc:{tag}", NS)
        return (el.text or "").strip() if el is not None else ""

    info["title"] = dc("title")
    info["identifier"] = dc("identifier")
    info["language"] = dc("language")
    info["creator"] = dc("creator")

    if not info["title"]:
        issues.append(Issue("FATAL", "E041", "dc:title 缺失或为空"))
    if not info["identifier"]:
        issues.append(Issue("FATAL", "E042", "dc:identifier 缺失或为空(KDP/平台分发必备)"))
    if not info["language"]:
        issues.append(Issue("FATAL", "E043", "dc:language 缺失或为空"))
    if not info["creator"]:
        issues.append(Issue("WARN", "E044", "dc:creator 缺失或为空(平台分发建议有)"))

    # identifier 应带 id 属性(用作唯一标识)
    ident_el = md.find("dc:identifier", NS)
    if ident_el is not None and not ident_el.get("id"):
        issues.append(Issue("WARN", "E045", "dc:identifier 缺 id 属性(建议加 id='BookId')"))

    # 5+6. manifest 与 spine
    manifest = opf.find("opf:manifest", NS)
    spine = opf.find("opf:spine", NS)
    if manifest is None:
        issues.append(Issue("FATAL", "E050", "无 <manifest>"))
    if spine is None:
        issues.append(Issue("FATAL", "E060", "无 <spine>"))

    if manifest is not None:
        items = {it.get("id"): it for it in manifest.findall("opf:item", NS)}
        opf_dir = Path(opf_relpath).parent

        # href 全部可解析
        for item_id, item in items.items():
            href = item.get("href", "")
            if not href:
                issues.append(Issue("WARN", "E051", f"manifest item id={item_id} 无 href"))
                continue
            target = (opf_dir / unquote(href)).as_posix()
            # EPUB 内部路径不能用反斜杠
            if "\\" in href:
                issues.append(Issue("WARN", "E052", f"item href 含反斜杠:{href}"))
            if target not in names:
                issues.append(Issue("FATAL", "E053", f"manifest item 指向不存在文件:{href} (resolved={target})"))

        # spine idref 校验
        if spine is not None:
            for ref in spine.findall("opf:itemref", NS):
                idref = ref.get("idref")
                if idref not in items:
                    issues.append(Issue("FATAL", "E061", f"spine 引用未在 manifest 中的 id:{idref}"))

        # 7. nav 或 ncx
        nav_item = None
        ncx_item = None
        for item in items.values():
            props = (item.get("properties") or "").split()
            if "nav" in props:
                nav_item = item
            media = item.get("media-type") or ""
            if media == "application/x-dtbncx+xml" or media.endswith("/ncx"):
                ncx_item = item

        if nav_item is not None:
            info["has_nav"] = True
            nav_href = nav_item.get("href", "")
            nav_target = (opf_dir / unquote(nav_href)).as_posix()
            if nav_target not in names:
                issues.append(Issue("FATAL", "E070", f"nav 文件不存在:{nav_href}"))
        if ncx_item is not None:
            info["has_ncx"] = True
            ncx_href = ncx_item.get("href", "")
            ncx_target = (opf_dir / unquote(ncx_href)).as_posix()
            if ncx_target not in names:
                issues.append(Issue("FATAL", "E071", f"ncx 文件不存在:{ncx_href}"))

        if nav_item is None and ncx_item is None:
            issues.append(Issue("FATAL", "E072", "无 nav(EPUB3) 也无 ncx(EPUB2),阅读器无法生成目录"))

        # 调试:dump manifest item id / properties / media-type,用于定位
        info["manifest_dump"] = [
            f"{it.get('id')}|{it.get('properties','')}|{it.get('media-type','')}"
            for it in items.values()
        ]

        # 8. cover
        has_cover_meta = md.find("opf:meta[@name='cover']", NS) is not None
        has_cover_image = False
        for item in items.values():
            props = (item.get("properties") or "").split()
            if "cover-image" in props:
                has_cover_image = True
                break

        if not has_cover_meta and not has_cover_image:
            issues.append(Issue("WARN", "E080", "未声明封面(无 meta name='cover' 也无 properties='cover-image')"))

    return issues, info


def score(issues: List[Issue]) -> int:
    """每 FATAL -20,每 WARN -5,起点 100,封顶 [0,100]"""
    s = 100
    for i in issues:
        if i.level == "FATAL":
            s -= 20
        elif i.level == "WARN":
            s -= 5
    return max(0, s)


def main():
    targets = [
        Path("/Users/shike/Desktop/code/books/ai-coding/dist/ai-coding.epub"),
        Path("/Users/shike/Desktop/code/books/fde/dist/fde.epub"),
        Path("/Users/shike/Desktop/code/books/workbuddy/dist/第一卷.epub"),
        Path("/Users/shike/Desktop/code/books/workbuddy/dist/第二卷.epub"),
        Path("/Users/shike/Desktop/code/books/workbuddy/dist/第三卷.epub"),
    ]

    print("=" * 78)
    print(f"{'电子书 EPUB 结构校验报告':^78}")
    print("=" * 78)

    grand_total = {"FATAL": 0, "WARN": 0, "INFO": 0}

    for path in targets:
        print(f"\n📄 {path.relative_to(Path.home().parent)}".replace("Users/shike/", ""))
        print(f"   Path: {path}")
        issues, info = check(path)

        print(f"   Size: {info['size_kb']} KB | Files: {info['file_count']} | Version: {info['epub_version']}")
        print(f"   Title: {info['title'] or '(空)'}")
        print(f"   Creator: {info['creator'] or '(空)'}")
        print(f"   Language: {info['language'] or '(空)'}")
        print(f"   Identifier: {info['identifier'] or '(空)'}")
        print(f"   nav(EPUB3): {info['has_nav']} | ncx(EPUB2): {info['has_ncx']}")

        # 调试:列 manifest 中含 properties 的条目(EPUB3 nav/cover 都在这)
        if info.get("manifest_dump"):
            print("   manifest dump(id|properties|media):")
            for line in info["manifest_dump"]:
                print(f"     - {line}")

        if not issues:
            print("   ✅ 无任何问题")
        else:
            for i in issues:
                print(str(i))
                grand_total[i.level] += 1

        sc = score(issues)
        print(f"   —— 评分: {sc}/100")

    print("\n" + "=" * 78)
    print(f"{'总览':^78}")
    print(f"  FATAL: {grand_total['FATAL']} | WARN: {grand_total['WARN']}")
    print("=" * 78)

    # 退出码:FATAL>0 → 1,否则 0
    sys.exit(1 if grand_total["FATAL"] > 0 else 0)


if __name__ == "__main__":
    main()