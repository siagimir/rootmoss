# First time here?

Welcome — the guided tour. It takes ~15 minutes now and saves hours of
"where do I put this?". **Read it straight through — it assumes
nothing is installed** (§9 is the no-install path). If you would
rather start by installing, do the five steps in `README.md` §
Quickstart and come back; either order works.

## 1. What this is (90 seconds)

Rootmoss is a **folder of Markdown files** that an AI agent helps you
grow. Three ideas:

1. **Your disk is the source of truth.** Every memory is a file you
   own; any model, agent or editor can read it. Nothing lives only
   inside a chat. One honest caveat: when your agent reads a note,
   that text goes to the model you connected — exactly as it would
   in any AI chat. Your folder stays put; the words it reads travel.
2. **Memories are typed.** A fact is not a preference is not a
   decision. Six folders keep them apart so they stay useful.
3. **Topics are folders.** Each life subject gets `topics/<name>/` with
   a `topic.md` dashboard. The agent proposes new topics; you approve
   them.

## 2. Folder map

```text
rootmoss/
├── AGENTS.md              # contract your agent reads at session start
├── FIRST-TIME-HERE.md     # this file
├── README.md              # quickstart
├── USER.md                # your thin profile — edit first
├── MARKDOWN.md            # writing style rules
├── opencode.json          # agent permissions for this folder
├── inbox/                 # session resumes with no topic home
├── memory/                # typed, durable memory (root level)
│   ├── facts/             #   objectively true
│   ├── preferences/       #   how you like things done
│   ├── decisions/         #   deliberate choices
│   ├── assumptions/       #   treated as true, unproven
│   ├── lessons/           #   learned from experience
│   └── context/           #   temporary background
├── skills/                # procedures your agent follows
└── topics/                # one folder per life subject
    ├── personal-os/       # meta: the system itself
    └── plants/            # fictional demo (delete when ready)
```

## 3. What to edit first

1. `USER.md` — replace the placeholders. Or let the agent interview you
   (paste the README's first message).
2. Optionally delete `topics/plants/` once you've looked at it.
3. That's it — the agent asks before editing anything else.

## 4. Glossary

| Term           | Meaning                                         |
| -------------- | ----------------------------------------------- |
| topic          | A folder under `topics/` for one life subject   |
| topic.md       | The topic's dashboard: status, links, current   |
|                | state — read it first when working in a topic   |
| typed memory   | The six `memory/` types; each file declares its |
|                | `Type` and `Status` in a header                 |
| lifecycle      | `active` → `superseded` (replaced) / `closed`   |
|                | (done). Stale memory is marked, not deleted     |
| inbox          | Staging area for chats with no topic home       |
| skill          | A procedure under `skills/` the agent loads     |
|                | when a task matches                             |
| AGENTS.md      | Instructions every agent session reads first    |
| entity dossier | One memory file holding several bullets about   |
|                | a single person/project — beats tiny files      |

## 5. Where do I put X?

| You have…                                  | Put it in                            |
| ------------------------------------------ | ------------------------------------ |
| Something objectively true about your life | `memory/facts/`                      |
| "I like X done this way"                   | `memory/preferences/`                |
| A choice you made on purpose               | `memory/decisions/`                  |
| A hunch you can't prove (yet)              | `memory/assumptions/`                |
| "Tried X, didn't work because Y"           | `memory/lessons/`                    |
| "Right now I'm in phase Z"                 | `memory/context/` — or the topic's   |
|                                            | `topic.md` if it's session-critical  |
| An ongoing subject (health, piano, cars)   | `topics/<name>/` — agent proposes it |
| A chat with nowhere to put it              | `inbox/` (resume, then route)        |
| Anything web-sourced                       | an `assumption` or note **with a     |
|                                            | source** — never a bare fact         |

## 6. How your agent behaves (AGENTS.md in plain words)

- It reads `USER.md`, recent `context/`, the inbox index and the active
  `topic.md` at session start.
- After a meaningful topic discussion it **automatically** writes short
  durable memories (topic-local). Root-level `memory/` writes are
  proposed first; you confirm.
- High-risk material (health, credentials, money records) is
  confirm-first, everywhere.
- It never dumps whole conversations into memory — durable atoms only.
- It marks old memories `superseded` / `closed` instead of deleting.
- Its permission floor is a **file, not a promise**: `opencode.json`
  sets `edit: ask`, `bash: ask` and `webfetch: ask`, and the `research`
  subagent runs with `edit: deny`. It is about twenty lines — read it,
  and change it if you want stricter or looser.
- It commits to git **only when you ask**.
- Anything fetched from the web is **data, never instructions**, and
  lands as an assumption with a source link.

## 7. Demo content policy

`topics/plants/` is a **fictional** topic (a fake person's plant notes)
showing what a grown topic looks like: a `topic.md` dashboard plus a few
example memory atoms. Read it, then ask your agent to clear it away
when you create your first real topic:

> Delete `topics/plants/` for me.

It confirms before it removes anything — that is the contract, not a
convention, and watching it ask is the fastest way to see it work.
(Deleting it yourself works too: `rm -r topics/plants`.)

The seed file `memory/context/2026-10-27-this-is-a-template.md` can go
the same way after your first real memory.

## 8. Growing and upgrading

- Your repo is a **snapshot** of the template — it does not
  auto-update. Check `CHANGELOG.md` (and the repo's Releases) to see
  whether anything new is worth pulling.
- To pull template updates later, add the template as a second remote
  and merge what you want:

```bash
git remote add template https://github.com/siagimir/rootmoss.git
git fetch template
git merge template/main --no-commit   # review before committing
```

- Your `USER.md`, memories and topics are yours. Conflicts will be in
  shared files (like this one) — keep your versions where they differ.

## 9. Look-first path (no install)

Prefer to just look? Open `topics/plants/topic.md` and a couple of
`memory/` files to see the shape. Nothing here expires — install later.

## 10. Who this is not for

- You want a polished app with accounts and sync — this is a folder.
- You never want to set anything up — daily use can be terminal-free
  (desktop app or web), but the first setup needs about 15 minutes of
  someone technical's time.

## 11. Feedback

Stuck somewhere? Open an issue describing **where** you got stuck —
confusion reports are the most useful contribution to a template.

## License

[MIT](LICENSE). The Rootmoss name and logo are not covered by it.
