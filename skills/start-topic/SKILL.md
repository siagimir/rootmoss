---
name: start-topic
description: Create a new well-structured topic under topics/ — top-level or
a child under an existing hub — when a subject needs its own ongoing home.
Propose first; never create silently.
---

# start-topic

## When to use

- User explicitly wants a new topic, **or**
- Topic routing in `AGENTS.md` says a new topic should be proposed and the
  user confirmed

## When not to use

- One-off question with no expected multi-session state
- Short finite plan the user prefers to keep in `inbox/`
- Subject already fits an existing `topics/*` folder or a **listed child**
  → switch there instead
- Subject is a slice of an existing hub (e.g. a condition under a
  `health` hub) → propose a **child**, not a sibling
- Meta work on this system → use `topics/personal-os`
- Global identity/preferences only → root `memory/`, no topic

## Process

0. List top-level `topics/` **and** children on any matching hub
   `topic.md`. If one fits, switch; do not create a duplicate.
1. **Scan `inbox/`** for open resumes/dumps whose tags or title match the
   proposed subject. Read them before drafting `topic.md` — they are the
   prior conversation substance.
2. Propose a short kebab-case folder name and one-line purpose. If it
   belongs under a hub, propose the **child path** (e.g.
   `topics/<hub>/conditions/<name>/`). Wait for confirmation unless the
   user already named it.
3. Create the same scaffold at the chosen path (top-level or nested):

   ```text
   topics/<name>/                  # or topics/<hub>/conditions/<name>/
   ├── topic.md
   ├── notes/
   └── memory/
       ├── facts/
       ├── preferences/
       ├── decisions/
       ├── assumptions/
       ├── lessons/
       └── context/
   ```

4. Write a useful initial `topic.md` containing:

   - Title / short description
   - Why it matters to the user
   - Current status (include outcomes folded from inbox resumes)
   - Open questions
   - Links to any relevant existing memory (hub, root, or other topics)

5. If this is a child: add it to the **hub** `topic.md` child index. If
   the repo keeps a topic registry (a `Topics:` bullet on
   `topics/personal-os/topic.md`), add the kebab name there.
6. **Fold inbox seeds**: turn low-risk durable bullets into topic-local
   memory (and a note if the narrative is long). High-risk health,
   credential, account, legal/admin or similarly consequential content
   is propose-first. Then **delete** inbox files after approved content
   lands (promoted staging — no duplicates).
7. Confirm the structure with the user and continue working inside the
   new topic (read hub then child `topic.md` on later turns).

## Rules

- **Propose → confirm → create** — never silently mkdir a topic.
- Topic-local `memory/` uses the **same six types** as root `memory/`.
- Prefer topic-local memory for topic-specific items; hub for
  cross-cutting; root for global ones.
- Filenames: `YYYY-MM-DD-short-kebab.md`.
- Matching `inbox/` resumes are first-class input — do not start a blank
  topic when prior resumes exist.
- High-risk persistence follows `AGENTS.md` even when the new topic is
  local.
