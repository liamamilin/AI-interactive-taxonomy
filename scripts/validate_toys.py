#!/usr/bin/env python3
"""
AI-Interactive-Taxonomy 质量门禁脚本 v2.0
检查项：
1. taxonomy.json 合法性、全局 plannedTopics slug 唯一性、tracks 指向有效性
2. domains/<domain>/<topic>/ 下 meta.json 合法性、branch 归属与 related 跨领域引用有效性
3. HTML 相对链接、DOM getElementById 目标与内嵌 JS 语法（如系统存在 node）
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAXONOMY_PATH = ROOT / "taxonomy.json"
DOMAINS_DIR = ROOT / "domains"


def main():
    issues = []
    taxonomy = json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))

    valid_domains = {}
    all_planned_slugs = set()
    all_valid_topic_ids = set()

    for d in taxonomy["domains"]:
        did = d["id"]
        valid_domains[did] = {b["id"] for b in d.get("branches", [])}
        for b in d.get("branches", []):
            for pt in b.get("plannedTopics", []):
                if not isinstance(pt, dict) or not pt.get("slug") or not pt.get("title"):
                    issues.append(f"taxonomy.json {did}/{b['id']}: plannedTopic 必须包含 slug 与 title")
                    continue
                slug = pt["slug"]
                if slug in all_planned_slugs:
                    issues.append(f"taxonomy.json 全局重复 planned slug: {slug}")
                all_planned_slugs.add(slug)
                all_valid_topic_ids.add(f"{did}/{slug}")

    # 预先收集全部真实存在的 topic_id 与 toy_id
    live_toy_ids = set()
    live_topic_slugs = set()
    if DOMAINS_DIR.exists():
        for dom_dir in sorted(DOMAINS_DIR.iterdir()):
            if not dom_dir.is_dir() or dom_dir.name.startswith("."):
                continue
            for topic_dir in sorted(dom_dir.iterdir()):
                if not topic_dir.is_dir() or topic_dir.name.startswith("."):
                    continue
                if topic_dir.name in live_topic_slugs:
                    issues.append(f"全局重复已实现主题 slug: {topic_dir.name}")
                live_topic_slugs.add(topic_dir.name)
                all_valid_topic_ids.add(f"{dom_dir.name}/{topic_dir.name}")
                for hf in topic_dir.glob("*.html"):
                    if hf.name.lower() != "index.html":
                        live_toy_ids.add(f"{dom_dir.name}/{topic_dir.name}/{hf.name}")

    # 校验 tracks 里的每个 toy_id 真实存在
    for tr in taxonomy.get("tracks", []):
        for tid in tr.get("toys", []):
            if tid not in live_toy_ids:
                issues.append(f"taxonomy.json track '{tr.get('id')}' 引用了不存在的玩具: {tid}")

    has_node = subprocess.run(["which", "node"], capture_output=True).returncode == 0
    checked_topics = 0
    checked_html = 0

    if DOMAINS_DIR.exists():
        for dom_dir in sorted(DOMAINS_DIR.iterdir()):
            if not dom_dir.is_dir() or dom_dir.name.startswith("."):
                continue
            if dom_dir.name not in valid_domains:
                issues.append(f"未知领域目录: domains/{dom_dir.name}")
                continue

            for topic_dir in sorted(dom_dir.iterdir()):
                if not topic_dir.is_dir() or topic_dir.name.startswith("."):
                    continue
                htmls = sorted(topic_dir.glob("*.html"))
                toy_files = [h.name for h in htmls if h.name.lower() != "index.html"]
                if not toy_files:
                    continue
                checked_topics += 1

                meta_path = topic_dir / "meta.json"
                if not meta_path.exists():
                    issues.append(f"缺少 meta.json: {topic_dir.relative_to(ROOT)}")
                else:
                    try:
                        meta = json.loads(meta_path.read_text(encoding="utf-8"))
                        branch = meta.get("branch")
                        if branch and branch not in valid_domains[dom_dir.name]:
                            issues.append(f"{meta_path.relative_to(ROOT)}: 未知 branch '{branch}'")
                        if "toys" in meta and set(meta["toys"].keys()) != set(toy_files):
                            issues.append(f"{meta_path.relative_to(ROOT)}: toys 键与 HTML 文件列表不一致")
                        for rel in meta.get("related", []):
                            if rel not in all_valid_topic_ids:
                                issues.append(f"{meta_path.relative_to(ROOT)}: 无效 related 引用 '{rel}'")
                    except Exception as e:
                        issues.append(f"{meta_path.relative_to(ROOT)}: JSON 解析失败 ({e})")

                for hf in htmls:
                    checked_html += 1
                    text = hf.read_text(encoding="utf-8", errors="ignore")
                    for href in re.findall(r'href="(\./[^"]+)"', text):
                        target = (topic_dir / href).resolve()
                        if not target.exists():
                            issues.append(f"{hf.relative_to(ROOT)}: 断链 {href}")
                    ids = set(re.findall(r'\bid="([^"]+)"', text))
                    for gid in re.findall(r'getElementById\(["\']([^"\']+)["\']\)', text):
                        if gid not in ids:
                            issues.append(f"{hf.relative_to(ROOT)}: 找不到 DOM id={gid}")
                    if has_node:
                        for i, sc in enumerate(re.findall(r"<script>(.*?)</script>", text, re.S)):
                            with tempfile.NamedTemporaryFile(suffix=".js", mode="w", delete=False) as tf:
                                tf.write(sc)
                                tmp = tf.name
                            r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
                            os.unlink(tmp)
                            if r.returncode != 0:
                                issues.append(f"{hf.relative_to(ROOT)} script[{i}] 语法错误: {r.stderr.strip()}")

    print(
        f"🔍 门禁 v2.0 扫描完成：{len(all_planned_slugs)} 个蓝图 slug，"
        f"{checked_topics} 个已点亮主题，{checked_html} 个 HTML 文件，发现问题：{len(issues)}"
    )
    for it in issues:
        print(" -", it)
    if issues:
        sys.exit(1)
    print("✅ 全部门禁检查通过！")


if __name__ == "__main__":
    main()
