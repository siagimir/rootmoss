#!/usr/bin/env python3
"""Structural repo-audit helper for the Rootmoss tree (mechanical only).

Performs deterministic tree, skills, topics, inbox, and basic lifecycle
scans. Outputs JSON (machine) and/or Markdown snippet. Stdlib only.

Usage:
  python3 skills/repo-audit/scripts/audit_structural.py
  python3 skills/repo-audit/scripts/audit_structural.py --json /tmp/audit.json
  python3 skills/repo-audit/scripts/audit_structural.py --md notes/audit.md
"""

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def core_skills_from_agents() -> list[str] | None:
    """Skill ids named on AGENTS.md's `Core skills:` paragraph, if present."""
    agents = ROOT / "AGENTS.md"
    if not agents.exists():
        return None
    text = agents.read_text(encoding="utf-8")
    lines = text.splitlines()
    para: list[str] = []
    for i, line in enumerate(lines):
        if "Core skills" in line:
            para.append(line)
            # continuation: indented/backticked lines until blank line
            for cont in lines[i + 1 :]:
                if not cont.strip():
                    break
                para.append(cont)
            break
    if not para:
        return None
    ids = re.findall(r"`([a-z0-9-]+(?:/[a-z0-9-]+)?)`", "\n".join(para))
    return ids or None


def listed_topics_from_dashboard() -> list[str] | None:
    """Topic names in the personal-os `Topics:` bullet, if the repo keeps one."""
    dash = ROOT / "topics" / "personal-os" / "topic.md"
    if not dash.exists():
        return None
    text = dash.read_text(encoding="utf-8")
    chunk: list[str] = []
    capturing = False
    found = False
    for line in text.splitlines():
        if line.startswith("- Topics:"):
            capturing = True
            found = True
            chunk.append(line)
            continue
        if capturing:
            if line.startswith("- "):
                break
            chunk.append(line)
    if not found:
        return None
    return sorted(set(re.findall(r"`([a-z0-9-]+)`", "\n".join(chunk))))


