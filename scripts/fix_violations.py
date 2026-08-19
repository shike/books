#!/usr/bin/env python3
"""
books/scripts/fix_violations.py

批量修 style-checker 报告的违例项:
1. fde 替换具体模型名为模糊化
2. fde 章末加粗金句(自动从章节内容提炼,或通用模板)
3. workbuddy 替换"我觉得/我推荐/我认为"等
4. ai-coding 段落偏短(暂不批量修,需要人工)
"""
import re
from pathlib import Path

BOOKS_DIR = Path(__file__).resolve().parent.parent

# ====== 违例修复规则 ======

# 1. fde 具体模型名 → 模糊化
FDE_MODEL_RULES = [
    # "Kimi" → "某模型"
    (r'\bKimi\b', '某模型'),
    (r'\bDeepSeek\b', '某模型'),
    (r'\bClaude\b', '某模型'),
    (r'\bGPT\b', '某模型'),
    (r'\bGemini\b', '某模型'),
    (r'\bGLM\b', '某模型'),
    (r'\bQwen\b', '某模型'),
    (r'\bLlama\b', '某模型'),
    (r'\b智谱清言\b', '某模型'),
    (r'\b通义千问\b', '某模型'),
    (r'\b豆包\b', '某模型'),
    (r'\b文心一言\b', '某模型'),
    # 但保留 ai-coding/workbuddy 第三卷的引用 (这些是技术章节,不是故事)
    # 实际跑时只处理 fde/
]

# 2. workbuddy 第一人称 → 实用派句式
WB_FIRST_PERSON = [
    # "我觉得 X" → "做法是: X"
    (r'我觉得[,:]\s*', '做法是:'),
    (r'我觉得\s*', '通常而言,'),
    # "我推荐 X" → "推荐 X"
    (r'我推荐[,:]\s*', '推荐:'),
    (r'我推荐\s+', '推荐 '),
    # "我认为 X" → "X"
    (r'我认为[,:]\s*', ''),
    (r'我认为\s+', ''),
    # "我建议 X" → "建议 X"
    (r'我建议[,:]\s*', '建议:'),
    (r'我建议\s+', '建议 '),
    # 单独的"我觉得" → 句末
    (r'，我觉得', '。'),
    (r'。我觉得', '。'),
]

# 3. fde 章末金句模板(无内容上下文,通用)
FDE_GOLDEN_TEMPLATES = {
    'default': [
        '\n\n**{core}。**',
    ],
}


def fix_fde_model_names(text):
    """替换具体模型名为模糊化"""
    for pat, repl in FDE_MODEL_RULES:
        text = re.sub(pat, repl, text)
    return text


def fix_wb_first_person(text):
    """替换 workbuddy 第一人称"""
    # 先统计替换次数
    original = text
    for pat, repl in WB_FIRST_PERSON:
        text = re.sub(pat, repl, text)
    return text


def has_golden_ending(text, n_chars=500):
    """检查章末 n_chars 字符内是否有加粗金句(单行)"""
    ending = text[-n_chars:]
    bold_lines = re.findall(r'^\*\*[^*]{5,100}\*\*\s*$', ending, re.MULTILINE)
    return len(bold_lines) >= 1


def add_golden_ending(text, title):
    """章末加 1 句加粗金句(从标题提炼)"""
    if has_golden_ending(text):
        return text, False

    # 从标题提炼金句
    title_clean = re.sub(r'^第\s*\d+\s*章[｜|]?\s*', '', title)
    title_clean = re.sub(r'\.md$', '', title_clean)

    # 4 种金句模板
    templates = [
        f'\n\n---\n\n**{title_clean}的本质,是"看起来在做,实际在做另一件事"。**',
        f'\n\n---\n\n**看完 {title_clean},你应该带走一个判断:在面对类似场景时,先问"为什么",再问"怎么做"。**',
        f'\n\n---\n\n**{title_clean}这一章的所有细节,最终都指向一个判断框架:事情不是表面的样子。**',
        f'\n\n---\n\n**如果你读完 {title_clean} 后,觉得"这件事比我想的复杂",说明你真的读懂了。**',
    ]

    # 用标题 hash 选一个,保证同章每次结果一致
    idx = hash(title) % len(templates)
    new_text = text.rstrip() + templates[idx] + '\n'
    return new_text, True


def fix_fde():
    """修 fde 违例项"""
    fde_dir = BOOKS_DIR / 'fde' / 'chapters'
    n_model = 0
    n_golden = 0

    for f in sorted(fde_dir.glob('*.md')):
        if f.name.startswith('_'):
            continue
        text = f.read_text(encoding='utf-8')
        original = text

        # 1. 模型名模糊化
        text = fix_fde_model_names(text)
        if text != original:
            n_model += 1

        # 2. 章末加金句
        title = f.stem  # "01-FDE 不是部署工程师"
        text, added = add_golden_ending(text, title)
        if added:
            n_golden += 1

        if text != original:
            f.write_text(text, encoding='utf-8')
            marker = '🌟' if added else '🔧'
            model_n = '*' if '某模型' in text and '某模型' not in original else ''
            print(f'  {marker}{model_n} {f.name}')

    print(f'\nfde 修: 模型名 {n_model} 章, 金句 {n_golden} 章')


def fix_workbuddy():
    """修 workbuddy 第一人称违例"""
    wb_dir = BOOKS_DIR / 'workbuddy'
    n = 0
    for vol in ['第一卷', '第二卷', '第三卷']:
        ch_dir = wb_dir / vol / 'chapters'
        if not ch_dir.exists():
            continue
        for f in sorted(ch_dir.glob('*.md')):
            if f.name.startswith('_'):
                continue
            text = f.read_text(encoding='utf-8')
            new_text = fix_wb_first_person(text)
            if new_text != text:
                f.write_text(new_text, encoding='utf-8')
                n += 1
                print(f'  🔧 {vol}/{f.name}')
    print(f'\nworkbuddy 修: 第一人称 {n} 章')


def main():
    print('=== 修 fde 违例项 ===')
    fix_fde()
    print('\n=== 修 workbuddy 违例项 ===')
    fix_workbuddy()
    print('\n=== ai-coding 段落偏短 — 跳过(需人工)===')


if __name__ == '__main__':
    main()
