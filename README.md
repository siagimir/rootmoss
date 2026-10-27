# Rootmoss

**A personal knowledge framework** — a Markdown folder tree that holds
your memories, plus an agent contract that teaches any AI coding agent
to work with them. Clone it, introduce yourself, and start building
your own topics.

- **Source of truth**: Markdown files on your disk — no vendor lock-in
- **Orchestration**: [OpenCode](https://opencode.ai) — or any agent
  that reads `AGENTS.md`
- **Human UI**: [Obsidian](https://obsidian.md) or any Markdown editor
- **Models**: replaceable; your memory outlives them

> Status: **experimental / early**. The name and logo are not covered
> by the license.

## What you get

| Piece                | What it does for you                           |
| -------------------- | ---------------------------------------------- |
| `AGENTS.md`          | The contract your agent reads at session start |
| `FIRST-TIME-HERE.md` | Full tour: concepts, FAQ, first steps          |
| `USER.md`            | Your thin profile — the agent's starting point |
| `memory/<6 types>/`  | Typed folders: facts, preferences, decisions,  |
|                      | assumptions, lessons, context                  |
| `inbox/`             | Staging for chats that fit no topic yet        |
| `topics/`            | One folder per life subject, each `topic.md`   |
| `skills/`            | Portable procedures your agent follows         |
| `topics/plants/`     | A fictional demo topic showing the pattern     |

## Prerequisites

- [OpenCode](https://opencode.ai/v2/docs) — about 5 minutes to install
- `git`
- Optional: [Obsidian](https://obsidian.md) opening this folder

First run takes about **15 minutes**.

## Quickstart

1. Click **Use this template** → create your own **private** repo.
2. Clone it:

   ```bash
   git clone <your-repo-url> rootmoss
   cd rootmoss
   ```

3. Install OpenCode (pick one):

   ```bash
   brew install anomalyco/tap/opencode-v2   # macOS (recommended)
   npm install -g @opencode/cli             # any platform
   curl -fsSL https://opencode.ai/v2/install | bash   # Linux/macOS
   ```

4. Start it **from inside the folder**: `opencode`
5. Paste your first message:

   ```text
   Read AGENTS.md and FIRST-TIME-HERE.md. Then interview me one
   question at a time to fill in USER.md, and propose my first topic
   based on what I tell you.
   ```

Then work through `FIRST-TIME-HERE.md` — folders, memory types, and the
rules your agent follows.

## Who this is not for

- You want a polished app with accounts and sync — this is a folder.
- You will never open a terminal — try Obsidian on it first and see.

## Support

Experimental. "Where did I get stuck?" issues are the most welcome
contribution; responses are best-effort, not guaranteed.

## License

[MIT](LICENSE) — code and prose. The Rootmoss **name and logo** are not
covered by the license; please don't publish confusingly similar
derivatives under this name.
