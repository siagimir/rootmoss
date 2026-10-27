#!/usr/bin/env python3
"""Memory header structure validator (deterministic).

Checks that all memory files have the required standardized header:
- **Type**
- **Status**
- **Created on**

Reports missing or malformed headers. Stdlib only.

Usage:
  python3 skills/repo-audit/scripts/check_memory_headers.py
  python3 skills/repo-audit/scripts/check_memory_headers.py --json /tmp/headers.json
  python3 skills/repo-audit/scripts/check_memory_headers.py --md notes/header-audit.md
"""

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any

ROOT = Path(__file__).resolve().parents[3]
MEMORY_ROOTS = [ROOT / "memory"] + [
    p for p in (ROOT / "topics").rglob("memory") if p.is_dir()
]

REQUIRED_KEYS = ["**Type**", "**Status**", "**Created on**"]
TYPE_VALUES = {"fact", "decision", "lesson", "preference", "assumption", "context"}
STATUS_VALUES = {"active", "superseded", "closed"}


def check_file(md_file: Path) -> List[Dict[str, str]]:
    issues: List[Dict[str, str]] = []
    try:
        content = md_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return [{"file": str(md_file.relative_to(ROOT)), "issue": "unreadable"}]

    if md_file.name == "README.md":
        return issues

    for key in REQUIRED_KEYS:
        if key not in content:
            issues.append({
                "file": str(md_file.relative_to(ROOT)),
                "issue": f"missing {key}"
            })

    # Basic value validation (only if keys are present)
    if "**Type**:" in content:
        m = re.search(r"\*\*Type\*\*:\s*(\w+)", content)
        if m and m.group(1) not in TYPE_VALUES:
            issues.append({
                "file": str(md_file.relative_to(ROOT)),
                "issue": f"invalid Type: {m.group(1)}"
            })

    if "**Status**:" in content:
        m = re.search(r"\*\*Status\*\*:\s*(\w+)", content)
        if m and m.group(1) not in STATUS_VALUES:
            issues.append({
                "file": str(md_file.relative_to(ROOT)),
                "issue": f"invalid Status: {m.group(1)}"
            })

    if "**Created on**:" in content:
        m = re.search(r"\*\*Created on\*\*:\s*(\d{4}-\d{2}-\d{2})", content)
        if not m:
            issues.append({
                "file": str(md_file.relative_to(ROOT)),
                "issue": "malformed Created on date"
            })

    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Memory header validator")
    parser.add_argument("--json", type=Path)
    parser.add_argument("--md", type=Path)
    args = parser.parse_args()

    all_issues: List[Dict[str, str]] = []

    for mem_root in MEMORY_ROOTS:
        if not mem_root.exists():
            continue
        for md in mem_root.rglob("*.md"):
            issues = check_file(md)
            all_issues.extend(issues)

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "files_checked": "all memory/*.md except READMEs",
        "issues_found": len(all_issues),
        "issues": all_issues,
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
        "# Memory Header Validation Report",
        f"**Generated**: {report['timestamp']}",
        "",
        f"**Issues found**: {report['issues_found']}",
        "",
    ]

    if report["issues_found"] == 0:
        lines.append("**Result**: All memory files have valid standardized headers")
    else:
        lines.append("## Issues")
        for issue in report["issues"]:
            lines.append(f"- `{issue['file']}`: {issue['issue']}")

    lines.append("")
    lines.append("Run with `--json` / `--md` for machine + human output.")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
