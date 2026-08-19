#!/usr/bin/env python3
"""
books/scripts/merge_short_paragraphs.py

合并相邻 2-3 个 < 80 字的段落,直到合并后 ≥ 80 字(最多合并 3 段)。
用"。"或"; "连接(根据前段结尾符号)。
"""
import re
from pathlib import Path

BOOKS_DIR = Path(__file__).resolve().parent.parent
WS = re.compile(r'\s+')


def split_paragraphs_full(text):
    """完整分段(含 # / > / 列表 / 表格 / 图片)"""
    paragraphs = []  # list of (type, content)
    in_code = False
    cur_type = None
    cur_content = []

    def flush():
        nonlocal cur_type, cur_content
        if cur_type and cur_content:
            paragraphs.append((cur_type, '\n'.join(cur_content).rstrip()))
        cur_type = None
        cur_content = []

    for line in text.split('\n'):
        if line.strip().startswith('```'):
            in_code = not in_code
            cur_content.append(line)
            continue
        if in_code:
            cur_content.append(line)
            continue

        if not line.strip():
            flush()
            paragraphs.append(('blank', ''))
            continue

        if line.startswith('#'):
            flush()
            cur_type = 'heading'
            cur_content.append(line)
        elif line.startswith('>'):
            flush()
            cur_type = 'quote'
            cur_content.append(line)
        elif line.startswith('|') or line.startswith('---'):
            flush()
            cur_type = 'table'
            cur_content.append(line)
        elif line.lstrip().startswith(('-',)) or line.lstrip().startswith('* '):
            flush()
            cur_type = 'list'
            cur_content.append(line)
        elif re.match(r'^\s*\d+\.\s+', line):
            flush()
            cur_type = 'list'
            cur_content.append(line)
        elif line.lstrip().startswith('!['):
            flush()
            cur_type = 'image'
            cur_content.append(line)
        else:
            # 普通段落:合并到上一段
            if cur_type == 'para':
                cur_content.append(line)
            else:
                flush()
                cur_type = 'para'
                cur_content.append(line)
    flush()
    return paragraphs


def join_paragraphs(paras):
    """合并相邻 'para' 类型的短段,直到 ≥ 80 字(跳过 blank/heading/quote)"""
    out = []
    i = 0
    while i < len(paras):
        ptype, content = paras[i]
        if ptype != 'para':
            out.append(paras[i])
            i += 1
            continue

        # 是 para,看是否需要合并
        cur_len = len(WS.sub('', content))
        if cur_len >= 80:
            out.append(paras[i])
            i += 1
            continue

        # 短段,尝试合并后续 1-2 个 para(跳过 blank/heading/quote)
        merged_content = content
        merged_count = 0
        j = i + 1
        while j < len(paras) and merged_count < 2:
            nptype, ncontent = paras[j]
            if nptype == 'para':
                # 检查合并后是否 ≥ 80
                if len(WS.sub('', merged_content)) >= 80:
                    break
                # 连接
                sep = '。 ' if merged_content.rstrip().endswith(('。', '!', '?', '!', '?')) else '; '
                merged_content = merged_content.rstrip() + sep + ncontent.lstrip()
                merged_count += 1
                j += 1
            elif nptype == 'blank':
                j += 1  # 跳过 blank
            else:
                break  # heading/quote/table/list/image 不能跨过

        out.append(('para', merged_content))
        i = j  # 跳过已合并的(包括跳过的 blank)

    return out


def rejoin(paras):
    """重新拼成字符串"""
    out = []
    for i, (ptype, content) in enumerate(paras):
        if i > 0 and ptype != 'blank':
            out.append('')
        out.append(content)
    return '\n'.join(out)


def process_chapter(f, target_median=80):
    """处理一个章节,返回是否修改"""
    text = f.read_text(encoding='utf-8')
    paras = split_paragraphs_full(text)

    # 计算修改前中位数
    real_paras = [c for t, c in paras if t == 'para' and len(WS.sub('', c)) >= 30]
    lens_before = sorted([len(WS.sub('', p)) for p in real_paras])
    med_before = lens_before[len(lens_before) // 2] if lens_before else 0

    # 合并
    new_paras = join_paragraphs(paras)
    new_text = rejoin(new_paras)

    # 计算修改后中位数
    new_real = [c for t, c in new_paras if t == 'para' and len(WS.sub('', c)) >= 30]
    lens_after = sorted([len(WS.sub('', p)) for p in new_real])
    med_after = lens_after[len(lens_after) // 2] if lens_after else 0

    if med_after > med_before:
        f.write_text(new_text, encoding='utf-8')
        return True, med_before, med_after, len(real_paras), len(new_real)
    return False, med_before, med_after, len(real_paras), len(new_real)


def main():
    targets = ['02-chapter.md', '05-chapter.md', '06-chapter.md', '07-chapter.md']
    ai_dir = BOOKS_DIR / 'ai-coding' / 'chapters'
    n = 0
    for fname in targets:
        f = ai_dir / fname
        if not f.exists():
            print(f'  --  {fname}: 不存在')
            continue
        changed, before, after, n1, n2 = process_chapter(f)
        if changed:
            n += 1
            print(f'  ✅  {fname}: {before} → {after}  ({n1} 段 → {n2} 段)')
        else:
            print(f'  --  {fname}: 无变化 ({before} → {after})')
    print(f'\n共修 {n} 章')


if __name__ == '__main__':
    main()
