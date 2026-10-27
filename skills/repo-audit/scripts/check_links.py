#!/usr/bin/env python3
"""Link resolution checker for Rootmoss (mechanical only).

Scans *.md files for relative Markdown links and validates them.
Follows the repo-audit rules:
- Resolve from the file's directory first
- If not found, try from the nearest topic root (topics/<name>/)
- Root memory refs from topics/ should use ../../memory/...

Stdlib only. Safe, read-only.

Usage:
  python3 skills/repo-audit/scripts/check_links.py
  python3 skills/repo-audit/scripts/check_links.py --json /tmp/links.json
  python3 skills/repo-audit/scripts/check_links.py --md notes/link-audit.md
"""

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any

ROOT = Path(__file__).resolve().parents[3]
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+?\.md(?:#[^)]*)?)\)")


def find_topic_roots(file_path: Path) -> List[Path]:
    """Ancestors that contain topic.md, nearest (child) first, then hub."""
    roots: List[Path] = []
    cur = file_path.parent
    while cur != ROOT and cur.name != "topics":
        if (cur / "topic.md").exists():
            roots.append(cur)
        if cur.parent == cur:
            break
        cur = cur.parent
    return roots


def resolve_link(
    link: str, file_dir: Path, topic_roots: List[Path]
) -> Path | None:
    """Resolve from file dir, then each ancestor topic root."""
    candidate = (file_dir / link.split("#")[0]).resolve()
    if candidate.exists():
        return candidate

    for topic_root in topic_roots:
        candidate2 = (topic_root / link.split("#")[0]).resolve()
        if candidate2.exists():
            return candidate2

    return None


def check_file(md_file: Path) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []
    try:
        content = md_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return issues

    file_dir = md_file.parent
    topic_roots = find_topic_roots(md_file)

    for match in LINK_RE.finditer(content):
        link = match.group(2).split("#")[0]
        if link.startswith(("http://", "https://", "mailto:")):
            continue  # external, not our concern

        resolved = resolve_link(link, file_dir, topic_roots)
        if not resolved:
            issues.append(
                {
                    "file": str(md_file.relative_to(ROOT)),
                    "link": link,
                    "line": content[: match.start()].count("\n") + 1,
                    "suggestion": "check path relative to file or topic root",
                }
            )

    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Link checker (deterministic)")
    parser.add_argument("--json", type=Path)
    parser.add_argument("--md", type=Path)
    args = parser.parse_args()

    all_issues: List[Dict[str, Any]] = []

    skip_dirs = {
        "node_modules",
        ".git",
        "__pycache__",
        "playwright-report",
        "test-results",
    }
    for md_file in ROOT.rglob("*.md"):
        if any(part in skip_dirs for part in md_file.parts):
            continue
        if "manuals/extracts" in str(md_file):
            continue
        issues = check_file(md_file)
        all_issues.extend(issues)

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "broken_links": len(all_issues),
        "issues": all_issues,
    }

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"JSON written to {args.json}")

    if args.md:
        args.md.parent.mkdir(parents=True, exist_ok=True)
        md_text = _generate_md(report)
        args.md.write_text(md_text, encoding="utf-8")
        print(f"Markdown written to {args.md}")

    if not args.json and not args.md:
        print(json.dumps(report, indent=2))


def _generate_md(report: Dict[str, Any]) -> str:
    lines = [
        "# Link Audit Report (deterministic)",
        f"**Generated**: {report['timestamp']}",
        "",
    ]

    if report["broken_links"] == 0:
        lines.append("**Result**: No broken relative links found")
    else:
        lines.append(f"**Broken links found**: {report['broken_links']}")
        lines.append("")
        for issue in report["issues"][:50]:  # cap output
            lines.append(
                f"- `{issue['file']}`:{issue['line']} → `{issue['link']}`"
            )
        if len(report["issues"]) > 50:
            lines.append(f"... and {len(report['issues']) - 50} more")

    lines.append("")
    lines.append("Run with `--json` / `--md` for full output.")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
