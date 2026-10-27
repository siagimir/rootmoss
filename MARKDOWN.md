# Markdown style

**Dialect**: [GitHub Flavored Markdown
(GFM)](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).
Prefer pure Markdown over HTML except where GFM needs it (`<br>`,
`<details>`, rare `<sub>` / `<sup>`).

Agents and humans follow this when writing or polishing `.md` in this
tree.

## Line length

| Content                                     | Rule                                            |
| ------------------------------------------- | ----------------------------------------------- |
| Prose, bullets, numbered lists, blockquotes | Soft wrap at **≤80** columns (word boundaries)  |
| Headings                                    | Prefer ≤80; leave longer if a single title      |
| **Tables** (header, separator, body rows)   | **Exempt from 80-col** — pad for alignment only |
| Fenced code blocks                          | Do not wrap inside the fence                    |
| Single long URL or path                     | Prefer own line; if still >80, leave unbroken   |

Blank line between paragraphs. No two-space hard breaks as the default
line-break style.

## Headings

- ATX style: `#` … `###` (deeper only if truly needed)
- One `#` title per file
- Blank line before and after headings
- Do not skip levels (`#` → `###`)

## Lists

- Bullets: `-` (not `*` or `+`)
- Ordered: `1.` `2.` …
- Nested: 2 spaces before the marker
- Blank line before a list when it follows a prose paragraph

## Emphasis and code

| Style               | Use               |
| ------------------- | ----------------- |
| Bold                | `**text**`        |
| Italic              | `_text_`          |
| Strike              | `~~text~~`        |
| Inline code / paths | `` `like/this` `` |

Avoid `__bold__` and `*italic*`.

## Tables (raw readability)

GFM renders unpadded tables; **we pad** so monospaced raw files stay
scannable:

1. Blank line before the table
2. Leading and trailing `|` on every row
3. Separator row with at least three `-` per column
4. **Pad cells** so columns align across rows
5. Escape pipe in cell content: `\|`
6. **No 80-col wrap** on table rows — width follows content
7. Huge unreadable table → split it (editorial)

## Code blocks

- Fenced with triple backticks, language tag when known
- Blank line before and after the fence
- Do not wrap lines inside the fence

## Task lists

- [ ] open
- [x] done

## Out of scope

- Do not change meaning, links, or Status values while "polishing"
- No required linter

## Related

- `AGENTS.md` — the agent contract; points here under style
