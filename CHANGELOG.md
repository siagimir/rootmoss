# Changelog

Notable changes to the Rootmoss template. Versions follow `0.x`
(minor = new content or skills, patch = fixes) until the agent
contract stabilizes at 1.0.

Your copy never updates itself — to see whether an update is worth
pulling, read the entries below, then follow `FIRST-TIME-HERE.md` §8.
To be emailed per release: **Watch** the repo → *Custom* → *Releases*.

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