def main() -> None:
    parser = argparse.ArgumentParser(description="Structural repo-audit (no LLM)")
    parser.add_argument("--json", type=Path, help="Write machine-readable report")
    parser.add_argument("--md", type=Path, help="Write human Markdown summary")
    args = parser.parse_args()

    report: dict = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tree_shape": {},
        "skills_match": {},
        "topics_match": {},
        "inbox": {},
        "lifecycle": {},
        "issues": [],
    }

    topics_dir = ROOT / "topics"
    skills_dir = ROOT / "skills"

    topic_dirs = sorted([p.name for p in topics_dir.iterdir() if p.is_dir()])
    skill_ids = sorted(
        str(p.parent.relative_to(skills_dir))
        for p in skills_dir.rglob("SKILL.md")
    )
    skill_dirs = sorted([p.name for p in skills_dir.iterdir() if p.is_dir()])

    report["tree_shape"]["topics"] = topic_dirs
    report["tree_shape"]["skills"] = skill_ids
    report["tree_shape"]["skill_top_dirs"] = skill_dirs

    # Every top-level topic has topic.md
    missing_topic_md = [
        t for t in topic_dirs if not (topics_dir / t / "topic.md").exists()
    ]
    if missing_topic_md:
        report["issues"].append(
            {"type": "missing_topic_md", "items": missing_topic_md}
        )

    # Any nested dir that looks like a topic (has notes/ or memory/)
    # must carry its own topic.md.
    missing_nested = []
    for md_file in topics_dir.rglob("topic.md"):
        pass  # presence already implied
    for group_dir in topics_dir.rglob("*"):
        if not group_dir.is_dir() or group_dir == topics_dir:
            continue
        if any((group_dir / sub).is_dir() for sub in ("notes", "memory")):
            if not (group_dir / "topic.md").exists():
                missing_nested.append(str(group_dir.relative_to(ROOT)))
    if missing_nested:
        report["issues"].append(
            {"type": "missing_nested_topic_md", "items": sorted(set(missing_nested))}
        )

    # Top-level skill dirs that look like skill folders but ship no
    # SKILL.md anywhere inside.
    missing_skill_md = []
    for top in skill_dirs:
        top_path = skills_dir / top
        if not (top_path / "SKILL.md").exists() and not any(
            top_path.rglob("SKILL.md")
        ):
            missing_skill_md.append(top)
    if missing_skill_md:
        report["issues"].append(
            {"type": "missing_skill_md", "items": missing_skill_md}
        )

    # AGENTS.md `Core skills:` line vs discovered skills (skipped if the
    # line is absent).
    expected_skills = core_skills_from_agents()
    if expected_skills is None:
        report["skills_match"]["skipped"] = "no Core skills line in AGENTS.md"
    else:
        missing_skills = [s for s in expected_skills if s not in skill_ids]
        extra_skills = [s for s in skill_ids if s not in expected_skills]
        if missing_skills or extra_skills:
            report["skills_match"]["mismatch"] = True
            report["issues"].append(
                {
                    "type": "skills_table_mismatch",
                    "missing": missing_skills,
                    "extra": extra_skills,
                }
            )
        else:
            report["skills_match"]["match"] = True

    # Optional topic registry (personal-os dashboard `Topics:` bullet)
    expected_topics = listed_topics_from_dashboard()
    if expected_topics is None:
        report["topics_match"]["skipped"] = "no Topics: registry bullet"
    else:
        missing_topics = [t for t in expected_topics if t not in topic_dirs]
        extra_topics = [t for t in topic_dirs if t not in expected_topics]
        if missing_topics or extra_topics:
            report["topics_match"]["mismatch"] = True
            report["issues"].append(
                {
                    "type": "topics_list_mismatch",
                    "missing": missing_topics,
                    "extra": extra_topics,
                }
            )
        else:
            report["topics_match"]["match"] = True

    # Inbox state (open resumes only)
    inbox_dir = ROOT / "inbox"
    open_resumes = sorted(
        [
            f.name
            for f in inbox_dir.iterdir()
            if f.is_file() and f.name != "README.md"
        ]
    )
    report["inbox"]["open_resumes"] = open_resumes
    if open_resumes:
        report["issues"].append(
            {
                "type": "open_inbox_resumes",
                "count": len(open_resumes),
                "files": open_resumes,
            }
        )

    # Nested topic.md inventory
    nested: list[str] = []
    for topic_md in topics_dir.rglob("topic.md"):
        rel = topic_md.relative_to(topics_dir)
        if len(rel.parts) > 2:
            nested.append(str(rel.parent))
    report["tree_shape"]["nested_topics"] = nested

    # Lightweight lifecycle Status scan (memory/ only)
    memory_roots = [ROOT / "memory"] + [
        p for p in topics_dir.rglob("memory") if p.is_dir()
    ]
    missing_status: list[str] = []
    for mem_root in memory_roots:
        if not mem_root.exists():
            continue
        for md_file in mem_root.rglob("*.md"):
            if md_file.name == "README.md":
                continue
            try:
                content = md_file.read_text(encoding="utf-8", errors="ignore")
                if "**Status**" not in content and "Status:" not in content[:200]:
                    missing_status.append(str(md_file.relative_to(ROOT)))
            except Exception:
                pass
    if missing_status:
        report["lifecycle"]["missing_status_count"] = len(missing_status)
        report["issues"].append(
            {
                "type": "missing_status",
                "count": len(missing_status),
                "sample": missing_status[:5],
            }
        )

    # Write outputs
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"JSON report written to {args.json}")

    if args.md:
        args.md.parent.mkdir(parents=True, exist_ok=True)
        md_text = _generate_md(report)
        args.md.write_text(md_text, encoding="utf-8")
        print(f"Markdown summary written to {args.md}")

    if not args.json and not args.md:
        print(json.dumps(report, indent=2))


def _generate_md(report: dict) -> str:
    lines: list[str] = [
        "# Structural Audit Report (deterministic)",
        f"**Generated**: {report['timestamp']}",
        "",
    ]

    if not report["issues"]:
        lines.append("**Result**: PASS (all structural checks)")
        lines.append("")
    else:
        lines.append("## Issues Found")
        for issue in report["issues"]:
            lines.append(f"- **{issue['type']}**: {json.dumps(issue, indent=2)}")
        lines.append("")

    lines.append("## Summary")
    lines.append(f"- Topics discovered: {len(report['tree_shape']['topics'])}")
    nested_n = len(report["tree_shape"].get("nested_topics") or [])
    lines.append(f"- Nested topics: {nested_n}")
    lines.append(f"- Skills discovered: {len(report['tree_shape']['skills'])}")
    lines.append(
        f"- Open inbox resumes: {len(report['inbox'].get('open_resumes', []))}"
    )
    if report["lifecycle"].get("missing_status_count"):
        lines.append(
            f"- Memory files missing Status: "
            f"{report['lifecycle']['missing_status_count']}"
        )

    lines.append("")
    lines.append("Run with `--json` / `--md` for machine + human output.")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
