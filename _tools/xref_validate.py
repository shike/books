#!/usr/bin/env python3
"""
跨章节引用校验器。

扫描三本书的所有章节 md,检查:
  1. 图片引用 (![alt](path)) - 文件是否存在(支持扩展名适配 png ↔ svg)
  2. 跨章节引用 ([text](other.md)) - 文件是否存在
  3. 锚点引用 ([text](#anchor)) - 仅记录,不深查

输出:FATAL(找不到)/WARN(锚点)/INFO(统计) + 总分
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/Users/shike/Desktop/code/books")

BOOKS = {
    "ai-coding": {
        "chapters_dir": ROOT / "ai-coding" / "chapters",
        "appendices_dir": ROOT / "ai-coding" / "appendices",
        "figures_dir": ROOT / "ai-coding" / "figures",
        "assets_prompts": ROOT / "ai-coding" / "assets" / "prompts",
    },
    "fde": {
        "chapters_dir": ROOT / "fde" / "chapters",
        "appendices_dir": ROOT / "fde" / "appendices",
        "figures_dir": ROOT / "fde" / "figures",
    },
    "workbuddy-vol1": {
        "chapters_dir": ROOT / "workbuddy" / "第一卷" / "chapters",
        "appendices_dir": ROOT / "workbuddy" / "第一卷" / "appendices",
        "figures_dir": ROOT / "workbuddy" / "第一卷" / "figures",
    },
    "workbuddy-vol2": {
        "chapters_dir": ROOT / "workbuddy" / "第二卷" / "chapters",
        "appendices_dir": ROOT / "workbuddy" / "第二卷" / "appendices",
        "figures_dir": ROOT / "workbuddy" / "第二卷" / "figures",
    },
    "workbuddy-vol3": {
        "chapters_dir": ROOT / "workbuddy" / "第三卷" / "chapters",
        "appendices_dir": ROOT / "workbuddy" / "第三卷" / "appendices",
        "figures_dir": ROOT / "workbuddy" / "第三卷" / "figures",
    },
}

IMG_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
LINK_RE = re.compile(r'(?<!!)\[([^\]]*)\]\(([^)]+)\)')


def check_file(md_path: Path, cfg: dict) -> tuple[list, list]:
    """检查单个 md 文件,返回 (img_issues, link_issues)。"""
    img_issues = []
    link_issues = []

    if not md_path.exists():
        return img_issues, link_issues

    text = md_path.read_text(encoding="utf-8", errors="replace")

    # 1. 图片引用
    for alt, ref in IMG_RE.findall(text):
        if ref.startswith(("http://", "https://", "data:")):
            continue
        if ref.startswith("#"):
            continue
        # 去掉可选标题 `path "title"`
        ref = ref.split()[0] if " " in ref else ref
        resolved = resolve_path(md_path, ref, cfg)
        if not resolved:
            img_issues.append((md_path, ref, alt))

    # 2. 跨章节 .md 链接
    for text_, ref in LINK_RE.findall(text):
        if ref.startswith(("http://", "https://", "data:", "mailto:")):
            continue
        if ref.startswith("#"):
            continue
        # 跳过 .png/.svg/.jpg(已经是图引用了,链接形态的图不常见)
        if ref.endswith((".png", ".svg", ".jpg", ".jpeg", ".webp", ".gif")):
            continue
        ref_clean = ref.split()[0] if " " in ref else ref
        # 去掉 #anchor
        if "#" in ref_clean:
            ref_clean = ref_clean.split("#")[0]
        if not ref_clean:
            continue
        # 只关心 .md 链接
        if not ref_clean.endswith(".md"):
            continue
        resolved = resolve_path(md_path, ref_clean, cfg)
        if not resolved:
            link_issues.append((md_path, ref_clean, text_))

    return img_issues, link_issues


def resolve_path(md_path: Path, rel: str, cfg: dict) -> Path | None:
    """解析相对路径,允许 ../figures/xxx.png 或 ../../其他目录。"""
    base = md_path.parent
    # 直接解析
    candidates = [
        base / rel,
        base / rel.replace("../", ""),
    ]
    # 处理 ../ 路径,逐级上升
    p = (base / rel).resolve()
    if p.exists():
        return p

    # 扩展名适配:.png → .svg
    if rel.endswith(".png"):
        svg_alt = rel[:-4] + ".svg"
        for c in [base / svg_alt, (base / svg_alt).resolve()]:
            if c.exists():
                return c
    elif rel.endswith(".svg"):
        png_alt = rel[:-4] + ".png"
        for c in [base / png_alt, (base / png_alt).resolve()]:
            if c.exists():
                return c

    return None


def main():
    print("=" * 78)
    print(f"{'跨章节引用校验':^78}")
    print("=" * 78)

    grand = {"img_broken": 0, "link_broken": 0, "files_checked": 0, "img_total": 0, "link_total": 0}

    for book_key, cfg in BOOKS.items():
        print(f"\n📚 {book_key}")

        # 扫描所有 md 文件
        md_files = []
        for d in [cfg.get("chapters_dir"), cfg.get("appendices_dir")]:
            if d and d.exists():
                md_files.extend(sorted(d.glob("*.md")))

        for md_path in md_files:
            grand["files_checked"] += 1
            img_issues, link_issues = check_file(md_path, cfg)

            # 统计总引用
            text = md_path.read_text(encoding="utf-8", errors="replace")
            grand["img_total"] += len(IMG_RE.findall(text))
            grand["link_total"] += len(LINK_RE.findall(text))

            for f, ref, alt in img_issues:
                grand["img_broken"] += 1
                print(f"   ❌ [IMG] {f.name}: {ref} (alt='{alt}')")
            for f, ref, text_ in link_issues:
                grand["link_broken"] += 1
                print(f"   ❌ [LINK] {f.name}: {ref} (text='{text_}')")

        # 章节数汇总
        n_chs = len(list(cfg["chapters_dir"].glob("*.md"))) if cfg.get("chapters_dir") else 0
        n_aps = len(list(cfg["appendices_dir"].glob("*.md"))) if cfg.get("appendices_dir") else 0
        print(f"   ✓ 扫描: {n_chs} 章 + {n_aps} 附录")

    print(f"\n{'=' * 78}")
    print(f"{'汇总':^78}")
    print(f"  文件扫描: {grand['files_checked']}")
    print(f"  图片引用: {grand['img_total']} 个(损坏: {grand['img_broken']})")
    print(f"  章节链接: {grand['link_total']} 个(损坏: {grand['link_broken']})")
    print(f"{'=' * 78}")

    return 0 if (grand["img_broken"] + grand["link_broken"]) == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())