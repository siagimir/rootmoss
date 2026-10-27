---
name: markdown-style
description: Apply the Rootmoss Markdown raw form (GFM, prose ≤80, padded
tables exempt from wrap). Use when polishing .md, bulk reformat, or on
"markdown style".
---

# markdown-style

## When to use

- User asks to polish Markdown, wrap lines, align tables
- After large writes that ignored `MARKDOWN.md`
- Optional: run the formatter script on paths

## Rules

Follow **`MARKDOWN.md`** exactly:

- GFM dialect
- Prose/bullets soft wrap **≤80** cols
- **Tables exempt** from 80 — pad columns for monospaced scan
- Do not change meaning while polishing

## Formatter

Optional helper (idempotent):

```bash
python3 skills/markdown-style/scripts/format_md.py
python3 skills/markdown-style/scripts/format_md.py --dry-run
python3 skills/markdown-style/scripts/format_md.py --paths path/to/file.md
```

## Related

- `MARKDOWN.md` — full style guide
- `AGENTS.md` Style section
