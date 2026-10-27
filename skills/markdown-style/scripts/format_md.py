#!/usr/bin/env python3
"""Format Rootmoss Markdown per MARKDOWN.md (prose ≤80; pad tables; no table wrap)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

WIDTH = 80
SKIP_PARTS = ("manuals/extracts",)


def should_skip(path: Path, root: Path) -> bool:
    rel = path.relative_to(root).as_posix()
    if any(s in rel for s in SKIP_PARTS):
        return True
    if path.name == "format_md.py":
        return True
    return False


def is_table_sep(line: str) -> bool:
    s = line.strip()
    if not s.startswith("|"):
        return False
    # | --- | :---: | ---: |
    core = s.strip("|").strip()
    if not core:
        return False
    parts = [p.strip() for p in s.split("|")]
    parts = [p for p in parts if p != ""]
    if not parts:
        return False
    return all(re.fullmatch(r":?-{3,}:?", p.strip()) for p in parts)


def is_table_row(line: str) -> bool:
    s = line.rstrip("\n")
    if "|" not in s:
        return False
    t = s.strip()
    if not t.startswith("|"):
        return False
    # at least two pipes
    if t.count("|") < 2:
        return False
    return True


def split_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def format_table(rows: list[str]) -> list[str]:
    parsed = [split_row(r) for r in rows]
    if not parsed:
        return rows
    ncols = max(len(r) for r in parsed)
    for r in parsed:
        while len(r) < ncols:
            r.append("")
    # widths from non-separator rows content; sep uses dashes
    widths = [0] * ncols
    sep_idx = None
    for i, r in enumerate(parsed):
        if is_table_sep(rows[i]):
            sep_idx = i
            continue
        for j, cell in enumerate(r):
            widths[j] = max(widths[j], len(cell))
    # minimum 3 for sep
    widths = [max(w, 3) for w in widths]

    out = []
    for i, r in enumerate(parsed):
        if sep_idx is not None and i == sep_idx:
            cells = []
            raw_cells = split_row(rows[i])
            while len(raw_cells) < ncols:
                raw_cells.append("---")
            for j in range(ncols):
                spec = raw_cells[j].strip() if j < len(raw_cells) else "---"
                left = spec.startswith(":")
                right = spec.endswith(":")
                # body of dashes
                dash_n = widths[j]
                if left and right:
                    inner = ":" + ("-" * max(dash_n - 2, 1)) + ":"
                elif right:
                    inner = ("-" * max(dash_n - 1, 1)) + ":"
                elif left:
                    inner = ":" + ("-" * max(dash_n - 1, 1))
                else:
                    inner = "-" * dash_n
                # pad inner to width for alignment of pipes
                if len(inner) < widths[j]:
                    # expand dashes in middle
                    if left and right:
                        need = widths[j] - len(inner)
                        inner = ":" + ("-" * (max(dash_n - 2, 1) + need)) + ":"
                    elif left:
                        need = widths[j] - len(inner)
                        inner = ":" + ("-" * (max(dash_n - 1, 1) + need))
                    elif right:
                        need = widths[j] - len(inner)
                        inner = ("-" * (max(dash_n - 1, 1) + need)) + ":"
                    else:
                        inner = "-" * widths[j]
                cells.append(inner.ljust(widths[j]))
            out.append("| " + " | ".join(cells) + " |")
        else:
            cells = [r[j].ljust(widths[j]) for j in range(ncols)]
            out.append("| " + " | ".join(cells) + " |")
    return out


def wrap_text(text: str, width: int, subsequent_indent: str = "") -> list[str]:
    text = text.rstrip()
    if not text:
        return [""]
    # never break inside a single unbreakable token longer than width
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    cur = words[0]
    first = True
    for w in words[1:]:
        limit = width if first else max(width - len(subsequent_indent), 1)
        if len(cur) + 1 + len(w) <= limit:
            cur = cur + " " + w
        else:
            lines.append(cur)
            cur = w
            first = False
    lines.append(cur)
    if not subsequent_indent:
        return lines
    return [lines[0]] + [subsequent_indent + L for L in lines[1:]]


def prefix_and_body(line: str) -> tuple[str, str] | None:
    """Return (prefix including trailing space, body) for wrappable lines."""
    if line.startswith("#"):
        return None
    if line.startswith("```"):
        return None
    if line.startswith("|"):
        return None
    if line.startswith("\t"):
        return None
    if re.match(r"^[-*_]{3,}\s*$", line.strip()):
        return None
    if line.strip() == "":
        return None
    # ASCII trees / box drawing — leave alone
    if re.search(r"[│├└─┌┐┘┤┴┬┼╱╲↗↘←→↑↓]", line):
        return None
    # pure indented code block (4 spaces) without list marker
    if re.match(r"^    [^-+*\d>]", line):
        return None

    # blockquote
    m2 = re.match(r"^((?:>\s?)+)(.*)$", line)
    if m2 and not line.lstrip().startswith("> [!"):
        return m2.group(1), m2.group(2)

    # unordered list (incl. task lists)
    m = re.match(r"^(\s*[-]\s+)(.*)$", line)
    if m:
        return m.group(1), m.group(2)

    # ordered list
    m = re.match(r"^(\s*\d+\.\s+)(.*)$", line)
    if m:
        return m.group(1), m.group(2)

    # already-wrapped continuation (indent + text, not a nested list)
    m = re.match(r"^(\s{2,})(\S.*)$", line)
    if m:
        rest = m.group(2)
        if rest.startswith("- ") or re.match(r"^\d+\.\s", rest):
            pass  # nested list handled above if marker at indent
        else:
            return m.group(1), rest

    # plain prose (column 0)
    if line.startswith(" "):
        return None
    return "", line


def format_content(text: str) -> str:
    # normalize newlines
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    # drop trailing spaces on lines (not meaningful for us)
    lines = [ln.rstrip() for ln in lines]

    out: list[str] = []
    i = 0
    in_fence = False

    while i < len(lines):
        line = lines[i]

        if line.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            i += 1
            continue

        if in_fence:
            out.append(line)
            i += 1
            continue

        # table block
        if is_table_row(line) and i + 1 < len(lines) and is_table_sep(lines[i + 1]):
            block = [line, lines[i + 1]]
            j = i + 2
            while j < len(lines) and is_table_row(lines[j]) and not is_table_sep(lines[j]):
                # continuation of table; stop on blank
                if lines[j].strip() == "":
                    break
                block.append(lines[j])
                j += 1
            # ensure blank line before table
            if out and out[-1].strip() != "":
                out.append("")
            out.extend(format_table(block))
            i = j
            continue

        # single table-like row without sep — leave (might be prose with |)
        pb = prefix_and_body(line)
        if pb is None:
            out.append(line)
            i += 1
            continue

        prefix, body = pb
        if not body:
            out.append(line)
            i += 1
            continue

        full = prefix + body
        if len(full) <= WIDTH:
            out.append(full)
            i += 1
            continue

        # unbreakable single token
        if " " not in body and len(full) > WIDTH:
            out.append(full)
            i += 1
            continue

        sub_indent = " " * len(prefix) if prefix else ""
        wrapped = wrap_text(body, WIDTH - len(prefix) if prefix else WIDTH, "")
        # first line with prefix; rest with indent
        out.append(prefix + wrapped[0])
        for cont in wrapped[1:]:
            out.append(sub_indent + cont)
        i += 1

    # collapse 3+ blank lines to 2
    collapsed: list[str] = []
    blank_run = 0
    for ln in out:
        if ln.strip() == "":
            blank_run += 1
            if blank_run <= 2:
                collapsed.append("")
        else:
            blank_run = 0
            collapsed.append(ln)

    result = "\n".join(collapsed)
    if text.endswith("\n") or not text:
        if not result.endswith("\n"):
            result += "\n"
    else:
        # keep final newline convention: always end with newline
        if not result.endswith("\n"):
            result += "\n"
    return result


def iter_md_files(root: Path) -> list[Path]:
    files = []
    for p in sorted(root.rglob("*.md")):
        if ".git" in p.parts:
            continue
        if should_skip(p, root):
            continue
        files.append(p)
    return files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--paths", nargs="*", help="optional subset of files")
    args = ap.parse_args()
    root = args.root.resolve()

    if args.paths:
        files = [Path(p).resolve() for p in args.paths]
    else:
        files = iter_md_files(root)

    changed = 0
    for f in files:
        if not f.is_file():
            continue
        if should_skip(f, root):
            continue
        original = f.read_text(encoding="utf-8")
        formatted = format_content(original)
        if formatted != original:
            changed += 1
            rel = f.relative_to(root) if f.is_relative_to(root) else f
            if args.dry_run:
                print(f"would change: {rel}")
            else:
                f.write_text(formatted, encoding="utf-8")
                print(f"changed: {rel}")

    print(f"{'would change' if args.dry_run else 'changed'} {changed} / {len(files)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
