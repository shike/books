#!/usr/bin/env python3
"""
books/scripts/image-audit.py

扫描 3 本书的 figures/ 目录:
- 列出所有图(大小 / 尺寸 / 引用状态)
- 找出未被任何 .md 引用的图
- 生成 promotion/image_index.md(自动)
- 输出未引用报告 + 总览

用法:
    python3 scripts/image-audit.py                    # 扫所有书
    python3 scripts/image-audit.py <book>             # 扫指定书
    python3 scripts/image-audit.py <book> --index    # 只生成 image_index.md
    python3 scripts/image-audit.py <book> --unused   # 只列未引用
"""
import sys
import os
import re
import argparse
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).resolve().parent
BOOKS_DIR = SCRIPT_DIR.parent

BOOKS = ['ai-coding', 'fde', 'workbuddy']

# 每本书的 figures 根目录 + chapters 根目录列表
BOOK_LAYOUTS = {
    'ai-coding': {
        'figures_root': 'figures',
        'chapters_roots': ['chapters', 'appendices', 'promotion'],
    },
    'fde': {
        'figures_root': 'figures',
        'chapters_roots': ['chapters', 'appendices'],
    },
    'workbuddy': {
        'figures_root': None,  # workbuddy 用 per-volume figures
        'chapters_roots': None,  # 特殊处理
        'volumes': ['第一卷', '第二卷', '第三卷'],
    },
}

def find_figures(book_dir, layout):
    """找出所有图文件"""
    figs = []
    if layout['figures_root']:
        fig_dir = book_dir / layout['figures_root']
        if fig_dir.exists():
            for ext in ['*.png', '*.jpg', '*.jpeg', '*.svg', '*.webp', '*.gif']:
                for f in fig_dir.rglob(ext):
                    if f.is_file():
                        figs.append(f)
    else:
        # workbuddy: per-volume
        for vol in layout['volumes']:
            vol_fig = book_dir / vol / 'figures'
            if vol_fig.exists():
                for ext in ['*.png', '*.jpg', '*.jpeg', '*.svg', '*.webp', '*.gif']:
                    for f in vol_fig.rglob(ext):
                        if f.is_file():
                            figs.append(f)
    return figs

def find_chapter_files(book_dir, layout):
    """找出所有可能引用图的 .md"""
    chapters = []
    if layout['chapters_roots']:
        for root in layout['chapters_roots']:
            d = book_dir / root
            if d.exists():
                for f in d.rglob('*.md'):
                    if f.is_file() and '_archive' not in str(f):
                        chapters.append(f)
    else:
        # workbuddy: per-volume
        for vol in layout['volumes']:
            d = book_dir / vol / 'chapters'
            if d.exists():
                for f in d.rglob('*.md'):
                    if f.is_file() and '_archive' not in str(f):
                        chapters.append(f)
            # appendices 也算
            ap = book_dir / vol / 'appendices'
            if ap.exists():
                for f in ap.rglob('*.md'):
                    if f.is_file() and '_archive' not in str(f):
                        chapters.append(f)
    return chapters

def is_referenced(fig_path, chapter_files):
    """检查 fig_path 是否被任何 .md 严格引用 (只算 ![]() 格式)"""
    import re
    fig_name = fig_path.name
    pattern = re.compile(r'!\[[^\]]*\]\((?:[^)]*/)?' + re.escape(fig_name) + r'\)')
    for cf in chapter_files:
        try:
            content = cf.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        if pattern.search(content):
            return True
    return False

def is_referenced_loose(fig_path, chapter_files):
    """宽松判断:fig_name 或 fig_stem 出现在 .md 中(包括 _archive 旧版)"""
    fig_name = fig_path.name
    fig_stem = fig_path.stem
    for cf in chapter_files:
        try:
            content = cf.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        if fig_name in content or fig_stem in content:
            return True
    return False

def generate_image_index(book_name, book_dir, layout):
    """生成 promotion/image_index.md"""
    figs = find_figures(book_dir, layout)
    if not figs:
        return None
    figs_sorted = sorted(figs, key=lambda x: str(x))
    lines = [
        f'# {book_name} 图片索引',
        '',
        f'> 自动生成于 {datetime.now().strftime("%Y-%m-%d %H:%M")}',
        f'> 总数: {len(figs_sorted)} 张',
        '',
        '| 序号 | 文件 | 大小 | 路径 |',
        '|---|---|---|---|',
    ]
    for i, f in enumerate(figs_sorted, 1):
        rel = f.relative_to(book_dir)
        size = f.stat().st_size
        if size > 1024 * 1024:
            size_str = f'{size/1024/1024:.1f} MB'
        elif size > 1024:
            size_str = f'{size/1024:.1f} KB'
        else:
            size_str = f'{size} B'
        lines.append(f'| {i} | `{f.name}` | {size_str} | `{rel}` |')
    lines.append('')
    out_path = book_dir / 'promotion' / 'image_index.md'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text('\n'.join(lines), encoding='utf-8')
    return out_path

def audit_book(book_name):
    """审计一本书: 返回 figs + unused"""
    book_dir = BOOKS_DIR / book_name
    layout = BOOK_LAYOUTS.get(book_name)
    if not layout:
        return None
    figs = find_figures(book_dir, layout)
    chapters = find_chapter_files(book_dir, layout)
    results = []
    for f in figs:
        used = is_referenced(f, chapters)
        size = f.stat().st_size
        results.append({
            'path': f,
            'rel': f.relative_to(book_dir),
            'size': size,
            'used': used,
        })
    return results, len(chapters)

def print_report(book_name, results, n_chapters):
    print(f'\n=== {book_name} ({n_chapters} 个 .md 扫描) ===')
    total = len(results)
    used = sum(1 for r in results if r['used'])
    unused = total - used
    total_size = sum(r['size'] for r in results)
    print(f'  总图: {total} 张, 已引用: {used}, 未引用: {unused}')
    print(f'  总大小: {total_size/1024/1024:.1f} MB')
    if unused > 0:
        print(f'  --- 未引用图 ---')
        for r in results:
            if not r['used']:
                size_str = f'{r["size"]/1024:.0f} KB' if r['size'] > 1024 else f'{r["size"]} B'
                print(f'    {size_str:>8s}  {r["rel"]}')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('book', nargs='?', help='只扫这本书 (ai-coding/fde/workbuddy)')
    ap.add_argument('--index', action='store_true', help='只生成 image_index.md')
    ap.add_argument('--unused', action='store_true', help='只列未引用')
    args = ap.parse_args()
    books = [args.book] if args.book else BOOKS
    for b in books:
        result = audit_book(b)
        if not result:
            print(f'未知书: {b}')
            continue
        results, n_chapters = result
        if args.index:
            out = generate_image_index(b, BOOKS_DIR / b, BOOK_LAYOUTS[b])
            if out:
                print(f'{b}: image_index.md 已生成 → {out.relative_to(BOOKS_DIR)}')
        else:
            print_report(b, results, n_chapters)
            if not args.unused:
                out = generate_image_index(b, BOOKS_DIR / b, BOOK_LAYOUTS[b])
                if out:
                    print(f'  image_index.md 已生成 → {out.relative_to(BOOKS_DIR)}')

if __name__ == '__main__':
    main()
