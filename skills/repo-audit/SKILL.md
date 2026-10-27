---
name: repo-audit
description: Whole-repository consistency check against the Rootmoss
structure (AGENTS.md shape) — all topics/skills, dashboards, links,
lifecycle, inbox, root context. Not domain claim validation. Run on
"audit" or after big sessions.
---

# repo-audit

## When to use

- User: "audit", "cleanup check", "repo health", "consistency", "check
  the whole tree"
- After a large burst of new topics/memory/skills
- Periodically (e.g. monthly) to catch drift

## When not to use

- Memory extract after one chat → `extract-memory`
- Creating topics → `start-topic`

## Stance

**Whole-repo structural hygiene and current-state consistency** vs
`AGENTS.md` conventions. Not domain expertise or external claim
validation. Flag; fix only clear safe issues. Propose larger
merges/deletes.

**Must catch:** `AGENTS.md` saying one operative rule while an
**active** root decision/preference says another. That is a
first-class fail — not a "nice semantic extra".

## Checklist

### 1. Tree shape

- [ ] Every `topics/*/` has `topic.md`
- [ ] Any nested directory that looks like a topic (contains `notes/`
      or `memory/`) has its own `topic.md`
- [ ] Every folder with `SKILL.md` under `skills/` is a skill (nested
      OK)
- [ ] Skills named in `AGENTS.md` ("Core skills") match discovered
      skill ids
- [ ] `inbox/`: only README and/or intentional **open** resumes/dumps
      (note stranded or stale open files; promoted should be deleted)

### 2. Per topic (changed / mature unless user asks full)

- [ ] `topic.md` has: Why, Current status, Open questions, Related,
      Scope
- [ ] Current status matches **active** decision/context files (not
      superseded-as-current)
- [ ] No material contradiction between dashboard state and active
      memory
- [ ] Related links resolve; Related stays **short** (soft warn ≫ ~12
      file links)
- [ ] New/touched memory uses exact lifecycle values; missing old
      `**Status**` stays active but annotated/custom values are flagged
- [ ] Superseded/closed not presented as current without label
- [ ] Obvious type misfile — flag only

### 3. Links

- [ ] From nested `memory/*/` files, relative-to-file paths resolve
- [ ] Broken = path does not resolve from the file's directory **nor**
      from the nearest topic root (walk up to each ancestor
      `topic.md`)
- [ ] Root refs from topics: enough `../` to reach repo-root `memory/`

### 4. Root / AGENTS spot-check

- [ ] **Policy split (required):** for each operative rule stated in
      `AGENTS.md` (memory writes, git, untrusted content, sealed
      session, binaries, topic routing), read the **active** root
      `memory/decisions/` + `memory/preferences/` on that subject
      (ignore `superseded` / `closed`). Same subject = one current
      rule. A split is **FAIL** even if links and dashboards are
      clean.
- [ ] Active `memory/context/` still true (or flag close/supersede)
- [ ] `USER.md` still thin; detail in `memory/facts/`
- [ ] `.gitignore` still covers binaries and secrets
- [ ] No secrets in tracked files (quick sanity)
- [ ] Spot-check files touched since last audit vs `MARKDOWN.md`

### 5. Output

Write: `topics/personal-os/notes/YYYY-MM-DD-repo-audit.md`

| Section             | Content                                              |
| ------------------- | ---------------------------------------------------- |
| Summary             | structural pass/fail + semantic spot-check result    |
| Policy split        | PASS/FAIL per subject in §4 (required)               |
| Fixed this run      | list                                                 |
| Needs user decision | merges, deletes, stale context, bulk Status backfill |
| Topic scores        | one line each                                        |
| Skills / tree       | match tables                                         |

### 6. Remediate

| Issue                       | Action                                                       |
| --------------------------- | ------------------------------------------------------------ |
| Broken link                 | Fix path                                                     |
| Skills list drift           | Update `AGENTS.md`                                           |
| Related too long            | Trim topic.md Related                                        |
| Stale Current status        | Align with active decisions                                  |
| Superseded still "current"  | Annotate or drop from Related                                |
| Dashboard-memory conflict   | Align current state; close/supersede stale operative file    |
| AGENTS vs active memory     | Surface split; propose which side wins; do not silently pick |
| Noncanonical new Status     | Normalize exact lifecycle value                              |
| Missing Status on old atoms | **Propose** bulk backfill — do not mass-edit unless asked    |
| Merge/delete candidates     | **Propose only**                                             |

Do not bulk-delete memory. Do not invent domain corrections.

## Helper scripts (deterministic, no LLM)

Optional fast structural scan — run before the full LLM audit:

```bash
python3 skills/repo-audit/scripts/audit_structural.py
python3 skills/repo-audit/scripts/audit_structural.py --json /tmp/audit.json
python3 skills/repo-audit/scripts/check_links.py
python3 skills/repo-audit/scripts/check_status.py
python3 skills/repo-audit/scripts/check_inbox.py
python3 skills/repo-audit/scripts/check_memory_headers.py
```

Output is safe, read-only, stdlib Python. The LLM still writes the
final dated note and handles semantic checks.

## Recommended hybrid workflow (credit saving)

1. Run the deterministic scripts first — fast, local, zero tokens.
2. Feed the JSON/Markdown outputs into the LLM session.
3. LLM only does **policy split** + semantic checks on changed or
   mature topics. Write the dated audit note; propose decisions.
4. Re-run scripts after fixes to confirm.

Do not add audit agents or new linters until the same gap hurts twice.

## Related

- `AGENTS.md` — constitution
- `skills/extract-memory/SKILL.md` — entity dossiers, Related short
- `skills/markdown-style/SKILL.md` — raw MD form
- `MARKDOWN.md` — style guide
