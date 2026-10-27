#!/usr/bin/env python3
"""Memory header migration tool (deterministic, safe).

Adds the standardized header to memory files that are missing it.
Uses git to determine creation date for old files.
Never modifies files by default — always dry-run first.

Usage:
  python3 skills/repo-audit/scripts/migrate_memory_headers.py --dry-run
  python3 skills/repo-audit/scripts/migrate_memory_headers.py --report notes/migration-report.md
  python3 skills/repo-audit/scripts/migrate_memory_headers.py --patches /tmp/patches
  python3 ... --apply   # only after you reviewed the patches
"""

import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

ROOT = Path(__file__).resolve().parents[3]
MEMORY_ROOTS = [ROOT / "memory"] + list((ROOT / "topics").glob("*/memory"))

TYPE_MAP = {
    "facts": "fact",
    "decisions": "decision",
    "lessons": "lesson",
    "preferences": "preference",
    "assumptions": "assumption",
    "context": "context",
}


def get_creation_date(file_path: Path) -> str:
    """Prefer filename date (YYYY-MM-DD- prefix) for legacy files.
    Fall back to git creation date only when filename has no date."""
    name = file_path.name
    if len(name) >= 10 and name[4] == name[7] == "-":
        # Looks like YYYY-MM-DD-...
        try:
            datetime.strptime(name[:10], "%Y-%m-%d")
            return name[:10]
        except ValueError:
            pass

    # Fallback to git
    try:
        result = subprocess.run(
            [
                "git",
                "log",
                "--follow",
                "--format=%ad",
                "--date=short",
                "-1",
                "--",
                str(file_path),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        date = result.stdout.strip()
        if date:
            return date
    except Exception:
        pass
    return datetime.now().strftime("%Y-%m-%d")


def needs_header(file_path: Path) -> bool:
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        # Needs migration if missing the new standardized keys
        return "**Created on**" not in content or "**Type**" not in content
    except Exception:
        return False


def get_type_from_path(file_path: Path) -> str:
    parent = file_path.parent.name
    return TYPE_MAP.get(parent, "fact")


def generate_header(file_path: Path) -> str:
    created = get_creation_date(file_path)
    typ = get_type_from_path(file_path)

    # Preserve existing Status value if present (superseded/closed), else default to active
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        import re
        m = re.search(r"\*\*Status\*\*:\s*(\w+)", content)
        status = m.group(1) if m else "active"
    except Exception:
        status = "active"

    return f"""**Type**: {typ}
**Status**: {status}
**Created on**: {created}

"""


def create_patch(file_path: Path, header: str) -> str:
    """Return a unified diff style patch for the file."""
    rel = file_path.relative_to(ROOT)
    old_content = file_path.read_text(encoding="utf-8", errors="ignore").splitlines(keepends=True)
    new_content = [header] + old_content
    diff = []
    diff.append(f"diff --git a/{rel} b/{rel}\n")
    diff.append("index 0000000..0000000 100644\n")
    diff.append(f"--- a/{rel}\n")
    diff.append(f"+++ b/{rel}\n")
    diff.append("@@ -0,0 +1," + str(len(header.splitlines())) + " @@\n")
    for line in header.splitlines():
        diff.append("+" + line + "\n")
    return "".join(diff)


def apply_header(file_path: Path, header: str) -> None:
    """Remove any old Status/Date lines, then insert clean standardized header after title."""
    content = file_path.read_text(encoding="utf-8", errors="ignore")
    lines = content.splitlines(keepends=True)

    # First pass: strip all old Status/Date lines (they may appear anywhere)
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("**Status**:") or stripped.startswith("**Date**:"):
            continue
        cleaned_lines.append(line)

    # Second pass: insert fresh header after title
    if cleaned_lines and cleaned_lines[0].startswith("# "):
        new_lines = [cleaned_lines[0], "\n", header] + cleaned_lines[1:]
    else:
        new_lines = [header] + cleaned_lines

    file_path.write_text("".join(new_lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Memory header migration (safe)")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--patches", type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--yes", action="store_true", help="Final confirmation for --apply")
    parser.add_argument("--topic", type=str, help="Only process this topic (e.g. a specific topic)")
    args = parser.parse_args()

    files_to_migrate: List[Path] = []
    for mem_root in MEMORY_ROOTS:
        if not mem_root.exists():
            continue
        for md in mem_root.rglob("*.md"):
            if md.name == "README.md":
                continue
            if args.topic:
                # Only process files under topics/<topic>/memory/
                rel = md.relative_to(ROOT)
                if not (rel.parts[0] == "topics" and rel.parts[1] == args.topic):
                    continue
            if needs_header(md):
                files_to_migrate.append(md)

    report_lines = [
        "# Memory Header Migration Report",
        f"**Generated**: {datetime.now().isoformat()}",
        f"**Files needing header**: {len(files_to_migrate)}",
        "",
    ]

    if args.patches:
        args.patches.mkdir(parents=True, exist_ok=True)

    for f in files_to_migrate:
        header = generate_header(f)
        rel = f.relative_to(ROOT)
        report_lines.append(f"- `{rel}` → Type: {get_type_from_path(f)} | Created: {get_creation_date(f)}")

        if args.patches:
            patch = create_patch(f, header)
            patch_file = args.patches / (rel.name + ".patch")
            patch_file.write_text(patch, encoding="utf-8")

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text("\n".join(report_lines), encoding="utf-8")
        print(f"Report written to {args.report}")

    if args.patches:
        print(f"Patches written to {args.patches}")

    if not args.report and not args.patches:
        print("\n".join(report_lines))

    if args.apply:
        if not args.yes:
            print("\n!!! SAFETY: --apply requires --yes flag.")
            print("    This will modify memory files. Review the report first.")
            print("    Example: python3 ... --apply --yes")
            return

        print(f"\nApplying headers to {len(files_to_migrate)} files...")
        for f in files_to_migrate:
            header = generate_header(f)
            apply_header(f, header)
            print(f"  + {f.relative_to(ROOT)}")

        print("\nMigration complete. Re-run the status linter to verify.")


if __name__ == "__main__":
    main()
