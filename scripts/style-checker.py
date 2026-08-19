#!/usr/bin/env python3
"""
books/scripts/style-checker.py

按风格手册规则,检查章节是否符合对应风格。
- 段落中位数
- 关键句式 / 关键词
- 章首必备
- 禁忌词
- 数字 / 引用

用法:
  python3 scripts/style-checker.py <book> [chapter]
  python3 scripts/style-checker.py <book> --report

输出:每章风格得分 (0-100) + 违例清单
"""
import sys
import os
import re
from pathlib import Path
import argparse

SCRIPT_DIR = Path(__file__).resolve().parent
BOOKS_DIR = SCRIPT_DIR.parent

BOOK_STYLE = {
    'ai-coding': 'style-1-行业战略派',
    'fde': 'style-2-故事叙事派',
    'workbuddy': 'style-3-实用操作派',
}

# 各风格的检查规则
RULES = {
    'style-1-行业战略派': {
        'required_opening': [
            (r'(本章导读|读者画像|核心命题|本书)', '章首导读'),
        ],
        'key_phrases': [
            r'这[不是]?的.{0,3}问题[是,是]',
            r'(大多数|多[数项])\s*[A-Za-z一-鿿]{0,8}(止步|内容|讨论)',
            r'(方法论|决策框架|选型清单|标准|原则)\s*[产出是为]?',
            r'(以.+为准|官方公告)',
        ],
        'forbidden': [
            (r'(小白入门|保姆级|震惊|绝对推荐|必杀技)', '营销词'),
            (r'(我觉得|我推荐|我认为|我建议)', '第一人称'),
        ],
        'paragraph_median_range': (80, 150),
        'must_have_terminology_def': True,
        'must_have_methodology_outline': True,
    },
    'style-2-故事叙事派': {
        'required_opening': [
            (r'##\s*(一个故事|另一个故事|第二个故事|故事|开篇)', '故事开场'),
        ],
        'key_phrases': [
            r'\d{4}\s*年',  # 年份
            r'(第一[个月周天]|第[一二三四五六七八九十]+\s*个[月周年天])',
            r'(没有人是|每个人都在|不是 X 的问题,是 Y 的问题)',
        ],
        'forbidden': [
            (r'##\s*1\.\d+', '数字分节(违和)'),
            (r'(本章学习目标|方法论产出|理论框架)', '学术风'),
            (r'>\s*\*\*本章学习目标\*\*', '实用派章首'),
            (r'(Kimi|Claude|GPT|DeepSeek)', '具体模型名'),
        ],
        'paragraph_median_range': (0, 80),
        'must_have_golden_ending': True,  # 章末加粗金句
    },
    'style-3-实用操作派': {
        'required_opening': [
            (r'>\s*\*\*本章学习目标\*\*', '学习目标块'),
        ],
        'key_phrases': [
            r'##\s*\d+\.\d+',  # N.M 分节
            r'(做法[是为]?|步骤[是为]?|流程[是为]?)',
            r'(具体.{0,4}(以.{0,8}(为准|公告)|.{0,8}为例))',
            r'(做 X\s*✅|不做 Y\s*❌|✅|❌)',
        ],
        'forbidden': [
            (r'(## 一个故事)', '故事开场'),
            # 强主观第一人称 (允许"我追问""我推荐""我会用"等中性叙述)
            (r'(我觉得|我认为|我感觉|我坚信|在我看来)', '主观第一人称'),
        ],
        'paragraph_median_range': (60, 100),
        'must_have_numbered_steps': True,  # 1. 2. 3. 步骤
        'must_have_3_level_numbering': True,  ## N.M
    },
    'style-4-学术综合派': {
        'required_opening': [
            (r'(理论框架|理论模型|根据|据.+报告|经典模型)', '理论引用'),
        ],
        'forbidden': [
            (r'(小白入门|保姆级)', '营销词'),
        ],
        'must_have_table': True,
        'must_have_risk_paragraph': True,
    },
    'style-5-极简口语派': {
        'required_opening': [
            (r'(说白了|你|我们|别)', '口语化'),
        ],
        'paragraph_median_range': (0, 50),
        'no_tables': True,
        'no_numbered_sections': True,  # 不 ## 1.1
    },
}


def chinese_chars_only(s):
    """只保留中文字符"""
    return ''.join(c for c in s if '\u4e00' <= c <= '\u9fff')


