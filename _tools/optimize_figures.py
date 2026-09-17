#!/usr/bin/env python3
"""
PNG 配图优化器。

策略:
  - 输入:任何 PNG > 1 MB
  - 操作:等比例缩放到 ≤ 1600 px 宽(质量保留),保存为 optimize=True
  - 二次尝试:若仍 > 1 MB,降到 quality=85
  - 兜底:若仍 > 1 MB,记录但不进一步压缩(避免损失过大)

设计原则:截图/示意图最大边 1600px 既满足 Web/电子书/EPUB 多种用途(视网膜屏 2x),
也足以看清细节;AGENTS.md 1.3 已规定"最大宽度 1600px"作为约定。
"""
from __future__ import annotations

import os
from pathlib import Path

from PIL import Image

ROOT = Path("/Users/shike/Desktop/code/books")

# 阈值
SIZE_THRESHOLD = 1024 * 1024  # 1 MB
MAX_WIDTH = 1600  # px
QUALITY_HIGH = 95
QUALITY_MID = 85


def is_png(p: Path) -> bool:
    return p.suffix.lower() == ".png"


def optimize_one(p: Path) -> tuple[int, int, str]:
    """优化单个 PNG,返回 (原大小, 新大小, 状态)。"""
    orig_size = p.stat().st_size
    if orig_size < SIZE_THRESHOLD:
        return orig_size, orig_size, "skip(<1MB)"

    im = Image.open(p)
    orig_mode = im.mode
    if orig_mode in ("RGBA", "LA", "P"):
        # 转 RGB 避免 PNG 透明通道不被 JPG 兼容,但这是 PNG 优化,
        # 所以保持原模式,只处理调色板
        if orig_mode == "P":
            im = im.convert("RGBA")
            orig_mode = "RGBA"

    # 等比例缩放
    w, h = im.size
    if w > MAX_WIDTH:
        new_h = int(h * MAX_WIDTH / w)
        im = im.resize((MAX_WIDTH, new_h), Image.LANCZOS)
        w, h = im.size

    # 保存(PNG 优化级别最高 9)
    im.save(p, format="PNG", optimize=True)

    new_size = p.stat().st_size
    if new_size <= SIZE_THRESHOLD:
        return orig_size, new_size, f"resized to {w}×{h}"

    # 兜底:不再压缩(PNG 是无损格式,resize 后已是最优)
    return orig_size, new_size, "kept(resize alone insufficient)"


def main():
    print("=" * 70)
    print(f"{'配图优化器 (>1MB → ≤1600px)':^70}")
    print("=" * 70)

    targets = []
    for p in ROOT.rglob("*.png"):
        if "/.git/" in str(p):
            continue
        if "/dist/" in str(p):
            continue
        if "/_archive/" in str(p) or "/_raw/" in str(p) or "/_refs/" in str(p):
            continue
        if p.stat().st_size >= SIZE_THRESHOLD:
            targets.append(p)

    print(f"\n  扫描到 {len(targets)} 个 PNG > 1 MB\n")

    total_orig = 0
    total_new = 0
    ok = 0
    skipped = 0
    failed = 0

    for p in sorted(targets):
        orig, new, status = optimize_one(p)
        total_orig += orig
        total_new += new
        rel = p.relative_to(ROOT)
        orig_kb = round(orig / 1024, 1)
        new_kb = round(new / 1024, 1)
        delta = round((1 - new / orig) * 100, 1) if orig > 0 else 0
        if status.startswith("skip"):
            skipped += 1
            marker = "·"
        elif status.startswith("kept"):
            failed += 1
            marker = "⚠"
        else:
            ok += 1
            marker = "✅"
        print(f"  {marker} {rel}")
        print(f"     {orig_kb:>8.1f} KB → {new_kb:>8.1f} KB (-{delta}%) {status}")

    print(f"\n{'=' * 70}")
    print(f"  处理: {ok} 优化 / {skipped} 跳过 / {failed} 兜底")
    saved_mb = round((total_orig - total_new) / 1024 / 1024, 2)
    print(f"  节省: {saved_mb} MB")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()