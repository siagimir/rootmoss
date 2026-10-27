---
name: extract-memory
description: After meaningful discussion, identify durable information and
save typed memory. Topic-local writes are automatic; root memory still
needs confirmation unless the user already said to save. Also
close/supersede stale atoms and keep topic.md current. Prefer entity
dossiers over micro-atoms.
---

# extract-memory

## When to run (automatic)

Run **without being asked** when any of these hold:

- End of a meaningful discussion that produced facts, decisions,
  lessons, preferences, assumptions, or situational context
- User is about to leave the topic / session wind-down / "thx" after
  real work
- A deliberate choice was made ("we'll do X not Y")
- A research outcome or plan that future sessions need
- An assumption was falsified, a context episode ended, or a newer atom
  replaces an older one
- After writing any new memory atom (the header `**Type**`,
  `**Status**`, `**Created on**` must be present)

**Do not run** for pure chit-chat, one-shot trivia with no ongoing
value, when nothing durable appeared, or when the user declared
**sealed session**.

Also run when the user explicitly asks to fill/save memory.

## Scope rules

| Target                                          | Write behavior                                      |
| ----------------------------------------------- | --------------------------------------------------- |
| `topics/<active>/memory/*` (incl. nested child) | **Auto-write** clear items; report paths written    |
| Lifecycle marks on topic-local files            | **Auto-update** when clearly warranted              |
| Active `topic.md` status / Related links        | **Auto-update** Current status; Related short       |
| Root `memory/*` (including lifecycle)           | **Propose → confirm** (unless globally approved)    |
| High-risk content in any location               | **Propose → confirm** with claim, type, path        |
| Deletes / overwrite of important decisions      | **Always confirm**                                  |
| Uncertain type or scope                         | Ask which type, or propose before write             |
| `inbox/` resumes fully promoted or routed       | Delete the inbox file after content lands           |
| Meaningful work with **no** topic home          | Auto-write a short `inbox/` session resume          |
| New memory atom header                          | **Must include** the standard header on every write |

High-risk content includes health claims, credentials, raw
financial/account data, legal or administrative records, and similarly
consequential personal data. Do not auto-write a sensitive orphan-
session resume. Ordinary low-risk topic-local extraction stays
automatic.

## Granularity (entity dossiers)

Default unit is an **entity dossier**, not one field per file.

- **Multi-bullet OK** — one file per stable entity (a person, product,
  project, cost baseline, strategy stack).
- **topic.md first** — if Current status already carries it for session
  use, skip a new atom unless it is stable reference future sessions
  need without re-deriving.
- **Append / update the same entity** before creating a parallel file
  on the same subject.
- **One active strategy decision** per topic thread; orthogonal choices
  stay separate files.
- **Append-first** — new file only for a new entity or a reversed
  decision. No per-session file-count cap.
- **Related list short** — canonical notes + open work + a few key
  dossiers; not every atom.
- Micro-atoms only when truly orthogonal and unlikely to merge (rare).

## Writing form

New/updated atoms follow `MARKDOWN.md` (prose ≤80 cols; pad tables;
tables not wrapped to 80).

## Process

1. Identify the **active topic** (or root-only if meta/global). If it
   is a nested child, that child is the write target; also refresh the
   hub `topic.md` one-liner when the child's current status changed.
2. List durable candidates; skip ephemeral reasoning and full chat
   dumps.
3. **Collapse** candidates into entities / strategy / orthogonal
   decisions before classifying.
4. Classify each into exactly one type:

| Folder         | Meaning                                    |
| -------------- | ------------------------------------------ |
| `facts/`       | Objectively true or strongly believed true |
| `preferences/` | How the user likes things done or valued   |
| `decisions/`   | Choices deliberately made                  |
| `assumptions/` | Treated as true but not proven             |
| `lessons/`     | Learned from experience                    |
| `context/`     | Temporary / situational background         |

5. Prefer **topic-local** paths when working inside a topic (the child
   if active is nested); hub for cross-cutting; root only if clearly
   global.
6. Filenames: `YYYY-MM-DD-short-kebab.md`. Prefer entity names over
   field names.
7. For decisions: date, rationale, optional "Revisit if".
8. New memory files: include `**Status**: active` near the top (after
   title).
9. **Lifecycle pass** (same run):

   - New atom replaces an old one → write new file; set old to
     `**Status**: superseded` + `**Superseded by**: \`path\``
   - Episode ended with no replacement → `**Status**: closed` +
     `**Closed**: YYYY-MM-DD — reason`
   - Unsure whether to close/supersede → ask one short question, or
     leave active

10. Apply the **risk gate**: high-risk candidates are proposed even
    when local.
11. **Write** low-risk topic-local files; **propose** root/high-risk
    files.
12. Update `topic.md`: **Current status** is mandatory; Related stays
    short and active-only.
13. Tell the user briefly what was saved / closed / superseded (bullet
    paths). Do not dump full file bodies unless asked.

## Wind-down check

After meaningful work, if lifecycle changes are ambiguous, ask one
line:

> Anything to close or supersede?

Skip the question when the discussion already made it obvious (then
just do it and report).

## Inbox session resume (orphan / off-topic)

If the session produced useful substance but **no** active topic
absorbed it via the steps above:

1. If it is high-risk, propose a destination/resume first; do not
   auto-write.
2. Otherwise write `inbox/YYYY-MM-DD-short-kebab.md` using the
   template in `inbox/README.md`.
3. Tags + resume bullets + seeds only — **not** a transcript.
4. Link prior related inbox resumes under Related inbox.
5. Report the path in the same brief "what was saved" line.

Skip when extract already wrote under `topics/<name>/` for that whole
thread, or when the user declared **sealed session**.

## Rules

- Never auto-persist entire conversations (inbox resumes are short
  summaries).
- Prefer focused entity dossiers over chat dumps and over micro-atom
  floods.
- Prefer new dated files + supersede when a decision **reverses**; for
  same-entity fact updates, append/edit the dossier or supersede with
  one replacement.
- Missing Status on old files = treat as **active** until marked
  otherwise.
- `active` means lifecycle-current, not verified, approved, executed,
  or successful.
- If active memory and `topic.md` contradict, surface and align the
  invalid current state before extracting more dependent knowledge.
- Do not load superseded/closed into reasoning unless history is
  requested.
- If nothing is worth saving, say so in one line (no empty ceremony).
- Do not invent parallel workflows — this skill is the memory write
  path.