def split_paragraphs(text):
    """按空行分段,过滤掉代码块/标题/引用/列表项/表格/图片说明"""
    paragraphs = []
    in_code = False
    for line in text.split('\n'):
        if line.strip().startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.startswith('#') or line.startswith('>'):
            continue
        # 表格行
        if line.startswith('|') or line.startswith('---'):
            continue
        # 列表项 (- 1. 2. 3. 等开头)
        if line.lstrip().startswith(('-', '*')):
            continue
        if re.match(r'^\s*\d+\.\s+', line):
            continue
        # 图片说明
        if line.lstrip().startswith('!['):
            continue
        if not line.strip():
            paragraphs.append(None)  # 段落分隔
        else:
            if paragraphs and paragraphs[-1] is not None:
                paragraphs[-1] += line
            else:
                paragraphs.append(line)
    return [p for p in paragraphs if p and len(p.strip()) > 20]


def para_median_len(paragraphs):
    """段落中位数字符数"""
    if not paragraphs:
        return 0
    # 只算中文 + 数字 + 标点
    cn_lens = [len(chinese_chars_only(p) + re.sub(r'[^a-zA-Z0-9]', '', p)) for p in paragraphs]
    cn_lens.sort()
    n = len(cn_lens)
    if n % 2 == 0:
        return (cn_lens[n//2 - 1] + cn_lens[n//2]) / 2
    return cn_lens[n//2]


def has_golden_ending(text):
    """章末 200 字内是否含 1-3 句加粗金句(单行)"""
    ending = text[-500:]
    bold_lines = re.findall(r'^\*\*[^*]+\*\*\s*$', ending, re.MULTILINE)
    return len(bold_lines) >= 1


def count_numbered_steps(text):
    """统计 1. 2. 3. 步骤编号段落数"""
    return len(re.findall(r'^\s*\d+\.\s+', text, re.MULTILINE))


def count_tables(text):
    """统计 markdown 表格数"""
    lines = text.split('\n')
    n = 0
    for i in range(len(lines) - 1):
        if '|' in lines[i] and '|' in lines[i+1] and re.match(r'^\s*\|?[\s\-:|]+\|', lines[i+1]):
            n += 1
    return n


def count_subsections(text):
    """统计 ## N.M 形式的分节数"""
    return len(re.findall(r'##\s*\d+\.\d+', text))


def count_first_person(text):
    """统计第一人称"""
    return len(re.findall(r'(我觉得|我推荐|我认为|我建议)', text))


def check_chapter(text, style):
    """检查单个章节,返回 (score, violations)"""
    if style not in RULES:
        return 0, [f'未知风格: {style}']
    
    rules = RULES[style]
    score = 100
    violations = []
    
    # 1. 段落中位数
    if 'paragraph_median_range' in rules:
        lo, hi = rules['paragraph_median_range']
        paragraphs = split_paragraphs(text)
        # 过滤掉 < 30 字的"引导句"(通常后接列表/表格,非真正内容段)
        real_paragraphs = [p for p in paragraphs if len(re.sub(r'\s', '', p)) >= 30]
        med = para_median_len(real_paragraphs)
        if med < lo:
            score -= 10
            violations.append(f'段落中位数 {med:.0f} < {lo} (偏短)')
        elif med > hi:
            score -= 10
            violations.append(f'段落中位数 {med:.0f} > {hi} (偏长)')
    
    # 2. 必现关键句
    for pat, name in rules.get('required_opening', []):
        if not re.search(pat, text):
            score -= 15
            violations.append(f'缺:{name} (匹配 {pat})')
    
    # 3. 关键句式(至少 1 个)
    key_phrases = rules.get('key_phrases', [])
    if key_phrases:
        found = sum(1 for pat in key_phrases if re.search(pat, text))
        if found == 0:
            score -= 10
            violations.append(f'缺:关键句式 (0/{len(key_phrases)})')
    
    # 4. 禁忌
    for pat, name in rules.get('forbidden', []):
        if re.search(pat, text):
            score -= 8
            violations.append(f'违:{name} ({pat})')
    
    # 5. 加粗金句
    if rules.get('must_have_golden_ending'):
        if not has_golden_ending(text):
            score -= 15
            violations.append('缺:章末加粗金句')
    
    # 6. 数字步骤
    if rules.get('must_have_numbered_steps'):
        n = count_numbered_steps(text)
        if n < 3:
            score -= 10
            violations.append(f'数字步骤少:仅 {n} 个 (建议 ≥3)')
    
    # 7. 三级编号
    if rules.get('must_have_3_level_numbering'):
        n = count_subsections(text)
        if n < 2:
            score -= 10
            violations.append(f'## N.M 分节少:仅 {n} 个 (建议 ≥2)')
    
    # 8. 表格
    if rules.get('must_have_table'):
        if count_tables(text) == 0:
            score -= 15
            violations.append('缺:对比表格')
    
    # 9. 风险段
    if rules.get('must_have_risk_paragraph'):
        if not re.search(r'(风险|代价|坑|失败)', text):
            score -= 10
            violations.append('缺:风险段')
    
    # 10. 不用表格
    if rules.get('no_tables'):
        if count_tables(text) > 0:
            score -= 15
            violations.append(f'违:用了表格 ({count_tables(text)} 个)')
    
    # 11. 不用 N.M 编号
    if rules.get('no_numbered_sections'):
        if count_subsections(text) > 0:
            score -= 15
            violations.append(f'违:用了 ## N.M 编号')
    
    # 12. 术语定义(粗略检查,跳过)
    # if rules.get('must_have_terminology_def'):
    #     pass

    score = max(0, score)
    return score, violations


def check_book(book, style=None):
    """检查一本书的所有章节"""
    book_dir = BOOKS_DIR / book
    if not book_dir.exists():
        return None
    
    if style is None:
        style = BOOK_STYLE.get(book, 'style-1-行业战略派')
    
    # 找章节文件
    if book == 'workbuddy':
        # 三卷结构
        chapters = []
        for vol in ['第一卷', '第二卷', '第三卷']:
            d = book_dir / vol / 'chapters'
            if d.exists():
                for f in sorted(d.glob('*.md')):
                    if f.name.startswith('_'):
                        continue
                    chapters.append((vol, f))
    else:
        d = book_dir / 'chapters'
        if not d.exists():
            return None
        chapters = [('', f) for f in sorted(d.glob('*.md')) if not f.name.startswith('_')]
    
    if not chapters:
        return None
    
    results = []
    for vol, f in chapters:
        text = f.read_text(encoding='utf-8')
        score, viol = check_chapter(text, style)
        rel = f.relative_to(book_dir)
        results.append({
            'chapter': str(rel),
            'vol': vol,
            'score': score,
            'violations': viol,
        })
    return results, style


def print_report(book, results, style):
    print(f'\n=== {book} ({style}) ===')
    if not results:
        print('  无章节')
        return
    scores = [r['score'] for r in results]
    print(f'  共 {len(results)} 章, 平均分 {sum(scores)/len(scores):.1f}')
    
    # 排序:低分在前
    results.sort(key=lambda r: r['score'])
    
    for r in results:
        marker = '🟢' if r['score'] >= 80 else ('🟡' if r['score'] >= 60 else '🔴')
        vol_str = f'[{r["vol"]}] ' if r['vol'] else ''
        print(f'  {marker} {r["score"]:3d}  {vol_str}{r["chapter"]}')
        if r['violations']:
            for v in r['violations'][:3]:
                print(f'           · {v}')
            if len(r['violations']) > 3:
                print(f'           · ... +{len(r["violations"])-3} more')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('book', help='书名 (ai-coding/fde/workbuddy)')
    ap.add_argument('chapter', nargs='?', help='指定章节文件名(可选)')
    ap.add_argument('--report', action='store_true', help='只输出报告')
    ap.add_argument('--style', help='强制风格 (style-1/2/3/4/5)')
    args = ap.parse_args()
    
    style = args.style
    if style and not style.startswith('style-'):
        style = f'style-{style}'
    if style and style not in RULES:
        print(f'未知风格: {style}')
        return
    
    result = check_book(args.book, style)
    if not result:
        print(f'未找到书: {args.book}')
        return
    
    results, used_style = result
    if args.chapter:
        # 只看指定章节
        for r in results:
            if args.chapter in r['chapter']:
                print(f"\n{r['chapter']} ({used_style})")
                print(f"  得分: {r['score']}")
                for v in r['violations']:
                    print(f"  · {v}")
                return
        print(f'未找到章节: {args.chapter}')
    else:
        print_report(args.book, results, used_style)


if __name__ == '__main__':
    main()
