#!/usr/bin/env python3
"""
多平台封面生成器。

输入:每本书的 `promotion/cover.png`(主源,1792×2400 / 1200×1800)
输出:5 个平台尺寸的 JPG 封面 + 1 个 PNG 高保真版本

策略:
  - 中心裁剪(center-crop):源图按目标比例裁掉多余部分,然后 resize
    → 适合 KDP / Apple Books 这类"封面必须填满整图"的平台
  - 长边填充(long-side-fit + pad):保持原图全部内容,白边填充
    → 适合 微信读书 / 豆瓣 这类"可接受白边"的平台
  - 默认 KDP/Apple 用 center-crop;微信/豆瓣/通用 用 long-side-fit

输出目录:`<book>/promotion/cover_<platform>.{jpg,png}`

依赖:Pillow (pip install pillow)
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Tuple

from PIL import Image

ROOT = Path("/Users/shike/Desktop/code/books")

# 平台规格:(平台名, 宽 W, 高 H, 策略, 格式)
PLATFORMS = [
    ("kdp", 1600, 2560, "crop", "jpg"),       # KDP Kindle (1:1.6)
    ("apple", 1400, 1873, "crop", "jpg"),     # Apple Books (1:1.34)
    ("wechat", 600, 800, "fit", "jpg"),       # 微信读书 (3:4)
    ("douban", 600, 800, "fit", "jpg"),       # 豆瓣阅读 (3:4)
    ("web", 800, 1200, "fit", "png"),         # 通用 web (2:3, PNG 无损)
]

BOOKS = ["ai-coding", "fde", "workbuddy"]


def center_crop_to_ratio(im: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """按目标比例中心裁剪,然后 resize 到精确尺寸。"""
    src_w, src_h = im.size
    target_ratio = target_h / target_w
    src_ratio = src_h / src_w

    if src_ratio > target_ratio:
        # 源图更"瘦高",按宽度裁 → 裁掉上下
        new_w = src_w
        new_h = int(src_w * target_ratio)
        top = (src_h - new_h) // 2
        im = im.crop((0, top, src_w, top + new_h))
    else:
        # 源图更"宽矮",按高度裁 → 裁掉左右
        new_h = src_h
        new_w = int(src_h / target_ratio)
        left = (src_w - new_w) // 2
        im = im.crop((left, 0, left + new_w, src_h))

    return im.resize((target_w, target_h), Image.LANCZOS)


def fit_with_pad(im: Image.Image, target_w: int, target_h: int, pad_color=(255, 255, 255)) -> Image.Image:
    """长边缩放,白边填充到精确尺寸。保留全部内容。"""
    src_w, src_h = im.size
    target_ratio = target_h / target_w
    src_ratio = src_h / src_w

    if src_ratio > target_ratio:
        # 源图更瘦高 → 按宽度缩放
        new_w = target_w
        new_h = int(target_w * src_ratio)
    else:
        # 源图更宽矮 → 按高度缩放
        new_h = target_h
        new_w = int(target_h / src_ratio)

    im_resized = im.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGB", (target_w, target_h), pad_color)
    canvas.paste(im_resized, ((target_w - new_w) // 2, (target_h - new_h) // 2))
    return canvas


def gen_one(book: str, platform: str, w: int, h: int, strategy: str, fmt: str) -> Tuple[Path, int]:
    src = ROOT / book / "promotion" / "cover.png"
    if not src.exists():
        raise FileNotFoundError(f"源文件不存在: {src}")

    im = Image.open(src).convert("RGB")

    if strategy == "crop":
        out_im = center_crop_to_ratio(im, w, h)
    elif strategy == "fit":
        out_im = fit_with_pad(im, w, h)
    else:
        raise ValueError(f"未知策略: {strategy}")

    ext = "jpg" if fmt == "jpg" else "png"
    out = ROOT / book / "promotion" / f"cover_{platform}.{ext}"

    save_kwargs = {}
    if fmt == "jpg":
        save_kwargs = {"quality": 95, "optimize": True, "progressive": True}

    out_im.save(out, **save_kwargs)
    return out, out.stat().st_size


def main():
    print("=" * 70)
    print(f"{'多平台封面生成器':^70}")
    print("=" * 70)

    total = 0
    for book in BOOKS:
        print(f"\n📚 {book}")
        for platform, w, h, strategy, fmt in PLATFORMS:
            try:
                out, size = gen_one(book, platform, w, h, strategy, fmt)
                size_kb = round(size / 1024, 1)
                strategy_zh = "中心裁剪" if strategy == "crop" else "长边填充"
                print(f"   ✅ {platform:<8} {w}×{h:<5} {fmt.upper():<3} {strategy_zh:<6} {size_kb:>7.1f} KB → {out.relative_to(ROOT)}")
                total += 1
            except FileNotFoundError as e:
                print(f"   ❌ {platform}: {e}")
            except Exception as e:
                print(f"   ❌ {platform}: {type(e).__name__}: {e}")

    print(f"\n{'=' * 70}")
    print(f"  生成完成: {total} / {len(BOOKS) * len(PLATFORMS)}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()