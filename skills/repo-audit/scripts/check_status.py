#!/usr/bin/env python3
"""Status linter for Rootmoss memory files.

Detects memory/*.md files missing the canonical **Status** line.
Helps with the recurring "bulk backfill" decision item in audits.

Stdlib only. Safe, read-only.

Usage:
  python3 skills/repo-audit/scripts/check_status.py
  python3 skills/repo-audit/scripts/check_status.py --json /tmp/status.json
  python3 skills/repo-audit/scripts/check_status.py --md notes/status-audit.md
"""

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any

ROOT = Path(__file__).resolve().parents[3]


def scan_memory_files() -> List[Path]:
    candidates: List[Path] = []
    # Root memory/
    if (ROOT / "memory").exists():
        candidates.extend((ROOT / "memory").rglob("*.md"))
    # Topic memory/ (including nested children)
    for topic_mem in (ROOT / "topics").rglob("memory"):
        if topic_mem.is_dir():
            candidates.extend(topic_mem.rglob("*.md"))
    return sorted(set(candidates))


def has_status(md_file: Path) -> bool:
    try:
        content = md_file.read_text(encoding="utf-8", errors="ignore")
        # Look for the canonical form near the top
        head = content[:1500]
        return "**Status**" in head or "Status:" in head[:300]
    except Exception:
        return True  # don't flag unreadable files


def main() -> None:
    parser = argparse.ArgumentParser(description="Status linter (missing **Status**)")
    parser.add_argument("--json", type=Path)
    parser.add_argument("--md", type=Path)
    args = parser.parse_args()

    files = scan_memory_files()
    missing: List[str] = []
    by_topic: Dict[str, int] = defaultdict(int)

    for f in files:
        if f.name == "README.md":
            continue
        if not has_status(f):
            rel = str(f.relative_to(ROOT))
            missing.append(rel)
            # Group by topic or root
            if "topics/" in rel:
                topic = rel.split("/")[1]
            else:
                topic = "root"
            by_topic[topic] += 1

    report: Dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_memory_files": len(files),
        "missing_status_count": len(missing),
        "by_topic": dict(by_topic),
        "missing_sample": missing[:10],
        "all_missing": missing,
    }

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"JSON written to {args.json}")

    if args.md:
        args.md.parent.mkdir(parents=True, exist_ok=True)
        args.md.write_text(_generate_md(report), encoding="utf-8")
        print(f"Markdown written to {args.md}")

    if not args.json and not args.md:
        print(json.dumps(report, indent=2))


def _generate_md(report: Dict[str, Any]) -> str:
    lines = [
        "# Status Linter Report",
        f"**Generated**: {report['timestamp']}",
        "",
        f"**Total memory files scanned**: {report['total_memory_files']}",
        f"**Missing **Status****: {report['missing_status_count']}",
        "",
    ]

    if report["missing_status_count"] == 0:
        lines.append("**Result**: All memory files have **Status**")
    else:
        lines.append("## Missing by location")
        for topic, count in sorted(report["by_topic"].items()):
            lines.append(f"- {topic}: {count}")
        lines.append("")
        lines.append("## Sample (first 10)")
        for path in report["missing_sample"]:
            lines.append(f"- `{path}`")
        if len(report["all_missing"]) > 10:
            lines.append(f"... +{len(report['all_missing']) - 10} more")

    lines.append("")
    lines.append("Use this to decide on bulk backfill or individual fixes.")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
