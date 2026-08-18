#!/usr/bin/env python3
"""
ai-coding 出版级正文清理脚本(2026-08-18)

替换规则(对齐 workbuddy 清理基准):
- OpenClaw / openclaw → 某开源 Agent 接入框架 / 该框架
- Kimi Claw / Claw Beta → 月之暗面云托管版
- Clawdbot / Moltbot → 早期版本代号
- 涉及 OpenClaw 的网址 / 仓库路径 / 文档名 → 中性化

注意:trademark.md 和 research/* 都不动(法律声明 / 元描述)。
"""
import re
import sys
from pathlib import Path

BOOK_DIR = Path("/Users/shike/Desktop/code/books/ai-coding")

# 替换规则(有序 — 先长后短,避免误伤)
REPLACEMENTS = [
    # 复合引用(必须先替换,避免被单条规则覆盖)
    ("OpenClaw 官方飞书渠道文档", "该框架官方飞书渠道文档"),
    ("OpenClaw Cron/Heartbeat 教程", "该框架 Cron/Heartbeat 教程"),
    ("OpenClaw 深度报道", "该框架深度报道"),
    ("OpenClaw 风险提示", "该框架风险提示"),
    ("OpenClaw+飞书周报全自动流程实战", "该框架+飞书周报全自动流程实战"),
    ("OpenClaw 的项目背景", "该框架的项目背景"),
    ("OpenClaw 接飞书", "该框架接飞书"),
    ("OpenClaw + 飞书对接架构", "该框架 + 飞书对接架构"),
    ("OpenClaw 是什么", "该框架是什么"),
    ("OpenClaw 部署的 Agent", "该框架部署的 Agent"),
    ("OpenClaw 是什么", "该框架是什么"),
    ("OpenClaw 提供", "该框架提供"),
    ("OpenClaw 文档", "该框架官方文档"),
    ("OpenClaw 配置", "该框架配置"),
    ("OpenClaw 默认", "该框架默认"),
    ("OpenClaw 接入飞书", "该框架接入飞书"),
    ("OpenClaw 案例", "该框架案例"),
    # 单个 product 名(大写在前,避免破坏 Clawdbot/Moltbot 这种 lineage 名称)
    ("Kimi Claw Beta", "月之暗面云托管版"),
    ("Kimi Claw", "月之暗面云托管版"),
    # 纯 OpenClaw 替换(放在最后,作为兜底)
    ("OpenClaw", "该框架"),
    ("openclaw", "该框架"),
    # Clawdbot/Moltbot 改名(仅在 chapter 06 body 内有用)
    ("Clawdbot→Moltbot→OpenClaw", "早期版本代号 A→B→C"),
]

# 清理目标文件
TARGET_FILES = [
    BOOK_DIR / "chapters/05-chapter.md",
    BOOK_DIR / "chapters/06-chapter.md",
    BOOK_DIR / "chapters/15-chapter.md",
    BOOK_DIR / "promotion/image_index.md",
    BOOK_DIR / "promotion/tools.md",
]


def clean_file(path: Path) -> tuple:
    """清理单个文件,返回 (before_count, after_count, changes)。"""
    text = path.read_text(encoding="utf-8")
    before = text
    changes = []
    for old, new in REPLACEMENTS:
        if old in text:
            count = text.count(old)
            text = text.replace(old, new)
            changes.append((old, new, count))
    if text != before:
        path.write_text(text, encoding="utf-8")
    return before, text, changes


def main():
    print("=== ai-coding 出版级正文清理 ===\n")
    total_changes = 0
    for f in TARGET_FILES:
        if not f.exists():
            print(f"⚠️  不存在: {f}")
            continue
        before, after, changes = clean_file(f)
        if changes:
            print(f"📝 {f.relative_to(BOOK_DIR)}")
            for old, new, count in changes:
                print(f"   · '{old}' → '{new}' × {count}")
            total_changes += sum(c for _, _, c in changes)
            print()
    print(f"=== 总替换: {total_changes} 处 ===")


if __name__ == "__main__":
    main()
