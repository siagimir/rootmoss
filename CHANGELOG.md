# Changelog

Notable changes to the Rootmoss template. Versions follow `0.x`
(minor = new content or skills, patch = fixes) until the agent
contract stabilizes at 1.0.

Your copy never updates itself — to see whether an update is worth
pulling, read the entries below, then follow `FIRST-TIME-HERE.md` §8.
To be emailed per release: **Watch** the repo → *Custom* → *Releases*.

## v0.1.5 — 2026-10-27

- README: first screen gains the **AGENTS.md template** phrasing and a
  link to the landing page (search + preview copy).

## v0.1.5 — 2026-10-27

- README hero: ownership sub-line **"Your memories, in files you
  own."** — mirrors the promo site after the two-model headline
  experiment (credibility champion across all panels).

## v0.1.4 — 2026-10-27

- README quickstart: **desktop app** and **web** options alongside
  the terminal; **Download ZIP** for non-git users; prerequisites
  match the terminal-free-daily-use story.

## v0.1.3 — 2026-10-27

- README + tour: honest run paths — OpenCode as **terminal, desktop
  app or web**; daily use can be terminal-free (desktop app or web),
  one-time setup still needed. Finder-first viewing; Obsidian/Zed
  explicitly optional, not the interface.

## v0.1.2 — 2026-10-27

- README: new hero + value framing — memory that doesn't reset, on
  your disk or private git repo, never in a vendor's cloud.

## v0.1.1 — 2026-10-27

- README: "Updates" section — how to watch releases for email
  notification and check the changelog before pulling.

## v0.1.0 — 2026-10-27

First public release.

- **Typed memory**: six folders (facts, preferences, decisions,
  assumptions, lessons, context) with mandatory `Type` / `Status` /
  `Created on` headers and the `active` → `superseded` / `closed`
  lifecycle.
- **Topic system**: one folder per life subject with a `topic.md`
  dashboard, hub/child routing, propose-before-create rule.
- **Agent contract**: `AGENTS.md` — session-start reading order,
  memory write policy (topic-local auto, root confirm, high-risk
  always confirm), untrusted-web-content rules, git only on request.
- **Skills**: `start-topic`, `extract-memory`, `repo-audit` (+ six
  deterministic audit scripts), `markdown-style` (+ formatter),
  `untrusted-research`.
- **Onboarding**: README quickstart, `FIRST-TIME-HERE.md` tour,
  inbox staging with resume template, fictional `plants` demo topic.
- **Config**: minimal `opencode.json` (permissions + locked-down
  research subagent).
- MIT license; the Rootmoss name and logo are excluded from it.
