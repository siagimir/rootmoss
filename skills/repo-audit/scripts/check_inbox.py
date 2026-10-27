#!/usr/bin/env python3
"""Inbox scanner for Rootmoss (metadata only).

Lists open resumes/dumps with title, status, tags, topic-fit only.
Never reads full body unless explicitly asked. Matches AGENTS.md inbox rules.

Stdlib only. Safe, read-only.

Usage:
  python3 skills/repo-audit/scripts/check_inbox.py
  python3 skills/repo-audit/scripts/check_inbox.py --json /tmp/inbox.json
  python3 skills/repo-audit/scripts/check_inbox.py --md notes/inbox-audit.md
"""

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any

ROOT = Path(__file__).resolve().parents[3]
INBOX = ROOT / "inbox"

TAG_RE = re.compile(
    r"\*{0,2}tags?\*{0,2}:\s*\[?([^\n\]]+)\]?", re.IGNORECASE
)
STATUS_RE = re.compile(
    r"\*{0,2}status\*{0,2}:\s*([a-z-]+)", re.IGNORECASE
)
TOPIC_RE = re.compile(
    r"\*{0,2}topic[ -]?fit\*{0,2}:\s*(.+)", re.IGNORECASE
)


def extract_metadata(md_file: Path) -> Dict[str, Any]:
    try:
        lines = md_file.read_text(encoding="utf-8", errors="ignore").splitlines()[:15]
    except Exception:
        return {"title": md_file.stem, "status": "unknown"}

    title = md_file.stem
    status = None
    tags: List[str] = []
    topic_fit = None

    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break

    head = "\n".join(lines)
    if m := STATUS_RE.search(head):
        status = m.group(1).strip()
    if m := TAG_RE.search(head):
        tags = [t.strip() for t in m.group(1).split(",") if t.strip()]
    if m := TOPIC_RE.search(head):
        topic_fit = m.group(1).strip().strip("*").strip()

    return {
        "title": title,
        "status": status or "open",
        "tags": tags,
        "topic_fit": topic_fit,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Inbox scanner (metadata only)")
    parser.add_argument("--json", type=Path)
    parser.add_argument("--md", type=Path)
    args = parser.parse_args()

    if not INBOX.exists():
        report = {"timestamp": datetime.now(timezone.utc).isoformat(), "open_count": 0, "items": []}
    else:
        items = []
        for f in sorted(INBOX.iterdir()):
            if f.is_file() and f.name != "README.md":
                meta = extract_metadata(f)
                meta["file"] = f.name
                items.append(meta)

        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "open_count": len(items),
            "items": items,
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
        "# Inbox Scan Report (metadata only)",
        f"**Generated**: {report['timestamp']}",
        "",
        f"**Open resumes/dumps**: {report['open_count']}",
        "",
    ]

    if report["open_count"] == 0:
        lines.append("No open inbox items.")
    else:
        for item in report["items"]:
            tags_str = ", ".join(item.get("tags", [])) or "—"
            topic = item.get("topic_fit") or "—"
            lines.append(
                f"- **{item['file']}** — {item['title']} | status: {item['status']} | tags: [{tags_str}] | topic-fit: {topic}"
            )

    lines.append("")
    lines.append("Only metadata shown. Full body read only on explicit request or topic match.")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
