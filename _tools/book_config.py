#!/usr/bin/env python3
"""
三本书的打包配置。
"""
import os

ROOT = "/Users/shike/Desktop/code/books"

BOOKS = {
    "ai-coding": {
        "title": "AI Coding · 人人都是程序员",
        "subtitle": "让非技术人用 AI 做出可交付产品",
        "author": "施可",
        "language": "zh-CN",
        "isbn": "978-7-XXXX-XXXX-X (电子书)",
        "publisher": "施可 · 三本书统一仓库",
        "year": 2026,
        "cover": f"{ROOT}/ai-coding/promotion/cover.png",
        "root_dir": f"{ROOT}/ai-coding",
        "chapters_dir": f"{ROOT}/ai-coding/chapters",
        "appendices_dir": None,  # ai-coding 没有传统 appendices 目录
        "appendix_files": [
            f"{ROOT}/ai-coding/assets/cheatsheet/data_source_decision.md",
            f"{ROOT}/ai-coding/assets/cheatsheet/four_levers.md",
            f"{ROOT}/ai-coding/assets/cheatsheet/issue_diagnosis.md",
            f"{ROOT}/ai-coding/assets/cheatsheet/model_selection.md",
        ],
        "figures_dir": f"{ROOT}/ai-coding/figures",
        "dist_dir": f"{ROOT}/ai-coding/dist",
        "intro_pages": [
            ("封面", "cover"),
            ("版权", f"{ROOT}/ai-coding/promotion/copyright.md"),
            ("致谢", f"{ROOT}/ai-coding/promotion/acknowledgment.md"),
            ("推荐语", f"{ROOT}/ai-coding/promotion/recommend.md"),
            ("自序 / 内容简介", f"{ROOT}/ai-coding/promotion/epilogue.md"),
            ("导读:本书阅读路线图", f"{ROOT}/ai-coding/chapters/00-chapter.md"),
            ("AI 披露", f"{ROOT}/ai-coding/promotion/ai_disclosure.md"),
            ("术语表", f"{ROOT}/ai-coding/promotion/glossary.md"),
            ("工具速查", f"{ROOT}/ai-coding/promotion/tools.md"),
            ("配图索引", f"{ROOT}/ai-coding/promotion/image_index.md"),
            ("作者介绍", f"{ROOT}/ai-coding/promotion/about_author.md"),
        ],
        "outro_pages": [
            ("微信二维码", f"{ROOT}/ai-coding/promotion/wechat_qr.png"),
            ("微信公众号介绍", f"{ROOT}/ai-coding/promotion/wechat_try.md"),
            ("视频脚本", f"{ROOT}/ai-coding/promotion/video_scripts.md"),
            ("勘误表", f"{ROOT}/ai-coding/promotion/corrections.md"),
        ],
        "metadata": {
            "title": "AI Coding · 人人都是程序员",
            "creator": "施可",
            "language": "zh-CN",
            "subject": "AI 编程 · 非技术读者 · 可交付产品",
            "description": "一本面向创业者、产品经理、设计师、独立顾问的实战书。教非程序员用 AI 做出可交付的产品。",
            "publisher": "施可 · 三本书统一仓库",
            "rights": "CC BY-NC-SA 4.0",
            "identifier": "urn:uuid:a6cb8625-3e0c-591c-8497-f3fa81afa5c6",
        }
    },
    "fde": {
        "title": "FDE · AI 竞赛不在于模型",
        "subtitle": "工程师在 AI 项目里做部署交付",
        "author": "施可",
        "language": "zh-CN",
        "isbn": "978-7-XXXX-XXXX-X (电子书)",
        "publisher": "施可 · 三本书统一仓库",
        "year": 2026,
        "cover": f"{ROOT}/fde/promotion/cover.png",
        "root_dir": f"{ROOT}/fde",
        "chapters_dir": f"{ROOT}/fde/chapters",
        "appendices_dir": f"{ROOT}/fde/appendices",
        "appendix_files": [
            f"{ROOT}/fde/appendices/00-main.md",
            f"{ROOT}/fde/appendices/case-studies/case-study-01.md",
            f"{ROOT}/fde/appendices/case-studies/case-study-02.md",
            f"{ROOT}/fde/appendices/case-studies/case-study-03.md",
        ],
        "figures_dir": None,  # fde 没有 figures
        "dist_dir": f"{ROOT}/fde/dist",
        "intro_pages": [
            ("封面", "cover"),
            ("版权", f"{ROOT}/fde/promotion/copyright.md"),
            ("致谢", f"{ROOT}/fde/promotion/acknowledgment.md"),
            ("推荐语", f"{ROOT}/fde/promotion/recommend.md"),
            ("自序 / 内容简介", f"{ROOT}/fde/promotion/epilogue.md"),
            ("AI 披露", f"{ROOT}/fde/promotion/ai_disclosure.md"),
            ("术语表", f"{ROOT}/fde/promotion/glossary.md"),
            ("工具速查", f"{ROOT}/fde/promotion/tools.md"),
            ("配图索引", f"{ROOT}/fde/promotion/image_index.md"),
            ("作者介绍", f"{ROOT}/fde/promotion/about_author.md"),
        ],
        "outro_pages": [
            ("微信二维码", f"{ROOT}/fde/promotion/wechat_qr.png"),
            ("微信公众号介绍", f"{ROOT}/fde/promotion/wechat_try.md"),
            ("视频脚本", f"{ROOT}/fde/promotion/video_scripts.md"),
            ("勘误表", f"{ROOT}/fde/promotion/corrections.md"),
        ],
        "metadata": {
            "title": "FDE · AI 竞赛不在于模型",
            "creator": "施可",
            "language": "zh-CN",
            "subject": "AI 项目部署 · FDE · 工程实践",
            "description": "一本面向 CTO、技术负责人、产品经理、想转 FDE 的人的实战书。从 PoC 到生产,把 AI 项目做稳做久。",
            "publisher": "施可 · 三本书统一仓库",
            "rights": "CC BY-NC-SA 4.0",
            "identifier": "urn:uuid:f6726c14-5cd9-55df-97e2-9570f9995580",
        }
    },
    "workbuddy": {
        "title": "WorkBuddy 三部曲",
        "subtitle": "管理者用桌面 AI 从个人 → 团队 → 组织",
        "author": "施可",
        "language": "zh-CN",
        "isbn": "978-7-XXXX-XXXX-X (电子书)",
        "publisher": "施可 · 三本书统一仓库",
        "year": 2026,
        "cover": f"{ROOT}/workbuddy/promotion/cover.png",
        "root_dir": f"{ROOT}/workbuddy",
        "chapters_dir": None,  # workbuddy 三卷分开
        "figures_dir": None,
        "dist_dir": f"{ROOT}/workbuddy/dist",
        "volumes": [
            {
                "name": "第一卷",
                "title": "WorkBuddy · 第一卷 · 个人篇",
                "subtitle": "从零到合格的 WorkBuddy 用户",
                "chapters_dir": f"{ROOT}/workbuddy/第一卷/chapters",
                "figures_dir": f"{ROOT}/workbuddy/第一卷/figures",
                "appendices_dir": f"{ROOT}/workbuddy/第一卷/appendices",
                "errata_dir": f"{ROOT}/workbuddy/第一卷/errata",
                "out_slug": "第一卷",
                "appendix_files": [
                    f"{ROOT}/workbuddy/第一卷/appendices/A-读者指南.md",
                    f"{ROOT}/workbuddy/第一卷/appendices/B-术语表.md",
                    f"{ROOT}/workbuddy/第一卷/appendices/C-提示词模板集.md",
                    f"{ROOT}/workbuddy/第一卷/appendices/D-检查清单.md",
                    f"{ROOT}/workbuddy/第一卷/appendices/E-案例库.md",
                    f"{ROOT}/workbuddy/第一卷/appendices/F-进一步阅读.md",
                ],
            },
            {
                "name": "第二卷",
                "title": "WorkBuddy · 第二卷 · 团队篇",
                "subtitle": "从个人到团队 · 试点 → 推广 → 沉淀",
                "chapters_dir": f"{ROOT}/workbuddy/第二卷/chapters",
                "figures_dir": f"{ROOT}/workbuddy/第二卷/figures",
                "appendices_dir": f"{ROOT}/workbuddy/第二卷/appendices",
                "errata_dir": f"{ROOT}/workbuddy/第二卷/errata",
                "out_slug": "第二卷",
                "appendix_files": [
                    f"{ROOT}/workbuddy/第二卷/appendices/A-读者指南.md",
                    f"{ROOT}/workbuddy/第二卷/appendices/B-术语表.md",
                    f"{ROOT}/workbuddy/第二卷/appendices/C-提示词模板集.md",
                    f"{ROOT}/workbuddy/第二卷/appendices/D-检查清单.md",
                    f"{ROOT}/workbuddy/第二卷/appendices/E-案例库.md",
                    f"{ROOT}/workbuddy/第二卷/appendices/F-进一步阅读.md",
                ],
            },
            {
                "name": "第三卷",
                "title": "WorkBuddy · 第三卷 · 组织篇",
                "subtitle": "从团队到组织 · 规模化 · 变革管理",
                "chapters_dir": f"{ROOT}/workbuddy/第三卷/chapters",
                "figures_dir": f"{ROOT}/workbuddy/第三卷/figures",
                "appendices_dir": f"{ROOT}/workbuddy/第三卷/appendices",
                "errata_dir": f"{ROOT}/workbuddy/第三卷/errata",
                "out_slug": "第三卷",
                "appendix_files": [
                    f"{ROOT}/workbuddy/第三卷/appendices/A-读者指南.md",
                    f"{ROOT}/workbuddy/第三卷/appendices/B-术语表.md",
                    f"{ROOT}/workbuddy/第三卷/appendices/C-提示词模板集.md",
                    f"{ROOT}/workbuddy/第三卷/appendices/D-检查清单.md",
                    f"{ROOT}/workbuddy/第三卷/appendices/E-案例库.md",
                    f"{ROOT}/workbuddy/第三卷/appendices/F-进一步阅读.md",
                ],
            },
        ],
        "intro_pages": [
            ("封面", "cover"),
            ("版权", f"{ROOT}/workbuddy/promotion/copyright.md"),
            ("致谢", f"{ROOT}/workbuddy/promotion/acknowledgment.md"),
            ("推荐语", f"{ROOT}/workbuddy/promotion/recommend.md"),
            ("自序 / 内容简介", f"{ROOT}/workbuddy/promotion/epilogue.md"),
            ("AI 披露", f"{ROOT}/workbuddy/promotion/ai_disclosure.md"),
            ("术语表", f"{ROOT}/workbuddy/promotion/glossary.md"),
            ("工具速查", f"{ROOT}/workbuddy/promotion/tools.md"),
            ("配图索引", f"{ROOT}/workbuddy/promotion/image_index.md"),
            ("作者介绍", f"{ROOT}/workbuddy/promotion/about_author.md"),
        ],
        "outro_pages": [
            ("微信二维码", f"{ROOT}/workbuddy/promotion/wechat_qr.png"),
            ("微信公众号介绍", f"{ROOT}/workbuddy/promotion/wechat_try.md"),
            ("视频脚本", f"{ROOT}/workbuddy/promotion/video_scripts.md"),
            ("勘误表", f"{ROOT}/workbuddy/promotion/corrections.md"),
        ],
        "metadata": {
            "title": "WorkBuddy 三部曲",
            "creator": "施可",
            "language": "zh-CN",
            "subject": "管理者 · 桌面 AI · 团队落地 · 组织变革",
            "description": "面向中层及以上管理者的三部曲。个人篇(用起来) → 团队篇(用起来) → 组织篇(变革管理)。配套培训交付件。",
            "publisher": "施可 · 三本书统一仓库",
            "rights": "CC BY-NC-SA 4.0",
            "identifier": "urn:uuid:027c99d0-b11c-5b19-a363-d5a39e9a2f39",
        }
    }
}

if __name__ == "__main__":
    for key, cfg in BOOKS.items():
        print(f"{key}: {cfg['title']}")
        print(f"  chapters: {cfg.get('chapters_dir')}")
        print(f"  figures: {cfg.get('figures_dir') or '(per-volume)'}")
        print(f"  dist: {cfg['dist_dir']}")