#!/usr/bin/env python3
"""
AI-Interactive-Taxonomy 质量门禁脚本
检查项：
1. taxonomy.json 合法性与域/分支唯一性
2. domains/<domain>/<topic>/ 下的 meta.json 合法性与归属校验
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
    for d in taxonomy["domains"]:
        valid_domains[d["id"]] = {b["id"] for b in d.get("branches", [])}

    has_node = subprocess.run(["which", "node"], capture_output=True).returncode == 0
    checked_topics = 0
    checked_html = 0

    if DOMAINS_DIR.exists():
        for dom_dir in sorted(DOMAINS_DIR.iterdir()):
            if not dom_dir.is_dir() or dom_dir.name.startswith("."):
                continue
            if dom_dir.name not in valid_domains:
                issues.append(f"未知领域目录: domains/{dom_dir.name}（未在 taxonomy.json 中定义）")
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

    print(f"🔍 质量门禁扫描完成：{checked_topics} 个主题，{checked_html} 个 HTML 文件，发现问题：{len(issues)}")
    for it in issues:
        print(" -", it)
    if issues:
        sys.exit(1)
    print("✅ 全部检查通过！")


if __name__ == "__main__":
    main()
