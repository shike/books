#!/usr/bin/env python3
"""
ai-coding 同步 dist/main.md 与 ai_coding_book_final.md 的清理
(这两份是 README 列为"已就绪的发布件"的合并版)
"""
from pathlib import Path

BOOK_DIR = Path("/Users/shike/Desktop/code/books/ai-coding")

REPLACEMENTS = [
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
    ("OpenClaw 提供", "该框架提供"),
    ("OpenClaw 文档", "该框架官方文档"),
    ("OpenClaw 配置", "该框架配置"),
    ("OpenClaw 默认", "该框架默认"),
    ("OpenClaw 接入飞书", "该框架接入飞书"),
    ("Clawdbot→Moltbot→OpenClaw", "早期版本 A→B→C(项目沿革代号)"),
    ("Kimi Claw Beta", "月之暗面云托管版"),
    ("Kimi Claw", "月之暗面云托管版"),
    ("OpenClaw", "该框架"),
    ("openclaw", "该框架"),
]

TARGETS = [
    BOOK_DIR / "dist/main.md",
    BOOK_DIR / "ai_coding_book_final.md",
]

for f in TARGETS:
    if not f.exists():
        continue
    text = f.read_text(encoding="utf-8")
    n = 0
    for old, new in REPLACEMENTS:
        if old in text:
            c = text.count(old)
            text = text.replace(old, new)
            n += c
    if n:
        f.write_text(text, encoding="utf-8")
        print(f"📝 {f.relative_to(BOOK_DIR)}: {n} 处")
    else:
        print(f"✓ {f.relative_to(BOOK_DIR)}: 无需改动")
