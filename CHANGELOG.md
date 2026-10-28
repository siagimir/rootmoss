# Changelog

Notable changes to the Rootmoss template. Versions follow `0.x`
(minor = new content or skills, patch = fixes) until the agent
contract stabilizes at 1.0.

Your copy never updates itself — to see whether an update is worth
pulling, read the entries below, then follow `FIRST-TIME-HERE.md` §8.
To be emailed per release: **Watch** the repo → *Custom* → *Releases*.

## v0.1.8 — 2026-10-28

Evidence-driven fixes from a 126-session simulated persona study plus
two independent expert reviews (see the personal-os topic note for the
full write-up). Three P0s and two P1s:

- **Show the enforcement.** The #1 objection across both study waves
  was that the safety guarantees are prose in `AGENTS.md` with nothing
  behind them — and `opencode.json` was named in the folder map but
  never opened anywhere in the funnel. It is now in the landing-page
  folder tree (`# what it may do without asking`), in README's *What
  you get* table with its real values, and in the tour §6 as a
  twenty-line file you are invited to read and change.
- **Say where the text goes.** *"Nothing leaves your disk"* was
  retired by v0.1.7, but no replacement sentence explained transit.
  One honest line now appears in all three docs: when the agent reads
  a note, that text goes to the model you connected — the folder
  stays put, the words it reads travel.
- **Split the door from the room (Path B).** The non-IT segment's
  dominant objection was that the page promises *"just a folder,
  Finder is enough"* and then arrives at GitHub, git and a one-line
  installer. Path B now states who does what: steps 1–4 once by
  someone technical, step 5 is yours, after that a bookmark. README's
  Quickstart opens with the same split.
- **Stop handing `rm -r` to an agent.** The tour told you to run
  `rm -r topics/plants` while the page sold write-safety — noticed
  unprompted by two respondents. It now asks your agent to remove it
  and confirms first, which also demonstrates the claim. The manual
  command remains as a parenthetical.
- **End the Tour ↔ README bounce.** The tour opened by sending you to
  the README, whose quickstart ends by sending you back to the tour.
  The tour now says it can be read straight through with nothing
  installed, and the README order is optional rather than recursive.

## v0.1.7 — 2026-10-27

- Honest storage claims (backed by a storage threat-model study):
  dropped the absolute **"never in a vendor's cloud"** — a private
  repo is hosted too. README now says memories stay on your disk and
  never get **locked inside a chat vendor's memory**; quickstart
  explains what "private" means and to keep raw sensitive documents
  out of any cloud repo. Promo site: card 05 retitled **"Nothing
  phones home"** (the guarantee the software actually makes);
  quickstart step 01 carries the same one-liner.

- README: new **"Storage is your choice"** section — hosting, backup
  and encryption are the user's decisions; the **3-2-1** rule with a
  link. `privacy.html` § The software itself mirrors the scope
  sentence.

## v0.1.6 — 2026-10-27

- README hero: ownership sub-line **"Your memories, in files you
  own."** — mirrors the promo site after the two-model headline
  experiment (credibility champion across all panels).

## v0.1.5 — 2026-10-27

- README: first screen gains the **AGENTS.md template** phrasing and a
  link to the landing page (search + preview copy).

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
