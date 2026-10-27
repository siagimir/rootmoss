# inbox/

Staging for **session resumes** and occasional **unrouted dumps** — not
long-term memory.

## Purpose

1. Log short resumes of chats that had no topic home (or only a weak fit)
2. Later judge **recurrence** → propose `topics/<name>/`
3. When a topic is created, **fold resume substance in**, then remove the
   file

Also: drop a quick personal dump here when placement is unclear.

## Filename

`YYYY-MM-DD-short-kebab.md`

## Session resume template

```markdown
# Session: short title

**Date**: YYYY-MM-DD
**Status**: open
**Tags**: kebab, tags
**Topic fit**: none | partial → topics/foo

## Resume

- What was asked / decided / left open (bullets; enough to rebuild
  context)
- Concrete outcomes (settings, decisions, links, numbers)

## Seeds (if a topic is created later)

- Candidates for facts / decisions / lessons (one line each)

## Related inbox

- Links to earlier resumes on the same subject (if any)
```

## Status values

| Status      | Meaning                                     |
| ----------- | ------------------------------------------- |
| `open`      | Still relevant; default                     |
| `promoted`  | Folded into a topic — **delete** the file   |
| `discarded` | One-off / obsolete — delete when convenient |

## Agent behavior

- **Write resume** after meaningful off-topic / orphan work (auto)
- **Session start**: read/list header metadata only; flag recurring tags
  or subjects. Read the body only when it matches the active work.
- **start-topic**: ingest matching open resumes, then delete them
- **High-risk content** (health, credentials, raw account data): propose
  before writing a resume; never auto-stage
- **Do not** treat the inbox as typed memory — never keep long-lived
  knowledge only here
- Full chat transcripts never belong here — resumes only
